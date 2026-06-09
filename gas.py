#!/usr/bin/env python3
import os
import json
import logging
import subprocess
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import List, Dict, Any, Generator, Optional
from openai import OpenAI

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("gas_debug.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

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
    "invece di inventare."
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
        self.tools_schema = [
            {"type": "function", "function": {"name": "run_command", "description": "Esegue comandi shell.", "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}},
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

        # Nessun user message in avanti: cerca all'indietro, cappato a n*2
        if start is None:
            cap = max(0, len(self.history) - n * 2)
            for i in range(cutoff - 1, cap - 1, -1):
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

    def execute_tool_call(self, name: str, args_str: Any) -> str:
        try:
            args = json.loads(args_str) if isinstance(args_str, str) else args_str
            cwd = Path(os.environ.get("GAS_CWD", str(self.root)))
            if name == "run_command":
                res = subprocess.run(args["command"], shell=True, cwd=cwd, capture_output=True, text=True, timeout=60)
                return res.stdout + res.stderr
            elif name == "write_file":
                path = (cwd / args["relative_path"]).resolve()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(args["content"], encoding="utf-8")
                return f"Successo: File {args['relative_path']} aggiornato."
            elif name == "read_file":
                return (cwd / args["relative_path"]).read_text(encoding="utf-8")
        except Exception as e:
            return f"Errore eseguendo {name}: {str(e)}"
        return "Tool non trovato."

    def run_turn(self, user_prompt: str) -> Generator[Dict[str, Any], None, None]:
        self._add_to_history("user", content=user_prompt)

        from brains.router import classifica_compito
        compito = classifica_compito(user_prompt)

        GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
        GROQ_URL   = "https://api.groq.com/openai/v1"

        if compito == "semplice":
            providers = [
                ("gemini-flash-lite", "GEMINI_API_KEY", GEMINI_URL, "gemini-2.0-flash-lite"),
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
            try:
                client = OpenAI(base_url=url, api_key=os.environ.get(env))
                for _ in range(10):  # max 10 iterazioni agentic loop
                    payload = [{"role": "system", "content": self.system_prompt}] + self._get_window()
                    response = client.chat.completions.create(
                        model=model, messages=payload,
                        tools=self.tools_schema, tool_choice="auto"
                    )
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
        ("gemini-flash-lite", "GEMINI_API_KEY", GEMINI_URL, "gemini-2.0-flash-lite"),
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