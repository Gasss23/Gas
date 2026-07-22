# Report — docs/chiusura-item-2026-07-22

**Data**: 2026-07-22
**Branch**: `docs/chiusura-item-2026-07-22`
**Tipo sessione**: DOC-ONLY (solo `reports/stato_progetto.md`)
**Revisore**: NON invocato — diff doc-only, il gate motore non si applica.

---

## Esito fette

| Fetta | Stato | Note |
|-------|-------|------|
| FETTA 1 — riga CI (PR #37 + PR #36) | FATTA | Run ID verificati live con `gh run list` |
| FETTA 2 — onestà contatore review | FATTA | 1 divergenza rispetto al prompt (vedi sotto) |
| FETTA 3 — bonifica branch remoti | FATTA | Numeri confermati live, nessuna divergenza |
| FETTA 4 — R-crm-1b fetta 3 telefono | FATTA | Assenza su main confermata via `git grep` |

---

## Misure reali rilevate

### Fetta 1 — CI run ID
- PR #37 merge `cb7ba8b` (2026-07-22): run `29942831200` SUCCESS (50s)
- PR #36 merge `4c63ff3` (2026-07-22): run `29941994238` SUCCESS (38s)

Fonte: `gh run list --branch main --limit 10` — nessuna invenzione.

### Fetta 2 — memoria_revisore.md

Comando: `grep -oE '#[0-9]+' .claude/agents/memoria_revisore.md | tr -d '#' | sort -n | uniq`

- Righe totali: **100** (corrisponde al prompt)
- Numeri `#N` distinti: **29** — il prompt dice 28 — **DIVERGENZA**
- Numeri trovati: 5, 6, 19, 26, 27, 29, 30, 31, 32, 36, 37, 38, 39, 40, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57
- Contigui da #51 a #57: confermato
- Numero più alto: #57
- Mancanti sotto #51: `1–4, 7–18, 20–25, 28, 33–35, 41, 45`
  Il prompt scriveva "7–25": impreciso perché **#19 è presente** nel file, quindi il gap reale è 7–18 + 20–25, non 7–25 — **DIVERGENZA**

Scritti nel file i valori misurati (29 numeri distinti; gap corretti).

Verifica "57" nelle due sezioni NON toccati (obbligatorio):
- Riga 9: "**57 review** completate" — invariato
- Riga 111: "**57 review**. Ultima: **#57**" — invariato

### Fetta 3 — branch remoti

Comandi: `git branch -r --merged origin/main` / `--no-merged`

- Merged (output grezzo): 24 righe (1 HEAD pseudo-ref + 23 branch reali incl. main)
- Branch mergiati in main (escluso main stesso): **22**
- Non mergiati: **4** — `feature/crm-dup-detect`, `fix/crm-idemp-diario`, `fix/review44-riserve-AC`, `claude/phone-gas-development-10svqc`
- Totale heads su origin: **27** (23 merged incl. main + 4 non-merged), oltre main: **26**

Nessuna divergenza dai numeri del prompt.

### Fetta 4 — telefono su main

Comando: `git grep -nE 'normalizza_telefono|rileva_duplicati_telefono' origin/main -- modules/`

Output: vuoto (0 match) — funzioni assenti su `origin/main` confermato.

---

## Invariante IP

Verificato PRE e POST edit:
```
git grep -nE '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b' -- reports/stato_progetto.md
```
Risultato: **0 match**

---

## Scope rispettato

- Toccato SOLO: `reports/stato_progetto.md` e `reports/ultimo_report.md`
- File di motore: non toccati
- Branch remoti: non cancellati
- PR: non mergiate
- Mojibake: non corretto (sessione dedicata separata, come da stop gate)
