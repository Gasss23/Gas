# ULTIMO REPORT — 2026-10-02 — Fetta C3 cancello: coda approvazioni SQLite

## DECISIONI UMANE RICHIESTE

1. **Gate §4 (check_verdetto) e verdetto verbatim**: il verdetto integrale della review #125 cita path abbreviati (`store.py:421`, `store.py:5131`, `store.py:1469`) e `gas.py:1948` (fuori dal diff). `check_verdetto.py` li considera "non nel diff di sessione" → gate B rosso. Per istruzione operatore il testo del verdetto NON è stato ritoccato: report e handoff sono scritti ma NON committati né pushati. Decidere: (a) accettare un §4 che fallisce il check (gate bypass esplicito), (b) far ri-emettere il verdetto al revisore con path completi, (c) correggere prima check_verdetto (fetta "controlli automatici", cfr. F-verdetto-ritoccato).
2. **PR #109**: superata da #110 (vedi sotto). Merge/chiusura a discrezione dell'operatore.
3. **Mini-fetta R-c3-1** (riserva media, da chiudere PRIMA di C4): proposta, non eseguita.
4. **C4** (rimozione stub C2, turno di sblocco, bridge Telegram, limite read-back ~4096 char §4c): proposta, non eseguita.

## Esito per step

- **Step 0 — Sonda**: FATTA.
  - #108 e #110 su origin/main. #109 OPEN (commit `7b6a471`, `c5feceb` non antenati di origin/main). Su indicazione operatore: partenza da origin/main attuale.
  - Verifica #109 (`git diff origin/main origin/chore/fine-task-robusto -- .claude/commands/fine-task.md`): **#109 superata** — #110 sostituisce i gate inline con `scripts/fine_task_finale.sh`; mergiare #109 riporterebbe indietro main. Unico elemento di #109 non su main: il check "handoff rigenerato in questa sessione" (`git diff --stat ${BASE}..HEAD -- reports/handoff.md`) e il relativo cat condizionale.
  - Cosa chiede §C3 (`reports/design_cancello.md:351-356`): tabella `approvals` in `modules/memory/store.py` con schema §4a (righe 192-209); metodi `enqueue_approval`, `resolve_approval(id, stato, telegram_user_id)`, `get_pending_approvals`, `expire_stale_approvals`; **zero modifiche a gas.py**; test: INSERT+resolve, doppio resolve no-op, scadenza artificiale (ts_expiry = now-1) → expired, integrità hash. Richiami: §4b (UUID uuid4 monouso, SHA-256 args, ts_expiry = now + GAS_APPROVAL_TIMEOUT_SECS), §4d/§8c (30 min, scaduta mai eseguita, resta per audit), §4e (token monouso, integrità args, stato immutabile), §8d (firma per-azione, niente batch).
  - Stub C2: `gas.py:1947-1952` (ramo IRREVERSIBLE / UNCERTAIN+contaminata che esegue con log `[GATE-C2-STUB]`). Rimozione = C4 (`design_cancello.md:358-368`, §4b turno di sblocco via callback Telegram).
  - Conflitto spec/brief segnalato all'operatore → decisione: **C3 come da spec** (solo store.py, stub resta fino a C4).
- **Step 1 — Doc**: FATTA. In `reports/stato_progetto.md` §Finding aperti: F-verdetto-ritoccato, R-finale-1, nota handoff PR #109; più voce C3 con riserve R-c3-1..5.
- **Step 2 — Implementazione §C3**: FATTA (scope spec). `modules/memory/store.py`: tabella `approvals` + 4 trigger (nasce solo pending, no DELETE, stato immutabile fuori da pending, payload immutabile); `hash_args`, `enqueue_approval`, `get_approval` (read-back integrale + `hash_ok`, aggiunta rispetto alla spec), `resolve_approval`, `get_pending_approvals`, `expire_stale_approvals`. Fail-closed su ogni errore. Nessun tool di approvazione esposto al modello. Stub C2 invariato (decisione operatore).
- **Step 3 — Test reali**: FATTA. T73a-g (40 check, SQLite reale, nessun mock). Adattamento allo scope: "eseguita una volta sola" → "risolta una volta sola" (l'esecuzione è C4). Suite kernel: 423 PASS / 5 FAIL → 463 PASS / 5 FAIL (5 FAIL = F-mac-1). pytest gate+hooks+voice_server: 144 passed prima e dopo.
- **Step 4 — Revisore Opus**: FATTA. Review #125 APPROVATO CON RISERVE (R-c3-1 media, R-c3-2..4 minori, R-c3-5 cosmetica). Commit motore `4f16a65`, memoria revisore `aa0b0d0`.
- **Fine-task (commit report + push + PR)**: DEFERITA — gate B `check_verdetto.py` rosso sul §4 verbatim; per istruzione operatore il verdetto non si modifica → STOP.

## Anomalie

- Il verdetto #125 cita `store.py:5131` e se ne autocorregge in coda (→ `tests/test_unit_kernel.py:5131`): lasciato verbatim.
- I commit `aa0b0d0` e `4f16a65` sono solo locali (branch mai pushato).
