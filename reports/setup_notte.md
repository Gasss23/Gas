# Setup — giro notturno di Gas sul Mac (FASE 4.5 fetta 1)

Cosa fa: ogni notte alle 03:00 il Mac lancia `python3 gas.py notte`. Gas legge
`~/.gas_notte.yaml`, esegue i compiti uno alla volta (ognuno da zero) e scrive il
riepilogo in `~/Gas/.gas_notte/ultimo_giro.md`. Nel diario va una riga per compito.

Ogni compito ha una cronologia sua (`.gas_notte/storia_<nome>.json`), separata dalla
tua conversazione. Eccezione: se approvi su Telegram un'azione parcheggiata di notte,
l'esito viene scritto nella conversazione del bot/operatore (riserva R-220-1).

Cosa NON fa da solo: le azioni rischiose (scrivere un file dopo aver letto contenuti
esterni, comandi in modalità non protetta, invii) vengono parcheggiate e chieste in
firma su Telegram. Gas non può modificare il proprio motore (gas.py, brains/, modules/)
né il catalogo (sta fuori dalla sua cartella). Quindi oggi **non** fa lavoro di
sviluppo sul codice: fa compiti di lettura, memoria, lead, resoconti.

## Passi (una volta sola)

1. Aggiorna il codice: `cd ~/Gas && git checkout main && git pull`
2. Catalogo: `cp ~/Gas/scripts/notte/catalogo_esempio.yaml ~/.gas_notte.yaml`
   e modifica i compiti a piacere (`nano ~/.gas_notte.yaml`).
2b. Tetto di spesa: nel `.env` metti `GAS_DAILY_TOKEN_BUDGET=1.0` (dollari in 24 ore, scegli tu
   il valore). Se manca, il giro notturno usa comunque 1.0 e lo segnala nel riepilogo.
2c. Tetti di tempo (opzionali, già attivi di default): `GAS_NOTTE_MAX_SEC_COMPITO=900`
   (15 minuti per compito) e `GAS_NOTTE_MAX_SEC_GIRO=7200` (2 ore per tutto il giro); i
   compiti rimasti oltre il tetto del giro vengono saltati e segnalati nel riepilogo.
   Ogni chiamata a un provider ha un timeout di 120s (`GAS_PROVIDER_TIMEOUT_SEC`; Ollama
   locale 600s, `GAS_OLLAMA_TIMEOUT_SEC`). I tetti NON sono duri: si controllano tra un
   passo e l'altro, e nel caso peggiore (tutti i provider appesi, 2 tentativi per
   provider — `GAS_PROVIDER_MAX_RETRIES=1` — Ollama compreso) un compito può sforare
   di circa 36 minuti (ordine di grandezza: un'attesa chiesta dal provider (Retry-After,
   es. su un 429) aggiunge fino a 60s per ritentativo).
3. Prova a mano: `cd ~/Gas && python3 gas.py notte` → poi `cat .gas_notte/ultimo_giro.md`
4. Timer notturno:
   ```
   mkdir -p ~/Gas/.gas_notte
   sed "s/TUO_UTENTE/$(whoami)/g" ~/Gas/scripts/notte/com.gas.notte.plist > ~/Library/LaunchAgents/com.gas.notte.plist
   launchctl load ~/Library/LaunchAgents/com.gas.notte.plist
   ```
   Prova subito senza aspettare le 3: `launchctl start com.gas.notte`, poi
   `cat ~/Gas/.gas_notte/launchd.log`.
5. Il Mac deve essere acceso (anche a schermo spento) alle 03:00; se dorme, launchd
   esegue il giro al risveglio.

## Spegnere

`launchctl unload ~/Library/LaunchAgents/com.gas.notte.plist`
(oppure metti `attivo: false` ai compiti).

## Exit code di `gas notte`

0 = tutti i compiti ok (o nessuno attivo) · 1 = almeno un compito KO, compiti saltati
per tempo o catalogo non valido · 2 = un altro giro era già in corso.
