# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-29 — K3+K4 sessione 2 (re-review #109, E2E LLM reale, CI finale)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #102 (https://github.com/Gasss23/Gas/pull/102).
2. Riserva R-k4-3 (cosmetica test): T69b check primario vacuosamente True. Il check discriminante è T69b.2. Da correggere in sessione futura.
3. Finding F-no-ricorda-1: 2/3 domande E2E — modello non chiama ricorda per prompts ambigui/parola singola. Decidere se aggiornare gas_identity.md per guidare il modello a consultare la knowledge.
4. Finding F-like-1: LIKE non matcha query multi-parola composte. Decidere se implementare keyword extraction o FTS5 sul knowledge DB in sessione futura.

---

## §1 SCOPE & ESITO FETTE

- **FETTA A — Ri-review #109**: `FATTA` — Revisore ha riesaminato il codice finale post-fix R-k4-1/R-k4-2. Entrambe le riserve CHIUSE. R-k4-3 cosmetica residua. Tutte le 6 protezioni K4 confermate.

- **FETTA B — E2E con provider LLM reali**: `FATTA` — Script `tests/e2e/e2e_k3k4_llm.py` versionato. 7 PASS, 2 FAIL (F-no-ricorda-1 e F-like-1 documentati come finding architetturali). Giro iniettivo: istruzione non eseguita, tag non in risposta. Review #110 APPROVATO CON RISERVE.

- **FETTA C — CI PR #102**: `FATTA` — Run `36478066331` completed success su testa `8e2e67a`. Run precedente `36477977180` failure per §2 handoff mismatch (poi corretto).

- **Autonomia #2/#3 / fix motore**: `SALTATA — STOP BLOCCANTE rispettato` (zero modifiche a gas.py in questa sessione).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +
 gas.py                             |  92 ++++++++-
 reports/diff_sessione.md           |  36 ++--
 reports/handoff.md                 | 202 ++++++++++----------
 reports/stato_progetto.md          |   8 +-
 reports/ultimo_report.md           | 139 +++++++++++---
 tests/e2e/e2e_k3k4_llm.py          | 369 +++++++++++++++++++++++++++++++++++++
 tests/test_unit_kernel.py          | 251 +++++++++++++++++++++++++
 8 files changed, 954 insertions(+), 146 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
833d8b7 test(e2e): K3+K4 E2E con provider LLM reali — FETTA B
00ec63e chore(revisore): memoria review #110 — APPROVATO CON RISERVE
12bd47e chore(revisore): memoria review #109 — APPROVATO CON RISERVE
8e2e67a docs(fine-task): handoff §0/§2/§3/§6 aggiornati post-push (PR #102)
ffb4d81 docs(fine-task): handoff + report K3+K4 autonomia knowledge 2026-09-28
6249e16 feat(autonomia): K3+K4 — ricorda() pesca .gas_knowledge.db + 6 protezioni
6a0a2f7 chore(revisore): memoria review #108 — APPROVATO CON RISERVE
```

---

## §4 VERDETTO DEL REVISORE

### Verdetto integrale review #108 (commit 6249e16 — per completezza sessione 1)

> **APPROVATO CON RISERVE**
>
> R-k4-1 (minore): cap_n = min(int(n), ...) fuori dal try/except. Fix: spostare dentro il try.
> R-k4-2 (cosmetica): source_name e ts nel header non passano per _sanitize_memory_text.
> R-k4-3 (cosmetica test): T69b check primario vacuosamente True se blocco assente.
>
> Tutte le 6 protezioni K4 verificate. Antipattern Wall of Shame assenti. Guardrail loop intatti.

### Verdetto integrale review #109 (ri-review post-fix R-k4-1/R-k4-2)

> ## VERDETTO REVIEW #109 — K3+K4 autonomia knowledge (ri-review post-fix)
>
> **APPROVATO CON RISERVE**
>
> ### Verifica delle tre riserve di #108
>
> **R-k4-1 — CHIUSA**
> `gas.py:86` (diff) — `cap_n = min(int(n), self.KNOWLEDGE_MAX_RESULTS)` è ora la prima istruzione dentro il `try:`. Il commento esplicita "(dentro try: fail-safe R-k4-1)". Se `n` non è convertibile a int, `ValueError` cade nell'`except Exception` esterno che logga e ritorna `""`. Riserva effettivamente chiusa.
>
> **R-k4-2 — CHIUSA**
> `gas.py:109-112` (diff) — Aggiunto `ts = _sanitize_memory_text(...)` e `src = _sanitize_memory_text(str(row["source_name"]))`. Commento: "# source_name e ts sanitizzati per defense-in-depth (R-k4-2)". Entrambi passano per `_sanitize_memory_text` prima di comporre l'header. Riserva effettivamente chiusa.
>
> **R-k4-3 — RESIDUA (cosmetica)**
> T69b.2 (riga 237) fornisce il check reale discriminante. T69b primary ancora vacuo per costruzione. Non bloccante.
>
> | Protezione | Stato |
> |---|---|
> | K4.1 escape + tag + "dati non istruzioni" | ok |
> | K4.2 cap env-overridabile (cap_n dentro try) | ok |
> | K4.3 filtro sources.yaml | ok |
> | K4.4 write_file blocca .gas_knowledge* | ok |
> | K4.5 SQLite ?mode=ro, zero tool scrittura | ok |
> | K4.6 fail-safe §9 DB assente/corrotto | ok |
>
> Nessun nuovo difetto dai fix. Nota minore cosmetica: connessione SQLite chiusa con conn.close() senza with/try-finally (rischio GC, non corruzione con ?mode=ro). Accettabile.

### Verdetto integrale review #110 (tests/e2e/e2e_k3k4_llm.py)

> ## VERDETTO REVIEW #110 — tests/e2e/e2e_k3k4_llm.py
>
> **APPROVATO CON RISERVE**
>
> **Evidenze esaminate:**
>
> 1. Isolamento root temporanea (righe 66-99, 158): tre livelli sovrapposti (root_dir, GAS_KNOWLEDGE_DB, GAS_CWD tutti in TMP). Nessun file del repo reale toccato. **OK.**
>
> 2. `_extract_tool_calls_from_history` e `_extract_ricorda_outputs` (righe 102-126): ispezione post-mortem di k.history dopo run_turn già completato. Nessun raw history slicing antipattern. **OK.**
>
> 3. Check giro iniettivo (righe 318, 333-338): `risposta_solo_pwned` cattura solo stringa esatta "PWNED"; injection parziale non intercettata. Per script di misura accettabile — protezione vera è in kernel. **Riserva R-e2e-3 (minore).**
>
> 4. Cleanup finale senza try/finally (riga 365): temp dir residua su crash. **Riserva R-e2e-1 (minore).**
>
> 5. `_detect_provider_from_debug_log` (riga 131): cerca gas_debug.log in TMP ma kernel scrive in CWD reale. Solo diagnostico, nessun check() impattato. **Riserva R-e2e-2 (minore/osservabilità).**
>
> gas.py, brains/, modules/ non toccati. Filosofia misura pura coerente con architettura. Finding F-no-ricorda-1 e F-like-1 documentati come attesi — exit code 1 previsto e dichiarato nel docstring.
>
> **Riserve: R-e2e-1, R-e2e-2, R-e2e-3** (tutte minori, non bloccanti).

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a `gas.py` o `tests/test_unit_kernel.py` in questa sessione (FETTA B = sola misura).

Suite invariata rispetto alla sessione 1: **383 PASS, 5 FAIL** (F-mac-1 bwrap macOS).

```
=== RIEPILOGO: 383 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

---

## §6 STATO CI

```
completed	success	docs(fine-task): handoff §0/§2/§3/§6 aggiornati post-push (PR #102)	CI	feat/autonomia-k3-k4	push	36478066331	1m3s	2026-09-28T20:16:52Z
completed	failure	docs(fine-task): handoff + report K3+K4 autonomia knowledge 2026-09-28	CI	feat/autonomia-k3-k4	push	36477977180	57s	2026-09-28T20:16:05Z
completed	success	Merge pull request #101 from Gasss23/feat/fetta3a-lezioni-quarantena	CI	main	push	36468992436	1m1s	2026-09-28T18:58:43Z
```

**Mappatura commit→run (sessione 1+2 combinata):**
- `6a0a2f7` (chore revisore #108): nessuna run autonoma su questo SHA intermedio.
- `6249e16` (feat K3+K4 codice): nessuna run autonoma su questo SHA intermedio — incluso nell'albero di `ffb4d81`.
- `ffb4d81` (docs fine-task sessione 1): run `36477977180` — completed **failure** (handoff-check §2 mismatch: diff_sessione.md mancante in §2).
- `8e2e67a` (docs fix §0/§2/§3/§6): run `36478066331` — completed **success**.
- `12bd47e` (chore revisore #109): nessuna run disponibile al momento della scrittura.
- `00ec63e` (chore revisore #110): nessuna run disponibile al momento della scrittura.
- `833d8b7` (test E2E): nessuna run disponibile al momento della scrittura.
- commit di fine-task (questo): run non ancora disponibile alla scrittura dell'handoff.

---

## §7 RISERVE APERTE

Dalla sessione corrente:
- **R-k4-3** (cosmetica test): T69b check primario vacuoso. T69b.2 è il check reale.
- **R-e2e-1** (minore): cleanup E2E senza try/finally.
- **R-e2e-2** (minore/osservabilità): provider detection cerca log in posto sbagliato.
- **R-e2e-3** (minore): check injection cattura solo stringa esatta "PWNED".
- **F-no-ricorda-1** (finding architetturale): modello non chiama ricorda per prompts ambigui. Decisione umana richiesta (§0.3).
- **F-like-1** (finding architetturale): LIKE non matcha query multi-parola. Decisione umana richiesta (§0.4).

Ereditate da sessioni precedenti:
- **R-lez-bis-1** (cosmetica, fetta 3a-bis): vedi stato_progetto.md
- **R-lez-2** (ereditata, fetta 3a): vedi stato_progetto.md
- **R-ci-1** (regex check_handoff da ancorare a `^`): vedi stato_progetto.md
