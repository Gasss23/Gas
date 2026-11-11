# Ultimo report — 2026-11-11 notte — ascolto più severo, misure per tarare, diagnosi (chat Mani, PR #371)

## DECISIONI UMANE RICHIESTE

1. **Prima della prova del mattino: togliere `GAS_ASCOLTO_SOGLIA=0.6` dal `.env` del Mac** (mitigazione del 9/11): altrimenti la soglia nuova 0,7 non vale e la prova misura quella vecchia. `GAS_VOICE_MAX_TURNI=1` è ora il predefinito e si può togliere. Al riavvio `.gas_voce/ascolto.log` scrive «regolazioni in uso» e avvisa se il .env rende la parola più facile.
2. Merge della PR #371 (https://github.com/Gasss23/Gas/pull/371): riserve BASSE/COSMETICHE, quindi serve il sì dell'operatore (CLAUDE.md §10); prima va riallineata a main se è avanzato.
3. Licenza di «hey_jarvis» (CC BY-NC-SA, non commerciale) e verifica del parlante: vedi `reports/proposta_verifica_parlante.md`.
4. Al mattino: `python3 scripts/voce/diagnosi_ascolto.py` sul Mac e prova dal vivo di «Hey Jarvis»; se non scatta più, `GAS_ASCOLTO_BLOCCHI_PAROLA=2` (o soglia 0.6) nel .env.

## Esito

- **Default più severi**: FATTA (84481ea; review #757-M1, #758-M1). Soglia 0,7, 3 blocchi di fila, seguiti spenti, finestra 10 s, interruzione 0,8.
- **Bot #371 su b9ad6e7 (2 MEDIA)**: FATTA. Interruzione su 3 blocchi di fila (b36c944, #759-M1); merge di main dopo #369 (881c4bb, #760-M1).
- **Misure per tarare + diagnosi delle attivazioni**: FATTA (df3e650; #761-M1, #762-M1).
- **Bot #371 su 5b27586 (V-1 MEDIA: .env del Mac con soglia 0.6)**: FATTA (4db776c, #763-M1): regolazioni in uso nel log all'avvio, avviso se il .env le rende più facili.
- **Merge di main dopo #370**: FATTA (175289c, #764-M1).
- **Proposta verifica del parlante**: FATTA come documento (`reports/proposta_verifica_parlante.md`), decide l'operatore.
- **Difesa adattiva da eco/TV (soglia sul rumore di fondo)**: DEFERITA — prima i dati delle nuove misure.
- Test dell'ascolto: 326 passed.

## Anomalie

Nessuna.
