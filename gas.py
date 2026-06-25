#!/usr/bin/env python3
import os
import json
import shlex
import logging
import subprocess
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import List, Dict, Any, Generator, Optional, Tuple
from openai import OpenAI
from modules.memory import MemoryStore, default_db_path, STATI_CHIUSI, STATI_CONTATTO, normalizza_chiave
from modules.memory import VectorStore, default_vectors_path, EMBED_MODEL_NAME

# Console solo da WARNING in su; il file (scatola nera) riceve tutto ciò che
# i logger lasciano passare. Il root logger resta a WARNING, quindi le librerie
# (httpx ecc.) non inquinano il log: solo i logger alzati esplicitamente a INFO
# (es. gas.snapshot) scrivono righe informative nella scatola nera.
_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("gas_debug.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"),
        _console_handler,
    ],
)
_snapshot_log = logging.getLogger("gas.snapshot")
_snapshot_log.setLevel(logging.INFO)

_GAS_SYSTEM_PROMPT_BASE = (
    "Sei Gas, un agente AI autonomo e personale che gira su VPS. "
    "Hai memoria persistente delle conversazioni in .gas_history.json.\n\n"
    "REGOLE TASSATIVE:\n"
    "- Usa SEMPRE i tool nativi (read_file, write_file, run_command). "
    "Non inventare, descrivere o simulare mai l'output: invocali davvero e aspetta il risultato.\n"
    "- Priorità assoluta alla robustezza: se qualcosa fallisce, gestisci l'errore senza bloccarti.\n"
    "- Rispondi sempre in italiano, in modo conciso e diretto.\n"
    "- Per conteggi, misure e calcoli esatti usa SEMPRE run_command (es. wc -l), "
    "non stimare mai a mente. Se non puoi verificare un dato, dichiara l'incertezza "
    "invece di inventare.\n"
    "- run_command è confinato: esegue SOLO comandi di sola lettura da una "
    "allowlist (ls, cat, head, tail, grep, wc, cut, diff...), SENZA shell. "
    "Pipe (|), redirezioni (>), concatenazioni (;, &&), command substitution "
    "($(...)) e interpreti NON funzionano: vengono trattati come testo o negati. "
    "Per i conteggi usa le opzioni native (es. 'grep -c X file', 'wc -l file'); "
    "per creare o modificare file usa SEMPRE write_file, mai redirezioni shell. "
    "Inoltre, dove disponibile, run_command gira in un sandbox a livello OS "
    "(rete ISOLATA e filesystem READ-ONLY): da lì non hai accesso di rete e non "
    "puoi scrivere file.\n"
    "- Non scrivere MAI file di memoria o cronologia (gas_history e simili): "
    "la memoria è gestita automaticamente dal kernel."
)

def _build_system_prompt(root: Path) -> str:
    """Costruisce il system prompt iniettando l'identità runtime (gas_identity.md)."""
    identity_md = root / "gas_identity.md"
    if identity_md.exists():
        identity = identity_md.read_text(encoding="utf-8")
        return f"# LA TUA IDENTITÀ\n\n{identity}\n\n{_GAS_SYSTEM_PROMPT_BASE}"
    return _GAS_SYSTEM_PROMPT_BASE

# Cache di processo della capacità del sandbox OS: la disponibilità di
# bwrap + namespace è statica per host, quindi sondiamo UNA volta sola (la
# sonda avvia un processo bwrap reale: non vogliamo pagarla a ogni init di
# GasKernel né a ogni run di doctor). None = non ancora sondato.
_OS_SANDBOX_CACHE: Optional[Tuple[bool, str]] = None

def _probe_os_sandbox(force: bool = False) -> Tuple[bool, str]:
    """Sonda REALE (non simulata) della disponibilità del sandbox OS.
    Ritorna (disponibile, dettaglio). Due condizioni: (1) bwrap installato;
    (2) i namespace richiesti sono concessi davvero dall'ambiente — verificato
    creandone uno minimale (rete+pid+proc, root read-only) ed eseguendovi
    'true'. In un container senza privilegi i namespace possono mancare anche
    con bwrap presente: per questo si SONDA, non si assume. Risultato cachato
    a livello di processo (force=True per ri-sondare)."""
    global _OS_SANDBOX_CACHE
    if _OS_SANDBOX_CACHE is not None and not force:
        return _OS_SANDBOX_CACHE
    import shutil
    bwrap = shutil.which("bwrap")
    if not bwrap:
        _OS_SANDBOX_CACHE = (False, "bwrap non installato")
        return _OS_SANDBOX_CACHE
    try:
        res = subprocess.run(
            [bwrap, "--unshare-net", "--unshare-pid", "--proc", "/proc",
             "--ro-bind", "/", "/", "--die-with-parent", "true"],
            capture_output=True, text=True, timeout=10)
    except Exception as e:
        _OS_SANDBOX_CACHE = (False, f"sonda namespace fallita: {str(e)[:60]}")
        return _OS_SANDBOX_CACHE
    if res.returncode != 0:
        _OS_SANDBOX_CACHE = (False, f"namespace non concessi: {res.stderr.strip()[:80]}")
        return _OS_SANDBOX_CACHE
    _OS_SANDBOX_CACHE = (True, "bwrap + namespace net/pid OK")
    return _OS_SANDBOX_CACHE

# --- Provider della cascata: PUNTO UNICO di verità (usato da run_turn E doctor) ---
# Endpoint OpenAI-compatibili e slug dei modelli, prima duplicati nei due punti.
# I due rung gratuiti (OpenRouter free, Ollama) sono la rete di salvataggio a budget
# zero, sempre ULTIMI nella cascata. Se il modello free OpenRouter NON supporta i
# tool, il loop agentico degrada a sola risposta testuale (accettabile, ultima spiaggia).
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROQ_URL = "https://api.groq.com/openai/v1"
OPENROUTER_URL = "https://openrouter.ai/api/v1"
GEMINI_FLASH_LITE_MODEL = "gemini-2.5-flash-lite"
GEMINI_FLASH_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENROUTER_FREE_MODEL = "meta-llama/llama-3.3-70b-instruct:free"  # tool-capable
OLLAMA_MODEL = "qwen2.5:7b-instruct"                             # tool-capable
TOKEN_LOG_FILENAME = ".gas_tokens.jsonl"                          # contabilità token per-chiamata

# Prezzi per milione di token (USD), approssimati — aggiornare se cambiano.
# Fonte: pagine prezzi ufficiali (rilevate al 2025-06).
# Chiave: nome provider come registrato in _log_tokens / .gas_tokens.jsonl.
_PROVIDER_PRICE_PER_MTok: Dict[str, Tuple[float, float]] = {
    "gemini-flash-lite": (0.10,  0.40),   # gemini-2.5-flash-lite: input / output
    "gemini-flash":      (0.30,  2.50),   # gemini-2.5-flash (no-thinking)
    "groq":              (0.59,  0.79),   # llama-3.3-70b-versatile (pay-as-you-go)
    "openrouter":        (0.00,  0.00),   # meta-llama free tier → 0
    "ollama":            (0.00,  0.00),   # locale → 0
}

# Registro STATICO dei modelli che DICHIARANO function calling. Serve SOLO per
# l'osservabilità nella scatola nera (sez.9): il rilevamento a runtime del degrado
# a solo-testo è rimandato (falsi positivi, TASK B / R2 #5). Tutti i modelli della
# cascata sono oggi tool-capable; il warning è una rete dormiente che si accende se
# in futuro entra in cascata un modello senza tool.
TOOL_CAPABLE_MODELS = frozenset({
    GEMINI_FLASH_LITE_MODEL, GEMINI_FLASH_MODEL, GROQ_MODEL,
    OPENROUTER_FREE_MODEL, OLLAMA_MODEL,
})

def _model_tool_capable(model: str) -> bool:
    """True se `model` dichiara function calling nel registro statico
    `TOOL_CAPABLE_MODELS`. Deterministico, nessuna chiamata di rete."""
    return model in TOOL_CAPABLE_MODELS

# --- Integrità del paracadute free (R1/R2 #5): metadati OpenRouter, NIENTE token ---
# La forma reale dell'API (sondata il 2026-06-14): il singolo modello vive su
# GET <base>/models/<slug>/endpoints -> {"data": {... "endpoints": [{...,
# "supported_parameters": [...]}, ...]}}. `supported_parameters` è PER-ENDPOINT
# (al livello "data" è None); "tools" dentro la lista = function calling dichiarato.
def _free_model_endpoint_url(base_url: str, model: str) -> str:
    """URL dei METADATI del singolo modello (non una generazione)."""
    return base_url.rstrip("/") + "/models/" + model + "/endpoints"

def _http_get_json(url: str, api_key: Optional[str] = None, timeout: int = 20):
    """GET minimale -> (status_code, json|None). 404 (e ogni HTTPError) torna il
    codice con body None, senza sollevare. Solo metadati: nessun token LLM."""
    import urllib.request, urllib.error
    headers = {"User-Agent": "gas-doctor"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None

def _classify_free_model(status_code: int, data: Optional[Dict[str, Any]]) -> Tuple[str, str]:
    """Classifica la salute del modello free dai SOLI metadati (mai una
    generazione). Tre esiti (R1/R2 #5):
      - 404                                  -> WARN (assente/rinominato)
      - esiste ma nessun endpoint ha 'tools' -> WARN (no function calling)
      - esiste e almeno un endpoint ha 'tools'-> OK
    Risposte non conclusive (altro status / JSON inatteso) -> WARN onesto."""
    if status_code == 404:
        return ("WARN", "modello free assente/rinominato lato OpenRouter")
    if status_code != 200 or not isinstance(data, dict):
        return ("WARN", f"check esistenza non conclusivo (HTTP {status_code})")
    node = data.get("data", data)
    endpoints = node.get("endpoints") if isinstance(node, dict) else None
    has_tools = False
    if isinstance(endpoints, list):
        for ep in endpoints:
            sp = ep.get("supported_parameters") if isinstance(ep, dict) else None
            if isinstance(sp, list) and "tools" in sp:
                has_tools = True
                break
    if has_tools:
        return ("OK", "modello free presente, function calling dichiarato")
    return ("WARN", "il modello free non dichiara function calling: "
                    "il loop agentico degraderebbe a solo-testo")

def _classify_provider_error(status_code: Optional[int], err_text: str,
                             obbligatoria: bool) -> Tuple[str, str]:
    """Classifica l'errore di un ping provider nel doctor (PURA, testabile a zero
    token). Esiti:
      - 429 (quota)                          -> QUOTA (avviso, non fallimento)
      - 402 (crediti esauriti) su rung OPZIONALE -> WARN: stato benigno atteso,
        a runtime la cascata scala da sé al rung successivo (§9), il paracadute
        free non è in cascata obbligatoria
      - 402 su rung OBBLIGATORIO              -> KO (un provider a pagamento senza
        credito è un problema reale)
      - tutto il resto                        -> KO
    Mantiene il dettaglio troncato a 60 char per il KO generico (come prima)."""
    txt = err_text[:200]
    if status_code == 429 or "429" in txt:
        return ("QUOTA", "429: quota esaurita")
    if (status_code == 402 or "402" in txt) and not obbligatoria:
        return ("WARN", "402: crediti esauriti (rung free opzionale)")
    return ("KO", err_text[:60])

def _probe_free_model(base_url: str, model: str, api_key: Optional[str], _fetch=None) -> Tuple[str, str]:
    """Fetch (mockabile via `_fetch`) + classificazione. `_fetch(url, api_key)`
    deve tornare (status_code, json|None). Errori di rete -> WARN onesto."""
    fetcher = _fetch or _http_get_json
    url = _free_model_endpoint_url(base_url, model)
    try:
        status, data = fetcher(url, api_key)
    except Exception as e:
        return ("WARN", f"check esistenza fallito: {str(e)[:50]}")
    return _classify_free_model(status, data)

def _parse_mode(env_var: str, allowed: Tuple[str, ...], default: str) -> str:
    """Parse fail-safe di una env di modalità: normalizza (trim/lower/`-`→`_`),
    valida contro `allowed`, ricade su `default` (loggando un warning) se il valore
    è ignoto. PUNTO UNICO: GasKernel.__init__ e doctor() lo usano entrambi così che,
    dato lo stesso env, risolvano lo STESSO mode (incluso ignoto → default)."""
    raw = os.environ.get(env_var, default).strip().lower().replace("-", "_")
    if raw not in allowed:
        logging.warning(f"{env_var}={raw!r} non riconosciuto, uso {default!r}")
        raw = default
    return raw

# --- Manutenzione snapshot (TASK C): retention IBRIDA, PURA e testabile ---
# Il nome ref è refs/gas/snapshots/<YYYYmmdd-HHMMSS.ns>-<sha8>: la parte data sta
# PRIMA dell'ultimo '-' (il ts contiene già un '-' tra data e ora).
def _ref_age_epoch(refname: str) -> Optional[float]:
    """Epoch (secondi) ricavato dal NOME del ref snapshot. None se non parsabile:
    il chiamante, conservativo, in tal caso TIENE il ref (non lo rimuove mai per
    un nome inatteso). Nessuna chiamata git: si legge solo la stringa."""
    import time
    base = refname.rsplit("/", 1)[-1]          # <ts>-<sha8>
    ts_part = base.rsplit("-", 1)[0]           # YYYYmmdd-HHMMSS.ns
    date_part = ts_part.split(".", 1)[0]       # YYYYmmdd-HHMMSS
    try:
        return time.mktime(time.strptime(date_part, "%Y%m%d-%H%M%S"))
    except Exception:
        return None

def _snapshot_retention(refs: List[str], now: float, keep_n: int,
                        keep_days: int) -> Tuple[List[str], List[str]]:
    """Retention IBRIDA. `refs` = refname ORDINATI lessicograficamente (=
    cronologicamente). Si TIENE l'UNIONE di (ultimi keep_n) e (più giovani di
    keep_days): quale delle due preserva di più, in una sessione intensa protegge
    comunque i recenti. Ritorna (keep, drop) preservando l'ordine. `drop` = ref
    oltre ENTRAMBE le soglie, candidati alla rimozione (un ref cancellato lascia
    l'oggetto git RECUPERABILE finché non gira `git gc`)."""
    if not refs:
        return [], []
    cutoff = now - keep_days * 86400
    keep_set = set(refs[-keep_n:]) if keep_n > 0 else set()
    for r in refs:
        age = _ref_age_epoch(r)
        if age is None or age >= cutoff:   # non parsabile o giovane -> tieni
            keep_set.add(r)
    keep = [r for r in refs if r in keep_set]
    drop = [r for r in refs if r not in keep_set]
    return keep, drop

def _env_int(name: str, default: int, min_val: int = 1) -> int:
    """Legge un intero da una variabile d'ambiente, FAIL-SAFE: assente o non
    parsabile -> default; sotto min_val -> clampato a min_val. Permette di
    configurare i tetti della memoria al deploy senza ricompilare (riserva R2
    della fetta 2b), senza mai rompersi su un valore sporco."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return max(min_val, int(raw))
    except (TypeError, ValueError):
        logging.warning(f"{name}={raw!r} non è un intero valido — uso default {default}")
        return default


def _env_float(name: str, default: float, min_val: float = 0.0,
               max_val: float = 1.0) -> float:
    """Legge un float da una variabile d'ambiente, FAIL-SAFE come `_env_int`:
    assente o non parsabile -> default; fuori range -> clampato a [min_val,
    max_val]. Usato per la soglia di similarità coseno VEC_MIN_SIM (R-wire-1):
    ri-tarabile al deploy senza ricompilare. Default di max_val=1.0 perché la
    similarità coseno degli embedding normalizzati è naturalmente limitata a 1."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return min(max_val, max(min_val, float(raw)))
    except (TypeError, ValueError):
        logging.warning(f"{name}={raw!r} non è un float valido — uso default {default}")
        return default


def _env_flag(name: str) -> bool:
    """Legge un flag booleano da env, FAIL-SAFE: vero solo per 1/true/on/yes/si
    (case-insensitive); assente o qualsiasi altro valore → False. Usato per i
    feature-gate OPT-IN (es. il retrieval semantico, spento di default)."""
    return os.environ.get(name, "").strip().lower() in ("1", "true", "on", "yes", "si")


class GasKernel:
    def __init__(self, root_dir: Optional[str] = None):
        self.root: Path = Path(root_dir or os.getcwd()).resolve()
        self.db_path: Path = self.root / ".gas_history.json"
        self.system_prompt: str = _build_system_prompt(self.root)
        self.history: List[Dict[str, Any]] = self._load_history()
        # Modalità del sandbox run_command: 'guarded' (default, vetting +
        # esecuzione senza shell) oppure 'dry_run' (anteprima fedele: fa il
        # vetting ma non esegue nulla — collaudo e kill-switch). Un valore non
        # riconosciuto ricade su 'guarded' (fail-safe). NON esiste una modalità
        # con shell grezza: le pipeline sono volutamente indisponibili.
        self.shell_mode: str = _parse_mode("GAS_SHELL_MODE", ("guarded", "dry_run"), "guarded")
        # Modalità del sandbox OS (ortogonale a GAS_SHELL_MODE: 'dove' si esegue,
        # non 'se'): 'os_strict' (default) pretende il confinamento OS e nega il
        # comando se manca; 'os_with_fallback' degrada alla sola sandbox
        # applicativa quando bwrap/namespace non ci sono. Valore ignoto →
        # fail-safe sul mode PIÙ severo (os_strict): la prod è protetta di default.
        self.sandbox_mode: str = _parse_mode("GAS_SANDBOX_MODE", ("os_strict", "os_with_fallback"), "os_strict")
        # Capacità del sandbox OS sondata una volta (cache di processo).
        self.os_sandbox_available: bool
        self._os_sandbox_detail: str
        self.os_sandbox_available, self._os_sandbox_detail = _probe_os_sandbox()
        # Memoria persistente (FASE 2): diario append-only + rubrica contatti,
        # DB SQLite a file singolo fuori da git. FAIL-SAFE (§9): se la memoria
        # degrada (available=False) o l'istanza non si crea affatto, il resto
        # del kernel funziona comunque — la memoria che non scrive NON deve MAI
        # far crashare GAS né fermare il loop. MemoryStore è già blindato al suo
        # interno; questa cintura copre l'eventualità remota di un errore
        # all'avvio (es. import/ambiente) per non far cadere l'intero kernel.
        self.memory: Optional[MemoryStore]
        try:
            self.memory = MemoryStore(default_db_path(self.root))
        except Exception as e:
            logging.warning(f"MemoryStore non inizializzato ({e}) — memoria disattivata")
            self.memory = None
        # Override via env dei tetti dell'iniezione memoria (riserva R2 fetta 2b):
        # fail-safe (valore sporco → default). Shadowano i default di classe.
        self.MEMORY_PIN_CHAR_CAP = _env_int("GAS_MEMORY_PIN_CHARS", GasKernel.MEMORY_PIN_CHAR_CAP, min_val=200)
        self.MEMORY_PIN_CONTACTS = _env_int("GAS_MEMORY_PIN_CONTACTS", GasKernel.MEMORY_PIN_CONTACTS, min_val=0)
        self.MEMORY_PIN_EVENTS = _env_int("GAS_MEMORY_PIN_EVENTS", GasKernel.MEMORY_PIN_EVENTS, min_val=0)
        self.MEMORY_PIN_SCAN = _env_int("GAS_MEMORY_PIN_SCAN", GasKernel.MEMORY_PIN_SCAN, min_val=10)
        self.WINDOW_CHAR_CAP = _env_int("GAS_WINDOW_CHAR_CAP", GasKernel.WINDOW_CHAR_CAP, min_val=1000)
        self.MEMORY_BACKUP_EVERY_SEC = _env_int("GAS_MEMORY_BACKUP_EVERY_SEC", GasKernel.MEMORY_BACKUP_EVERY_SEC, min_val=0)
        # Backup off-site: dir esterna configurabile (vuota = OFF, default).
        _raw_offsite = os.environ.get("GAS_MEMORY_BACKUP_OFFSITE_DIR", "").strip()
        self.MEMORY_BACKUP_OFFSITE_DIR: Optional[str] = _raw_offsite if _raw_offsite else None
        self.MEMORY_BACKUP_OFFSITE_EVERY_SEC = _env_int(
            "GAS_MEMORY_BACKUP_OFFSITE_EVERY_SEC",
            GasKernel.MEMORY_BACKUP_OFFSITE_EVERY_SEC, min_val=0)
        self.MEMORY_BACKUP_OFFSITE_KEEP = _env_int(
            "GAS_MEMORY_BACKUP_OFFSITE_KEEP",
            GasKernel.MEMORY_BACKUP_OFFSITE_KEEP, min_val=0)
        # Retrieval semantico (FASE 2 — wiring): vector store su sidecar SEPARATO
        # (.gas_vectors.db), cache DERIVATA dal diario. OPT-IN via env GAS_VECTORS
        # perché carica un modello di embedding locale (~500MB su disco + RAM): di
        # default SPENTO, così il deploy base e la suite non lo pagano e il VPS a
        # 1GB RAM (R-vec-3) non viene caricato senza una scelta esplicita. Quando
        # attivo è comunque ADDITIVO e FAIL-SAFE (§9): self.vectors None/degradato →
        # ricorda ricade su FTS/substring, il catch-up è un no-op, GAS gira identico.
        # Stessa doppia cintura di self.memory.
        self.vectors: Optional[VectorStore] = None
        if _env_flag("GAS_VECTORS"):
            try:
                _vec_db = os.environ.get("GAS_VECTORS_DB", "").strip()
                _vec_path = Path(_vec_db).resolve() if _vec_db else default_vectors_path(self.root)
                _vec_model = os.environ.get("GAS_EMBED_MODEL", "").strip() or EMBED_MODEL_NAME
                self.vectors = VectorStore(_vec_path, model_name=_vec_model)
            except Exception as e:
                logging.warning(f"VectorStore non inizializzato ({e}) — retrieval semantico disattivato")
                self.vectors = None
        # Watermark del catch-up indexing: id diario massimo già indicizzato. None =
        # da risolvere al primo turno (letto dal sidecar). Tetto di righe indicizzate
        # per turno (override env): il catch-up resta BOUNDED, niente picchi dopo lunghe
        # pause; recupera l'arretrato in più turni.
        self._vec_watermark: Optional[int] = None
        self.VEC_CATCHUP_MAX = _env_int("GAS_VECTORS_CATCHUP_MAX", GasKernel.VEC_CATCHUP_MAX, min_val=1)
        # Soglia di similarità semantica ri-tarabile al deploy senza ricompilare
        # (R-wire-1): il default x86 0.30 va ricalibrato sul primo diario reale del VPS.
        self.VEC_MIN_SIM = _env_float("GAS_VECTORS_MIN_SIM", GasKernel.VEC_MIN_SIM)
        self.tools_schema = [
            {"type": "function", "function": {"name": "run_command", "description": "Esegue un comando di sola lettura da una allowlist, senza shell (no pipe/redirezioni/interpreti). Dove disponibile gira in sandbox OS: rete isolata, filesystem read-only.", "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}},
            {"type": "function", "function": {"name": "write_file", "description": "Scrive file.", "parameters": {"type": "object", "properties": {"relative_path": {"type": "string"}, "content": {"type": "string"}}, "required": ["relative_path", "content"]}}},
            {"type": "function", "function": {"name": "read_file", "description": "Legge file.", "parameters": {"type": "object", "properties": {"relative_path": {"type": "string"}}, "required": ["relative_path"]}}},
            {"type": "function", "function": {"name": "ricorda", "description": "Consulta la memoria di lungo periodo di Gas (SOLA LETTURA): il diario delle azioni passate e le schede dei lead/contatti. Usalo per ricordare cosa è già successo con un lead o cosa hai già fatto in passato. Non scrive nulla.", "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "parole da cercare negli eventi del diario; la ricerca è per parole/radici e ordinata per pertinenza (opzionale)"}, "contatto": {"type": "string", "description": "chiave o nome di un lead per vederne scheda e storia (opzionale)"}, "n": {"type": "integer", "description": "numero massimo di eventi da restituire (default 10)"}}, "required": []}}},
            {"type": "function", "function": {"name": "salva_contatto", "description": "Crea o aggiorna un lead/contatto nella rubrica di Gas (memoria persistente). Usalo per registrare un nuovo lead o aggiornarne nome/recapito/prossima azione/note. NON cambia lo stato del lead nel funnel: per quello usa imposta_stato_contatto.", "parameters": {"type": "object", "properties": {"chiave": {"type": "string", "description": "identificatore univoco del lead (email/handle/telefono normalizzato)"}, "nome": {"type": "string"}, "contatto": {"type": "string", "description": "recapito: email/telefono/handle"}, "prossima_azione": {"type": "string"}, "note": {"type": "string"}}, "required": ["chiave"]}}},
            {"type": "function", "function": {"name": "imposta_stato_contatto", "description": "Cambia lo STATO di un lead esistente nel funnel (nuovo, contattato, risposto, interessato, rifiutato, chiuso). Il lead deve già esistere: crealo prima con salva_contatto.", "parameters": {"type": "object", "properties": {"chiave": {"type": "string"}, "stato": {"type": "string", "description": "uno tra: nuovo, contattato, risposto, interessato, rifiutato, chiuso"}, "prossima_azione": {"type": "string"}}, "required": ["chiave", "stato"]}}}
        ]

    def _load_history(self) -> List[Dict[str, Any]]:
        if self.db_path.exists():
            try:
                with open(self.db_path, "r", encoding="utf-8") as f: return json.load(f)
            except Exception: return []
        return []

    def _save_history(self):
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Errore scrittura storico: {e}")

    def _log_tokens(self, provider: str, model: str, in_tok: int, out_tok: int) -> None:
        """Appende una riga JSONL al log token (TOKEN_LOG_FILENAME). Fail-safe: un
        errore di I/O non interrompe mai il turno (§9). Log per-chiamata API, non
        per-turno: cattura ogni round-trip inside il loop agentico."""
        try:
            record = {
                "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
                "provider": provider,
                "model": model,
                "in": int(in_tok),
                "out": int(out_tok),
            }
            log_path = self.root / TOKEN_LOG_FILENAME
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.warning("_log_tokens: scrittura fallita (%s) — ignorato", e)

    def _add_to_history(self, role: str, content: Optional[str] = None, tool_calls: Optional[List[Any]] = None, tool_call_id: Optional[str] = None, name: Optional[str] = None):
        """Costruisce un dizionario puro, evitando oggetti complessi."""
        entry = {"role": role}
        if content is not None: entry["content"] = content
        if tool_calls:
            entry["tool_calls"] = [{"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in tool_calls]
        if tool_call_id: entry["tool_call_id"] = tool_call_id
        if name: entry["name"] = name
        self.history.append(entry)

    def _get_window(self, n: int = 10) -> List[Dict[str, Any]]:
        if not self.history:
            return []
        cutoff = max(0, len(self.history) - n)

        # Cerca in avanti da cutoff: primo user message nella finestra
        start = None
        for i in range(cutoff, len(self.history)):
            if self.history[i]["role"] == "user":
                start = i
                break

        # Nessun user message in avanti: cerca all'indietro fino in fondo.
        # Niente cap qui: con una catena tool lunga (fino a 10 coppie per il
        # loop cap = 21 messaggi) l'unico user può stare oltre n*2 e una
        # finestra senza user è un payload malformato (peggio di una lunga).
        if start is None:
            for i in range(cutoff - 1, -1, -1):
                if self.history[i]["role"] == "user":
                    start = i
                    break

        if start is None:
            return []

        # Se il messaggio prima del punto di partenza è un tool_result orfano,
        # risali fino all'assistant che contiene il tool_use corrispondente
        if start > 0 and self.history[start - 1]["role"] == "tool":
            for i in range(start - 2, -1, -1):
                if self.history[i]["role"] == "assistant" and self.history[i].get("tool_calls"):
                    start = i
                    break

        # Il cap di caratteri SI COMPONE con la finestra strutturale: prima
        # _get_window garantisce l'ancora (inizio = user, niente tool orfani),
        # poi _cap_window_chars taglia i messaggi più vecchi che sforano il
        # budget e RIALLINEA di nuovo a un user. Mai slicing dentro un messaggio.
        return self._cap_window_chars(self.history[start:])

    # Tetto RIGIDO di caratteri sulla finestra inviata ai provider, a
    # granularità di MESSAGGIO (mai slicing grezzo: Wall of Shame sez.5). È un
    # secondo limite che si compone con il cap a 10 messaggi di _get_window e
    # con TOOL_OUTPUT_CAP (8k/tool): nel worst case 10 messaggi × ~8k = ~80k
    # caratteri saturerebbero comunque i limiti TPM (incidente 2026-06-10:
    # 84 KB → ~24k token → Groq 413). 24000 caratteri ≈ 6-7k token, soglia di
    # sicurezza con margine ampio sotto i limiti dei provider.
    WINDOW_CHAR_CAP = 24000

    # --- Iniezione memoria always-on (lato lettura, fetta 2b) ---
    # Il blocco-memoria vive NEL messaggio system (fuori dalla finestra), quindi
    # NON passa da _get_window/_cap_window_chars: la finestra conversazionale
    # resta intatta. Il pin ha un suo tetto dedicato, ampiamente sotto
    # WINDOW_CHAR_CAP, così il payload totale (system+pin+finestra) resta sano.
    # Default (override via env, risolti in __init__ — riserva R2 fetta 2b):
    MEMORY_PIN_CHAR_CAP = 3000     # tetto rigido del solo blocco-memoria
    MEMORY_PIN_CONTACTS = 8        # max lead attivi nel pin
    MEMORY_PIN_EVENTS = 6          # max eventi diario "significativi" nel pin
    # Quanti eventi grezzi scandire all'indietro per trovare MEMORY_PIN_EVENTS
    # eventi "buoni" (riserva R3 fetta 2b): finestra AMPIA e BOUNDED, così se il
    # rumore di lettura è denso le azioni vere poco più indietro emergono comunque
    # (LIMIT su SQLite locale: costo trascurabile).
    MEMORY_PIN_SCAN = 200
    # Rumore di sola lettura: eventi che NON meritano l'iniezione always-on (il
    # diario li conserva comunque a monte — decisione A; il filtro è di LETTURA).
    DIARIO_NOISE_TIPI = frozenset({"read_file", "run_command", "ricorda"})

    # --- Backup automatico della memoria (anti auto-corruzione, §10 FASE 2) ---
    # Il DB di memoria è il dato più prezioso e meno rimpiazzabile: un backup
    # THROTTLED (copia coerente via API SQLite) parte a inizio turno, al più una
    # volta ogni MEMORY_BACKUP_EVERY_SEC, con rotazione a MEMORY_BACKUP_KEEP copie.
    # Protegge dall'auto-corruzione.
    # Override via env (risolti in __init__): GAS_MEMORY_BACKUP_EVERY_SEC / _KEEP.
    MEMORY_BACKUP_EVERY_SEC = 6 * 3600   # un backup ogni ~6 ore di attività
    MEMORY_BACKUP_KEEP = 10              # copie .bak conservate (rotazione)
    # --- Backup off-site della memoria (anti-disastro-disco, FASE 5/VPS) ---
    # Throttle SEPARATO: la dir esterna (volume montato / dir sincronizzata) può
    # essere lenta senza interferire col backup locale. Default OFF (dir vuota).
    # Override via env (risolti in __init__): GAS_MEMORY_BACKUP_OFFSITE_DIR /
    # _EVERY_SEC / _KEEP.
    MEMORY_BACKUP_OFFSITE_EVERY_SEC = 86400  # una volta al giorno
    MEMORY_BACKUP_OFFSITE_KEEP = 10

    # --- Retrieval semantico (FASE 2 — wiring del vector store) ---
    # Quante righe di diario nuove indicizzare AL MASSIMO per turno (catch-up
    # bounded; override env GAS_VECTORS_CATCHUP_MAX, risolto in __init__).
    VEC_CATCHUP_MAX = 64
    # Soglia minima di similarità coseno per accettare un hit semantico. MISURATA
    # dal vivo: il MiniLM mean-pooled separa DEBOLMENTE le query corte in italiano
    # (coseni reali ~0.2-0.6 anche per coppie pertinenti, niente soglia netta), quindi
    # il semantico è un SUPPLEMENTO di recall che RIEMPIE i posti liberi dopo FTS, non
    # un sostituto della precisione lessicale (R-wire-1). Soglia conservativa e
    # tarabile: override env GAS_VECTORS_MIN_SIM, risolto in __init__.
    VEC_MIN_SIM = 0.30

    @staticmethod
    def _msg_chars(msg: Dict[str, Any]) -> int:
        """Caratteri 'di payload' di un messaggio: content + (per le tool call)
        argomenti e nome funzione. Misura per il budget a granularità messaggio."""
        total = len(msg.get("content") or "")
        for tc in msg.get("tool_calls") or []:
            fn = tc.get("function") or {}
            total += len(fn.get("arguments") or "") + len(fn.get("name") or "")
        return total

    def _cap_window_chars(self, window: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Applica WINDOW_CHAR_CAP a una finestra GIÀ strutturalmente valida.
        Due passi, in quest'ordine (l'ordine è l'invariante critica):
        1) BUDGET: somma i caratteri dal messaggio più recente all'indietro; i
           messaggi più vecchi che sforano il budget vengono SCARTATI INTERI
           (mai un taglio dentro un messaggio). Il messaggio più recente è
           sempre tenuto intero, anche se da solo supera il budget.
        2) RIALLINEAMENTO: dopo lo scarto l'inizio può non essere più un user
           (un tool/assistant-con-tool orfano in testa rompe Gemini → 400). Si
           riallinea in avanti al primo user. Se il budget avesse scartato OGNI
           user, si ricade sull'ultimo user dell'intera finestra: un payload
           lungo è preferibile a uno vuoto/malformato (lezione 2026-06-11)."""
        if not window:
            return window
        # passo 1 — budget per scarto di messaggi interi (dal più recente)
        total = 0
        kept_start = 0
        for i in range(len(window) - 1, -1, -1):
            c = self._msg_chars(window[i])
            if i < len(window) - 1 and total + c > self.WINDOW_CHAR_CAP:
                kept_start = i + 1
                break
            total += c
        capped = window[kept_start:]
        # passo 2 — riallineamento dell'inizio a un role:user coerente
        for i, m in enumerate(capped):
            if m["role"] == "user":
                return capped[i:]
        # nessun user sopravvissuto al budget: fallback all'ultimo user di tutta
        # la finestra (mai partire da non-user, mai vuoto se un user esiste)
        for i in range(len(window) - 1, -1, -1):
            if window[i]["role"] == "user":
                return window[i:]
        return capped

    def clear_history(self):
        self.history = []
        if self.db_path.exists(): self.db_path.unlink()

    # Cap sull'output dei tool, in caratteri. Senza questo limite un singolo
    # read_file su un file grosso inietta decine di KB nella storia, che
    # _get_window si trascina dietro a ogni chiamata API successiva saturando
    # i limiti TPM (incidente 2026-06-10: 84 KB letti → richiesta successiva
    # da 23.879 token → Groq 413). Protegge anche la futura pipeline di
    # apprendimento: le trascrizioni Whisper sono tipicamente 80-100 KB per
    # 30 minuti di audio.
    TOOL_OUTPUT_CAP = 8000

    def _cap_tool_output(self, name: str, args: Dict[str, Any], out: str) -> str:
        if len(out) <= self.TOOL_OUTPUT_CAP:
            return out
        target = args.get("relative_path") or args.get("command", "?")
        logging.warning(f"Output tool troncato: {name} su {target!r}, {len(out)} caratteri originali")
        return (
            out[:self.TOOL_OUTPUT_CAP]
            + f"\n\n[OUTPUT TRONCATO: erano {len(out)} caratteri totali, mostrati "
            f"i primi {self.TOOL_OUTPUT_CAP}. Se serve il resto, leggi il file "
            "a pezzi (es. head/tail/sed -n) o usa run_command con grep/wc per "
            "estrarre solo ciò che serve.]"
        )

    def _safe_path(self, cwd: Path, relative_path: str) -> Optional[Path]:
        # Guardrail anti-traversal: il path risolto deve restare dentro la
        # root. Con write_file un "../" può autodistruggere file esterni,
        # con read_file può esfiltrare segreti (es. API key in ~/.bashrc)
        # dentro la history. None = negato.
        path = (cwd / relative_path).resolve()
        if not path.is_relative_to(self.root):
            logging.warning(f"Path traversal bloccato: {relative_path!r} risolve fuori root ({path})")
            return None
        return path

    # Snapshot preventivo (anti-autodistruzione): fotografa il repo PRIMA di
    # ogni operazione che può alterare i file. Meccanismo: indice git
    # temporaneo (GIT_INDEX_FILE) + write-tree + commit-tree + ref dedicata
    # in refs/gas/snapshots/ — include anche i file non tracciati (che
    # "git stash create" ignorerebbe) e non tocca né il branch né la staging
    # area dell'utente. Il ripristino è SOLO umano (vedi README): nessun tool
    # di restore è esposto ai modelli.
    # Retention IBRIDA (TASK C): si tiene l'UNIONE di (ultimi SNAPSHOT_KEEP) e
    # (più giovani di SNAPSHOT_KEEP_DAYS). I recenti sopravvivono anche a una
    # sessione che ruota >100 ref. La rimozione dei ref oltre policy è LOGGATA;
    # l'oggetto resta recuperabile finché non gira `git gc` (mai automatico, §10).
    SNAPSHOT_KEEP = 100
    SNAPSHOT_KEEP_DAYS = 7
    SNAPSHOT_LOG_MAX_BYTES = 1_000_000  # rotazione semplice di snapshots.log (.1)

    def _snapshot(self, trigger: str, target: str) -> Optional[str]:
        """Fotografa lo stato corrente del repo (file tracciati E non tracciati)
        in un commit fuori-branch referenziato da refs/gas/snapshots/<ts>-<sha8>.
        Ritorna lo SHA dello snapshot; None se fallisce — chi chiama DEVE
        trattare None come blocco dell'operazione (fail-closed)."""
        import shutil
        import tempfile
        import time
        tmpdir = tempfile.mkdtemp(prefix="gas_snap_idx_")
        try:
            env = os.environ.copy()
            # Indice temporaneo: non sporca la staging area dell'utente
            env["GIT_INDEX_FILE"] = os.path.join(tmpdir, "index")
            # Identità esplicita: commit-tree fallirebbe senza user.name/email
            env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "gas-snapshot"
            env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "gas@kernel"

            def git(*args: str) -> str:
                res = subprocess.run(["git", "-C", str(self.root), *args],
                                     env=env, capture_output=True, text=True, timeout=30)
                if res.returncode != 0:
                    raise RuntimeError(f"git {args[0]}: {res.stderr.strip()[:200]}")
                return res.stdout.strip()

            # Riserva R1 (review #3): git -C risale ai repo genitori. Se la
            # root non ha un proprio .git, lo snapshot fotograferebbe il repo
            # SBAGLIATO e l'operazione passerebbe: fail-closed esplicito.
            toplevel = git("rev-parse", "--show-toplevel")
            if Path(toplevel).resolve() != self.root:
                raise RuntimeError(f"la root {self.root} non è la radice di un repo git (toplevel: {toplevel})")
            git("add", "-A")  # a differenza di stash create, prende anche i non tracciati
            # La memoria di Gas è gitignorata ma va protetta quanto il codice
            if (self.root / ".gas_history.json").exists():
                git("add", "-f", "--", ".gas_history.json")
            tree = git("write-tree")
            head = subprocess.run(["git", "-C", str(self.root), "rev-parse", "--verify", "-q", "HEAD"],
                                  env=env, capture_output=True, text=True, timeout=30)
            parent = ["-p", head.stdout.strip()] if head.returncode == 0 else []
            sha = git("commit-tree", tree, *parent, "-m", f"gas snapshot [{trigger}] {target}")
            # Timestamp a nanosecondi: i ref ordinano lessicograficamente =
            # cronologicamente, anche con più snapshot nello stesso secondo
            ns = time.time_ns()
            ts = time.strftime("%Y%m%d-%H%M%S", time.localtime(ns // 1_000_000_000)) + f".{ns % 1_000_000_000:09d}"
            ref = f"refs/gas/snapshots/{ts}-{sha[:8]}"
            git("update-ref", ref, sha)
        except Exception as e:
            logging.warning(f"Snapshot FALLITO [{trigger}] su {target!r}: {e} — operazione bloccata (fail-closed)")
            return None
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

        # Da qui in poi lo snapshot ESISTE: errori di contorno (indice
        # leggibile, retention) non bloccano l'operazione, solo warning.
        _snapshot_log.info(f"Snapshot creato [{trigger}] su {target!r}: {sha} ({ref})")
        try:
            index_file = self.root / "reports" / "snapshots.log"
            index_file.parent.mkdir(parents=True, exist_ok=True)
            with open(index_file, "a", encoding="utf-8") as f:
                f.write(f"{ts}  {sha}  {trigger}  {target}\n")
            # Rotazione semplice (.1): quando si supera il cap, l'attuale diventa
            # snapshots.log.1 (sovrascrive il precedente) e si riparte da vuoto.
            if index_file.stat().st_size > self.SNAPSHOT_LOG_MAX_BYTES:
                index_file.replace(index_file.parent / "snapshots.log.1")
        except Exception as e:
            logging.warning(f"Indice reports/snapshots.log non aggiornato: {e}")
        try:
            res = subprocess.run(["git", "-C", str(self.root), "for-each-ref",
                                  "--format=%(refname)", "refs/gas/snapshots/"],
                                 capture_output=True, text=True, timeout=30)
            refs = res.stdout.split()  # for-each-ref ordina lessicograficamente
            import time as _t
            _, drop = _snapshot_retention(refs, _t.time(),
                                          self.SNAPSHOT_KEEP, self.SNAPSHOT_KEEP_DAYS)
            for old in drop:
                subprocess.run(["git", "-C", str(self.root), "update-ref", "-d", old],
                               capture_output=True, text=True, timeout=30)
                # Rimozione LOGGATA: l'oggetto resta recuperabile fino a `git gc`.
                _snapshot_log.info(f"Retention: ref oltre policy rimosso {old} "
                                   f"(oggetto recuperabile fino a git gc)")
        except Exception as e:
            logging.warning(f"Retention snapshot non applicata: {e}")
        return sha

    # --- Sandbox run_command (chiude l'esfiltrazione naïve via shell) ---
    # Allowlist di binari di SOLA LETTURA: nessuno di questi può aprire socket,
    # avviare sottoprocessi (niente awk/sed -e/find -exec/xargs: bypasserebbero
    # il controllo) né scrivere su un path passato come FLAG. Tutto il resto è
    # negato con un messaggio esplicito. Estendere questa lista con interpreti
    # (python, bash...) RIAPRE l'esecuzione di codice arbitrario: è una scelta
    # consapevole dell'operatore, non il default.
    SHELL_ALLOWLIST = frozenset({
        "ls", "cat", "head", "tail", "wc", "grep", "echo", "pwd", "date",
        "stat", "file", "uniq", "cut", "tr", "nl", "diff", "comm", "true",
        "false", "basename", "dirname", "printf", "seq", "rev",
    })
    # Variabili d'ambiente da rimuovere dai processi figli: qualsiasi cosa che
    # somigli a un segreto. Toglie il bersaglio principale dell'esfiltrazione
    # anche se restasse un buco a monte. PATH/HOME/LANG restano (servono ai
    # binari e nessuno contiene questi marcatori).
    SHELL_ENV_SENSITIVE_MARKERS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL", "AUTH")

    def _sanitized_subprocess_env(self) -> Dict[str, str]:
        """Copia dell'ambiente con le variabili sensibili (API key, token...)
        rimosse, da passare ai processi figli di run_command."""
        env = os.environ.copy()
        for var in list(env):
            up = var.upper()
            if any(marker in up for marker in self.SHELL_ENV_SENSITIVE_MARKERS):
                env.pop(var, None)
        return env

    def _bwrap_prefix(self, cwd: Path) -> List[str]:
        """Prefisso bwrap (fino a '--') per confinare run_command a livello OS.
        Profilo (decisione §6.1):
        - --unshare-net: nessuna rete (solo loopback) → niente esfiltrazione;
        - --unshare-pid --proc /proc: PID namespace isolato + procfs pulita;
        - --new-session --die-with-parent: niente TTY ereditato, il figlio muore
          col kernel di Gas;
        - --ro-bind / /: tutto il filesystem in SOLA LETTURA;
        - --tmpfs /home --tmpfs /root --tmpfs /run: MASCHERANO le home (chiavi,
          token, ~/.ssh, ~/.config): non leggibili nemmeno se un buco nel vetting
          passasse un path lì sotto (chiude R2 anche in lettura);
        - --ro-bind <root> <root> PER ULTIMO: ri-espone in RO la sola project
          root, così i comandi leciti leggono i file del progetto anche se la
          root sta sotto /home (caso VPS), DOPO che il tmpfs l'ha mascherata;
        - --clearenv + --setenv di ogni var GIÀ sanificata: env del figlio
          controllata esattamente (PATH incluso, segreti esclusi a monte)."""
        env = self._sanitized_subprocess_env()
        prefix: List[str] = [
            "bwrap",
            "--unshare-net", "--unshare-pid", "--proc", "/proc",
            "--new-session", "--die-with-parent",
            "--ro-bind", "/", "/",
            "--tmpfs", "/home", "--tmpfs", "/root", "--tmpfs", "/run",
            "--ro-bind", str(self.root), str(self.root),
            "--chdir", str(cwd),
            "--clearenv",
        ]
        for var, val in env.items():
            prefix += ["--setenv", var, val]
        prefix.append("--")
        return prefix

    def _vet_command(self, command: str, cwd: Path) -> Tuple[Optional[List[str]], Optional[str]]:
        """Vetting fail-closed di un comando PRIMA di eseguirlo o fotografarlo.
        Ritorna (argv, None) se consentito, (None, motivo) se negato.
        Tre barriere: (1) parsing senza shell — pipe/redirezioni/$(...) restano
        testo o rompono il parse; (2) argv[0] nell'allowlist; (3) ogni altro
        token risolto con _safe_path (lo stesso di T10: .resolve() segue anche
        i symlink) deve restare dentro la root."""
        try:
            argv = shlex.split(command)
        except ValueError as e:
            return None, (f"Operazione negata: comando non interpretabile ({e}). "
                          "run_command non usa una shell: virgolette ed escape "
                          "devono essere bilanciati. (fail-closed)")
        if not argv:
            return None, "Operazione negata: comando vuoto. (fail-closed)"
        binario = argv[0]
        if binario not in self.SHELL_ALLOWLIST:
            return None, (
                f"Operazione negata: comando '{binario}' non consentito. "
                "run_command esegue SOLO comandi di sola lettura da una "
                "allowlist, senza shell: niente pipe, redirezioni, "
                "concatenazioni, command substitution, interpreti o rete. Per "
                "scrivere file usa write_file, per leggerli usa read_file. "
                "(fail-closed)")
        for token in argv[1:]:
            if self._safe_path(cwd, os.path.expanduser(token)) is None:
                return None, (
                    f"Operazione negata: l'argomento '{token}' risolve fuori "
                    "dalla root di Gas. run_command può toccare solo percorsi "
                    "interni al progetto. (fail-closed)")
        return argv, None

    @staticmethod
    def _riassumi_args(name: str, args_str: Any) -> str:
        """Sintesi compatta degli argomenti di una tool call, per il diario.
        Non deve mai sollevare: argomenti illeggibili -> placeholder."""
        try:
            args = json.loads(args_str) if isinstance(args_str, str) else (args_str or {})
        except Exception:
            return "<argomenti non parsabili>"
        if not isinstance(args, dict):
            return str(args)[:120]
        if name == "run_command":
            return f"command={str(args.get('command', ''))[:160]!r}"
        if name in ("write_file", "read_file"):
            return f"path={str(args.get('relative_path', ''))[:160]!r}"
        if name == "salva_contatto":
            return f"contatto chiave={str(args.get('chiave', ''))[:80]!r}"
        if name == "imposta_stato_contatto":
            return (f"chiave={str(args.get('chiave', ''))[:80]!r} "
                    f"stato={str(args.get('stato', ''))[:40]!r}")
        if name == "unisci_contatti":
            return (f"da={str(args.get('chiave_da', ''))[:80]!r} "
                    f"verso={str(args.get('chiave_verso', ''))[:80]!r}")
        if name == "ricorda":
            return (f"query={str(args.get('query', '') or '')[:60]!r} "
                    f"contatto={str(args.get('contatto', '') or '')[:60]!r}")
        # tool sconosciuto: dump compatto delle chiavi (difensivo)
        return ", ".join(f"{k}={str(v)[:60]!r}" for k, v in args.items())[:200]

    @staticmethod
    def _esito_sintetico(out: str) -> str:
        """Esito sintetico di una tool call a partire dal suo output testuale.
        L'esito NEGATIVO è incluso: i rami di errore/diniego del kernel
        iniziano con 'Errore eseguendo' o 'Operazione negata'."""
        s = (out or "").strip()
        negativo = s.startswith("Errore eseguendo") or s.startswith("Operazione negata")
        snippet = s.replace("\n", " ")[:160]
        return f"[{'KO' if negativo else 'OK'}] {snippet}"

    def _diario_log(self, tipo: str, descrizione: str) -> None:
        """Registra UN evento nel diario della memoria, in modo FAIL-SAFE (§9):
        la memoria che non scrive NON deve MAI interrompere il turno. La memoria
        assente/degradata o qualunque errore vengono solo loggati nella scatola
        nera; il loop agentico prosegue. Scrittura IN-PROCESS (codice fidato del
        kernel, bypassa correttamente il sandbox bwrap di run_command)."""
        if self.memory is None:
            return
        try:
            self.memory.append_diario(tipo, descrizione)
        except Exception as e:
            # append_diario è già blindato (ritorna None in degrado); questa è
            # solo una cintura ulteriore perché il loop non cada MAI per il diario.
            logging.warning(f"diario non scritto ({tipo}): {e}")

    def _memoria_backup_auto(self) -> None:
        """Backup automatico THROTTLED del DB di memoria: backup LOCALE (anti
        auto-corruzione) + backup OFF-SITE (anti-disastro-disco, solo se
        GAS_MEMORY_BACKUP_OFFSITE_DIR è configurata). Entrambi THROTTLED e con
        throttle SEPARATI (la dir esterna può essere lenta). FAIL-SAFE §9: memoria
        assente/degradata o qualunque errore → il turno PROSEGUE, mai crash."""
        if self.memory is None:
            return
        try:
            self.memory.backup_auto(self.MEMORY_BACKUP_EVERY_SEC,
                                    keep=self.MEMORY_BACKUP_KEEP)
        except Exception as e:
            logging.warning(f"backup memoria locale saltato: {e}")
        # Backup off-site (solo se configurato): throttle separato, fail-safe §9.
        if self.MEMORY_BACKUP_OFFSITE_DIR is not None:
            try:
                self.memory.backup_offsite_auto(
                    self.MEMORY_BACKUP_OFFSITE_DIR,
                    self.MEMORY_BACKUP_OFFSITE_EVERY_SEC,
                    keep=self.MEMORY_BACKUP_OFFSITE_KEEP,
                )
            except Exception as e:
                logging.warning(f"backup off-site saltato: {e}")

    def _vettori_catchup(self) -> None:
        """Catch-up indexing del vector store: indicizza nel sidecar le righe di
        diario NUOVE oltre il watermark, una volta per turno e BOUNDED (al più
        VEC_CATCHUP_MAX righe). Pigro (solo l'arretrato, non un rebuild) e
        incrementale: l'arretrato grande si recupera in più turni senza picchi.
        FAIL-SAFE §9: vector store assente/degradato, memoria assente o qualunque
        errore → no-op, il turno PROSEGUE, mai crash. L'indice è una cache derivata:
        un buco si auto-recupera al turno dopo (o con un rebuild manuale)."""
        if self.vectors is None or not self.vectors.available or self.memory is None:
            return
        try:
            if self._vec_watermark is None:
                # primo turno: riparte dall'ultimo id già indicizzato nel sidecar
                self._vec_watermark = self.vectors.max_source_ref("diario") or 0
            righe = self.memory.diario_dopo(self._vec_watermark, limit=self.VEC_CATCHUP_MAX)
            if not righe:
                return
            items = [("diario", r["id"], r["descrizione"], r["ts"]) for r in righe]
            n = self.vectors.index_batch(items)
            if n:  # avanza il watermark SOLO se l'indicizzazione è riuscita
                self._vec_watermark = max(int(r["id"]) for r in righe)
        except Exception as e:
            logging.warning(f"catch-up vettoriale saltato: {e}")

    def _fmt_evento_datato(self, e: Dict[str, Any]) -> str:
        """Formatta UN evento di diario per il retrieval: datato col `ts` SORGENTE e,
        se l'evento è legato a un lead (contatto_id), affiancato dallo stato CORRENTE
        del lead letto live dalla rubrica. Così il ricordo resta un EVENTO episodico
        passato, ma chi legge vede subito se quel fatto è ancora valido ("la memoria
        non mente" anche in lettura). Lo stato si legge a runtime, NON si denormalizza
        nel sidecar (cache derivata)."""
        ts = str(e.get("ts") or "")[:10]
        testo = e.get("descrizione")
        riga = f"- [{ts}] {testo}" if ts else f"- {testo}"
        cid = e.get("contatto_id")
        if cid and self.memory is not None:
            try:
                c = self.memory.get_contatto(int(cid))
            except (TypeError, ValueError):
                c = None
            if c:
                nome = c.get("nome") or c.get("chiave") or "?"
                riga += f" — lead {nome}: oggi '{c.get('stato')}'"
        return riga

    def _memoria_pin(self) -> str:
        """Blocco di memoria ALWAYS-ON (lato lettura, fetta 2b) da appendere al
        system prompt: riassunto COMPATTO e CAPATO di lead attivi + poche azioni
        recenti significative (escluso il rumore di lettura). Sta NEL messaggio
        system (FUORI dalla finestra) → NON passa da _get_window/_cap_window_chars,
        la finestra conversazionale resta intatta; il pin è limitato dal suo cap
        dedicato MEMORY_PIN_CHAR_CAP. Si calcola UNA volta per turno (no eco delle
        azioni in corso, no query ripetute nel loop a 10 iterazioni).

        Fail-safe (§9): memoria None/degradata o qualunque errore → stringa
        vuota, il turno prosegue. Ritorna "" (niente da iniettare) oppure il
        blocco già preceduto da due newline, pronto per `system_prompt + pin`."""
        if self.memory is None:
            return ""
        try:
            righe: List[str] = []
            attivi = [c for c in self.memory.lista_contatti()
                      if c.get("stato") not in STATI_CHIUSI][:self.MEMORY_PIN_CONTACTS]
            if attivi:
                righe.append("## Lead attivi")
                for c in attivi:
                    nome = c.get("nome") or c.get("chiave") or "?"
                    pa = f" → prossima: {c['prossima_azione']}" if c.get("prossima_azione") else ""
                    ult = f" (ultimo: {str(c['ultimo_contatto'])[:10]})" if c.get("ultimo_contatto") else ""
                    righe.append(f"- {nome} [{c.get('stato')}]{pa}{ult}")
            # eventi recenti, escluso il rumore di lettura. Si scandisce una
            # finestra AMPIA e bounded (MEMORY_PIN_SCAN) e si filtra, così anche
            # con rumore denso le azioni vere poco più indietro emergono (R3).
            eventi = [e for e in self.memory.diario_recente(self.MEMORY_PIN_SCAN)
                      if e.get("tipo") not in self.DIARIO_NOISE_TIPI][:self.MEMORY_PIN_EVENTS]
            if eventi:
                righe.append("## Ultime azioni")
                for e in eventi:
                    righe.append(f"- [{e.get('tipo')}] {e.get('descrizione')}")
            if not righe:
                return ""
            blocco = ("# MEMORIA (sola lettura — usa il tool 'ricorda' per "
                      "approfondire il diario o un lead)\n" + "\n".join(righe))
            # Tetto rigido del pin (stesso principio di _cap_tool_output: tronco
            # il TESTO, non sequenze di messaggi → niente slicing della storia).
            # Taglio all'ultima riga intera per non lasciare una riga monca.
            if len(blocco) > self.MEMORY_PIN_CHAR_CAP:
                tagliato = blocco[:self.MEMORY_PIN_CHAR_CAP].rsplit("\n", 1)[0]
                blocco = tagliato + "\n…[memoria troncata]"
            return "\n\n" + blocco
        except Exception as e:
            logging.warning(f"_memoria_pin fallito: {e}")
            return ""

    def _trova_contatto(self, termine: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Risolve un termine a UN contatto. Priorità: (1) match ESATTO sulla
        chiave (via indice UNIQUE); (2) altrimenti substring case-insensitive su
        chiave+nome. Ritorna (contatto|None, nota_ambiguità|None): se il substring
        trova PIÙ lead si prende il più recente ma si SEGNALA l'ambiguità invece di
        sceglierne uno in silenzio (riserva R1 fetta 2b). Fail-safe: memoria
        None/degradata → (None, None)."""
        if self.memory is None:
            return None, None
        esatto = self.memory.get_contatto_per_chiave(termine)
        if esatto:
            return esatto, None
        # Substring case-insensitive con collasso del whitespace su ENTRAMBI i lati
        # (riuso normalizza_chiave SOLO ai fini del confronto, non muta nulla):
        # needle e haystack (chiave+nome) sono normalizzati al volo, così un needle
        # con spazi multipli ("anna   rossi") combacia con la chiave storata (già
        # normalizzata) "anna rossi". Il nome non è normalizzato in storage ma qui
        # viene canonicalizzato solo per il match, simmetrico al needle.
        ago = normalizza_chiave(termine)
        cand = [c for c in self.memory.lista_contatti()
                if ago in (normalizza_chiave(c.get("chiave", "")) + " "
                           + normalizza_chiave(c.get("nome", "")))]
        if not cand:
            return None, None
        if len(cand) == 1:
            return cand[0], None
        # lista_contatti è ordinata per aggiornato_il DESC → cand[0] è il più recente
        nomi = ", ".join((c.get("nome") or c.get("chiave") or "?") for c in cand[:5])
        nota = (f"⚠ {len(cand)} lead corrispondono a '{termine}' ({nomi}…); mostro il "
                f"più recente. Usa la chiave esatta per disambiguare.")
        return cand[0], nota

    def _ricorda(self, query: Optional[str] = None, contatto: Optional[str] = None,
                 n: int = 10) -> str:
        """Lettura on-demand della memoria (tool 'ricorda'). SOLA LETTURA: nessuna
        scrittura/mutazione. Output compatto (poi capato da _cap_tool_output come
        ogni tool). Fail-safe: memoria None/degradata → messaggio gentile, mai
        crash (le letture di MemoryStore degradano già a [])."""
        if self.memory is None:
            return "Memoria non disponibile: nessun ricordo accessibile."
        try:
            n = max(1, min(int(n or 10), 50))
        except (TypeError, ValueError):
            n = 10
        parti: List[str] = []
        # 1) scheda + storia di un lead specifico (chiave esatta o nome)
        if contatto:
            match, nota = self._trova_contatto(str(contatto))
            if match:
                if nota:
                    parti.append(nota)
                parti.append(
                    f"CONTATTO {match.get('nome') or match.get('chiave')} "
                    f"[{match.get('stato')}] — prossima: "
                    f"{match.get('prossima_azione') or '—'} — note: "
                    f"{match.get('note') or '—'}")
                eventi = self.memory.diario_di_contatto(int(match["id"]))[:n]
                parti.append("Storia:")
                parti += ([f"- [{e['tipo']}] {e['descrizione']}" for e in eventi]
                          or ["- (nessun evento)"])
            else:
                parti.append(f"Nessun lead trovato per '{contatto}'.")
        # 2) ricerca testuale nel diario. Prima la ricerca FTS5 (Strato A del
        #    Vector DB): per parole/radici, ordinata per pertinenza. Se FTS è
        #    assente o non trova nulla, si ricade sulla ricerca substring storica
        #    (pavimento sempre disponibile, comportamento invariato) — cascata
        #    fail-safe §9, mai un buco di funzionalità.
        if query:
            # Cascata NON regressiva (rivista rispetto a §FINALE dopo misura dal vivo
            # della qualità semantica del MiniLM, R-wire-1):
            #   (1) FTS5 (cerca_diario) = BASE, precisione lessicale, comportamento
            #       ODIERNO preservato (mai soppresso dal semantico);
            #   (2) SEMANTICO = RIEMPIE i posti liberi fino a n (recall per SIGNIFICATO:
            #       'preventivo' può ripescare 'offerta'), saltando i duplicati di FTS.
            #       Opt-in/fail-safe: salta se spento/degradato. Gli hit (source_ref =
            #       id diario) si risolvono alle righe complete (ts + contatto_id);
            #   (3) substring storico = ultimo pavimento se tutto il resto è vuoto.
            hit: List[Dict[str, Any]] = self.memory.cerca_diario(str(query), n)
            if len(hit) < n and self.vectors is not None and self.vectors.available:
                visti = {e.get("id") for e in hit}
                try:
                    sem = self.vectors.search(str(query), k=n,
                                              min_sim=self.VEC_MIN_SIM, source="diario")
                except Exception as ex:
                    logging.warning(f"ricerca semantica saltata: {ex}")
                    sem = []
                for h in sem:
                    try:
                        row = self.memory.get_diario(int(h["source_ref"]))
                    except (TypeError, ValueError):
                        row = None
                    if row and row.get("id") not in visti:
                        hit.append(row)
                        visti.add(row.get("id"))
                        if len(hit) >= n:
                            break
            if not hit:
                q = str(query).lower()
                hit = [e for e in self.memory.diario_recente(200)
                       if q in str(e.get("descrizione", "")).lower()
                       or q in str(e.get("tipo", "")).lower()][:n]
            parti.append(f"Diario per '{query}' ({len(hit)}):")
            parti += ([self._fmt_evento_datato(e) for e in hit]
                      or ["- (nessun risultato)"])
        # 3) default: ultimi eventi del diario
        if not contatto and not query:
            eventi = self.memory.diario_recente(n)
            parti.append(f"Ultimi {len(eventi)} eventi del diario:")
            parti += ([f"- [{e['tipo']}] {e['descrizione']}" for e in eventi]
                      or ["- (diario vuoto)"])
        return "\n".join(parti) if parti else "Nessun ricordo."

    def _salva_contatto(self, args: Dict[str, Any]) -> str:
        """Crea/aggiorna un lead nella rubrica (tool salva_contatto). Scrittura
        in-process fidata (parametrizzata, niente SQL grezzo dal modello). NON
        tocca lo stato del funnel (separazione identità/ciclo di vita, come
        upsert_contatto). Fail-safe: memoria assente/degradata → messaggio, mai
        crash."""
        if self.memory is None:
            return "Memoria non disponibile: contatto non salvato."
        chiave = str(args.get("chiave") or "").strip()
        if not chiave:
            return "Operazione negata: 'chiave' obbligatoria per salvare un contatto."
        cid = self.memory.upsert_contatto(
            chiave=chiave, nome=args.get("nome"), contatto=args.get("contatto"),
            prossima_azione=args.get("prossima_azione"), note=args.get("note"))
        if cid is None:
            return f"Memoria in degrado: contatto '{chiave}' non salvato."
        # Mostra la chiave nella forma CANONICA persistita (normalizzata), così
        # schermo e DB coincidono (chiude R-crm-norm-1).
        return f"Successo: contatto '{normalizza_chiave(chiave)}' salvato (id={cid})."

    def _imposta_stato_contatto(self, args: Dict[str, Any]) -> str:
        """Transizione di stato di un lead esistente (tool imposta_stato_contatto).
        Il lead deve esistere (match ESATTO sulla chiave: una transizione di stato
        non può essere ambigua). Valida lo stato prima di toccare il DB. Fail-safe:
        memoria/lead assenti → messaggio chiaro, mai crash."""
        if self.memory is None:
            return "Memoria non disponibile: stato non aggiornato."
        chiave = str(args.get("chiave") or "").strip()
        stato = str(args.get("stato") or "").strip()
        if not chiave or not stato:
            return "Operazione negata: servono sia 'chiave' sia 'stato'."
        if stato not in STATI_CONTATTO:
            return (f"Operazione negata: stato '{stato}' non valido. "
                    f"Ammessi: {', '.join(STATI_CONTATTO)}.")
        c = self.memory.get_contatto_per_chiave(chiave)
        if c is None:
            return (f"Operazione negata: nessun lead con chiave '{chiave}'. "
                    f"Crealo prima con salva_contatto.")
        ok = self.memory.update_stato_contatto(
            int(c["id"]), stato, prossima_azione=args.get("prossima_azione"))
        # Chiave nella forma CANONICA persistita (chiude R-crm-norm-1).
        return (f"Successo: lead '{normalizza_chiave(chiave)}' ora in stato '{stato}'." if ok
                else f"Memoria in degrado: stato di '{chiave}' non aggiornato.")

    def _unisci_contatti(self, args: Dict[str, Any]) -> str:
        """Fonde due schede dello stesso lead: es. quando si scopre che 'Anna' e
        'anna@ex.com' sono la stessa persona (R-crm-1b). Merge a lapide, NON
        distruttivo (vedi MemoryStore.unisci_contatti): non cancella nulla, la
        storia resta. Entrambe le chiavi devono esistere. Fail-safe: memoria/lead
        assenti → messaggio chiaro, mai crash.

        ⚠ OPERAZIONE DI MANUTENZIONE UMANA, NON un tool autopilot. NON è cablata al
        dispatcher dei tool (execute_tool_call) e il modello non può invocarla da
        sé: il merge è mutante e IRREVERSIBILE (lossy, COALESCE senza inverso
        pulito), stessa classe del restore di snapshot e del git gc — solo umano.
        Il dedup mancato è recuperabile, un merge errato no. Il metodo resta come
        helper richiamabile per l'uso manuale/futuro; il MECCANISMO di merge in
        MemoryStore resta intatto."""
        if self.memory is None:
            return "Memoria non disponibile: contatti non uniti."
        da = str(args.get("chiave_da") or "").strip()
        verso = str(args.get("chiave_verso") or "").strip()
        if not da or not verso:
            return "Operazione negata: servono sia 'chiave_da' sia 'chiave_verso'."
        if self.memory.get_contatto_per_chiave(da) is None:
            return (f"Operazione negata: nessun lead con chiave '{da}'. "
                    f"Nulla da unire.")
        if self.memory.get_contatto_per_chiave(verso) is None:
            return (f"Operazione negata: nessun lead con chiave '{verso}'. "
                    f"Nulla da unire.")
        cid = self.memory.unisci_contatti(da, verso)
        if cid is None:
            return f"Memoria in degrado: '{da}' e '{verso}' non uniti."
        return (f"Successo: lead '{da}' unito in '{verso}' "
                f"(lead canonico id={cid}). La storia è stata preservata.")

    def execute_tool_call(self, name: str, args_str: Any) -> str:
        try:
            args = json.loads(args_str) if isinstance(args_str, str) else args_str
            cwd = Path(os.environ.get("GAS_CWD", str(self.root)))
            if name == "run_command":
                command = args["command"]
                # 1) Vetting PRIMA di tutto: i comandi negati non sprecano
                #    nemmeno uno snapshot (mitiga in parte R2).
                argv, motivo = self._vet_command(command, cwd)
                if argv is None:
                    logging.warning(f"run_command negato: {command!r}")
                    return motivo
                # 2) Dry-run: anteprima fedele, non esegue e non fotografa.
                if self.shell_mode == "dry_run":
                    _snapshot_log.info(f"[DRY-RUN] comando consentito, non eseguito: {command!r}")
                    return f"[DRY-RUN] comando consentito ma NON eseguito (modalità dry-run): {command}"
                # 3) Check sandbox OS per mode (§6.3) — PRIMA dello snapshot
                #    (riordino R1 #6). In os_strict il confinamento OS è
                #    obbligatorio: se manca, il comando NON viene eseguito
                #    (fail-closed) e il rifiuto NON deve sprecare uno snapshot.
                #    In os_with_fallback NON si nega qui: si degrada alla sola
                #    sandbox applicativa e il comando gira davvero (lo snapshot
                #    al passo 4 serve, perché c'è un'esecuzione da fotografare).
                if not self.os_sandbox_available and self.sandbox_mode == "os_strict":
                    logging.warning(
                        f"run_command negato: sandbox OS assente "
                        f"({self._os_sandbox_detail}) e GAS_SANDBOX_MODE=os_strict")
                    return ("Operazione negata: sandbox OS (bwrap + namespace) "
                            "non disponibile e GAS_SANDBOX_MODE=os_strict, "
                            "comando non eseguito (fail-closed). Usa "
                            "GAS_SANDBOX_MODE=os_with_fallback per accettare la "
                            "sola sandbox applicativa, oppure avvia 'gas doctor' "
                            "per la diagnosi. Dettagli in gas_debug.log.")
                # 4) Snapshot preventivo solo ora che eseguiremo davvero (in
                #    bwrap se disponibile, altrimenti app-layer in os_with_fallback).
                if self._snapshot("run_command", command[:120]) is None:
                    return ("Operazione negata: snapshot preventivo fallito, "
                            "comando non eseguito (fail-closed). Dettagli in "
                            "gas_debug.log.")
                # 5) Esecuzione SENZA shell (argv già parsato) e con env
                #    ripulita dalle variabili sensibili. Dove disponibile, dentro
                #    il sandbox OS (rete chiusa, fs read-only); altrimenti
                #    (os_with_fallback) sola sandbox applicativa.
                if self.os_sandbox_available:
                    exec_argv = self._bwrap_prefix(cwd) + argv
                else:
                    logging.warning(
                        "run_command in fallback applicativo: sandbox OS assente "
                        "(GAS_SANDBOX_MODE=os_with_fallback)")
                    exec_argv = argv
                res = subprocess.run(exec_argv, shell=False, cwd=cwd,
                                     capture_output=True, text=True, timeout=60,
                                     env=self._sanitized_subprocess_env())
                out = res.stdout + res.stderr
            elif name == "write_file":
                # Guardrail: la memoria è gestita solo dal kernel, mai dai modelli
                # (llama su Groq allucina scritture su varianti di gas_history)
                normalized = args["relative_path"].lower().replace("-", "_").replace(" ", "_")
                if "gas_history" in normalized:
                    return ("Operazione negata: la memoria di Gas è gestita "
                            "automaticamente dal kernel, non scriverla mai.")
                path = self._safe_path(cwd, args["relative_path"])
                if path is None:
                    return (f"Operazione negata: il percorso '{args['relative_path']}' "
                            "esce dalla root di Gas. Usa solo percorsi relativi "
                            "interni al progetto.")
                # Snapshot preventivo DOPO la validazione del path: fotografa
                # lo stato prima di sovrascrivere
                if self._snapshot("write_file", args["relative_path"]) is None:
                    return ("Operazione negata: snapshot preventivo fallito, "
                            "file non scritto (fail-closed). Dettagli in "
                            "gas_debug.log.")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(args["content"], encoding="utf-8")
                out = f"Successo: File {args['relative_path']} aggiornato."
            elif name == "read_file":
                path = self._safe_path(cwd, args["relative_path"])
                if path is None:
                    return (f"Operazione negata: il percorso '{args['relative_path']}' "
                            "esce dalla root di Gas. Usa solo percorsi relativi "
                            "interni al progetto.")
                out = path.read_text(encoding="utf-8")
            elif name == "ricorda":
                # Lettura della memoria di lungo periodo. SOLA LETTURA, in-process
                # (codice fidato): non tocca il filesystem né la rete, non passa
                # dal sandbox di run_command. Nessuno snapshot (non muta nulla).
                out = self._ricorda(args.get("query") if isinstance(args, dict) else None,
                                    args.get("contatto") if isinstance(args, dict) else None,
                                    args.get("n", 10) if isinstance(args, dict) else 10)
            elif name == "salva_contatto":
                # Scrittura nella rubrica, in-process (codice fidato): niente FS/
                # rete, niente sandbox/snapshot. La riga viene comunque tracciata
                # nel diario dal loop (fetta 2a). SQL parametrizzato in MemoryStore.
                out = self._salva_contatto(args if isinstance(args, dict) else {})
            elif name == "imposta_stato_contatto":
                out = self._imposta_stato_contatto(args if isinstance(args, dict) else {})
            else:
                # unisci_contatti NON è più un tool autopilot: il merge di lead è
                # mutante e irreversibile (lossy), quindi è MANUTENZIONE UMANA e non
                # passa più di qui (vedi _unisci_contatti). Il meccanismo di merge
                # in MemoryStore resta intatto. Tool ignoto → diniego pulito.
                return "Tool non trovato."
            return self._cap_tool_output(name, args, out)
        except Exception as e:
            return f"Errore eseguendo {name}: {str(e)}"

    def run_turn(self, user_prompt: str) -> Generator[Dict[str, Any], None, None]:
        self._add_to_history("user", content=user_prompt)

        from brains.router import classifica_compito
        compito = classifica_compito(user_prompt)

        # Iniezione memoria ALWAYS-ON (fetta 2b): calcolata UNA volta per turno
        # (no eco delle azioni in corso, no query ripetute nel loop a 10 iter).
        # Vive nel messaggio system (system_prompt + mem_pin), FUORI dalla
        # finestra: _get_window/_cap_window_chars restano intatti. Fail-safe:
        # "" se la memoria è assente/degradata.
        mem_pin = self._memoria_pin()

        # Backup automatico THROTTLED del DB di memoria (anti auto-corruzione):
        # una volta per turno valuta se è ora di una copia coerente; il throttling
        # e l'integrità sono gestiti da MemoryStore.backup_auto. Fail-safe: non
        # interrompe mai il turno.
        self._memoria_backup_auto()

        # Catch-up indexing del vector store (retrieval semantico): indicizza le
        # nuove righe di diario nel sidecar, una volta per turno e BOUNDED, FUORI dal
        # loop dei provider. No-op se GAS_VECTORS è spento o il layer è degradato.
        self._vettori_catchup()

        # Endpoint/modelli dalle costanti di modulo (punto unico, condiviso con doctor).
        # Pavimento offline Ollama: NON gira nel Codespace. Sul PC/VPS si esporta
        # GAS_OLLAMA_URL=http://localhost:11434/v1 (endpoint OpenAI-compatibile di
        # Ollama). Se la variabile e' assente, il rung viene saltato dal gate del
        # loop (`if not os.environ.get(env): continue`) -> skip pulito, mai crash.
        OLLAMA_URL = os.environ.get("GAS_OLLAMA_URL")

        # Rung GRATUITI, sempre ULTIMI: rete di salvataggio a budget zero.
        # Ollama: la "chiave" del gate e' GAS_OLLAMA_URL (presenza), percio'
        # api_key=base_url=URL: Ollama ignora la chiave, e' deliberato.
        FREE_RUNGS = [
            ("openrouter", "OPENROUTER_API_KEY", OPENROUTER_URL, OPENROUTER_FREE_MODEL),
            ("ollama",     "GAS_OLLAMA_URL",     OLLAMA_URL,     OLLAMA_MODEL),
        ]

        if compito == "semplice":
            providers = [
                ("gemini-flash-lite", "GEMINI_API_KEY", GEMINI_URL, GEMINI_FLASH_LITE_MODEL),
                ("gemini-flash",      "GEMINI_API_KEY", GEMINI_URL, GEMINI_FLASH_MODEL),
                ("groq",              "GROQ_API_KEY",   GROQ_URL,   GROQ_MODEL),
            ] + FREE_RUNGS
        else:
            providers = [
                ("gemini-flash", "GEMINI_API_KEY", GEMINI_URL, GEMINI_FLASH_MODEL),
                ("groq",         "GROQ_API_KEY",   GROQ_URL,   GROQ_MODEL),
            ] + FREE_RUNGS

        for name, env, url, model in providers:
            if not os.environ.get(env): continue
            # Osservabilità (sez.9): se il brain selezionato monta un modello che
            # NON dichiara function calling, il turno sarebbe tool-blind (read_file/
            # write_file persi). Solo log nella scatola nera: NON si forza lo skip,
            # NON si tocca l'ordine del fallback. Rilevamento a runtime rimandato.
            if not _model_tool_capable(model):
                logging.warning(f"brain {name}: modello {model} senza function calling "
                                f"dichiarato, turno potenzialmente tool-blind")
            payload: List[Dict[str, Any]] = []
            try:
                client = OpenAI(base_url=url, api_key=os.environ.get(env))
                for _ in range(10):  # max 10 iterazioni agentic loop
                    payload = [{"role": "system", "content": self.system_prompt + mem_pin}] + self._get_window()
                    try:
                        response = client.chat.completions.create(
                            model=model, messages=payload,
                            tools=self.tools_schema, tool_choice="auto"
                        )
                    except Exception as e:
                        # Il 400 di Gemini può essere transitorio (diagnosi
                        # 2026-06-10: stesso payload accettato 5/5 al replay):
                        # UN solo retry con payload identico, poi fallback
                        if not (name.startswith("gemini") and "400" in str(e)[:120]):
                            raise
                        try:
                            response = client.chat.completions.create(
                                model=model, messages=payload,
                                tools=self.tools_schema, tool_choice="auto"
                            )
                            logging.warning(f"retry Gemini 400 ({name}): OK")
                        except Exception:
                            logging.warning(f"retry Gemini 400 ({name}): ancora 400, fallback")
                            raise
                    usage = getattr(response, "usage", None)
                    if usage:
                        self._log_tokens(name, model,
                                         getattr(usage, "prompt_tokens", 0) or 0,
                                         getattr(usage, "completion_tokens", 0) or 0)
                    msg = response.choices[0].message

                    if msg.tool_calls:
                        self._add_to_history("assistant", content=msg.content, tool_calls=msg.tool_calls)
                        for tc in msg.tool_calls:
                            out = self.execute_tool_call(tc.function.name, tc.function.arguments)
                            # Diario memoria (FASE 2 fetta 2a, SOLO scrittura):
                            # una riga per OGNI tool call, DOPO l'esecuzione per
                            # catturarne l'esito (negativo incluso). Fail-safe
                            # (§9): la memoria che non scrive NON ferma il turno.
                            self._diario_log(
                                tc.function.name,
                                f"{self._riassumi_args(tc.function.name, tc.function.arguments)}"
                                f" | {self._esito_sintetico(out)}",
                            )
                            self._add_to_history("tool", content=out, tool_call_id=tc.id, name=tc.function.name)
                            yield {"type": "tool_res", "output": out}
                        self._save_history()
                        # continua il loop per ottenere la risposta finale
                    elif msg.content:
                        self._add_to_history("assistant", content=msg.content)
                        self._save_history()
                        yield {"type": "final", "content": msg.content}
                        return
                    else:
                        break  # risposta vuota inattesa
            except Exception as e:
                if name.startswith("gemini") and "400" in str(e)[:120]:
                    # Diagnosi 400: sequenza dei role della finestra inviata,
                    # con dettaglio tool_calls/content per gli assistant
                    seq = [
                        f"assistant(tool_calls={len(m.get('tool_calls') or [])},"
                        f"content={'sì' if m.get('content') else 'no'})"
                        if m["role"] == "assistant" else m["role"]
                        for m in payload
                    ]
                    logging.warning(f"Diagnosi 400 {name}: payload = {' | '.join(seq)}")
                logging.warning(f"Provider {name} ({model}) fallito: {e}")
                continue
        yield {"type": "error", "content": "Pipeline esausta."}

def doctor(root_dir: Optional[str] = None) -> int:
    """Auto-diagnosi di Gas: check di integrità senza consumare token LLM
    (solo ping minimi ai provider). Ritorna 0 se tutto OK/WARN, 1 se FAIL."""
    import time
    root = Path(root_dir or os.getcwd()).resolve()
    results: List[Dict[str, str]] = []

    def check(sezione: str, voce: str, esito: str, dettaglio: str):
        results.append({"sezione": sezione, "voce": voce, "esito": esito, "dettaglio": dettaglio})

    # 1. API keys (solo presenza, mai il valore)
    for key, obbligatoria in (("GEMINI_API_KEY", True), ("GROQ_API_KEY", True), ("OPENROUTER_API_KEY", False)):
        if os.environ.get(key):
            check("API keys", key, "OK", "presente")
        else:
            check("API keys", key, "FAIL" if obbligatoria else "WARN",
                  "assente" if obbligatoria else "assente (opzionale, non in cascata)")

    # 2. Connettività provider: ping minimo (max_tokens=1) per ogni brain.
    # I rung gratuiti (openrouter/ollama) sono OPZIONALI: se manca chiave/endpoint
    # -> WARN, non FAIL (non sono in cascata obbligatoria; coerente con sez.9).
    OLLAMA_URL = os.environ.get("GAS_OLLAMA_URL")
    providers = [
        # (name, env, url, model, obbligatoria) — modelli/URL dalle costanti di modulo
        ("gemini-flash-lite", "GEMINI_API_KEY", GEMINI_URL, GEMINI_FLASH_LITE_MODEL, True),
        ("gemini-flash",      "GEMINI_API_KEY", GEMINI_URL, GEMINI_FLASH_MODEL, True),
        ("groq",              "GROQ_API_KEY",   GROQ_URL,   GROQ_MODEL, True),
        ("openrouter",        "OPENROUTER_API_KEY", OPENROUTER_URL, OPENROUTER_FREE_MODEL, False),
        ("ollama",            "GAS_OLLAMA_URL",     OLLAMA_URL,     OLLAMA_MODEL, False),
    ]
    for name, env, url, model, obbligatoria in providers:
        if not os.environ.get(env):
            check("Provider", name, "FAIL" if obbligatoria else "WARN",
                  "non testabile: API key assente" if obbligatoria
                  else "assente (opzionale: rung free non configurato)")
            continue
        try:
            client = OpenAI(base_url=url, api_key=os.environ[env], timeout=15)
            t0 = time.monotonic()
            client.chat.completions.create(model=model, messages=[{"role": "user", "content": "ping"}], max_tokens=1)
            check("Provider", name, "OK", f"{(time.monotonic() - t0) * 1000:.0f} ms")
        except Exception as e:
            esito, dettaglio = _classify_provider_error(
                getattr(e, "status_code", None), str(e), obbligatoria)
            check("Provider", name, esito, dettaglio)

    # 2b. Integrità del modello free (R1/R2 #5): METADATI OpenRouter, NESSUNA
    # generazione (coerente con "doctor non consuma token LLM"). SOLO se la chiave
    # OpenRouter è presente; assente -> già coperto sopra come WARN, qui si salta
    # (comportamento attuale invariato). Esiti: 404 -> WARN (modello assente/
    # rinominato, VISIBILE: il fail-safe regge ma non in silenzio); 'tools' assente
    # -> WARN (degraderebbe a solo-testo); presente e tool-capable -> OK.
    if os.environ.get("OPENROUTER_API_KEY"):
        esito, dettaglio = _probe_free_model(
            OPENROUTER_URL, OPENROUTER_FREE_MODEL, os.environ["OPENROUTER_API_KEY"])
        check("Paracadute", "modello free", esito, dettaglio)

    # 3. Integrità file
    for fname in ("gas.py", "CLAUDE.md"):
        check("File", fname, "OK" if (root / fname).exists() else "FAIL",
              "presente" if (root / fname).exists() else "mancante")
    check("File", "gas_identity.md", "OK" if (root / "gas_identity.md").exists() else "WARN",
          "presente" if (root / "gas_identity.md").exists() else "assente (fallback su prompt base)")
    db_path = root / ".gas_history.json"
    history = None
    if not db_path.exists():
        check("File", ".gas_history.json", "WARN", "assente (verrà creato al primo run)")
    else:
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            check("File", ".gas_history.json", "OK", f"JSON valido, {len(history)} messaggi")
        except Exception as e:
            check("File", ".gas_history.json", "FAIL", f"JSON corrotto: {str(e)[:50]}")

    # 4. Integrità storia: tool result orfani + finestra valida
    if history is not None:
        valid_ids = set()
        orfani = 0
        for msg in history:
            for tc in msg.get("tool_calls") or []:
                valid_ids.add(tc["id"])
            if msg.get("role") == "tool" and msg.get("tool_call_id") not in valid_ids:
                orfani += 1
        check("Storia", "tool orfani", "OK" if orfani == 0 else "FAIL",
              "zero orfani" if orfani == 0 else f"{orfani} tool result senza tool_use")
        window = GasKernel(str(root))._get_window()
        if not window:
            check("Storia", "_get_window", "OK", "finestra vuota (storia senza user message)")
        elif window[0]["role"] == "user":
            check("Storia", "_get_window", "OK", f"{len(window)} messaggi, parte da role:user")
        else:
            check("Storia", "_get_window", "FAIL", f"parte da role:{window[0]['role']}")

    # 5. Log
    log_path = root / "gas_debug.log"
    if not log_path.exists():
        check("Log", "gas_debug.log", "OK", "assente")
    else:
        size_mb = log_path.stat().st_size / (1024 * 1024)
        check("Log", "gas_debug.log", "WARN" if size_mb > 5 else "OK",
              f"{size_mb:.2f} MB" + (" — supera 5MB, rotazione al deploy VPS" if size_mb > 5 else ""))

    # 6. Sandbox OS: si sonda SEMPRE (indipendente dal mode, §6.3). La gravità
    # quando manca dipende dal mode: os_strict (default) = FAIL ovunque (la prod
    # è protetta di default); os_with_fallback = WARN (degrado consapevole alla
    # sola sandbox applicativa).
    avail, detail = _probe_os_sandbox()
    sb_mode = _parse_mode("GAS_SANDBOX_MODE", ("os_strict", "os_with_fallback"), "os_strict")
    if avail:
        check("Sandbox OS", "bwrap+namespace", "OK", f"{detail} (mode={sb_mode})")
    else:
        check("Sandbox OS", "bwrap+namespace",
              "FAIL" if sb_mode == "os_strict" else "WARN",
              f"{detail} — mode={sb_mode}"
              + (" (run_command bloccato)" if sb_mode == "os_strict"
                 else " (fallback sandbox applicativa)"))

    # 7. Manutenzione snapshot (TASK C) — SOLO REPORT, nessuna azione distruttiva.
    # Un `git gc` è IRREVERSIBILE (potrebbe spazzare gli oggetti degli snapshot
    # rimossi da policy): resta OPT-IN manuale, MAI automatico (§10). Qui si
    # mostrano solo i numeri per decidere a ragion veduta.
    try:
        res = subprocess.run(["git", "-C", str(root), "for-each-ref",
                              "--format=%(refname)", "refs/gas/snapshots/"],
                             capture_output=True, text=True, timeout=30)
        n_refs = len(res.stdout.split())
        soglia = GasKernel.SNAPSHOT_KEEP
        check("Snapshot", "ref totali",
              "WARN" if n_refs > soglia else "OK",
              f"{n_refs} ref" + (f" (> soglia {soglia}: valuta gc OPT-IN manuale)"
                                 if n_refs > soglia else ""))
    except Exception as e:
        check("Snapshot", "ref totali", "WARN", f"conteggio non riuscito: {str(e)[:40]}")
    try:
        res = subprocess.run(["git", "-C", str(root), "count-objects", "-v"],
                             capture_output=True, text=True, timeout=30)
        info = dict(l.split(": ", 1) for l in res.stdout.splitlines() if ": " in l)
        loose = int(info.get("count", "0"))
        size_kb = int(info.get("size", "0"))
        check("Snapshot", "oggetti loose",
              "WARN" if loose > 10000 else "OK",
              f"{loose} loose, {size_kb} KB"
              + (" (molti: valuta `git gc` OPT-IN manuale)" if loose > 10000 else ""))
    except Exception as e:
        check("Snapshot", "oggetti loose", "WARN", f"hint non riuscito: {str(e)[:40]}")
    log_snap = root / "reports" / "snapshots.log"
    if log_snap.exists():
        kb = log_snap.stat().st_size / 1024
        cap_kb = GasKernel.SNAPSHOT_LOG_MAX_BYTES / 1024
        check("Snapshot", "snapshots.log",
              "WARN" if log_snap.stat().st_size > GasKernel.SNAPSHOT_LOG_MAX_BYTES else "OK",
              f"{kb:.1f} KB" + (f" (> {cap_kb:.0f} KB: rotazione .1 al prossimo snapshot)"
                                if log_snap.stat().st_size > GasKernel.SNAPSHOT_LOG_MAX_BYTES else ""))
    else:
        check("Snapshot", "snapshots.log", "OK", "assente (nessuno snapshot ancora)")

    # 8. Memoria di lungo periodo (.gas_memory.db): il dato più prezioso e meno
    # rimpiazzabile. Tutto LOCALE (SQLite/file) → NESSUN token. Apre il DB SOLO se
    # esiste, per non crearlo come effetto collaterale della diagnosi.
    from modules.memory import MemoryStore, default_db_path
    mem_path = default_db_path(root)
    mem: Optional[MemoryStore] = None   # definita sotto se DB esiste
    if not mem_path.exists():
        check("Memoria", ".gas_memory.db", "WARN",
              "assente (verrà creato al primo run agentico)")
    else:
        mem = MemoryStore(mem_path)
        if not mem.available:
            # TASK B: motivo esplicito del fallimento (collisione vs. corruzione).
            if mem.collisione_chiave_norm:
                check("Memoria", "apertura", "FAIL",
                      f"collisione chiave_norm: {mem.collisione_chiave_norm[:100]}")
            else:
                check("Memoria", "apertura", "FAIL",
                      "DB non apribile, schema non inizializzabile o corruzione all'init")
        else:
            ok_int, det_int = mem.integrity_check()
            check("Memoria", "integrità", "OK" if ok_int else "FAIL",
                  "quick_check ok" if ok_int else f"quick_check: {det_int[:50]}")
            check("Memoria", "ricerca FTS5", "OK" if mem.fts_available else "WARN",
                  "attiva" if mem.fts_available else "assente (fallback su substring)")
            last_bak = mem.ultimo_backup()
            if last_bak is None:
                check("Memoria", "backup", "WARN",
                      "nessun backup ancora (verrà creato a runtime)")
            else:
                age_h = (time.time() - last_bak.stat().st_mtime) / 3600
                n_bak = len(mem._backup_files(mem_path.parent))
                check("Memoria", "backup", "OK",
                      f"ultimo {age_h:.1f}h fa, {n_bak} copie ({last_bak.name})")

    # TASK A — off-site backup: check dir + età ultimo backup (solo se configurata).
    # Indipendente da mem.available: la dir check è puramente filesystem.
    _offsite_env = os.environ.get("GAS_MEMORY_BACKUP_OFFSITE_DIR", "").strip()
    if _offsite_env:
        _odir = Path(_offsite_env)
        if not _odir.exists():
            check("Memoria", "off-site dir", "WARN",
                  f"{_offsite_env!r} non esiste (backup off-site rotto)")
        elif not os.access(_offsite_env, os.W_OK):
            check("Memoria", "off-site dir", "WARN",
                  f"{_offsite_env!r} non scrivibile (backup off-site rotto)")
        else:
            _last_off = mem.ultimo_backup(_odir) if mem is not None else None
            if _last_off is None:
                check("Memoria", "off-site bak", "WARN",
                      "dir ok ma nessun backup off-site ancora")
            else:
                _age_off = (time.time() - _last_off.stat().st_mtime) / 3600
                _n_off = len(mem._backup_files(_odir)) if mem is not None else 0
                check("Memoria", "off-site bak", "OK",
                      f"ultimo {_age_off:.1f}h fa, {_n_off} copie")
    else:
        check("Memoria", "off-site bak", "OK", "non configurato (OFF)")

    # TASK B — vector store visibility (chiude R-reidx-deps): controlla SOLO
    # importabilità/flag, NIENTE download del modello né embedding. Zero token.
    if _env_flag("GAS_VECTORS"):
        try:
            from modules.memory.vectors import VectorStore as _VS
            _vs_probe = _VS(default_vectors_path(root))  # init: DB sidecar, NO model load
            if _vs_probe.available:
                check("Memoria", "vector store", "OK",
                      "dipendenze ok, sidecar apribile (GAS_VECTORS=1)")
            else:
                check("Memoria", "vector store", "WARN",
                      "GAS_VECTORS=1 ma non disponibile (deps assenti o sidecar corrotto)")
        except Exception as _e:
            check("Memoria", "vector store", "WARN",
                  f"GAS_VECTORS=1 ma errore probe ({str(_e)[:50]})")
    else:
        check("Memoria", "vector store", "OK", "disabilitato (GAS_VECTORS non settata)")

    # 9. Configurazione: valori effettivi delle costanti override-abili via env.
    # Informativo, sempre OK. Permette di verificare i valori attivi senza leggere
    # il codice, utile al deploy VPS dove si settano queste variabili d'ambiente.
    _cfg_wcc = _env_int("GAS_WINDOW_CHAR_CAP", GasKernel.WINDOW_CHAR_CAP, min_val=1000)
    _cfg_mps = _env_int("GAS_MEMORY_PIN_SCAN", GasKernel.MEMORY_PIN_SCAN, min_val=10)
    check("Config", "WINDOW_CHAR_CAP", "OK",
          f"{_cfg_wcc} chr" + ("" if os.environ.get("GAS_WINDOW_CHAR_CAP") else " (default)"))
    check("Config", "MEMORY_PIN_SCAN", "OK",
          f"{_cfg_mps} eventi" + ("" if os.environ.get("GAS_MEMORY_PIN_SCAN") else " (default)"))
    if _env_flag("GAS_VECTORS"):
        _cfg_em = os.environ.get("GAS_EMBED_MODEL", "").strip() or EMBED_MODEL_NAME
        _cfg_vdb = os.environ.get("GAS_VECTORS_DB", "").strip() or str(default_vectors_path(root))
        check("Config", "EMBED_MODEL", "OK",
              f"{_cfg_em}" + ("" if os.environ.get("GAS_EMBED_MODEL") else " (default)"))
        check("Config", "VECTORS_DB", "OK",
              f"{_cfg_vdb}" + ("" if os.environ.get("GAS_VECTORS_DB") else " (default)"))

    # Report tabellare
    print("\n=== GAS DOCTOR ===\n")
    for r in results:
        print(f"[{r['esito']:<5}] {r['sezione']:<10} {r['voce']:<20} {r['dettaglio']}")
    fails = sum(1 for r in results if r["esito"] == "FAIL")
    warns = sum(1 for r in results if r["esito"] in ("WARN", "QUOTA", "KO"))
    if fails:
        print(f"\nVERDETTO: PROBLEMI RILEVATI ({fails} FAIL, {warns} avvisi)")
        return 1
    if warns:
        print(f"\nVERDETTO: OPERATIVO CON AVVISI ({warns} avvisi)")
        return 0
    print("\nVERDETTO: TUTTO OK")
    return 0


def backup_cmd(root_dir: Optional[str] = None) -> int:
    """Comando `gas backup`: backup on-demand integrity-gated su locale + off-site
    (se GAS_MEMORY_BACKUP_OFFSITE_DIR è configurata). SOLO-CLI come `gas reindex`
    — NON in tools_schema né nel dispatcher, fuori dalla mano del modello.
    Sorgente corrotta → exit 1 con messaggio chiaro. Zero token LLM."""
    root = Path(root_dir or os.getcwd()).resolve()
    from modules.memory import MemoryStore, default_db_path
    mem = MemoryStore(default_db_path(root))
    if not mem.available:
        print("[KO] backup: memoria non disponibile -- impossibile fare backup.")
        return 1
    ok, det = mem.integrity_check()
    if not ok:
        print(f"[KO] backup: integrita' KO ({det[:60]}) -- backup NON eseguito.")
        return 1
    dest = mem.backup()
    if dest is None:
        print("[KO] backup: backup locale fallito.")
        return 1
    print(f"[OK] backup locale: {dest}")
    raw_offsite = os.environ.get("GAS_MEMORY_BACKUP_OFFSITE_DIR", "").strip()
    if raw_offsite:
        keep = _env_int("GAS_MEMORY_BACKUP_OFFSITE_KEEP",
                        GasKernel.MEMORY_BACKUP_OFFSITE_KEEP, min_val=0)
        dest_off = mem.backup(raw_offsite, keep=keep)
        if dest_off is None:
            print(f"[KO] backup off-site: fallito (dir: {raw_offsite})")
        else:
            print(f"[OK] backup off-site: {dest_off}")
    else:
        print("  (off-site non configurato: GAS_MEMORY_BACKUP_OFFSITE_DIR vuota)")
    return 0


def reindex(root_dir: Optional[str] = None,
            vectors: Optional[VectorStore] = None) -> int:
    """Comando `gas reindex`: RICOSTRUISCE da zero l'indice vettoriale (la cache
    derivata `.gas_vectors.db`) a partire dal diario. È l'operazione UMANA dietro al
    catch-up automatico: serve dopo un cambio di modello di embedding (i vettori
    vecchi sono di un altro modello/dim → incompatibili), per indicizzare in un colpo
    un diario già grosso quando si accende il layer, o se si sospetta un indice
    incoerente. SICURA: tocca SOLO la cache derivata, MAI il diario/`.gas_memory.db`
    (che restano la verità intatta); e `ricostruisci_da_diario` calcola tutti gli
    embedding PRIMA di svuotare, quindi un fallimento NON distrugge l'indice buono.

    Esplicito e on-demand: costruisce il vector store a prescindere da `GAS_VECTORS`
    (chi lancia `reindex` vuole l'indice ora). `vectors` è un seam di test (iniezione
    di un VectorStore con embed_fn deterministica). Exit code 0 se OK, 1 in degrado.
    NON consuma token LLM (solo embedding locali)."""
    root = Path(root_dir or os.getcwd()).resolve()
    memory = MemoryStore(default_db_path(root))
    if not memory.available:
        print("✗ reindex: memoria non disponibile/degradata — niente da indicizzare.")
        return 1
    vs = vectors if vectors is not None else VectorStore(default_vectors_path(root))
    if not vs.available:
        print("✗ reindex: vector store non disponibile (numpy/fastembed assenti o DB "
              "sidecar corrotto). Installa le dipendenze (requirements.txt) e riprova.")
        return 1
    import time
    t0 = time.time()
    n = vs.ricostruisci_da_diario(memory)
    dt = time.time() - t0
    if n is None:
        print("✗ reindex: ricostruzione fallita (modello non caricabile/rete assente o "
              "errore DB). L'indice preesistente NON è stato toccato.")
        return 1
    print(f"✓ reindex: {n} eventi del diario re-indicizzati in {dt:.1f}s")
    print(f"  sidecar: {vs.db_path}")
    print(f"  vettori 'diario' nell'indice: {vs.conta('diario')}")
    return 0


def tokens_cmd(root_dir: Optional[str] = None, days: Optional[int] = None) -> int:
    """Comando `gas tokens`: report di contabilità token aggregato dal log
    TOKEN_LOG_FILENAME. Raggruppa per provider, mostra totali globali e degli ultimi
    N giorni (default 7). Exit code 0. Zero token LLM."""
    root = Path(root_dir or os.getcwd()).resolve()
    log_path = root / TOKEN_LOG_FILENAME
    if not log_path.exists():
        print("Nessun log token trovato. Il log si popola dalla prima chiamata ai provider.")
        return 0

    records: List[Dict[str, Any]] = []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    except Exception as e:
        print(f"✗ tokens: lettura log fallita ({e})")
        return 1

    if not records:
        print("Log token vuoto.")
        return 0

    n_days = days if days is not None else 7
    cutoff = None
    try:
        from datetime import timedelta
        cutoff = (datetime.now(timezone.utc) - timedelta(days=n_days)).strftime("%Y-%m-%dT%H:%M:%S")
    except Exception:
        pass

    # Aggregazione globale e per provider (token + costo stimato)
    totali: Dict[str, Dict] = {}
    recenti: Dict[str, Dict] = {}
    for r in records:
        prov = r.get("provider", "?")
        try:
            in_t = int(r.get("in", 0))
            out_t = int(r.get("out", 0))
        except (TypeError, ValueError):
            continue  # record JSONL malformato — skip silenzioso (§9)
        p_in, p_out = _PROVIDER_PRICE_PER_MTok.get(prov, (0.0, 0.0))
        cost = in_t * p_in / 1_000_000 + out_t * p_out / 1_000_000
        for bucket, cond in ((totali, True), (recenti, cutoff is not None and r.get("ts", "") >= cutoff)):
            if not cond:
                continue
            if prov not in bucket:
                bucket[prov] = {"turns": 0, "in": 0, "out": 0, "cost": 0.0}
            bucket[prov]["turns"] += 1
            bucket[prov]["in"] += in_t
            bucket[prov]["out"] += out_t
            bucket[prov]["cost"] += cost

    has_costs = any(d["cost"] > 0 for d in totali.values())
    cost_lbl = "Costo (★ USD)" if has_costs else "Costo"
    print(f"\n=== GAS — Token Usage ===  ({log_path.name})\n")
    hdr = f"{'Provider':<22} {'Calls':>6} {'Tokens In':>12} {'Tokens Out':>12} {'Totale':>12} {cost_lbl:>14}"
    print(hdr)
    print("─" * len(hdr))
    g_turns = g_in = g_out = 0
    g_cost = 0.0
    for prov, d in sorted(totali.items()):
        tot = d["in"] + d["out"]
        print(f"{prov:<22} {d['turns']:>6,} {d['in']:>12,} {d['out']:>12,} {tot:>12,} ${d['cost']:>12.4f}")
        g_turns += d["turns"]; g_in += d["in"]; g_out += d["out"]; g_cost += d["cost"]
    print("─" * len(hdr))
    print(f"{'TOTALE':<22} {g_turns:>6,} {g_in:>12,} {g_out:>12,} {g_in+g_out:>12,} ${g_cost:>12.4f}")

    if recenti:
        r_cost = sum(d["cost"] for d in recenti.values())
        print(f"\nUltimi {n_days} giorni:")
        for prov, d in sorted(recenti.items()):
            print(f"  {prov:<20} {d['in']:,} in + {d['out']:,} out = {d['in']+d['out']:,} tok  ${d['cost']:.4f}")
        print(f"  {'TOTALE':<20} {sum(d['in'] for d in recenti.values()):,} in + "
              f"{sum(d['out'] for d in recenti.values()):,} out  ${r_cost:.4f}")

    if has_costs:
        print("\n  ★ prezzi appross. (2025-06) — aggiornare _PROVIDER_PRICE_PER_MTok se cambiano")
    print()
    return 0


def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "doctor":
        sys.exit(doctor())
    if len(sys.argv) > 1 and sys.argv[1] == "reindex":
        sys.exit(reindex())
    if len(sys.argv) > 1 and sys.argv[1] == "backup":
        sys.exit(backup_cmd())
    if len(sys.argv) > 1 and sys.argv[1] == "tokens":
        try:
            days = int(sys.argv[2]) if len(sys.argv) > 2 else None
        except ValueError:
            print(f"Uso: gas tokens [giorni]  (es. gas tokens 7)")
            sys.exit(1)
        sys.exit(tokens_cmd(days=days))
    kernel = GasKernel()
    while True:
        try:
            prompt = input("Gas❯ ").strip()
            if not prompt: continue
            if prompt == "exit": break
            if prompt == "clear": 
                kernel.clear_history()
                print("✓ Cronologia pulita.")
                continue
            for event in kernel.run_turn(prompt):
                if event["type"] == "final": print(f"\n{event['content']}\n")
                elif event["type"] == "tool_res": print(f"  → {event['output'].strip()}")
                elif event["type"] == "error": print(f"\n✗ {event['content']}\n")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    main()
