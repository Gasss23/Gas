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

# T11f: retention — mai più di SNAPSHOT_KEEP ref, i più vecchi potati
k.SNAPSHOT_KEEP = 3
for i in range(5):
    k.execute_tool_call("write_file", {"relative_path": "giro.txt", "content": f"giro {i}"})
check("T11f retention pota i ref oltre il limite", len(snap_refs(root)) == 3,
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

# ---------- riepilogo ----------
print(f"\n=== RIEPILOGO: {len(PASS)} PASS, {len(FAIL)} FAIL ===")
for f in FAIL:
    print(f"  FAIL: {f}")
sys.exit(1 if FAIL else 0)
