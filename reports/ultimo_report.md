# Ultimo report — 2026-11-03 — Voce V10: «audio+pezzi», voce senza schermo (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #330 (https://github.com/Gasss23/Gas/pull/330), secondo la regola di merge di CLAUDE.md §10.
2. Il client H24 (`clients/voice/ascolto.py`, chat Mani) deve mandare `X-Gas-Formato: audio+pezzi` e leggere NDJSON solo con `Content-Type: application/x-ndjson`; altrimenti è un JSON unico: 200 `{"content": ""}`, 200 con `errore_voce` (senza chiave ElevenLabs), oppure `{"error": ...}` con 401/400/429/500/502/503 prima del turno.

## Esito delle fette

- **V10 — voce senza schermo**: `FATTA` — formato `audio+pezzi` (costante `_FORMATO_PEZZI_VOCE`): stesse righe NDJSON della V7b; il turno usa `ISTRUZIONE_VOCE` (niente dettaglio da leggere); si dice tutta la risposta divisa in frasi (`frasi_voce`), entro 1500 caratteri, mai «Il resto è a schermo»; anche «non ho capito» e «uso» arrivano a righe. Review #660-M2 APPROVATO CON RISERVE (basse/cosmetiche).
- **Bot su 956a00a**: taglio oltre 1500 caratteri ora annunciato («C'è altro, chiedimi se vuoi il resto.»), `FATTA` (review #661-M2).
- **Riserve del bot su ef88184 e della verifica esterna su 956a00a**: BASSE/COSMETICHE, `REGISTRATE` senza giro (decisione di M1).
- **Merge di origin/main (#327, V9)**: `FATTA` (review #662-M2 APPROVATO); suite completa 1063 PASS, 0 FAIL.
- Test: voice_server + voice_stt + voice_contesto + voce_ascolto + voice_prova_voci 334 passed (browser obbligatorio); mutanti → test V10 falliti.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- Il client H24 non è toccato qui (lo scrive la chat Mani): la prova vera è sul Mac.
