"""Suite di unit test a ZERO token LLM per il kernel di Gas.

Tutto gira su root temporanee con client API finto iniettato in gas.OpenAI:
nessuna chiamata reale, nessuna scrittura su .gas_history.json del repo.
"""
import json
import os
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
    tmp = tempfile.mkdtemp(prefix="gas_test_")
    os.environ["GAS_CWD"] = tmp
    return GasKernel(root_dir=tmp)

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
try:
    k = kernel_tmp()
    eventi = list(k.run_turn("ciao test loop"))  # corto, no keyword -> 'semplice' -> 3 provider
finally:
    gas.OpenAI = _vero_openai

tool_res = [e for e in eventi if e["type"] == "tool_res"]
errori = [e for e in eventi if e["type"] == "error"]
check("T9a ogni provider cappato a 10 iterazioni",
      all(n == 10 for n in chiamate.values()) and len(chiamate) == 3,
      f"chiamate per modello: {chiamate}")
check("T9b loop infinito assorbito senza crash, pipeline esausta dichiarata",
      len(errori) == 1 and errori[0]["content"] == "Pipeline esausta.",
      f"tool_res={len(tool_res)} errori={len(errori)}")
check("T9c storia salvata su disco nella root temporanea", k.db_path.exists() and k.db_path.stat().st_size > 0)

# ---------- T10: osservazione sicurezza — path traversal in write_file ----------
tmp_inner = tempfile.mkdtemp(prefix="gas_test_inner_")
os.environ["GAS_CWD"] = tmp_inner
k = GasKernel(root_dir=tmp_inner)
out = k.execute_tool_call("write_file", {"relative_path": "../gas_traversal_proof.txt", "content": "fuori"})
fuori = Path(tmp_inner).parent / "gas_traversal_proof.txt"
scappato = fuori.exists()
if scappato:
    fuori.unlink()
print(f"[NOTA] T10 path traversal write_file: escape riuscito={scappato} "
      f"-> {out[:60]} (finding aperto, vedi roadmap anti-autodistruzione)")

# ---------- riepilogo ----------
print(f"\n=== RIEPILOGO: {len(PASS)} PASS, {len(FAIL)} FAIL ===")
for f in FAIL:
    print(f"  FAIL: {f}")
sys.exit(1 if FAIL else 0)
