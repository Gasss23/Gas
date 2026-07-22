# Report — docs/chiusura-item-2026-07-22 (sessione completa)

**Data**: 2026-07-22
**Branch**: `docs/chiusura-item-2026-07-22`
**Tipo sessione**: DOC-ONLY (solo `reports/`)
**Revisore**: NON invocato — diff doc-only, il gate motore non si applica.

---

## DECISIONI UMANE RICHIESTE

1. **R-crm-1b fetta 3 (telefono)**: scegliere tra riscrittura pulita su main vs recupero dal branch `feature/crm-dup-detect` (commit `1d32819`, review #49 non più valida sul contesto attuale). Blocca la chiusura di R-crm-1b.
2. **Bonifica branch remoti**: 22 branch mergiati cancellabili da UI GitHub. Azione umana — NON da sessione agente.
3. **PR #38**: mergiare `docs/chiusura-item-2026-07-22` dopo verifica (doc-only, self-merge consentito).

---

## Esito fette (sessione completa)

| Fetta | Stato | Dettaglio |
|-------|-------|-----------|
| FETTA 1 — riga CI (PR #37 + PR #36) | FATTA | Run ID `29942831200` e `29941994238` verificati live |
| FETTA 2 — onestà contatore review | FATTA + CORRETTA | Prima stesura con numeri inaffidabili (29/#19 era PR); corretta nella stessa sessione: rimossi tutti i conteggi, conservati solo dati verificabili |
| FETTA 3 — bonifica branch remoti | FATTA | 27 heads, 22 mergiati, 4 non mergiati — confermati live |
| FETTA 4 — R-crm-1b fetta 3 telefono | FATTA | Assenza su `origin/main` confermata via `git grep` (0 match) |
| CORREZIONE fetta 2 | FATTA | `#19` in `memoria_revisore.md` era ref a PR, non review; 4 formati di entry → nessun conteggio difendibile; rimossi numeri totali e liste gap |

---

## Anomalie / divergenze rilevate

- Prompt indicava 28 numeri `#N` distinti — il grep restituiva 29, ma `#19` era un riferimento a PR, non a una review, rendendo il numero invalido. Corretto in-session eliminando il conteggio.
- Prompt indicava gap "7–25" ma `#19` era presente nel file — anche questo eliminato come non difendibile.
- Testo finale in `stato_progetto.md`: nessun numero totale, nessuna lista gap; solo dati verificabili (`#57` massimo, contigui solo da `#51` a `#57`).

---

## Invariante IP

`git grep -nE IP_PATTERN -- reports/stato_progetto.md` → **0 match** verificato.
