# Ultimo report — 2026-11-24 — Voce: modello «ehi jarvis» con accento italiano

## DECISIONI UMANE RICHIESTE
1. Merge della PR (verdetto del revisore APPROVATO CON RISERVE: serve il «mergia» dell'operatore, salvo verdetto pulito del bot).
2. R-854-1, scelta tra due opzioni:
   - modello italiano: prende molte più chiamate, ma risponde a chiunque dica «ehi Jarvis» e fa più falsi sui quasi-omofoni (flusso B 49,8/h contro 33,9). Si sceglie con `bash scripts/voce/installa.sh --italiano`;
   - hey_jarvis col filtro della voce: è quello che resta se si lancia senza `--italiano`.
3. Licenza del modello CC BY-NC-SA (uso personale) in un repo pubblico: è la stessa di hey_jarvis, ma la decisione resta dell'operatore (V-3 della verifica esterna #405).
4. Prova sul Mac con la voce vera.

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

- **Fetta 3 — Riserve di verifica esterna e bot su #405**: FATTA (review #856/#857).
  - V-1 ve: `GAS_ASCOLTO_SOGLIA=0.5` scritta insieme al modello.
  - V-4 ve: ripiego su hey_jarvis anche col file mancante.
  - V-1 bot: col filtro hey_jarvis il modello si sceglie solo con `--italiano`.
  - V-3 bot: test del collegamento rilevatore→file.
  - V-2 ve, V-2 e V-4 bot: limiti e documenti riscritti.
  - R-856-1: chiusa.
- **Fetta 3c — Conflitto con main (PR #404 CRM)**: FATTA. Merge c85490e5 (review #860-MERGE APPROVATO).
- **Fetta 4 — Prova sul Mac con la voce dell'operatore**: DEFERITA. Il Mac non è raggiungibile da questa sessione.

## Anomalie
- Suite completa: 35 FAIL. I 34 di `tests/test_unit_web_browser.py` vengono da bwrap, assente nel container, e su origin/main falliscono allo stesso modo. Il FAIL di `tests/test_unit_voice_server.py` (`test_collection_dell_intero_repo_non_esplode`) era invece di questa PR, e l'avevo attribuito per errore a bwrap. Causa: gli script `frasi_test.py` e `quasi_test.py` della simulazione, che pytest prende per test. La CI l'ha trovato (unit-suite rosso su d6a980a5). Li ho rinominati in `*_prova.py` e il test ora passa.
- La prima review è stata interrotta dal limite d'uso ed è stata ripresa dopo il reset.
- L'agente di addestramento ha aggiunto all'ambiente cloud «Gas» l'host `us.aws.cdn.hf.co` (CDN di Hugging Face), con l'approvazione dell'operatore.
- Il primo handoff (21a68a4f) è uscito rovinato: la shell ha interpretato i backtick e ha lanciato `git pull` (già aggiornato) e `installa.sh` (fermato da sé: «solo per il Mac»). Nessun danno; testo corretto in d63cb6f5.
