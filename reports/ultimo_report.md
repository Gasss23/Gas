# Report: Allineamento canonici — suite reale + sonda E2E lang-rule

**Data**: 2026-09-21  
**Branch**: `docs/reverifica-lang-rule`  
**Scope**: NESSUNA modifica al motore. Solo misure reali e aggiornamento canonici.

---

## PASSO 1 — Suite kernel reale (macOS 2026-09-21)

**Comando eseguito**:
```
cd /Users/gas/Gas && source .venv/bin/activate && python tests/test_unit_kernel.py
```

**Nota**: `test_unit_kernel.py` è uno script standalone (termina con `sys.exit()`), NON un file pytest standard — causa INTERNALERROR se lanciato con `pytest tests/`. Va eseguito con `python tests/test_unit_kernel.py`.

**Output riepilogo verbatim**:
```
[PASS] T63a _GAS_SYSTEM_PROMPT_BASE contiene regola lingua forte — cercato: "anche se l'utente scrive in un'altra lingua"
[PASS] T63b _build_system_prompt senza gas_identity.md contiene regola lingua
[PASS] T63c _build_system_prompt con gas_identity.md contiene regola lingua
[PASS] T63d gas_identity.md reale contiene regola lingua

=== RIEPILOGO: 294 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

**Pytest altri test** (test_unit_gasmerge, handoff_check, hooks, voice_server, voice_stt, voice_tts):
```
cd /Users/gas/Gas && source .venv/bin/activate && python -m pytest tests/ --ignore=tests/test_unit_kernel.py -q --tb=short
132 passed in 38.71s
```

**Totale macOS**: **294 PASS kernel + 132 PASS pytest = 426 PASS, 5 FAIL** (tutti bwrap macOS, F-mac-1 già documentato).

**Nota sulla precedente dichiarazione "299 PASS (2026-08-29)"**: era corretta per Linux/WSL (bwrap presente, tutti 299 test kernel passano). Su macOS: 294 PASS + 5 FAIL bwrap = 299 totali. T63a-d (lang-rule) aggiunti DOPO quell'ultima misura: ora 299 totali in kernel script (294 PASS macOS + 5 FAIL bwrap).

**Conclusione**: nessuna regressione rispetto a 2026-08-29. I 5 FAIL sono identici a F-mac-1. T63a/b/c/d tutti PASS ✅.

---

## PASSO 2 — Sonda E2E reale (lingua italiana)

**Setup**: history temporanea isolata via `tmpdir`, nessuna scrittura su `.gas_history.json` del repo.

**Input (in inglese)**:
```
Hello, what is 7 times 8 and who are you?
```

**Cascade status**:
- `gemini-flash-lite` → **429 QUOTA** (free tier 20 req/day esaurita — quota giornaliera, non recuperabile oggi)
- `gemini-flash` → **429 QUOTA** (stesso motivo)
- `groq/openai/gpt-oss-120b` → **✅ RISPOSTA**

**Rung che ha risposto**: **Groq** (`openai/gpt-oss-120b`)

**Risposta VERBATIM**:
```
Il risultato è **56**.

Io sono **Gas**, il tuo agente AI autonomo e personale, progettato per operare 24/7 su VPS come partner strategico per il business, focalizzato su autonomia, interfaccia vocale e marketing.
```

**Valutazione**: risposta in italiano dal primo messaggio su input inglese ✅. La regola `"RISPONDI SEMPRE IN ITALIANO, anche se l'utente scrive in un'altra lingua"` funziona correttamente su Groq.

**Secondo rung**: OPENROUTER_API_KEY non configurata su questa macchina; Ollama non configurato (GAS_OLLAMA_URL assente). Solo Groq testabile oggi. Gemini tornerà disponibile domani (quota giornaliera free tier).

---

## PASSO 3 — Branch `docs/reverifica-lang-rule`

**Status**: branch remoto non mergiato. Sono attualmente su questo branch.

**Contenuto diff vs main** (`git diff main..HEAD --stat`):
```
reports/diff_sessione.md  | 28 lines
reports/handoff.md        | 79 lines  
reports/stato_progetto.md |  2 lines
reports/ultimo_report.md  | 88 lines
4 files changed, 111 insertions(+), 86 deletions(-)
```

**Analisi**: tutti e 4 i file sono doc/report della sessione di re-verifica precedente (2026-09-21 mattina). Nessun codice motore, nessun file di test. Il contenuto è:
- `stato_progetto.md`: aggiornamento header data (1 riga)
- `ultimo_report.md`: report re-verifica precedente (ora sovrascritto da questo report)
- `handoff.md` + `diff_sessione.md`: dossier della sessione precedente

**Valutazione**: il branch contiene solo documenti di sessione, nessun contenuto tecnico non recuperabile. **Da scartare** (merge o chiusura), decisione all'operatore.

---

## Aggiornamenti canonici applicati

- `reports/stato_progetto.md`: aggiornato con numeri reali suite macOS + esito sonda E2E
- `reports/ultimo_report.md`: questo report

**Nessuna modifica al motore** (gas.py, gas_identity.md, brains/, modules/, tests/ NON toccati).
