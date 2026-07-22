# Report — fix/encoding-stato-progetto — 2026-07-23

## Task
Bonifica mojibake UTF-8 in `reports/stato_progetto.md` (testo UTF-8 letto come cp1252 e ri-salvato).
Due fette in commit separati. Nessun altro file toccato.

## Revisore
Non invocato: diff doc-only (solo `reports/stato_progetto.md`, zero motore/brains/modules/tests).

---

## Fetta 1 — Riparazione encoding (commit `01cd95b`)

**Script usato**: `/tmp/fix_moji.py` (esattamente come da istruzione, non modificato).

**Misure reali:**
- Righe totali: **287**
- Righe riparate: **37**
- Righe NON riparabili: **1** (riga 167 — l'item R-encoding che citava le sequenze mojibake come esempi nel testo)

**Righe riparate (numeri):**
12, 13, 14, 17, 18, 20, 21, 22, 31, 33, 35, 36, 43, 44, 45, 91, 93, 94, 96, 97,
101, 102, 108, 109, 110, 112, 115, 117, 119, 121, 122, 123, 126, 127, 128, 129, 131

**Coincidenza con attesa dal brief:** ✅ 37 riparate, 1 NON riparabile (riga 167), 287 righe — nessuna divergenza.

---

## Verifiche bloccanti (tutte superate prima del commit)

| # | Check | Risultato | Esito |
|---|-------|-----------|-------|
| 1 | `wc -l` = 287 | `287 reports/stato_progetto.md` | ✅ |
| 2 | `git diff --stat` = 1 file, ~37 righe | `1 file changed, 37 insertions(+), 37 deletions(-)` | ✅ |
| 3 | `git diff --numstat` insertions == deletions | `37	37` | ✅ |
| 4 | `git grep` IP = 0 match | exit code 1 (nessun match) | ✅ |
| 5 | Diff visivo: ogni riga cambia solo per emoji/accentati | Verificato riga per riga nel diff completo | ✅ |

Tipi di mojibake corretti: `â€"` → `—`, `âœ…` → `✅`, `â†'` → `→`, `ðŸ"´` → `🔴`,
`ðŸŸ¡` → `🟡`, `Ã¨` → `è`, `Ã ` → `à`, `GiÃ ` → `già`, `Ã©` → `é`, ecc.

---

## Fetta 2 — Chiusura finding (commit `b695e63`)

Riga 167 sostituita con il testo di chiusura R-encoding come da template del brief.
Il file cresce da 287 a 293 righe (item da 1 riga → 7 righe): comportamento atteso,
la sostituzione è semantica non encoding.

---

## Log commit della sessione

```
b695e63 docs(stato): chiude R-encoding
01cd95b fix(encoding): ripara mojibake UTF-8 in stato_progetto.md (37 righe)
```

---

## STOP gate

- ✅ Solo `reports/stato_progetto.md` toccato
- ✅ Fetta 1 e fetta 2 in commit separati
- ✅ `/tmp/fix_moji.py` non committato
- ✅ Nessun merge, nessun `gh pr merge`, nessun motore/brains/modules/tests toccato
- ✅ PR aperta, non mergiata (vedi sotto)
