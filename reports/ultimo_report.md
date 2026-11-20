# Ultimo report — 2026-11-20 — Voce: la registrazione tiene solo «Hey Jarvis» veri

## DECISIONI UMANE RICHIESTE
1. Merge della PR (fix/voce-registra-solo-parola) col «mergia» dell'operatore se il bot dà riserve.
2. Dopo il merge, sul Mac: rifare la registrazione della voce con lo script corretto e incollare il riepilogo.

## Esito
- **Causa trovata dall'operatore (20-11):** le clip «altra stanza / camminando / di spalle» erano rumori (lavastoviglie, pentole) salvati come «Hey Jarvis». `registra_voce.py` controllava solo il volume; dall'altra stanza il bip non si sente e la finestra era di 3 s. Il filtro non ha mai visto la voce da lontano.
- **Correzione #810 (992cef9b, review #810-M1coord APPROVATO CON RISERVE):**
  - ogni clip passa dal modello della parola (`MotoreOWW.misura`): sotto la soglia base (0,25) non si salva e lo script dice «rifallo» (3 prove);
  - gruppi lontani (attesa ≥ 6 s): finestra di 6 s, si tiene la clip di 3 s che finisce 0,5 s dopo il picco;
  - LEGGIMI aggiornato.
- **Correzione #811 (e27c655a, review #811-M1coord APPROVATO):** picco nei primi 0,5 s = parola tagliata all'inizio: si rifà (R-810M1-1 chiusa).
- Prova col modello vero openWakeWord 0.6.0 (venv locale): «Hey Jarvis» sintetico → 0,996; rumore casuale → 0,07.

## Test
- `tests/test_unit_voce_ascolto.py`: 373 su main d03e5bf2 → 375 (#810) → 376 passed (#811).

## Riserve aperte
- **R-810M1-2 BASSA:** il messaggio «di' Hey Jarvis ogni N secondi» (quando dall'altra stanza non si sente il bip) non conta la durata del bip e dell'analisi: da verificare sul Mac.
- Non verificato qui: punteggi reali della voce dell'operatore da 3 metri e dall'altra stanza (serve il microfono del Mac).
- Dalle PR #382/#383: V-1/V-2 bot #382 (ripiego del filtro durante l'ascolto, controllo delle cartelle sopra), V-2/V-3 bot #383 (varianti di «Jarvis» in tutti i punti, «Dimmi.» su una variante nel seguito).
