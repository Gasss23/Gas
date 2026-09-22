# Autonomia GAS — Capacità #1 "Studia/Comprendi" — K0+K1+K2
> Task: prima fetta di codice (knowledge store + CLI ingest off-loop)
> Data: 2026-09-22
> Branch: sonda/autonomia-studia-cap1

---

## DECISIONI ARCHITETTURALI APPLICATE

**Decisione capo-eng (vincolante):** la knowledge base va in un file SEPARATO
`.gas_knowledge.db`. NON si scrive mai in `.gas_memory.db`. Il diario è intoccabile.

Questa decisione diverge dal piano K1 originale della sonda (che prevedeva la tabella
`knowledge` dentro `.gas_memory.db`). La ragione è l'isolamento totale tra memoria
runtime (diario, contatti) e conoscenza deliberata.

---

## FILE CREATI / MODIFICATI

| File | Tipo | Descrizione |
|------|------|-------------|
| `knowledge/sources.yaml` | **nuovo** (K0) | Catalogo fonti fidate — fonte unica di autorità |
| `knowledge/test_source.txt` | **nuovo** (K0) | Fonte test locale per validare il pipeline |
| `tools/ingest_knowledge.py` | **nuovo** (K1+K2) | CLI off-loop: schema DB + ingest idempotente |
| `.gitignore` | modificato | Aggiunta esclusione `.gas_knowledge.db` + WAL/SHM |
| `requirements.txt` | modificato | Aggiunta `pyyaml>=6.0` (già installata nel .venv) |

**File NON toccati:** `gas.py`, `brains/`, `modules/`, `tests/`, `.gas_memory.db`.

---

## K0 — `knowledge/sources.yaml`

Catalogo YAML versionato in git. Una sola fonte di test per ora.

```yaml
sources:
  - nome: test_local
    tipo: file
    uri: knowledge/test_source.txt
    descrizione: "Fonte di test locale per validare il pipeline K0-K2"
    approvata_il: "2026-09-22"
    chunk_max: 10
    attiva: true
```

Campi per entry: `nome` (slug/source_name), `tipo` (file|url), `uri`, `descrizione`,
`approvata_il`, `chunk_max`, `attiva`.

---

## K1 — Schema `.gas_knowledge.db`

Nuovo DB SQLite separato. Schema:

```sql
CREATE TABLE knowledge (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name    TEXT    NOT NULL,
    chunk_ref      TEXT    NOT NULL,         -- es. "chunk_0001"
    testo          TEXT    NOT NULL,
    hash_contenuto TEXT    NOT NULL,         -- SHA-256 del testo
    ts_source      TEXT,                     -- mtime/data fonte originale
    ts_ingested    TEXT    NOT NULL,
    origine_uri    TEXT,
    versione       INTEGER NOT NULL DEFAULT 1,
    stato          TEXT    NOT NULL DEFAULT 'active'  -- 'active'|'superseded'
);
-- Partial unique index: al massimo un record 'active' per (source_name, chunk_ref)
CREATE UNIQUE INDEX idx_knowledge_active
    ON knowledge(source_name, chunk_ref) WHERE stato = 'active';
```

Il vincolo UNIQUE(source_name, chunk_ref) è implementato come **partial unique index**
su `stato = 'active'`: permette di mantenere più versioni storiche (stato='superseded')
per la stessa chiave logica, soddisfacendo il requisito "vecchia versione MAI cancellata".

---

## K2 — `tools/ingest_knowledge.py`

CLI standalone off-loop. Flusso:

1. Legge `knowledge/sources.yaml`
2. Per ogni fonte `attiva: true` di tipo `file`: legge il file, calcola `ts_source` dal mtime
3. Chunking per capoversi (~1800 char ≈ 500 token): `chunk_text()`
4. Per ogni chunk: calcola SHA-256, controlla se esiste già un record `active` con stesso hash
   - Stesso hash → **skip** (idempotenza)
   - Hash diverso → UPDATE vecchio a `stato='superseded'`, INSERT nuovo con `versione+1`
   - Non esiste → INSERT con `versione=1`
5. `conn.commit()` al termine di ogni fonte
6. Logging INFO per ogni chunk ingerito/superseded, DEBUG per ogni skip

```
python tools/ingest_knowledge.py [--source NOME] [--dry-run] [--db PATH] [--verbose]
```

---

## TEST REALI (mai simulati)

### Test 1 — Primo ingest

```
$ python tools/ingest_knowledge.py
2026-09-22T21:14:13 [INFO] Fonti attive da processare: 1
2026-09-22T21:14:13 [INFO] DB: /Users/gas/Gas/.gas_knowledge.db
2026-09-22T21:14:13 [INFO] [test_local] chunk_0000 v1 ingerito (1505 chars)
2026-09-22T21:14:13 [INFO] [test_local] chunk_0001 v1 ingerito (314 chars)
2026-09-22T21:14:13 [INFO] [test_local] completato — ingested=2 skipped=0 superseded=0
2026-09-22T21:14:13 [INFO] === TOTALE: ingested=2  skipped=0 ===
```

**Righe scritte in `.gas_knowledge.db`:**

| id | source_name | chunk_ref  | versione | stato  | len  | ts_source                       |
|----|-------------|------------|----------|--------|------|---------------------------------|
|  1 | test_local  | chunk_0000 |        1 | active | 1505 | 2026-09-22T17:13:33.437742+00:00|
|  2 | test_local  | chunk_0001 |        1 | active |  314 | 2026-09-22T17:13:33.437742+00:00|

### Test 2 — Idempotenza (secondo ingest identico)

```
$ python tools/ingest_knowledge.py
2026-09-22T21:14:24 [INFO] Fonti attive da processare: 1
2026-09-22T21:14:24 [INFO] DB: /Users/gas/Gas/.gas_knowledge.db
2026-09-22T21:14:24 [INFO] [test_local] completato — ingested=0 skipped=2 superseded=0
2026-09-22T21:14:24 [INFO] === TOTALE: ingested=0  skipped=2 ===
```

**PASS: ingested=0, skipped=2. Zero doppioni.**

### Test 3 — Isolamento `.gas_memory.db`

```
gas_memory.db mtime PRIMA : 1789992259
gas_memory.db mtime DOPO  : 1789992259
PASS: .gas_memory.db NON modificato
Righe in diario: 20 (invariate)
```

**PASS: `.gas_memory.db` non toccato né in scrittura né in lettura.**

---

## COSA NON È STATO FATTO (scope rispettato)

- **K3** (wiring `ricorda` in gas.py): VIETATO in questo giro — nessuna modifica al motore
- **K4** (protezioni anti-prompt-injection, anti-crescita): rimandato
- Fonti reali (URL, RSS): nessuna aggiunta — solo fonte test locale
- Scheduling/automazione: zero
- VPS: non toccato

---

## TROVATI APERTI / NOTE

- **F-K2-1** (minore): il campo `chunk_chars` per fonte in sources.yaml non è documentato
  nel template del file (ci sono solo i campi obbligatori). Da aggiungere come commento
  facoltativo nel template prima di usare fonti reali.
- **R-K5 confermato**: al primo uso su un Mac senza venv con fastembed scaricato,
  i pesi MiniLM vengono scaricati da HuggingFace. L'ingest K2 NON usa ancora
  `.gas_vectors.db` (aggancio rimandato a K3), quindi per ora il rischio è N/A.
- **pyyaml**: era già installata nel `.venv` ma non in `requirements.txt`. Aggiunta
  come `pyyaml>=6.0`.

---

## PROSSIMI PASSI PROPOSTI

1. **K3** — wiring di `ricorda` per includere `source='knowledge'` nel retrieval vettoriale
   (unica fetta che tocca gas.py → gate revisore obbligatorio prima del commit)
2. **K4** — sanitizer anti-prompt-injection nel chunker (wrapper `[FONTE: nome]`)
3. Aggiungere prima fonte reale a sources.yaml (approvazione umana esplicita)
4. Estensione `gas doctor` con conteggio chunk per fonte (protezione anti-crescita)
