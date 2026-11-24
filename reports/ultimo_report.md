# Ultimo report — 2026-11-24 — Voce: modello «ehi jarvis» con accento italiano

## DECISIONI UMANE RICHIESTE
1. Merge della PR (verdetto del revisore APPROVATO CON RISERVE: serve il «mergia» dell'operatore, salvo verdetto pulito del bot).
2. R-854-1: col modello italiano il filtro della voce dell'operatore (fatto per hey_jarvis) resta spento. `installa.sh` sceglie il modello italiano e avvisa. Per tornare indietro: `GAS_ASCOLTO_MODELLO=hey_jarvis` nel `.env`.
3. Una prova sul Mac con la voce vera dopo `git pull` e `bash scripts/voce/installa.sh`.

## Esito
- **Fetta 1 — Addestramento del modello** (agente in background, solo scratchpad): FATTA. Modello `ehi_jarvis_it.onnx` (sha256 88430a55…). Rete e ricetta di openWakeWord, riscritte in JAX perché download.pytorch.org è bloccato. Esportato in ONNX: stessi punteggi del modello JAX.
  - Positivi: 6000 clip sintetiche.
  - Negativi: frasi avversarie, MLS italiano, AMI, feature ACAV.
  - Simulazione, 1 fase, prese a vicino / −6 / −12 / −20 dB:

    | | voci della simulazione | voci mai viste |
    |---|---|---|
    | ehi_jarvis_it | 100 / 100 / 87 / 47% | 90 / 75 / 70 / 58% |
    | hey_jarvis | 23 / 33 / 3 / 0% | 50 / 40 / 40 / 20% |

  - Falsi all'ora:

    | | parlato italiano | audio generico |
    |---|---|---|
    | ehi_jarvis_it | 0,35 | 0 |
    | hey_jarvis | 1,06 | 0,47 |

- **Fetta 2 — Integrazione in Gas**: FATTA.
  - `clients/voice/ascolto.py`, `modello_della_parola()`: carica `.gas_voce/modelli/<nome>.onnx` solo se il nome è semplice e il file è fidato. Se il file c'è ma non è fidato, ripiega su hey_jarvis.
  - Il modello sta nel repo: `clients/voice/modelli/`, con un LEGGIMI su risultati, limiti e licenza.
  - `scripts/voce/installa.sh` copia il modello (permessi 700/600). Se il `.env` non sceglie già un modello, scrive `GAS_ASCOLTO_MODELLO=ehi_jarvis_it`. Se esiste il filtro hey_jarvis, avvisa che resta spento.
  - Script e risultati riproducibili in `reports/voce_simulazione_2026-11-23/modello_italiano/`.
- **Prova dal vero in sessione**: openWakeWord vero e `rilevatore_openwakeword("ehi_jarvis_it")` che carica il file da `.gas_voce/modelli`.

  | Frase (espeak italiano) | ehi_jarvis_it | hey_jarvis |
  |---|---|---|
  | «ehi jarvis, accendi la luce» | 1,00 | 0,49 |
  | frase neutra | 0,00 | 0,00 |

- **Fetta 3 — Prova sul Mac con la voce dell'operatore**: DEFERITA. Il Mac non è raggiungibile da questa sessione.

## Anomalie
- Suite completa: 35 FAIL, tutti in `tests/test_unit_web_browser.py` (34) e `tests/test_unit_voice_server.py` (1). Causa: bwrap non c'è in questo container. Su origin/main `tests/test_unit_web_browser.py` fallisce allo stesso modo; il test di `tests/test_unit_voice_server.py` non l'ho riprovato su main. I file della modifica non c'entrano. `tests/test_unit_voce_ascolto.py`: 388 passed.
- La prima review è stata interrotta dal limite d'uso ed è stata ripresa dopo il reset.
- L'agente di addestramento ha aggiunto all'ambiente cloud «Gas» l'host `us.aws.cdn.hf.co` (CDN di Hugging Face), con l'approvazione dell'operatore.
