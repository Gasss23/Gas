# Ultimo report — 2026-11-05 — Fetta bot: parser del verdetto e verdetto compresso fra i job (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #337 (https://github.com/Gasss23/Gas/pull/337): tocca la macchina del bot, quindi il bot darà neutral e il merge lo decide l'operatore (sì già dato via M1 per la fetta). Dopo il merge: rilancio una volta del bot sulla PR #335.

## Esito delle fette

- **(a1) Parser, verdetto #336 su e619103 letto come MEDIA**: `FATTA` — «una read bloccante» nella descrizione di una BASSA; `_BLOCCANTE_TECNICO` (solo read, write, recv, send, socket, I/O, select, poll).
- **(a2) Parser, verdetto #329 su 7957a15 letto «ambiguo» (3 nov)**: `FATTA` — la causa non era «R-615-4 (MEDIA, preesistente)» (già gestito) ma la prosa «- Verifica esterna su 3b92254: …» presa per titolo; `_CITAZIONE_VERIFICA_PASSATA` a lista bianca.
- **(b) Verdetto scartato da GitHub perché contiene il valore di un secret**: `FATTA` — gzip+base64 fra i job, `leggi_verdetto()` con tetto 1 MB.
- Test sui due verdetti veri (`tests/dati_verifica_bot/`) e sui casi avversari delle review: 582 passed; 21 falliscono su main.
- Review #671-M2 e #672-M2 BOCCIATO (ognuna ha trovato allentamenti NO→sì, chiusi), #673-M2 APPROVATO CON RISERVE (R-673-1/2 chiuse subito), #673-M2 bis APPROVATO.
- **Rilancio del bot sulla #335 e merge**: `DEFERITA — dopo il merge della #337` (il workflow gira dalla versione di main).
- **C1, profilo voce, sottofondo**: `DEFERITE` — ordine di M1, dopo questa fetta.

## Anomalie

- Branch nuovo `feat/bot-verdetto-m2` (diverso da quello di lavoro della voce): la correzione deve entrare in main da sola prima del rilancio sulla #335.
- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
