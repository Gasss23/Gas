# Report — 2026-07-15 — Fix guardia handoff.md e auto-riferimento §5

## DECISIONI UMANE RICHIESTE

Nessuna.

---

## Scope & Esito

### FETTA UNICA — 2 fix a `.claude/commands/fine-task.md` (doc-only)

**FIX 1 — guardia sul punto 4**: `FATTA`
Aggiunto blocco "Check comune (vale per i punti 4 e 5)" tra il punto 3 e il punto 4.
Il check esegue `git diff --stat ${BASE}..HEAD -- reports/handoff.md` una sola volta.
Il punto 4 ora condiziona il cat:
- output vuoto → stampa `"handoff.md non rigenerato in questa sessione — nessun contenuto da stampare."`
- output non vuoto → catta il file.
Il punto 5 riferisce lo stesso esito senza rieseguire il comando.
Motivo incluso nel file: un handoff di sessione precedente presentato come output corrente è indistinguibile da uno fresco.

**FIX 2 — auto-riferimento numerico**: `FATTA`
"Se il check al punto 5 è vuoto, l'assenza dell'URL è l'informazione corretta"
→ "Se il check diff --stat è vuoto, l'assenza dell'URL è l'informazione corretta".
Grep `punto [0-9]` sul file dopo il fix: nessun altro riferimento auto-numerato rimasto.

### Verifica scope ${BASE}

`${BASE}` è definito in §0 del documento. Il check comune in §5 usa `${BASE}..HEAD -- reports/handoff.md`,
coerente con i range già presenti in §2 e §3. Stesso punto di dipendenza del check preesistente al punto 5.
**Verdetto**: in scope. Stop gate non attivato.

---

## Anomalie

Nessuna.
