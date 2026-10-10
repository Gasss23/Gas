"""FASE 4.5 fetta 1 — giro autonomo ("Direttore", primo mattone).

`gas notte` legge un CATALOGO di compiti (YAML, scritto dall'operatore) e li
esegue uno alla volta col kernel, senza nessuno davanti. Lo avvia un timer del
sistema (launchd sul Mac, cron/systemd altrove): QUANDO girare lo decide il
timer, COSA fare lo decide il catalogo.

Invarianti di sicurezza:
- Il catalogo sta FUORI dalla cartella di Gas (default ~/.gas_notte.yaml):
  write_file è confinato alla root, quindi Gas non può riscriversi da solo i
  compiti notturni. Un catalogo dentro la root viene rifiutato.
- Ogni compito parte con una cronologia VUOTA e propria
  (.gas_notte/storia_<nome>.json): la conversazione dell'operatore
  (.gas_history.json) non entra nella finestra e non viene scritta dal giro, e
  un compito non contamina il successivo. Eccezione (R-220-1): l'esito di
  un'azione parcheggiata e poi firmata su Telegram lo scrive il kernel del bot
  nella conversazione dell'operatore.
- Il cancello resta quello di sempre: le azioni irreversibili (o incerte dopo
  input non fidato) vengono parcheggiate e chieste in firma su Telegram (senza
  Telegram configurato la richiesta è revocata), mai eseguite da sole. Il tetto
  di 10 iterazioni vale anche qui (è dentro run_turn).
- Tetto di spesa (V-1 verifica esterna #160): il budget di run_turn è attivo
  solo con GAS_DAILY_TOKEN_BUDGET > 0, e di default è spento. Senza nessuno
  davanti non deve esserlo: se la variabile manca o vale 0, il giro la imposta
  per il SOLO processo notturno a BUDGET_NOTTE_DEFAULT_USD.
- Nel diario va SOLO una riga di metadati per compito (nome, esito, numero di
  tool, durata), MAI il testo della risposta: il diario finisce nel prompt di
  sistema tramite il pin di memoria, e la risposta del modello non è fidata.
  Il testo va nel riepilogo .gas_notte/ultimo_giro.md, che legge l'operatore.
- Tetto di tempo (R-220-3): ogni compito ha un tetto (GAS_NOTTE_MAX_SEC_COMPITO,
  default 900s) e il giro intero un altro (GAS_NOTTE_MAX_SEC_GIRO, default
  7200s). Il controllo è COOPERATIVO: avviene tra un evento e l'altro di
  run_turn (il generatore viene chiuso, esito 'ko' per tempo) e prima di ogni
  compito (quelli rimasti vengono saltati con avviso). Una singola chiamata
  appesa non si interrompe da qui: la limita il timeout HTTP dei provider
  (GasKernel.PROVIDER_TIMEOUT_SEC) e quello dei comandi. Il tetto NON è duro
  (R-226-2): tra due eventi possono passare fino a (1 + PROVIDER_MAX_RETRIES)
  tentativi x timeout per ogni rung della cascata: 4 rung remoti x 2 x 120s +
  Ollama 2 x 600s = ~36 min nel caso peggiore (R-227-2, V-1 bot #162), più
  l'eventuale attesa chiesta dal provider con Retry-After su una risposta
  ritentata (429, 5xx...; max 60s per ritentativo); il
  timeout HTTP vale per fase di rete, non per l'intera risposta, quindi è un
  ordine di grandezza, non un limite. Compito e giro possono sforare.
- Riepilogo su Telegram (fetta 2): a fine giro (anche se il giro si è
  interrotto per un errore: testo fisso col solo tipo d'eccezione, o se un altro
  giro tiene ancora il lock: testo fisso «NON avviato») e a lock già
  rilasciato, se Telegram è configurato
  (TELEGRAM_BOT_TOKEN + TELEGRAM_ALLOWED_IDS) e GAS_NOTTE_TELEGRAM non vale
  "0", parte un messaggio breve per l'operatore. Contiene SOLO metadati
  (compito, esito, tool, durata, negate/in attesa, avvisi del giro), MAI il
  testo della risposta né il messaggio d'errore: non sono fidati (un link o
  un'istruzione del modello finirebbe sul telefono come se l'avesse scritta
  Gas). Il testo resta in .gas_notte/ultimo_giro.md. Un invio fallito viene
  solo loggato: non cambia l'exit code del giro.
- Un solo giro alla volta (lock su file). Un compito che fallisce viene
  registrato e si passa al successivo; il giro non solleva mai eccezioni (§9).
"""

from __future__ import annotations

import logging
import math
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

try:
    import fcntl
except ImportError:  # Windows: niente lock, il giro resta comunque eseguibile
    fcntl = None  # type: ignore[assignment]

NOTTE_DIR = ".gas_notte"
RIEPILOGO = "ultimo_giro.md"
MAX_COMPITI = 10          # compiti eseguiti per giro, oltre si ignorano (avviso)
MAX_PROMPT_CHARS = 4000   # prompt di un compito
MAX_RISPOSTA_CHARS = 3000  # risposta riportata nel riepilogo, per compito
BUDGET_NOTTE_DEFAULT_USD = "1.0"  # tetto di spesa 24h se l'operatore non ne ha messo uno
MAX_SEC_COMPITO_DEFAULT = 900    # tetto di tempo per compito (env GAS_NOTTE_MAX_SEC_COMPITO)
MAX_SEC_GIRO_DEFAULT = 7200      # tetto di tempo del giro (env GAS_NOTTE_MAX_SEC_GIRO)
MIN_SEC = 30                     # sotto questo valore l'env viene alzato
GIRO_OCCUPATO = "giro_occupato"  # valore di `interrotto` quando il lock è già preso
MAX_AVVISI_TELEGRAM = 5          # avvisi riportati nel messaggio del mattino
MAX_AVVISO_CHARS = 200           # lunghezza di ciascun avviso nel messaggio
_NOME_RE = re.compile(r"[a-z0-9_-]{1,40}")
_NEGATA = "Operazione negata"
_IN_ATTESA = "Azione in attesa di approvazione umana"  # gas.py _parcheggia_e_notifica


def catalogo_default() -> Path:
    """Path del catalogo: env GAS_NOTTE_CATALOGO, altrimenti ~/.gas_notte.yaml."""
    raw = os.environ.get("GAS_NOTTE_CATALOGO", "").strip()
    return Path(raw).expanduser() if raw else Path.home() / ".gas_notte.yaml"


def _dentro(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def carica_catalogo(path: Path, root: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    """Legge e valida il catalogo. Ritorna (compiti attivi validi, avvisi).

    Formato:
        compiti:
          - nome: rassegna_lead        # [a-z0-9_-], max 40, unico
            prompt: "Fai il punto sui lead attivi ..."
            attivo: true               # opzionale, default true

    Mai eccezioni: ogni problema diventa un avviso e la voce viene saltata."""
    avvisi: List[str] = []
    try:
        path = path.expanduser().resolve()
        root = root.resolve()
    except Exception as e:
        return [], [f"catalogo non risolvibile: {e}"]
    if _dentro(path, root):
        return [], [f"catalogo rifiutato: {path} sta dentro la cartella di Gas "
                    "(Gas potrebbe riscriverselo da solo). Spostalo fuori, "
                    "es. ~/.gas_notte.yaml"]
    if not path.is_file():
        return [], [f"catalogo assente: {path}"]
    try:
        import yaml
        dati = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [], [f"catalogo illeggibile ({type(e).__name__}): {path}"]
    voci = dati.get("compiti") if isinstance(dati, dict) else None
    if not isinstance(voci, list):
        return [], ["catalogo senza lista 'compiti'"]

    compiti: List[Dict[str, str]] = []
    visti: set = set()
    for i, v in enumerate(voci, start=1):
        if not isinstance(v, dict):
            avvisi.append(f"voce {i}: non è un oggetto, saltata")
            continue
        nome, prompt, attivo = v.get("nome"), v.get("prompt"), v.get("attivo", True)
        if not isinstance(nome, str) or not _NOME_RE.fullmatch(nome):
            avvisi.append(f"voce {i}: nome mancante o non valido (solo a-z 0-9 _ -, max 40), saltata")
            continue
        if nome in visti:
            avvisi.append(f"voce {i}: nome '{nome}' duplicato, saltata")
            continue
        visti.add(nome)
        if attivo is not True and attivo is not False:
            avvisi.append(f"compito '{nome}': attivo deve essere true/false, saltato")
            continue
        if not attivo:
            continue
        if not isinstance(prompt, str) or not prompt.strip():
            avvisi.append(f"compito '{nome}': prompt mancante, saltato")
            continue
        if len(prompt) > MAX_PROMPT_CHARS:
            avvisi.append(f"compito '{nome}': prompt oltre {MAX_PROMPT_CHARS} caratteri, saltato")
            continue
        compiti.append({"nome": nome, "prompt": prompt.strip()})
    if len(compiti) > MAX_COMPITI:
        avvisi.append(f"{len(compiti)} compiti attivi: eseguiti solo i primi {MAX_COMPITI}")
        compiti = compiti[:MAX_COMPITI]
    return compiti, avvisi


def _env_secondi(nome: str, default: int) -> int:
    """Intero da env, FAIL-SAFE: assente/non valido → default; sotto MIN_SEC → MIN_SEC."""
    raw = os.environ.get(nome, "").strip()
    if not raw:
        return default
    try:
        return max(MIN_SEC, int(raw))
    except ValueError:
        logging.warning("notte: %s=%r non è un intero valido, uso %d", nome, raw, default)
        return default


def _esegui_compito(kernel: Any, compito: Dict[str, str], notte_dir: Path,
                    max_sec: float = MAX_SEC_COMPITO_DEFAULT) -> Dict[str, Any]:
    """Esegue UN compito su un kernel nuovo, con cronologia vuota e propria.
    Oltre max_sec (controllo tra un evento e l'altro) il turno viene chiuso ed
    esito='ko'. Mai eccezioni: un errore diventa esito 'ko'."""
    nome = compito["nome"]
    esito: Dict[str, Any] = {"nome": nome, "esito": "ko", "tool": 0,
                             "risposta": "", "errore": "", "negate": 0, "in_attesa": 0}
    t0 = time.monotonic()
    gen = None
    try:
        kernel.history = []
        kernel.db_path = notte_dir / f"storia_{nome}.json"
        gen = kernel.run_turn(compito["prompt"])
        for ev in gen:
            tipo = ev.get("type") if isinstance(ev, dict) else None
            if tipo == "tool_res":
                esito["tool"] += 1
                out = str(ev.get("output", ""))
                if out.startswith(_NEGATA):
                    esito["negate"] += 1
                elif out.startswith(_IN_ATTESA):
                    # Prefisso dell'esito del cancello. Limite dichiarato (R-222-2): un
                    # file/stdout che INIZIA con la stessa frase gonfia solo il conteggio.
                    esito["in_attesa"] += 1
            elif tipo == "final":
                esito["esito"] = "ok"
                esito["risposta"] = str(ev.get("content", ""))
            elif tipo == "error":
                esito["errore"] = str(ev.get("content", ""))
            if tipo not in ("final", "error") and time.monotonic() - t0 > max_sec:
                logging.warning("notte: compito %s oltre il tetto di %ss, interrotto",
                                nome, int(max_sec))
                esito["errore"] = (f"tempo scaduto: oltre {int(max_sec)}s, "
                                   "compito interrotto")
                break
    except Exception as e:
        logging.warning("notte: compito %s fallito: %s", nome, e)
        esito["esito"] = "ko"
        esito["errore"] = f"eccezione {type(e).__name__} (dettagli in gas_debug.log)"
    finally:
        if gen is not None and hasattr(gen, "close"):
            try:
                gen.close()  # GeneratorExit dentro run_turn: i suoi finally girano
            except Exception as e:
                logging.warning("notte: chiusura turno %s: %s", nome, e)
    esito["durata"] = round(time.monotonic() - t0, 1)
    try:
        kernel._diario_log(
            "notte",
            f"compito={nome} ; esito={esito['esito']} ; tool={esito['tool']} ; "
            f"durata={esito['durata']}s",
            fonte="kernel")
    except Exception as e:
        logging.warning("notte: diario non scritto per %s: %s", nome, e)
    return esito


def _componi_riepilogo(inizio: str, catalogo: Path, esiti: List[Dict[str, Any]],
                       avvisi: List[str]) -> str:
    ok = sum(1 for e in esiti if e["esito"] == "ok")
    righe = [f"# Giro notturno di Gas — {inizio}", "",
             f"Catalogo: `{catalogo}` — compiti eseguiti: {len(esiti)}, ok: {ok}, "
             f"ko: {len(esiti) - ok}", ""]
    if avvisi:
        righe += ["## Avvisi", ""] + [f"- {a}" for a in avvisi] + [""]
    for e in esiti:
        righe += [f"## {e['nome']} — {e['esito'].upper()} "
                  f"({e['tool']} tool, {e.get('durata', 0)}s)", ""]
        if e.get("negate") or e.get("in_attesa"):
            righe += [f"Azioni bloccate dal cancello o negate: {e.get('negate', 0)} · "
                      f"in attesa della tua firma su Telegram: {e.get('in_attesa', 0)}", ""]
        if e["errore"]:
            righe += [f"Errore: {e['errore']}", ""]
        if e["risposta"]:
            testo = e["risposta"]
            if len(testo) > MAX_RISPOSTA_CHARS:
                testo = testo[:MAX_RISPOSTA_CHARS] + "\n…[troncato]"
            righe += ["Risposta (testo del modello, NON verificato):", "", testo, ""]
    righe.append("Azioni rischiose: mai eseguite da sole. Quelle «in attesa» aspettano la "
                 "tua firma su Telegram (`python3 gas.py telegram`); quelle negate non "
                 "sono state eseguite.")
    return "\n".join(righe) + "\n"


def componi_messaggio_telegram(inizio: str, esiti: List[Dict[str, Any]],
                               avvisi: List[str], solo_conteggi: bool = False) -> str:
    """Riepilogo breve del giro per Telegram: solo metadati, mai la risposta del
    modello né il testo degli errori (non fidati). Con `solo_conteggi` (testo
    completo oltre il limite di Telegram) restano i soli conteggi."""
    ok = sum(1 for e in esiti if e["esito"] == "ok")
    righe = [f"Gas — giro notturno del {inizio}",
             f"Compiti eseguiti: {len(esiti)} · ok: {ok} · ko: {len(esiti) - ok}", ""]
    if solo_conteggi:
        return "\n".join(righe + [
            f"Avvisi: {len(avvisi)} (dettaglio troppo lungo per Telegram)",
            f"Risposte e dettagli (testo NON verificato): {NOTTE_DIR}/{RIEPILOGO}"])
    for e in esiti:
        segno = "OK" if e["esito"] == "ok" else "KO"
        riga = f"{segno} {e['nome']} ({e['tool']} tool, {e.get('durata', 0)}s)"
        note = []
        if e.get("negate"):
            note.append(f"negate: {e['negate']}")
        if e.get("in_attesa"):
            note.append(f"in attesa della tua firma: {e['in_attesa']}")
        if e.get("errore"):
            note.append("errore (vedi riepilogo)")
        if note:
            riga += " — " + ", ".join(note)
        righe.append(riga)
    if avvisi:
        righe += ["", f"Avvisi: {len(avvisi)}"]
        for a in avvisi[:MAX_AVVISI_TELEGRAM]:
            a = a if len(a) <= MAX_AVVISO_CHARS else a[:MAX_AVVISO_CHARS] + "…"
            righe.append(f"- {a}")
        if len(avvisi) > MAX_AVVISI_TELEGRAM:
            righe.append(f"- …e altri {len(avvisi) - MAX_AVVISI_TELEGRAM}")
    righe += ["", f"Risposte e dettagli (testo NON verificato): {NOTTE_DIR}/{RIEPILOGO}"]
    return "\n".join(righe)


def _notifica_telegram(inizio: str, esiti: List[Dict[str, Any]], avvisi: List[str],
                       interrotto: Optional[str] = None) -> None:
    """Compone e invia il riepilogo del mattino. Mai eccezioni: anche un errore nel
    comporre il messaggio è solo loggato e non cambia l'esito del giro (R-238-2).
    `interrotto` = nome del tipo d'eccezione se il giro si è fermato prima della
    fine: parte un testo fisso, così il silenzio non si confonde con «Telegram
    spento» (V-1 bot #169)."""
    if os.environ.get("GAS_NOTTE_TELEGRAM", "").strip() == "0":
        return
    try:
        from modules.telegram.bot import TELEGRAM_MAX_CHARS, invia_notifica, lunghezza_telegram
        if interrotto is not None:
            if interrotto == GIRO_OCCUPATO:
                # V-1 bot #170: il silenzio col lock occupato non è distinguibile da
                # «Telegram spento»; un giro appeso lascerebbe muti anche i successivi.
                testo = (f"Gas — giro notturno NON avviato alle {inizio}: un altro giro "
                         "è ancora in corso. Se succede più notti di fila, controlla "
                         "gas_debug.log.")
            else:
                testo = (f"Gas — giro notturno INTERROTTO alle {inizio}: {interrotto}. "
                         "Dettagli in gas_debug.log.")
        else:
            testo = componi_messaggio_telegram(inizio, esiti, avvisi)
        if interrotto is None and lunghezza_telegram(testo) > TELEGRAM_MAX_CHARS:
            # V-1 verifica esterna #169: meglio i soli conteggi che nessun messaggio.
            testo = componi_messaggio_telegram(inizio, esiti, avvisi, solo_conteggi=True)
        inviato, motivo = invia_notifica(testo)
    except Exception as e:
        logging.warning("notte: riepilogo Telegram non inviato: %s", type(e).__name__)
        return
    if not inviato:
        logging.warning("notte: riepilogo Telegram non inviato: %s", motivo)


def _ora_locale() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")


def _env_budget() -> float:
    """GAS_DAILY_TOKEN_BUDGET come float; assente o non valido → 0.0 (spento)."""
    try:
        v = float(os.environ.get("GAS_DAILY_TOKEN_BUDGET", "").strip() or 0.0)
    except ValueError:
        return 0.0
    return v if math.isfinite(v) else 0.0


def _scrivi_atomico(path: Path, testo: str) -> None:
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp.write_text(testo, encoding="utf-8")
    os.replace(tmp, path)


def esegui_notte(root_dir: Optional[str] = None, catalogo: Optional[Path] = None,
                 kernel_factory: Optional[Callable[[str], Any]] = None) -> int:
    """Un giro completo. Exit code: 0 tutti i compiti ok (o nessuno attivo),
    1 almeno un compito ko, saltato per tempo o catalogo non valido, 2 un altro
    giro è in corso."""
    root = Path(root_dir or os.getcwd()).resolve()
    catalogo = (catalogo or catalogo_default()).expanduser()
    notte_dir = root / NOTTE_DIR
    lock_f = None
    da_notificare: Optional[Tuple[Any, ...]] = None
    try:
        notte_dir.mkdir(parents=True, exist_ok=True)
        if fcntl is not None:
            lock_f = open(notte_dir / "lock", "w")
            try:
                fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                print("Un altro giro notturno è già in corso: esco.")
                logging.warning("notte: giro NON avviato, lock occupato da un altro giro")
                da_notificare = (_ora_locale(), [], [], GIRO_OCCUPATO)
                return 2
        inizio = _ora_locale()
        compiti, avvisi = carica_catalogo(catalogo, root)
        catalogo_ko = bool(avvisi) and not compiti  # solo il catalogo decide l'exit code
        if _env_budget() <= 0.0:
            os.environ["GAS_DAILY_TOKEN_BUDGET"] = BUDGET_NOTTE_DEFAULT_USD
            avvisi.append(f"GAS_DAILY_TOKEN_BUDGET non impostato: tetto di spesa del giro "
                          f"= {BUDGET_NOTTE_DEFAULT_USD} USD/24h (impostalo nel .env)")
        for a in avvisi:
            logging.warning("notte: %s", a)
        if kernel_factory is None:
            from gas import GasKernel
            kernel_factory = lambda r: GasKernel(root_dir=r)  # noqa: E731
        max_compito = _env_secondi("GAS_NOTTE_MAX_SEC_COMPITO", MAX_SEC_COMPITO_DEFAULT)
        max_giro = _env_secondi("GAS_NOTTE_MAX_SEC_GIRO", MAX_SEC_GIRO_DEFAULT)
        t_giro = time.monotonic()
        tempo_finito = False
        esiti: List[Dict[str, Any]] = []
        for i, c in enumerate(compiti):
            resta = max_giro - (time.monotonic() - t_giro)
            if resta <= 0:
                saltati = [x["nome"] for x in compiti[i:]]
                avvisi.append(f"tetto di tempo del giro ({max_giro}s) raggiunto: "
                              f"saltati {len(saltati)} compiti ({', '.join(saltati)})")
                logging.warning("notte: %s", avvisi[-1])
                tempo_finito = True
                break
            try:
                kernel = kernel_factory(str(root))
            except Exception as e:
                logging.warning("notte: kernel non creato per %s: %s", c["nome"], e)
                esiti.append({"nome": c["nome"], "esito": "ko", "tool": 0, "durata": 0,
                              "risposta": "", "errore": "kernel non avviato (gas_debug.log)"})
                continue
            esiti.append(_esegui_compito(kernel, c, notte_dir, min(max_compito, resta)))
        testo = _componi_riepilogo(inizio, catalogo, esiti, avvisi)
        try:
            _scrivi_atomico(notte_dir / RIEPILOGO, testo)
        except Exception as e:
            logging.warning("notte: riepilogo non scritto: %s", e)
        print(testo)
        da_notificare = (inizio, esiti, avvisi)  # inviato a lock rilasciato (V-2 #169)
        if not compiti:
            return 1 if catalogo_ko else 0
        if tempo_finito:
            return 1
        return 0 if all(e["esito"] == "ok" for e in esiti) else 1
    except Exception as e:
        logging.warning("notte: giro interrotto: %s", e)
        print(f"Giro notturno interrotto: {type(e).__name__} (dettagli in gas_debug.log)")
        # Solo il nome del tipo: il messaggio dell'eccezione può contenere testo non fidato.
        da_notificare = (_ora_locale(),
                         [], [], type(e).__name__)
        return 1
    finally:
        if lock_f is not None:
            try:
                lock_f.close()
            except Exception:
                pass
        if da_notificare is not None:
            _notifica_telegram(*da_notificare)
