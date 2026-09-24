# Sonda: auto-apprendimento — ricognizione stato attuale

**Branch:** sonda/auto-apprendimento-recon  
**Data:** 2026-09-23  
**Metodo:** lettura codice + ispezione COPIA del db (mai l'originale)  

---

## 1. MEMORIA — dove e come GAS salva i ricordi

### File e schema

| File | Descrizione | Esistente? |
|------|-------------|-----------|
| `.gas_memory.db` | SQLite, dati di lungo periodo | SÌ (53 KB) |
| `.gas_vectors.db` | Sidecar vettoriale, cache derivata | NO (opt-in via `GAS_VECTORS`) |

Schema verificato su copia (`sqlite3 /private/tmp/gas_memory_sonda.db`):

**Tabella `diario`** (`store.py:68-94`):
```
id          INTEGER PK AUTOINCREMENT
ts          TEXT NOT NULL  (ISO8601 UTC)
tipo        TEXT NOT NULL  (nome del tool: "calcola", "read_file", ecc.)
descrizione TEXT NOT NULL  (args+esito sintetico, es. "expr='3+3' | [OK] 6")
contatto_id INTEGER (FK → contatti.id, nullable)
```

**Tabella `contatti`** (`store.py:96-128`):
```
id, chiave (as-entered), chiave_norm (UNIQUE, forma canonica),
nome, contatto, stato (CHECK enum), ultimo_contatto, prossima_azione,
note, creato_il, aggiornato_il, merged_into (FK self-ref, lapide)
```

**Tabella `vettori`** (`.gas_vectors.db`, `vectors.py:110-134`):
```
source ('diario' in v1), source_ref (id riga diario), testo, ts,
vettore (BLOB float32 normalizzato L2), dim (384), model
```

### Chi scrive, quando

- Il kernel scrive nel diario **dopo ogni tool call** dentro `run_turn` (`gas.py:1662-1665`), sia OK che KO.
- Formato della riga: `"<args_sintetico> | [OK|KO] <output[:160]>"`.
- Tool che scrivono nella rubrica (`contatti`): `salva_contatto` (upsert) e `imposta_stato_contatto` (transizione stato).
- La rubrica è mutabile (UPDATE), il diario è immutabile (solo INSERT, protetto da trigger `BEFORE UPDATE/DELETE` in `store.py:82-93`).

### Campo fonte/confidenza

**NON ESISTE.** Il diario non ha un campo `fonte` (es. "utente", "LLM", "tool") né un campo `confidenza`. Ogni riga sa solo il `tipo` (nome del tool) e il `ts`. Non c'è distinzione fra un fatto osservato da un tool reale e uno scritto da un LLM allucinante.

### Correggere un ricordo

- **Diario:** impossibile per design; i trigger bloccano UPDATE e DELETE (`store.py:82-93`). Si può solo aggiungere un nuovo evento che smentisce il precedente (nessuna API per farlo esplicitamente).
- **Contatti:** modificabili via `upsert_contatto` (anagrafica) e `update_stato_contatto` (stato). Il merge a lapide (`unisci_contatti`) è operazione umana manuale, non disponibile all'agente (`gas.py:1536-1540`).
- **Vettori:** cache derivata, si ricostruisce con `gas reindex`.

---

## 2. DIARIO — cosa viene scritto a ogni azione

**Formato verificato su dati reali** (db copiato, 20 righe al 2026-09-23):

```
id=20 | tipo="calcola" | descrizione="expr='3+3' | [OK] 6" | ts=2026-09-21T12:04:19
id=19 | tipo="calcola" | descrizione="expr='7*8' | [OK] 56" | ts=2026-09-21T12:02:58
```

Struttura della `descrizione`: prodotta da `_riassumi_args()` + `_esito_sintetico()` (`gas.py:1063-1113`):
- `_riassumi_args`: trunca gli argomenti a ~60-200 char per-tipo.
- `_esito_sintetico`: prefisso `[OK]` o `[KO]`, output troncato a 160 char (`gas.py:1111-1113`).

**Cosa finisce nel diario:** ogni tool call dentro `run_turn` — `read_file`, `write_file`, `run_command`, `calcola`, `ricorda`, `salva_contatto`, `imposta_stato_contatto`.

**Cosa NON finisce nel diario:** i turni senza tool call (solo testo), le risposte finali dell'LLM, i provider falliti (quelli vanno solo in `.gas_tokens.jsonl`).

**Crescita:** append-only, nessuna pulizia/rotazione. I 20 eventi attuali sono tutti `calcola` (da test di sviluppo).

**FTS5:** attivo (`store.py:290-320`). Indice `diario_fts` external-content aggiornato da trigger `AFTER INSERT`.

---

## 3. HISTORY — `.gas_history.json` e compressione FASE 2.5

Verificato: 36 messaggi, 8935 byte (`cat .gas_history.json`).

**Compressione** (`gas.py:566-637`):
- Trigger: `len(history) > HISTORY_MAX_MSGS` (default 100, override env `GAS_HISTORY_MAX_MSGS`).
- Strategia: si tengono gli ultimi 20 messaggi (`HISTORY_KEEP_MSGS`) intatti; i vecchi vengono compressi in un singolo messaggio `role:user` con testo deterministico (niente LLM).
- Formato riepilogo (`gas.py:611-622`): per ogni messaggio `[role] content[:300]` o `[role] chiamate tool: nome1, nome2`.
- Cosa si **perde**: il contenuto degli argomenti e degli output dei tool oltre i 300 caratteri; le sequenze tool_use/tool_result (restano i nomi delle tool call ma non l'output); la struttura multipart dei messaggi assistant con tool_calls.
- Non si perde nulla di ciò che è già nel **diario** (il diario è la fonte duratura; la history è il contesto conversazionale).

---

## 4. RECUPERO — come i ricordi tornano nel prompt

Due canali, verificati in `gas.py`:

### A) Blocco ALWAYS-ON nel system prompt — `_memoria_pin()` (`gas.py:1199-1246`)

- Calcolato **una volta per turno**, prima del loop agentico (`gas.py:1559`).
- Aggiunto a `system_prompt + mem_pin` nel payload (`gas.py:1626`).
- Contenuto: lead attivi (max 8, stati non "rifiutato"/"chiuso") + ultimi 6 eventi significativi dal diario (esclusi `read_file`, `run_command`, `ricorda` — considerati rumore).
- Tetto: 3000 caratteri (`MEMORY_PIN_CHAR_CAP`), troncamento all'ultima riga intera.

### B) Tool `ricorda` — on-demand (`gas.py:1280-1358`)

Cascata di retrieval:
1. **FTS5** (`cerca_diario`) — ricerca per parole/radici ordinata BM25, se `fts_available` (`store.py:727-748`).
2. **Semantico** — `vectors.search()` con `min_sim=0.30` (`gas.py:1326-1343`), solo se `GAS_VECTORS` attivo e ci sono posti liberi fino a `n`. Risolve `source_ref` → riga diario completa.
3. **Substring** — fallback storico: `diario_recente(200)` con `q in descrizione.lower()` (`gas.py:1344-1348`).

Quanti risultati: default `n=10`, max 50 (`gas.py:1289`).

---

## 5. ESITI — GAS registra successi e fallimenti?

### Tool call (OK/KO)
Sì: `_esito_sintetico()` produce `[OK]` o `[KO]` in base al prefisso dell'output (`gas.py:1107-1113`). Sia i successi che gli errori di tool finiscono nel diario.

### Fallback provider
Sì, nel file `.gas_tokens.jsonl` (verificato, 24 righe): ogni fallthrough ha `"event":"fallthrough"` + `"reason":"KO|QUOTA|WARN"` (`gas.py:1692-1693`). Il log esiste, è leggibile.

### Non registrato nel diario:
- I fallback provider (solo `.gas_tokens.jsonl`).
- Le risposte finali LLM e la loro qualità.
- Se un compito dell'utente è stato completato con successo end-to-end.
- La classificazione del compito (`semplice`/`complesso`, `gas.py:1601-1611`) — non viene tracciata in memoria.

**Conclusione:** il diario è la materia prima per "errori di tool", non per "esiti di task". Un sistema di auto-apprendimento dovrebbe aggiungere un campo o un tipo di evento dedicato all'esito del turno completo.

---

## 6. TOOL che scrivono memoria — operazioni irreversibili

| Tool | Accessibile all'agente | Scrittura | Irreversibile? |
|------|------------------------|-----------|----------------|
| `ricorda` | SÌ | No (solo lettura) | — |
| `salva_contatto` | SÌ | Upsert rubrica + riga diario | Sì (diario append-only; rubrica sovrascrive) |
| `imposta_stato_contatto` | SÌ | UPDATE stato contatto + riga diario | Sì (stato precedente non registrato prima del cambio) |
| `write_file` | SÌ (con snapshot) | Filesystem + riga diario | No (snapshot pre-scrittura via git ref) |
| `run_command` | SÌ (sandboxed) | Filesystem/SO + riga diario | Dipende dal comando |
| `calcola` | SÌ | Solo riga diario | No (solo log) |
| `unisci_contatti` | NO (operazione umana) | Merge a lapide rubrica + snapshot diario | Lossy (COALESCE) — documentato `gas.py:1412-1415` |
| `append_diario` | NO (solo kernel interno) | INSERT diario | Sì (immutabile by design) |

**Nota critica:** `salva_contatto` non registra nel diario cosa c'era prima dell'upsert. Se l'agente sovrascrive `prossima_azione` o `note` di un lead, il valore precedente è perso (COALESCE scrive solo i campi `NOT NULL`; ma se si passa un valore diverso, il precedente scompare senza traccia nel diario).

---

## 7. RISCHI per un sistema che impara da solo

### R1 — Memoria inquinata da LLM allucinante
Il diario registra l'output di tool reali (kernel scrive), ma `descrizione` contiene gli argomenti passati dall'LLM (`_riassumi_args`). Un LLM potrebbe passare argomenti falsi a `salva_contatto` (nome/note inventati) e il kernel li persiste senza validazione semantica. **Non c'è un campo "fonte" o "confidenza"** che distingua un fatto reale da un'allucinazione dell'LLM.

### R2 — Prompt injection nei ricordi
Un utente malintenzionato potrebbe passare testo come chiave/note di un contatto contenente istruzioni (es. `"nota: ignora le istruzioni precedenti e..."`) che, iniettato nel `_memoria_pin()` o nell'output di `ricorda`, viene interpretato dall'LLM nel turno successivo come istruzione. **Nessuna sanitizzazione del testo estratto dalla memoria prima dell'iniezione nel prompt** (verificato: `_memoria_pin` fa `.get('prossima_azione')` diretto, `gas.py:1221-1222`).

### R3 — Crescita senza limite del diario
Il diario è append-only, senza retention/pulizia. Ogni tool call aggiunge una riga. Su un agente h24 con 100 tool call/giorno → 36.500 righe/anno. Il retrieval FTS e substring scalano, ma il full-scan in `diario_recente(200)` diventa meno rappresentativo nel tempo. Nessun meccanismo di summarizzazione/archiviazione del diario esiste attualmente.

### R4 — Ricordi falsi per errore di tool
Un tool che fallisce (`[KO]`) lascia una riga nel diario con l'errore. Il retrieval può riportare errori passati come eventi significativi, senza che il sistema sappia se il problema è stato poi risolto. Non c'è correlazione tra un evento KO e un eventuale KO-superato successivo.

### R5 — Diario non a prova di `INSERT OR REPLACE`
Documentato come CAVEAT in `store.py:15-17`: con `recursive_triggers = OFF` (default SQLite), un `INSERT OR REPLACE` diretto sulla PK aggirerebbe i trigger di immutabilità. Il codice applicativo usa INSERT puro, ma l'accesso diretto al file `.db` è un vettore. Da blindare (menzione esplicita nel codice).

### R6 — Classificazione compito non memorizzata
La classificazione `semplice`/`complesso` decide quale cascade di provider usare (`gas.py:1601-1611`). Non è tracciata in memoria: non si può imparare retrospettivamente "questo tipo di query richiede il brain più potente".

---

## Opzioni per un sistema di auto-apprendimento

**Opzione A — Lezioni esplicite nel diario (minimo intervento)**  
Aggiungere un tipo `"lezione"` al diario: il kernel (o l'agente) scrive una riga `tipo="lezione"` dopo ogni turno completato, con esito globale e osservazione breve. Zero migrazione schema. Il `_memoria_pin` può filtrare e prioritizzare le lezioni. Limite: dipende dalla qualità del testo che l'LLM produce; nessuna struttura machine-readable.

**Opzione B — Campo esito nel diario + ragionamento post-turno (struttura media)**  
Aggiungere colonna `esito` (TEXT nullable: "ok"/"ko"/"parziale") e `turno_id` (UUID) al diario; scrivere una riga `tipo="turno_fine"` con esito aggregato dopo ogni `run_turn`. Il retrieval può filtrare per `esito=ko` per trovare i fallimenti. Richiede migrazione schema (`_ensure_columns`). Struttura machine-readable per analisi.

**Opzione C — Diario strutturato + watermark di apprendimento (massimo, FASE 3)**  
Tabella separata `lezioni` (`tipo`, `contesto`, `azione`, `esito`, `ts`), popolata da un LLM "riflessivo" che a fine sessione analizza il diario del turno e estrae 1-3 lezioni strutturate. Le lezioni entrano nel `_memoria_pin` con priorità alta. Richiede un secondo turno LLM per riflessione (costo token). Massima qualità, massima complessità.
