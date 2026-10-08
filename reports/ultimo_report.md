# ULTIMO REPORT — 2026-10-08 — Follow-up #155: riserve del bot sul log di `rifletti` (PR #156)

## Riassunto

Chiuse le 3 riserve BASSE del bot di verifica su PR #155. L'anteprima della risposta
scartata ora resta limitata anche quando il provider restituisce qualcosa che non è testo,
è marcata NON FIDATA, e la lunghezza non dice più "0" a vuoto. PR #156, impilata su #155.

## DECISIONI UMANE RICHIESTE

1. Mergiare PRIMA la PR #155 (https://github.com/Gasss23/Gas/pull/155), POI la PR #156
   (https://github.com/Gasss23/Gas/pull/156). Dopo il merge di #155 il report di #156 va
   rigenerato (lo faccio io: il diff di #156 si riduce al solo commit `ad7b87e`).
2. Decidere se allineare CLAUDE.md ai 3 check required del ruleset `main-lock` (aperto da #155).
3. Dopo i merge, sul Mac: `gas rifletti` e mandare la riga `riflessione: … risposta non valida` di `gas_debug.log`.

## Esito

- **V-1 bot — anteprima senza limite per content non testuale** (`gas.py`, `ad7b87e`): FATTA — il `repr`
  viene troncato con la stessa logica inizio+coda e preceduto dal tipo (`<list> …`).
- **V-2 bot — anteprima di output non fidato in log e stderr**: FATTA — marcatore `anteprima[NON FIDATA]=`.
- **V-3 bot — `lunghezza=0` fuorviante, motivo "mai chiuso" impreciso**: FATTA — `_lunghezza_log`
  (`n/d (<tipo>)`); motivo "nessuna '}' dopo la prima '{'".
- **V-3 bot — scarto 703/705 locale vs CI**: SALTATA — non è un difetto del codice; causa non indagata.
- **Test**: FATTA — T80l2 esteso, T80l4, T80u4. Suite kernel: 705 PASS, 0 FAIL.
- **Revisore**: #215 APPROVATO (due note cosmetiche non vincolanti).

## Anomalie

- PR #156 è impilata su #155: finché #155 non è mergiata, diff e handoff includono anche i commit di #155.
