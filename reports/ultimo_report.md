# Ultimo report — 2026-11-21 — CRM: note minori chiuse

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta (l'operatore ha chiesto «sistema anche le note minori»). Il test del bot tocca la macchina del bot: verifica-bot sarà neutral e il merge lo decide l'operatore.
2. Restano per l'operatore: password delle copie nel `.env` del Mac, `pip install -r requirements.txt`, `pwd` della cartella di Gas, secondo controllo su claude.ai.
3. Da decidere: aggiungere al bot come gravi «alto», «severo», «serio», «elevato».

## Esito
- **PR #388 e #389**: MERGIATE il 20-11 (f75e09a2, 09e112f5).
- **Note minori**: FATTE (cd46a249, f126fbd5; review #834, #835, #836 APPROVATO CON RISERVE).
  - Un file in chiaro rimasto da un ripristino interrotto viene tolto anche subito dopo un riavvio del Mac, quando il numero del processo è stato riassegnato: conta l'ora di avvio del sistema.
  - Ripristino di un file che non si legge: messaggio che dice di controllare il percorso.
  - La pulizia dei resti avviene anche con la password sbagliata: ora è scritto nel codice.
  - Avviso della copia esterna fallita senza «riuscita» ripetuto.
  - Bot: test per «Non: grave» e «Non, grave».

## Test
- `tests/test_unit_crm.py`: 138 su main → 139 passed; `tests/test_unit_verifica_bot.py`: 630 → 632 passed. I test nuovi falliscono sul codice di prima e uccidono i mutanti indicati dal revisore.
- mypy: 0 errori in `modules/crm`. Kernel non toccato.

## Riserve aperte
- R-836-1 COSMETICA: nel test, se manca un parametro del sysctl il messaggio di errore è meno chiaro (il test fallisce comunque).
- Non verificabile qui: formato vero di `sysctl -n kern.boottime` su un Mac.
