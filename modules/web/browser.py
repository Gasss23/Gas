"""Lettura di una pagina con un browser senza schermo (R6, fetta 33, chat Mani).

Per le pagine che senza JavaScript sono vuote: Chromium senza schermo (Playwright per Node,
come i test della voce) in un processo figlio, che esce in rete SOLO dal proxy filtrante
(modules/web/proxy.py: le regole di leggi_pagina su OGNI richiesta della pagina). È SPENTO per
default: si accende con GAS_WEB_BROWSER=1 (servono node, il pacchetto playwright e Chromium).

Regole (fail-safe, CLAUDE.md §9):
  - rete solo dal proxy, anche per il loopback (`--proxy-bypass-list=<-loopback>`, R-585-5);
    QUIC spento, WebRTC senza UDP fuori dal proxy, niente prefetch né rete di sfondo;
  - spenti nelle pagine e nei frame WebSocket, RTCPeerConnection, notifiche, service worker,
    download, permessi e popup; JavaScript acceso, perché è lo scopo. NON nei Dedicated Worker
    (lo script iniettato lì non vale, e routeWebSocket non li copre): da un worker un wss://
    verso un host pubblico passa dal tunnel 443, come già un fetch https (V-1 ve #315);
  - profilo temporaneo cancellato a ogni lettura, ambiente minimo (niente chiavi di Gas);
  - tempo massimo; alla fine (anche in errore) si uccidono node e tutti i processi di Chromium
    della lettura, riconosciuti da un segno nel loro ambiente (Playwright mette Chromium in una
    sessione sua: il gruppo di node non basta, R-593-1), prima di cancellare il profilo;
  - tetto di memoria per processo (ulimit -d, ereditato da Chromium) e per il motore JavaScript;
  - esce SOLO il testo visibile (innerText) e il titolo, passati nella pulizia di leggi.py e
    messi tra i marcatori NON FIDATO; niente HTML grezzo, niente screenshot;
  - mai eccezioni verso chi chiama: in errore {"ok": False, "motivo": ...}.

Limiti dichiarati: Chromium gira senza la sua sandbox (Playwright la toglie da root) e senza
bwrap: un difetto di Chromium sfruttato da una pagina arriva ai file dell'utente di Gas. Da
non accendere sul VPS prima dell'isolamento (punto 4 del piano: bwrap come per run_command).
Il proxy filtra le destinazioni, non i dati: la pagina può mandare dati a un host pubblico.
Il proxy giudica ogni richiesta da sola: la regola di leggi_pagina «niente redirect da https a
http» qui non vale, e il browser riscarica la pagina, che il server può servire diversa (R-593-6).
«X-Gas-Proxy: rifiuto» il proxy lo toglie dalle risposte http dei server, non da quelle dentro
un tunnel https: lì un sito può far dire «pagina rifiutata dal proxy» alla sua pagina (R-593-3).
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from typing import Optional

from modules.web import leggi as _leggi
from modules.web.proxy import ProxyFiltrante

logger = logging.getLogger("gas.web")

TEMPO_MAX = 25.0              # secondi per tutta la lettura (avvio di Chromium compreso)
TEMPO_PAGINA = 15.0           # secondi per il caricamento della pagina
ATTESA_JS = 2.0               # secondi al più, dopo il caricamento, per la rete degli script
MEMORIA_PROCESSO = 2 << 30    # byte di dati per ogni processo (RLIMIT_DATA)
MEMORIA_JS_MB = 256           # heap di V8 per pagina
MAX_USCITA = 4 * _leggi.MAX_CARATTERI  # caratteri di testo che il figlio può mandare

# Variabili d'ambiente passate al figlio: nient'altro (le chiavi di Gas restano fuori).
_AMBIENTE = ("PATH", "NODE_PATH", "PLAYWRIGHT_BROWSERS_PATH", "LANG")

_ARGOMENTI = (
    "--proxy-bypass-list=<-loopback>",  # R-585-5: anche 127.0.0.1 passa dal proxy
    "--disable-quic",
    "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
    "--webrtc-ip-handling-policy=disable_non_proxied_udp",
    "--disable-background-networking",
    "--disable-component-update",
    "--disable-default-apps",
    "--disable-sync",
    "--disable-extensions",
    "--no-pings",
    "--no-first-run",
    "--disable-features=NetworkPrediction,DnsOverHttps,MediaRouter,Translate,OptimizationHints",
    "--renderer-process-limit=2",
    f"--js-flags=--max-old-space-size={MEMORIA_JS_MB}",
)

# Codice del figlio (Node). Argomenti: url, porta del proxy, millisecondi di pagina e di
# attesa degli script, caratteri massimi, argomenti di Chromium in JSON. Scrive su stdout una
# riga JSON {"testo", "titolo", "url"} oppure {"errore"} (motivo scritto qui, mai dalla pagina).
_FIGLIO = r"""
const { chromium } = require('playwright');
const [url, porta, msPagina, msJs, maxCar, argomenti] = process.argv.slice(1);
const SPEGNI = () => {
  for (const n of ['WebSocket', 'WebSocketStream', 'RTCPeerConnection', 'webkitRTCPeerConnection',
                   'RTCDataChannel', 'RTCSessionDescription', 'Notification', 'SharedWorker']) {
    try { Object.defineProperty(window, n, { value: undefined, configurable: false, writable: false }); }
    catch (e) {}
  }
  try { Object.defineProperty(window, 'open', { value: () => null, configurable: false, writable: false }); }
  catch (e) {}
  try { Object.defineProperty(Navigator.prototype, 'serviceWorker', { get: () => undefined, configurable: false }); }
  catch (e) {}
};
(async () => {
  let browser = null;
  try {
    browser = await chromium.launch({
      headless: true,
      args: [`--proxy-server=http://127.0.0.1:${porta}`, ...JSON.parse(argomenti)],
    });
    const contesto = await browser.newContext({
      acceptDownloads: false, serviceWorkers: 'block', permissions: [], javaScriptEnabled: true,
    });
    await contesto.addInitScript(SPEGNI);
    if (contesto.routeWebSocket) await contesto.routeWebSocket(/.*/, ws => ws.close());
    const pagina = await contesto.newPage();
    contesto.on('page', p => { if (p !== pagina) p.close().catch(() => {}); });
    pagina.on('dialog', d => d.dismiss().catch(() => {}));
    let risposta = null;
    try {
      risposta = await pagina.goto(url, { waitUntil: 'load', timeout: Number(msPagina) });
    } catch (e) {
      process.stdout.write(JSON.stringify({ errore: 'pagina non caricata' }) + '\n');
      return;
    }
    if (risposta && risposta.headers()['x-gas-proxy'] === 'rifiuto') {
      process.stdout.write(JSON.stringify({ errore: 'pagina rifiutata dal proxy' }) + '\n');
      return;
    }
    try { await pagina.waitForLoadState('networkidle', { timeout: Number(msJs) }); } catch (e) {}
    const letto = await pagina.evaluate((max) => ({
      testo: (document.body ? document.body.innerText : '').slice(0, max),
      titolo: String(document.title || '').slice(0, 1000),
    }), Number(maxCar));
    process.stdout.write(JSON.stringify({ ...letto, url: pagina.url() }) + '\n');
  } catch (e) {
    process.stdout.write(JSON.stringify({ errore: 'browser non avviato o fallito' }) + '\n');
  } finally {
    if (browser) await browser.close().catch(() => {});
  }
})();
"""


_ERRORI_FIGLIO = frozenset({"pagina non caricata", "pagina rifiutata dal proxy",
                            "browser non avviato o fallito"})


def attivo() -> bool:
    """Acceso solo con GAS_WEB_BROWSER=1, su Linux e con node nel PATH."""
    return (os.environ.get("GAS_WEB_BROWSER") == "1" and sys.platform == "linux"
            and shutil.which("node") is not None)


# I tetti li mette la shell prima di exec (niente preexec_fn con i thread del proxy vivi,
# R-593-5): valgono per node e per ogni processo di Chromium, che li eredita.
_AVVIO = 'ulimit -d "$1" && ulimit -c 0 && shift && exec "$@"'
_SEGNO = "GAS_BROWSER_LETTURA"


def _stato(pid: int) -> tuple:
    """(stato, gruppo) dal /proc/<pid>/stat, o None se il processo non c'è più."""
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            campi = f.read().rsplit(b")", 1)[1].split()
        return campi[0].decode(), int(campi[2])
    except (OSError, IndexError, ValueError):
        return None


def _vivi() -> dict:
    """PID → gruppo dei processi vivi (gli zombie, già morti, non contano)."""
    vivi = {}
    for nome in os.listdir("/proc"):
        if nome.isdigit():
            st = _stato(int(nome))
            if st and st[0] not in ("Z", "X"):
                vivi[int(nome)] = st[1]
    return vivi


def _col_segno(pid: int, segno: bytes) -> bool:
    try:
        with open(f"/proc/{pid}/environ", "rb") as f:
            return segno in f.read().split(b"\0")
    except OSError:
        return False


def _uccidi_tutti(proc: subprocess.Popen, segno: bytes) -> None:
    """R-593-1: Playwright mette Chromium in una sessione sua, e zygote e renderer non tengono
    l'ambiente. Si uccidono i gruppi di node e di ogni processo col segno della lettura (zygote
    e renderer stanno nel gruppo del Chromium principale), finché nei gruppi non resta nessuno."""
    gruppi = {proc.pid}
    mio = os.getpgrp()
    for _ in range(100):
        vivi = _vivi()
        gruppi |= {g for pid, g in vivi.items() if g != mio and _col_segno(pid, segno)}
        rimasti = {g for g in vivi.values() if g in gruppi}
        if not rimasti:
            return
        for g in rimasti:
            try:
                os.killpg(g, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
        time.sleep(0.02)
    logger.warning("leggi_con_browser: processi del browser ancora vivi dopo l'uccisione")


def _esegui(url: str, porta: int, scadenza: float) -> dict:
    with tempfile.TemporaryDirectory(prefix="gas-browser-") as casa:
        env = {k: os.environ[k] for k in _AMBIENTE if k in os.environ}
        # Con HOME cambiato Playwright non troverebbe più Chromium nella cache dell'utente.
        cache = os.path.expanduser("~/.cache/ms-playwright")
        if "PLAYWRIGHT_BROWSERS_PATH" not in env and os.path.isdir(cache):
            env["PLAYWRIGHT_BROWSERS_PATH"] = cache
        env.update(HOME=casa, TMPDIR=casa, XDG_CONFIG_HOME=casa, XDG_CACHE_HOME=casa)
        env[_SEGNO] = casa
        segno = f"{_SEGNO}={casa}".encode()
        ms_pagina = int(1000 * min(TEMPO_PAGINA, max(0.1, scadenza - time.monotonic() - ATTESA_JS)))
        proc = subprocess.Popen(
            ["sh", "-c", _AVVIO, "sh", str(MEMORIA_PROCESSO // 1024),
             "node", "-e", _FIGLIO, url, str(porta), str(ms_pagina), str(int(1000 * ATTESA_JS)),
             str(MAX_USCITA), json.dumps(_ARGOMENTI)],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            env=env, cwd=casa, start_new_session=True)
        try:
            uscita, _ = proc.communicate(timeout=max(0.1, scadenza - time.monotonic()))
        except subprocess.TimeoutExpired:
            _uccidi_tutti(proc, segno)
            proc.communicate()
            raise _leggi._Rifiuto("tempo massimo del browser superato") from None
        finally:
            _uccidi_tutti(proc, segno)  # anche i processi di Chromium, prima di cancellare il profilo
    # R-593-2: solo «\n» separa le righe (U+2028 e U+0085 restano dentro il JSON).
    righe = [r for r in uscita.decode("utf-8", "replace").split("\n") if r.strip()]
    try:
        esito = json.loads(righe[-1]) if righe else {}
    except ValueError:
        esito = {}
    if not isinstance(esito, dict) or not esito:
        raise _leggi._Rifiuto("risposta del browser non valida")
    if "errore" in esito:
        motivo = esito["errore"]
        raise _leggi._Rifiuto(motivo if motivo in _ERRORI_FIGLIO else "risposta del browser non valida")
    if not all(isinstance(esito.get(k), str) for k in ("testo", "titolo", "url")):
        raise _leggi._Rifiuto("risposta del browser non valida")
    return esito


def leggi_con_browser(
    url: str,
    *,
    _risolvi: Optional[_leggi.Risolutore] = None,
    _connetti: Optional[_leggi.Connettore] = None,
) -> dict:
    """Carica UNA pagina in Chromium senza schermo e ne restituisce il testo visibile.

    → come leggi_pagina: {"ok": True, "url", "testo", "troncato", "fidato": False, "codice"},
      con «testo» dentro i marcatori NON FIDATO; {"ok": False, "motivo"} in ogni errore.
    Non controlla GAS_WEB_BROWSER: lo fa chi chiama (leggi_pagina). I parametri con il
    trattino basso servono solo ai test (DNS e connessioni finti, passati al proxy).
    """
    scadenza = time.monotonic() + TEMPO_MAX
    try:
        _, _, _, _, normalizzato = _leggi._valida_url(url)
        with ProxyFiltrante(durata=TEMPO_MAX, _risolvi=_risolvi, _connetti=_connetti) as proxy:
            esito = _esegui(normalizzato, proxy.porta, scadenza)
        finale = esito["url"]
        try:
            finale = _leggi._valida_url(finale)[4]
        except _leggi._Rifiuto:
            finale = normalizzato  # una pagina finita fuori dal web (about:blank…): fonte di partenza
        corpo = _leggi._pulisci(esito["testo"])
        titolo = _leggi._pulisci(esito["titolo"]).replace("\n", " ")[:_leggi.MAX_TITOLO]
        return _leggi._incornicia(finale, titolo, corpo, troncato=len(esito["testo"]) >= MAX_USCITA)
    except _leggi._Rifiuto as e:
        return {"ok": False, "motivo": e.motivo}
    except Exception as e:  # noqa: BLE001 — mai eccezioni verso chi chiama (§9)
        logger.warning("leggi_con_browser: errore %s", type(e).__name__)
        return {"ok": False, "motivo": f"errore del browser ({type(e).__name__})"}
