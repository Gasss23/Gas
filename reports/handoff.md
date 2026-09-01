# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-01 — Chiusura finding F1 CRITICO (calcola() vs run_command)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #81 (https://github.com/Gasss23/Gas/pull/81) — doc-only, nessun motore toccato.
2. Valutare deploy VPS — FASE 3 completa non deployata; VPS stantio a commit `f3a8acc` (2026-06-29), 391 commit dietro origin/main.
3. Prima del deploy VPS: rotare chiave ElevenLabs (ATTESTATO SUP. 2026-08-22, ancora aperto).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 0 — Baseline E2E**: `FATTA` — Sonda su Gemini (gemini-flash, flash-lite 429) e Groq: 4 PASS su 4. Tool=`calcola()`, args corretti, output attesi (56 e 12.0).
- **Fetta 1 — Fix chirurgico**: `SALTATA — fix già in place` — `gas.py:49-50` ha già la direttiva corretta (`calcola()` per aritmetica) dal commit `62af5ee` (review #93, 2026-08-29). `git diff main HEAD -- gas.py` = vuoto. Il finding citava righe 46-48 di una versione precedente.
- **Fetta 2 — Revisore**: `FATTA` — Review #95 APPROVATO. Verdetto integrale in §4.
- **Fetta 3 — Suite completa**: `FATTA` — 299 PASS, 0 FAIL. Stop gate rispettato.
- **Fetta 4 — Confronto prima/dopo**: `FATTA` — Tabella in `reports/ultimo_report.md`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 reports/diff_sessione.md           |  37 +++++++----
 reports/handoff.md                 |  79 ++++++++++++++---------
 reports/stato_progetto.md          |   8 +--
 reports/ultimo_report.md           | 125 +++++++++++++++----------------------
 5 files changed, 128 insertions(+), 122 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
a3b87f4 docs(fine-task): chiusura finding F1 CRITICO — calcola() certificata 2026-09-01
fc211db chore(revisore): memoria review #95 — APPROVATO
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun commit motore (gas.py/brains/modules/tests/ non toccati in questa sessione). Il revisore è stato invocato in modalità ATTESTATIVA per certificare lo stato corrente.

**Review #95 — APPROVATO** (attestativa, nessun diff di codice):

> Commit `fc211db` confermato.
>
> **VERDETTO FINALE — Review #95: APPROVATO**
>
> **(a) `_GAS_SYSTEM_PROMPT_BASE` — direttiva calcoli**
> `gas.py:49-50` — ordina esplicitamente `calcola()` per calcoli aritmetici ("Per CALCOLI ARITMETICI usa SEMPRE calcola()"), con esempi `calcola('7*8')` e `calcola('math.sqrt(144)')`. La vecchia direttiva errata che ordinava `run_command` per "conteggi, misure e calcoli esatti" (F1 CRITICO, riga originale 46-48) **non è più presente**. `gas.py:51` delimita run_command a "CONTEGGI E MISURE SU FILE", scope corretto e separato. Nessun'altra riga del prompt risulta anomala: la lista tool a riga 42-44 è completa (7 tool), il contratto anti-simulazione a riga 44-46 è integro.
>
> **(b) `SHELL_ALLOWLIST` — assenza calcolatori**
> `gas.py:992-996` — `SHELL_ALLOWLIST = frozenset({"ls", "cat", "head", "tail", "wc", "grep", "echo", "pwd", "date", "stat", "file", "uniq", "cut", "tr", "nl", "diff", "comm", "true", "false", "basename", "dirname", "printf", "seq", "rev"})`. Nessun calcolatore presente: `bc`, `python`, `expr`, `awk`, `perl` sono assenti. **Nessuna violazione di sicurezza**.
>
> **(c) Guardrail di sicurezza — nessun indebolimento**
> `SHELL_ENV_SENSITIVE_MARKERS` (riga 1001) intatto. Sandbox bwrap (riga 1013+) intatto. Costanti anti-DoS di `calcola()` (`_CALCOLA_MAX_EXP`, `_CALCOLA_MAX_DIGITS`, `_CALCOLA_MAX_FACTORIAL`, righe 70-72) intatte. Schema tool (`tools_schema`, righe 508-514) coerente con system prompt e implementazione.
>
> **Rischio esplicitamente escluso**: comportamento dei provider alternativi (Groq, OpenRouter, Ollama) quando ricevono il system prompt aggiornato in turno reale — non verificabile in questa sessione senza chiavi API attive su quei rung. Il CAVEAT (ii) di stato_progetto.md (comportamento Groq contraddittorio) resta finding aperto distinto.
>
> File rilevanti verificati:
> - `/home/gqual/Gas/gas.py` (righe 40-60 e 992-996)
> - `/home/gqual/Gas/reports/stato_progetto.md`
> - `/home/gqual/Gas/.claude/agents/memoria_revisore.md`

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a `gas.py` o `tests/` in questa sessione.

Suite precedente: 299 PASS, 0 FAIL.  
Suite questa sessione: 299 PASS, 0 FAIL.  
Delta: 0.

---

## §6 STATO CI

```
completed  failure  docs(fine-task): chiusura finding F1 CRITICO — calcola() certificata …  CI  fix/chiusura-f1-calcola-2026-09-01  push  33543803998  1m7s  2026-09-01T18:28:18Z
completed  success  Merge pull request #80 from Gasss23/sonda/e2e-calcola-gemini-2026-09-01  CI  main  push  33541870284  1m1s  2026-09-01T18:08:22Z
completed  success  docs(fine-task): aggiorna §0 handoff con PR #80 reale (gate bash)  CI  sonda/e2e-calcola-gemini-2026-09-01  push  33540427549  48s  2026-09-01T17:53:36Z
```

Mappatura commit→run:
- `fc211db` (chore revisore): nessuna run CI su questo SHA — commit pushato isolato non triggera run separata; testato nell'albero di `a3b87f4`.
- `a3b87f4` (docs fine-task, primo push): run `33543803998` — **FAILURE** sul job `handoff-check` (placeholder `PLACEHOLDER_DIFF_STAT` nel blocco §2). Fix applicato in commit successivo.

**Nota**: il commit corrente (fine-task con blocchi git reali) non ha ancora run CI al momento della scrittura — "run non ancora disponibile alla scrittura dell'handoff".

---

## §7 RISERVE APERTE

Riserve emerse da questa sessione:
- **R-quota-gemini-lite**: gemini-2.5-flash-lite ha esaurito la quota gratuita giornaliera (20 RPD) durante la sonda. Il paracadute (fallback su gemini-flash) ha funzionato correttamente. Non bloccante ma da monitorare.
- **R-groq-openrouter-ollama**: comportamento dei provider alternativi (OpenRouter, Ollama) con il nuovo system prompt non verificato in questa sessione (assenza chiavi). Dichiarato come rischio dal revisore #95.

Riserve precedenti rimaste aperte (non toccate in questa sessione):
- R-finegat-1, R-finegat-2 (review #92)
- R-client4a-1 (review #91)
- R-tts-1 (review #89)
- Rotazione chiave ElevenLabs pre-VPS
