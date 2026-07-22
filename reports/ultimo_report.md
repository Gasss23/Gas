# Report — docs/chiusura-item-2026-07-22

**Data**: 2026-07-22
**Branch**: `docs/chiusura-item-2026-07-22`
**Tipo sessione**: DOC-ONLY (solo `reports/stato_progetto.md`)
**Revisore**: NON invocato — diff doc-only, il gate motore non si applica.

---

## DECISIONI UMANE RICHIESTE

1. **R-crm-1b fetta 3 (telefono)**: scegliere tra riscrittura pulita su main vs recupero dal branch `feature/crm-dup-detect` (commit `1d32819`, review #49 non più valida sul contesto attuale). Blocca la chiusura di R-crm-1b.
2. **Bonifica branch remoti**: 22 branch mergiati cancellabili da UI GitHub. Azione umana richiesta — NON da sessione agente.

---

## Esito fette

| Fetta | Stato | Dettaglio |
|-------|-------|-----------|
| FETTA 1 — riga CI (PR #37 + PR #36) | FATTA | Run ID verificati live: `29942831200` e `29941994238` |
| FETTA 2 — onestà contatore review | FATTA | 2 divergenze rispetto al prompt (vedi sotto) |
| FETTA 3 — bonifica branch remoti | FATTA | Numeri confermati live, nessuna divergenza |
| FETTA 4 — R-crm-1b fetta 3 telefono | FATTA | Assenza su main confermata via `git grep` (0 match) |

---

## Misure reali e divergenze

### Fetta 1 — CI run ID
- PR #37 `cb7ba8b` (2026-07-22): run `29942831200` SUCCESS (50s)
- PR #36 `4c63ff3` (2026-07-22): run `29941994238` SUCCESS (38s)

### Fetta 2 — memoria_revisore.md (divergenze dal prompt)

Comando usato: `grep -oE '#[0-9]+' .claude/agents/memoria_revisore.md | tr -d '#' | sort -n | uniq`

- Righe totali: **100** (corrisponde al prompt)
- Numeri `#N` distinti: **29** — il prompt diceva 28 — **DIVERGENZA scritta nel file**
- Numeri trovati: 5, 6, 19, 26, 27, 29-32, 36-40, 42-44, 46-57
- Gap mancanti sotto #51: `1–4, 7–18, 20–25, 28, 33–35, 41, 45`
  Il prompt scriveva "7–25" ma #19 è presente → gap corretto in `7–18, 20–25` — **DIVERGENZA scritta nel file**
- I "57" nelle due sezioni (riga 9 e riga 111) NON sono stati toccati — verificato

### Fetta 3 — branch remoti
- 27 heads su origin, 26 oltre main
- 22 mergiati in main (escl. main stesso)
- 4 non mergiati: `feature/crm-dup-detect`, `fix/crm-idemp-diario`, `fix/review44-riserve-AC`, `claude/phone-gas-development-10svqc`

### Fetta 4 — funzioni telefono
- `git grep normalizza_telefono|rileva_duplicati_telefono origin/main -- modules/`: 0 match

---

## Invariante IP

`git grep -nE IP_PATTERN -- reports/stato_progetto.md` → **0 match** pre e post edit.
