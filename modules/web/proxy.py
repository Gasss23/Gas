"""Proxy filtrante per il browser senza schermo (R6, fetta 32, chat Mani).

Il browser (modules/web/browser.py, fetta 33) esce in rete SOLO da qui: ogni richiesta
della pagina (documento, immagini, script, redirect) passa le stesse regole di leggi_pagina.

Regole (fail-safe, CLAUDE.md §9):
  - ascolta solo su 127.0.0.1, porta scelta dal sistema;
  - http in chiaro: solo GET e HEAD in forma assoluta («GET http://host/... HTTP/1.1»),
    niente corpo; https: solo CONNECT verso la porta 443;
  - host, schema e porta validati da leggi._valida_url (solo 80 e 443, niente
    credenziali, niente localhost); il nome si risolve QUI e ci si collega all'IP
    controllato (niente indirizzi interni, niente DNS rebinding);
  - niente «Upgrade» (WebSocket in chiaro); le intestazioni hop-by-hop, Proxy-* e quelle
    nominate in «Connection» non passano, l'Host lo scrive il proxy;
  - la testa della risposta http si riscrive con «Connection: close» (R-585-4): il browser
    non riusa la connessione, quindi un server non può far arrivare una seconda risposta
    come se fosse quella della richiesta successiva (anche verso un altro sito);
  - tetti: richieste, byte in tutto, durata, connessioni contemporanee, testa della
    richiesta; superato un tetto la connessione si chiude;
  - un rifiuto è una risposta 403 col motivo scritto qui (mai preso dalla pagina), con
    «X-Gas-Proxy: rifiuto» perché il browser la riconosca, e una riga in `rifiuti`; un
    errore di rete è un 502; mai un'eccezione verso chi chiama.

Limiti dichiarati (review #585): il proxy filtra le DESTINAZIONI, non i dati. Dentro un
tunnel verso 443 passa qualunque cosa (anche un POST cifrato) verso un host pubblico. È
senza autenticazione: un altro processo dello stesso computer può usarlo finché è vivo,
ma ha già la rete diretta (la sandbox di run_command ha una rete sua, --unshare-net).

Zero dipendenze esterne: solo stdlib.
"""
from __future__ import annotations

import ipaddress
import logging
import re
import select
import socket
import socketserver
import threading
import time
from typing import Optional

from modules.web import leggi as _leggi

MAX_RICHIESTE = 200          # richieste (e tunnel) per ogni avvio del proxy
MAX_BYTE_TOTALI = 20_000_000  # byte inoltrati in tutto, nei due versi (teste e «200» comprese)
DURATA = 60.0                # secondi di vita del proxy dopo avvia()
MAX_CONNESSIONI = 16         # connessioni contemporanee dal browser
MAX_TESTA = 16_384           # byte della testa di una richiesta
MAX_TESTA_RISPOSTA = 65_536  # byte della testa di una risposta http
MAX_INTERMEDIE = 5           # risposte 1xx prima di quella vera
TIMEOUT_INATTIVITA = 10.0    # secondi senza dati su una connessione
MAX_RIFIUTI = 100            # motivi tenuti in memoria

_METODI = frozenset({"GET", "HEAD"})
_SALTO = frozenset({"connection", "keep-alive", "proxy-connection", "proxy-authorization",
                    "proxy-authenticate", "te", "trailer", "transfer-encoding", "upgrade", "host"})
_SALTO_RISPOSTA = frozenset({"connection", "keep-alive", "proxy-connection", "upgrade", "te",
                             "trailer", "x-gas-proxy"})  # R-593-3: il segno è solo del proxy
_OK_TUNNEL = b"HTTP/1.1 200 Connection established\r\n\r\n"
_FINE_TESTA = re.compile(rb"\r?\n\r?\n")
_RIGA_STATO = re.compile(r"HTTP/1\.[01] ([1-5][0-9]{2})(?: [^\x00-\x08\x0a-\x1f\x7f]*)?")
_PORTA_TUNNEL = re.compile(r"[0-9]{1,5}")
_NOME_INTESTAZIONE = re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+")

log = logging.getLogger("gas.web.proxy")


def _intestazioni(righe: list, motivo: str) -> list:
    """Coppie (nome, valore); una riga malformata o con caratteri di controllo è un rifiuto."""
    intestazioni = []
    for riga in righe:
        nome, sep, valore = riga.partition(":")
        if not sep or not _NOME_INTESTAZIONE.fullmatch(nome) or any(
                ord(c) < 0x20 and c != "\t" or ord(c) == 0x7F for c in valore):
            raise _leggi._Rifiuto(motivo)
        intestazioni.append((nome, valore.strip()))
    return intestazioni


def _senza_salto(intestazioni: list, salto: frozenset) -> list:
    """Toglie le hop-by-hop, le Proxy-* e quelle nominate in «Connection» (V-4 bot #312)."""
    nominate = {t.strip().lower() for nome, valore in intestazioni
                if nome.lower() in ("connection", "proxy-connection") for t in valore.split(",")}
    return [(n, v) for n, v in intestazioni
            if n.lower() not in salto and n.lower() not in nominate
            and not n.lower().startswith("proxy-")]


class ProxyFiltrante:
    """Uso: `with ProxyFiltrante() as p: porta = p.porta` (o avvia()/ferma())."""

    def __init__(self, *, max_richieste: int = MAX_RICHIESTE, max_byte: int = MAX_BYTE_TOTALI,
                 durata: float = DURATA, _risolvi: Optional[_leggi.Risolutore] = None,
                 _connetti: Optional[_leggi.Connettore] = None) -> None:
        self.max_richieste = max_richieste
        self.max_byte = max_byte
        self.durata = durata
        self._risolvi = _risolvi or _leggi._risolvi_dns
        self._connetti = _connetti or _leggi._connetti_tcp
        self._lock = threading.Lock()
        self._posti = threading.BoundedSemaphore(MAX_CONNESSIONI)
        self._server: Optional[socketserver.ThreadingTCPServer] = None
        self._aperte: set[socket.socket] = set()
        self._scadenza = 0.0
        self.porta = 0
        self.richieste = 0
        self.byte = 0
        self.rifiuti: list[str] = []

    # ───────────────────────── vita del proxy ─────────────────────────

    def avvia(self) -> int:
        proxy = self

        class _Gestore(socketserver.BaseRequestHandler):
            def handle(self) -> None:
                proxy._gestisci(self.request)

        srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), _Gestore)
        srv.daemon_threads = True
        self._server = srv
        self._scadenza = time.monotonic() + self.durata
        self.porta = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05},
                         name="gas-web-proxy", daemon=True).start()
        return self.porta

    def ferma(self) -> None:
        """Ferma l'ascolto e chiude anche le connessioni e i tunnel ancora aperti (R-585-3)."""
        srv, self._server = self._server, None
        if srv is not None:
            srv.shutdown()
            srv.server_close()
        with self._lock:
            self._scadenza = 0.0
            aperte, self._aperte = list(self._aperte), set()
        for s in aperte:
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

    def __enter__(self) -> "ProxyFiltrante":
        self.avvia()
        return self

    def __exit__(self, *_: object) -> None:
        self.ferma()

    # ───────────────────────── una connessione ─────────────────────────

    def _gestisci(self, client: socket.socket) -> None:
        if not self._posti.acquire(blocking=False):
            self._rifiuta(client, 503, "troppe connessioni contemporanee")
            return
        risposto = [False]
        self._registra(client)
        try:
            client.settimeout(TIMEOUT_INATTIVITA)
            self._servi(client, risposto)
        except _leggi._Rifiuto as r:
            if not risposto[0]:
                self._rifiuta(client, 403, r.motivo)
            else:
                self._annota(r.motivo)
        except Exception as e:  # noqa: BLE001 — §9: nessun errore esce dal proxy
            log.warning("proxy web: errore %s", type(e).__name__)
            if not risposto[0]:
                self._rifiuta(client, 502, "errore di rete o di protocollo")
        finally:
            self._togli(client)
            self._posti.release()

    def _servi(self, client: socket.socket, risposto: list) -> None:
        metodo, bersaglio, intestazioni = self._leggi_richiesta(client)
        self._conta_richiesta()
        nomi = {nome.lower() for nome, _ in intestazioni}
        if "upgrade" in nomi:
            raise _leggi._Rifiuto("upgrade non permesso (WebSocket)")
        if metodo == "CONNECT":
            self._tunnel(client, bersaglio, risposto)
            return
        if metodo not in _METODI:
            raise _leggi._Rifiuto("metodo non permesso: solo GET e HEAD")
        if "transfer-encoding" in nomi or any(
                nome.lower() == "content-length" and valore.strip() != "0"
                for nome, valore in intestazioni):
            raise _leggi._Rifiuto("corpo della richiesta non permesso")
        schema, host, porta, percorso, _ = _leggi._valida_url(bersaglio)
        if schema != "http":
            raise _leggi._Rifiuto("https solo attraverso CONNECT")
        host_header = f"[{host}]" if ":" in host else host
        if porta != 80:
            host_header += f":{porta}"
        righe = [f"{metodo} {percorso} HTTP/1.1", f"Host: {host_header}"]
        righe += [f"{nome}: {valore}" for nome, valore in _senza_salto(intestazioni, _SALTO)]
        righe.append("Connection: close")
        testa = ("\r\n".join(righe) + "\r\n\r\n").encode("latin-1")
        # V-1 bot #312: anche la testa inoltrata conta; R-590-2: contata prima di aprire.
        self._conta_byte(len(testa))
        remoto = self._apri(host, porta)
        try:
            self._invia(remoto, testa)
            self._risposta(remoto, client, risposto)
            self._pompa(remoto, client)
        finally:
            self._togli(remoto)
            remoto.close()

    def _tunnel(self, client: socket.socket, bersaglio: str, risposto: list) -> None:
        host, sep, porta_txt = bersaglio.rpartition(":")
        if not sep or not host or not _PORTA_TUNNEL.fullmatch(porta_txt) or any(
                c in bersaglio for c in "/?#\\"):
            raise _leggi._Rifiuto("richiesta non valida")
        if int(porta_txt) != 443:
            raise _leggi._Rifiuto("tunnel solo verso la porta 443")
        _, host_valido, porta, _, _ = _leggi._valida_url(f"https://{bersaglio}/")
        # Review #585: la porta del tunnel è quella che urlsplit ha letto, non il testo.
        if porta != 443:
            raise _leggi._Rifiuto("tunnel solo verso la porta 443")
        remoto = self._apri(host_valido, porta)
        try:
            self._conta_byte(len(_OK_TUNNEL))  # V-2 bot #312 su 805b4d8: anche il «200» conta
            risposto[0] = True
            self._invia(client, _OK_TUNNEL)
            self._pompa(remoto, client, client_a_remoto=True)
        finally:
            self._togli(remoto)
            remoto.close()

    # ───────────────────────── pezzi ─────────────────────────

    def _leggi_richiesta(self, client: socket.socket) -> tuple:
        # Review #585 (R-585-2): la testa ha un tempo massimo in tutto, non per ogni pezzo.
        scadenza = min(self._scadenza, time.monotonic() + TIMEOUT_INATTIVITA)
        motivo = ("tempo massimo del proxy superato" if scadenza == self._scadenza
                  else "connessione inattiva")
        dati = b""
        while b"\r\n\r\n" not in dati:
            if len(dati) > MAX_TESTA:
                raise _leggi._Rifiuto("richiesta troppo grande")
            rimasto = scadenza - time.monotonic()
            if rimasto <= 0:
                raise _leggi._Rifiuto(motivo)
            client.settimeout(rimasto)
            try:
                pezzo = client.recv(4096)
            except socket.timeout:  # R-585-6: un 403 col motivo, non un 502
                raise _leggi._Rifiuto(motivo) from None
            if not pezzo:
                raise _leggi._Rifiuto("richiesta non valida")
            dati += pezzo
        client.settimeout(TIMEOUT_INATTIVITA)  # R-586-1: il timeout corto della testa non resta
        testa, _, resto = dati.partition(b"\r\n\r\n")
        if len(testa) > MAX_TESTA:
            raise _leggi._Rifiuto("richiesta troppo grande")
        if resto:  # un corpo (o una seconda richiesta) già in arrivo: non si inoltra
            raise _leggi._Rifiuto("corpo della richiesta non permesso")
        righe = testa.decode("latin-1").split("\r\n")
        parti = righe[0].split(" ")
        if len(parti) != 3 or not parti[2].startswith("HTTP/1."):
            raise _leggi._Rifiuto("richiesta non valida")
        return parti[0], parti[1], _intestazioni(righe[1:], "richiesta non valida")

    def _risposta(self, remoto: socket.socket, client: socket.socket, risposto: list) -> None:
        """R-585-4: inoltra la testa della risposta riscritta, con «Connection: close»; poi il
        corpo passa così com'è fino alla chiusura del server. Le 1xx (non 101) passano prima."""
        dati = b""
        for _ in range(MAX_INTERMEDIE + 1):
            testa, dati = self._testa_risposta(remoto, dati)
            righe = [r.removesuffix("\r") for r in testa.decode("latin-1").split("\n")]
            stato = _RIGA_STATO.fullmatch(righe[0])
            if not stato:
                raise _leggi._Rifiuto("risposta del server non valida")
            codice = int(stato.group(1))
            if codice == 101:
                raise _leggi._Rifiuto("upgrade non permesso (WebSocket)")
            intestazioni = _intestazioni(righe[1:], "risposta del server non valida")
            uscita = [righe[0]] + [f"{n}: {v}" for n, v in _senza_salto(intestazioni, _SALTO_RISPOSTA)]
            if codice >= 200:
                uscita.append("Connection: close")
            pezzo = ("\r\n".join(uscita) + "\r\n\r\n").encode("latin-1")
            self._conta_byte(len(pezzo) + (len(dati) if codice >= 200 else 0))
            risposto[0] = True  # da qui la risposta al browser è quella del server
            self._invia(client, pezzo)
            if codice >= 200:
                if dati:
                    self._invia(client, dati)
                return
        raise _leggi._Rifiuto("troppe risposte intermedie dal server")

    def _testa_risposta(self, remoto: socket.socket, dati: bytes) -> tuple[bytes, bytes]:
        """Legge una testa di risposta (righe chiuse da CRLF o LF, come accetta il browser)."""
        while True:
            fine = _FINE_TESTA.search(dati)
            if fine:
                return dati[:fine.start()], dati[fine.end():]
            if len(dati) > MAX_TESTA_RISPOSTA:
                raise _leggi._Rifiuto("risposta del server troppo grande")
            attesa = min(TIMEOUT_INATTIVITA, self._scadenza - time.monotonic())
            if attesa <= 0:
                raise _leggi._Rifiuto("tempo massimo del proxy superato")
            remoto.settimeout(attesa)
            try:
                pezzo = remoto.recv(65536)
            except socket.timeout:
                raise _leggi._Rifiuto("tempo massimo del proxy superato" if attesa < TIMEOUT_INATTIVITA
                                      else "connessione inattiva") from None
            if not pezzo:
                raise _leggi._Rifiuto("risposta del server non valida")
            dati += pezzo

    def _apri(self, host: str, porta: int) -> socket.socket:
        scadenza = min(self._scadenza, time.monotonic() + 2 * _leggi.TIMEOUT_CONNESSIONE)
        try:
            ipaddress.ip_address(host)
            ips = [host]
        except ValueError:
            ips = _leggi._risolvi_con_tempo(self._risolvi, host, porta, scadenza)
        if any(_leggi.indirizzo_interno(ip) for ip in ips):
            raise _leggi._Rifiuto("indirizzo interno non permesso")
        remoto = self._connetti(ips[0], porta, min(_leggi.TIMEOUT_CONNESSIONE, _leggi._rimasto(scadenza)))
        remoto.settimeout(TIMEOUT_INATTIVITA)
        self._registra(remoto)
        return remoto

    def _pompa(self, remoto: socket.socket, client: socket.socket,
               client_a_remoto: bool = False) -> None:
        """Copia i dati finché un lato chiude, fino ai tetti di byte, durata e inattività."""
        coppie = {remoto: client}
        if client_a_remoto:
            coppie[client] = remoto
        while True:
            attesa = min(TIMEOUT_INATTIVITA, self._scadenza - time.monotonic())
            if attesa <= 0:
                raise _leggi._Rifiuto("tempo massimo del proxy superato")
            pronti, _, _ = select.select(list(coppie), [], [], attesa)
            if not pronti:
                raise _leggi._Rifiuto("connessione inattiva")
            for sorgente in pronti:
                dati = sorgente.recv(65536)
                if not dati:
                    return
                self._conta_byte(len(dati))
                self._invia(coppie[sorgente], dati)

    def _invia(self, s: socket.socket, dati: bytes) -> None:
        """V-2 bot #312: anche un invio verso chi non legge si ferma alla scadenza del proxy."""
        rimasto = self._scadenza - time.monotonic()
        if rimasto <= 0:
            raise _leggi._Rifiuto("tempo massimo del proxy superato")
        s.settimeout(min(TIMEOUT_INATTIVITA, rimasto))
        try:
            s.sendall(dati)
        except socket.timeout:  # R-590-1: il motivo dice chi ha chiuso
            raise _leggi._Rifiuto("tempo massimo del proxy superato" if rimasto < TIMEOUT_INATTIVITA
                                  else "connessione inattiva") from None

    def _registra(self, s: socket.socket) -> None:
        with self._lock:
            self._aperte.add(s)

    def _togli(self, s: socket.socket) -> None:
        with self._lock:
            self._aperte.discard(s)

    def _conta_richiesta(self) -> None:
        with self._lock:
            if time.monotonic() >= self._scadenza:
                raise _leggi._Rifiuto("tempo massimo del proxy superato")
            if self.richieste >= self.max_richieste:
                raise _leggi._Rifiuto("troppe richieste")
            # V-1 bot #312: a tetto superato nessuna richiesta nuova esce (URL e intestazioni).
            if self.byte >= self.max_byte:
                raise _leggi._Rifiuto("troppi byte")
            self.richieste += 1

    def _conta_byte(self, n: int) -> None:
        with self._lock:
            self.byte += n
            if self.byte > self.max_byte:
                raise _leggi._Rifiuto("troppi byte")

    def _annota(self, motivo: str) -> None:
        with self._lock:
            if len(self.rifiuti) < MAX_RIFIUTI:
                self.rifiuti.append(motivo)
        log.info("proxy web: rifiuto (%s)", motivo)

    def _rifiuta(self, client: socket.socket, codice: int, motivo: str) -> None:
        self._annota(motivo)
        corpo = motivo.encode("utf-8")
        frase = {403: "Forbidden", 502: "Bad Gateway", 503: "Service Unavailable"}[codice]
        try:
            client.sendall(f"HTTP/1.1 {codice} {frase}\r\nContent-Type: text/plain; charset=utf-8\r\n"
                           f"Content-Length: {len(corpo)}\r\nX-Gas-Proxy: rifiuto\r\nConnection: close\r\n\r\n".encode()
                           + corpo)
        except OSError:
            pass
