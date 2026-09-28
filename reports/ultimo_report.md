# Report: Fetta 3a-bis — fix pre-merge PR #101

**Data:** 2026-09-28  
**Branch:** feat/fetta3a-lezioni-quarantena  
**PR:** #101  
**Commit:** 427fcf0  
**Revisore:** #107 — APPROVATO CON RISERVE

---

## Verifica DB E2E (Punto 1)

**File DB usato dall'E2E Fetta 3a:** DB temporaneo in-process (`kernel_tmp()` con dir isolata). Il DB reale `.gas_memory.db` NON conteneva lezioni di test.

**Output `gas lezioni lista` sul DB reale:**

```
Nessuna lezione trovata.
```

Nessuna lezione da ritirare — DB di produzione pulito.

---

## Cosa è stato fatto

### 1. Lista testo completo + autore (`gas.py:lezioni_cmd`)

Rimosso `[:80]` dal display testo. Aggiunto campo `autore`. La riga ora mostra:

```
  [  id] [stato     ] <testo intero> | autore: <autore> | decisa: <data> | turni: <...>
```

### 2. Rifiuto `\n`/`\r` (`modules/memory/store.py:aggiungi_lezione`)

Check aggiunto DOPO `strip()` e PRIMA del len-check:

```python
if "\n" in testo or "\r" in testo:
    return None, "Il testo della lezione non può contenere a-capo (\\n, \\r): una lezione = una riga."
```

Niente scrittura su DB in caso di rifiuto (verificato da T68q).

### 3. R-lez-3: guard `json.loads` turni_sorgente (`gas.py:lezioni_cmd`)

```python
try:
    turni_list = json.loads(l.get("turni_sorgente") or "[]") or []
    ...
except (json.JSONDecodeError, TypeError):
    turni_label = " | turni: <illeggibile>"
```

Nessun crash su DB corrotto. T68r inietta JSON malformato direttamente via sqlite3 e verifica `rc==0` + `"<illeggibile>"` in output.

### 4. `write_file` blocco esteso (`gas.py:execute_tool_call`)

```python
_MEM_FILE_PREFIXES = ("gas_history", ".gas_memory", ".gas_vectors", ".gas_tokens")
if any(p in normalized for p in _MEM_FILE_PREFIXES):
    return "Operazione negata: la memoria di Gas è gestita automaticamente dal kernel, non scriverla mai."
```

La normalizzazione `lower().replace("-","_").replace(" ","_")` già presente garantisce:
- `.gas_memory.db-wal` → `.gas_memory.db_wal` → contiene `.gas_memory` → bloccato
- `.GAS_MEMORY.db` → `.gas_memory.db` → bloccato
- `.gas_vectors.*`, `.gas_tokens.*` → bloccati

---

## Risultati test

**Suite kernel completa (macOS, 2026-09-28):**

| Categoria | Risultato |
|-----------|-----------|
| Suite totale | **366 PASS, 5 FAIL** |
| F-mac-1 bwrap (invariati) | T11c2, T11e, T12a, T12c, T12e |
| Nuovi FAIL | **0** |
| T68o-T68s (nuovi) | **5/5 PASS** |

**Dettaglio T68o-T68s:**
- T68o PASS: lista mostra testo 120 char intero senza troncamento
- T68p PASS: lista mostra campo `autore:`
- T68q PASS: testo con `\n` rifiutato, count DB invariato
- T68r PASS: `turni_sorgente` corrotto → rc=0, output `<illeggibile>`
- T68s PASS: write_file negato per `.gas_memory.db`, `.gas_memory.db-wal`, `.GAS_MEMORY.db`, `.gas_vectors.index`, `.gas_tokens.cache`, `gas_history.json`

---

## Verdetto revisore #107 (INTEGRALE)

**APPROVATO CON RISERVE**

### Letture obbligatorie eseguite
- CLAUDE.md (dal system prompt, sez. 5 Wall of Shame, sez. 8 guardrail, sez. 10 roadmap)
- reports/stato_progetto.md: stato corrente, finding aperti R-lez-1/2/3
- .claude/agents/memoria_revisore.md: ultima review #106 APPROVATO CON RISERVE

### Analisi elementi del diff

**1. `gas.py:1552` — `_MEM_FILE_PREFIXES` e guardrail write_file esteso**

Introduce tupla locale `_MEM_FILE_PREFIXES = ("gas_history", ".gas_memory", ".gas_vectors", ".gas_tokens")` e sostituisce il singolo check con `any(p in normalized for p in _MEM_FILE_PREFIXES)`. Verificato sul file reale (riga 1552 confermata). La normalizzazione `lower().replace("-","_").replace(" ","_")` già applicata al rigo 1551 garantisce: `.gas_memory.db-wal` → `.gas_memory.db_wal` → contiene `.gas_memory` → bloccato; `.GAS_MEMORY.db` → `.gas_memory.db` → bloccato per `.lower()`. T68s verifica 6 varianti con asserzione discriminante. Rischio falsi positivi: trascurabile (prefissi esclusivi dei file runtime). Esito: **ok**. Riserva cosmetica: `_MEM_FILE_PREFIXES` è ricreata ad ogni call — meglio come costante di modulo, ma non bloccante.

**2. `modules/memory/store.py:1186` — rifiuto `\n`/`\r` in `aggiungi_lezione`**

Check inserito DOPO `testo.strip()` (riga 1183) e PRIMA del len-check. Interazione con strip() corretta: strip rimuove whitespace di bordo ma lascia intatti i newline embedded. `"riga1\nriga2"` supera strip invariato e viene catturato. T68q verifica sia il rifiuto (id is None) sia l'assenza di scrittura su DB (count invariato prima==dopo). Esito: **ok**.

**3. `gas.py:2677-2686` — lezioni_cmd: guard JSON, testo completo, autore**

`try/except (json.JSONDecodeError, TypeError)` chiude R-lez-3: join su lista con non-stringa solleva TypeError, catturato. Fallback `" | turni: <illeggibile>"` user-friendly. Rimozione `[:80]` corretta per CLI umana. `l.get('autore', '?')` sicuro su campo assente. T68r inietta direttamente JSON malformato via sqlite3 e verifica `rc==0 AND "<illeggibile>" in output` — asserzione discriminante. Esito: **ok**.

**4. `tests/test_unit_kernel.py:4259-4328` — T68o-T68s**

T68o/T68p: riuso corretto dello stesso kernel/stdout. T68r: test più robusto (corruzione SQL diretta + verifica degradazione ordinata). T68s: 6 varianti incluse uppercase e WAL. Nessun antipattern Wall of Shame (niente slicing history, niente simulazione tool). `_run_lezioni_cmd` cattura stdout con `redirect_stdout` e patcha `sys.argv` correttamente. Esito: **ok**.

### Verifica guardrail di progetto

- Nessuna nuova eccezione non catturata propagata al crash.
- Guardrail anti-loop cap 10 iterazioni: non toccato.
- `_get_window()`: non toccato.
- Wall of Shame: niente slicing `[-n:]` né simulazione tool output.
- Fail-safe §9: `store.py` ritorna `(None, msg)` senza mai propagare eccezioni.

### Riserve (non bloccanti)

- **R-lez-bis-1 (cosmetica):** `_MEM_FILE_PREFIXES` definita inline nel branch write_file di `execute_tool_call` — preferibile come costante di modulo. Nessun impatto funzionale o di sicurezza.
- **R-lez-2 (ereditata da #106, non chiusa):** nessun blocco architetturale in `execute_tool_call` per i metodi `lezioni_*` — mitigata da T68n, non aggravata.

### Rischio esplicitamente escluso

Comportamento su VPS (Python 3.12.3, dipendenze complete) non verificato — il diff non introduce dipendenze da versione Python né librerie esterne nuove, rischio di regressione VPS-specifica stimato trascurabile.

---

## Fuori scope (rimandato)

- Fetta 3b: generatore LLM di lezioni (proposte automatiche)
- R-lez-bis-1: spostamento `_MEM_FILE_PREFIXES` a costante di modulo
- R-lez-2: blocco architetturale `lezioni_*` in `execute_tool_call`
