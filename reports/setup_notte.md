# Setup — giro notturno di Gas sul Mac (FASE 4.5 fetta 1)

Cosa fa: ogni notte alle 03:00 il Mac lancia `python3 gas.py notte`. Gas legge
`~/.gas_notte.yaml`, esegue i compiti uno alla volta (ognuno da zero) e scrive il
riepilogo in `~/Gas/.gas_notte/ultimo_giro.md`. Nel diario va una riga per compito.

Cosa NON fa da solo: le azioni rischiose (scrivere un file dopo aver letto contenuti
esterni, comandi in modalità non protetta, invii) vengono parcheggiate e chieste in
firma su Telegram. Gas non può modificare il proprio motore (gas.py, brains/, modules/)
né il catalogo (sta fuori dalla sua cartella). Quindi oggi **non** fa lavoro di
sviluppo sul codice: fa compiti di lettura, memoria, lead, resoconti.

## Passi (una volta sola)

1. Aggiorna il codice: `cd ~/Gas && git checkout main && git pull`
2. Catalogo: `cp ~/Gas/scripts/notte/catalogo_esempio.yaml ~/.gas_notte.yaml`
   e modifica i compiti a piacere (`nano ~/.gas_notte.yaml`).
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

0 = tutti i compiti ok (o nessuno attivo) · 1 = almeno un compito KO o catalogo non
valido · 2 = un altro giro era già in corso.
