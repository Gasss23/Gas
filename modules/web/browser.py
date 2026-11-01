"""Lettura di una pagina con un browser senza schermo (R6, fette 33-34, chat Mani).

Per le pagine che senza JavaScript sono vuote: Chromium senza schermo (Playwright per Node,
come i test della voce) in un processo figlio, che esce in rete SOLO dal proxy filtrante
(modules/web/proxy.py: le regole di leggi_pagina su OGNI richiesta della pagina). È SPENTO per
default: si accende con GAS_WEB_BROWSER=1 (servono node, il pacchetto playwright, Chromium e
bwrap funzionante: senza isolamento il browser non parte).

Regole (fail-safe, CLAUDE.md §9):
  - isolamento (fetta 34, punto 4 del piano): node e Chromium girano in bwrap con tutti i
    namespace nuovi (anche la rete: dentro c'è solo il loopback) e senza capability
    (--cap-drop ALL: anche da root non si smonta niente, R-599-3); filesystem in sola lettura,
    nascosti /home, /root, /run, /tmp, /var, /srv, /mnt, /media, /opt e la cartella di Gas
    (lì stanno chiavi, dati e i socket Unix degli altri programmi, che una sola lettura non
    ferma: R-599-1); di nuovo visibili in sola lettura solo node, i moduli di Node e Chromium,
    rifiutati se coprirebbero Gas, la home o una cartella nascosta (R-599-2); Gas e la home
    nascoste anche nel loro percorso vero, se ci si arriva da un collegamento (R-600-1); i
    tmpfs che nascondono sono da 1 MB (R-600-3: scriverci non riempie la RAM), /dev/shm da
    256 MB; scrivibile senza tetto solo la cartella della lettura; --die-with-parent e PID
    namespace: morto bwrap, muore tutto;
  - il proxy ascolta su un socket Unix nella cartella della lettura; dentro bwrap node apre un
    ponte da 127.0.0.1 a quel socket, l'unica uscita prevista del sandbox;
  - rete solo dal proxy, anche per il loopback (`--proxy-bypass-list=<-loopback>`, R-585-5);
    QUIC spento, WebRTC senza UDP fuori dal proxy, niente prefetch né rete di sfondo;
  - spenti nelle pagine e nei frame (anche about:blank) WebSocket, RTCPeerConnection,
    notifiche, Worker e SharedWorker, service worker, download, permessi e popup; JavaScript
    acceso, perché è lo scopo. Worker spenti perché lo script iniettato nei worker non vale e
    routeWebSocket non li copre: da un worker un wss:// passava dal tunnel 443 (V-1 ve #315);
    routeWebSocket è obbligatorio (senza, il figlio fallisce);
  - profilo temporaneo cancellato a ogni lettura, ambiente minimo (niente chiavi di Gas);
  - tempo massimo; alla fine (anche in errore) si uccidono node e tutti i processi di Chromium
    della lettura, riconosciuti da un segno nel loro ambiente (Playwright mette Chromium in una
    sessione sua: il gruppo di node non basta, R-593-1), prima di cancellare il profilo;
  - tetto di memoria per processo (ulimit -d, ereditato da Chromium) e per il motore JavaScript;
  - esce SOLO il testo visibile (innerText) e il titolo, passati nella pulizia di leggi.py e
    messi tra i marcatori NON FIDATO; niente HTML grezzo, niente screenshot;
  - mai eccezioni verso chi chiama: in errore {"ok": False, "motivo": ...}.

Limiti dichiarati: sul Mac il browser resta SPENTO (bwrap non esiste: niente isolamento,
niente browser). Chromium gira senza la sua sandbox (Playwright la toglie per default): un
difetto di Chromium sfruttato da una pagina resta dentro bwrap (niente rete fuori dal proxy,
niente file di Gas né home); vede però in sola lettura /usr, /etc e il resto del sistema non
nascosto, e un socket Unix lasciato lì da un altro programma resterebbe raggiungibile.
Una pagina senza Worker può non funzionare (si legge il testo che c'è). Il proxy filtra le
destinazioni, non i dati: la pagina può mandare dati a un host pubblico.
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
MEMORIA_SHM = 256 << 20       # byte del /dev/shm del sandbox (memoria condivisa di Chromium)
TETTO_NASCOSTE = 1 << 20      # byte di ogni tmpfs che nasconde una cartella (R-600-3)
MAX_USCITA = 4 * _leggi.MAX_CARATTERI  # caratteri di testo che il figlio può mandare

# Variabili d'ambiente passate al figlio: nient'altro (le chiavi di Gas restano fuori).
_AMBIENTE = ("PATH", "NODE_PATH", "PLAYWRIGHT_BROWSERS_PATH", "LANG")
# Nascoste nel sandbox (tmpfs sopra): le chiavi e i dati stanno lì. La cartella di Gas si
# aggiunge in _comando_bwrap.
_NASCOSTE = ("/home", "/root", "/run", "/tmp", "/var", "/srv", "/mnt", "/media", "/opt")
_GAS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Codice del figlio (Node). Argomenti: url, socket Unix del proxy, millisecondi di pagina e di
# attesa degli script, caratteri massimi, argomenti di Chromium in JSON. Apre il ponte
# 127.0.0.1 → socket (dentro bwrap non c'è altra rete), poi Chromium. Scrive su stdout una
# riga JSON {"testo", "titolo", "url"} oppure {"errore"} (motivo scritto qui, mai dalla pagina).
_FIGLIO = r"""
const net = require('net');
const { chromium } = require('playwright');
const [url, presa, msPagina, msJs, maxCar, argomenti] = process.argv.slice(1);
const ponte = net.createServer(c => {
  const u = net.connect(presa);
  c.on('error', () => u.destroy()); u.on('error', () => c.destroy());
  c.pipe(u); u.pipe(c);
});
const SPEGNI = () => {
  for (const n of ['WebSocket', 'WebSocketStream', 'RTCPeerConnection', 'webkitRTCPeerConnection',
                   'RTCDataChannel', 'RTCSessionDescription', 'Notification', 'SharedWorker',
                   'Worker']) {
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
    await new Promise((ok, ko) => { ponte.once('error', ko); ponte.listen(0, '127.0.0.1', ok); });
    const porta = ponte.address().port;
    browser = await chromium.launch({
      headless: true,
      args: [`--proxy-server=http://127.0.0.1:${porta}`, ...JSON.parse(argomenti)],
    });
    const contesto = await browser.newContext({
      acceptDownloads: false, serviceWorkers: 'block', permissions: [], javaScriptEnabled: true,
    });
    await contesto.addInitScript(SPEGNI);
    if (!contesto.routeWebSocket) throw new Error('routeWebSocket mancante');  // obbligatorio
    await contesto.routeWebSocket(/.*/, ws => ws.close());
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
    process.exit(0);  // il ponte e le sue connessioni aperte non devono tenere vivo node
  }
})();
"""


_ERRORI_FIGLIO = frozenset({"pagina non caricata", "pagina rifiutata dal proxy",
                            "browser non avviato o fallito"})


def attivo() -> bool:
    """Acceso solo con GAS_WEB_BROWSER=1, su Linux, con node e bwrap nel PATH."""
    return (os.environ.get("GAS_WEB_BROWSER") == "1" and sys.platform == "linux"
            and shutil.which("node") is not None and shutil.which("bwrap") is not None)


_BWRAP_OK: Optional[bool] = None


def _bwrap_funziona() -> bool:
    """Sonda una volta sola che bwrap riesca a creare i namespace (come in gas.py)."""
    global _BWRAP_OK
    if _BWRAP_OK is None:
        bwrap = shutil.which("bwrap")
        try:
            _BWRAP_OK = bwrap is not None and subprocess.run(
                [bwrap, "--unshare-all", "--die-with-parent", "--ro-bind", "/", "/",
                 "--proc", "/proc", "--dev", "/dev", "true"],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=10).returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            _BWRAP_OK = False
        if not _BWRAP_OK:
            logger.warning("leggi_con_browser: bwrap non funziona, il browser resta spento")
    return _BWRAP_OK


_MODULI: dict = {}


def _cartelle_di_playwright(node: str, env: dict) -> list:
    """Dove stanno davvero i pacchetti playwright e playwright-core (spesso sono collegamenti
    fuori da NODE_PATH): le loro cartelle node_modules vanno ri-esposte nel sandbox."""
    chiave = (node, env.get("NODE_PATH", ""))
    if chiave not in _MODULI:
        trovate = []
        try:
            uscita = subprocess.run(
                [node, "-e", "const p = require('path'); const a = require.resolve('playwright/package.json');"
                 "const b = require.resolve('playwright-core/package.json', { paths: [a] });"
                 "console.log(p.dirname(p.dirname(a))); console.log(p.dirname(p.dirname(b)));"],
                env={k: v for k, v in env.items() if k in ("PATH", "NODE_PATH")}, cwd="/",  # R-600-2
                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10).stdout
            trovate = [r for r in uscita.splitlines() if r.startswith("/")]
        except (OSError, subprocess.TimeoutExpired):
            pass
        _MODULI[chiave] = trovate
    return _MODULI[chiave]


def _copre(percorso: str, protetto: str) -> bool:
    """Vero se ri-esporre «percorso» renderebbe di nuovo visibile «protetto» (uguale o antenato)."""
    return protetto == percorso or protetto.startswith(percorso.rstrip("/") + "/")


def _comando_bwrap(casa: str, env: dict) -> list:
    """Prefisso bwrap (fino a «--»): tutti i namespace nuovi, nessuna capability, sistema in sola
    lettura, nascoste le cartelle di _NASCOSTE e quella di Gas; poi di nuovo visibili (in sola
    lettura) solo node, i moduli di Node e Chromium, e scrivibile la cartella della lettura."""
    cmd = ["bwrap", "--unshare-all", "--cap-drop", "ALL", "--die-with-parent", "--new-session",
           "--ro-bind", "/", "/", "--dev", "/dev", "--size", str(MEMORIA_SHM), "--tmpfs", "/dev/shm",
           "--proc", "/proc"]
    casa_utente = os.path.expanduser("~")
    nascoste = list(_NASCOSTE) + [_GAS, os.path.realpath(_GAS), os.path.realpath(casa_utente)]
    for nascosta in dict.fromkeys(nascoste):  # R-600-1: anche il percorso vero, senza doppioni
        cmd += ["--size", str(TETTO_NASCOSTE), "--tmpfs", nascosta]
    node = os.path.realpath(shutil.which("node") or "node")
    servono = [os.path.dirname(os.path.dirname(node)), env.get("PLAYWRIGHT_BROWSERS_PATH", "")]
    servono += env.get("NODE_PATH", "").split(os.pathsep) + _cartelle_di_playwright(node, env)
    protetti = [os.path.realpath(_GAS), os.path.realpath(casa_utente)]
    protetti += [os.path.realpath(n) for n in _NASCOSTE]
    for percorso in servono:
        if percorso and os.path.isdir(percorso):
            vero = os.path.realpath(percorso)
            if any(_copre(vero, p) for p in protetti):
                # R-599-2 (es. node in ~/bin: il prefisso sarebbe la home intera, Gas compreso).
                raise _leggi._Rifiuto("browser non isolabile: node, Playwright o i moduli di Node "
                                      "stanno in una cartella che scoprirebbe Gas o la home")
            cmd += ["--ro-bind", vero, vero]
    cmd += ["--bind", casa, casa, "--chdir", casa, "--clearenv"]
    for k, v in env.items():
        cmd += ["--setenv", k, v]
    return cmd + ["--"]


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


def _esegui(url: str, casa: str, presa: str, scadenza: float) -> dict:
    env = {k: os.environ[k] for k in _AMBIENTE if k in os.environ}
    # Con HOME cambiato (e nascosto) Playwright non troverebbe più Chromium nella cache.
    cache = os.path.expanduser("~/.cache/ms-playwright")
    if "PLAYWRIGHT_BROWSERS_PATH" not in env and os.path.isdir(cache):
        env["PLAYWRIGHT_BROWSERS_PATH"] = cache
    if env.get("PLAYWRIGHT_BROWSERS_PATH", "0") != "0":  # «0» per Playwright è un valore speciale
        env["PLAYWRIGHT_BROWSERS_PATH"] = os.path.realpath(env["PLAYWRIGHT_BROWSERS_PATH"])
    env.update(HOME=casa, TMPDIR=casa, XDG_CONFIG_HOME=casa, XDG_CACHE_HOME=casa)
    env[_SEGNO] = casa
    segno = f"{_SEGNO}={casa}".encode()
    ms_pagina = int(1000 * min(TEMPO_PAGINA, max(0.1, scadenza - time.monotonic() - ATTESA_JS)))
    node = os.path.realpath(shutil.which("node") or "node")
    proc = subprocess.Popen(
        _comando_bwrap(casa, env) + [
            "sh", "-c", _AVVIO, "sh", str(MEMORIA_PROCESSO // 1024),
            node, "-e", _FIGLIO, url, presa, str(ms_pagina), str(int(1000 * ATTESA_JS)),
            str(MAX_USCITA), json.dumps(_ARGOMENTI)],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        env=env, cwd=casa, start_new_session=True)
    ucciso = False
    try:
        uscita, _ = proc.communicate(timeout=max(0.1, scadenza - time.monotonic()))
    except subprocess.TimeoutExpired:
        _uccidi_tutti(proc, segno)
        ucciso = True  # R-595-2: una sola uccisione, non due da 2 s l'una
        proc.communicate()
        raise _leggi._Rifiuto("tempo massimo del browser superato") from None
    finally:
        if not ucciso:  # anche i processi di Chromium, prima di cancellare il profilo
            _uccidi_tutti(proc, segno)
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
        if not _bwrap_funziona():
            raise _leggi._Rifiuto("browser senza isolamento (bwrap) non permesso")
        with tempfile.TemporaryDirectory(prefix="gas-browser-") as casa:
            presa = os.path.join(casa, "proxy.sock")
            with ProxyFiltrante(durata=TEMPO_MAX, percorso=presa, _risolvi=_risolvi,
                                _connetti=_connetti):
                esito = _esegui(normalizzato, casa, presa, scadenza)
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
