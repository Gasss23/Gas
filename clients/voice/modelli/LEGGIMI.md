# Modelli della parola addestrati per Gas

## ehi_jarvis_it.onnx

- **Cos'è**: un riconoscitore di «ehi/hey Jarvis» detto con accento italiano. Ha la stessa rete e la stessa ricetta di openWakeWord ed è stato addestrato il 2026-11-24 su voci sintetiche: piper it_IT, voci straniere che leggono fonemi italiani, espeak.
- **sha256**: `88430a5524b7f60c721d5f4beb1ccdefbd07c1155211aa3064b39b2cefa79a86`
- **Come si usa**: `scripts/voce/installa.sh` lo copia in `.gas_voce/modelli/` (cartella 700, file 600). Se nel `.env` manca `GAS_ASCOLTO_MODELLO`, lo script scrive `GAS_ASCOLTO_MODELLO=ehi_jarvis_it` e `GAS_ASCOLTO_SOGLIA=0.5`. Se c'è il filtro della voce fatto per hey_jarvis, che col modello italiano si spegne, lo fa solo con `bash scripts/voce/installa.sh --italiano`. Per tornare indietro: nel `.env` `GAS_ASCOLTO_MODELLO=hey_jarvis` e togli `GAS_ASCOLTO_SOGLIA=0.5`.
- **Soglia**: 0,5, quella dei numeri qui sotto. `installa.sh` scrive `GAS_ASCOLTO_SOGLIA=0.5` insieme al modello, se nel `.env` non c'è già una soglia. I punteggi stanno quasi tutti vicino a 0 o a 1, quindi tra 0,4 e 0,8 cambia poco: a 0,7 la chiamata da −20 dB passa da 14/30 a 12/30. Si usa con 1 fase e senza il filtro della voce, che è legato a hey_jarvis e con questo modello resta spento da solo. Se il file manca, l'ascolto ripiega su hey_jarvis e lo scrive nel log.
- **Risultati della simulazione** (1 fase, chiamate da vicino / −6 / −12 / −20 dB):

  | | chiamate prese, voci della simulazione | chiamate prese, voci mai viste | falsi/ora, parlato italiano | falsi/ora, audio generico |
  |---|---|---|---|---|
  | hey_jarvis 0,7 | 23 / 33 / 3 / 0% | 50 / 40 / 40 / 20% | 1,06 | 0,47 |
  | ehi_jarvis_it 0,5 | 100 / 100 / 87 / 47% | 90 / 75 / 70 / 58% | 0,35 | 0 |

- **Limiti** (dettagli in `reports/voce_simulazione_2026-11-23/modello_italiano/LEGGIMI.md`):
  - Le voci sono sintetiche: la prova vera è la voce dell'operatore sul Mac.
  - Il modello non riconosce chi parla: prende il 75% delle «ehi jarvis» dette da altre voci, contro il 40% di hey_jarvis.
  - Scatta su frasi del tipo «ehi … jarvis». «ehi, chi è jarvis»: 50% contro 12%.
  - Sui flussi della simulazione pieni di quasi-omofoni («ehi gianni», «hey jasmine», «ehi, sai chi è jarvis») fa più falsi di hey_jarvis: flusso B 49,8 all'ora contro 33,9.
- **Licenza**: CC BY-NC-SA 4.0, solo uso personale e non commerciale. Il motivo è che tra i negativi dell'addestramento ci sono le feature openWakeWord ACAV100M, che hanno questa licenza. Hanno la stessa licenza anche i modelli pronti di openWakeWord, hey_jarvis compreso.
- **Attribuzioni**:
  - openWakeWord (David Scripka), feature ACAV100M;
  - Multilingual LibriSpeech (MLS) e AMI Meeting Corpus (CC BY 4.0);
  - voci piper: paola e faber (CC0), serena, LibriTTS-R e VCTK (CC BY 4.0), L2-ARCTIC (CC BY-NC 4.0), sharvard (CC BY 3.0), riccardo (M-AILABS);
  - risposte all'impulso di Traer & McDermott (MIT).
- **Rifarlo**: il metodo, lo script e il rapporto completo sono in `reports/voce_simulazione_2026-11-23/modello_italiano/`.
