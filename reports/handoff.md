# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-29 — Audit system prompt: direttive contraddittorie e ambigue

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #77 (https://github.com/Gasss23/Gas/pull/77).
2. Scegliere quale fix applicare al system prompt (per ogni finding):
   - **F1 CRITICO** `gas.py:46-48`: sostituire "calcoli esatti" con scope reale (solo conteggi file/righe/parole) [opzione a — zero rischio], oppure aggiungere `bc` all'allowlist [opzione b], oppure invariato [accetta il rischio].
   - **F2/F3 ALTO** `gas_identity.md:3` + `gas.py:42`: aggiornare le liste tool con i 6 tool reali, oppure invariato.
   - **F4 MEDIO** `gas.py:42-44`: generalizzare il workaround "dichiara l'incertezza" a policy globale di fallback, oppure invariato.

---

## §1 SCOPE & ESITO FETTE

**Fetta 1 — Verifica registrazione subagent "revisore"**: `FATTA` — `.claude/agents/revisore.md` presente.

**Fetta 2 — Estrazione verbatim system prompt**: `FATTA` — `_GAS_SYSTEM_PROMPT_BASE` (`gas.py:38-60`), `_build_system_prompt` (`gas.py:62-68`), `gas_identity.md`.

**Fetta 3 — Audit direttive vs realtà del motore**: `FATTA` — 6 finding classificati (1 CRITICO, 2 ALTO, 1 MEDIO, 2 MINORI). Dettaglio integrale in `reports/ultimo_report.md`.

**Fetta 4 — Aggiornamento reports/**: `FATTA` — `ultimo_report.md` e `stato_progetto.md` aggiornati e committati (`7c4aec8`).

**Fetta 5 — Nessuna modifica al motore**: `RISPETTATO` — zero commit su `gas.py`, `brains/`, `modules/`, `tests/`. Stop gate bloccante osservato.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  |  22 ++--
 reports/handoff.md        |  59 ++++-----
 reports/stato_progetto.md |  40 +++++-
 reports/ultimo_report.md  | 312 +++++++++++++++++-----------------------------
 4 files changed, 190 insertions(+), 243 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
7c4aec8 docs(audit): system prompt — 4 finding (CRITICO/ALTO×2/MEDIO), audit read-only
2575e0a docs(fine-task): handoff diagnosi bug kernel-rifiuta-7x8 — 2026-08-29
e0afbd1 docs(diagnosi): bug kernel-rifiuta-7x8 — causa radice isolata (system-prompt vs allowlist)
b0dde4c docs(fine-task): handoff + diff_sessione sonda VPS 2026-08-26 — PR #77
b7ab347 docs(sonda-vps): fotografia deploy GAS 2026-08-26 — VPS stabile, 391 commit dietro origin/main
cab1352 docs(sonda-vps): §0 handoff — PR #77 e istruzioni sblocco SSH
3cde16b docs(sonda-vps): report sonda VPS 2026-08-26 — task SALTATA (SSH non configurato)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore in questa sessione (audit read-only, nessuna modifica a `gas.py`, `brains/`, `modules/`, `tests/`). Revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a `gas.py`/`tests/` in questa sessione. Nessun delta test.

---

## §6 STATO CI

```
completed	success	docs(audit): system prompt — 4 finding (CRITICO/ALTO×2/MEDIO), audit …	CI	sonda/vps-stato-2026-08-26	push	33256290842	59s	2026-08-29T13:56:36Z
completed	success	docs(fine-task): handoff diagnosi bug kernel-rifiuta-7x8 — 2026-08-29	CI	sonda/vps-stato-2026-08-26	push	33255256347	53s	2026-08-29T13:32:01Z
completed	success	docs(diagnosi): bug kernel-rifiuta-7x8 — causa radice isolata (system…	CI	sonda/vps-stato-2026-08-26	push	33255140643	54s	2026-08-29T13:29:25Z
```

Mappatura commit→run:
- `7c4aec8` → run `33256290842` ✅ SUCCESS (push che contiene questo commit come HEAD)
- `2575e0a` → run `33255256347` ✅ SUCCESS
- `e0afbd1` → run `33255140643` ✅ SUCCESS
- `b0dde4c`, `b7ab347`, `cab1352`, `3cde16b` → commit di sessioni precedenti, run precedenti non elencate (sessione chiusa).

Il commit di fine-task corrente non ha ancora run CI al momento della scrittura dell'handoff (run non ancora disponibile alla scrittura dell'handoff).

---

## §7 RISERVE APERTE

Da sessioni precedenti (invariate):
- R-client4a-1: eccezioni di rete non gestite in `main()` di `probe_client_4a.py` (non bloccante per client usa-e-getta).
- R-tts-1: cap testo implicito in `modules/voice/tts.py`.

Finding nuovi da questo audit (riserve aperte, fix richiede scope operatore):
- F1 CRITICO `gas.py:46-48`: direttiva "calcoli esatti" impossibile con SHELL_ALLOWLIST attuale — nessun calcolatore disponibile.
- F2 ALTO `gas_identity.md:3`: lista tool incompleta nell'identità runtime (3 di 6).
- F3 ALTO `gas.py:42`: lista tool incompleta nelle REGOLE TASSATIVE.
- F4 MEDIO `gas.py:42-44`: conflitto "non bloccarti" vs "non simulare" senza policy globale di fallback per tool failure.
