# «Ehi Jarvis» con accento italiano — modello openWakeWord addestrato su CPU (24/11/2026)

**Esito**: `ehi_jarvis_it.onnx` (856 kB, sha256 `88430a55…a86`) prende quasi tutte le chiamate all'italiana che hey_jarvis perde, con meno falsi su audio generico e su parlato italiano vero; sui flussi pieni di quasi-omofoni («ehi gianni», «hey jasmine») sbaglia quanto hey_jarvis. Si carica così com'è: `Model(wakeword_models=[percorso], inference_framework="onnx")`, chiave `ehi_jarvis_it`.

## Come è fatto (script in `script/`, tutto rifacibile con `script/rifai_tutto.sh`)
- **Positivi**: 6000 clip sintetiche (pronuncia italiana di «ehi/hei jarvis/giàrvis» in IPA, 15% all'inglese). Voci piper paola, serena, pt_BR faber, più 800 parlanti libritts, 90 vctk, 20 l2arctic e 1 sharvard che leggono **fonemi italiani**, e 20 varianti espeak-ng it. Con length/noise scale casuali.
- **Augmentation**: velocità ±10%, livello da vicino a −28 dB, riverbero (270 risposte all'impulso MIT o sintetiche), filtro del microfono, rumore di stanza e a volte parlato vero sotto. 3 giri, cioè 18 000 finestre da 2 s.
- **Negativi**:
  - 6000 frasi italiane, parole a metà e quasi-omofoni;
  - 8000 «ehi/hey + nome»: la seconda tornata, perché il primo modello scattava su «ehi gianni»;
  - 15 h di parlato italiano letto (MLS) e 9,7 h di riunioni inglesi registrate da lontano (AMI);
  - 2,5 milioni di finestre ACAV100M, cioè 5 fette da 1,5 GB scaricate con richieste Range (non i 17 GB).
- **Rete e addestramento**: la stessa rete di openwakeword/train.py (16×96 → 128 → LayerNorm → 1), scritta in JAX perché download.pytorch.org è bloccato. Ricetta auto_train: 3 sequenze, 50k+5k+5k passi, negativi pesati fino a 1500, esempi difficili. Checkpoint scelti sulla metà A di validation_set e mediati. Circa 15 minuti di CPU. ONNX scritto a mano, uguale a JAX entro 1e-7.
- **Voci tenute fuori dall'addestramento** e usate per la prova: piper riccardo (voce italiana maschile), libritts 800–903, vctk 90–108, l2arctic 20–23, sharvard 1, espeak it+m3 (l'«operatore» della simulazione del 23/11). Anche le frasi e i quasi-omofoni della simulazione sono esclusi dall'addestramento.

## Numeri — rilevatore e ciclo VERI di `clients/voice/ascolto.py` (copia di HEAD), senza filtro della voce
Flussi A–D: simulazione del 23/11. G: 160 chiamate di voci tenute fuori. H: 5,7 h di parlato italiano vero (MLS test, 10 lettori mai visti).
| modello, fasi, soglia | A vicino/−6/−12/−20 dB | G vicino/−6/−12/−20 dB | altre voci (D) | FP/h B parlato op. | FP/h C TV | FP/h H parlato vero | FP/h audio generico* |
|---|---|---|---|---|---|---|---|
| hey_jarvis, 1, 0,7 (oggi) | 23/33/3/0% | 50/40/40/20% | 40% | 33,9 | 54,0 | 1,06 | 0,47 |
| hey_jarvis, 1, 0,5 | 47/33/3/0% | 50/42/42/25% | 42% | 37,9 | 62,0 | 1,06 | 0,47 |
| hey_jarvis, 4, 0,5 | 63/47/3/3% | 62/52/50/35% | 52% | 47,9 | 72,0 | 1,76 | – |
| **ehi_jarvis_it, 1, 0,5** | **100/100/87/47%** | **90/75/70/58%** | 75% | 49,8 | 48,0 | **0,35** | **0,0** |
| ehi_jarvis_it, 4, 0,5 | 100/100/90/60% | 95/85/70/62% | 78% | 55,8 | 60,0 | n.m. | – |
| _sensibile (variante), 1, 0,5 | 100/100/100/93% | 100/92/75/75% | 80% | 65,8 | 87,9 | 1,23 | 0,75 (metà B: 0,19) |

\* validation_set_features di openWakeWord, 10,7 h. La metà A è servita a scegliere i checkpoint. Sulla metà B, mai usata, ehi_jarvis_it fa 0 falsi a ogni soglia.

- **Latenza mediana** dalla fine della parola: 0,15 s (hey_jarvis 0,45 s).
- **Quasi-omofoni** detti da 4 voci tenute fuori, vicino al Mac (`ris/quasi_v7.txt`):

  | | «ehi jarvis» presi | quasi-omofoni nuovi | quelli della simulazione | «ehi, chi è jarvis» |
  |---|---|---|---|---|
  | ehi_jarvis_it | 100% | 5% | 12% | 50% |
  | hey_jarvis | 75% | 12% | 10% | 12% |
- **Dove nascono i falsi di B e C**: circa il 40% delle frasi di B sono quasi-omofoni ripetuti di continuo. ehi_jarvis_it scatta su 3 di queste frasi: «ehi, sai chi è jarvis», «hey jasmine», «ehi gianni». hey_jarvis scatta su «hey jasmine», «hey chavez», «hey jealous», «ehi sai chi è jarvis». Sulle frasi normali e sulla TV ehi_jarvis_it non supera 0,01; hey_jarvis arriva a 0,33.

## Soglia consigliata
**0,5 su 1 blocco, 1 fase, senza filtro della voce.** I punteggi sono quasi tutti vicini a 0 o a 1: tra 0,4 e 0,8 cambia poco (a 0,7 si perde qualche chiamata a −20 dB). Le 4 fasi aggiungono qualche presa lontana ma anche falsi su B e C: non servono senza il filtro.

## Limiti onesti
- Voci sintetiche ≠ operatore; microfono, riverbero e rumore sono simulati. Le voci piper italiane sono solo 3, e riccardo (quella tenuta fuori) è di bassa qualità. Gli altri parlanti sono voci inglesi, spagnole e portoghesi che leggono fonemi italiani. **La prova vera è sul Mac.**
- Il modello non distingue chi parla: accetta il 75% delle «ehi jarvis» di altre voci, contro il 40% di hey_jarvis. Scatta anche su frasi che contengono «ehi … jarvis» e su «ehi gianni».
- Il filtro della voce attuale è addestrato su hey_jarvis e non vale per questo modello. Con `GAS_ASCOLTO_MODELLO=ehi_jarvis_it` risulta «assente», quindi 1 fase. Per riaddestrarlo, `scripts/voce/registra_voce.py` deve accettare il modello da file: è un passo successivo, non fatto.
- Il parlato vero di H è lettura di audiolibri, non conversazione né TV vera.
- Non misurati: le interruzioni con la voce di Gas (ElevenLabs) dalle casse e la CPU sul Mac. La rete è minuscola, il costo è quello dell'embedding, come hey_jarvis.
- Variante `ehi_jarvis_it_sensibile.onnx`: più prese lontane ma circa il doppio dei falsi. Da provare solo se l'altra risponde poco sul Mac.

## Licenze dei dati e degli strumenti
- **Feature openWakeWord** (ACAV100M e validation_set): **CC BY-NC-SA 4.0**. Ne segue che il modello è **solo per uso personale, non commerciale**.
- **Parlato e risposte all'impulso**: MLS italiano CC BY 4.0; AMI CC BY 4.0; risposte all'impulso MIT (Traer & McDermott), licenza non dichiarata su HF, dati pubblicati per la ricerca.
- **Voci piper**:
  - paola e faber: CC0;
  - serena, libritts_r e vctk: CC BY 4.0;
  - l2arctic: CC BY-NC 4.0;
  - sharvard: CC BY 3.0;
  - riccardo (M-AILABS): licenza «vedi URL», di tipo BSD.
- **Strumenti usati solo per generare i dati, non distribuiti**: piper-tts 1.8 GPL-3.0, espeak-ng GPL-3.0. openWakeWord: codice Apache-2.0, modelli pronti CC BY-NC-SA.

## Per usarlo
Il caricamento da file è nel repo: `GAS_ASCOLTO_MODELLO` in `clients/voice/ascolto.py`. Modello, soglia e istruzioni sono in `clients/voice/modelli/LEGGIMI.md`; l'installazione la fa `bash scripts/voce/installa.sh`, con `--italiano` se c'è il filtro della voce di hey_jarvis.
