# Diagnosi bug "7×8 in text-only mode" — 2026-08-29

**Branch:** `sonda/vps-stato-2026-08-26`  
**Data:** 2026-08-29  
**Tipo:** Sonda read-only / diagnosi. Zero modifiche al motore.  
**Attività:** Riproduzione e isolamento del bug "kernel rifiuta 7×8" attestato il 2026-08-22.

---

## 1. Verifica pre-task

**Subagent revisore:** presente (`/.claude/agents/revisore.md` + `memoria_revisore.md` verificati da `ls .claude/agents/`). ✅

---

## 2. Riproduzione reale

### 2a. Ambiente

- Python: `venv/bin/python3` (3.12, dipendenze motore installate)
- Chiavi attive da `.env`: `GROQ_API_KEY` ✅ · `ELEVENLABS_API_KEY` ✅
- Chiavi assenti da `.env`: `GEMINI_API_KEY` · `OPENROUTER_API_KEY`
- Cascata effettiva per questo host (compito "semplice"): gemini-flash-lite → **SKIP** (no key) · gemini-flash → **SKIP** (no key) · **groq** (primo rung attivo)

### 2b. Input 1: `"7×8"`

```
classifica_compito('7×8') = 'semplice'   ← gas.py:1480-1485
EVENT tool_res: (nessuno)
EVENT final: "Non ho a disposizione un comando consentito dall'allowlist che mi
  permetta di eseguire direttamente una moltiplicazione, quindi non posso
  verificare con run_command il risultato di 7 × 8.
  Devo quindi dichiarare l'incertezza sul valore esatto."
```

### 2c. Input 2: `"sette per otto"`

```
classifica_compito('sette per otto') = 'semplice'
EVENT tool_res: (nessuno)
EVENT final: "Non ho a disposizione un comando consentito dall'allowlist che mi
  permetta di eseguire direttamente una moltiplicazione, quindi devo dichiarare
  che non posso fornire con certezza il risultato di 7 × 8."
```

### 2d. `gas_debug.log`

Nessun `WARNING Provider groq` emesso → la chiamata Groq API ha avuto **successo**.  
Nessun `WARNING Provider gemini` → i due rung Gemini saltati per assenza chiave (nessun errore, solo `continue`).  
Nessun evento `error` nella pipeline → la pipeline è **funzionante**.

---

## 3. Causa radice

Il bug non è un crash né un fallthrough di provider. La pipeline funziona; il problema è **semantico**: il modello produce un `final` con contenuto inutile.

### 3a. Meccanismo

Il sistema prompt base (`gas.py:46-55`, variabile `_GAS_SYSTEM_PROMPT_BASE`) contiene **due regole in tensione con l'allowlist**:

> "Per conteggi, misure e calcoli esatti usa SEMPRE run_command (es. wc -l),  
>  non stimare mai a mente. Se non puoi verificare un dato, dichiara l'incertezza  
>  invece di inventare."

La `SHELL_ALLOWLIST` (`gas.py:874-878`) include:

```python
SHELL_ALLOWLIST = frozenset({
    "ls", "cat", "head", "tail", "wc", "grep", "echo", "pwd", "date",
    "stat", "file", "uniq", "cut", "tr", "nl", "diff", "comm", "true",
    "false", "basename", "dirname", "printf", "seq", "rev",
})
```

**Nessun comando di calcolo aritmetico** è presente: né `python`, né `bc`, né `expr`, né `awk`, né `dc`.  
Il vet `_vet_command` (`gas.py:927-957`) rifiuta qualsiasi binario fuori allowlist.

### 3b. Catena causale

1. Il modello Groq riceve `"7×8"` + system prompt con la regola "usa SEMPRE run_command".
2. Il modello ragiona: "devo usare run_command → ma non ho un comando aritmetico nell'allowlist → non posso verificare → devo dichiarare incertezza".
3. Il modello risponde direttamente con la dichiarazione di incertezza **senza tentare alcuna tool call** (zero eventi `tool_res`).
4. `run_turn` emette `{"type": "final", "content": "Non ho a disposizione..."}`.
5. `server.py:152-154` invia `{"content": "..."}` → HTTP 200 al client.
6. Il client in `--text-only` stampa la risposta → **nessun calcolo visibile all'utente**.

### 3c. Evidenza verbatim (path:riga)

| Elemento | Path:riga | Contenuto |
|---|---|---|
| Regola "usa SEMPRE run_command" | `gas.py:50-52` | `"usa SEMPRE i tool nativi... non inventare"` |
| Regola "dichiara incertezza" | `gas.py:53-55` | `"dichiara l'incertezza invece di inventare"` |
| SHELL_ALLOWLIST senza aritmetica | `gas.py:874-878` | `frozenset({...})` — nessun `bc`/`python`/`expr` |
| Vet fail-closed | `gas.py:943-950` | binario non in allowlist → messaggio di diniego |
| Cascata "semplice" | `gas.py:1480-1485` | gemini-flash-lite → gemini-flash → groq |
| Loop agentic | `gas.py:1504` | `for _ in range(10)` |
| Emit final | `gas.py:1550-1554` | `elif msg.content: … yield {"type": "final", ...}` |
| Server consuma final | `server.py:152-153` | `result_content = event.get("content", "")` |
| Server risponde JSON | `server.py:171` | `self._send_json(200, {"content": result_content})` |

---

## 4. Opzioni di fix (nessuna implementata — decide l'operatore)

### Opzione A — Eccezione nel system prompt (solo testo)
**Cosa:** Aggiungere al system prompt una riga del tipo:
> "Per aritmetica elementare (moltiplicazioni, addizioni, potenze di singoli numeri) puoi rispondere direttamente — la regola run_command vale per misurazioni di file e sistema, non per calcolo puro."

**File toccati:** `gas.py:50-55` (1 riga aggiunta)  
**Rischio:** Basso. Nessuna modifica al codice; il modello potrebbe comunque "stimare" anche su conteggi che richiedono run_command. Richiede review.  
**Nota:** Gemini (su VPS) potrebbe comportarsi diversamente da Groq; fix da verificare su entrambi.

### Opzione B — Aggiungere `bc` all'allowlist
**Cosa:** `SHELL_ALLOWLIST` include `"bc"`. Il modello può fare `run_command bc <<< "7*8"` …  
**Attenzione:** `bc` senza shell non riceve input da stdin nel modo usuale via subprocess; richiederebbe passaggio via file temporaneo o pipe (non disponibile). Probabilmente non risolve il problema senza modifiche aggiuntive al sandbox.  
**File toccati:** `gas.py:874-878`  
**Rischio:** Medio. Richiede analisi dei vettori di abuso `bc`.

### Opzione C — Tool dedicato `calcola(expr)`
**Cosa:** Nuovo tool `calcola` con `eval()` Python ristretto (solo operatori numerici + `math.*`), nessuna shell.  
**File toccati:** `gas.py:390-397` (tools_schema) + nuovo dispatch in `execute_tool_call` + test.  
**Rischio:** Alto (eval). Richiede sandboxing rigoroso dell'input e review completa. Soluzione più robusta a lungo termine.

### Opzione D — `printf` con aritmetica (no-op)
**Nota:** `printf` è già in allowlist ma non fa aritmetica senza shell. Non percorribile.

---

## 5. Gate rispettati

- **Zero modifiche al motore** (gas.py, brains/, modules/, tests/): rispettato.
- **Zero commit al codice** del motore: rispettato.
- **Il revisore non è stato invocato** (task doc-only, nessun diff motore da revisionare): corretto.

---

## 6. Sintesi

| Domanda | Risposta |
|---|---|
| Il kernel crasha? | No — evento `final` emesso correttamente |
| Il provider fallisce? | No — Groq risponde HTTP 200 |
| Manca un tool aritmetico? | **Sì** — nessun comando in allowlist esegue aritmetica |
| Qual è il gate/guardia che causa il problema? | Il system prompt (`gas.py:50-55`) + l'assenza di aritmetica in SHELL_ALLOWLIST (`gas.py:874-878`) |
| Il comportamento è coerente su `7×8` e `sette per otto`? | **Sì** — identico |
| È bloccante per il giro audio? | No (già attestato dal supervisore 2026-08-22) |
| Prossimo passo | L'operatore sceglie tra opzione A/B/C; poi si apre una fetta di fix con revisione |
