# Proposta: una parola di attivazione nostra («Hey Gas», forse «Jarvis») con openWakeWord

Chat Mani, 6 novembre 2026, su richiesta di M1. Solo documento: nessun codice cambia.
Le fonti sono state lette sul repo ufficiale di openWakeWord. Alcuni siti erano bloccati
dalla rete della sessione: Hugging Face, Colab, home-assistant.io e il sito di ACAV100M.
Quello che viene solo da ricerche web o da repo di terzi è segnato come **non verificato**.

## In breve

1. **Tecnicamente si può**, e su Gas non serve cambiare codice. La versione fissata di
   openWakeWord (0.6.0) carica un file `.onnx` se gli si passa il percorso; basta
   `GAS_ASCOLTO_MODELLO=/percorso/hey_gas.onnx` nel `.env`
   ([model.py v0.6.0, righe 89-100](https://github.com/dscripka/openWakeWord/blob/v0.6.0/openwakeword/model.py)).
2. **La licenza NON si risolve da sola.** Il notebook ufficiale usa come esempi negativi le
   feature ACAV100M. Secondo la loro scheda (non verificato: sito bloccato) sono CC BY-NC-SA 4.0,
   la stessa licenza non commerciale che oggi blocca «hey_jarvis». Per un modello usabile al
   lavoro servono negativi con licenze permissive, più un parere legale.
3. **L'italiano non è supportato ufficialmente.** Il generatore di voci sintetiche del
   notebook è solo inglese ([README](https://github.com/dscripka/openWakeWord#training-new-models):
   «Currently, openWakeWord only supports English»). «Hey Gas» detto in italiano va ottenuto
   con un trucco (grafia inglese che suoni simile) o modificando lo script con voci Piper
   italiane. Per l'italiano non c'è una strada ufficiale.
4. **«Jarvis» da solo** funziona già in parte con il modello attuale, ma con più parole
   perse ([doc hey_jarvis](https://github.com/dscripka/openWakeWord/blob/main/docs/models/hey_jarvis.md)).
   Le parole di due sillabe danno più falsi allarmi: Home Assistant consiglia 3-4 sillabe
   (non verificato: sito bloccato).

**Raccomandazione:** prima la licenza, poi la parola. Il primo passo costa poco ed è
un'ora su Colab gratis:
- addestrare una prova di «Hey Gas» col notebook ufficiale, così com'è, solo per uso
  personale a casa;
- misurare i falsi allarmi sul Mac per qualche giorno.

Se funziona, una seconda fetta rifà l'addestramento con negativi a licenza permissiva
prima di usarlo al lavoro.

## 1. Dove si addestra

- **Colab** (consigliato): è Linux, che è l'unico sistema supportato. Il notebook dice
  «automated model training is only supported on linux systems» per via di Piper.
  - **Colab semplice**, sotto un'ora, senza esperienza: «the performance of the model may
    be low in some deployment scenarios»
    ([README](https://github.com/dscripka/openWakeWord#training-new-models)).
  - **Notebook completo** `notebooks/automatic_model_training.ipynb`, che «can produce high
    quality models».
- **Mac M-series in locale**: non supportato. Il notebook dice «may be possible… not (yet)
  been tested». Da evitare.
- **Linux con GPU**: va bene, ma non lo abbiamo.

Passi del notebook completo:
1. installa piper-sample-generator con una voce inglese, openWakeWord e dipendenze vecchie
   fissate (tensorflow-cpu 2.8.1, ecc.);
2. scarica i dati negativi e le risposte d'ambiente;
3. genera le frasi sintetiche, le «sporca» con rumore ed eco, addestra;
4. esporta `.onnx` e `.tflite`.

**Attenzione (non verificato, da repo di terzi del 2026):** il notebook ufficiale si sarebbe
«guastato» con le versioni nuove di Python e delle librerie. Un repo della community
([openwakeword-colab-2026](https://github.com/alfiedennen/openwakeword-colab-2026)) lo ha
rimesso in piedi. Va provato prima di contarci.

## 2. Quanti campioni

- Esempi sintetici: «minimum of 20,000 recommended, often 100,000+ is best»
  ([examples/custom_model.yml](https://github.com/dscripka/openWakeWord/blob/main/examples/custom_model.yml)).
  Il notebook di esempio ne usa 1.000 solo per fare prima.
- **Registrazioni della voce dell'operatore: non servono per addestrare.** I modelli pronti
  sono «100% synthetic».
- Servono invece per il **«custom verifier»**, un secondo filtro sulla voce dell'operatore
  che c'è già nella 0.6.0. Bastano almeno 3 registrazioni della parola e circa 10 secondi di
  parlato normale («<5 minutes of effort»). «can greatly improve performance» sui falsi
  allarmi, ma poi Gas risponde meno alle altre voci
  ([docs/custom_verifier_models.md](https://github.com/dscripka/openWakeWord/blob/main/docs/custom_verifier_models.md)).
  **È la cosa più utile contro le attivazioni per sbaglio** (TV, altre persone) e si può fare
  anche col modello attuale.

## 3. Tempi e costi

- Circa **un'ora** su Colab, secondo la guida di Home Assistant (non verificato: sito
  bloccato). Generare 1.000 frasi richiede circa 10 minuti su Colab gratis con GPU T4
  (notebook).
- Secondo terzi (non verificato): 75-90 minuti su Colab Pro (circa 10 $ al mese), circa 2,5 ore
  sul Colab gratis, con il rischio che la sessione cada.
- Spazio: circa 17 GB per le feature ACAV100M più la validazione e il resto, quindi 20-45 GB
  liberi (non verificato, da repo di terzi). Il notebook ufficiale non dà cifre.

## 4. Formato e come lo usa Gas

- Esce un file `.onnx` (e un `.tflite`). Gas usa `onnx`.
- Uso: copiare `hey_gas.onnx` sul Mac (per esempio in `~/Gas/.gas_voce/`), poi nel `.env`
  `GAS_ASCOLTO_MODELLO=/Users/<nome>/Gas/.gas_voce/hey_gas.onnx`, poi
  `bash scripts/voce/installa.sh`. Nessun cambio al codice.
- Da aggiornare a mano: il LEGGIMI e la frase «Hey Jarvis» nei messaggi di riprendi.sh e
  della voce (piccola fetta).

## 5. Licenze

| Pezzo | Licenza | Fonte |
|---|---|---|
| Codice openWakeWord | Apache 2.0 | [LICENSE](https://github.com/dscripka/openWakeWord#license) |
| Modelli pronti (hey_jarvis compreso) | CC BY-NC-SA 4.0, non commerciale | README |
| Modello base di Google (embedding) | Apache 2.0 | README |
| piper-sample-generator (codice) | MIT | [LICENSE.md](https://github.com/rhasspy/piper-sample-generator/blob/master/LICENSE.md) |
| Feature ACAV100M (negativi del notebook) | CC BY-NC-SA 4.0 (**non verificato**) | scheda Hugging Face, bloccata |
| FMA (musica) | per brano, «for research purposes» | [fma](https://github.com/mdeff/fma#acknowledgments-and-licenses) |
| Voce inglese del generatore (LibriTTS-R) | CC BY 4.0 (**non verificato**) | openslr |
| Un modello addestrato da noi | il repo non dice nulla | — |

Conseguenza: con il notebook così com'è, il modello eredita con buona probabilità il vincolo
non commerciale dei negativi. È anche l'opinione di un repo di terzi, non un parere legale.
Per un modello «pulito» bisogna sostituire i negativi con dati a licenza permissiva.
Candidati, tutti da verificare:
- Common Voice (CC0);
- MUSAN (CC BY 4.0);
- LibriTTS-R (CC BY 4.0);
- registrazioni nostre.

La decisione finale spetta a un legale.

## 6. Parole corte

- «Jarvis» da solo con il modello attuale: «may also work, but likely with higher
  false-reject rates». Una segnalazione aperta dice che hey_jarvis scatta già su «hey ja»
  ([issue #142](https://github.com/dscripka/openWakeWord/issues/142)).
- Le difese contro i falsi allarmi ci sono già in openWakeWord:
  - la soglia (in Gas `GAS_ASCOLTO_SOGLIA`);
  - il filtro VAD;
  - il custom verifier;
  - le «frasi negative» nell'addestramento.
- «Hey Gas» (2-3 sillabe) è al limite del consiglio di 3-4 sillabe. Un'alternativa più
  robusta: «Ehi Gas, ascolta» o «Okay Gas».

## 7. Lingua italiana

- Il generatore ufficiale è inglese (voce `en_US-libritts_r-medium`, fonetica inglese).
- Trucco ufficiale: scrivere la parola in modo che la voce inglese la pronunci come noi, per
  esempio «hey gahs». L'accento resta inglese.
- Strada italiana, senza percorso ufficiale: piper-sample-generator accetta voci Piper
  `.onnx` di altre lingue (per esempio `it_IT-paola-medium`, `it_IT-riccardo-x_low`,
  [VOICES.md](https://github.com/rhasspy/piper/blob/master/VOICES.md)), ma `train.py` va
  modificato. Esiste una guida della community per il francese (non verificata).

## Cosa deve fare l'operatore

1. **Decidere la parola**: «Hey Gas», «Ehi Gas», «Okay Gas», oppure tenere «Hey Jarvis».
2. **Decidere sulla licenza**: se Gas resta a casa, il modello attuale e una prova col
   notebook vanno bene; per l'uso al lavoro serve un parere legale e un addestramento con
   negativi puliti.
3. **Subito, a costo zero, contro le attivazioni per sbaglio**: registrare sul Mac 3-5 volte
   «Hey Jarvis» e 10 secondi di parlato normale, per il «custom verifier» (fetta piccola
   lato Mani).
4. Se si va avanti con «Hey Gas»: un account Google per Colab (gratis va bene, Pro più
   comodo), circa un'ora con la scheda del browser aperta; poi copiare il file `.onnx` sul Mac.
5. Per completare le verifiche: consentire nella rete della sessione `huggingface.co`,
   `home-assistant.io` e `acav100m.github.io`. Servono a leggere licenze e dimensioni
   ufficiali.
