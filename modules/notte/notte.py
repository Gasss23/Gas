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
  la cronologia di un compito non entra nel successivo. Eccezione voluta (V-1 bot
  #222, 2026-10-20): un contatto scritto da un compito che ha letto testo di terzi
  resta «non fidato» e, finché è nel blocco di memoria, contamina i compiti dopo
  (le loro scritture non documentali vanno alla firma). I kernel del giro nascono con
  carica_storia=False (R-220-2, V-1 bot #176): la conversazione non viene
  nemmeno letta (né messa in quarantena se corrotta) né copiata negli snapshot.
  Eccezione (R-220-1): l'esito di
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
  La riflessione di fine compito (fetta 2.6/2) parte solo se il compito è
  rimasto sotto il suo tetto, ma il suo tempo NON entra nella «durata» né nel
  tetto per compito: conta solo in quello del giro, che può sforare di una
  cascata intera (stesso caso peggiore non duro, R-345-1).
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
- Riflessione automatica (FASE 2.6 fetta 2, decisione operatore 2026-10-15): a
  fine di ogni compito RIUSCITO (esito ok: niente seconda cascata quando i
  provider stanno già fallendo, V-1 bot #211; non scaduto per tempo,
  cronologia non vuota) il kernel
  del compito esegue rifletti(iniettabile=False): le lezioni vanno in
  QUARANTENA (entrano nel prompt solo con `gas lezioni approva <id>`) e il recap
  diventa 'recap_notte', MAI reiniettato nel prompt di sistema (stesso motivo
  della risposta: testo del modello senza nessuno davanti). Una chiamata LLM in
  più per compito, sotto lo stesso tetto di spesa; spegnibile con
  GAS_RIFLESSIONE_AUTO=0. Nel riepilogo e su Telegram va SOLO il numero di
  lezioni proposte, mai il loro testo.
- Un solo giro alla volta (lock su file). Un compito che fallisce viene
  registrato e si passa al successivo; il giro non solleva mai eccezioni (§9).
"""

from __future__ import annotations

import errno
import json
import logging
import math
import os
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

try:
    import fcntl
except ImportError:  # Windows: niente lock, il giro resta comunque eseguibile
    fcntl = None  # type: ignore[assignment]

NOTTE_DIR = ".gas_notte"
RIEPILOGO = "ultimo_giro.md"
# R-394-1: scritto appena il giro parte; il bot Telegram lo usa per capire se un giro
# lanciato da lui è morto prima di arrivare qui (in quel caso nessuno ha avvisato).
AVVIO = "ultimo_avvio"
# R7 (M3, ripresa dopo un crash): compiti iniziati e non finiti. Un compito entra qui
# prima di partire ed esce quando finisce (anche ko o tempo scaduto); se il processo
# muore a metà (crash, kill, corrente) resta, e il giro dopo lo riprende (dopo gli altri).
IN_CORSO = "in_corso.json"
MAX_TENTATIVI = 3         # avvii interrotti dopo i quali il compito non si riprende più
NOTA_RIPRESA = ("\n\n[NOTA DEL KERNEL — RIPRESA] Il giro precedente si è interrotto a metà "
                "di questo compito. Prima di rifare qualcosa controlla cosa è già stato "
                "fatto (strumento `ricorda`, file già scritti) e non ripetere le azioni "
                "già eseguite.")
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
GIORNI_LEAD_FERMO = 7            # lead attivo senza aggiornamenti da tanti giorni = fermo
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


_CHIAVI_COMPITO = frozenset({"nome", "prompt", "attivo", "cervello"})


def _somiglia_cervello(chiave: str) -> bool:
    """R-ve269-1: una chiave sconosciuta che sembra «cervello» (maiuscole, refusi)."""
    import difflib
    k = str(chiave).strip().casefold()
    return k.startswith("cerv") or difflib.SequenceMatcher(None, k, "cervello").ratio() >= 0.75


def carica_catalogo(path: Path, root: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    """Legge e valida il catalogo. Ritorna (compiti attivi validi, avvisi).

    Formato:
        compiti:
          - nome: rassegna_lead        # [a-z0-9_-], max 40, unico
            prompt: "Fai il punto sui lead attivi ..."
            attivo: true               # opzionale, default true
            cervello: forte            # opzionale: solo il cervello forte (R2), mai i gratuiti

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
        ignote = [str(k) for k in v if k not in _CHIAVI_COMPITO]
        if not isinstance(nome, str) or not _NOME_RE.fullmatch(nome):
            avvisi.append(f"voce {i}: nome mancante o non valido "
                          "(solo a-z 0-9 _ -, max 40), saltata")
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
        if any(_somiglia_cervello(k) for k in ignote):
            # R-ve269-1: «cervelo», «Cervello»… scritto male → il compito NON gira
            # (fail-closed: senza il vincolo finirebbe ai gratuiti)
            avvisi.append(f"compito '{nome}': chiave {ignote} non valida (forse "
                          "'cervello'?), saltato")
            continue
        if ignote:
            avvisi.append(f"compito '{nome}': chiavi sconosciute ignorate: {ignote}")
        cervello = v.get("cervello")
        # V-2 ve #269: un campo presente ma vuoto (null, ~) non è «nessun vincolo»
        if "cervello" in v and cervello != "forte":
            # Fail-closed: un valore sbagliato non deve far finire il lavoro ai gratuiti
            avvisi.append(f"compito '{nome}': cervello può essere solo 'forte', saltato")
            continue
        voce = {"nome": nome, "prompt": prompt.strip()}
        if cervello:
            voce["cervello"] = cervello
        compiti.append(voce)
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


def riflessione_auto_attiva() -> bool:
    """FASE 2.6 fetta 2: riflessione automatica (fine compito notturno e `clear`
    nel REPL). Accesa di default; la spegne SOLO GAS_RIFLESSIONE_AUTO=0."""
    return os.environ.get("GAS_RIFLESSIONE_AUTO", "").strip() != "0"


def _rifletti_compito(kernel: Any, nome: str) -> Dict[str, Any]:
    """Riflessione di fine compito: ritorna solo metadati (ok, numero di lezioni
    proposte). Mai eccezioni (§9); il motivo di un fallimento va nel log."""
    try:
        r = kernel.rifletti(iniettabile=False)
        if not isinstance(r, dict) or not r.get("ok"):
            errore = r.get("errore") if isinstance(r, dict) else type(r).__name__
            logging.warning("notte: riflessione di %s non eseguita: %s", nome, errore)
            return {"ok": False, "lezioni": 0}
        return {"ok": True, "lezioni": len(r.get("lezioni") or [])}
    except Exception as e:
        logging.warning("notte: riflessione di %s fallita: %s", nome, e)
        return {"ok": False, "lezioni": 0}


def _esegui_compito(kernel: Any, compito: Dict[str, str], notte_dir: Path,
                    max_sec: float = MAX_SEC_COMPITO_DEFAULT,
                    al_termine: Optional[Callable[[], None]] = None) -> Dict[str, Any]:
    """Esegue UN compito su un kernel nuovo, con cronologia vuota e propria.
    Oltre max_sec (controllo tra un evento e l'altro) il turno viene chiuso ed
    esito='ko'. Mai eccezioni: un errore diventa esito 'ko'. V-1 bot #234:
    `al_termine` si chiama appena il turno è chiuso, PRIMA della riflessione e del
    diario, così un crash in quel momento non fa riprendere un compito già finito."""
    nome = compito["nome"]
    esito: Dict[str, Any] = {"nome": nome, "esito": "ko", "tool": 0,
                             "risposta": "", "errore": "", "negate": 0, "in_attesa": 0}
    t0 = time.monotonic()
    gen = None
    scaduto = False
    try:
        kernel.history = []
        kernel.db_path = notte_dir / f"storia_{nome}.json"
        prompt = compito["prompt"] + (NOTA_RIPRESA if compito.get("ripresa") else "")
        gen = (kernel.run_turn(prompt, cervello="forte") if compito.get("cervello") == "forte"
               else kernel.run_turn(prompt))
        for ev in gen:
            tipo = ev.get("type") if isinstance(ev, dict) else None
            if tipo == "tool_res":
                esito["tool"] += 1
                out = str(ev.get("output", ""))
                if "cancello" in ev:
                    # R-222-2: l'esito lo dice il kernel, non l'inizio del testo (un
                    # file che comincia con «Operazione negata» non conta più)
                    cancello = ev.get("cancello")
                else:  # kernel senza la chiave (vecchio o finto): prefisso del testo
                    cancello = ("negata" if out.startswith(_NEGATA) else
                                "in_attesa" if out.startswith(_IN_ATTESA) else None)
                if cancello == "negata":
                    esito["negate"] += 1
                elif cancello == "in_attesa":
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
                scaduto = True
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
    if al_termine is not None:
        try:
            al_termine()
        except Exception as e:
            logging.warning("notte: fine del compito %s non registrata: %s", nome, e)
    if (esito["esito"] == "ok" and not scaduto and time.monotonic() - t0 < max_sec
            and riflessione_auto_attiva() and getattr(kernel, "history", None)):
        esito["riflessione"] = _rifletti_compito(kernel, nome)
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
                       avvisi: List[str], stato: Optional[Dict[str, Any]] = None) -> str:
    ok = sum(1 for e in esiti if e["esito"] == "ok")
    righe = [f"# Giro notturno di Gas — {inizio}", "",
             f"Catalogo: `{catalogo}` — compiti eseguiti: {len(esiti)}, ok: {ok}, "
             f"ko: {len(esiti) - ok}", ""]
    righe_stato = righe_stato_mattino(stato)
    if righe_stato:
        righe += ["## Stato (calcolato dal kernel)", ""] + [f"- {r}" for r in righe_stato] + [""]
    if avvisi:
        righe += ["## Avvisi", ""] + [f"- {a}" for a in avvisi] + [""]
    for e in esiti:
        ripreso = " — ripreso dopo un'interruzione" if e.get("ripreso") else ""  # R-406-3
        righe += [f"## {e['nome']} — {e['esito'].upper()} "
                  f"({e['tool']} tool, {e.get('durata', 0)}s){ripreso}", ""]
        if e.get("negate") or e.get("in_attesa"):
            righe += [f"Azioni bloccate dal cancello o negate: {e.get('negate', 0)} · "
                      f"in attesa della tua firma su Telegram: {e.get('in_attesa', 0)}", ""]
        if e["errore"]:
            righe += [f"Errore: {e['errore']}", ""]
        rif = e.get("riflessione")
        if rif:
            if not rif["ok"]:
                testo_rif = "Riflessione non riuscita (dettagli in gas_debug.log)"
            elif rif["lezioni"]:
                testo_rif = (f"Riflessione: {rif['lezioni']} lezioni proposte, in attesa del "
                             f"tuo sì (`python3 gas.py lezioni lista`)")
            else:  # V-3 bot #211: niente «0 lezioni … in attesa del tuo sì»
                testo_rif = "Riflessione: nessuna lezione nuova"
            righe += [testo_rif, ""]
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
                               avvisi: List[str], solo_conteggi: bool = False,
                               lezioni_in_attesa: Optional[int] = None,
                               stato: Optional[Dict[str, Any]] = None) -> str:
    """Riepilogo breve del giro per Telegram: solo metadati, mai la risposta del
    modello né il testo degli errori (non fidati). Con `solo_conteggi` (testo
    completo oltre il limite di Telegram) restano i soli conteggi.
    `lezioni_in_attesa` = TUTTE le lezioni ancora da decidere (anche di giri o clear
    precedenti, R-345-3); None se non contate → solo quelle proposte stanotte."""
    ok = sum(1 for e in esiti if e["esito"] == "ok")
    righe = [f"Gas — giro notturno del {inizio}",
             f"Compiti eseguiti: {len(esiti)} · ok: {ok} · ko: {len(esiti) - ok}"]
    righe += righe_stato_mattino(stato) + [""]  # solo numeri del kernel, mai nomi
    nuove = sum(e["riflessione"]["lezioni"] for e in esiti
                if e.get("riflessione") and e["riflessione"]["ok"])
    # R-359-1: lista_lezioni dà [] anche a DB rotto: mai meno di quelle di stanotte.
    lezioni = nuove if lezioni_in_attesa is None else max(nuove, lezioni_in_attesa)
    di_cui = f" (di cui {nuove} di stanotte)" if 0 < nuove < lezioni else ""
    riga_lezioni = (["", f"Lezioni da approvare: {lezioni}{di_cui} — python3 gas.py lezioni lista"]
                    if lezioni else [])
    if solo_conteggi:
        # V-1 bot #217: anche nei soli conteggi resta il numero delle lezioni.
        return "\n".join(righe + [
            f"Avvisi: {len(avvisi)} (dettaglio troppo lungo per Telegram)"] + riga_lezioni + [
            "", f"Risposte e dettagli (testo NON verificato): {NOTTE_DIR}/{RIEPILOGO}"])
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
        rif = e.get("riflessione")
        if rif and rif["ok"] and rif["lezioni"]:
            note.append(f"lezioni proposte: {rif['lezioni']}")
        elif rif and not rif["ok"]:
            note.append("riflessione non riuscita")
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
    righe += riga_lezioni
    righe += ["", f"Risposte e dettagli (testo NON verificato): {NOTTE_DIR}/{RIEPILOGO}"]
    return "\n".join(righe)


def _giorni_fa(ts: Any, adesso: datetime) -> Optional[float]:
    """Giorni passati da un timestamp ISO della memoria; None se illeggibile."""
    try:
        t = datetime.fromisoformat(str(ts))
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        return (adesso - t).total_seconds() / 86400
    except (TypeError, ValueError):
        return None


CODA_LOG_TOKEN = 65536  # byte finali del log dei token controllati dal resoconto


def _tetto_applicato() -> float:
    """V-2 verifica esterna #241: il tetto mostrato è quello che applica
    _budget_superato (stessa lettura e stessi limiti); ripiego _env_budget."""
    try:
        from gas import _env_float
        return _env_float("GAS_DAILY_TOKEN_BUDGET", 0.0, min_val=0.0, max_val=100_000.0)
    except Exception:
        return _env_budget()


def _righe_illeggibili_log(root: Any) -> int:
    """Righe non JSON del log dei token DENTRO la finestra di 24 ore di _daily_cost_usd
    (V-1 bot #241), cercate negli ultimi CODA_LOG_TOKEN byte: contano solo quelle dopo
    l'ultima riga valida più vecchia di 24 ore (il log è in sola aggiunta, quindi in
    ordine di tempo). Una riga finale senza a capo è in scrittura e non conta.
    Log assente (o root ignota) → 0; log che non si apre → -1. Mai eccezioni.
    Limite dichiarato: oltre 64 KB di log nelle 24 ore le righe più vecchie non si vedono."""
    if root is None:
        return 0
    try:
        from gas import TOKEN_LOG_FILENAME
        path = Path(root) / TOKEN_LOG_FILENAME
        if not path.exists():
            return 0
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            fine = f.tell()
            f.seek(max(0, fine - CODA_LOG_TOKEN))
            coda = f.read()
        righe = coda.split(b"\n")
        righe = righe[:-1]  # l'ultimo pezzo è vuoto o una riga ancora in scrittura
        if fine > CODA_LOG_TOKEN:
            righe = righe[1:]  # la prima è probabilmente tagliata a metà
        # stesso formato e stessa soglia di _daily_cost_usd (ts UTC "%Y-%m-%dT%H:%M:%S")
        soglia = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
        rotte = 0
        for r in righe:
            if not r.strip():
                continue
            try:
                d = json.loads(r)
            except ValueError:
                d = None
            if not isinstance(d, dict):
                rotte += 1
            elif d.get("ts") and str(d["ts"]) < soglia:
                # riga valida fuori finestra: le rotte prima sono vecchie. Ts assente =
                # dentro la finestra (R-459-3: nel dubbio non si azzera)
                rotte = 0
        return rotte
    except Exception as e:
        logging.warning("notte: log dei token non controllato: %s", type(e).__name__)
        return -1


def stato_mattino(kernel: Any) -> Dict[str, Any]:
    """R1 «resoconto di spesa e stato»: numeri calcolati dal kernel a fine giro, senza
    modello e senza token: spesa delle ultime 24 ore e tetto, lead attivi e fermi,
    firme in attesa. SOLO conteggi (mai nomi o testo dei lead: vanno su Telegram).
    Ogni voce è indipendente e fail-safe (§9): se non si legge vale None."""
    stato: Dict[str, Any] = {"spesa": None, "tetto": _tetto_applicato() or None,
                             "log_illeggibili": 0, "lead_attivi": None, "lead_fermi": None,
                             "firme_in_attesa": None}
    try:
        costo = getattr(kernel, "_daily_cost_usd", None)
        if callable(costo):
            v = float(costo())
            stato["spesa"] = v if math.isfinite(v) else None
            # V-1 verifica esterna #241: _daily_cost_usd salta le righe rotte (e dà 0.0
            # a log illeggibile): «$0.00» non deve rassicurare se il log è rovinato.
            stato["log_illeggibili"] = _righe_illeggibili_log(getattr(kernel, "root", None))
    except Exception as e:
        logging.warning("notte: spesa non letta per il resoconto: %s", type(e).__name__)
    mem = getattr(kernel, "memory", None)
    if mem is None or not getattr(mem, "available", True):
        return stato
    # R-453-1: lista_contatti dà [] anche a DB rotto («0 lead» rassicurerebbe il falso).
    # conta_approvazioni sullo stesso DB dà None in quel caso: se fallisce, lead e
    # firme restano «non letti».
    try:
        conta = mem.conta_approvazioni()
    except Exception as e:
        conta = None
        logging.warning("notte: firme non contate per il resoconto: %s", type(e).__name__)
    if conta is None:
        return stato
    stato["firme_in_attesa"] = int(conta.get("in_attesa", 0))
    try:
        from modules.memory import STATI_CHIUSI
        attivi = [c for c in mem.lista_contatti() if c.get("stato") not in STATI_CHIUSI]
        adesso = datetime.now(timezone.utc)
        giorni = [_giorni_fa(c.get("aggiornato_il"), adesso) for c in attivi]
        stato["lead_attivi"] = len(attivi)
        # data illeggibile = fermo (nel dubbio si segnala, non si nasconde)
        stato["lead_fermi"] = sum(1 for g in giorni if g is None or g >= GIORNI_LEAD_FERMO)
    except Exception as e:
        logging.warning("notte: lead non contati per il resoconto: %s", type(e).__name__)
    return stato


def righe_stato_mattino(stato: Optional[Dict[str, Any]]) -> List[str]:
    """Righe brevi del resoconto (riepilogo e Telegram). Voce None → «non letta»."""
    if not stato:
        return []
    spesa, tetto = stato.get("spesa"), stato.get("tetto")
    if spesa is None:
        r_spesa = "Spesa ultime 24 ore: non letta"
    elif tetto:
        r_spesa = f"Spesa ultime 24 ore: ${spesa:.2f} su un tetto di ${tetto:.2f}"
    else:
        r_spesa = f"Spesa ultime 24 ore: ${spesa:.2f} (nessun tetto)"
    rotte = stato.get("log_illeggibili") or 0
    if spesa is not None and rotte:
        r_spesa += (" — ATTENZIONE: log dei token illeggibile, spesa forse sottostimata"
                    if rotte < 0 else
                    f" — ATTENZIONE: {rotte} righe illeggibili nel log dei token, "
                    "spesa forse sottostimata")
    attivi, fermi = stato.get("lead_attivi"), stato.get("lead_fermi")
    r_lead = ("Lead attivi: non letti" if attivi is None else
              f"Lead attivi: {attivi} (fermi da {GIORNI_LEAD_FERMO}+ giorni: {fermi})")
    firme = stato.get("firme_in_attesa")
    r_firme = f"Firme in attesa: {'non lette' if firme is None else firme}"
    return [r_spesa, r_lead, r_firme]


def _stampa_sicura(testo: str) -> None:
    """R-267-1: print che non solleva mai (stdout chiuso, pipe rotta, disco pieno):
    chiamata dal `finally` del giro, un'eccezione qui sostituirebbe l'exit code."""
    try:
        print(testo, flush=True)
    except Exception:
        pass


def _firma_notturna(kernel: Any) -> None:
    """Decisione operatore 2026-10-19: le firme chieste di notte scadono dopo 24 ore
    (env GAS_APPROVAL_TIMEOUT_NOTTE_SECS), non dopo 30 minuti. Mai eccezioni: un
    kernel che non accetta l'attributo resta col default di giorno (più corto, quindi
    più prudente)."""
    try:
        from modules.memory import approval_timeout_notte_secs
        kernel.approval_timeout_secs = approval_timeout_notte_secs()
    except Exception as e:
        logging.warning("notte: scadenza notturna delle firme non impostata: %s", e)


def _chiudi_firme_scadute(root: Path) -> int:
    """C5: a fine giro chiude le richieste di firma scadute senza risposta (restano
    nel DB per audit) e ritorna quante: il numero va negli avvisi del mattino, al
    posto di un messaggio a parte. Mai eccezioni (§9): errore → 0."""
    try:
        from modules.memory import MemoryStore, default_db_path
        # R-381-3: come gas doctor, niente DB creato come effetto collaterale.
        if not default_db_path(root).exists():
            return 0
        mem = MemoryStore(default_db_path(root))
        if not mem.available:
            return 0
        return len(mem.scadi_approvazioni())
    except Exception as e:
        logging.warning("notte: firme scadute non controllate: %s", e)
        return 0


def _lezioni_in_attesa(kernel: Any) -> Optional[int]:
    """R-345-3: quante lezioni aspettano ancora il sì dell'operatore. Mai eccezioni:
    kernel o memoria assenti/rotti → None (il messaggio conta solo quelle di stanotte)."""
    try:
        mem = getattr(kernel, "memory", None)
        if mem is None:
            return None
        return len(mem.lista_lezioni("proposta"))
    except Exception as e:
        logging.warning("notte: lezioni in attesa non contate: %s", e)
        return None


def _notifica_telegram(inizio: str, esiti: List[Dict[str, Any]], avvisi: List[str],
                       interrotto: Optional[str] = None,
                       lezioni_in_attesa: Optional[int] = None,
                       stato: Optional[Dict[str, Any]] = None) -> None:
    """Compone e invia il riepilogo del mattino. Mai eccezioni: anche un errore nel
    comporre il messaggio è solo loggato e non cambia l'esito del giro (R-238-2).
    `interrotto` = nome del tipo d'eccezione se il giro si è fermato prima della
    fine, oppure GIRO_OCCUPATO se non è partito per il lock già preso: in entrambi
    i casi parte un testo fisso, così il silenzio non si confonde con «Telegram
    spento» (V-1 bot #169, V-1 bot #170)."""
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
            testo = componi_messaggio_telegram(inizio, esiti, avvisi,
                                               lezioni_in_attesa=lezioni_in_attesa,
                                               stato=stato)
        if interrotto is None and lunghezza_telegram(testo) > TELEGRAM_MAX_CHARS:
            # V-1 verifica esterna #169: meglio i soli conteggi che nessun messaggio.
            testo = componi_messaggio_telegram(inizio, esiti, avvisi, solo_conteggi=True,
                                               lezioni_in_attesa=lezioni_in_attesa,
                                               stato=stato)
        inviato, motivo = invia_notifica(testo)
    except Exception as e:
        logging.warning("notte: riepilogo Telegram non inviato: %s", type(e).__name__)
        _stampa_sicura(f"Riepilogo Telegram NON inviato: errore {type(e).__name__} "
                       "(dettagli in gas_debug.log)")
        return
    # Prova reale 2026-10-11: il messaggio non è arrivato e il motivo stava solo in
    # gas_debug.log. Ora si vede a schermo e nel log del timer (launchd.log).
    # `motivo` è un testo fisso di bot.py (mai token né ID).
    if not inviato:
        logging.warning("notte: riepilogo Telegram non inviato: %s", motivo)
        _stampa_sicura(f"Riepilogo Telegram NON inviato: {motivo}")
    else:
        _stampa_sicura("Riepilogo Telegram inviato.")


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


def _leggi_in_corso(notte_dir: Path) -> Dict[str, Dict[str, Any]]:
    """R7: i compiti rimasti a metà nei giri precedenti, {nome: {tentativi, inizio}}.
    Mai eccezioni: file assente → {}; illeggibile o rovinato → {} e avviso nel log
    (un registro rotto non deve fermare il giro)."""
    path = notte_dir / IN_CORSO
    try:
        dati = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except Exception as e:
        logging.warning("notte: %s illeggibile (%s): nessuna ripresa", IN_CORSO, e)
        return {}
    if not isinstance(dati, dict):
        return {}
    pulito: Dict[str, Dict[str, Any]] = {}
    for nome, v in dati.items():
        t = v.get("tentativi") if isinstance(v, dict) else None
        # V-4 verifica esterna #234: niente bool (True è un int) né numeri assurdi
        sospetto = isinstance(v, dict) and v.get("sospetto") is True
        # R-419-1: tentativi 0 ammesso solo per un compito «sospetto» (saltato dopo
        # MAX_TENTATIVI interruzioni: riparte da capo ma in coda, dopo gli altri)
        if (isinstance(nome, str) and _NOME_RE.fullmatch(nome) and type(t) is int
                and (0 < t <= 1000 or (t == 0 and sospetto))):  # V-2 #234: sospetto anche t>0
            pulito[nome] = {"tentativi": t, "inizio": str(v.get("inizio", ""))[:40]}
            if sospetto:
                pulito[nome]["sospetto"] = True
    return pulito


def _scrivi_in_corso(notte_dir: Path, in_corso: Dict[str, Dict[str, Any]]) -> None:
    """R7: salva il registro dei compiti in corso (scrittura atomica). Mai eccezioni:
    se non si scrive, il giro va avanti senza ripresa (avviso nel log)."""
    try:
        _scrivi_atomico(notte_dir / IN_CORSO, json.dumps(in_corso, ensure_ascii=False))
    except Exception as e:
        logging.warning("notte: %s non scritto (%s): ripresa non garantita", IN_CORSO, e)


def _ordina_riprese(compiti: List[Dict[str, Any]], in_corso: Dict[str, Dict[str, Any]],
                    avvisi: List[str], a_mano: bool = False, pota: bool = True
                    ) -> Tuple[List[Dict[str, Any]], int]:
    """R7: i compiti rimasti a metà ripartono DOPO quelli mai interrotti (prima chi
    è stato interrotto una volta, poi chi 2+ volte), marcati `ripresa`. Oltre
    MAX_TENTATIVI avvii interrotti il compito si salta (avviso) e il suo conto si
    azzera, così il giro dopo ci riprova da capo invece di saltarlo per sempre;
    R-419-1: resta però segnato «sospetto» e riparte in coda, dopo gli altri, finché
    non finisce una volta senza far cadere Gas.
    R-406-1: ritorna anche quanti compiti sono stati saltati (contano come ko per
    l'exit code); `a_mano` (gas notte <nome>, /compito) = l'operatore lo chiede
    esplicitamente: si rilancia lo stesso. R-406-2: in un giro completo le voci di
    compiti che non sono più tra quelli attivi del catalogo si tolgono; R-407-1: solo
    se il catalogo è stato letto senza avvisi (`pota`), così un catalogo assente o
    rovinato per un momento non cancella i conti dei crash."""
    nomi = {c["nome"] for c in compiti}
    if not a_mano and pota:
        for vecchio in [n for n in in_corso if n not in nomi]:
            del in_corso[vecchio]
    ripresi: List[Dict[str, Any]] = []
    altri: List[Dict[str, Any]] = []
    in_coda: List[Dict[str, Any]] = []  # V-1 bot #234: ripresi già falliti 2+ volte
    saltati = 0
    for c in compiti:
        info = in_corso.get(c["nome"])
        if info is None:
            altri.append(c)
        elif info["tentativi"] == 0:  # R-419-1: sospetto, riparte da capo ma in coda
            in_coda.append(c)
        elif info.get("sospetto") and info["tentativi"] < MAX_TENTATIVI:
            # V-2 verifica #234 (4° giro): un sospetto ricaduto resta in coda, ripreso
            in_coda.append({**c, "ripresa": True, "rilancio_a_mano": False,
                            "interruzioni": info["tentativi"]})
        elif info["tentativi"] >= MAX_TENTATIVI and not a_mano:
            avvisi.append(f"compito '{c['nome']}' interrotto {info['tentativi']} volte di "
                          "fila: saltato in questo giro, controlla gas_debug.log")
            in_corso[c["nome"]] = {"tentativi": 0, "inizio": info.get("inizio", ""),
                                   "sospetto": True}
            saltati += 1
        else:
            # V-2 bot #234: l'avviso «ripreso» lo scrive il giro quando il compito parte
            # davvero (kernel avviato, tempo rimasto), non qui.
            voce = {**c, "ripresa": True,
                    "rilancio_a_mano": info["tentativi"] >= MAX_TENTATIVI,
                    "interruzioni": info["tentativi"]}
            # V-1 bot #234: interrotto una volta → tra i ripresi; 2+ volte → in coda.
            (in_coda if info["tentativi"] >= 2 else ripresi).append(voce)
    # V-1 verifica esterna #234 (3° giro, MEDIA) e R-419-1: i compiti mai interrotti
    # (e mai sospetti) partono SEMPRE per primi; poi i ripresi (interrotti una volta),
    # infine quelli già falliti 2+ volte e i sospetti. Un compito che fa cadere Gas
    # costa agli altri solo la prima notte, quando non si sa ancora che crasha.
    return altri + ripresi + in_coda, saltati


def esegui_notte(root_dir: Optional[str] = None, catalogo: Optional[Path] = None,
                 kernel_factory: Optional[Callable[[str], Any]] = None,
                 solo: Optional[str] = None) -> int:
    """Un giro completo (R1: con `solo` = nome, il solo compito del catalogo con quel
    nome esatto; nome assente o non attivo → avviso ed exit 1; R7: i compiti rimasti
    a metà per un crash ripartono dopo gli altri, oltre MAX_TENTATIVI si saltano → exit 1).
    Exit code: 0 tutti i compiti ok (o nessuno attivo),
    1 almeno un compito ko, saltato per tempo, catalogo non valido o giro
    interrotto da un errore (anche un lock che fallisce per un motivo diverso dal
    lock occupato), 2 un altro giro è in corso. A fine giro, a lock rilasciato,
    parte il messaggio Telegram: riepilogo, «INTERROTTO alle …» o «NON avviato»."""
    root = Path(root_dir or os.getcwd()).resolve()
    catalogo = (catalogo or catalogo_default()).expanduser()
    notte_dir = root / NOTTE_DIR
    lock_f = None
    da_notificare: Optional[Tuple[Any, ...]] = None
    try:
        notte_dir.mkdir(parents=True, exist_ok=True)
        try:
            (notte_dir / AVVIO).write_text(_ora_locale() + "\n", encoding="utf-8")
        except Exception as e:
            logging.warning("notte: marcatore di avvio non scritto: %s", e)
        if fcntl is not None:
            lock_f = open(notte_dir / "lock", "w")
            try:
                fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as e:
                # V-2 bot #171: «un altro giro in corso» solo se il lock è davvero
                # occupato; ENOLCK/EINVAL (fs senza flock) vanno come giro interrotto.
                if e.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                    raise
                print("Un altro giro notturno è già in corso: esco.")
                logging.warning("notte: giro NON avviato, lock occupato da un altro giro")
                da_notificare = (_ora_locale(), [], [], GIRO_OCCUPATO)
                return 2
        inizio = _ora_locale()
        compiti, avvisi = carica_catalogo(catalogo, root)
        if solo is not None:
            compiti = [c for c in compiti if c["nome"] == solo]
            if not compiti:
                nome_vis = solo if _NOME_RE.fullmatch(str(solo)) else "(nome non valido)"
                avvisi.append(f"compito '{nome_vis}' non trovato tra i compiti attivi del catalogo")
        catalogo_ko = bool(avvisi) and not compiti  # solo il catalogo decide l'exit code
        in_corso = _leggi_in_corso(notte_dir)  # R7: ripresa dei compiti rimasti a metà
        letto = dict(in_corso)
        compiti, saltati_r7 = _ordina_riprese(compiti, in_corso, avvisi,
                                              a_mano=solo is not None, pota=not avvisi)
        if in_corso != letto:
            _scrivi_in_corso(notte_dir, in_corso)  # conto azzerato dei compiti saltati
        if _env_budget() <= 0.0:
            os.environ["GAS_DAILY_TOKEN_BUDGET"] = BUDGET_NOTTE_DEFAULT_USD
            avvisi.append(f"GAS_DAILY_TOKEN_BUDGET non impostato: tetto di spesa del giro "
                          f"= {BUDGET_NOTTE_DEFAULT_USD} USD/24h (impostalo nel .env)")
        for a in avvisi:
            logging.warning("notte: %s", a)
        if kernel_factory is None:
            from gas import GasKernel
            # R-220-2: il compito non tocca la conversazione dell'operatore.
            kernel_factory = lambda r: GasKernel(root_dir=r, carica_storia=False)  # noqa: E731
        max_compito = _env_secondi("GAS_NOTTE_MAX_SEC_COMPITO", MAX_SEC_COMPITO_DEFAULT)
        max_giro = _env_secondi("GAS_NOTTE_MAX_SEC_GIRO", MAX_SEC_GIRO_DEFAULT)
        t_giro = time.monotonic()
        tempo_finito = False
        esiti: List[Dict[str, Any]] = []
        kernel: Any = None
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
                _firma_notturna(kernel)
            except Exception as e:
                logging.warning("notte: kernel non creato per %s: %s", c["nome"], e)
                esiti.append({"nome": c["nome"], "esito": "ko", "tool": 0, "durata": 0,
                              "risposta": "", "errore": "kernel non avviato (gas_debug.log)"})
                continue
            if c.get("ripresa"):  # V-2 bot #234: avviso solo per una ripresa vera
                extra = (f" (rilanciato a mano dopo {c.get('interruzioni')} interruzioni)"
                         if c.get("rilancio_a_mano") else "")
                avvisi.append(f"compito '{c['nome']}' ripreso: il giro precedente si era "
                              f"interrotto a metà{extra}")
                logging.warning("notte: %s", avvisi[-1])  # R-416-1: anche nella scatola nera
            info_prima = in_corso.get(c["nome"], {})
            prima = info_prima.get("tentativi", 0)
            in_corso[c["nome"]] = {"tentativi": prima + 1, "inizio": _ora_locale()}
            if info_prima.get("sospetto"):  # V-2 #234: resta sospetto finché non finisce bene
                in_corso[c["nome"]]["sospetto"] = True
            _scrivi_in_corso(notte_dir, in_corso)
            def _finito(nome: str = c["nome"]) -> None:
                in_corso.pop(nome, None)  # finito (anche ko): non è un crash
                _scrivi_in_corso(notte_dir, in_corso)
            esito_c = _esegui_compito(kernel, c, notte_dir, min(max_compito, resta),
                                      al_termine=_finito)
            if c.get("ripresa"):
                esito_c["ripreso"] = True
            esiti.append(esito_c)
            if c["nome"] in in_corso:  # rete di sicurezza: al_termine non è stato chiamato
                _finito()
        scadute = _chiudi_firme_scadute(root)
        if scadute:
            avvisi.append(f"{scadute} richiesta/e di firma scaduta/e senza risposta: "
                          f"chiuse, NON eseguite")
            logging.warning("notte: %s", avvisi[-1])  # R-417-1: anche in gas_debug.log
        stato = stato_mattino(kernel)
        testo = _componi_riepilogo(inizio, catalogo, esiti, avvisi, stato)
        try:
            _scrivi_atomico(notte_dir / RIEPILOGO, testo)
        except Exception as e:
            logging.warning("notte: riepilogo non scritto: %s", e)
        print(testo)
        # inviato a lock rilasciato (V-2 #169)
        da_notificare = (inizio, esiti, avvisi, None, _lezioni_in_attesa(kernel), stato)
        if saltati_r7:  # R-406-1: un salto per crash ripetuti è un ko, anche se era l'unico
            return 1
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
