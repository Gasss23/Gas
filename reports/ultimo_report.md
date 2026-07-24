# Report: fix/t9a-deterministico — 2026-07-24

## Esito per fetta

| Fetta | Esito | Note |
|---|---|---|
| 0 — Sanare venv | FATTA | Nessun commit |
| 1 — T9a/T9c deterministici | FATTA | Commit `f6b6caa`, revisore #59 APPROVATO |
| 2 — Canonici stato_progetto.md | FATTA | Commit `0034a17` |

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

---

## FETTA 1 — T9a/T9c DETERMINISTICI

### Modifiche

**`tests/test_unit_kernel.py`** (blocco T9):
- Iniettate `GEMINI_API_KEY="fake-gemini-key-for-test"` e `GROQ_API_KEY="fake-groq-key-for-test"` nel blocco try/finally con pattern save/restore identico a quello già presente per `OPENROUTER_API_KEY` e `GAS_OLLAMA_URL`.
- Rimosso gate `_has_live_keys` (era inutilizzato dopo la rimozione dei 2 branch if/else).
- T9a e T9c ora sono `check(...)` incondizionali.

**`.github/workflows/ci.yml`** (SOLO commenti, zero modifiche agli step):
- `python-version: "3.11"`: commento corretto (divergenza 3.11 CI vs 3.12.3 WSL dichiarata).
- Job Summary: riga T9a/T9c aggiornata.
- Step "Gate — sandbox OS attivo": commento allineato.

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
- Ogni rung in `run_turn` (gas.py:1503): `client = OpenAI(base_url=url, api_key=os.environ.get(env))` — intercettato da `gas.OpenAI = FakeOpenAI`.
- `_probe_free_model` / `urllib` (gas.py:159-167): chiamati SOLO da `doctor()` (gas.py:1629), NON raggiungibili da `run_turn`.

**(c) Prova one-off zero-rete (socket.socket bloccato nello stesso processo, NON committata):**
```
[PASS] T9a ogni provider cappato a 10 iterazioni — chiamate per modello: {'gemini-2.5-flash-lite': 10, 'gemini-2.5-flash': 10, 'openai/gpt-oss-120b': 10}
[PASS] T9b loop infinito assorbito senza crash, pipeline esausta dichiarata — tool_res=30 errori=1
[PASS] T9c storia salvata su disco nella root temporanea
=== RIEPILOGO: 250 PASS, 0 FAIL ===
EXIT CODE: 0
```

### Revisore

**Revisore #59 (2026-07-24) — VERDETTO INTEGRALE VERBATIM:**

> **VERDETTO FINALE: APPROVATO**
>
> Il commit può procedere. File aggiornato: `/home/gqual/Gas/.claude/agents/memoria_revisore.md` (riga `#59` aggiunta in coda).

---

## FETTA 2 — CANONICI (reports/stato_progetto.md)

1. Review counter: #57 → #59 (#58=PR#41 R-ci-summary, #59=T9a/T9c).
2. R-ci-summary: ✅ CHIUSO (PR #41, merge `55959ef`, CI `30051234981`).
3. R-ci-openrouter: ✅ CHIUSO con storia errori conservata. Difetto reale: gate `_has_live_keys` → T9a/T9c sempre SKIP in CI → cap loop mai coperto da CI.
4. Nuovo ℹ️ lezione T9b: test verde a vuoto (0 rung) non dimostra ciò che dichiara.
5. CI: aggiunti PR #40 (`4391c8b`, CI `29967190300`) e PR #41 (`55959ef`, CI `30051234981`).
6. Head origin: 5 live pre-push.
7. §7 venv WSL: aggiornato (dipendenze 2026-07-24, Python 3.12.3 vs 3.11 CI ℹ️ aperta).
8. Errore dichiarato: "247 PASS WSL 2026-07-19" era falso.
9. Azioni senza traccia git: pip install registrato.

---

## CI

Branch fix/t9a-deterministico: run `30054898882` — ✅ SUCCESS (2026-07-24T00:00:35Z)
PR #42: https://github.com/Gasss23/Gas/pull/42
