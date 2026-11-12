# Voce H24 sul Mac — Gas sempre in ascolto (R8)

Gas ascolta sempre il microfono del Mac. Quando dici la parola di attivazione fa un bip,
registra fino a quando smetti di parlare, manda la richiesta al server voce e ti risponde
a voce, una frase alla volta: la prima si sente appena è pronta, mentre il server prepara
le altre. Dopo la risposta Gas torna subito ad aspettare «Hey Jarvis»: per un'altra
domanda si ripete la parola (dalla sera del 10/11, obiettivo «zero risposte non richieste»).

**Conversazione senza ripetere la parola (spenta di default):** con `GAS_VOICE_MAX_TURNI`
più di 1 (es. 3), dopo la risposta Gas resta in ascolto finché non passano
`GAS_VOICE_FINESTRA` secondi (10) senza che nessuno parli, e vale quanto segue.

**Nella conversazione, senza la parola** (difese contro il parlato della stanza):
- una frase senza «Hey Jarvis» lunga circa 15 secondi o più (contando anche la breve pausa
  finale) non viene mandata a Gas e chiude la conversazione (quasi sempre sono persone che
  parlano tra loro);
- se nella conversazione dici di nuovo «Hey Jarvis, …», è una richiesta normale: Gas può
  usare i suoi strumenti e la frase può durare fino a 30 secondi. Qui non c'è il bip: puoi
  dirlo tutto di seguito («Hey Jarvis, che ore sono») o fare una pausa dopo la parola (Gas
  aspetta fino a 5 secondi che cominci a parlare). Ridire la parola fa ripartire il conto dei
  turni (`GAS_VOICE_MAX_TURNI`). Del parlato di prima della parola resta
  solo un attimo (circa un secondo e mezzo, la parola compresa), e una parola sentita più di
  2 secondi prima che si cominci a parlare non conta;
- Gas decide se il parlato è rivolto a lui: se non lo è, non risponde e chiude la
  conversazione;
- se dici «pausa» (o «standby», «basta così») Gas chiude la conversazione e torna ad
  aspettare «Hey Jarvis»: senza la parola lo fa in silenzio, con «Hey Jarvis, pausa»
  risponde «Va bene.». Per riprendere basta la parola. Lo standby vero, che non sente nemmeno la
  parola, resta `bash scripts/voce/pausa.sh` (vedi sotto);
- se qualcosa va storto in un turno senza la parola, la conversazione si chiude in silenzio.

**«Sì, signore?»:** dopo la parola, invece del bip, Jarvis risponde «Sì, signore?» con la sua
voce. L'audio lo prepara il server voce una volta per voce; l'ascolto lo scarica in sottofondo
all'avvio e lo tiene in memoria. Finché non c'è, o se il server dà errore, senti il bip di
sempre. Quando interrompi Gas resta il bip, più rapido; nella conversazione senza la parola non c'è bip.
Se cambi la voce di Jarvis sul server, «Sì, signore?» resta con la voce vecchia fino al
riavvio dell'ascolto: `bash scripts/voce/installa.sh`.

**Richiesta d'un fiato:** se dici «Hey Jarvis, che ore sono» senza pause, Jarvis non dice
«Sì, signore?» (coprirebbe la tua frase) e registra subito. Basta che nel primo 0,6 s dopo
la parola parta voce continua per almeno 0,4 s; se invece ti fermi dopo «Hey Jarvis», senti la conferma e
poi parli. Se dopo la parola senti
comunque «Sì, signore?», la frase era troppo corta (sotto circa due terzi di secondo, es. «Hey
Jarvis, pausa» detto di corsa): non è stata mandata, ripetila dopo la conferma. Nel log, ogni «richiesta registrata» dice anche quanti secondi di voce e quanto
forte (in multipli di `GAS_ASCOLTO_VOCE_RMS`): utile se le richieste arrivano tagliate.

**Interrompere Gas:** mentre risponde, di' di nuovo la parola di attivazione: si ferma
subito, salta le frasi che mancavano, fa il bip e ascolta la nuova domanda. Serve proprio
la parola, non basta parlare: con le casse del Mac il microfono sente anche la voce di Gas.
Per questo, mentre Gas parla, la parola deve essere riconosciuta con più sicurezza (soglia
0.8 invece di 0.7, e come sempre per `GAS_ASCOLTO_BLOCCHI_PAROLA` blocchi di fila). Anche coi turni di seguito spenti (il default) un'interruzione apre la
nuova domanda; se interrompi di nuovo anche quella risposta, Gas si ferma e torna ad
aspettare la parola. Se non ti sente, avvicinati o abbassa un po' il volume; con le cuffie va meglio.
Se nella risposta Gas stesso dice la parola («di' Hey Jarvis…»), per quella risposta
l'interruzione è spenta: altrimenti si interromperebbe da solo, sentendosi dalle casse.
Questo controllo vale con il formato di risposta predefinito (a frasi): con
`GAS_ASCOLTO_FORMATO` vuoto (un solo MP3) il testo della risposta non arriva e
l'interruzione resta accesa.

**Parola di attivazione: «Hey Jarvis»** (modello pronto di openWakeWord). Una parola
nostra («Hey Gas») non si fa: decisione dell'operatore del 7 novembre 2026
(`reports/proposta_parola_gas.md`).

**Licenza (decidi tu, R-615-5):** i modelli pronti di openWakeWord, «hey_jarvis» compreso,
sono sotto licenza CC BY-NC-SA 4.0, cioè **non commerciale**. Per provare a casa va bene;
per Gas al lavoro è una zona grigia, e resta da decidere.

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

## Pausa (standby) e ripresa

Per una pausa, per esempio mentre parli con un'altra persona:

```bash
bash scripts/voce/pausa.sh      # Gas non ascolta più, nemmeno «Hey Jarvis»
bash scripts/voce/riprendi.sh   # Gas ascolta di nuovo
```

La pausa ferma solo l'ascolto: il server voce resta acceso e non si toglie nessun file.
`riprendi.sh` controlla anche che l'ascolto resti acceso: se si ferma subito (per esempio
perché l'ambiente Python è rotto) lo dice e indica il log da guardare. Il controllo
guarda i primi 3 secondi: un errore che arriva dopo (per esempio il permesso del microfono
o il caricamento del modello) non lo vede, e se l'ascolto si riavvia di continuo può
capitare che risponda «Gas sta già ascoltando». In questi casi guarda il log.
Dura fino a `riprendi.sh` o al prossimo riavvio del Mac (all'accesso l'ascolto riparte da
solo).

## Privacy

- Prima della parola di attivazione l'audio resta solo in memoria. Lo legge openWakeWord
  sul Mac: niente rete, niente disco.
- **Attenzione alle attivazioni per sbaglio (R-615-6):** se la TV o un'altra persona dice
  qualcosa che somiglia alla parola, quell'audio della stanza va al server voce (e quindi a
  Groq). Per questo dalla sera del 10/11 la parola vale solo se è chiara (soglia 0,7, 3
  blocchi da 80 ms di fila) e dopo la risposta non si ascolta senza la parola. Se riaccendi
  i turni di seguito (`GAS_VOICE_MAX_TURNI`), anche chi parla nei secondi dopo una risposta
  finisce al server: senza la parola ogni frase dura al massimo 15 secondi (oltre non si
  manda) e Gas chiude la conversazione se capisce che non parlavi a lui.
- **Il `.env` vince sui predefiniti.** Se nel `.env` hai ancora `GAS_ASCOLTO_SOGLIA=0.6`
  (la mitigazione del 9/11), la soglia nuova 0,7 non vale: toglila. `GAS_VOICE_MAX_TURNI=1`
  ora è il predefinito e si può togliere. All'avvio `.gas_voce/ascolto.log` scrive
  «regolazioni in uso: …» e avvisa se il `.env` rende la parola più facile dei predefiniti.
- Se la parola vera non scatta più: lancia `python3 scripts/voce/taratura_parola.py`
  (dici «Hey Jarvis» qualche volta e lo script consiglia soglia e blocchi sulla tua voce,
  senza salvare audio), oppure abbassa `GAS_ASCOLTO_SOGLIA` (0.6). Se nel `.env` c'è
  `GAS_ASCOLTO_BLOCCHI_PAROLA=2` o `3`, toglilo: con la pronuncia italiana il picco della
  parola dura 1-2 blocchi (misura del 12/11, `reports/voce_taratura_2026-11-12.md`).
- Se la parola scatta spesso per sbaglio, alza `GAS_ASCOLTO_SOGLIA` o `GAS_ASCOLTO_BLOCCHI_PAROLA`; per parlare
  con qualcuno senza Gas, `bash scripts/voce/pausa.sh`.
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
| `GAS_ASCOLTO_SOGLIA` | 0.7 | sensibilità della parola (più alta = meno attivazioni per sbaglio) |
| `GAS_ASCOLTO_BLOCCHI_PAROLA` | 1 | blocchi da 80 ms di fila sopra la soglia perché la parola valga (1–5; più alto = meno attivazioni per sbaglio) |
| `GAS_ASCOLTO_VOCE_RMS` | 200 | volume sopra cui conta come voce (più basso = sente anche la voce piana; se in una stanza rumorosa parte da solo o non chiude la richiesta, alzalo a 300–500) |
| `GAS_ASCOLTO_SILENZIO` | 0.8 | secondi di silenzio che chiudono la richiesta |
| `GAS_ASCOLTO_CONFERMA` | 1 | `0` = dopo la parola solo il bip, senza «Sì, signore?» |
| `GAS_ASCOLTO_INTERRUZIONE` | 1 | `0` = la parola non interrompe Gas mentre parla |
| `GAS_ASCOLTO_SOGLIA_INTERRUZIONE` | 0.8 | sensibilità della parola mentre Gas parla (più bassa = la sente meglio, ma rischia di attivarsi con la voce di Gas) |
| `GAS_VOICE_FINESTRA` | 10 | secondi di silenzio dopo i quali la conversazione si chiude (0–120; `0` = niente finestra. La stessa variabile vale per la pagina web della voce, che accetta solo da più di 0 fino a 120: se usi anche quella, non mettere 0) |
| `GAS_VOICE_SEGUITO_MAX` | 15 | secondi massimi di una frase senza «Hey Jarvis» nella conversazione (3–30) |
| `GAS_VOICE_MAX_TURNI` | 1 | turni dopo la parola, il primo compreso (1 = solo la richiesta dopo «Hey Jarvis»: per continuare si ripete la parola; 3 = la richiesta più 2 di seguito senza ripeterla) |
| `GAS_ASCOLTO_MODELLO` | hey_jarvis | modello di openWakeWord |
| `GAS_ASCOLTO_FORMATO` | audio+pezzi | risposta a frasi in fila; vuoto = un solo audio alla fine, come prima |

Dopo una modifica: `bash scripts/voce/installa.sh` (riavvia i servizi).

## Log

- `.gas_voce/ascolto.log`: attivazioni, invii, errori dell'ascolto. Solo numeri, mai audio
  né testo: ogni «parola di attivazione» dice il punteggio della parola e quante salite
  troppo corte (falsi «Hey Jarvis» fermati) ci sono state prima; ogni «richiesta
  registrata» dice secondi di voce e volume medio e massimo (in multipli di
  `GAS_ASCOLTO_VOCE_RMS`).
  Ogni «parola quasi sentita» è una salita del rilevatore (punteggio da 0,30 in su) che
  NON ha attivato: punteggio massimo, blocchi, soglia in uso (al massimo una riga ogni 5 s,
  le altre contate col loro punteggio massimo; il conteggio è una stima). Vale solo nell'attesa di «Hey Jarvis»: nella
  finestra dopo una risposta e mentre Gas parla le salite scartate non si scrivono. Se «Hey Jarvis» detto da te finisce lì con punteggi tra 0,5 e 0,7, la
  soglia è troppo alta: `GAS_ASCOLTO_SOGLIA=0.6` in `.env` e `bash scripts/voce/installa.sh`.
- **Diagnosi in un comando:** `python3 scripts/voce/diagnosi_ascolto.py` (dalla cartella di
  Gas) riassume gli ultimi 2 giorni: attivazioni con richiesta, senza richiesta (di solito
  false: TV, persone), sospette (meno di 0,6 s di voce, dove Whisper inventa «Grazie»), e
  le ultime 20 con ora e punteggio. Più giorni: `--giorni 7 --ultime 50`. È una stima, non
  la verità: «senza richiesta» può anche essere un «Hey Jarvis» vero senza domanda dopo.
- `.gas_voce/voce.server.log`: il server voce. Contiene i suoi messaggi a schermo e gli
  avvisi (da WARNING in su) di tutto Gas.
- `gas_debug.log`, nella cartella di Gas accanto a `gas.py` (anche sotto launchd: il
  percorso non dipende dalla cartella di avvio): la scatola nera di Gas. Qui finiscono
  anche i **tempi della voce**: una riga INFO per ogni richiesta di cui il server ha
  misurato dei tempi (trascrizione, cervello, voce; niente riga, per esempio, per una
  richiesta rifiutata col 401). La riga non contiene il nome del logger (`gas.voce.tempi`): si cerca col testo,
  `grep "tempi voce" gas_debug.log` (es. `tempi voce (200): trascrizione=0.81s cervello=2.40s server=3.30s`;
  le altre voci possibili sono `voce` e `voce_tutta`).

I due log in `.gas_voce/` non ruotano da soli (`gas_debug.log` invece ruota a 5 MB): con il microfono staccato si aggiunge una riga ogni 5 secondi.
Se crescono troppo, svuotali senza cancellarli: `: > .gas_voce/ascolto.log` e
`: > .gas_voce/voce.server.log` (cancellati,
i servizi continuerebbero a scrivere sul file tolto fino al riavvio).
