# Handoff sessione: feat/gate-c1 (2026-09-30)

## §0 — DECISIONI UMANE RICHIESTE

Nessuna decisione bloccante. Riserve tecniche da risolvere prima dell'integrazione C3/C4:

1. **R-gate-1** — `modules/gate/gate.py:88`: sostituire `unicodedata.normalize("NFC", p)` con `unicodedata.normalize("NFKC", p)`. Caratteri FULLWIDTH (U+FF0E ．, U+FF0F ／) non ridotti da NFC, bypassano la denylist.
2. **R-gate-2** — `modules/gate/gate.py:195-202`: splittare ogni token su `=` se inizia con `-`; controllare la parte destra contro `_in_denylist`. Vettore `--flag=.env.prod` attualmente non bloccato.
3. **R-gate-3** — `.github/workflows/ci.yml`: aggiungere step `python -m pytest tests/test_unit_gate.py` al workflow CI. Non modificato in C1 per rispettare lo stop gate scope.

**PR**: https://github.com/Gasss23/Gas/pull/107 (feat/gate-c1 → main, no merge)

---

## §1 — Esito sonda / test

- Gate test (locale): **65 PASS, 0 FAIL** (`python -m pytest tests/test_unit_gate.py -v`)
- Suite kernel macOS (pre-C1, invariata): **400 PASS, 5 FAIL** F-mac-1 (bwrap macOS, pre-esistenti, non toccati da C1)
- `.gas_memory.db` SHA256 invariato: `d1c8f0cc2961145a629bf0b57a43d1b0328fe4db1bf5c428a8037c92b756ef11` (confermato durante la sessione)

---

## §2 — `git diff --stat` REALE della sessione

```
.claude/agents/memoria_revisore.md |   3 +
 modules/gate/__init__.py           |   4 +
 modules/gate/gate.py               | 214 ++++++++++++++++++++++++++
 reports/stato_progetto.md          |   9 +++++---
 tests/test_unit_gate.py            | 298 +++++++++++++++++++++++++++++++++++++
 reports/ultimo_report.md           | (nuovo)
 reports/handoff.md                 | (nuovo)
 reports/diff_sessione.md           | (nuovo)
```

(BASE = `12eccd5f22cc711474ff66515e18ae12d77ef86d`)

---

## §3 — `git log` dei commit della sessione

```
83354d8 chore(revisore): memoria review #12 — ?
d74fed0 feat(gate-c1): scaffolding gate — GateClass, GATE_ALLOWLIST, gate_classify + test
8b15b69 docs(gate-c1): passo 0 — rettifica #115 + finding F-diario-args
```

---

## §4 — Verdetto INTEGRALE revisore #116

**APPROVATO CON RISERVE**

> #116 — 2026-09-30 — APPROVATO CON RISERVE — Gate C1 scaffolding (modules/gate/gate.py + tests/test_unit_gate.py). R-gate-1: NFC invece di NFKC (gate.py:88) — FULLWIDTH FULL STOP U+FF0E non ridotto a '.', bypassa denylist. R-gate-2: token --flag=value in run_command (gate.py:195-202) non splittati su '=', valore dopo '=' non controllato. R-gate-3: tests/test_unit_gate.py escluso da ci.yml. Entrambe R-gate-1 e R-gate-2 da chiudere prima dell'integrazione C3/C4.

Lezioni aggiunte in memoria_revisore.md:

> - 2026-09-30 — In un modulo di sicurezza che normalizza path con Unicode, NFC non è sufficiente: i caratteri di compatibilità (FULLWIDTH FULL STOP ．U+FF0E, FULLWIDTH SOLIDUS ／U+FF0F) non vengono ridotti ai corrispondenti ASCII da NFC, solo da NFKC. Usare sempre NFKC nei path classifier di sicurezza. Corollario: la lezione CRM del 2026-06-18 "NFKC PRIMA di collapse-whitespace/lower" vale anche per i path di sicurezza, non solo per le chiavi CRM.
> - 2026-09-30 — Il vettore --flag=value per run_command (lezione #12) rimane aperto anche dopo C1. Il Gate deve splittare ogni token sul primo '=' se inizia con '-' e controllare la parte destra contro la denylist. Non bloccante in C1 (zero integrazione con gas.py) ma obbligatorio prima dell'integrazione C3/C4.

---

## §5 — Finding CI

**R-gate-3 (processo)**: `tests/test_unit_gate.py` NON incluso in `.github/workflows/ci.yml`.

Il workflow CI (`ci.yml`) include solo per nome esplicito:
- `python tests/test_unit_kernel.py`
- `python -m pytest tests/test_unit_hooks.py`
- `python -m pytest tests/test_unit_voice_server.py`

Il nuovo file `tests/test_unit_gate.py` non verrà eseguito in CI finché non verrà aggiunto un passo dedicato. `ci.yml` NON è stato modificato in questa fetta per rispettare lo stop gate (scope C1 = solo nuovo modulo, zero file motore/infra esistenti). Da risolvere in una prossima fetta o PR separata.

---

## §6 — Prossimi passi consigliati

1. Chiudere R-gate-1 (NFC→NFKC) e R-gate-2 (--flag=value split) in C1-bis o C2 prima dell'integrazione.
2. Aggiungere step pytest gate a `ci.yml` (R-gate-3).
3. Procedere con Fetta C2 (integrazione gate in gas.py/execute_tool_call, gating DENY e UNCERTAIN).
4. Merge PR #107 dopo CI verde.
