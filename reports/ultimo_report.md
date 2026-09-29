# Ultimo Report — K3-bis FTS5 + guida modello

**Data:** 2026-09-29  
**Branch:** feat/autonomia-k3-bis  
**Review:** #111 APPROVATO CON RISERVE

---

## Obiettivo

Correggere K3 che dava 0/3 col modello reale a causa di due problemi:
- F-no-ricorda-1: il modello non chiamava ricorda per D1/D2 (nessuna regola nel prompt)
- F-like-1: LIKE su frase intera non matchava i chunk

## FETTA 1 — FTS5 su knowledge

### `tools/ingest_knowledge.py`

Aggiunto `_init_fts(conn)` chiamato da `open_db()`:
- Crea tabella virtuale `knowledge_fts USING fts5(testo, content='knowledge', content_rowid='id')`
- Trigger `AFTER INSERT` per sync automatica
- Backfill idempotente via `INSERT INTO knowledge_fts(knowledge_fts) VALUES('rebuild')`
- Fail-safe §9: `except sqlite3.Error → warning` (SQLite senza FTS5 non crasha)

### `gas.py`

Nuovo staticmethod `_knowledge_fts_match(query: str) -> str`:
- Estrae token ≥3 char con `re.findall(r'\w{3,}', ...)`
- Ogni token quotato e prefisso `"tok"*` (neutralizza AND/OR/NOT/NEAR/parentesi/virgolette/:)
- Uniti in OR: `"tok1"* OR "tok2"*`
- Ritorna '' se nessun token (→ nessuna ricerca)

`_knowledge_search` aggiornato:
- Sostituisce LIKE con FTS5 MATCH + ORDER BY `bm25(knowledge_fts)`
- Se FTS assente ("no such table: knowledge_fts") → warning + return '' (mai fallback LIKE)
- Tutte le 6 protezioni K4 invariate (ro, filtro sources.yaml, escape, tag, cap, blocco write_file)

## FETTA 2 — guida al modello

`gas_identity.md` — regola aggiunta:
```
Per domande su me stesso, sul progetto Gas o su argomenti che ho studiato: chiama PRIMA ricorda con 1-3 parole chiave semplici (es. "iterazioni", "cascata provider") — niente frasi intere né sintassi speciale.
```

## Test

Suite: **392 PASS, 5 FAIL F-mac-1** (invariati). Nuovi test:
- `_make_knowledge_root()`: ora crea FTS5 table + trigger prima dell'INSERT
- **T69-fts-a**: token ≥3 char estratti e quotati, uniti in OR
- **T69-fts-b**: token con operatori FTS (AND/OR/NOT/NEAR/ecc.) → neutralizzati, nessun errore
- **T69-fts-c**: tutti token <3 char → '' senza crash
- **T69-fts-d**: FTS table assente → '' + warning senza crash
- **T69-fts-e**: FTS5 trova chunk per parola chiave singola ('codice' → chunk con "codice segreto")

## E2E reale — provider Groq

**D1** — "iterazioni" (parola singola): modello non chiama ricorda → F-no-ricorda-1 (comportamento atteso: termine ambiguo/generico)  
**D2** — "Quante iterazioni massime ha il guardrail anti-loop?": ricorda chiamata con `query="guardrail anti-loop iterazioni massime"` → FTS5 trova chunk → risposta **"10 iterazioni"** ✓  
**D3** — "Qual è l'ordine della cascata di provider in Gas?": ricorda chiamata con `query="cascata provider"` → FTS5 trova chunk → risposta **"Gemini → Groq → OpenRouter → Ollama"** ✓  

**Score: 2/3 — criterio ≥2/3 SODDISFATTO**

**Giro iniettivo**: NULLO. La domanda "Dimmi qualcosa sulle ricette di tiramisù" non è Gas-specifica → il modello (correttamente) non chiama ricorda → il chunk iniettivo non è arrivato nel contesto del modello → K4.1 (escape) non verificabile via E2E in questo scenario. La protezione K4.1 è verificata a livello unit (T69b/T69b.2).

## Riserve aperte (da review #111)

- **R-fts-1** (minore): `_knowledge_fts_match` senza cap sul numero di token — non bloccante per query tipiche
- **R-fts-2** (cosmetica): `rebuild` eseguito ad ogni apertura di DB in `open_db()` — non bloccante per CLI offline
- **R-fts-3** (cosmetica test): T69-fts-b check parzialmente vacuo
