# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-29 — Fetta A prompt hardening + Fetta B tool calcola()

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #77 (https://github.com/Gasss23/Gas/pull/77).
2. **Deploy VPS**: dopo il merge su main, portare il codice su S2 e validare il round-trip agentico con modello reale (Groq o Gemini) — richiesto dal revisore come rischio residuo non testabile in review statica.

---

## §1 SCOPE & ESITO FETTE

**Fetta A — Prompt hardening (gas.py + gas_identity.md)**: FATTA
- #1a: run_command ristretto a conteggi/misure su file; calcola() indicato per aritmetica.
- #2+#3: 7 tool nativi elencati esplicitamente nel system prompt e in gas_identity.md.
- #4: regola fallback universale — tool fallito → dichiarazione esplicita, mai simulazione.
- #5: self-intro unificata (rimossa da `_GAS_SYSTEM_PROMPT_BASE`, sola in gas_identity.md).
- #6: finding echo NON toccato (innocuo, come da istruzione operatore).

**Fetta B — Tool calcola()**: FATTA
- Parser AST ricorsivo con whitelist (operatori + funzioni math.* + costanti).
- `eval` con `__builtins__={}` e namespace minimale — zero shell/file.
- Schema in tools_schema; dispatch in execute_tool_call.
- T62a-T62k: 16 nuovi test (292 PASS totali, 0 FAIL).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 gas.py                             | 123 ++++++++++++---
 gas_identity.md                    |  11 +-
 reports/diff_sessione.md           |  21 +--
 reports/handoff.md                 | 102 +++++++++----
 reports/stato_progetto.md          |  40 ++++-
 reports/ultimo_report.md           | 299 ++++++++-----------------------------
 tests/test_unit_kernel.py          |  35 +++++
 8 files changed, 338 insertions(+), 294 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
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

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

**Commit:** `62af5ee feat(kernel): prompt hardening (Fetta A) + tool calcola() ast-whitelist (Fetta B)`

**Verdetto review #93: APPROVATO CON RISERVE**

Elementi verificati con evidenza:
- `gas.py:83` — cortocircuito `or` in ramo BinOp: semantica corretta (primo errore vince). **ok**
- `gas.py:91` — indentazione `return err` nel diff era artefatto di formattazione; file reale ha 12 spazi. **ok**
- `gas.py:135-138` — `eval` con `__builtins__={}` + namespace whitelist: sicuro contro tutti gli exploit noti (lambda, import, open, os.system, listcomp). **ok**
- `gas.py:40-60` — system prompt: chiude F1 CRITICO, F2+F3 ALTO, F4 MEDIO dell'audit. **ok**
- `tests/test_unit_kernel.py:3645` — T62f condizione `or _r.startswith("Errore")` troppo larga. **riserva minore**

Riserve non bloccanti:
- **R-calcola-1**: `math.factorial(171)` → OverflowError non testato (nota: Python bigint non dà OverflowError; aggiunto T62k che verifica nessun crash + risultato numerico — chiarito post-review).
- **R-calcola-2**: T62f accetta "Errore di sintassi" come risposta valida agli exploit — riduce la discriminazione del test senza impatto sulla sicurezza reale.

Rischio esplicitamente escluso dal revisore: round-trip agentico con modello reale (Groq) non verificato — richiede chiavi API live, non eseguibile in review statica. Da validare prima del deploy VPS.

---

## §5 DELTA TEST DEL MOTORE

**Prima:** 276 PASS, 0 FAIL (baseline pre-sessione)
**Dopo:** 292 PASS, 0 FAIL (+16 nuovi T62a-T62k)

```
=== RIEPILOGO: 292 PASS, 0 FAIL ===
```

Nessun FAIL. I 16 nuovi test coprono: operazioni aritmetiche base (T62a-T62e), rifiuto input malevoli (T62f ×6), edge case divisione per zero e espressione vuota (T62g-T62h), factorial bigint (T62k), dispatch execute_tool_call (T62i-T62j).

---

## §6 STATO CI

```
completed  failure  feat(kernel): prompt hardening (Fetta A) + tool calcola() ast-whiteli…  CI  sonda/vps-stato-2026-08-26  push  33257612901  45s  2026-08-29T14:26:32Z
completed  success  docs(fine-task): handoff audit system-prompt 2026-08-29 — PR #77        CI  sonda/vps-stato-2026-08-26  push  33256417734  1m14s  2026-08-29T14:00:00Z
completed  success  docs(audit): system prompt — 4 finding (CRITICO/ALTO×2/MEDIO), audit … CI  sonda/vps-stato-2026-08-26  push  33256290842  59s  2026-08-29T13:56:36Z
```

Mappatura commit→run:
- `62af5ee` (commit motore) → run `33257612901` **failure**: `unit-suite` ✓ verde; `handoff-check` ✗ — §2 del handoff.md committato in `62af5ee` listava solo 4 file (reports precedenti), ma il diff reale BASE..HEAD ne aveva 8. Causa: il handoff di sessione precedente era in stage, non il nuovo. Corretto con il commit di fine-task corrente (questo).
- `37b991d` (memoria revisore) → nessuna run dedicata; incluso nell'albero testato dalla run `33257612901`.
- Commit `17b96d0`..`3cde16b` (sessioni precedenti) → run `33256417734` e `33256290842` (già dichiarati nei rispettivi handoff).

---

## §7 RISERVE APERTE

Da review #93 (questa sessione):
- **R-calcola-1**: T62k aggiunto (math.factorial bigint — no OverflowError in Python 3); riserva chiusa operativamente.
- **R-calcola-2**: T62f condizione `or _r.startswith("Errore")` troppo larga — sicurezza non impattata, test da affinare in sessione futura se si vuole discriminazione più stretta.
- **Rischio residuo revisore**: round-trip agentico con LLM reale non verificato in review statica — da validare al primo deploy VPS su S2.

Da sessioni precedenti (ancora aperte):
- R-stt-1: json.JSONDecodeError avvolto (chiusa).
- R-client4a-1: eccezioni di rete non gestite in main() di probe_client_4a.py — non bloccante per uso-e-getta.
- R-voice-3: da completare (dettaglio in handoff.md precedente).
