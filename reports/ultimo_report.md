# Ultimo report — 2026-11-02 — Voce V7b: voce frase per frase (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #325 (https://github.com/Gasss23/Gas/pull/325), secondo la regola di merge di CLAUDE.md §10.
2. Sul Mac, dopo il merge: parlare a Gas dalla pagina del browser e sentire se comincia a rispondere dopo la prima frase; confrontare la riga «tempi» con quella della V7a.

## Esito delle fette

- **V7b — voce frase per frase**: `FATTA` — formato «audio+testo+pezzi»: il server manda righe NDJSON (testo + prima frase, poi le altre frasi, poi «fine» coi tempi), una sintesi per frase; errore della voce → stop; pagina chiusa → stop della sintesi. Il proxy della pagina inoltra le righe appena arrivano e chiude la connessione verso il server se la pagina se ne va. La pagina suona le frasi in fila; interruzione, pausa ed errore fermano le frasi in arrivo; riascolto di tutta la parte parlata. Review #618–#621-M2 (riserve chiuse), #622-M2 APPROVATO.
- **Allineamento alla V7a mergiata (PR #322) e a main**: `FATTA` — test nel browser con i modi «pezzi», «pezzi_interrotti» e «guasto» insieme; review #651-M2 APPROVATO.
- **V-3 COSMETICA del bot su #322** (tipo di `t_cervello`): `FATTA`, review #652-M2 APPROVATO.
- Test: test_unit_voice_server + test_unit_voice_stt 183 passed (browser obbligatorio); 184 dopo la #653-M2.
- **Bot e verifica esterna su a73916a**: APPROVATO CON RISERVE (solo basse/cosmetiche); note del bot `FATTE` (righe chiuse su risposta illeggibile, proxy senza 502 falso, test più netto, errore della voce in console), review #653-M2.
- **V8, V9**: `DEFERITE` — PR in ordine dopo il merge della precedente.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- La resa vera (MP3 frase per frase con ElevenLabs, Safari/Chrome sul Mac) si prova solo sul Mac.
