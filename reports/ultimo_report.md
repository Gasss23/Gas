# Report task: fix/gasmerge-ip-guard-mac — fix F-mac-4

**Data:** 2026-09-12
**Branch:** fix/gasmerge-ip-guard-mac
**Tipo:** fix scripts/ (tooling merge)
**Revisore:** #97 APPROVATO

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #88 (https://github.com/Gasss23/Gas/pull/88).

---

## Esito fette

**SONDA 0 — Conferma rosso di partenza**: FATTA.
- `pytest tests/test_unit_gasmerge.py -q` → 10 FAIL / 10 PASS (confermato).
- `git grep -nE '\b...\b' HEAD -- scripts/` → exit 1, zero match (confermato: `\b` non funziona su macOS POSIX ERE).

**FIX — 3 righe in scripts/gasmerge.sh**: FATTA.
- Riga 91 (`git grep`): `\b[0-9]...\b` → `(^|[^0-9.])..([^0-9.]|$)`
- Riga 103 (`sed` loopback-strip): `\b127...\b` → `127...` (word boundary non necessaria per lo strip loopback; sufficiente rimuovere `127.x.x.x` ovunque nella riga)
- Riga 104 (`grep -qE`): `\b[0-9]...\b` → `(^|[^0-9.])..([^0-9.]|$)`

NOTA: lo scope dichiarato era "2 righe". La terza (riga 103 `sed`) ha lo stesso `\b` ed era necessaria per la correttezza del loopback-check: senza di essa il sed non avrebbe rimosso i loopback, e il grep (riga 104) fissato avrebbe trovato l'IP loopback nel residuo → BLOCCO errato. Inclusa nel fix come parte della stessa radice.

**VERIFICA**: FATTA.
- `pytest tests/test_unit_gasmerge.py -q` → **20/20 PASS** (era 10 FAIL).
- `pytest tests/ --ignore=tests/test_unit_kernel.py -q` → **121/121 PASS** (zero regressioni).

**REVISORE #97**: APPROVATO.
- Semantica fail-closed verificata.
- Nessun antipattern sez. 5/9 violato.
- Rischio falso-positivo su versioni 4-numeri (es. 1.0.73.2) già noto da review #62 — NON peggiorato. (gasmerge-ip-ok)

**FINDING NOTE**: F-mac-4 CHIUSO per il gate locale Mac. La CI GitHub (Ubuntu) non era mai stata colpita (Linux ERE supporta `\b`).

---

## Anomalie

Nessuna anomalia critica. La terza riga `sed` (103) con `\b` non era stata identificata nell'analisi preliminare — scoperta durante l'applicazione del fix. Segnalata e gestita nel perimetro della stessa root cause.
