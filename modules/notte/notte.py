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
  (.gas_notte/storia_<nome>.json): non legge né sporca la conversazione
  dell'operatore (.gas_history.json), e un compito non contamina il successivo.
- Il cancello resta quello di sempre: le azioni irreversibili (o incerte dopo
  input non fidato) vengono parcheggiate e chieste in firma su Telegram, mai
  eseguite da sole. Il tetto di 10 iterazioni e il budget giornaliero valgono
  anche qui (sono dentro run_turn).
- Nel diario va SOLO una riga di metadati per compito (nome, esito, numero di
  tool, durata), MAI il testo della risposta: il diario finisce nel prompt di
  sistema tramite il pin di memoria, e la risposta del modello non è fidata.
  Il testo va nel riepilogo .gas_notte/ultimo_giro.md, che legge l'operatore.
- Un solo giro alla volta (lock su file). Un compito che fallisce viene
  registrato e si passa al successivo; il giro non solleva mai eccezioni (§9).
"""

from __future__ import annotations

import logging
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
_NOME_RE = re.compile(r"[a-z0-9_-]{1,40}")


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


def _esegui_compito(kernel: Any, compito: Dict[str, str], notte_dir: Path) -> Dict[str, Any]:
    """Esegue UN compito su un kernel nuovo, con cronologia vuota e propria.
    Mai eccezioni: un errore diventa esito 'ko'."""
    nome = compito["nome"]
    esito: Dict[str, Any] = {"nome": nome, "esito": "ko", "tool": 0,
                             "risposta": "", "errore": ""}
    t0 = time.monotonic()
    try:
        kernel.history = []
        kernel.db_path = notte_dir / f"storia_{nome}.json"
        for ev in kernel.run_turn(compito["prompt"]):
            tipo = ev.get("type") if isinstance(ev, dict) else None
            if tipo == "tool_res":
                esito["tool"] += 1
            elif tipo == "final":
                esito["esito"] = "ok"
                esito["risposta"] = str(ev.get("content", ""))
            elif tipo == "error":
                esito["errore"] = str(ev.get("content", ""))
    except Exception as e:
        logging.warning("notte: compito %s fallito: %s", nome, e)
        esito["esito"] = "ko"
        esito["errore"] = f"eccezione {type(e).__name__} (dettagli in gas_debug.log)"
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
        if e["errore"]:
            righe += [f"Errore: {e['errore']}", ""]
        if e["risposta"]:
            testo = e["risposta"]
            if len(testo) > MAX_RISPOSTA_CHARS:
                testo = testo[:MAX_RISPOSTA_CHARS] + "\n…[troncato]"
            righe += ["Risposta (testo del modello, NON verificato):", "", testo, ""]
    righe.append("Azioni rischiose: NON eseguite da sole — se ce ne sono, "
                 "aspettano la tua firma su Telegram (`python3 gas.py telegram`).")
    return "\n".join(righe) + "\n"


def _scrivi_atomico(path: Path, testo: str) -> None:
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp.write_text(testo, encoding="utf-8")
    os.replace(tmp, path)


def esegui_notte(root_dir: Optional[str] = None, catalogo: Optional[Path] = None,
                 kernel_factory: Optional[Callable[[str], Any]] = None) -> int:
    """Un giro completo. Exit code: 0 tutti i compiti ok (o nessuno attivo),
    1 almeno un compito ko o catalogo non valido, 2 un altro giro è in corso."""
    root = Path(root_dir or os.getcwd()).resolve()
    catalogo = (catalogo or catalogo_default()).expanduser()
    notte_dir = root / NOTTE_DIR
    lock_f = None
    try:
        notte_dir.mkdir(parents=True, exist_ok=True)
        if fcntl is not None:
            lock_f = open(notte_dir / "lock", "w")
            try:
                fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                print("Un altro giro notturno è già in corso: esco.")
                return 2
        inizio = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
        compiti, avvisi = carica_catalogo(catalogo, root)
        for a in avvisi:
            logging.warning("notte: %s", a)
        if kernel_factory is None:
            from gas import GasKernel
            kernel_factory = lambda r: GasKernel(root_dir=r)  # noqa: E731
        esiti: List[Dict[str, Any]] = []
        for c in compiti:
            try:
                kernel = kernel_factory(str(root))
            except Exception as e:
                logging.warning("notte: kernel non creato per %s: %s", c["nome"], e)
                esiti.append({"nome": c["nome"], "esito": "ko", "tool": 0, "durata": 0,
                              "risposta": "", "errore": "kernel non avviato (gas_debug.log)"})
                continue
            esiti.append(_esegui_compito(kernel, c, notte_dir))
        testo = _componi_riepilogo(inizio, catalogo, esiti, avvisi)
        try:
            _scrivi_atomico(notte_dir / RIEPILOGO, testo)
        except Exception as e:
            logging.warning("notte: riepilogo non scritto: %s", e)
        print(testo)
        if not compiti:
            return 1 if avvisi else 0
        return 0 if all(e["esito"] == "ok" for e in esiti) else 1
    except Exception as e:
        logging.warning("notte: giro interrotto: %s", e)
        print(f"Giro notturno interrotto: {type(e).__name__} (dettagli in gas_debug.log)")
        return 1
    finally:
        if lock_f is not None:
            try:
                lock_f.close()
            except Exception:
                pass
