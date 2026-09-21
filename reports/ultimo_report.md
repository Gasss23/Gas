# SONDA — Autonomia GAS, Capacità #1 "Studia/Comprendi"
> Task: sonda architetturale + piano a fette (NO codice)
> Data: 2026-09-21
> Branch: sonda/autonomia-studia-cap1

---

## 1. STATO ATTUALE DEL SOTTOSISTEMA MEMORIA/CONOSCENZA

### 1.1 `.gas_memory.db` — diario e contatti

**Schema (tabelle principali):**
- `diario` (id, ts, tipo, descrizione, contatto_id): log eventi append-only. 20 righe reali al momento della sonda (tutte chiamate `calcola` da test). Campo `tipo` = nome del tool; `descrizione` = argomenti + risultato compatti.
- `diario_fts` + tabelle accessorie: indice FTS5 su (descrizione, tipo) — "Strato A" del retrieval testuale.
- `contatti` (id, chiave, chiave_norm, nome, contatto, stato, ...): rubrica CRM mutabile. 0 righe al momento della sonda.

**Quando e come si scrive:**
- `_diario_log(tipo, descrizione)` in `gas.py:1115` — chiamato da `execute_tool_call` una volta per ogni tool call completata all'interno del loop `run_turn`.
- Scrittura in-process, codice fidato del kernel, bypassa correttamente il sandbox bwrap (che vale solo per `run_command`).
- Il diario è **IMMUTABILE**: solo append, nessuna modifica/cancellazione di righe esistenti.

**Accesso in lettura:**
- `_memoria_pin()` (gas.py:1199): inietta un blocco always-on nel messaggio system a ogni turno (lead attivi + eventi significativi filtrati). Non passa da `_get_window`.
- Tool `ricorda` (gas.py:1280): sola lettura on-demand. Prima FTS5 (`cerca_diario`), poi opzionalmente ricerca semantica su vettori (Strato B), poi fallback a `diario_recente`.

### 1.2 `.gas_vectors.db` — sidecar vettoriale

**Stato attuale: il file NON ESISTE** (non ancora creato su questa macchina).

**Architettura implementata (ma non ancora attiva per default):**
- Modulo `modules/memory/vectors.py` — standalone, additive, completamente implementato.
- **Opt-in**: attivato solo se env `GAS_VECTORS=1` è settata. Senza di essa il layer non si inizializza e GAS gira identico.
- Schema tabella `vettori`: `(id, source, source_ref, testo, ts, vettore, dim, model, UNIQUE(source, source_ref, model))`. I campi `source`/`source_ref` sono **generici**: in v1 si usa solo `source='diario'`, ma il design è già aperto a source futuri senza migrazione dello schema.
- Embedding: `paraphrase-multilingual-MiniLM-L12-v2` (384-dim, fastembed locale, multilingue, regge l'italiano). Pesi scaricati da HuggingFace al primo uso.
- Ricerca: brute-force cosine (dot product su vettori normalizzati) — sotto 10ms per le dimensioni attuali.
- Fingerprint-guard: mismatch modello/dim/versione fastembed → layer disabilitato, turno prosegue (fail-safe §9).

**Come si (ri)costruisce il sidecar:**
- `ricostruisci_da_diario()` (vectors.py:391): svuota tutti i vettori `source='diario'` e re-indicizza da zero dal diario, in batch paginati (`REINDEX_BATCH_SIZE=256`). Atomic swap: accumula prima, poi in una transazione svuota+reinserisce. Un fallimento batch → None, l'indice vecchio resta intatto.
- `_vec_catchup` (gas.py:1157): catch-up incrementale, eseguito una volta per turno al max `VEC_CATCHUP_MAX=64` righe nuove oltre il watermark (`_vec_watermark`). Pigro e bounded: non è un rebuild, solo l'arretrato.

### 1.3 Esiste già un percorso di ingest esterno o RAG?

**No.** Allo stato attuale:
- Non esiste nessun tool, CLI, script o modulo per ingerire materiale esterno (PDF, URL, file di testo, RSS).
- Non esiste una tabella `knowledge` né una lista di "fonti fidate".
- Il solo `source` presente (e cablato) è `'diario'`.
- Il tool `ricorda` cerca esclusivamente nel diario.
- La `gas CLI` espone `gas reindex` (rebuild vettori dal diario), `gas calibrate-vectors`, `gas eval-vectors` — tutti orientati al solo diario runtime.

Il **sidecar vettoriale è l'unico layer semi-pronto** per un'espansione: il suo schema generica `source`/`source_ref` è il punto di aggancio naturale.

---

## 2. PUNTO DI INNESTO

Il punto di innesto per la capacità "studia da fonte fidata → arricchisci la conoscenza" è:

> **Una nuova `source='knowledge'` nel sidecar vettoriale `.gas_vectors.db`, alimentata da un ingestor OFF-LOOP completamente separato dal motore runtime.**

**Cosa NON toccare (stop gate architetturali):**
- `gas.py` / `run_turn` / `execute_tool_call`: nessuna modifica al loop.
- `_diario_log`: il diario resta esclusivamente runtime.
- La tabella `diario` in `.gas_memory.db`: il diario è immutabile e non va mescolato con la conoscenza deliberata.
- `_memoria_pin`: nessuna modifica all'iniezione sempre attiva.

**Cosa si può toccare senza rischio:**
- `.gas_vectors.db` (sidecar): aggiungere `source='knowledge'` è un'operazione di sola scrittura sullo schema già predisposto.
- Il tool `ricorda`: la ricerca vettoriale accetta già un parametro `source` opzionale. Estenderlo per includere `source='knowledge'` è un'aggiunta lato lettura, non tocca il loop.

---

## 3. PIANO A FETTE (PROPOSTE A PAROLE, ZERO CODICE)

### Fetta K0 — Lista fonti approvate (il "catalogo delle verità autorizzate")

**Dove vive:** file `knowledge/sources.yaml` versionato in git. Solo un commit umano può aggiungere/rimuovere/modificare una fonte. Il file è la **fonte unica di autorità** su cosa Gas è autorizzato a studiare.

**Schema logico di ogni entry:**
- `nome`: identificativo stabile della fonte (slug, usato come `source_name`).
- `tipo`: `url | file | rss` (v1: solo `url` e `file`).
- `uri`: URL o path relativo al repo.
- `descrizione`: testo leggibile per l'operatore.
- `approvata_il`: data ISO dell'approvazione umana.
- `chunk_max`: limite massimo di chunk ingeribili da questa fonte (protezione anti-crescita).
- `attiva`: bool — le fonti disattivate non vengono re-ingerite ma i loro vettori non vengono cancellati automaticamente (cancellazione esplicita umana).

### Fetta K1 — Tabella `knowledge` in `.gas_memory.db`

**Perché in `.gas_memory.db` e non in un DB separato:** mantiene un solo punto di backup, il pattern del repo è già "un DB sacro + un sidecar vettoriale ricostruibile". La `knowledge` è dati deliberati (non runtime), ma è comunque memoria — appartiene al DB sacro insieme ai contatti.

**Schema logico:**
- `id`: PK autoincrement.
- `source_name`: slug dalla sources.yaml (FK logica, non vincolata per semplicità).
- `chunk_ref`: identificatore stabile del chunk all'interno della fonte (es. `chunk_0042`). Con source_name forma la chiave naturale UNIQUE.
- `testo`: testo grezzo del chunk.
- `ts_ingested`: timestamp ISO dell'ingest.
- `ts_source`: timestamp della fonte (data dell'articolo, mtime del file) — "la memoria non mente".
- `hash_contenuto`: SHA-256 del testo. Usato per l'idempotenza: re-ingest dello stesso contenuto → no-op.
- `origine_uri`: URI esatto da cui proviene il chunk.
- `versione`: numero di versione (incrementato a ogni re-ingest con contenuto cambiato).

**Garanzia di reversibilità:** ogni chunk porta `source_name`. Una purge di una fonte è un `DELETE FROM knowledge WHERE source_name = ?` + `DELETE FROM vettori WHERE source = 'knowledge' AND source_ref IN (...)`. Operazione offline, non tocca il diario, non tocca il motore.

### Fetta K2 — CLI di ingest off-loop

**Script:** `tools/ingest_knowledge.py` (non in `gas.py`, non in `modules/`, non chiamato da `run_turn`).

**Flusso logico:**
1. Legge `knowledge/sources.yaml`.
2. Per ogni fonte attiva: scarica/legge il contenuto.
3. Chunking (lunghezza configurabile per fonte, default ~500 token). Ogni chunk ottiene un `chunk_ref` stabile (es. hash del testo originale prima del chunking, o indice ordinale + hash).
4. Calcola `hash_contenuto`. Se già presente in `knowledge` con stesso hash → skip (idempotenza).
5. Inserisce/aggiorna in `knowledge` (upsert su `UNIQUE(source_name, chunk_ref)`).
6. Chiama `VectorStore.index(source='knowledge', source_ref=<id knowledge>, testo=..., ts=<ts_source>)` per ogni chunk nuovo/modificato.
7. Logging esplicito: ogni chunk ingerito/skippato/fallito è loggato con fonte + chunk_ref.

**Script di purge:** `tools/purge_knowledge.py --source <nome>` — elimina da `knowledge` e dal sidecar vettoriale tutti i chunk della fonte specificata. Operazione reversibile se la fonte non è stata modificata (re-ingest ricicrea tutto).

**Separazione dal diario runtime:** l'ingest non chiama `_diario_log`. Non passa da `run_turn`. Non c'è interazione con il loop. È un'operazione da CLI/cron, eseguita offline dall'operatore.

### Fetta K3 — Wiring in `ricorda` (lettura)

**Cosa cambia:** il tool `ricorda` estende la ricerca vettoriale per includere `source='knowledge'` oltre a `source='diario'`.

**Come (a parole):** aggiungere un secondo `VectorStore.search(query, source='knowledge')` in `_ricorda`, poi fondere e de-duplicare i risultati. I risultati knowledge vengono formattati con prefisso `[FONTE: <source_name>]` per distinguerli chiaramente dagli eventi del diario.

**Invariante "la memoria non mente":** i risultati knowledge mostrano `ts_source` (data della fonte originale) non `ts_ingested`. Se la fonte ha data ignota, si mostra `ts_ingested` con prefisso esplicito "ingerito il".

**Stop gate K3:** questa è l'unica fetta che tocca `gas.py`. Va sottoposta a review del revisore prima del commit, come da regola gate CLAUDE.md §3.

### Fetta K4 — Protezioni anti-prompt-injection e anti-crescita

**Prompt injection da fonte fidata:**
- Il testo di ogni chunk viene sanificato pre-ingest: stripping di sequenze HTML/markdown che mimano istruzioni di sistema, wrapping esplicito nel formato `"[FONTE: nome] testo"`.
- Il retrieval in `ricorda` mostra i chunk con il wrapper — il modello vede sempre l'origine. Non vengono mai iniettati nel system prompt senza wrapper.
- Il sanitizer è parte dell'ingestor (K2), non del retrieval (K3): la fonte di verità è già "pulita" a monte.

**Anti-crescita vettori:**
- `chunk_max` per fonte (sources.yaml) — ingestor rifiuta di superarlo.
- `gas doctor` (estensione futura): aggiungere a sezione diagnostica il conteggio `knowledge` per fonte.

---

## 4. RISCHI ED EDGE CASE

### R-K1 — Fonte che cambia contenuto nel tempo
Una URL può cambiare. L'hash non matcha più → re-ingest produce una nuova versione. Senza policy esplicita, le vecchie versioni restano nel sidecar (consumano spazio, possono produrre risultati obsoleti nel retrieval).
**Mitigazione proposta:** campo `versione` in `knowledge`. L'ingestor nella fetta K2 mantiene solo l'ultima versione (DELETE della precedente prima dell'INSERT). Se serve storico: `keep_versions: N` in sources.yaml. Default: keep 1.

### R-K2 — Doppioni inter-fonte
La stessa informazione può arrivare da due fonti diverse (es. due URL con lo stesso articolo). UNIQUE(source_name, chunk_ref) non li elimina perché hanno `source_name` diversi.
**Mitigazione proposta:** al momento nessuna deduplication cross-source (complessità alta, beneficio basso). Il retrieval mostra entrambi i risultati con la propria fonte — l'utente può valutare. Monitorare nel log dell'ingestor.

### R-K3 — Prompt injection da fonte fidata compromessa
Una fonte approvata può essere compromessa nel tempo: l'URL cambia contenuto (redirect, hack del sito), il file locale viene modificato senza commit. Il contenuto iniettato nel contesto può tentare di manipolare il comportamento di Gas.
**Mitigazioni:**
- Il catalogo in git è la prima barriera: solo fonti deliberatamente approvate.
- Il wrapper `[FONTE: nome]` rende visibile al modello l'origine. Non elimina il rischio ma riduce il vettore di attacco.
- Il sanitizer (K4) filtra pattern di istruzione ovvi (system-prompt-like).
- **Rischio residuo:** un testo apparentemente normale può contenere istruzioni latenti. Mitigazione finale: non iniettare chunk direttamente nel system prompt, solo come risposta contestuale a una query esplicita (pattern del tool `ricorda`).

### R-K4 — Crescita incontrollata dei vettori con fonti dinamiche
Se una fonte è un RSS o un feed che cambia ogni giorno, ogni re-ingest aggiunge chunk. Con `keep_versions=1` si sostituisce, ma se il feed ha 100 articoli al giorno il sidecar cresce comunque.
**Mitigazione:** `chunk_max` per fonte in sources.yaml è la protezione primaria. Aggiungere alert nel `gas doctor` (conteggio per source, soglia configurabile).

### R-K5 — Modello embedding offline al primo uso
I pesi di MiniLM devono essere scaricati da HuggingFace al primo `VectorStore.index()`. Se al momento dell'ingest la rete è assente → embedding fail → chunk non indicizzato (fail-safe già implementato in vectors.py).
**Mitigazione:** pre-scaricare i pesi nel provisioning del VPS (già documentato nei report precedenti come requisito). L'ingestor dovrebbe loggare warning esplicito se il vector store è `available=False` e raccomandare il pre-download.

### R-K6 — Conflitto semantico diario vs conoscenza
Il retrieval potrebbe restituire informazioni contraddittorie: un chunk di conoscenza obsoleto che contraddice un evento recente del diario.
**Mitigazione:** nel formato risposta del tool `ricorda`, i risultati `knowledge` vengono mostrati DOPO quelli `diario` (il diario è sempre il dato più recente e specifico). La datazione esplicita (`ts_source` vs `ts` del diario) lascia al modello la valutazione della freschezza.

---

## 5. PROPOSTE FUORI SCOPE CORRENTE (per il report, non da fare ora)

- Interfaccia Telegram per approvare fonti da telefono (richiede modifica bot).
- Scheduling automatico dell'ingest (cron): da valutare dopo K0-K2 stabili.
- FTS5 anche su `knowledge` (oggi solo su `diario`): utile ma non bloccante.
- Versioning dei chunk con storico N versioni: solo se emerge il bisogno reale.

---

## 6. RIEPILOGO DECISIONI UMANE RICHIESTE

Prima di procedere alle fette K0-K3, l'operatore deve decidere:

1. **Dove vive la prima fonte fidata?** Suggerimento: `knowledge/sources.yaml` in git. Alternativa: un file JSON fuori repo. La scelta condiziona la fetta K0.
2. **Granularità chunk:** quanti token per chunk? Default proposto ~500. Dipende dal tipo di fonti (articoli lunghi vs doc tecnica vs FAQ).
3. **Policy versioning:** keep 1 (ultima versione, default proposto) o keep N? Trade-off: spazio vs storico.
4. **Fetta K3 (wiring `ricorda`):** è l'unica che tocca `gas.py`. Va deciso se fare K2 standalone (CLI ma non ancora integrato nel tool `ricorda`) come milestone intermedia, o procedere direttamente a K3 dopo K2.
5. **Attivare `GAS_VECTORS=1`** sul Mac dev prima di iniziare K1/K2 (i test degli script richiedono il sidecar attivo).
