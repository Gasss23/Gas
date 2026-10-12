# Report di fine task — 2026-10-12 — FETTA 1 cervello forte: budget prima di ogni chiamata

## DECISIONI UMANE RICHIESTE

1. Merge della PR #191: verdetti APPROVATO CON RISERVE (solo BASSE/COSMETICHE) → per la regola di CLAUDE.md decide l'operatore.
2. Al 1° giro (SHA e9d1058) il check `verifica-bot` è stato failure su un verdetto senza ALTA/MEDIA: probabile falso positivo di `scripts/bot_esito.py` (macchina del bot, decide l'operatore se correggerla). Al 2° giro: success.
3. Cervello forte, Fette 2–4: da discutere con l'operatore («ci sono due cose da capire») prima di qualunque codice.

## Esito

- **Merge PR #185**: `SALTATA — già mergiata dall'operatore il 2026-10-11 (20:56)`.
- **Fetta 1 — budget ricontrollato prima di ogni chiamata (chiude F2)**: `FATTA`. `GasKernel._budget_superato()` a inizio turno, prima di ogni `create` del ciclo agentico (anche il retry del Gemini 400) e prima di ogni rung di `rifletti()`; `turno_fine` marca « ; motivo=budget». Test T88a–j + T88c2. Kernel 811 → 822 PASS / 0 FAIL (locale); pytest 1032 passed (prima dei fix del bot). Review #293, #294, #295, #296 APPROVATO CON RISERVE.
- **Fix dai verificatori della PR #191** (due giri di bot e verifica esterna): `FATTA` per bot V-1/V-2 (×2 giri), verifica esterna V-2, revisore R-293-3, R-294-1, R-294-2, R-295-1. Aperte: R-293-1 (BASSA), R-296-1 e note cosmetiche dell'handoff.
- **Fette 2–4 cervello forte**: `DEFERITA — l'operatore vuole discuterle prima`.

## Anomalie

- `gh` nel container non è autenticato (GH_TOKEN rifiutato): PR e CI gestite con gli strumenti GitHub MCP.
- Bot #191 (1° giro): failure con verdetto testuale APPROVATO CON RISERVE (vedi decisione 2).
