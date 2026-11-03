# Ultimo report — 2026-11-03 — Mani: fetta 39, ascolto H24 a frasi in fila

## DECISIONI UMANE RICHIESTE
1. Merge della PR della fetta 39: lo decide l'operatore. Il verdetto del revisore è APPROVATO CON RISERVE e la PR tocca la voce, che sta nel perimetro di review.
2. La voce veloce serve **anche** al formato «audio+pezzi» lato server, che fa M2: finché non è in main, l'ascolto riceve un solo audio, come prima. Dopo tutti e due i merge, sul Mac: `git pull`, `bash scripts/voce/installa.sh`, «Hey Jarvis» e una domanda: la prima frase deve partire subito.

## Esito
- **PR #328 (fetta 38)**: `FATTA` — mergiata (e3056fe).
- **Ascolto a frasi in fila (richiesta di M1)**: `FATTA` — `clients/voice/ascolto.py` chiede `audio+pezzi` e suona ogni frase appena arriva; ripieghi su JSON e audio/mpeg; test con un server vero che aspetta che la prima frase sia suonata.
- **Lettura del .env in installa.sh (V-1/V-2 bot #328)**: `FATTA` — come `gas._carica_dotenv`, con un test di confronto su 20 casi.
- **Rilevatore a intermittenza (V-1 ve #328)**: `FATTA` — il conto si azzera dopo 10 s senza errori.
- **R-625-1, R-625-2, R-631-1, R-631-2, V-3 ve #328**: `FATTA`.
- **Review #632**: APPROVATO CON RISERVE (R-632-1/2 BASSE, R-632-3 COSMETICA, registrate in stato_progetto).
- **Formato «audio+pezzi» sul server**: `DEFERITA — è di M2 (modules/voice/ non si tocca da qui)`.
