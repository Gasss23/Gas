# Report — docs/chiusura-item-2026-07-22 (correzione contatore review)

**Data**: 2026-07-22
**Branch**: `docs/chiusura-item-2026-07-22`
**Tipo sessione**: DOC-ONLY — correzione puntuale su `reports/stato_progetto.md`
**Revisore**: NON invocato — diff doc-only, il gate motore non si applica.

---

## FETTA UNICA — Correzione misura contatore review

**Stato**: FATTA

**Problema**: il testo introdotto nella sessione precedente affermava "29 numeri `#N` distinti"
con gap espliciti "7–18, 20–25". Entrambi i valori sono inaffidabili per due motivi:
- `#19` a riga 93 di `memoria_revisore.md` è un riferimento alla PR #19, NON a una review.
- Il file usa almeno 4 formati di entry diversi (`(review #N)`, `(review #N TASK X)`,
  `- #N — data`, `#N — data`, più entry prive di numero) → metodi di conteggio diversi
  danno 29, 28 e 22. Nessun numero totale è difendibile.

**Sostituzione eseguita in `stato_progetto.md` riga 111**: il segmento da
"Misura 2026-07-22:" fino a "è un metodo INVALIDO." è stato rimpiazzato con testo
che rimuove ogni numero totale e ogni elenco di gap, conservando solo i dati
effettivamente verificabili: numero più alto = `#57`; entries contigue solo da `#51` a `#57`.

---

## Verifiche bloccanti

| Check | Esito |
|-------|-------|
| `git diff --stat` mostra UN SOLO file | `reports/stato_progetto.md` — 1 file, 1 insertion, 1 deletion |
| Testo finale senza numeri totali né elenchi gap | Confermato |
| IP invariant (0 match) | 0 match |
