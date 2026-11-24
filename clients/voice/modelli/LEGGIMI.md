# Modelli della parola addestrati per Gas

## ehi_jarvis_it.onnx

- **Cos'è**: un riconoscitore di «ehi/hey Jarvis» detto con accento italiano. Ha la stessa rete e la stessa ricetta di openWakeWord ed è stato addestrato il 2026-11-24 su voci sintetiche: piper it_IT, voci straniere che leggono fonemi italiani, espeak.
- **sha256**: `88430a5524b7f60c721d5f4beb1ccdefbd07c1155211aa3064b39b2cefa79a86`
- **Come si usa**: `scripts/voce/installa.sh` lo copia in `.gas_voce/modelli/` (cartella 700, file 600). Se nel `.env` manca `GAS_ASCOLTO_MODELLO`, lo script scrive `GAS_ASCOLTO_MODELLO=ehi_jarvis_it`. Per tornare indietro: `GAS_ASCOLTO_MODELLO=hey_jarvis`.
- **Soglia**: va bene quella predefinita. I punteggi stanno quasi tutti vicino a 0 o a 1, e tra 0,4 e 0,8 i risultati cambiano poco. Si usa con 1 fase e senza il filtro della voce: il filtro attuale è legato a hey_jarvis e con questo modello resta spento da solo.
- **Risultati della simulazione** (1 fase, chiamate da vicino / −6 / −12 / −20 dB):

  | | chiamate prese, voci della simulazione | chiamate prese, voci mai viste | falsi/ora, parlato italiano | falsi/ora, audio generico |
  |---|---|---|---|---|
  | hey_jarvis 0,7 | 23 / 33 / 3 / 0% | 50 / 40 / 40 / 20% | 1,06 | 0,47 |
  | ehi_jarvis_it 0,5 | 100 / 100 / 87 / 47% | 90 / 75 / 70 / 58% | 0,35 | 0 |

- **Limiti**:
  - Le voci sono sintetiche: la prova vera è la voce dell'operatore sul Mac.
  - Il modello non riconosce chi parla.
  - Scatta anche su frasi del tipo «ehi … jarvis».
- **Licenza**: CC BY-NC-SA 4.0, solo uso personale e non commerciale. Il motivo è che tra i negativi dell'addestramento ci sono le feature openWakeWord ACAV100M, che hanno questa licenza. Hanno la stessa licenza anche i modelli pronti di openWakeWord, hey_jarvis compreso.
- **Attribuzioni**:
  - openWakeWord (David Scripka), feature ACAV100M;
  - Multilingual LibriSpeech (MLS) e AMI Meeting Corpus (CC BY 4.0);
  - voci piper: paola e faber (CC0), serena, LibriTTS-R e VCTK (CC BY 4.0), L2-ARCTIC (CC BY-NC 4.0), sharvard (CC BY 3.0), riccardo (M-AILABS);
  - risposte all'impulso di Traer & McDermott (MIT).
- **Rifarlo**: il metodo, lo script e il rapporto completo sono in `reports/voce_simulazione_2026-11-23/modello_italiano/`.
