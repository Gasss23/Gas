# Ultimo report — 2026-11-03 — Mani: fetta 39, ascolto H24 a frasi in fila

## DECISIONI UMANE RICHIESTE
1. Merge della PR #329 della fetta 39: **sì dell'operatore** (via M1, 3 novembre: «mergia #329 e #330»); la #330 è già in main. Il merge lo faccio io con la CI verde.
2. La voce veloce serve **anche** al formato «audio+pezzi» lato server, che fa M2: finché non è in main, l'ascolto riceve un solo audio, come prima. Dopo tutti e due i merge, sul Mac: `git pull`, `bash scripts/voce/installa.sh`, «Hey Jarvis» e una domanda: la prima frase deve partire subito.

## Esito
- **PR #328 (fetta 38)**: `FATTA` — mergiata (e3056fe).
- **Ascolto a frasi in fila (richiesta di M1)**: `FATTA` — `clients/voice/ascolto.py` chiede `audio+pezzi` e suona ogni frase appena arriva; ripieghi su JSON e audio/mpeg; test con un server vero che aspetta che la prima frase sia suonata.
- **Lettura del .env in installa.sh (V-1/V-2 bot #328)**: `FATTA` — come `gas._carica_dotenv`, con un test di confronto su 20 casi.
- **Rilevatore a intermittenza (V-1 ve #328)**: `FATTA` — il conto si azzera dopo 10 s senza errori.
- **R-625-1, R-625-2, R-631-1, R-631-2, V-3 ve #328**: `FATTA`.
- **Review #632**: APPROVATO CON RISERVE (R-632-1/2 BASSE, R-632-3 COSMETICA, registrate in stato_progetto).
- **Merge di main (PR #327, voce V9) nella #329**: `FATTA` in 96f569e, review #633 APPROVATO.
- **Prova contro la PR #330 di M2**: `FATTA` — server di #330 e ascolto di #329 insieme: frasi in fila, errore a metà, «non ho capito», senza chiave ElevenLabs e testo vuoto gestiti.
- **Bot e verifica esterna su 3b92254**: APPROVATO CON RISERVE tutti e due, solo BASSE e COSMETICHE (rilevatore che sbaglia spesso, LEGGIMI prima della #330, formati con lo schermo accettati, risposta troncata senza bip, test di R-625-2): `REGISTRATE` in stato_progetto.
- **Formato «audio+pezzi» sul server**: `FATTA da M2` — PR #330 in main (805c272).
- **Merge di main (PR #330) nella #329**: `FATTA` in d32d326, review #634 APPROVATO CON RISERVE (R-634-1/3 BASSE, R-634-2 COSMETICA, registrate); prova dal vero col server di main: frasi in fila, la prima a 0,3 s.
- **Bot su fc1cab7**: APPROVATO CON RISERVE (neutral). V-1 BASSA (server a un thread occupato durante la riproduzione): `REGISTRATA`.
- **Bot su 7957a15**: testo APPROVATO CON RISERVE, check failure per una riga del verdetto letta come «ambigua» dal parser del bot (macchina di M2). V-1 BASSA e V-2/V-3 COSMETICHE: `REGISTRATE`. Il rilancio non conta (G-2): serve un commit nuovo, questo.
