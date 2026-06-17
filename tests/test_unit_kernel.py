"""Suite di unit test a ZERO token LLM per il kernel di Gas.

Tutto gira su root temporanee con client API finto iniettato in gas.OpenAI:
nessuna chiamata reale, nessuna scrittura su .gas_history.json del repo.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gas
from gas import GasKernel

PASS, FAIL = [], []

def check(nome: str, cond: bool, dettaglio: str = ""):
    (PASS if cond else FAIL).append(f"{nome}{' — ' + dettaglio if dettaglio else ''}")
    print(f"[{'PASS' if cond else 'FAIL'}] {nome}" + (f" — {dettaglio}" if dettaglio else ""))

def kernel_tmp() -> GasKernel:
    # git init: lo snapshot preventivo è fail-closed, senza repo git
    # write_file e run_command sono bloccati (testato a parte in T11c)
    tmp = tempfile.mkdtemp(prefix="gas_test_")
    subprocess.run(["git", "init", "-q", tmp], check=True, capture_output=True)
    os.environ["GAS_CWD"] = tmp
    return GasKernel(root_dir=tmp)

def git_out(root: str, *args: str) -> str:
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True).stdout.strip()

def snap_refs(root: str) -> list:
    return git_out(root, "for-each-ref", "--format=%(refname)", "refs/gas/snapshots/").split()

# ---------- T1-T4: _get_window ----------
k = kernel_tmp()
check("T1 finestra su storia vuota -> []", k._get_window() == [])

k = kernel_tmp()
k.history = [{"role": "assistant", "content": "x"}, {"role": "tool", "content": "y", "tool_call_id": "a"}]
check("T2 storia senza alcun user -> []", k._get_window() == [])

# T3: cutoff cade dentro una sequenza tool: la finestra deve comunque partire da user
k = kernel_tmp()
k.history = [{"role": "user", "content": "domanda"}]
for i in range(12):  # 12 coppie assistant(tool_calls)+tool dopo l'unico user
    k.history.append({"role": "assistant", "tool_calls": [{"id": f"c{i}", "type": "function", "function": {"name": "run_command", "arguments": "{}"}}]})
    k.history.append({"role": "tool", "content": "out", "tool_call_id": f"c{i}", "name": "run_command"})
w = k._get_window()
check("T3 cutoff dentro catena tool -> parte da user", bool(w) and w[0]["role"] == "user",
      f"primo={w[0]['role'] if w else 'VUOTA'} len={len(w)}")

# T4: nessun tool result orfano nella finestra
ids = set()
orfani = 0
for m in w:
    if m["role"] == "assistant":
        ids |= {tc["id"] for tc in m.get("tool_calls") or []}
    elif m["role"] == "tool" and m.get("tool_call_id") not in ids:
        orfani += 1
check("T4 zero tool orfani nella finestra", orfani == 0, f"orfani={orfani}")

# ---------- T5: _cap_tool_output ai bordi ----------
k = kernel_tmp()
esatto = "x" * 8000
check("T5a output esattamente 8000 -> intatto", k._cap_tool_output("read_file", {"relative_path": "f"}, esatto) == esatto)
oltre = "x" * 8001
capped = k._cap_tool_output("read_file", {"relative_path": "f"}, oltre)
check("T5b output 8001 -> troncato con marker",
      capped.startswith("x" * 8000) and "OUTPUT TRONCATO" in capped and "8001 caratteri" in capped,
      f"len={len(capped)}")

# ---------- T6: guardrail anti-memoria, varianti di nome ----------
k = kernel_tmp()
bloccati = ["gas_history.json", "GAS_HISTORY.JSON", "gas-history-backup.txt",
            "gas history vecchia.txt", "backup/gas_history_old.json", ".gas_history.json"]
for nome in bloccati:
    out = k.execute_tool_call("write_file", {"relative_path": nome, "content": "x"})
    ok = "Operazione negata" in out and not (Path(os.environ["GAS_CWD"]) / nome).exists()
    check(f"T6 guardrail blocca {nome!r}", ok, out[:50])
out = k.execute_tool_call("write_file", {"relative_path": "storia_del_gas_naturale.txt", "content": "lecito"})
check("T6 controllo: file lecito passa", out.startswith("Successo"), out[:60])

# ---------- T7: errori dei tool non crashano ----------
k = kernel_tmp()
out = k.execute_tool_call("read_file", {"relative_path": "non_esiste.txt"})
check("T7a read_file su file mancante -> stringa di errore", out.startswith("Errore eseguendo read_file"), out[:70])
out = k.execute_tool_call("tool_inventato", {})
check("T7b tool sconosciuto -> 'Tool non trovato.'", out == "Tool non trovato.")
out = k.execute_tool_call("write_file", "json non valido {{{")
check("T7c argomenti malformati -> stringa di errore", out.startswith("Errore eseguendo"), out[:70])

# ---------- T8: .gas_history.json corrotto -> storia vuota, zero crash ----------
tmp = tempfile.mkdtemp(prefix="gas_test_")
(Path(tmp) / ".gas_history.json").write_text("{ json corrotto !!!", encoding="utf-8")
k = GasKernel(root_dir=tmp)
check("T8 storia corrotta -> _load_history ritorna []", k.history == [])

# ---------- T9: cap del loop agentico (client finto sempre-tool) ----------
chiamate = {}  # (model) -> n. chiamate create

class FakeMsg:
    pass

def fake_response(i):
    tc = SimpleNamespace(id=f"loop{i}", function=SimpleNamespace(name="run_command", arguments='{"command": "true"}'))
    msg = SimpleNamespace(content=None, tool_calls=[tc])
    return SimpleNamespace(choices=[SimpleNamespace(message=msg)])

class FakeCompletions:
    def __init__(self, model_counter):
        self._n = 0
    def create(self, model=None, messages=None, tools=None, tool_choice=None):
        chiamate[model] = chiamate.get(model, 0) + 1
        self._n += 1
        return fake_response(self._n)

class FakeOpenAI:
    def __init__(self, base_url=None, api_key=None):
        self.chat = SimpleNamespace(completions=FakeCompletions(chiamate))

_vero_openai = gas.OpenAI
gas.OpenAI = FakeOpenAI
# I rung gratuiti (openrouter/ollama) sono OPZIONALI e la loro presenza dipende
# dall'ambiente: per un conteggio deterministico della cascata 'semplice' (3
# provider obbligatori) li disattiviamo qui, ripristinando l'ambiente dopo.
_or_key = os.environ.pop("OPENROUTER_API_KEY", None)
_ol_url = os.environ.pop("GAS_OLLAMA_URL", None)
try:
    k = kernel_tmp()
    eventi = list(k.run_turn("ciao test loop"))  # corto, no keyword -> 'semplice' -> 3 provider
finally:
    gas.OpenAI = _vero_openai
    if _or_key is not None: os.environ["OPENROUTER_API_KEY"] = _or_key
    if _ol_url is not None: os.environ["GAS_OLLAMA_URL"] = _ol_url

tool_res = [e for e in eventi if e["type"] == "tool_res"]
errori = [e for e in eventi if e["type"] == "error"]
check("T9a ogni provider cappato a 10 iterazioni",
      all(n == 10 for n in chiamate.values()) and len(chiamate) == 3,
      f"chiamate per modello: {chiamate}")
check("T9b loop infinito assorbito senza crash, pipeline esausta dichiarata",
      len(errori) == 1 and errori[0]["content"] == "Pipeline esausta.",
      f"tool_res={len(tool_res)} errori={len(errori)}")
check("T9c storia salvata su disco nella root temporanea", k.db_path.exists() and k.db_path.stat().st_size > 0)

# ---------- T9d: rung gratuiti — append in coda + skip pulito senza endpoint ----------
# OpenRouter presente (chiave fittizia) -> deve comparire IN CODA; Ollama senza
# GAS_OLLAMA_URL -> skip pulito (mai crash), il suo modello NON deve apparire.
chiamate2 = {}
class FakeCompletions2(FakeCompletions):
    def create(self, model=None, messages=None, tools=None, tool_choice=None):
        chiamate2[model] = chiamate2.get(model, 0) + 1
        return fake_response(1)
class FakeOpenAI2:
    def __init__(self, base_url=None, api_key=None):
        self.chat = SimpleNamespace(completions=FakeCompletions2(chiamate2))
gas.OpenAI = FakeOpenAI2
_or_key = os.environ.get("OPENROUTER_API_KEY")
_ol_url = os.environ.pop("GAS_OLLAMA_URL", None)
os.environ["OPENROUTER_API_KEY"] = "dummy-for-test"
try:
    k = kernel_tmp()
    list(k.run_turn("ciao test loop free"))  # 'semplice' -> 3 obbligatori + openrouter
finally:
    gas.OpenAI = _vero_openai
    if _or_key is not None: os.environ["OPENROUTER_API_KEY"] = _or_key
    else: os.environ.pop("OPENROUTER_API_KEY", None)
    if _ol_url is not None: os.environ["GAS_OLLAMA_URL"] = _ol_url
check("T9d openrouter free in coda alla cascata 'semplice'",
      "meta-llama/llama-3.3-70b-instruct:free" in chiamate2,
      f"modelli interpellati: {sorted(chiamate2)}")
check("T9e ollama skippato senza GAS_OLLAMA_URL (skip pulito, niente crash)",
      "qwen2.5:7b-instruct" not in chiamate2,
      f"modelli interpellati: {sorted(chiamate2)}")

# ---------- T10: sicurezza — path traversal BLOCCATO (write_file e read_file) ----------
tmp_inner = tempfile.mkdtemp(prefix="gas_test_inner_")
subprocess.run(["git", "init", "-q", tmp_inner], check=True, capture_output=True)
os.environ["GAS_CWD"] = tmp_inner
k = GasKernel(root_dir=tmp_inner)

# T10a: write_file con ../ non deve scrivere fuori dalla root
out = k.execute_tool_call("write_file", {"relative_path": "../gas_traversal_proof.txt", "content": "fuori"})
fuori = Path(tmp_inner).parent / "gas_traversal_proof.txt"
scappato = fuori.exists()
if scappato:
    fuori.unlink()
check("T10a write_file con ../ -> negato, niente file fuori root",
      "Operazione negata" in out and not scappato, out[:70])

# T10b: read_file con ../ non deve esfiltrare file esterni (es. API key in ~/.bashrc)
segreto = Path(tmp_inner).parent / "gas_segreto_esterno.txt"
segreto.write_text("API_KEY=supersegreta", encoding="utf-8")
out = k.execute_tool_call("read_file", {"relative_path": "../gas_segreto_esterno.txt"})
segreto.unlink()
check("T10b read_file con ../ -> negato, nessuna esfiltrazione",
      "Operazione negata" in out and "supersegreta" not in out, out[:70])

# T10c: anche i path assoluti fuori root sono negati
out = k.execute_tool_call("write_file", {"relative_path": "/tmp/gas_abs_proof.txt", "content": "abs"})
check("T10c write_file con path assoluto fuori root -> negato",
      "Operazione negata" in out and not Path("/tmp/gas_abs_proof.txt").exists(), out[:70])

# T10d: controllo — i path legittimi (anche in sottocartelle) continuano a passare
out = k.execute_tool_call("write_file", {"relative_path": "sub/dir/ok.txt", "content": "dentro"})
check("T10d write_file legittimo in sottocartella passa", out.startswith("Successo"), out[:60])
out = k.execute_tool_call("read_file", {"relative_path": "sub/dir/ok.txt"})
check("T10e read_file legittimo passa", out == "dentro", out[:40])

# ---------- T11: snapshot preventivo anti-autodistruzione ----------
# T11a: write_file crea uno snapshot PRIMA di scrivere
k = kernel_tmp()
root = os.environ["GAS_CWD"]
k.execute_tool_call("write_file", {"relative_path": "doc.txt", "content": "versione 1"})
refs_prima = snap_refs(root)
out = k.execute_tool_call("write_file", {"relative_path": "doc.txt", "content": "versione 2 distruttiva"})
nuovi = [r for r in snap_refs(root) if r not in refs_prima]
check("T11a write_file crea uno snapshot prima di scrivere",
      out.startswith("Successo") and len(nuovi) == 1, f"nuovi ref={len(nuovi)}")

# T11b: lo snapshot contiene lo stato PRE-modifica e il ripristino umano
# (git restore --source) riporta il contenuto esatto
snap_ref = nuovi[0] if nuovi else "REF_MANCANTE"
check("T11b snapshot = stato pre-modifica", git_out(root, "show", f"{snap_ref}:doc.txt") == "versione 1")
subprocess.run(["git", "-C", root, "restore", "--worktree", "--source", snap_ref, "--", "doc.txt"],
               capture_output=True)
check("T11b2 git restore riporta il file alla versione pre-modifica",
      (Path(root) / "doc.txt").read_text(encoding="utf-8") == "versione 1")

# T11c: fail-closed — root senza repo git = snapshot impossibile = scrittura
# e comandi shell BLOCCATI, nessun file creato
tmp_nogit = tempfile.mkdtemp(prefix="gas_test_nogit_")
os.environ["GAS_CWD"] = tmp_nogit
k_nogit = GasKernel(root_dir=tmp_nogit)
out = k_nogit.execute_tool_call("write_file", {"relative_path": "vittima.txt", "content": "x"})
check("T11c snapshot fallito -> write_file bloccata (fail-closed)",
      "Operazione negata" in out and "snapshot" in out and not (Path(tmp_nogit) / "vittima.txt").exists(),
      out[:70])
out = k_nogit.execute_tool_call("run_command", {"command": "ls -la"})
# 'ls' È in allowlist: supera il vetting e arriva fino allo snapshot, che
# qui fallisce (niente repo git). Senza un comando consentito il test
# morirebbe prima, al vetting, e NON eserciterebbe più il fail-closed dello
# snapshot (falso verde): l'asserzione su "snapshot" lo garantisce.
check("T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed)",
      "Operazione negata" in out and "snapshot" in out
      and not (Path(tmp_nogit) / "vittima2.txt").exists(), out[:70])

# T11d: i file NON tracciati finiscono nello snapshot (trappola stash create)
k = kernel_tmp()
root = os.environ["GAS_CWD"]
(Path(root) / "non_tracciato.txt").write_text("mai committato", encoding="utf-8")
k.execute_tool_call("write_file", {"relative_path": "altro.txt", "content": "y"})
ultimo = snap_refs(root)[-1]
check("T11d file non tracciato incluso nello snapshot",
      git_out(root, "show", f"{ultimo}:non_tracciato.txt") == "mai committato")

# T11e: anche run_command fa scattare lo snapshot
prima = len(snap_refs(root))
out = k.execute_tool_call("run_command", {"command": "true"})
check("T11e run_command fa scattare lo snapshot",
      len(snap_refs(root)) == prima + 1 and not out.startswith("Operazione negata"),
      f"refs {prima} -> {len(snap_refs(root))}")

# T11f: retention IBRIDA (TASK C) — ramo count-based. Con la policy ibrida i ref
# GIOVANI sono protetti dall'età: per esercitare il limite per-conteggio si azzera
# SNAPSHOT_KEEP_DAYS (nessuna protezione d'età) e resta solo "ultimi N".
k.SNAPSHOT_KEEP = 3
k.SNAPSHOT_KEEP_DAYS = 0
for i in range(5):
    k.execute_tool_call("write_file", {"relative_path": "giro.txt", "content": f"giro {i}"})
check("T11f retention (ramo count, età disattivata) tiene solo gli ultimi N",
      len(snap_refs(root)) == 3,
      f"refs={len(snap_refs(root))} (limite 3)")

# T11g: root annidata in un repo esterno senza proprio .git -> fail-closed,
# lo snapshot NON deve "riuscire" fotografando il repo genitore (riserva R1)
tmp_outer = tempfile.mkdtemp(prefix="gas_test_outer_")
subprocess.run(["git", "init", "-q", tmp_outer], check=True, capture_output=True)
nested = Path(tmp_outer) / "annidata"
nested.mkdir()
os.environ["GAS_CWD"] = str(nested)
k_nested = GasKernel(root_dir=str(nested))
out = k_nested.execute_tool_call("write_file", {"relative_path": "vittima3.txt", "content": "x"})
check("T11g root annidata in repo esterno -> bloccata, nessun ref nel repo genitore",
      "Operazione negata" in out and not (nested / "vittima3.txt").exists()
      and snap_refs(tmp_outer) == [], out[:70])

# ---------- T12: sandbox run_command (allowlist + no-shell + dry-run) ----------
# Ogni asserzione è costruita per FALLIRE se la barriera corrispondente viene
# tolta: sono test che "mordono", non decorativi.
k = kernel_tmp()
root = os.environ["GAS_CWD"]

# T12a: comando in allowlist eseguito davvero (output reale, non simulato)
(Path(root) / "dati.txt").write_text("riga1\nriga2\nriga3\n", encoding="utf-8")
out = k.execute_tool_call("run_command", {"command": "wc -l dati.txt"})
check("T12a comando in allowlist (wc) eseguito, output reale",
      "3" in out and "Operazione negata" not in out, out[:60])

# T12b: comando fuori allowlist negato (qui 'touch' = scrittura mascherata)
out = k.execute_tool_call("run_command", {"command": "touch intruso.txt"})
check("T12b comando fuori allowlist negato, nessun effetto",
      "Operazione negata" in out and "non consentito" in out
      and not (Path(root) / "intruso.txt").exists(), out[:60])

# T12c: la PIPE non viene interpretata come shell. shlex la spezza e 'grep'
# riceve '|' e 'wc' come ARGOMENTI (nomi di file inesistenti): nessun
# secondo processo, nessun '3' come se il conteggio fosse passato a wc.
out = k.execute_tool_call("run_command", {"command": "grep riga dati.txt | wc -l"})
check("T12c pipe non interpretata (niente shell)",
      "Operazione negata" not in out and out.strip() != "3", out[:70])

# T12d: la REDIRESIONE non crea file. '>' e il target finiscono come
# argomenti di cat, non come redirezione: 'bersaglio.txt' non deve nascere.
out = k.execute_tool_call("run_command", {"command": "cat dati.txt > bersaglio.txt"})
check("T12d redirezione non crea file (niente shell)",
      not (Path(root) / "bersaglio.txt").exists(), out[:70])

# T12e: la COMMAND SUBSTITUTION non viene eseguita. '$(...)' resta testo
# letterale passato a echo, non l'output di un sottocomando.
out = k.execute_tool_call("run_command", {"command": "echo $(cat dati.txt)"})
check("T12e command substitution non eseguita (resta letterale)",
      "$(cat" in out and "riga1" not in out, out[:70])

# T12f: argomento-path con ../ negato anche dentro run_command (stesso
# guardrail di T10, applicato ai token del comando)
out = k.execute_tool_call("run_command", {"command": "cat ../etc_passwd_finto"})
check("T12f argomento traversal in run_command negato",
      "Operazione negata" in out and "fuori" in out, out[:70])

# T12g: comando non interpretabile (virgolette sbilanciate) negato dal parser,
# non passato a subprocess
out = k.execute_tool_call("run_command", {"command": 'cat "non chiusa'})
check("T12g comando non interpretabile negato (fail-closed)",
      "Operazione negata" in out and "non interpretabile" in out, out[:70])

# T12h: l'ambiente del processo figlio è ripulito dai segreti. Inietto una
# finta API key, poi provo a stamparla con env: 'cat' su /proc non serve,
# uso il fatto che _sanitized_subprocess_env la rimuove a monte.
os.environ["FAKE_SECRET_KEY"] = "supersegreta-da-non-vedere"
try:
    env_figlio = k._sanitized_subprocess_env()
finally:
    os.environ.pop("FAKE_SECRET_KEY", None)
check("T12h env figlio privo di variabili sensibili (KEY/TOKEN/SECRET...)",
      "FAKE_SECRET_KEY" not in env_figlio and "PATH" in env_figlio,
      f"chiavi sensibili residue: {[v for v in env_figlio if 'SECRET' in v.upper()]}")

# T12i: dry-run — comando consentito ma NON eseguito, e NESSUNO snapshot creato
os.environ["GAS_SHELL_MODE"] = "dry_run"
try:
    k_dry = GasKernel(root_dir=root)
    refs_prima = len(snap_refs(root))
    out = k_dry.execute_tool_call("run_command", {"command": "wc -l dati.txt"})
    refs_dopo = len(snap_refs(root))
finally:
    os.environ.pop("GAS_SHELL_MODE", None)
check("T12i dry-run: comando non eseguito e nessuno snapshot",
      "DRY-RUN" in out and "NON eseguito" in out and refs_dopo == refs_prima,
      f"refs {refs_prima}->{refs_dopo}, out={out[:40]}")

# T12j: modalità sconosciuta ricade su 'guarded' (fail-safe), non spegne il sandbox
os.environ["GAS_SHELL_MODE"] = "modalita-inventata"
try:
    k_fb = GasKernel(root_dir=root)
finally:
    os.environ.pop("GAS_SHELL_MODE", None)
check("T12j GAS_SHELL_MODE non valido -> fallback su 'guarded'",
      k_fb.shell_mode == "guarded", f"shell_mode={k_fb.shell_mode}")

# ---------- T13: sandbox OS (bwrap) — barriere che MORDONO ----------
# I test di barriera (a/b/c) esercitano il profilo bwrap DIRETTAMENTE via
# _bwrap_prefix: l'allowlist read-only non contiene binari di rete/scrittura,
# quindi non si potrebbe provare net/fs/mascheramento passando per run_command.
# Ognuno fallisce se la barriera corrispondente viene tolta dal profilo.
OS_SB = gas._probe_os_sandbox()[0]

def skip(nome: str, motivo: str):
    print(f"[SKIP] {nome} — {motivo}")

k = kernel_tmp()
root = os.environ["GAS_CWD"]
(Path(root) / "dati.txt").write_text("riga1\nriga2\nriga3\n", encoding="utf-8")

# T13a: rete BLOCCATA dentro il sandbox (--unshare-net). Un comando di rete
# (risoluzione DNS) deve fallire: solo loopback disponibile.
if OS_SB:
    res = subprocess.run(k._bwrap_prefix(Path(root)) + ["getent", "hosts", "github.com"],
                         capture_output=True, text=True, timeout=30)
    check("T13a rete bloccata nel sandbox (DNS fallisce)",
          res.returncode != 0, f"rc={res.returncode} out={res.stdout.strip()[:40]!r}")
else:
    skip("T13a rete bloccata", "sandbox OS non disponibile in questo ambiente")

# T13b: filesystem READ-ONLY. Una scrittura sulla project root (RO-bind) deve
# essere negata dal kernel e nessun file deve nascere.
if OS_SB:
    bersaglio = Path(root) / "scrittura_vietata.txt"
    res = subprocess.run(k._bwrap_prefix(Path(root)) + ["touch", str(bersaglio)],
                         capture_output=True, text=True, timeout=30)
    nato = bersaglio.exists()
    if nato:
        bersaglio.unlink()
    check("T13b filesystem read-only (scrittura su project root negata)",
          res.returncode != 0 and not nato, f"rc={res.returncode} nato={nato}")
else:
    skip("T13b filesystem read-only", "sandbox OS non disponibile in questo ambiente")

# T13c: SECRET ON-DISK MASCHERATI (§6.1). Un'esca segreta creata sotto /home
# (~) NON deve essere leggibile dentro il sandbox: il --tmpfs /home la copre.
# È il test dell'irrobustimento §6.1 — chiude R2 anche in LETTURA.
if OS_SB:
    esca = Path.home() / f"gas_esca_segreta_{os.getpid()}.txt"
    try:
        esca.write_text("API_KEY=TOPSECRET-non-deve-uscire", encoding="utf-8")
        res = subprocess.run(k._bwrap_prefix(Path(root)) + ["cat", str(esca)],
                             capture_output=True, text=True, timeout=30)
        ok = res.returncode != 0 and "TOPSECRET" not in (res.stdout + res.stderr)
        check("T13c segreto on-disk sotto /home mascherato (tmpfs lo copre)",
              ok, f"rc={res.returncode} out={(res.stdout + res.stderr).strip()[:50]!r}")
    finally:
        esca.unlink(missing_ok=True)
else:
    skip("T13c segreto on-disk mascherato", "sandbox OS non disponibile in questo ambiente")

# T13d: fallback corretto secondo GAS_SANDBOX_MODE (deterministico, NON richiede
# bwrap: si forza os_sandbox_available=False). os_strict assente -> negato;
# os_with_fallback assente -> esegue comunque (sola sandbox applicativa).
k_strict = kernel_tmp()
k_strict.os_sandbox_available = False
k_strict.sandbox_mode = "os_strict"
out = k_strict.execute_tool_call("run_command", {"command": "true"})
check("T13d os_strict + sandbox assente -> run_command negato (fail-closed)",
      "Operazione negata" in out and "sandbox OS" in out, out[:70])

k_fb = kernel_tmp()
rootfb = os.environ["GAS_CWD"]
(Path(rootfb) / "dati.txt").write_text("a\nb\nc\n", encoding="utf-8")
k_fb.os_sandbox_available = False
k_fb.sandbox_mode = "os_with_fallback"
out = k_fb.execute_tool_call("run_command", {"command": "wc -l dati.txt"})
check("T13d2 os_with_fallback + sandbox assente -> esegue (sandbox applicativa)",
      "Operazione negata" not in out and "3" in out, out[:60])

# T13e: comando lecito read-only ANCORA funzionante nella project root CON il
# sandbox OS attivo (os_strict + disponibile) e lo snapshot scatta. Conferma
# che il wrapping bwrap non rompe l'uso normale.
if OS_SB:
    k_ok = kernel_tmp()
    rootok = os.environ["GAS_CWD"]
    (Path(rootok) / "dati.txt").write_text("u\nd\nt\n", encoding="utf-8")
    refs_prima = len(snap_refs(rootok))
    out = k_ok.execute_tool_call("run_command", {"command": "wc -l dati.txt"})
    check("T13e comando lecito read-only funziona dentro bwrap + snapshot scatta",
          "3" in out and "Operazione negata" not in out
          and len(snap_refs(rootok)) == refs_prima + 1,
          f"out={out[:30]!r} refs {refs_prima}->{len(snap_refs(rootok))}")
else:
    skip("T13e comando lecito dentro bwrap", "sandbox OS non disponibile in questo ambiente")

# ---------- T14: WINDOW_CHAR_CAP / _cap_window_chars (review #7, R1) ----------
# Test deterministici a cap abbassato sull'istanza: mordono ognuno una barriera
# diversa del cap. Se la logica si rompe (slicing dentro un messaggio, ultimo
# scartato, mancato riallineamento, mancato fallback) il check corrispondente FALLISCE.

def _u(s): return {"role": "user", "content": s}
def _a(content, name="run_command", args="{}", cid="c0"):
    return {"role": "assistant", "content": content,
            "tool_calls": [{"id": cid, "type": "function",
                            "function": {"name": name, "arguments": args}}]}
def _t(s, cid="c0"): return {"role": "tool", "content": s, "tool_call_id": cid, "name": "run_command"}

# T14a — _msg_chars conta content + (per le tool call) arguments + name
k = kernel_tmp()
check("T14a _msg_chars = content + tool args + tool name",
      k._msg_chars(_a("abc", name="run", args="{}")) == 3 + 2 + 3,
      f"atteso 8, ottenuto {k._msg_chars(_a('abc', name='run', args='{}'))}")
check("T14a2 _msg_chars su content assente/None -> 0",
      k._msg_chars({"role": "user"}) == 0 and k._msg_chars({"role": "user", "content": None}) == 0)

# T14b — finestra vuota -> []
check("T14b finestra vuota -> []", k._cap_window_chars([]) == [])

# T14c — finestra sotto il cap -> restituita INVARIATA (nessuno scarto)
k.WINDOW_CHAR_CAP = 1000
win_small = [_u("aa"), _a("bb"), _t("cc")]
check("T14c finestra sotto il cap -> invariata", k._cap_window_chars(win_small) == win_small)

# T14d — ultimo messaggio da solo > cap -> tenuto INTERO; i precedenti scartati
k.WINDOW_CHAR_CAP = 10
win_big_last = [_u("a" * 5), _u("b" * 100)]
out_d = k._cap_window_chars(win_big_last)
check("T14d ultimo msg > cap tenuto intero (non troncato, non scartato)",
      len(out_d) == 1 and out_d[0]["content"] == "b" * 100,
      f"len={len(out_d)} content_len={len(out_d[0]['content']) if out_d else 'NA'}")

# T14e — scarto di messaggi INTERI, mai slicing dentro un messaggio
k.WINDOW_CHAR_CAP = 10
win_e = [_u("vecchio" * 10), _u("ccc"), _u("dddd")]   # 70, 3, 4
out_e = k._cap_window_chars(win_e)
intatti = all(m in win_e for m in out_e)               # ogni msg tenuto è identico all'originale
check("T14e scarto di messaggi interi (mai taglio dentro un messaggio)",
      out_e == [_u("ccc"), _u("dddd")] and intatti,
      f"out={[m['content'] for m in out_e]}")

# T14f — riallineamento: dopo lo scarto un orfano in testa -> si riparte da user
k.WINDOW_CHAR_CAP = 10
win_f = [_u("u1"), _a("A" * 5), _t("out"), _u("u2"), {"role": "assistant", "content": "fine"}]
out_f = k._cap_window_chars(win_f)
check("T14f riallineamento dell'inizio a role:user (no tool/assistant orfano in testa)",
      bool(out_f) and out_f[0]["role"] == "user" and out_f[0]["content"] == "u2",
      f"primo={out_f[0]['role'] if out_f else 'VUOTA'}:{out_f[0].get('content') if out_f else ''}")

# T14g — budget scarta TUTTI gli user -> fallback all'ultimo user dell'intera finestra
#         (mai partire da non-user, mai vuoto se un user esiste)
k.WINDOW_CHAR_CAP = 10
win_g = [_u("U"), _a("a" * 5), _t("o")]                # cap lascerebbe solo il tool (orfano, no user)
out_g = k._cap_window_chars(win_g)
check("T14g nessun user sopravvissuto -> fallback all'ultimo user (finestra valida, non vuota)",
      out_g == win_g and out_g[0]["role"] == "user",
      f"primo={out_g[0]['role'] if out_g else 'VUOTA'} len={len(out_g)}")

# T14h — componibilità: _get_window APPLICA il cap (scarta l'user più vecchio)
k = kernel_tmp()
k.WINDOW_CHAR_CAP = 10
k.history = [_u("aaaa"), _u("bbbb"), _u("cccc")]        # 3 user piccoli, budget 10
w_h = k._get_window()
check("T14h _get_window applica WINDOW_CHAR_CAP (componibilità col cap a 10 msg)",
      w_h == [_u("bbbb"), _u("cccc")] and w_h[0]["role"] == "user",
      f"len={len(w_h)} primo={w_h[0]['content'] if w_h else 'VUOTA'}")

# ---------- T16: de-dup parse mode condiviso __init__ ⇄ doctor (TASK A) ----------
# Refactor PURO: __init__ e doctor devono risolvere lo STESSO mode dato lo stesso
# env, perché ora usano l'unico helper gas._parse_mode (niente logica duplicata).
SB_ALLOWED = ("os_strict", "os_with_fallback")
_sb_bak = os.environ.get("GAS_SANDBOX_MODE")
_sh_bak = os.environ.get("GAS_SHELL_MODE")
try:
    # T16a — normalizzazione (trim / lower / '-'→'_')
    os.environ["GAS_SANDBOX_MODE"] = "  OS-With-Fallback "
    os.environ["GAS_SHELL_MODE"] = "DRY-RUN"
    k = kernel_tmp()
    check("T16a _parse_mode normalizza i valori di mode",
          k.sandbox_mode == "os_with_fallback" and k.shell_mode == "dry_run",
          f"sb={k.sandbox_mode} sh={k.shell_mode}")
    # T16b — valore ignoto -> default fail-safe (identico al comportamento storico)
    os.environ["GAS_SANDBOX_MODE"] = "falopso"
    os.environ["GAS_SHELL_MODE"] = "rawshell"
    k = kernel_tmp()
    check("T16b mode ignoto -> default (os_strict / guarded)",
          k.sandbox_mode == "os_strict" and k.shell_mode == "guarded",
          f"sb={k.sandbox_mode} sh={k.shell_mode}")
    # T16c — __init__ e doctor risolvono lo STESSO mode per lo stesso env (incl. ignoto)
    coerente = True
    dettagli = []
    for val in ("os_strict", "os_with_fallback", "ignoto-xyz", "OS_STRICT"):
        os.environ["GAS_SANDBOX_MODE"] = val
        init_mode = kernel_tmp().sandbox_mode                                   # via __init__
        doctor_mode = gas._parse_mode("GAS_SANDBOX_MODE", SB_ALLOWED, "os_strict")  # via doctor
        coerente = coerente and (init_mode == doctor_mode)
        dettagli.append(f"{val!r}->{init_mode}")
    check("T16c __init__ e doctor risolvono lo STESSO mode (incl. ignoto -> os_strict)",
          coerente, "; ".join(dettagli))
finally:
    os.environ.pop("GAS_SANDBOX_MODE", None)
    os.environ.pop("GAS_SHELL_MODE", None)
    if _sb_bak is not None: os.environ["GAS_SANDBOX_MODE"] = _sb_bak
    if _sh_bak is not None: os.environ["GAS_SHELL_MODE"] = _sh_bak

# ---------- T17: integrità paracadute free (TASK B, R1/R2 #5) — ZERO token ----------
# Mock della risposta /models/<slug>/endpoints: nessuna rete, nessuna generazione.
# La forma replica quella REALE sondata il 2026-06-14 (supported_parameters è
# PER-ENDPOINT, "tools" dentro la lista = function calling dichiarato).
def _fake_fetch(status, data):
    return lambda url, api_key: (status, data)

_ep_with_tools = {"data": {"id": gas.OPENROUTER_FREE_MODEL, "endpoints": [
    {"provider_name": "x", "supported_parameters": ["max_tokens", "temperature", "tools", "tool_choice"]}]}}
_ep_no_tools = {"data": {"id": gas.OPENROUTER_FREE_MODEL, "endpoints": [
    {"provider_name": "x", "supported_parameters": ["max_tokens", "temperature", "top_p"]}]}}

# T17a — 404 -> WARN (modello assente/rinominato, VISIBILE)
e, d = gas._probe_free_model(gas.OPENROUTER_URL, gas.OPENROUTER_FREE_MODEL, "k", _fetch=_fake_fetch(404, None))
check("T17a 404 -> WARN (modello free assente/rinominato)", e == "WARN", f"esito={e} · {d}")

# T17b — esiste ma nessun endpoint dichiara 'tools' -> WARN (degrado solo-testo)
e, d = gas._probe_free_model(gas.OPENROUTER_URL, gas.OPENROUTER_FREE_MODEL, "k", _fetch=_fake_fetch(200, _ep_no_tools))
check("T17b modello senza 'tools' -> WARN (degrado a solo-testo)", e == "WARN", f"esito={e} · {d}")

# T17c — esiste e almeno un endpoint dichiara 'tools' -> OK
e, d = gas._probe_free_model(gas.OPENROUTER_URL, gas.OPENROUTER_FREE_MODEL, "k", _fetch=_fake_fetch(200, _ep_with_tools))
check("T17c modello presente + 'tools' dichiarato -> OK", e == "OK", f"esito={e} · {d}")

# T17d — _classify_free_model è la barriera (morde per MUTAZIONE dei tre rami)
check("T17d classify: i tre rami sono distinti e corretti",
      gas._classify_free_model(404, None)[0] == "WARN"
      and gas._classify_free_model(200, _ep_no_tools)[0] == "WARN"
      and gas._classify_free_model(200, _ep_with_tools)[0] == "OK")

# T17e — registro statico tool-capability (osservabilità run_turn): morde se si
# rimuove un modello dal registro o vi si aggiunge un modello text-only.
check("T17e _model_tool_capable: cascata tool-capable, ignoto -> False",
      all(gas._model_tool_capable(m) for m in (
          gas.GEMINI_FLASH_LITE_MODEL, gas.GEMINI_FLASH_MODEL, gas.GROQ_MODEL,
          gas.OPENROUTER_FREE_MODEL, gas.OLLAMA_MODEL))
      and not gas._model_tool_capable("provider/modello-solo-testo"))

# ---------- T18: retention IBRIDA snapshot (TASK C) — logica pura, ZERO git ----------
import time as _time
def _mkref(epoch, sha="ab12cd34"):
    ts = _time.strftime("%Y%m%d-%H%M%S", _time.localtime(epoch)) + ".000000000"
    return f"refs/gas/snapshots/{ts}-{sha}"

_now = _time.time()
_DAY = 86400
# Lista ORDINATA cronologicamente (come la dà for-each-ref): vecchi -> recenti.
_ages_days = [30, 29, 28, 27, 26, 2, 1]
_refs = [_mkref(_now - d * _DAY, sha=f"{d:08d}") for d in _ages_days]  # già ascendente
keep, drop = gas._snapshot_retention(_refs, _now, keep_n=3, keep_days=7)

# T18a — i ref GIOVANI (< keep_days) sopravvivono sempre
check("T18a recenti (<7gg) sopravvivono",
      _mkref(_now - 1 * _DAY, "00000001") in keep and _mkref(_now - 2 * _DAY, "00000002") in keep,
      f"keep={len(keep)} drop={len(drop)}")

# T18b — i vecchi oltre ENTRAMBE le soglie (fuori dagli ultimi 3 E > 7gg) sono droppati
check("T18b vecchi oltre N E oltre T -> drop",
      all(_mkref(_now - d * _DAY, f"{d:08d}") in drop for d in (30, 29, 28, 27))
      and len(drop) == 4,
      f"drop={drop}")

# T18c — keep_n protegge un ref VECCHIO (26gg) solo perché tra gli ultimi 3
check("T18c keep_n protegge il vecchio dentro gli ultimi N",
      _mkref(_now - 26 * _DAY, "00000026") in keep)

# T18d — MORDACE: abbassare keep_n smaschera il 26gg (cambia il set protetto)
keep2, drop2 = gas._snapshot_retention(_refs, _now, keep_n=2, keep_days=7)
check("T18d soglia più stretta -> set protetto diverso (mordace)",
      _mkref(_now - 26 * _DAY, "00000026") in drop2 and _mkref(_now - 26 * _DAY, "00000026") in keep)

# T18e — nome ref non parsabile -> conservativo: TENUTO (mai rimosso per nome inatteso)
keep3, drop3 = gas._snapshot_retention(["refs/gas/snapshots/spazzatura"], _now, keep_n=0, keep_days=0)
check("T18e ref non parsabile -> tenuto (conservativo)",
      drop3 == [] and gas._ref_age_epoch("refs/gas/snapshots/spazzatura") is None)

# T18f — _ref_age_epoch estrae la data dal nome ref valido
check("T18f _ref_age_epoch parsa il ts dal nome ref",
      abs(gas._ref_age_epoch(_mkref(_now - 5 * _DAY, "00000005")) - (_now - 5 * _DAY)) < 2,
      f"delta≈{gas._ref_age_epoch(_mkref(_now - 5 * _DAY, '00000005')) - (_now - 5 * _DAY):.0f}s")

# ---------- T19: memoria FASE 2 fetta 1 (modules/memory, storage SQLite) ----------
# Tutto locale, ZERO token: DB su file temporaneo, niente LLM.
import sqlite3 as _sqlite3
from modules.memory import (
    MemoryStore, STATI_CONTATTO, STATI_CHIUSI, STATO_DEFAULT, default_db_path,
)

def mem_tmp() -> MemoryStore:
    d = tempfile.mkdtemp(prefix="gas_mem_")
    return MemoryStore(default_db_path(d))

# T19a — diario: append + lettura recente (ordine: più recente prima)
m = mem_tmp()
id1 = m.append_diario("sistema", "avvio GAS")
id2 = m.append_diario("tool_call", "run_command: ls")
rec = m.diario_recente(10)
check("T19a diario append+lettura", isinstance(id1, int) and isinstance(id2, int)
      and len(rec) == 2 and rec[0]["descrizione"] == "run_command: ls"
      and rec[0]["tipo"] == "tool_call", f"rec={[r['descrizione'] for r in rec]}")

# T19b — contatti: upsert crea (stato default), poi aggiorna l'anagrafica senza duplicare
cid = m.upsert_contatto("lead@ex.com", nome="Mario", contatto="lead@ex.com")
c0 = m.get_contatto(cid)
cid2 = m.upsert_contatto("lead@ex.com", nome="Mario Rossi")  # stessa chiave -> update
c1 = m.get_contatto(cid)
check("T19b upsert crea+aggiorna senza duplicare",
      cid == cid2 and c0["stato"] == STATO_DEFAULT and c0["nome"] == "Mario"
      and c1["nome"] == "Mario Rossi" and len(m.lista_contatti()) == 1,
      f"cid={cid} cid2={cid2} nome={c1['nome'] if c1 else None}")

# T19c — upsert NON tocca lo stato in conflitto (la transizione passa altrove)
m.update_stato_contatto(cid, "interessato")
m.upsert_contatto("lead@ex.com", note="ricontattare")  # upsert non deve resettare lo stato
check("T19c upsert non resetta lo stato", m.get_contatto(cid)["stato"] == "interessato",
      f"stato={m.get_contatto(cid)['stato']}")

# T19d — transizione di stato (aggiorna/invalida) + filtro per stato
m.update_stato_contatto(cid, "rifiutato", prossima_azione="nessuna")
crf = m.get_contatto(cid)
attivi = m.lista_contatti("interessato")
rifiutati = m.lista_contatti("rifiutato")
check("T19d transizione stato + filtro + invalidazione",
      crf["stato"] == "rifiutato" and crf["stato"] in STATI_CHIUSI
      and crf["ultimo_contatto"] is not None and len(attivi) == 0
      and len(rifiutati) == 1, f"stato={crf['stato']}")

# T19e — stato non valido respinto (CHECK + guardia applicativa)
try:
    m.update_stato_contatto(cid, "stato_inventato")
    _bad = True
except ValueError:
    _bad = False
check("T19e stato non valido respinto", _bad is False)

# T19f — IMMUTABILITÀ del diario: UPDATE e DELETE devono FALLIRE (trigger DB)
con = _sqlite3.connect(str(m.db_path))
up_bloccato = del_bloccato = False
try:
    con.execute("UPDATE diario SET descrizione='manomesso' WHERE id=?", (id1,)); con.commit()
except _sqlite3.Error:
    up_bloccato = True
try:
    con.execute("DELETE FROM diario WHERE id=?", (id1,)); con.commit()
except _sqlite3.Error:
    del_bloccato = True
con.close()
righe_intatte = len(m.diario_recente(10)) == 2 and m.diario_recente(10)[-1]["descrizione"] == "avvio GAS"
check("T19f diario immutabile (UPDATE e DELETE bloccati)",
      up_bloccato and del_bloccato and righe_intatte,
      f"up={up_bloccato} del={del_bloccato} intatte={righe_intatte}")

# T19g — diario_di_contatto lega gli eventi al lead
m.append_diario("messaggio", "inviato DM", contatto_id=cid)
m.append_diario("messaggio", "nessuna risposta", contatto_id=cid)
eventi = m.diario_di_contatto(cid)
check("T19g diario_di_contatto filtra per lead",
      len(eventi) == 2 and all(e["contatto_id"] == cid for e in eventi),
      f"n={len(eventi)}")

# T19h — backup: produce una copia LEGGIBILE con gli stessi dati
bdir = tempfile.mkdtemp(prefix="gas_mem_bak_")
bpath = m.backup(bdir)
ok_bak = False
if bpath and bpath.exists():
    cb = _sqlite3.connect(str(bpath))
    n_diario = cb.execute("SELECT COUNT(*) FROM diario").fetchone()[0]
    n_contatti = cb.execute("SELECT COUNT(*) FROM contatti").fetchone()[0]
    cb.close()
    ok_bak = n_diario == 4 and n_contatti == 1
check("T19h backup -> copia leggibile con gli stessi dati", ok_bak,
      f"path={bpath}")

# T19i — fail-safe: DB ASSENTE viene creato, le operazioni funzionano (no crash)
d_new = tempfile.mkdtemp(prefix="gas_mem_new_")
p_new = default_db_path(d_new)
m_new = MemoryStore(p_new)
check("T19i DB assente -> creato e operativo",
      m_new.available and isinstance(m_new.append_diario("x", "y"), int)
      and p_new.exists())

# T19j — fail-safe: DB CORROTTO non crasha, degrada a valori sicuri
d_bad = tempfile.mkdtemp(prefix="gas_mem_bad_")
p_bad = Path(d_bad) / "corrotto.db"
p_bad.write_bytes(b"questo non e' un database sqlite, e' spazzatura binaria")
m_bad = MemoryStore(p_bad)  # init non deve sollevare
check("T19j DB corrotto -> degrada senza crash",
      m_bad.available is False and m_bad.append_diario("x", "y") is None
      and m_bad.diario_recente(5) == [] and m_bad.get_contatto(1) is None
      and m_bad.lista_contatti() == [])

# ---------- T20: aggancio diario a run_turn (FASE 2 fetta 2a, SOLO scrittura) ----------
# Round-trip agentico REALE a ZERO token: client finto SCRIPTATO. Verifica che
# il loop scriva UNA riga di diario per OGNI tool call, nell'ordine giusto,
# con l'esito (anche negativo), e che la memoria degradata NON fermi il turno.

class ScriptedCompletions:
    """Risponde seguendo uno 'script': ogni elemento è o una stringa (risposta
    finale) o una lista di (name, arguments) -> assistant con quei tool_calls."""
    def __init__(self, script):
        self._script = list(script)
        self._i = 0
    def create(self, model=None, messages=None, tools=None, tool_choice=None):
        step = self._script[self._i] if self._i < len(self._script) else "fine"
        self._i += 1
        if isinstance(step, str):
            msg = SimpleNamespace(content=step, tool_calls=None)
        else:
            tcs = [SimpleNamespace(id=f"d{self._i}_{j}",
                   function=SimpleNamespace(name=n, arguments=a))
                   for j, (n, a) in enumerate(step)]
            msg = SimpleNamespace(content=None, tool_calls=tcs)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])

def run_turn_scriptato(k, prompt, script):
    """Esegue un round-trip di run_turn col client scriptato, isolando l'ambiente
    (un solo provider deterministico: gemini-flash-lite, gli altri rung spenti)."""
    saved = {kk: os.environ.get(kk) for kk in
             ("GEMINI_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY", "GAS_OLLAMA_URL")}
    for kk in ("GROQ_API_KEY", "OPENROUTER_API_KEY", "GAS_OLLAMA_URL"):
        os.environ.pop(kk, None)
    os.environ["GEMINI_API_KEY"] = "dummy-for-test"
    class _FakeOpenAI:
        def __init__(self, base_url=None, api_key=None):
            self.chat = SimpleNamespace(completions=ScriptedCompletions(script))
    _orig = gas.OpenAI
    gas.OpenAI = _FakeOpenAI
    try:
        return list(k.run_turn(prompt))
    finally:
        gas.OpenAI = _orig
        for kk, v in saved.items():
            if v is None: os.environ.pop(kk, None)
            else: os.environ[kk] = v

# T20a — round-trip MULTI-TOOL: una riga di diario per ogni tool, ordine giusto
k = kernel_tmp()
script_a = [[("write_file", '{"relative_path": "uno.txt", "content": "1"}'),
            ("write_file", '{"relative_path": "due.txt", "content": "2"}'),
            ("read_file",  '{"relative_path": "uno.txt"}')],
           "fatto tutto"]
ev_a = run_turn_scriptato(k, "scrivi e leggi", script_a)
diario_a = k.memory.diario_recente(10)  # DESC: più recente prima
# atteso (in ordine cronologico): write uno, write due, read uno
crono = list(reversed(diario_a))
ordine_ok = (len(diario_a) == 3
             and "path='uno.txt'" in crono[0]["descrizione"] and crono[0]["tipo"] == "write_file"
             and "path='due.txt'" in crono[1]["descrizione"] and crono[1]["tipo"] == "write_file"
             and "path='uno.txt'" in crono[2]["descrizione"] and crono[2]["tipo"] == "read_file")
final_a = [e for e in ev_a if e["type"] == "final"]
check("T20a round-trip multi-tool: 1 riga/diario per tool, ordine giusto",
      ordine_ok and len(final_a) == 1,
      f"n={len(diario_a)} tipi={[r['tipo'] for r in crono]} final={len(final_a)}")

# T20b — tutti gli esiti delle write sono OK e la read di file esistente è OK
esiti_a = [r["descrizione"].split("|")[-1].strip() for r in crono]
check("T20b esiti positivi marcati [OK]", all(e.startswith("[OK]") for e in esiti_a),
      f"esiti={esiti_a}")

# T20c — tool che FALLISCE: il diario registra [KO] E il loop prosegue/termina
k = kernel_tmp()
script_c = [[("read_file", '{"relative_path": "non_esiste.txt"}')], "gestito l'errore"]
ev_c = run_turn_scriptato(k, "leggi inesistente", script_c)
diario_c = k.memory.diario_recente(5)
final_c = [e for e in ev_c if e["type"] == "final"]
err_c = [e for e in ev_c if e["type"] == "error"]
check("T20c tool fallito -> diario [KO] e turno NON interrotto",
      len(diario_c) == 1 and "[KO]" in diario_c[0]["descrizione"]
      and diario_c[0]["tipo"] == "read_file"
      and len(final_c) == 1 and len(err_c) == 0,
      f"diario={diario_c[0]['descrizione'][:80] if diario_c else 'VUOTO'} final={len(final_c)}")

# T20d — memoria DEGRADATA (DB corrotto): il round-trip funziona comunque
k = kernel_tmp()
p_corr = Path(os.environ["GAS_CWD"]) / "mem_corrotta.db"
p_corr.write_bytes(b"spazzatura non-sqlite")
k.memory = MemoryStore(p_corr)  # available=False
script_d = [[("write_file", '{"relative_path": "vivo.txt", "content": "ok"}')], "concluso"]
ev_d = run_turn_scriptato(k, "scrivi con memoria rotta", script_d)
final_d = [e for e in ev_d if e["type"] == "final"]
check("T20d memoria degradata -> round-trip OK, turno non interrotto",
      k.memory.available is False and len(final_d) == 1
      and (Path(os.environ["GAS_CWD"]) / "vivo.txt").exists()
      and k.memory.diario_recente(5) == [],
      f"available={k.memory.available} final={len(final_d)}")

# T20e — memoria ASSENTE (self.memory = None): il loop non deve mai cadere
k = kernel_tmp()
k.memory = None
ev_e = run_turn_scriptato(k, "memoria None", [[("read_file", '{"relative_path": "x.txt"}')], "ok"])
check("T20e memoria None -> nessun crash, turno completato",
      len([e for e in ev_e if e["type"] == "final"]) == 1)

# ---------- T21: lato LETTURA della memoria (FASE 2 fetta 2b) ----------
# Pin always-on nel system message + tool ricorda(). Tutto locale, ZERO token.

# Helper: popola la memoria di un kernel con lead (attivi/chiusi) ed eventi.
def _popola(k):
    cid = k.memory.upsert_contatto("mario@ex.com", nome="Mario", contatto="mario@ex.com",
                                   prossima_azione="inviare preventivo")
    k.memory.update_stato_contatto(cid, "interessato")
    k.memory.upsert_contatto("luca@ex.com", nome="Luca")  # resta 'nuovo' (attivo)
    cchiuso = k.memory.upsert_contatto("spam@ex.com", nome="Spammer")
    k.memory.update_stato_contatto(cchiuso, "rifiutato")  # chiuso -> fuori dal pin
    # eventi: alcuni "veri" (write_file/messaggio), altri rumore (read_file/run_command/ricorda)
    k.memory.append_diario("write_file", "path='piano.txt' | [OK] scritto")
    k.memory.append_diario("messaggio", "DM inviato a Mario", contatto_id=cid)
    k.memory.append_diario("read_file", "path='x.txt' | [OK] letto")     # rumore
    k.memory.append_diario("run_command", "command='ls' | [OK]")          # rumore
    k.memory.append_diario("ricorda", "query=storia | [OK]")              # rumore
    return cid

# T21a — il pin contiene i lead ATTIVI e gli eventi VERI, esclude chiusi e rumore
k = kernel_tmp(); _popola(k)
pin = k._memoria_pin()
# NB: la parola "ricorda" compare nell'intestazione del pin (rimando al tool):
# si verifica l'assenza delle DESCRIZIONI degli eventi-rumore, non della parola.
check("T21a pin: lead attivi + azioni vere, no chiusi/rumore",
      "# MEMORIA" in pin and "Mario" in pin and "Luca" in pin
      and "Spammer" not in pin                       # lead chiuso escluso
      and "DM inviato a Mario" in pin and "piano.txt" in pin
      and "x.txt" not in pin                          # evento read_file escluso
      and "command='ls'" not in pin                   # evento run_command escluso
      and "query=storia" not in pin,                  # evento ricorda escluso
      f"len={len(pin)} pin={pin!r}")

# T21b — pin VUOTO con memoria vuota e con memoria None (fail-safe)
k_vuoto = kernel_tmp()
pin_vuoto = k_vuoto._memoria_pin()
k_none = kernel_tmp(); k_none.memory = None
check("T21b pin vuoto se memoria vuota o None",
      pin_vuoto == "" and k_none._memoria_pin() == "",
      f"vuoto={pin_vuoto!r}")

# T21c — ricorda(contatto=...) restituisce scheda + storia del lead
k = kernel_tmp(); cid = _popola(k)
r_c = k._ricorda(contatto="mario")
check("T21c ricorda per contatto -> scheda + storia",
      "CONTATTO Mario" in r_c and "interessato" in r_c
      and "inviare preventivo" in r_c and "DM inviato a Mario" in r_c,
      r_c[:80])

# T21d — ricorda(query=...) filtra il diario per testo
r_q = k._ricorda(query="preventivo")  # nessun evento contiene 'preventivo' nel testo
r_q2 = k._ricorda(query="DM")
check("T21d ricorda per query filtra il diario",
      "Diario per 'preventivo' (0)" in r_q and "DM inviato a Mario" in r_q2,
      r_q2[:80])

# T21e — ricorda() default: ultimi eventi del diario (rumore incluso: è lettura esplicita)
r_def = k._ricorda()
check("T21e ricorda default -> ultimi eventi",
      "Ultimi" in r_def and "eventi del diario" in r_def and "DM inviato a Mario" in r_def,
      r_def[:60])

# T21f — INIEZIONE nel payload: pin nel system message, finestra INTATTA
captured = {}
class RecordingCompletions:
    def __init__(self, *a, **kw): pass
    def create(self, model=None, messages=None, tools=None, tool_choice=None):
        captured.setdefault("msgs", messages)
        captured.setdefault("tools", tools)
        return SimpleNamespace(choices=[SimpleNamespace(
            message=SimpleNamespace(content="ho finito", tool_calls=None))])
def run_turn_recording(k, prompt):
    saved = {kk: os.environ.get(kk) for kk in
             ("GEMINI_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY", "GAS_OLLAMA_URL")}
    for kk in ("GROQ_API_KEY", "OPENROUTER_API_KEY", "GAS_OLLAMA_URL"):
        os.environ.pop(kk, None)
    os.environ["GEMINI_API_KEY"] = "dummy-for-test"
    class _FO:
        def __init__(self, base_url=None, api_key=None):
            self.chat = SimpleNamespace(completions=RecordingCompletions())
    _orig = gas.OpenAI; gas.OpenAI = _FO
    try:
        return list(k.run_turn(prompt))
    finally:
        gas.OpenAI = _orig
        for kk, v in saved.items():
            if v is None: os.environ.pop(kk, None)
            else: os.environ[kk] = v

k = kernel_tmp(); _popola(k)
ev_f = run_turn_recording(k, "che situazione abbiamo?")
msgs = captured.get("msgs", [])
tool_names = {t["function"]["name"] for t in (captured.get("tools") or [])}
sys0 = msgs[0] if msgs else {}
finestra_pulita = len(msgs) >= 2 and all(m["role"] != "system" for m in msgs[1:]) and msgs[1]["role"] == "user"
check("T21f iniezione: pin nel system, 1 solo system, finestra parte da user",
      sys0.get("role") == "system" and "# MEMORIA" in sys0.get("content", "")
      and "Mario" in sys0["content"] and finestra_pulita
      and "ricorda" in tool_names
      and len([e for e in ev_f if e["type"] == "final"]) == 1,
      f"n_msgs={len(msgs)} ruoli={[m['role'] for m in msgs]}")

# T21g — fail-safe lettura: memoria degradata -> pin vuoto, round-trip OK, ricorda gentile
k = kernel_tmp()
p_corr = Path(os.environ["GAS_CWD"]) / "mem_lett_corrotta.db"
p_corr.write_bytes(b"non-sqlite")
k.memory = MemoryStore(p_corr)  # available=False
captured.clear()
ev_g = run_turn_recording(k, "ciao")
msgs_g = captured.get("msgs", [])
ric_g = k._ricorda()  # degradato: nessun crash, stringa gentile
k.memory = None
ric_none = k._ricorda(contatto="x")
check("T21g memoria degradata/None -> pin vuoto, turno OK, ricorda non crasha",
      k._memoria_pin() == "" and "# MEMORIA" not in (msgs_g[0]["content"] if msgs_g else "")
      and len([e for e in ev_g if e["type"] == "final"]) == 1
      and isinstance(ric_g, str)
      and ric_none == "Memoria non disponibile: nessun ricordo accessibile.",
      f"ric_g={ric_g[:40]!r}")

# T21h — il pin rispetta il tetto MEMORY_PIN_CHAR_CAP (troncamento del testo).
# I cap per-conteggio (6 eventi) da soli non bastano a sforare: servono eventi
# LUNGHI (6 × ~600 char > 3000) per esercitare davvero il troncamento testuale.
k = kernel_tmp()
for i in range(10):
    k.memory.append_diario("messaggio", f"evento {i}: " + "x" * 600)
pin_big = k._memoria_pin()
check("T21h pin capato a MEMORY_PIN_CHAR_CAP (no slicing della storia)",
      len(pin_big) <= k.MEMORY_PIN_CHAR_CAP + len("\n\n") + len("\n…[memoria troncata]")
      and "memoria troncata" in pin_big,
      f"len_pin={len(pin_big)} cap={k.MEMORY_PIN_CHAR_CAP}")

# ---------- T22: scrittura contatti dal loop + chiusura riserve R1/R2/R3 ----------
from modules.memory import STATI_CONTATTO

# T22a — salva_contatto crea e poi aggiorna (via execute_tool_call), no duplicati
k = kernel_tmp()
o1 = k.execute_tool_call("salva_contatto", {"chiave": "anna@ex.com", "nome": "Anna",
                                            "prossima_azione": "chiamare"})
o2 = k.execute_tool_call("salva_contatto", {"chiave": "anna@ex.com", "note": "VIP"})
c = k.memory.get_contatto_per_chiave("anna@ex.com")
check("T22a salva_contatto crea+aggiorna senza duplicare",
      o1.startswith("Successo") and o2.startswith("Successo")
      and c is not None and c["nome"] == "Anna" and c["note"] == "VIP"
      and c["stato"] == "nuovo" and len(k.memory.lista_contatti()) == 1,
      f"o1={o1[:40]} c={c['nome'] if c else None}")

# T22b — salva_contatto senza chiave -> negato; memoria None -> messaggio, no crash
o_noch = k.execute_tool_call("salva_contatto", {"nome": "SenzaChiave"})
k_none = kernel_tmp(); k_none.memory = None
o_none = k_none.execute_tool_call("salva_contatto", {"chiave": "x@y.z"})
check("T22b salva_contatto: chiave mancante negata, memoria None gestita",
      "Operazione negata" in o_noch and "Memoria non disponibile" in o_none,
      f"noch={o_noch[:40]} none={o_none[:40]}")

# T22c — imposta_stato_contatto: cambia stato; inesistente/stato invalido -> negato
o_st = k.execute_tool_call("imposta_stato_contatto", {"chiave": "anna@ex.com", "stato": "interessato"})
o_inex = k.execute_tool_call("imposta_stato_contatto", {"chiave": "ghost@ex.com", "stato": "interessato"})
o_bad = k.execute_tool_call("imposta_stato_contatto", {"chiave": "anna@ex.com", "stato": "fantasia"})
check("T22c imposta_stato: ok + inesistente/stato-invalido negati",
      o_st.startswith("Successo")
      and k.memory.get_contatto_per_chiave("anna@ex.com")["stato"] == "interessato"
      and "nessun lead" in o_inex and "non valido" in o_bad,
      f"st={o_st[:40]} inex={o_inex[:30]} bad={o_bad[:30]}")

# T22d — store.get_contatto_per_chiave: lookup esatto + None se assente
check("T22d get_contatto_per_chiave: esatto + None",
      k.memory.get_contatto_per_chiave("anna@ex.com") is not None
      and k.memory.get_contatto_per_chiave("non@esiste.x") is None)

# T22e (R1) — _trova_contatto: chiave esatta ha priorità + nota su match multipli
k = kernel_tmp()
k.memory.upsert_contatto("mario.rossi@ex.com", nome="Mario Rossi")
k.memory.upsert_contatto("mario.bianchi@ex.com", nome="Mario Bianchi")
m_exact, nota_exact = k._trova_contatto("mario.rossi@ex.com")   # chiave esatta
m_amb, nota_amb = k._trova_contatto("mario")                    # substring -> 2 match
check("T22e (R1) match esatto prioritario + ambiguità segnalata",
      m_exact is not None and m_exact["chiave"] == "mario.rossi@ex.com" and nota_exact is None
      and m_amb is not None and nota_amb is not None and "2 lead corrispondono" in nota_amb,
      f"nota_amb={nota_amb}")

# T22f (R2) — override via env dei tetti del pin + fail-safe su valore sporco
import gas as _gasmod
_saved_env = {kk: os.environ.get(kk) for kk in
              ("GAS_MEMORY_PIN_CHARS", "GAS_MEMORY_PIN_CONTACTS", "GAS_MEMORY_PIN_EVENTS")}
os.environ["GAS_MEMORY_PIN_CHARS"] = "5000"
os.environ["GAS_MEMORY_PIN_EVENTS"] = "abc"   # sporco -> default
try:
    k_env = kernel_tmp()
    ok_env = (k_env.MEMORY_PIN_CHAR_CAP == 5000
              and k_env.MEMORY_PIN_EVENTS == GasKernel.MEMORY_PIN_EVENTS  # default per valore sporco
              and _gasmod._env_int("NON_ESISTE_XYZ", 7) == 7
              and _gasmod._env_int("GAS_MEMORY_PIN_CHARS", 9999, min_val=200) == 5000)
finally:
    for kk, v in _saved_env.items():
        if v is None: os.environ.pop(kk, None)
        else: os.environ[kk] = v
check("T22f (R2) override env dei tetti memoria + fail-safe valore sporco", ok_env,
      f"chars={k_env.MEMORY_PIN_CHAR_CAP} events={k_env.MEMORY_PIN_EVENTS}")

# T22g (R3) — scansione robusta: un'azione vera resta visibile sotto rumore denso
k = kernel_tmp()
k.memory.append_diario("messaggio", "AZIONE VERA molto indietro")  # la più vecchia
for i in range(40):                                                # 40 eventi di rumore più recenti
    k.memory.append_diario("read_file", f"path='f{i}.txt' | [OK]")
pin_r3 = k._memoria_pin()
check("T22g (R3) azione vera emerge sotto 40 eventi di rumore (scan ampio)",
      "AZIONE VERA molto indietro" in pin_r3 and "f39.txt" not in pin_r3,
      f"scan={k.MEMORY_PIN_SCAN}")

# T22h — ROUND-TRIP: l'agente popola la rubrica e il pin la riflette
k = kernel_tmp()
script_h = [[("salva_contatto", '{"chiave":"lucia@ex.com","nome":"Lucia","prossima_azione":"inviare offerta"}'),
            ("imposta_stato_contatto", '{"chiave":"lucia@ex.com","stato":"interessato"}')],
           "rubrica aggiornata"]
ev_h = run_turn_scriptato(k, "registra Lucia come lead interessato", script_h)
c_h = k.memory.get_contatto_per_chiave("lucia@ex.com")
diario_h = [r["tipo"] for r in k.memory.diario_recente(5)]
pin_h = k._memoria_pin()
check("T22h round-trip: rubrica popolata dal loop + diario + pin riflette",
      c_h is not None and c_h["stato"] == "interessato"
      and "salva_contatto" in diario_h and "imposta_stato_contatto" in diario_h
      and "Lucia" in pin_h and "interessato" in pin_h
      and len([e for e in ev_h if e["type"] == "final"]) == 1,
      f"stato={c_h['stato'] if c_h else None} diario={diario_h}")

# ---------- T23: normalizzazione chiavi lead (R-crm-1) ----------
from modules.memory import normalizza_chiave

# T23a — due chiavi che differiscono solo per maiuscole/spazi -> STESSO record, no doppione
m23 = mem_tmp()
id_a = m23.upsert_contatto("Anna ", nome="Anna")
id_b = m23.upsert_contatto(" anna", note="seconda")          # equivalente -> update, non insert
got23 = m23.get_contatto_per_chiave("ANNA")                  # lookup con altra forma ancora
check("T23a (R-crm-1) chiavi equivalenti = stesso record, nessun doppione",
      id_a == id_b and len(m23.lista_contatti()) == 1 and got23 is not None
      and got23["chiave"] == "anna" and got23["nome"] == "Anna"
      and got23["note"] == "seconda",
      f"id_a={id_a} id_b={id_b} n={len(m23.lista_contatti())}")

# T23b — imposta_stato_contatto trova il lead con chiave NON normalizzata in input
k23 = kernel_tmp()
k23.execute_tool_call("salva_contatto", {"chiave": "Bob White", "nome": "Bob"})
o23 = k23.execute_tool_call("imposta_stato_contatto",
                            {"chiave": "  bob   white ", "stato": "interessato"})
c23 = k23.memory.get_contatto_per_chiave("BOB WHITE")
check("T23b update_stato trova il lead con chiave non normalizzata in input",
      o23.startswith("Successo") and c23 is not None and c23["stato"] == "interessato"
      and len(k23.memory.lista_contatti()) == 1,
      f"o={o23[:50]} n={len(k23.memory.lista_contatti())}")

# T23c — fail-safe: chiave None / vuota / non-stringa -> nessun crash, degrado sicuro
no_crash23 = True
try:
    r1 = normalizza_chiave(None)
    r2 = normalizza_chiave("   ")
    r3 = normalizza_chiave(12345)
    m23c = mem_tmp()
    look_none = m23c.get_contatto_per_chiave(None)   # non deve sollevare
except Exception as e:
    no_crash23 = False
    r1 = r2 = r3 = repr(e); look_none = "CRASH"
check("T23c fail-safe: chiave None/vuota/non-stringa -> nessun crash",
      no_crash23 and r1 == "" and r2 == "" and r3 == "12345" and look_none is None,
      f"r1={r1!r} r2={r2!r} r3={r3!r} look_none={look_none!r}")

# T23d — la normalizzazione è IDEMPOTENTE: normalizza(normalizza(x)) == normalizza(x)
campioni23 = ["Anna ", "  BOB   white ", "x@Y.Z", "", "Multi\tTab\nNewline", "ÀÉÎ"]
idem23 = all(normalizza_chiave(normalizza_chiave(s)) == normalizza_chiave(s)
             for s in campioni23)
check("T23d normalizzazione idempotente + esiti attesi",
      idem23 and normalizza_chiave("Anna ") == "anna"
      and normalizza_chiave("  BOB   white ") == "bob white",
      f"idem={idem23}")

# T23e — coerenza scrittura-normalizzata <-> lettura-substring: il lead salvato con
# chiave NON normalizzata resta TROVABILE via ricorda con varianti di case/spazi.
# (chiave "  Anna   Rossi " -> storata "anna rossi"; "anna rossi" risolve via match
# esatto normalizzato, "ANNA" via substring case-insensitive).
k23e = kernel_tmp()
k23e.execute_tool_call("salva_contatto", {"chiave": "  Anna   Rossi ", "nome": "Anna Rossi"})
o_e1 = k23e.execute_tool_call("ricorda", {"contatto": "anna rossi"})  # variante normalizzata
o_e2 = k23e.execute_tool_call("ricorda", {"contatto": "ANNA"})         # variante case, substring
check("T23e lettura substring trova il lead salvato con chiave normalizzata",
      "Anna Rossi" in o_e1 and "Nessun lead" not in o_e1
      and "Anna Rossi" in o_e2 and "Nessun lead" not in o_e2,
      f"e1={o_e1[:60]!r} e2={o_e2[:60]!r}")

# T23f — la normalizzazione NON fonde identità cross-formato (e NON deve: niente
# fuzzy). 'anna@ex.com' (norm-> 'anna@ex.com') e 'Anna' (norm-> 'anna') sono stringhe
# diverse -> restano DUE record finché non si chiede ESPLICITAMENTE la fusione
# (R-crm-1b, ora chiusa dal tool unisci_contatti — vedi T24). Questo test blinda il
# confine: la canonicalizzazione lessicale resta deterministica e non indovina mai.
k23f = kernel_tmp()
k23f.execute_tool_call("salva_contatto", {"chiave": "anna@ex.com", "nome": "Anna"})
k23f.execute_tool_call("salva_contatto", {"chiave": "Anna", "nome": "Anna"})
n_rec = len(k23f.memory.lista_contatti())
check("T23f (R-crm-1b APERTA) normalizzazione NON fonde identità cross-formato",
      n_rec == 2
      and k23f.memory.get_contatto_per_chiave("anna@ex.com") is not None
      and k23f.memory.get_contatto_per_chiave("Anna") is not None
      and k23f.memory.get_contatto_per_chiave("Anna")["chiave"] == "anna",
      f"n_record={n_rec}")

# ---------- T24: fusione lead cross-formato (R-crm-1b) — merge a lapide ----------
# Chiude R-crm-1b: lo STESSO lead salvato con chiavi diverse (es. nome + email) si
# fonde in modo NON distruttivo e compatibile con l'immutabilità del diario.

# T24a — unisci_contatti: 'da' diventa lapide del 'verso', UN solo lead vivo,
# le vecchie chiavi risolvono ENTRAMBE al canonico, anagrafica completata.
k24 = kernel_tmp()
k24.execute_tool_call("salva_contatto", {"chiave": "Anna", "nome": "Anna"})
k24.execute_tool_call("salva_contatto", {"chiave": "anna@ex.com", "contatto": "anna@ex.com"})
o24 = k24.execute_tool_call("unisci_contatti", {"chiave_da": "Anna", "chiave_verso": "anna@ex.com"})
vivi24 = k24.memory.lista_contatti()                       # esclude le lapidi
canon = k24.memory.get_contatto_per_chiave("anna@ex.com")
via_vecchia = k24.memory.get_contatto_per_chiave("Anna")   # vecchia chiave -> canonico
check("T24a unisci_contatti: lapide + 1 lead vivo + vecchia chiave risolve al canonico",
      o24.startswith("Successo") and len(vivi24) == 1
      and canon is not None and via_vecchia is not None
      and canon["id"] == via_vecchia["id"]
      and canon["chiave"] == "anna@ex.com"
      and canon["nome"] == "Anna" and canon["contatto"] == "anna@ex.com",
      f"o={o24[:50]} vivi={len(vivi24)}")

# T24b — la STORIA è preservata: gli eventi del doppione confluiscono nel canonico
# (diario IMMUTABILE: nessun UPDATE/DELETE, espansione in diario_di_contatto).
k24b = kernel_tmp()
k24b.execute_tool_call("salva_contatto", {"chiave": "Bob", "nome": "Bob"})
id_bob = k24b.memory.get_contatto_per_chiave("Bob")["id"]
k24b.memory.append_diario("nota", "primo contatto con Bob", contatto_id=id_bob)
k24b.execute_tool_call("salva_contatto", {"chiave": "bob@ex.com", "contatto": "bob@ex.com"})
id_email = k24b.memory.get_contatto_per_chiave("bob@ex.com")["id"]
k24b.memory.append_diario("nota", "offerta inviata via email", contatto_id=id_email)
k24b.memory.unisci_contatti("Bob", "bob@ex.com")           # canonico = bob@ex.com
canon_id = k24b.memory.get_contatto_per_chiave("bob@ex.com")["id"]
storia = [e["descrizione"] for e in k24b.memory.diario_di_contatto(canon_id)]
check("T24b la storia del doppione confluisce nel canonico (diario immutabile)",
      any("primo contatto" in d for d in storia)
      and any("offerta inviata" in d for d in storia),
      f"storia={storia}")

# T24c — fail-safe/idempotenza: chiave inesistente negata; fondere ciò che è già
# fuso (o un lead in se stesso) è un no-op; chiavi mancanti negate.
k24c = kernel_tmp()
k24c.execute_tool_call("salva_contatto", {"chiave": "carla@ex.com", "nome": "Carla"})
o_ghost = k24c.execute_tool_call("unisci_contatti", {"chiave_da": "ghost", "chiave_verso": "carla@ex.com"})
o_noargs = k24c.execute_tool_call("unisci_contatti", {"chiave_da": "carla@ex.com"})
o_self = k24c.execute_tool_call("unisci_contatti", {"chiave_da": "carla@ex.com", "chiave_verso": "carla@ex.com"})
o_again = k24c.execute_tool_call("unisci_contatti", {"chiave_da": "carla@ex.com", "chiave_verso": "carla@ex.com"})
check("T24c fail-safe: inesistente/args mancanti negati; self-merge e ri-merge = no-op",
      "Operazione negata" in o_ghost and "Operazione negata" in o_noargs
      and o_self.startswith("Successo") and o_again.startswith("Successo")
      and len(k24c.memory.lista_contatti()) == 1,
      f"ghost={o_ghost[:40]} self={o_self[:40]}")

# T24d — il pin always-on NON mostra le lapidi (solo lead canonici), memoria None
# gestita senza crash.
k24d = kernel_tmp()
k24d.execute_tool_call("salva_contatto", {"chiave": "Dora", "nome": "Dora"})
k24d.execute_tool_call("salva_contatto", {"chiave": "dora@ex.com", "contatto": "dora@ex.com"})
k24d.execute_tool_call("unisci_contatti", {"chiave_da": "Dora", "chiave_verso": "dora@ex.com"})
pin24 = k24d._memoria_pin()
no_crash_none = True
try:
    k24d_none = kernel_tmp(); k24d_none.memory = None
    o_none24 = k24d_none.execute_tool_call("unisci_contatti", {"chiave_da": "a", "chiave_verso": "b"})
except Exception as e:
    no_crash_none = False; o_none24 = repr(e)
check("T24d pin mostra 1 sola scheda (no lapidi) + memoria None gestita",
      pin24.count("Dora") == 1 and no_crash_none and "non disponibile" in o_none24,
      f"pin_dora={pin24.count('Dora')} none={o_none24[:40]}")

# T24e — catena profonda al più 1: A->B poi B->C ri-punta A direttamente a C
# (invariante: ogni lapide punta a un canonico VIVO).
k24e = kernel_tmp()
for ch in ("a@ex.com", "b@ex.com", "c@ex.com"):
    k24e.execute_tool_call("salva_contatto", {"chiave": ch, "nome": ch})
k24e.memory.unisci_contatti("a@ex.com", "b@ex.com")   # A -> B
k24e.memory.unisci_contatti("b@ex.com", "c@ex.com")   # B -> C (deve ri-puntare A a C)
canon_c = k24e.memory.get_contatto_per_chiave("c@ex.com")
risolve_a = k24e.memory.get_contatto_per_chiave("a@ex.com")   # deve dare C
risolve_b = k24e.memory.get_contatto_per_chiave("b@ex.com")   # deve dare C
check("T24e catena profonda <=1: A->B->C, sia A sia B risolvono al canonico C",
      len(k24e.memory.lista_contatti()) == 1
      and risolve_a is not None and risolve_b is not None
      and risolve_a["id"] == canon_c["id"] and risolve_b["id"] == canon_c["id"],
      f"vivi={len(k24e.memory.lista_contatti())}")

# T24f — MIGRAZIONE su DB LEGACY: una tabella `contatti` senza la colonna
# merged_into (com'era prima di R-crm-1b) deve aprirsi SENZA degrado, col dato
# preesistente intatto, e supportare subito unisci_contatti. Blinda il bug
# d'ordine ALTER/CREATE INDEX trovato in review (l'indice non deve precedere la
# colonna). Costruisce a mano lo schema VECCHIO, poi apre MemoryStore sopra.
d24f = tempfile.mkdtemp(prefix="gas_mem_legacy_")
legacy_db = Path(d24f) / "old.db"
_con = _sqlite3.connect(str(legacy_db))
_con.executescript("""
    CREATE TABLE contatti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chiave TEXT NOT NULL UNIQUE, nome TEXT, contatto TEXT,
        stato TEXT NOT NULL DEFAULT 'nuovo', ultimo_contatto TEXT,
        prossima_azione TEXT, note TEXT,
        creato_il TEXT NOT NULL, aggiornato_il TEXT NOT NULL
    );
    INSERT INTO contatti (chiave, nome, stato, creato_il, aggiornato_il)
    VALUES ('vecchio@ex.com', 'Vecchio Lead', 'interessato', '2026-01-01', '2026-01-01');
""")
_con.commit(); _con.close()
m24f = MemoryStore(legacy_db)                 # apertura -> deve migrare, non degradare
pre = m24f.get_contatto_per_chiave("vecchio@ex.com")
# e un merge sul DB migrato deve funzionare
m24f.upsert_contatto("nuovo@ex.com", nome="Stesso Lead")
cid_mig = m24f.unisci_contatti("nuovo@ex.com", "vecchio@ex.com")
check("T24f migrazione DB legacy: available, dato intatto, merge funziona",
      m24f.available is True and pre is not None
      and pre["nome"] == "Vecchio Lead" and pre["stato"] == "interessato"
      and cid_mig is not None and len(m24f.lista_contatti()) == 1,
      f"available={m24f.available} pre={pre is not None} cid={cid_mig}")

# ---------- T25: ricerca testuale FTS5 sul diario (Vector DB Strato A) ----------
# Ricerca per parole/radici dentro lo stesso .db, ranking BM25, fail-safe con
# fallback substring. Tutto locale, ZERO token.

# T25a — cerca_diario trova per RADICE (prefix) e ignora i caratteri speciali
m25 = mem_tmp()
m25.append_diario("nota", "offerta fitness inviata ad Anna")
m25.append_diario("nota", "chiamata con Marco per il preventivo")
m25.append_diario("messaggio", "DM inviato a Lucia")
hit_radice = [e["descrizione"] for e in m25.cerca_diario("fitnes", 10)]   # radice -> 'fitness'
hit_safe = m25.cerca_diario('AND OR "(((', 10)                            # niente crash sintassi
hit_none = m25.cerca_diario("inesistente", 10)
check("T25a FTS5: match per radice, query con caratteri speciali non crasha",
      m25.fts_available is True
      and any("fitness" in d for d in hit_radice)
      and isinstance(hit_safe, list) and hit_none == [],
      f"fts={m25.fts_available} radice={hit_radice} safe={type(hit_safe).__name__}")

# T25b — ranking per pertinenza: l'evento con più occorrenze del termine viene prima
m25b = mem_tmp()
m25b.append_diario("nota", "breve cenno al budget")
m25b.append_diario("nota", "budget budget budget: discusso a lungo il budget col cliente")
top = m25b.cerca_diario("budget", 10)
check("T25b FTS5 ranking BM25: il più pertinente viene prima",
      len(top) == 2 and "a lungo" in top[0]["descrizione"],
      f"top0={top[0]['descrizione'][:40] if top else None!r}")

# T25c — backfill su DB con eventi PREESISTENTI: l'indice si popola al rebuild di init.
# Costruisco un DB con diario già pieno SENZA la tabella FTS, poi apro MemoryStore.
d25 = tempfile.mkdtemp(prefix="gas_mem_fts_")
pre_db = Path(d25) / "pre.db"
_c = _sqlite3.connect(str(pre_db))
_c.executescript("""
    CREATE TABLE diario (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL,
        tipo TEXT NOT NULL, descrizione TEXT NOT NULL, contatto_id INTEGER);
    INSERT INTO diario (ts, tipo, descrizione) VALUES ('2026-01-01','nota','vecchia nota su campagna Instagram');
""")
_c.commit(); _c.close()
m25c = MemoryStore(pre_db)
back = [e["descrizione"] for e in m25c.cerca_diario("instagram", 10)]
check("T25c FTS5 backfill indicizza il diario preesistente al rebuild di init",
      m25c.available is True and any("Instagram" in d for d in back),
      f"available={m25c.available} back={back}")

# T25d — integrazione in ricorda(query): usa FTS, immutabilità del diario INTATTA,
# e i vincoli storici di T21d restano veri (preventivo -> 0, DM -> trovato).
k25 = kernel_tmp()
k25.memory.append_diario("nota", "DM inviato a Mario")
k25.memory.append_diario("nota", "spedito catalogo prodotti")
r_dm = k25._ricorda(query="DM")
r_prev = k25._ricorda(query="preventivo")        # nessun evento -> 0 (come T21d)
r_catalogo = k25._ricorda(query="catalog")       # radice -> trova 'catalogo'
# immutabilità: UPDATE sul diario deve restare vietato anche con l'indice FTS attivo
imm_ok = False
try:
    with _sqlite3.connect(str(k25.memory.db_path)) as _cc:
        _cc.execute("UPDATE diario SET descrizione='X' WHERE id=1")
except _sqlite3.Error:
    imm_ok = True
check("T25d ricorda(query) via FTS + vincoli T21d + diario immutabile",
      "DM inviato a Mario" in r_dm and "Diario per 'preventivo' (0)" in r_prev
      and "spedito catalogo" in r_catalogo and imm_ok,
      f"dm={'DM' in r_dm} prev0={'(0)' in r_prev} cat={'catalogo' in r_catalogo} imm={imm_ok}")

# T25e — fail-safe: FTS forzato non-disponibile -> cerca_diario [] e ricorda
# ricade sul substring storico (nessun buco di funzionalità).
m25e = mem_tmp()
m25e.append_diario("nota", "promemoria fattura cliente")
m25e.fts_available = False                        # simula build senza FTS5
deg = m25e.cerca_diario("fattura", 10)
k25e = kernel_tmp()
k25e.memory.append_diario("nota", "promemoria fattura cliente")
k25e.memory.fts_available = False
r_fb = k25e._ricorda(query="fattura")             # deve trovarlo via substring
check("T25e FTS assente -> cerca_diario [] e ricorda ricade su substring",
      deg == [] and "promemoria fattura cliente" in r_fb,
      f"deg={deg} fb={'fattura' in r_fb}")

# ---------- T26: rete di sicurezza della memoria (integrità + backup) ----------
# Il DB di memoria è il dato più prezioso: integrity_check + backup automatico
# rotante + skip su corruzione. Tutto locale, ZERO token.

# T26a — integrity_check: DB sano -> (True,'ok'); file corrotto -> (False, det), no crash
m26 = mem_tmp()
m26.append_diario("nota", "evento")
ok_sano, det_sano = m26.integrity_check()
with open(m26.db_path, "wb") as _f:               # corrompo il file su disco
    _f.write(b"non sono un database sqlite" * 10)
ok_rotto, det_rotto = m26.integrity_check()
check("T26a integrity_check: sano->ok, corrotto->False senza crash",
      ok_sano is True and det_sano == "ok"
      and ok_rotto is False and isinstance(det_rotto, str),
      f"sano={ok_sano}/{det_sano!r} rotto={ok_rotto}")

# T26b — backup crea una copia LEGGIBILE + rotazione tiene le ultime N + retention pura
m26b = mem_tmp()
m26b.upsert_contatto("z@ex.com", nome="Zed")
bdir = Path(tempfile.mkdtemp(prefix="gas_bak_"))
paths = [m26b.backup(bdir, keep=3) for _ in range(5)]   # 5 backup, keep=3
files_rim = sorted(bdir.glob("*.bak"))
last_ok = False
try:
    cc = _sqlite3.connect(str(paths[-1])); cc.row_factory = _sqlite3.Row
    r = cc.execute("SELECT nome FROM contatti WHERE chiave='z@ex.com'").fetchone()
    last_ok = (r is not None and r["nome"] == "Zed"); cc.close()
except Exception:
    last_ok = False
keep_t, drop_t = MemoryStore._backup_retention([Path(f"{i}.bak") for i in range(5)], 2)
check("T26b backup: copia leggibile + rotazione ultime N + retention pura",
      last_ok and len(files_rim) == 3 and len(keep_t) == 2 and len(drop_t) == 3,
      f"rimasti={len(files_rim)} keep={len(keep_t)} drop={len(drop_t)}")

# T26c — backup_auto throttled: prima volta crea, subito dopo NO (non è ora),
# intervallo 0 ricrea sempre
m26c = mem_tmp()
bdir_c = Path(tempfile.mkdtemp(prefix="gas_bak_c_"))
first = m26c.backup_auto(3600, dest_dir=bdir_c)         # nessun backup prima -> crea
second = m26c.backup_auto(3600, dest_dir=bdir_c)        # appena fatto -> non è ora
third = m26c.backup_auto(0, dest_dir=bdir_c)            # intervallo 0 -> sempre ora
check("T26c backup_auto throttled: crea, poi salta, intervallo 0 ricrea",
      first is not None and second is None and third is not None
      and m26c.ultimo_backup(bdir_c) is not None,
      f"first={first is not None} second={second} third={third is not None}")

# T26d — backup_auto NON copia un DB corrotto (non propaga la corruzione nei backup)
m26d = mem_tmp()
bdir_d = Path(tempfile.mkdtemp(prefix="gas_bak_d_"))
with open(m26d.db_path, "wb") as _f:
    _f.write(b"corrotto")
res_d = m26d.backup_auto(0, dest_dir=bdir_d)            # intervallo 0 ma DB rotto
check("T26d backup_auto salta se l'integrità è KO (non propaga corruzione)",
      res_d is None and list(bdir_d.glob("*.bak")) == [],
      f"res={res_d}")

# T26e — kernel _memoria_backup_auto fail-safe: crea il backup + memoria None gestita
k26 = kernel_tmp()
k26.memory.append_diario("nota", "x")
k26._memoria_backup_auto()                             # primo backup (nessuno prima)
bak_kernel = k26.memory.ultimo_backup()
no_crash26 = True
try:
    k26n = kernel_tmp(); k26n.memory = None
    k26n._memoria_backup_auto()                        # memoria None -> deve solo uscire
except Exception:
    no_crash26 = False
check("T26e kernel backup auto: crea backup + memoria None senza crash",
      bak_kernel is not None and no_crash26,
      f"bak={bak_kernel is not None} no_crash={no_crash26}")

# ---------- T27: classificazione errori provider nel doctor (402/429) ----------
# Helper PURO _classify_provider_error: un 402 (crediti esauriti) su un rung
# OPZIONALE è uno stato benigno (la cascata scala da sé a runtime) -> WARN, non KO.
# Tutto locale, ZERO token.

# T27a — 429 -> QUOTA (per qualunque rung); via status_code e via testo
q1 = gas._classify_provider_error(429, "boh", False)
q2 = gas._classify_provider_error(None, "Error code: 429 - rate", True)
check("T27a 429 -> QUOTA (status_code o testo)",
      q1[0] == "QUOTA" and q2[0] == "QUOTA",
      f"q1={q1[0]} q2={q2[0]}")

# T27b — 402 su rung OPZIONALE -> WARN (non KO); via status_code e via testo
w1 = gas._classify_provider_error(402, "Payment Required", False)
w2 = gas._classify_provider_error(None, "Error code: 402 - crediti", False)
check("T27b 402 su rung opzionale -> WARN (non KO)",
      w1[0] == "WARN" and w2[0] == "WARN" and "402" in w1[1],
      f"w1={w1[0]} w2={w2[0]} det={w1[1]!r}")

# T27c — 402 su rung OBBLIGATORIO -> KO (provider a pagamento senza credito = problema)
k1 = gas._classify_provider_error(402, "Payment Required", True)
check("T27c 402 su rung obbligatorio -> KO",
      k1[0] == "KO",
      f"k1={k1[0]}")

# T27d — errore generico -> KO con dettaglio troncato a 60 char (comportamento storico)
lungo = "X" * 200
g1 = gas._classify_provider_error(500, lungo, False)
check("T27d errore generico -> KO, dettaglio <=60 char",
      g1[0] == "KO" and len(g1[1]) == 60,
      f"g1={g1[0]} len={len(g1[1])}")

# ---------- riepilogo ----------
print(f"\n=== RIEPILOGO: {len(PASS)} PASS, {len(FAIL)} FAIL ===")
for f in FAIL:
    print(f"  FAIL: {f}")
sys.exit(1 if FAIL else 0)
