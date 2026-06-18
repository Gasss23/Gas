# Vector store — WIRING: retrieval semantico agganciato al kernel

**Data:** 2026-06-18
**Commit motore:** vedi hash stampato a fine task (revisore #24 — APPROVATO CON RISERVE)
**Commit doc:** vedi hash stampato a fine task
**Suite:** **152/152, 0 FAIL** (era 145)
**Scope:** cablaggio della fetta 1 (storage+embedding, già in main, review #23) al motore:
`run_turn` (catch-up indexing) + `ricorda` (cascata semantica) + snippet datato. Tocca
`gas.py`. Invarianti del motore blindato INTATTE.

---

## COSA È STATO FATTO

### 1. `gas.py __init__` — `self.vectors` OPT-IN e fail-safe
- Costruito SOLO se env `GAS_VECTORS` è truthy (nuovo helper `_env_flag`: vero per
  1/true/on/yes/si, tutto il resto → False). **Default OFF di proposito**: il modello di
  embedding pesa ~500MB su disco + RAM (R-vec-3, VPS 1GB irrisolta) — non va imposto al
  deploy base né alla suite. Quando OFF, GAS gira **bit-identico a ieri**.
- Stessa **doppia cintura fail-safe** di `self.memory` (try/except in `__init__` → `None`).
- `self._vec_watermark` (id diario max già indicizzato, risolto al primo turno dal sidecar)
  + `self.VEC_CATCHUP_MAX` (env `GAS_VECTORS_CATCHUP_MAX`) + costante `VEC_MIN_SIM`.

### 2. `_vettori_catchup()` — indicizzazione pigra, bounded, una volta per turno
- Chiamato in `run_turn` DOPO `_memoria_backup_auto`, **FUORI dal `for _ in range(10)`**
  (come pin e backup): nessun impatto sul loop agentico.
- Indicizza solo le righe di diario **NUOVE** oltre il watermark (lettore incrementale
  `MemoryStore.diario_dopo`), in BLOCCO (`VectorStore.index_batch` = una sola chiamata di
  embedding), BOUNDED a `VEC_CATCHUP_MAX` per turno → niente picchi dopo lunghe pause,
  l'arretrato si recupera in più turni. Avanza il watermark **solo se l'index riesce**.
- Fail-safe §9: vector store assente/degradato o memoria assente → no-op, turno prosegue.

### 3. `_ricorda(query)` — cascata NON regressiva + snippet datato
- **FTS5 (base)**: `cerca_diario` resta l'autorità lessicale → **comportamento odierno
  preservato**, mai soppresso.
- **Semantico (riempie)**: solo se FTS non satura `n` e il layer è attivo, `vectors.search`
  aggiunge gli hit per SIGNIFICATO che FTS ha mancato, deduplicati per id, fino a `n`.
- **Substring (pavimento)**: ultimo fallback se tutto il resto è vuoto (invariato).
- **Snippet `_fmt_evento_datato`**: ogni evento mostra il `ts` SORGENTE e, se legato a un
  lead (`contatto_id`), lo **stato CORRENTE** del lead letto LIVE dalla rubrica (non
  denormalizzato nel sidecar). "La memoria non mente" anche in lettura: il ricordo è un
  evento passato datato, ma chi legge vede se è ancora valido.

### 4. Supporto in `store.py` / `vectors.py`
- `MemoryStore.diario_dopo(after_id, limit)` e `get_diario(id)` — **SOLA LETTURA**
  (immutabilità append-only del diario intatta).
- `VectorStore.index_batch(items)` (embedding in blocco) e `max_source_ref(source)`
  (watermark).

---

## DECISIONE DI DESIGN — deviazione ONESTA dal §FINALE (motivata da misura dal vivo)

Il §FINALE della fetta 1 proponeva "semantico PRIMA, poi FTS". **Misurando dal vivo** la
qualità del MiniLM su query corte italiane ho trovato che NON separa in modo affidabile:

```
query 'preventivo':  'telefonata di vendita' 0.33 | 'caffè al bar' 0.288 |
                     'offerta commerciale ad Anna' 0.237   ← il pertinente PERDE col rumore
query 'animale domestico':  'gatto dorme' 0.148  ← praticamente pari al rumore
query 'vendita':     'telefonata di vendita' 0.562  ← qui invece separa bene
```

Mettere il semantico PRIMA di FTS avrebbe **REGREDITO** la precisione: il rumore semantico
(es. 'caffè' per 'preventivo') avrebbe soppresso i match lessicali esatti di FTS. Ho quindi
**invertito** la cascata: **FTS resta l'autorità** (precisione, comportamento collaudato),
il **semantico RIEMPIE** solo i posti liberi (recall additivo per significato), mai
sopprimendo. Soglia `VEC_MIN_SIM=0.30` conservativa. È la scelta giusta per "robustezza >
potenza": un layer nuovo non deve mai peggiorare ciò che già funziona. Riserva R-wire-1
(soglia da rendere env-config e ri-tarare sul corpus reale); R-wire-2 (qualità MiniLM
limitata = limite di POTENZA del modello forzato dall'assenza di e5-small + RAM VPS).

---

## VERIFICHE (dal vivo)

### A. Suite
`python tests/test_unit_kernel.py` → **`152 PASS, 0 FAIL`** (era 145). Nuovi T31a-g:
catch-up (indicizza/watermark/idempotenza), catch-up bounded a scaglioni, snippet datato +
stato corrente del lead, semantico che RIEMPIE quando FTS è assente, fail-safe del layer
degradato (catch-up no-op + ricorda non crasha), default OFF (vectors None), gate env lazy.

### B. End-to-end REALE (modello vero, `GAS_VECTORS=1`)
Seed: lead Anna ('interessato') + evento "ho mandato l'offerta commerciale ad Anna" + un
distrattore. Query **'vendita'** (che FTS NON matcha lessicalmente) → recuperata per
SIGNIFICATO:
```
Diario per 'vendita' (1):
- [2026-06-18] ho mandato l'offerta commerciale ad Anna — lead Anna: oggi 'interessato'
```
Conferma: catch-up reale (2 indicizzati, watermark 2), recall semantico + snippet datato +
stato lead live. (Onestà: per query corte/astratte il MiniLM a volte non aggancia il
pertinente — R-wire-2; il fallback FTS/substring resta sempre il pavimento.)

### C. `git diff --cached --stat` (commit motore)
```
 gas.py                    | 122 ++++++++++++++++++++++-
 modules/memory/store.py   |  30 ++++++
 modules/memory/vectors.py |  46 ++++++++
 tests/test_unit_kernel.py | 113 +++++++++++++++++
```
Invarianti motore (`_get_window`/`_cap_window_chars`/`for _ in range(10)`/sandbox/snapshot/
pin always-on) INTATTE. Con GAS_VECTORS spento il ramo semantico è gated da
`vectors is not None and available` → comportamento bit-identico.

---

## PROCESSO
- **Gate di review §3**: diff su `gas.py`+`modules/`+`tests/` → subagent **revisore** sul
  diff staged PRIMA del commit → **APPROVATO CON RISERVE** (review #24). Verifiche del
  revisore: invarianti motore intatte, default-OFF bit-identico, immutabilità diario,
  bontà della deviazione di design. Riserve **R-wire-1..4** (minori) tracciate in
  `stato_progetto.md`; nessuna è di sicurezza, quindi tracciate (non chiuse in sessione).
- `stato_progetto.md` e `diff_sessione.md` aggiornati; `memoria_revisore.md` aggiornata dal
  revisore (2 lezioni nuove datate 2026-06-18).

---

## COME USARLO / ABILITARLO
- **Acceso:** `export GAS_VECTORS=1` (default OFF). Tetti: `GAS_VECTORS_CATCHUP_MAX`
  (righe/turno). Sidecar `<root>/.gas_vectors.db` (gitignorato, cache ricostruibile).
- **VPS:** prima di accendere, pre-provisionare i pesi del modello (R-vec-3) e verificare
  la wheel onnxruntime ARM + la RAM. Con GAS_VECTORS spento Gas funziona identico, senza il
  modello.

## §FINALE — Cosa resta fuori (PROPOSTE, non fatte)
1. **`gas reindex` umano**: un comando CLI che chiami `VectorStore.ricostruisci_da_diario`
   (già esposto, motore pronto) per un rebuild completo dell'indice — utile dopo un cambio
   di modello o un sospetto di indice incoerente. Operazione manuale/umana, non autopilot.
2. **R-wire-1**: `GAS_VECTORS_MIN_SIM` configurabile via env + ri-taratura della soglia sul
   primo diario reale del VPS (oggi 0.30 da pochi esempi sintetici).
3. **R-wire-2 / R-vec-3**: rivalutare un modello e5 (qualità semantica migliore) quando si
   scioglie il nodo RAM del VPS — la qualità del retrieval per significato è oggi limitata
   dal MiniLM, scelto per vincoli di disponibilità/RAM, non per qualità.
