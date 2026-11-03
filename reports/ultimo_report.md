# Ultimo report — 2026-11-03 — Voce V10: «audio+pezzi», voce senza schermo (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR della V10 (numero nell'handoff §0), secondo la regola di merge di CLAUDE.md §10.
2. Il client H24 (`clients/voice/ascolto.py`, chat Mani) deve mandare `X-Gas-Formato: audio+pezzi` e leggere le righe NDJSON; senza chiave ElevenLabs la risposta è un JSON 200 con `errore_voce` (non NDJSON, non 503): il client deve gestire anche questo.

## Esito delle fette

- **V10 — voce senza schermo**: `FATTA` — formato `audio+pezzi` (costante `_FORMATO_PEZZI_VOCE`): stesse righe NDJSON della V7b; il turno usa `ISTRUZIONE_VOCE` (niente dettaglio da leggere); si dice tutta la risposta divisa in frasi (`frasi_voce`), entro 1500 caratteri, mai «Il resto è a schermo»; anche «non ho capito» e «uso» arrivano a righe. Review #660-M2 APPROVATO CON RISERVE (basse/cosmetiche).
- Test: voice_server + voice_stt + voice_contesto + voce_ascolto + voice_prova_voci 334 passed (browser obbligatorio); mutanti → test V10 falliti.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- Il client H24 non è toccato qui (lo scrive la chat Mani): la prova vera è sul Mac.
