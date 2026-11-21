# Ultimo report — 2026-11-21 — Voce: registrazione, microfono muto e secondi del messaggio

## DECISIONI UMANE RICHIESTE
1. Merge di questa PR col «mergia» dell'operatore se il bot dà riserve.

## Esito
- **PR #390 (registrazione solo con «Hey Jarvis» veri): MERGIATA** il 21-11 (dcedea6a) col via dell'operatore.
- **Correzione #813 (b46fde99, review #813-M1coord APPROVATO CON RISERVE)**: chiude V-1/V-2 del bot su #390 e R-810M1-2.
  - Microfono muto senza errore (permesso negato): la registrazione si ferma dopo le prime 3 prove con il messaggio sul permesso del microfono, invece di 45 bip a vuoto.
  - Gruppi lontani: «dillo ogni 9 secondi circa» (numero intero, con il margine del ciclo vero: bip, analisi, pausa).
  - LEGGIMI aggiornato.
- Ramo ripartito da main dcedea6a con cherry-pick dei commit di #813: il diff di codice ha lo stesso SHA-256 di quello revisionato (31c92e5c).

## Test
- `tests/test_unit_voce_ascolto.py`: 376 su main → 379 passed.

## Riserve aperte
- **R-813M1-1 BASSA:** manca un test «suono forte non riconosciuto 3 volte → la registrazione non si ferma».
- **Bot #390 (ultimo giro), BASSE:** V-1 nessun test di main() con un motore che ha `misura`; V-2 soglia di 0,5 s per la parola tagliata all'inizio forse troppo larga (verso 1 s, o energia dei primi blocchi); V-3 clip da vicino accorciate dal taglio sul picco.
- Non verificabile qui: comportamento di macOS col permesso del microfono negato (silenzio puro o rumore minimo).
