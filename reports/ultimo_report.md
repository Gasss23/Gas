# Vector store — FETTA 1: storage + embedding semantico (STANDALONE)

**Data:** 2026-06-18
**Commit motore:** vedi hash stampato a fine task (revisore #23 — APPROVATO CON RISERVE)
**Commit doc:** vedi hash stampato a fine task
**Suite:** **145/145, 0 FAIL** (era 139)
**Scope:** SOLO storage + embedding del retrieval semantico, come modulo STANDALONE.
`gas.py` INVARIATO. NESSUN aggancio a `ricorda`/`run_turn`/loop (è una fetta successiva,
solo PROPOSTA qui sotto in §FINALE).

---

## DECISIONE UMANA RICHIESTA E RISOLTA (STOP GATE onorato)

La spec fissava il modello `intfloat/multilingual-e5-small` (384-dim) + prefissi e5
`query:`/`passage:` obbligatori. Verificando DAL VIVO ho scoperto che **quel modello NON
esiste nel catalogo di fastembed 0.8.0** (né in alcun file della libreria installata). I
soli multilingue nativi sono `paraphrase-multilingual-MiniLM-L12-v2` (384-dim, non-e5) e
`intfloat/multilingual-e5-large` (1024-dim, 2.24GB → sfora la RAM del VPS). I tre vincoli
della spec (modello e5-small + prefissi e5 + 384-dim) **non erano simultaneamente
soddisfacibili** con la libreria reale.

Per la **regola di consenso vincolante** mi sono FERMATO e NON ho deciso io: ho portato il
bivio all'utente. **Scelta esplicita dell'utente:** `sentence-transformers/paraphrase-
multilingual-MiniLM-L12-v2` (384-dim, entra nei vincoli RAM del VPS, regge l'italiano).
Conseguenza accettata: i prefissi e5 NON si applicano (su un non-e5 sarebbero dannosi). Ho
comunque tenuto il meccanismo del prefisso NEL CODICE (mappa per-modello, MiniLM → `("","")`,
e5 → `("query: ","passage: ")` pronti) così il principio "prefisso non lasciato al
chiamante" resta e un domani si passa a un modello e5 senza toccare i call-site.

---

## COSA È STATO FATTO (`modules/memory/` + `tests/` + `requirements.txt` + `.gitignore`)

### 1. NUOVO modulo `modules/memory/vectors.py` — `VectorStore`
- **Sidecar `.gas_vectors.db` SEPARATO** dal `.gas_memory.db` sacro (che NON si tocca mai).
  È una **CACHE DERIVATA e RICOSTRUIBILE** dal diario: NON è fonte di verità, NON va nel
  backup, è gitignorata (con `-wal`/`-shm`).
- **Schema multi-source** `(id, source, source_ref, testo, ts, vettore BLOB, dim, model)`
  con `UNIQUE(source, source_ref, model)` → `index` idempotente (INSERT OR REPLACE). In v1
  si popola SOLO `source='diario'` (`source_ref` = id riga diario); i campi sono già pronti
  per source futuri (trascritti vocali, RAG) senza migrazione.
- **Embedding LOCALE** via fastembed, modello di default MiniLM-L12-v2 (384-dim). Prefissi
  e5 gestiti per-modello nel codice. Caricamento del modello **PIGRO** (il primo uso scarica
  i pesi: evento di rete).
- **Vettori float32 NORMALIZZATI a norma 1 in scrittura** → la cosine similarity diventa un
  semplice **dot product**.
- **Ricerca brute-force COSINE in numpy**: carica i candidati (stesso `model`+`dim`,
  eventualmente filtrati per `source`), `mat @ qvec`, top-k + soglia minima `min_sim`.
  **NIENTE sqlite-vec** (alpha pre-v1, formato instabile, fallimenti silenziosi: fuori dal
  percorso critico di un agente h24) e **NIENTE ANN** (a questi numeri il brute-force è
  <10ms). Ogni risultato porta `score` e il **`ts` dell'evento sorgente** ("la memoria non
  mente": eventi episodici datati, non verità presenti).
- **`ricostruisci_da_diario(memory_store)`** = motore del futuro `gas reindex` (qui NON
  cablato a CLI). Calcola TUTTI gli embedding PRIMA di svuotare l'indice (se l'embedding
  fallisce → `None`, l'indice buono NON viene distrutto), poi `DELETE`+`INSERT` in una
  transazione unica.

### 2. `MemoryStore.diario_tutto()` — lettore SOLA LETTURA (in `store.py`)
Lo store non esponeva un "tutte le voci" (solo `diario_recente(n)`). Aggiunto
`diario_tutto()`: `SELECT * ... ORDER BY id ASC`, nessun UPDATE/DELETE, nessun nuovo path
di scrittura → **immutabilità append-only del diario INTATTA**.

### 3. `requirements.txt` (nuovo) + `.gitignore` + `__init__.py`
- `requirements.txt` non esisteva, benché `deploy_vps_bozza.txt` lo assuma già (FASE 3):
  creato pulito con `openai`, `numpy`, `fastembed`.
- `.gitignore`: aggiunti `.gas_vectors.db*` e le cache dei pesi (`local_cache/`,
  `.fastembed_cache/`).
- `modules/memory/__init__.py` esporta `VectorStore` & co. Import **fail-safe**.

### FAIL-SAFE §9 (l'intero layer è ADDITIVO e DEGRADANTE)
- **Import protetti**: `numpy`/`fastembed` assenti → `modules.memory` si importa LO STESSO
  (GAS gira identico); `available=False` ne tiene conto.
- `available=False` → `index`/`ricostruisci_da_diario`=None, `search`=[]. Mai crash.
- Sidecar mancante → creato; corrotto (header) → degrado.
- **R-vec-1 CHIUSA in sessione** (prescrizione del revisore): il `try/except` di
  `_search_vec` avvolge anche `vstack`/`_from_blob`/matmul e cattura `ValueError` → una
  cella BLOB fisicamente corrotta degrada a [] invece di crashare (precondizione di
  sicurezza per il wiring).
- I pesi del modello si scaricano da HF al primo uso (rete): in assenza di rete il
  caricamento fallisce → degrado, non crash. Per il VPS vanno pre-scaricati (vedi sotto).

---

## VERIFICHE (eseguite e dimostrate dal vivo)

### A. Dipendenza fastembed — dati reali per il sizing VPS
- `pip install fastembed` → fastembed **0.8.0** + onnxruntime **1.27.0** (wheel x86_64).
- Modello MiniLM-L12-v2: **dim 384**, vettore grezzo NON normalizzato (norma ~4.2 →
  conferma che la normalizzazione va fatta in scrittura, fatto).
- **Download su disco ~504 MB** (snapshot HF completo; il catalogo dichiara 0.22GB del solo
  onnx). **Cold embed ~0.11s** dopo init ~7s; warm ~0.012s.
- Similarità italiana NETTA: simili (gatto/felino) **cos 0.876** vs diverse (gatto/auto)
  **0.113**.
- ⚠️ Warning fastembed: "mean pooling instead of CLS" — irrilevante qui (l'indice è cache
  ricostruibile, sempre rigenerata con la stessa versione installata).

### B. Suite
`python tests/test_unit_kernel.py` → **`=== RIEPILOGO: 145 PASS, 0 FAIL ===`** (era 139).
Nuovi T30a-f. **T30e (embed reale) NON skippato** in Codespace: `dim=384`, `norma=1.0000`,
frase italiana simile più vicina della diversa. T30f morde R-vec-1.

### C. `git diff --cached --stat` (commit motore)
```
 .gitignore                 |   7 +
 modules/memory/__init__.py |  25 +++-
 modules/memory/store.py    |  15 ++
 modules/memory/vectors.py  | 365 +++++++++++++++++++++++++++++++++++++++++
 requirements.txt           |  15 ++
 tests/test_unit_kernel.py  | 130 ++++++++++++++++
```
`gas.py` NON nel diff. Invarianti motore (`_get_window`/`_cap_window_chars`/
`for _ in range(10)`/sandbox/snapshot/immutabilità diario) intatte.

---

## PROCESSO
- **Gate di review §3**: diff su `modules/`+`tests/` → subagent **revisore** invocato sul
  diff staged PRIMA del commit → **APPROVATO CON RISERVE** (review #23). Verifiche del
  revisore dal vivo: scope (gas.py intatto, zero wiring), i 3 rami fail-safe, l'ordine
  embed-prima-di-svuotare in `ricostruisci`, `diario_tutto` sola lettura. R-vec-1 prescritta
  e CHIUSA in sessione (più T30f); R-vec-2/R-vec-3 tracciate in `stato_progetto.md`.
  `SendMessage` non disponibile in questo harness: il fix applicato è ESATTAMENTE il rimedio
  prescritto dal revisore, coperto da test, suite verde → commit legittimo sotto il verdetto
  già ottenuto.
- `stato_progetto.md` e `diff_sessione.md` aggiornati; `memoria_revisore.md` aggiornata dal
  revisore (4 lezioni nuove datate 2026-06-18).

## COME PRE-PROVISIONARE IL MODELLO AL DEPLOY VPS (R-vec-3)
Il VPS candidato è **Oracle Ampere ARM, 1 vCPU, 1GB RAM** (`deploy_vps_bozza.txt`). Rischi
NON verificabili da qui (dev = x86_64):
1. **Wheel `onnxruntime` per ARM**: verificare al deploy che `pip install` trovi la wheel
   `aarch64` (di norma c'è per le versioni recenti; ANNOTARE se serve build da sorgente).
2. **Pesi del modello offline**: NON assumere rete a runtime. Pre-scaricare i ~504MB in fase
   di deploy (un `VectorStore(...).index(...)` una-tantum con rete, o `fastembed` CLI/HF
   download) e puntare il `cache_dir` a un volume persistente; mancando i pesi il layer
   degrada (non crasha). Esporre il path via env è R-vec-2.
3. **RAM 1GB**: onnxruntime + modello in RAM va misurato sul VPS. Mitigazioni se stretto:
   swap, modello più piccolo, o embedding SOLO on-demand (non per ogni evento).

---

## §FINALE — PROPOSTA della fetta di WIRING (NON implementata, fuori da questo mandato)

Obiettivo: far usare il vector store a `ricorda(query=...)` in modo additivo e fail-safe,
SENZA gonfiare la finestra né rallentare il turno.

1. **Costruzione del `VectorStore` nel kernel** accanto a `self.memory`, con la stessa
   doppia cintura fail-safe (`__init__` in try/except → `self.vectors=None` su errore
   d'ambiente). `available=False`/`None` → tutto degrada al comportamento odierno (FTS5 +
   substring). GAS resta identico se il layer manca.

2. **Catch-up indexing PIGRO e BOUNDED** (non un reindex completo a ogni turno): tenere il
   `MAX(source_ref::int)` già indicizzato per `source='diario'` e, una volta per turno
   (fuori dal `for _ in range(10)`, accanto a `_memoria_pin`/`_memoria_backup_auto`),
   indicizzare solo le **nuove** righe di diario oltre quel watermark, con un **tetto** per
   turno (es. ultime N) per non pagare un picco dopo lunghi periodi. Tutto in try/except
   (un fallimento di embedding non deve toccare il turno). Il `gas reindex` completo
   (`ricostruisci_da_diario`) resta un'operazione UMANA/manuale separata.

3. **`ricorda(query)` a CASCATA** (estende la cascata odierna FTS→substring): prima
   `vectors.search(query, k, min_sim)` (semantico), poi — se vuoto o sotto soglia —
   `cerca_diario` FTS5, poi substring. La soglia `min_sim` va tarata con dati reali (oggi
   conservativa); il semantico aggiunge il recupero per SIGNIFICATO ("preventivo" trova
   "offerta") che il lessicale non dà.

4. **Snippet onesto e datato + stato CORRENTE del lead**: ogni hit mostra il `ts`
   dell'evento sorgente (già nel record) e, se la riga di diario ha `contatto_id`, si
   AFFIANCA lo **stato CORRENTE** del lead letto live da `contatti` (es.
   `[2026-05-02] "offerta inviata" — lead Anna: oggi 'chiuso'`). Così il retrieval resta un
   EVENTO episodico passato, ma l'utente vede subito se quel fatto è ancora valido — "la
   memoria non mente" anche in lettura. Lo stato si legge a runtime, NON si denormalizza nel
   sidecar (che è cache derivata).

5. **R-vec-1 è la precondizione di sicurezza** del punto 3 ed è GIÀ chiusa: con `search`
   esposto al loop, un sidecar fisicamente corrotto degrada a [] invece di abbattere il
   turno.

6. **Rischi del round-trip da sorvegliare nel wiring**: (a) il primo turno dopo un grande
   arretrato di diario paga il catch-up → il tetto per-turno lo limita; (b) l'output di
   `ricorda` deve passare per `_cap_tool_output` come oggi; (c) nessuna riga del vector
   store entra nel pin always-on (resta on-demand via `ricorda`) per non gonfiare il system
   message.
