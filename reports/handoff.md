# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-29 — Chiusura riserve calcola(): tetto anti-DoS + test stringenti

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #77 (https://github.com/Gasss23/Gas/pull/77).
2. **Deploy VPS + test E2E live**: dopo il merge, portare il codice su S2 e validare il round-trip agentico: input "sette per otto" → modello chiama `calcola('7*8')` → risposta "56". Non eseguibile in dev (API key assenti).

---

## §1 SCOPE & ESITO FETTE

**1. Tetto anti-DoS in calcola()**: FATTA
- Tre strati: validazione AST (esponente letterale ≤ 1000, factorial arg letterale ≤ 1000), namespace eval ripulito (`pow` rimosso), check post-eval ≤ 500 cifre.
- `9**9**9` → RIFIUTATO in 0.000s (zero hang).

**2. Whitelist nodi AST esplicitata**: FATTA
- Blocco commento aggiunto sopra `_calcola_validate` con elenco verbatim degli `ast.*` ammessi.

**3. Test end-to-end LLM live**: SALTATA — API key assenti in dev (Gemini, Groq). Da eseguire su VPS S2. NON dichiarato passato.

**4. Fix T62f — rifiuto stringente (R-calcola-2)**: FATTA
- Condizione da `startswith("Rifiutato") or startswith("Errore")` a solo `startswith("Rifiutato")`.
- `pow(9, 387420489)` aggiunto a bad_inputs.

**5. Commit hash + conferma branch**: FATTA — commit `873220a`, branch `sonda/vps-stato-2026-08-26`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 gas.py                             | 155 +++++++++++++++++---
 gas_identity.md                    |  11 +-
 reports/diff_sessione.md           |  21 +--
 reports/handoff.md                 | 112 ++++++++++----
 reports/stato_progetto.md          |  40 ++++-
 reports/ultimo_report.md           | 292 ++++++++-----------------------------
 tests/test_unit_kernel.py          |  60 ++++++++
 8 files changed, 404 insertions(+), 289 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
873220a feat(kernel): calcola() tetto anti-DoS + fix T62f rifiuto stringente
6f42a2b chore(revisore): memoria review #94 — APPROVATO
d8cfb2a docs(fine-task): handoff Fetta A+B prompt hardening + calcola() 2026-08-29 — PR #77
62af5ee feat(kernel): prompt hardening (Fetta A) + tool calcola() ast-whitelist (Fetta B)
37b991d chore(revisore): memoria review #93 — APPROVATO CON RISERVE
17b96d0 docs(fine-task): handoff audit system-prompt 2026-08-29 — PR #77
7c4aec8 docs(audit): system prompt — 4 finding (CRITICO/ALTO×2/MEDIO), audit read-only
2575e0a docs(fine-task): handoff diagnosi bug kernel-rifiuta-7x8 — 2026-08-29
e0afbd1 docs(diagnosi): bug kernel-rifiuta-7x8 — causa radice isolata (system-prompt vs allowlist)
b0dde4c docs(fine-task): handoff + diff_sessione sonda VPS 2026-08-26 — PR #77
b7ab347 docs(sonda-vps): fotografia deploy GAS 2026-08-26 — VPS stabile, 391 commit dietro origin/main
cab1352 docs(sonda-vps): §0 handoff — PR #77 e istruzioni sblocco SSH
3cde16b docs(sonda-vps): report sonda VPS 2026-08-26 — task SALTATA (SSH non configurato)
```

NB: il commit di fine-task che contiene questo file non compare, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

**Commit `873220a` — feat(kernel): calcola() tetto anti-DoS + fix T62f rifiuto stringente**

**Verdetto review #94: APPROVATO**

Elementi verificati:
- Difese anti-DoS su tre strati indipendenti (AST/namespace/post-eval): strutturalmente solide.
- T62f condizione stringente (`startswith("Rifiutato")` solo): corretta.
- Wall of Shame §5 rispettato. Nessun guardrail indebolito.
- Suite: 299 PASS, 0 FAIL.

Riserva residua non bloccante: R-calcola-1 da #93 (math.factorial argomento borderline — coperta da `except Exception → stringa errore, zero crash`).

**Commit `62af5ee` — feat(kernel): prompt hardening (Fetta A) + tool calcola() ast-whitelist (Fetta B)**

**Verdetto review #93: APPROVATO CON RISERVE**

Elementi verificati:
- `eval` con `__builtins__={}` + namespace whitelist: sicuro contro tutti gli exploit noti.
- System prompt: chiude F1 CRITICO, F2+F3 ALTO, F4 MEDIO dell'audit.

Riserve (chiuse in questa sessione):
- R-calcola-1: chiusa con T62k + tetto factorial.
- R-calcola-2: chiusa con fix T62f in questa sessione.

---

## §5 DELTA TEST DEL MOTORE

**Prima sessione corrente:** 292 PASS, 0 FAIL (baseline post-sessione precedente)
**Dopo:** 299 PASS, 0 FAIL (+7 nuovi T62l-T62p + 1 T62f aggiornato)

```
=== RIEPILOGO: 299 PASS, 0 FAIL ===
```

Nuovi test: T62l (9**9**9 senza hang), T62m (esponente > MAX_EXP), T62n (factorial > MAX_FACTORIAL), T62o (2**1000 valido ≤ 500 cifre), T62p (factorial arg non letterale), + pow(9,387420489) in T62f.

---

## §6 STATO CI

```
completed	success	docs(fine-task): handoff Fetta A+B prompt hardening + calcola() 2026-…	CI	sonda/vps-stato-2026-08-26	push	33259588195	52s	2026-08-29T15:11:59Z
completed	failure	feat(kernel): prompt hardening (Fetta A) + tool calcola() ast-whiteli…	CI	sonda/vps-stato-2026-08-26	push	33257612901	45s	2026-08-29T14:26:32Z
completed	success	docs(fine-task): handoff audit system-prompt 2026-08-29 — PR #77	CI	sonda/vps-stato-2026-08-26	push	33256417734	1m14s	2026-08-29T14:00:00Z
```

Mappatura commit→run:
- `873220a` (commit motore anti-DoS) → run non ancora disponibile (push avviene dopo la scrittura di questo handoff).
- `6f42a2b` (memoria revisore #94) → nessuna run dedicata; incluso nell'albero testato dal push successivo.
- `d8cfb2a` (fine-task sessione precedente) → run `33259588195`: `unit-suite` ✓, `handoff-check` ✓.
- `62af5ee` (commit motore sessione precedente) → run `33257612901`: `unit-suite` ✓, `handoff-check` ✗ (§2 stale — corretto nel commit `d8cfb2a`).
- Commit `37b991d`..`3cde16b` → sessioni precedenti, già dichiarati nei rispettivi handoff.

---

## §7 RISERVE APERTE

Da questa sessione: nessuna (R-calcola-1 e R-calcola-2 chiuse).

Da sessioni precedenti (ancora aperte):
- R-client4a-1: eccezioni di rete non gestite in main() di probe_client_4a.py — non bloccante per uso-e-getta.
- **Rischio residuo deploy**: round-trip agentico con LLM reale non testato in dev — da validare su VPS S2.
