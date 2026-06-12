#!/usr/bin/env python3
import os
import json
import shlex
import logging
import subprocess
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import List, Dict, Any, Generator, Optional, Tuple
from openai import OpenAI

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
    "per creare o modificare file usa SEMPRE write_file, mai redirezioni shell.\n"
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
        raw_mode = os.environ.get("GAS_SHELL_MODE", "guarded").strip().lower().replace("-", "_")
        if raw_mode not in ("guarded", "dry_run"):
            logging.warning(f"GAS_SHELL_MODE={raw_mode!r} non riconosciuto, uso 'guarded'")
            raw_mode = "guarded"
        self.shell_mode: str = raw_mode
        self.tools_schema = [
            {"type": "function", "function": {"name": "run_command", "description": "Esegue un comando di sola lettura da una allowlist, senza shell (no pipe/redirezioni/interpreti).", "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}},
            {"type": "function", "function": {"name": "write_file", "description": "Scrive file.", "parameters": {"type": "object", "properties": {"relative_path": {"type": "string"}, "content": {"type": "string"}}, "required": ["relative_path", "content"]}}},
            {"type": "function", "function": {"name": "read_file", "description": "Legge file.", "parameters": {"type": "object", "properties": {"relative_path": {"type": "string"}}, "required": ["relative_path"]}}}
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

        return self.history[start:]

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
    SNAPSHOT_KEEP = 100  # retention: oltre questo numero i ref più vecchi vengono potati

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
        except Exception as e:
            logging.warning(f"Indice reports/snapshots.log non aggiornato: {e}")
        try:
            res = subprocess.run(["git", "-C", str(self.root), "for-each-ref",
                                  "--format=%(refname)", "refs/gas/snapshots/"],
                                 capture_output=True, text=True, timeout=30)
            refs = res.stdout.split()
            for old in refs[:-self.SNAPSHOT_KEEP]:
                subprocess.run(["git", "-C", str(self.root), "update-ref", "-d", old],
                               capture_output=True, text=True, timeout=30)
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
                # 3) Snapshot preventivo solo ora che eseguiremo davvero.
                if self._snapshot("run_command", command[:120]) is None:
                    return ("Operazione negata: snapshot preventivo fallito, "
                            "comando non eseguito (fail-closed). Dettagli in "
                            "gas_debug.log.")
                # 4) Esecuzione SENZA shell (argv già parsato) e con env
                #    ripulita dalle variabili sensibili.
                res = subprocess.run(argv, shell=False, cwd=cwd,
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
            else:
                return "Tool non trovato."
            return self._cap_tool_output(name, args, out)
        except Exception as e:
            return f"Errore eseguendo {name}: {str(e)}"

    def run_turn(self, user_prompt: str) -> Generator[Dict[str, Any], None, None]:
        self._add_to_history("user", content=user_prompt)

        from brains.router import classifica_compito
        compito = classifica_compito(user_prompt)

        GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
        GROQ_URL   = "https://api.groq.com/openai/v1"

        if compito == "semplice":
            providers = [
                ("gemini-flash-lite", "GEMINI_API_KEY", GEMINI_URL, "gemini-2.5-flash-lite"),
                ("gemini-flash",      "GEMINI_API_KEY", GEMINI_URL, "gemini-2.5-flash"),
                ("groq",              "GROQ_API_KEY",   GROQ_URL,   "llama-3.3-70b-versatile"),
            ]
        else:
            providers = [
                ("gemini-flash", "GEMINI_API_KEY", GEMINI_URL, "gemini-2.5-flash"),
                ("groq",         "GROQ_API_KEY",   GROQ_URL,   "llama-3.3-70b-versatile"),
            ]

        for name, env, url, model in providers:
            if not os.environ.get(env): continue
            payload: List[Dict[str, Any]] = []
            try:
                client = OpenAI(base_url=url, api_key=os.environ.get(env))
                for _ in range(10):  # max 10 iterazioni agentic loop
                    payload = [{"role": "system", "content": self.system_prompt}] + self._get_window()
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
                    msg = response.choices[0].message

                    if msg.tool_calls:
                        self._add_to_history("assistant", content=msg.content, tool_calls=msg.tool_calls)
                        for tc in msg.tool_calls:
                            out = self.execute_tool_call(tc.function.name, tc.function.arguments)
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

    # 2. Connettività provider: ping minimo (max_tokens=1) per ogni brain
    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    GROQ_URL   = "https://api.groq.com/openai/v1"
    providers = [
        ("gemini-flash-lite", "GEMINI_API_KEY", GEMINI_URL, "gemini-2.5-flash-lite"),
        ("gemini-flash",      "GEMINI_API_KEY", GEMINI_URL, "gemini-2.5-flash"),
        ("groq",              "GROQ_API_KEY",   GROQ_URL,   "llama-3.3-70b-versatile"),
    ]
    for name, env, url, model in providers:
        if not os.environ.get(env):
            check("Provider", name, "FAIL", "non testabile: API key assente")
            continue
        try:
            client = OpenAI(base_url=url, api_key=os.environ[env], timeout=15)
            t0 = time.monotonic()
            client.chat.completions.create(model=model, messages=[{"role": "user", "content": "ping"}], max_tokens=1)
            check("Provider", name, "OK", f"{(time.monotonic() - t0) * 1000:.0f} ms")
        except Exception as e:
            if getattr(e, "status_code", None) == 429 or "429" in str(e)[:200]:
                check("Provider", name, "QUOTA", "429: quota esaurita")
            else:
                check("Provider", name, "KO", str(e)[:60])

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

def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "doctor":
        sys.exit(doctor())
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
