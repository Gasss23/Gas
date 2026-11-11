# Proposta — verifica del parlante per la voce H24 (solo la voce dell'operatore)

**Data:** 2026-11-11 (notte) · **Chat:** Mani · **Stato:** PROPOSTA, decide l'operatore. Niente è costruito.

## Il problema

Jarvis risponde anche ad altre persone e alla TV. Le soglie più severe (PR #371: parola a 0,7
su 3 blocchi di fila, niente turni di seguito) riducono i falsi «Hey Jarvis», ma non
distinguono **chi** parla. La verifica del parlante accetta la richiesta solo se la voce è
quella dell'operatore.

## Decisione urgente, indipendente da questa proposta

**Il modello «hey_jarvis» che usiamo oggi ha una licenza NON commerciale.** Il codice di
openWakeWord è Apache-2.0, ma tutti i suoi modelli pre-addestrati (hey_jarvis compreso)
sono CC BY-NC-SA 4.0 (README di openWakeWord, verificato). Gas è usato per lavoro: è un
rischio già oggi. Strade possibili:
1. addestrare una parola nostra («Ehi Gas», già in roadmap) con la pipeline di addestramento
   di openWakeWord (codice Apache), controllando la licenza dei dati usati;
2. accettare il rischio in modo consapevole finché la parola nostra non c'è.

## Opzioni (tutte in locale sul Mac)

| Opzione | Serve torch? | Licenza codice / modello | Registrazione della voce | Peso e ritardo (stima) | Nota |
|---|---|---|---|---|---|
| openWakeWord «custom verifier» | no | Apache / quella del modello della parola (hey_jarvis: non commerciale) | almeno 3 «Hey Jarvis» + ~10 s di voce senza la parola (+ rumori di casa, consigliati) | quasi zero | la doc dice che **non** è una vera verifica del parlante: è un filtro sopra la parola |
| sherpa-onnx + modello WeSpeaker (VoxCeleb, ONNX) | no (onnxruntime) | Apache / CC BY 4.0 (uso commerciale con citazione) | 5–10 frasi dell'operatore, mediate | basso, ~20–60 ms per 1–2 s di audio | **consigliato** |
| SpeechBrain ECAPA-TDNN | sì | Apache / da confermare sulla scheda Hugging Face | pochi secondi | medio-alto, ~50–150 ms; centinaia di MB di dipendenze | errore dichiarato 0,8–0,9 % (VoxCeleb1-O) |
| Resemblyzer | sì | Apache / Apache | 5–30 s | medio | progetto fermo, pensato per l'inglese |
| pyannote.audio | sì | MIT / da confermare, serve un token Hugging Face | pochi secondi | alto | pensato per separare i parlanti: troppo per noi |

Fonti lette dall'agente di ricerca: README di openWakeWord e `docs/custom_verifier_models.md`,
repo di Resemblyzer, SpeechBrain (ricetta VoxCeleb), pyannote-audio, sherpa-onnx (esempio
`speaker-identification.py`, pagina PyPI: wheel per macOS arm64 con Python 3.11), WeSpeaker
(`docs/pretrained.md`). **Non verificate** (siti non raggiungibili dalla sessione): le schede
dei modelli su Hugging Face e l'elenco dei file della release «speaker-recongition-models» di
sherpa-onnx. Vanno controllate prima di costruire.

## Proposta in due passi

**Passo 1 — subito, costo quasi zero (filtro):** custom verifier di openWakeWord addestrato
sulla voce dell'operatore e sui falsi allarmi registrati (TV). Si addestra in pochi minuti
con `openwakeword.train_custom_verifier(...)`, nessuna dipendenza nuova. Limite: eredita la
licenza non commerciale di hey_jarvis e non è una verifica vera.

**Passo 2 — la soluzione solida:** sherpa-onnx con un modello WeSpeaker VoxCeleb.
- Registrazione: l'operatore registra 5–10 frasi in condizioni diverse (vicino, lontano,
  voce stanca); si salva solo il **profilo** (un vettore di numeri), non l'audio.
- Dopo «Hey Jarvis» si calcola il profilo dei primi ~2 s (la parola più l'inizio della
  richiesta: un secondo solo è poco affidabile) e lo si confronta con quello registrato.
- Sotto la soglia: la richiesta **non parte** (niente Groq, niente risposta), riga nel log
  con il punteggio di somiglianza, per tarare.
- Tutto fail-safe: se il modello non si carica, l'ascolto continua come oggi e lo scrive
  nel log (decisione da prendere: continuare senza filtro o fermarsi).

## Rischi

- **Falsi rifiuti:** voce rauca, raffreddore, microfono lontano, rumore. Si riducono con più
  campioni e una soglia tarata sui dati veri; serve una via d'uscita (riprovare, o la
  conferma «Non ti riconosco» con un bip diverso).
- **Una registrazione dell'operatore riprodotta da una cassa passa.** Nessuna di queste
  opzioni distingue una voce viva da una registrata: va usata come filtro contro TV e altre
  persone, **non** come sicurezza per azioni sensibili.
- **Privacy:** il profilo vocale è un dato biometrico dell'operatore: resta sul Mac, fuori
  dal repo, come i token.

## Cosa deve decidere l'operatore

1. La licenza di hey_jarvis: parola nostra («Ehi Gas») o rischio accettato per ora.
2. Se costruire il passo 1, il passo 2, o entrambi.
3. Cosa fare se la verifica non è disponibile (modello rotto): ascolto come oggi o fermo.
