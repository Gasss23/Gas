# Report: fix/t9a-deterministico — 2026-07-24

## SCOPE

Branch: `fix/t9a-deterministico` da `origin/main` (`55959ef`).  
Sessione: sanare il venv, rendere T9a/T9c deterministici, allineare i canonici.

---

## FETTA 0 — SANARE IL VENV (nessun commit)

- **Python del venv WSL**: 3.12.3
- **Dipendenze installate**: `pip install -r requirements.txt -r requirements-dev.txt`
  - openai 2.43.0 · fastembed 0.8.0 · numpy 2.4.6 · onnxruntime 1.27.0 · requests 2.34.2 · pytest 9.1.1
- **Suite kernel PRIMA (pre-fix)**:
  ```
  === RIEPILOGO: 248 PASS, 0 FAIL ===
  [SKIP] T9a ogni provider cappato a 10 iterazioni — richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI
  [SKIP] T9c storia salvata su disco nella root temporanea — richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI
  ```
- Primo run: scaricamento modello fastembed (~90MB in ~/.cache); i run successivi sono immediati.

---

## FETTA 1 — T9a/T9c DETERMINISTICI

### Modifiche

**`tests/test_unit_kernel.py`** (blocco T9, righe ~132-163):
- Iniettate `GEMINI_API_KEY="fake-gemini-key-for-test"` e `GROQ_API_KEY="fake-groq-key-for-test"` nel blocco try/finally con pattern save/restore identico a quello già presente per `OPENROUTER_API_KEY` e `GAS_OLLAMA_URL`.
- Rimosso gate `_has_live_keys` (definizione riga 147 + 2 branch if/else a righe 148 e 158).
- T9a e T9c ora sono `check(...)` incondizionali.

**`.github/workflows/ci.yml`** (SOLO commenti, zero modifiche agli step):
- Riga `python-version: "3.11"`: commento corretto da `# combacia col venv del progetto (3.11.9)` a `# DIVERGENZA DICHIARATA: CI usa 3.11, venv WSL è 3.12.3 (misurato 2026-07-24)`.
- Job Summary: riga `T9a/T9c sono SKIP in CI...` aggiornata a `T9a/T9c girano sempre con chiavi fittizie e client OpenAI finto (zero rete, zero token)`.
- Step "Gate — sandbox OS attivo": commento allineato (rimozione riferimento a "T9a/T9c SKIP in CI assenza API key").

### Prove obbligatorie

**(a) Suite DOPO il fix:**
```
[PASS] T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {'gemini-2.5-flash-lite': 10, 'gemini-2.5-flash': 10, 'openai/gpt-oss-120b': 10}
[PASS] T9b loop infinito assorbito senza crash, pipeline esausta dichiarata — tool_res=30 errori=1
[PASS] T9c storia salvata su disco nella root temporanea
=== RIEPILOGO: 250 PASS, 0 FAIL ===
(0 SKIP residui)
```

**(b) Prova zero-rete (ispezione gas.py):**
- Ogni rung della cascata in `run_turn` (gas.py:1503) passa da `client = OpenAI(base_url=url, api_key=os.environ.get(env))`.
- Il test sostituisce `gas.OpenAI = FakeOpenAI` → intercetta TUTTE le istanziazioni client.
- `_probe_free_model` / `urllib` (gas.py:159-167) sono chiamati SOLO da `doctor()` (gas.py:1629), NON raggiungibili da `run_turn`.
- Risultato: il ciclo agentico di T9 gira interamente in-process, zero connessioni di rete.

**(c) Prova one-off zero-rete (socket.socket bloccato nello stesso processo, NON committata):**
```
# Patch socket.socket nel processo prima di exec tests/test_unit_kernel.py
[PASS] T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {'gemini-2.5-flash-lite': 10, 'gemini-2.5-flash': 10, 'openai/gpt-oss-120b': 10}
[PASS] T9b loop infinito assorbito senza crash, pipeline esausta dichiarata — tool_res=30 errori=1
[PASS] T9c storia salvata su disco nella root temporanea
=== RIEPILOGO: 250 PASS, 0 FAIL ===
EXIT CODE: 0
```
I warning "402 Payment Required" nei T34 (doctor) sono attesi: doctor usa urllib con chiavi fittizie, non fa parte di T9.

### Revisore

**Revisore #59 (2026-07-24) — VERDETTO INTEGRALE VERBATIM:**

> **VERDETTO FINALE: APPROVATO**
>
> Il commit può procedere. File aggiornato: `/home/gqual/Gas/.claude/agents/memoria_revisore.md` (riga `#59` aggiunta in coda).

### Commit fetta 1

`f6b6caa` — `test(T9a/T9c): rendi deterministici iniettando chiavi fittizie Gemini/Groq`

---

## FETTA 2 — CANONICI (reports/stato_progetto.md)

Tutte le modifiche basate su dati live, misurati in questa sessione:

1. **Contatore review**: aggiornato da #57 a #59 (numero più alto in `memoria_revisore.md`, tail verificato live). #58 = PR #41 R-ci-summary, APPROVATO. #59 = questo commit.
2. **R-ci-summary**: ✅ CHIUSO. Evidenza: ispezione `.github/workflows/ci.yml` su `origin/main` (`55959ef`) — step "Run hook suite" con `pipefail` + `tee hooks_output.txt`, Job Summary legge `hooks_output.txt`. PR #41, merge `55959ef`, CI `30051234981` ✅ SUCCESS.
3. **R-ci-openrouter**: riscritto con storia degli errori (NON cancellata) + diagnosi reale (gate `_has_live_keys` rendeva T9a/T9c sempre SKIP + T9b verde a vuoto). ✅ CHIUSO (fetta 1 commit `f6b6caa`).
4. **Nuovo finding T9b**: registrato come ℹ️ lezione: test verde a vuoto (cascata a 0 rung) non dimostra ciò che dichiara. Con chiavi fittizie T9b è ora test reale (30 tool_res).
5. **PR #40 e #41**: aggiunti alla riga CI — PR #41 merge `55959ef` CI `30051234981`; PR #40 merge `4391c8b` CI `29967190300`. Hash e run ID da `git log origin/main` e `gh run list`, verbatim.
6. **Head su origin**: 5 (live `git ls-remote --heads origin | wc -l`, pre-push; dopo push fix/t9a-deterministico = 6). Valore concordante con bonifica 2026-07-22.
7. **§7 venv WSL**: aggiornato. Dipendenze installate 2026-07-24. Suite eseguibile. Divergenza Python 3.12.3 vs 3.11 CI registrata come ℹ️ nota aperta (non sanata, solo dichiarata).
8. **Contraddizione**: "Suite WSL locale 2026-07-19: 247 PASS" era FALSA (venv aveva solo pytest, suite non eseguibile). Dichiarato come errore nel file.
9. **Azioni senza traccia in git**: `pip install -r requirements.txt -r requirements-dev.txt` nel venv WSL (2026-07-24), registrato nella sezione sessione.

---

## ESITO COMPLESSIVO

- Fetta 0: ✅ FATTA (venv sanato, nessun commit)
- Fetta 1: ✅ FATTA (commit `f6b6caa`, revisore #59 APPROVATO)
- Fetta 2: ✅ FATTA (questo commit)
- PR: aperta su `fix/t9a-deterministico`
- Merge: azione umana con `gasmerge`, fuori da questa sessione
