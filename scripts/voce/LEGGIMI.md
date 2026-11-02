# Voce H24 sul Mac — Gas sempre in ascolto (R8)

Gas ascolta sempre il microfono del Mac. Quando dici la parola di attivazione fa un bip,
registra fino a quando smetti di parlare, manda la richiesta al server voce e ti risponde
a voce. Dopo la risposta hai 12 secondi per continuare senza ripetere la parola.

**Parola di attivazione, per ora: «Hey Jarvis»** (modello pronto di openWakeWord).
«Ehi Gas» va addestrata a parte: sarà una fetta successiva.

**Licenza (decidi tu, R-615-5):** i modelli pronti di openWakeWord, «hey_jarvis» compreso,
sono sotto licenza CC BY-NC-SA 4.0, cioè **non commerciale**. Per provare a casa va bene;
per Gas al lavoro è una zona grigia. Il modello «Ehi Gas» addestrato da noi chiude la
questione.

## Accendere (un solo comando)

Dalla cartella di Gas, sul Mac:

```bash
bash scripts/voce/installa.sh
```

Lo script fa tutto da solo e si ferma con «STOP: …» se qualcosa manca:
1. controlla che `GAS_VOICE_TOKEN` sia nel `.env` (non lo stampa);
2. installa le dipendenze in `.venv` (`requirements.txt` e `clients/voice/requirements-ascolto.txt`);
3. scarica il modello «hey_jarvis»;
4. mette i due servizi in `~/Library/LaunchAgents` (`com.gas.voce.server` e `com.gas.ascolto`);
5. li accende con launchd, che li riavvia da solo se cadono e li riaccende a ogni accesso;
6. controlla che girino e che il server voce risponda su 127.0.0.1.

**Permesso del microfono (da provare sul Mac, R-615-4).** macOS dovrebbe chiedere il
permesso la prima volta: rispondi «Consenti». Un programma avviato da launchd però può
anche essere bloccato in silenzio, senza nessuna richiesta. Come accorgersene: dopo un
minuto `.gas_voce/ascolto.log` dice «solo silenzio assoluto». In quel caso:
1. guarda in Impostazioni di Sistema → Privacy e sicurezza → Microfono se c'è Python e
   accendilo;
2. se Python non c'è, non provare altro: dimmelo e scegliamo un'altra strada (per
   esempio un'app che lo avvia). Finché non lo proviamo sul Mac, la voce H24 non è
   dichiarata funzionante.

## Spegnere

```bash
bash scripts/voce/spegni.sh
```

Spegne i due servizi e toglie i loro file da `~/Library/LaunchAgents`: non ripartono
nemmeno al prossimo accesso. Per riaccendere: di nuovo `installa.sh`.

Per una pausa veloce senza togliere niente:
`launchctl bootout gui/$(id -u)/com.gas.ascolto` (lo riaccende il prossimo `installa.sh`
o il prossimo accesso al Mac).

## Privacy

- Prima della parola di attivazione l'audio resta solo in memoria. Lo legge openWakeWord
  sul Mac: niente rete, niente disco.
- **Attenzione alle attivazioni per sbaglio (R-615-6):** se la TV o un'altra persona dice
  qualcosa che somiglia alla parola, oppure se qualcuno parla nei 12 secondi dopo una
  risposta, quell'audio della stanza va al server voce (e quindi a Groq) e Gas lo prende
  come una richiesta. Al massimo 5 turni di fila da 30 secondi, poi serve di nuovo la
  parola. Se succede spesso, alza `GAS_ASCOLTO_SOGLIA`.
- Se dopo un bip di errore non sai se Gas ha fatto la cosa (il server può aver eseguito
  la richiesta e poi fallito la voce), chiediglielo invece di ripeterla.
- La richiesta registrata resta in memoria e va solo al server voce. **Nessuna
  registrazione viene salvata.**
- Il server voce manda l'audio a Groq per la trascrizione e il testo a ElevenLabs per la
  voce (vedi `modules/voice/server.py`): questo vale da quando dici la parola, non prima.
- La risposta di Gas passa da un file temporaneo leggibile solo da te, cancellato appena
  finisce di parlare.
- Il log dell'ascolto (`.gas_voce/ascolto.log`) contiene solo eventi e codici di errore,
  mai l'audio né il token. Il log del server (`.gas_voce/voce.server.log`) raccoglie
  invece gli avvisi di tutto Gas e può contenere pezzi della conversazione: trattalo
  come privato (V-4 della verifica esterna #323).

## Regolazioni (nel `.env`)

| Variabile | Default | Cosa fa |
|---|---|---|
| `GAS_ASCOLTO_SOGLIA` | 0.5 | sensibilità della parola (più alta = meno attivazioni per sbaglio) |
| `GAS_ASCOLTO_VOCE_RMS` | 500 | volume sopra cui conta come voce |
| `GAS_ASCOLTO_SILENZIO` | 0.8 | secondi di silenzio che chiudono la richiesta |
| `GAS_VOICE_FINESTRA` | 12 | secondi per continuare dopo la risposta |
| `GAS_VOICE_MAX_TURNI` | 5 | turni di fila senza ripetere la parola |
| `GAS_ASCOLTO_MODELLO` | hey_jarvis | modello di openWakeWord |

Dopo una modifica: `bash scripts/voce/installa.sh` (riavvia i servizi).

## Log

- `.gas_voce/ascolto.log`: attivazioni, invii, errori dell'ascolto.
- `.gas_voce/voce.server.log`: il server voce, cioè quello che stampa e gli avvisi
  (da WARNING in su) di tutto Gas.
- `gas_debug.log`, nella cartella di Gas accanto a `gas.py` (anche sotto launchd: il
  percorso non dipende dalla cartella di avvio): la scatola nera di Gas. Qui finiscono
  anche i **tempi della voce**, una riga INFO per richiesta. La riga non contiene il
  nome del logger (`gas.voce.tempi`): si cerca col testo,
  `grep "tempi voce" gas_debug.log` (es. `tempi voce (200): trascrizione=0.81s cervello=2.40s server=3.30s`;
  le altre voci possibili sono `voce` e `voce_tutta`).

I due log in `.gas_voce/` non ruotano da soli (`gas_debug.log` invece ruota a 5 MB): con il microfono staccato si aggiunge una riga ogni 5 secondi.
Se crescono troppo, svuotali senza cancellarli: `: > .gas_voce/ascolto.log` e
`: > .gas_voce/voce.server.log` (cancellati,
i servizi continuerebbero a scrivere sul file tolto fino al riavvio).
