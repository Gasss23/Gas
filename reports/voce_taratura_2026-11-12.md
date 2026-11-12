# Voce — perché «Hey Jarvis» non risponde (misura del 12/11/2026 notte, M1)

**Sintomo (operatore, sera 11/11):** dopo l'aggiornamento con soglia 0,7 e 3 blocchi di fila Jarvis risponde una volta e poi «non risponde più»; nel log una sola attivazione (23:38, punteggio 0,90).

## Metodo
Riproducibile con `scripts/voce/misura_parola_sintetica.py` (fuori dai test: serve espeak-ng, ffmpeg e openwakeword; `--grezzi` per una riga per prova).
Modello vero `hey_jarvis_v0.1` di openWakeWord (onnx, come sul Mac), stessi blocchi da 80 ms dell'ascolto, nel container cloud. Voci sintetiche espeak-ng (it, en-us, en-gb; velocità 130/170/210; volume pieno e basso; con e senza rumore). Limite: voci sintetiche, non la voce dell'operatore. Per la voce vera c'è `scripts/voce/taratura_parola.py`.

## Risultati
**Chiamate vere** (81 prove di «hey jarvis», «hey jarvis, what time is it», «ehi jarvis»):

| regola | attivate |
|---|---|
| soglia 0,5 · 1 blocco | 37/81 |
| soglia 0,7 · 1 blocco | 35/81 |
| soglia 0,7 · 2 blocchi | 24/81 |
| soglia 0,7 · 3 blocchi (regola dell'11/11 sera) | 19/81 |

- La soglia (0,5 → 0,7) quasi non cambia le chiamate prese; **i blocchi di fila sì** (35 → 19).
- Con la pronuncia italiana il picco supera 0,7 per **1-2 blocchi** soltanto (es. voce «it» a 130/170: max 0,91-0,93, 1 blocco sopra 0,7): con 3 blocchi non scatta mai.
- Prova «taratura» con 5 chiamate di fila: 3 blocchi → **2 su 5**; 1 blocco → **5 su 5** (anche con soglia 0,8).
- Un solo «Hey Jarvis» può dare due salite staccate da 1-3 blocchi bassi (0,57 poi 0,93): la taratura le unisce.

**Falsi** (120 frasi comuni italiane e inglesi, compresi «jarvis» dentro una frase, nomi simili):
- Le frasi comuni (TV, conversazione) danno punteggio ~0: nessuna attivazione a nessuna soglia.
- Scattano solo quasi-omofoni («hey Jervis», «hey Chavez», «hey Jasmine»): 9 a 0,7·1 blocco, 3 a 0,7·3 blocchi — nessuna regola sui punteggi li distingue davvero.
- Le false attivazioni dei giorni scorsi coincidono con `GAS_ASCOLTO_SOGLIA=0.35` nel `.env` del Mac (tolta l'11/11).

## Decisione tecnica (PR di questa notte)
- Predefinito **soglia 0,7 e 1 blocco** (prima 3).
- La riga «parola quasi sentita» dice anche quanti blocchi di fila erano sopra soglia (distingue «soglia troppo alta» da «troppi blocchi»).
- `scripts/voce/taratura_parola.py`: 40 s di microfono, nessun audio salvato, consiglia la regolazione più severa che prende tutte le chiamate dell'operatore.

## Ancora aperto
- **Compromesso da confermare (operatore):** con 1 blocco i falsi sui quasi-omofoni passano da 3 a 9 su 120 frasi; le frasi comuni restano a ~0. Scelto per prendere le chiamate vere.
- Bot #378 V-1 (chiusa): l'interruzione mentre Gas parla resta su 3 blocchi di fila (`GAS_ASCOLTO_BLOCCHI_INTERRUZIONE`), perché lì il rischio è l'eco della voce di Gas, che questa misura non copre. Il blocco unico vale per l'attesa della parola e per la finestra dopo un turno (spenta di default).
- Verifica sulla voce vera (taratura sul Mac).
- Contro TV/altre persone resta la proposta di verifica del parlante (`reports/proposta_verifica_parlante.md`).
- Latenza: la prima frase arriva al client solo a fine turno (~6 s); lo streaming #374 prepara la voce prima ma la risposta parte a turno finito.
