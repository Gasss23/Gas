# Ultimo report — 2026-11-23 — Voce: simulazione completa, 4 fasi e interruzione col filtro

## DECISIONI UMANE RICHIESTE
1. Merge della PR (fix/voce-fasi-interruzione) col «mergia» dell'operatore se il bot dà riserve.
2. Dopo il merge, una sola prova sul Mac: `taratura_parola.py --chiamate 6` pronunciando «HEY JARVIS» all'inglese. Niente nuove registrazioni finché non si vede l'esito.
3. Decisione aperta: se anche così i punteggi restano bassi, un modello «ehi Jarvis» addestrato apposta (circa 1 giorno + 2-4 ore di GPU in cloud; non fattibile da questo ambiente, Hugging Face bloccato).

## Esito
- **Simulazione end-to-end (23/11)**, script e risultati in `reports/voce_simulazione_2026-11-23/`:
  - voci espeak a varie distanze (−6/−12/−20 dB), riverbero, rumore, TV;
  - gira il codice vero: `registra_voce.main` (microfono finto, `misura` e `addestra` veri) e `Ascolto.gira` su flussi di 30 minuti;
  - numeri: prima (verifica 0,5) vicino 89–93%, −12 dB 28–41%, 2–13 attivazioni sbagliate/ora; con le 4 fasi vicino 96%, −12 dB 41%, 1,3–4,7/ora (soglia 0,6);
  - scoperta: il modello hey_jarvis dà 0,90 a «HEY JARVIS» all'inglese e 0,40 a «ehi jarvis» all'italiana (stessa voce sintetica). È il limite vero da lontano.
- **Correzione #815 (ce04e9c7, review #815-M1coord APPROVATO CON RISERVE):**
  - 4 modelli della parola sfalsati di 20 ms, si prende il massimo (`GAS_ASCOLTO_FASI`, default 4): il punteggio dipendeva molto dalla posizione della parola sui blocchi da 80 ms;
  - interruzione col filtro attivo: soglia della parola su 1 blocco (prima 0,8 su 3, non scattava quasi mai);
  - `registra_voce`: silenzio in blocchi interi e prima ripetizione senza spostamento (clip buone scartate 4/74 → 0/74).
- **Correzione #816 (8faff652, review #816-M1coord APPROVATO CON RISERVE):** R-815-1 (la taratura usa le stesse fasi dell'ascolto), R-815-2, R-815-3 (LEGGIMI: togliere una vecchia `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8` dal `.env`), R-815-4.
- Prova col modello vero (voce chiara): 4 fasi danno 0,998 a ogni sfasamento.

- **Correzione #817 (27d33851, review #817-M1coord APPROVATO CON RISERVE):** finding del bot su #400. V-1 MEDIA: script e risultati della simulazione ora in `reports/voce_simulazione_2026-11-23/`; V-2 test dell'avviso col filtro; V-3 ambiente dei test; V-4 docstring. R-817-1 (`sim/` nel `.gitignore`) chiusa nei documenti.

- **Interruzione con 4 fasi misurata (risposta a V-1 bot #400 su b1ca6dc9):** nella configurazione predefinita (filtro + 4 fasi, 0,5 su 1 blocco) prese 170/180 nelle pause, 0 auto-interruzioni all'ora dalla voce di Gas simulata; con 0,8 su 3 blocchi 8/180. Script `interr_f4.py` e risultati `interr_f4.txt`, `interr_1fase.txt` in `reports/voce_simulazione_2026-11-23/`.

- **Correzioni #819/#820 (8c4728c0, b1cf2c4e; review #819-M1coord APPROVATO CON RISERVE, #820-M1coord APPROVATO):** finding del bot su 58fc7ed7. Soglia della verifica 0,6, la regolazione misurata con le 4 fasi: vicino 96%, −12 dB 41%, 1,3/4,7 falsi all'ora (con 0,5 e 4 fasi salivano a 6,6/8,7). 4 fasi solo col filtro della voce attivo, anche nel ripiego se il filtro non si carica.

## Test
- `tests/test_unit_voce_ascolto.py`: 379 su main → 384 passed; `pytest tests/ -k voce` 538 passed (revisore).

## Riserve aperte
- **Da provare sul Mac:** auto-interruzione con la voce vera di Gas e CPU con 4 fasi.
- Simulazione con voci sintetiche: i valori assoluti non valgono per la voce e il microfono veri; CPU con 4 fasi sul Mac da verificare.
- Interruzione mentre la voce di Gas copre la chiamata: ancora 0/180 in simulazione; funziona solo nelle pause.
- Aperte da prima: R-813M1-1, R-810M1-2, note bot #390/#395, #382 V-1/V-2, #383 V-2/V-3 (vedi `reports/stato_progetto.md`).
