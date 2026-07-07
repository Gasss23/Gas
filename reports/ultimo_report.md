# Ultimo report

## Task
Motore leggero, due fette con gate condizionale. Branch dedicato `refactor/model-ids-fonte-unica`
(no merge su main). Modello: Sonnet.

## FETTA 1 — Sonda

Grep di TUTTI i model string hardcoded su `gas.py`, `brains/`, `modules/` (esclusi `tests/`,
`__pycache__`, `.venv`):

| File | Riga | Stringa | Contesto |
|---|---|---|---|
| `gas.py` | 110 | `gemini-2.5-flash-lite` | definizione cascata (`GEMINI_FLASH_LITE_MODEL`) |
| `gas.py` | 111 | `gemini-2.5-flash` | definizione cascata (`GEMINI_FLASH_MODEL`) |
| `gas.py` | 112 | `llama-3.3-70b-versatile` | definizione cascata (`GROQ_MODEL`) |
| `gas.py` | 113 | `meta-llama/llama-3.3-70b-instruct:free` | definizione cascata (`OPENROUTER_FREE_MODEL`) |
| `gas.py` | 114 | `qwen2.5:7b-instruct` | definizione cascata (`OLLAMA_MODEL`) |
| `brains/groq_brain.py` | 25 | `llama-3.3-70b-versatile` | payload `"model"` |
| `brains/claude_brain.py` | 59 | `meta-llama/llama-3.3-70b-instruct:free` | 1 elemento di lista `models_to_try` (6 elementi) |
| `brains/claude_brain.py` | 76 | `llama-3.3-70b-versatile` | payload `"model"` (fallback Groq) |
| `brains/gemini_brain.py` | 18 | `gemini-2.5-flash` | f-string URL endpoint |
| `brains/gemini_brain.py` | 64 | `llama-3.3-70b-versatile` | payload `"model"` (fallback Groq) |

Altri ID modello trovati (fuori dai 5 canonici, NON mappano a nessun rung della cascata GAS):
- `brains/claude_brain.py:57-59` — altri 5 slug in `models_to_try`: `anthropic/claude-3.5-sonnet`,
  `anthropic/claude-3.5-sonnet:beta`, `google/gemini-2.5-pro`, `meta-llama/llama-3.3-70b-instruct`
  (senza `:free`), `deepseek/deepseek-r1:free`.
- `brains/openrouter_brain.py:6-9` — lista `MODELS` propria e indipendente: `qwen/qwen-2.5-72b-instruct:free`,
  `cohere/command-r-plus:free`, `meta-llama/llama-3-8b-instruct:free`.
- `modules/memory/vectors.py:84,91-93` — `EMBED_MODEL_NAME` e dizionario `_MODEL_PREFIXES`
  (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, `intfloat/multilingual-e5-small`,
  `intfloat/multilingual-e5-large`): categoria diversa (modello di EMBEDDING, non chat/cascade),
  ha già proprio meccanismo env `GAS_EMBED_MODEL` documentato in roadmap.

Nota strutturale rilevata: `brains/claude_brain.py`, `brains/groq_brain.py`, `brains/gemini_brain.py`,
`brains/openrouter_brain.py`, `brains/router.py` e `self_improve/` NON sono agganciati al
`GasKernel`/`run_turn` attivo — l'unico import da `brains/` in `gas.py` è
`from brains.router import classifica_compito` (riga 1394/1397), usato solo per classificazione
per keyword, zero model string coinvolte. Zero copertura test su questi 5 file. È la pipeline
"legacy" già segnalata dall'item roadmap #8 come fuori dalla definizione della cascata.

### Verdetto GATE
**PROCEDI a FETTA 2**, con scope preciso: i 5 ID modello canonici della cascata GAS (quelli
richiesti nell'istruzione) hanno UNA sola forma semplice — stringa letterale sostituibile con
una costante — ovunque compaiano, incluse le occorrenze nei file brain legacy. Il rischio di
import circolare segnalato dalla roadmap (item #8: "se i brains importano da gas.py") è nullo per
il design a modulo standalone `brains/model_ids.py` (zero import di progetto). Gli ID modello
extra trovati (liste di fallback multi-modello nei file legacy) NON hanno un rung/costante
corrispondente nel design a 5 costanti richiesto: lasciati hardcoded, fuori scope, proposti sotto
come decisione futura — non è "complessità strutturale non eliminabile", è semplicemente materiale
non compreso nella definizione dei 5 rung canonici.

## FETTA 2 — Fonte unica

- **Nuovo** `brains/model_ids.py`: modulo standalone, unico import `os` (stdlib), zero import di
  progetto. 5 costanti env-overridabili, default byte-identici alle stringhe sostituite:
  `MODEL_GEMINI_LITE`, `MODEL_GEMINI_FLASH`, `MODEL_GROQ`, `MODEL_OPENROUTER`, `MODEL_OLLAMA`
  (env: `GAS_MODEL_GEMINI_LITE`, `GAS_MODEL_GEMINI_FLASH`, `GAS_MODEL_GROQ`, `GAS_MODEL_OPENROUTER`,
  `GAS_MODEL_OLLAMA`).
- `gas.py`: importa da `brains.model_ids`; le costanti storiche (`GEMINI_FLASH_LITE_MODEL`,
  `GEMINI_FLASH_MODEL`, `GROQ_MODEL`, `OPENROUTER_FREE_MODEL`, `OLLAMA_MODEL`) diventano alias
  locali — i ~15 punti d'uso in `run_turn`, `doctor`, `TOOL_CAPABLE_MODELS` restano invariati
  (nessuna rinomina, diff minimo, comportamento bit-identico).
- `brains/groq_brain.py`, `brains/claude_brain.py`, `brains/gemini_brain.py`: le occorrenze
  hardcoded dei 5 ID canonici sostituite con import da `brains.model_ids`. Nel `models_to_try` di
  `claude_brain.py` sostituito SOLO l'elemento corrispondente a `MODEL_OPENROUTER`; gli altri 5
  slug restano letterali (fuori scope, vedi sonda).
- Nessun valore di modello cambiato (verificato riga per riga nel diff e dal revisore).
- **T56** aggiunto in `tests/test_unit_kernel.py`: override env `GAS_MODEL_GROQ` →
  `importlib.reload(brains.model_ids)` → la costante riflette il nuovo valore → pop env + reload
  per ripristinare il default e non contaminare il resto della suite. Zero token LLM.

### Suite locale
Eseguita per intero in Codespace: **217 PASS, 0 FAIL** (216 attesi con chiavi API live presenti
nell'ambiente + il nuovo T56). Nessuna anomalia sui test bwrap-dipendenti (comportamento già noto
e atteso in Codespace, verifica reale rimandata alla CI).

### Review revisore — verdetto INTEGRALE

```
## Verdetto

**APPROVATO CON RISERVE**

### Analisi

**Correttezza tecnica**
- `brains/model_ids.py`: modulo standalone, unico import `os` (stdlib) — verificato con `grep`, zero import di progetto. Nessun rischio di import circolare.
- I 5 default in `model_ids.py` sono byte-identici alle stringhe hardcoded sostituite (confrontati diff riga per riga: `gemini-2.5-flash-lite`, `gemini-2.5-flash`, `llama-3.3-70b-versatile`, `meta-llama/llama-3.3-70b-instruct:free`, `qwen2.5:7b-instruct`) — nessun valore di modello cambiato, solo la fonte.
- `gas.py`: le costanti storiche (`GEMINI_FLASH_LITE_MODEL` ecc.) sono ora alias che puntano a `model_ids`; verificato via `grep` che i ~15 punti d'uso in `run_turn`, `doctor`, `TOOL_CAPABLE_MODELS` (righe 137-138, 1442-1456, 1567-1597) restano intatti e continuano a leggere gli alias — comportamento bit-identico.
- I tre brain-file legacy (`claude_brain.py`, `groq_brain.py`, `gemini_brain.py`): confermato con `grep` su `gas.py` che l'unico import da `brains/` nel kernel attivo è `from brains.router import classifica_compito` (riga 1397), mai `rispondi()`/`_chiama()` che innescherebbero il caricamento di questi tre file. Zero copertura di test (`grep` su `tests/` non trova riferimenti). La claim "codice non wired" è verificata, non solo assunta.
- Le sostituzioni nei tre brain-file sono puntuali e corrette (payload dict, f-string URL, un elemento della lista `models_to_try`), nessuna logica alterata oltre alla sostituzione della stringa.
- Scelte di scope verificate e ragionevoli: `brains/openrouter_brain.py` ha una `MODELS` propria (`qwen/qwen-2.5-72b-instruct:free`, `cohere/command-r-plus:free`, `meta-llama/llama-3-8b-instruct:free`) — nessuno slug corrisponde a una costante canonica, corretto non toccarla; gli altri 5 slug OpenRouter in `claude_brain.py` (claude-3.5-sonnet, gemini-2.5-pro, ecc.) idem; `modules/memory/vectors.py::EMBED_MODEL_NAME` è un modello di embedding, categoria diversa, con proprio meccanismo env (`GAS_EMBED_MODEL`) già documentato in roadmap — corretto non toccarlo.
- Suite eseguita **dal vivo** in sessione di review: **217 PASS, 0 FAIL**, incluso T56. Nessun FAIL, nessuna anomalia bwrap.
- T56: verificato che `importlib.reload(brains.model_ids)` NON retroagisce sui binding già fatti altrove (`from brains.model_ids import X` in `gas.py` e nei brain-file punta ancora al vecchio oggetto stringa dopo il reload del modulo sorgente) — il test è quindi onesto: valida solo il comportamento di `model_ids.py` in isolamento, non un ipotetico re-binding di `gas.GROQ_MODEL`. È collocato come **ultimo test del file** (prima del riepilogo): dato che la suite è uno script eseguito top-to-bottom (non pytest), non c'è alcun test successivo che possa essere contaminato dal reload/pop env. Pattern accettabile così com'è.

**Coerenza col progetto e con la roadmap**
- Questo refactor risolve esattamente l'item roadmap #8 "Config-drift stringhe modello", incluso l'avvertimento esplicito lì registrato ("attenzione: se i brains importano da gas.py, rischio import circolare") — la soluzione adottata (modulo terzo, standalone, importato sia da `gas.py` sia dai brain-file, mai il contrario) evita quel rischio per costruzione.
- Zero tocco a `run_turn`, `_get_window`, `_cap_window_chars`, cap 10 iterazioni, cap 8k output, guardrail memoria: il diff è strettamente config-source, nessun impatto sui guardrail sorvegliati da CLAUDE.md sez. 8/9.
- Nessuna tool simulation, nessuno slicing raw della history nel codice TOCCATO da questo diff.

**Riserve (non bloccanti)**
1. Durante l'ispezione dei brain-file legacy ho notato che `brains/claude_brain.py` riga 38 contiene `for m in messages[-8:]:` — uno slicing raw della history, pattern esplicitamente vietato da CLAUDE.md sez. 5. **Non è stato introdotto da questo diff** (riga pre-esistente, non toccata) ed è in codice confermato non wired al kernel attivo/zero copertura test, quindi oggi è inerte e non bloccante per QUESTO commit. Va però registrato come debito tecnico latente in `stato_progetto.md`: se questi file legacy venissero mai ri-agganciati all'agente attivo, quello slicing violerebbe direttamente il Wall of Shame.
2. Nessuna riserva sul test T56 in sé, ma va tenuto a mente per il futuro: se altri test venissero aggiunti DOPO T56 nello stesso file, andrebbe verificato che non dipendano da uno stato "sporco" del modulo `model_ids` (oggi non accade, essendo l'ultimo test).

### Motivazione sintetica
Refactor puro di provenienza-configurazione, a rischio minimo: nessun valore di modello cambiato, nessun guardrail toccato, risolve un item di roadmap già registrato evitando esattamente il rischio che la roadmap stessa segnalava, copertura di test aggiunta e verificata dal vivo (217 PASS, 0 FAIL). Le riserve sono cosmetiche/di tracciamento (un antipattern pre-esistente scoperto per adiacenza, non causato da questo diff) e non richiedono modifiche prima del commit.
```

## STOP — proposte NON eseguite (fuori scope di questo task)

1. **Riserva #1 del revisore**: registrare in `stato_progetto.md` il debito tecnico latente
   `messages[-8:]` in `brains/claude_brain.py:38` (violazione sez. 5 CLAUDE.md, oggi inerte perché
   file non wired al kernel attivo). Non toccato in questa sessione: scope bloccato ai soli file
   di FETTA 2 dall'istruzione ricevuta.
2. **Liste di fallback multi-modello nei file legacy** (`claude_brain.py` 5 slug residui,
   `openrouter_brain.py` 3 slug propri): se in futuro si decide di dare una fonte unica anche a
   questi, serve un design diverso (lista di costanti o costante multi-valore), non il pattern
   "1 costante per rung" usato qui — decisione da prendere separatamente.
3. **Migrazione Groq** (deadline 2026-08-16, `llama-3.3-70b-versatile` dismesso): questo refactor
   crea il punto singolo (`MODEL_GROQ` in `brains/model_ids.py`) dove il valore andrà cambiato
   quando arriverà quella fetta — non eseguita qui per istruzione esplicita.

## File toccati
- `brains/model_ids.py` (nuovo — fonte unica dei 5 ID modello canonici)
- `gas.py` (import da model_ids, costanti storiche diventano alias)
- `brains/groq_brain.py`, `brains/claude_brain.py`, `brains/gemini_brain.py` (occorrenze hardcoded
  sostituite con import da model_ids)
- `tests/test_unit_kernel.py` (T56, + `import importlib`)
- `reports/ultimo_report.md` (questo file)
