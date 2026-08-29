# Audit System Prompt — Direttive contraddittorie e ambigue
**Data:** 2026-08-29
**Branch:** sonda/vps-stato-2026-08-26
**Scope:** READ-ONLY audit del system prompt in gas.py. Nessuna modifica al motore.
**Oggetto:** rilevare direttive contraddittorie, ambigue o impossibili da eseguire — stessa classe del bug 7×8.

---

## Materiale esaminato

| File | Righe | Contenuto |
|------|-------|-----------|
| `gas.py` | 38–60 | `_GAS_SYSTEM_PROMPT_BASE` |
| `gas.py` | 62–68 | `_build_system_prompt()` — logic di composizione |
| `gas.py` | 390–397 | `tools_schema` — tool esposti al modello |
| `gas.py` | 874–878 | `SHELL_ALLOWLIST` — binari consentiti in run_command |
| `gas_identity.md` | 1–5 | identità runtime iniettata prima del base prompt |

**System prompt effettivo** (quando `gas_identity.md` esiste, gas.py:67):
```
# LA TUA IDENTITÀ
[gas_identity.md]

[_GAS_SYSTEM_PROMPT_BASE]
```

---

## Finding F1 — CRITICO: "calcoli esatti" impossibili con run_command

**Path:righe:** `gas.py:46-48`

**Citazione verbatim:**
```
"Per conteggi, misure e calcoli esatti usa SEMPRE run_command (es. wc -l), "
"non stimare mai a mente. Se non puoi verificare un dato, dichiara l'incertezza "
"invece di inventare.\n"
```

**SHELL_ALLOWLIST effettiva** (`gas.py:874-878`):
```python
SHELL_ALLOWLIST = frozenset({
    "ls", "cat", "head", "tail", "wc", "grep", "echo", "pwd", "date",
    "stat", "file", "uniq", "cut", "tr", "nl", "diff", "comm", "true",
    "false", "basename", "dirname", "printf", "seq", "rev",
})
```

**Perché è un problema:** Il sistema ordina a Gas di usare run_command per "calcoli esatti" ma la SHELL_ALLOWLIST non contiene nessun calcolatore: `bc`, `expr`, `awk`, `python`, `python3` sono assenti. `seq` genera sequenze, `printf` formatta testo, `wc` conta caratteri/righe/parole — nessuno può fare aritmetica. Se l'utente chiede `7×8`, `15% di 340`, o qualunque operazione aritmetica, run_command verrà negata con "comando non consentito". Gas si trova in stallo: gli è stato ordinato di usare un tool che non ha per fare una cosa. È **esattamente la classe del bug 7×8** documentata nella diagnosi `e0afbd1`.

**Opzioni fix (scelta all'operatore, NON impegnata):**
- (a) Riscrivere la direttiva: sostituire "calcoli esatti" con "conteggi di file/righe/parole" — zero rischio, massima onestà sul perimetro reale.
- (b) Aggiungere `bc` all'allowlist — richiede `bc` installato su VPS; rischio basso ma estende superficie.
- (c) Aggiungere `python3` all'allowlist con regex di vetting speciale — apre esecuzione di codice arbitrario, rischio alto.

**Raccomandazione:** opzione (a) — riscrivere la direttiva senza ampliare l'allowlist.

---

## Finding F2 — ALTO: gas_identity.md cita 3 tool, il kernel ne espone 6

**Path:righe:** `gas_identity.md:3`

**Citazione verbatim:**
```
agisco sul mondo con i tool nativi read_file, write_file e run_command
```

**Tool effettivi** (`gas.py:390-397`, `tools_schema`):
```
run_command, write_file, read_file, ricorda, salva_contatto, imposta_stato_contatto
```

**Perché è un problema:** Gas legge la propria identità come parte del system prompt a ogni turno. Crede di avere 3 tool nativi; in realtà ne ha 6. I 3 non citati sono:
- `ricorda` — unico modo corretto di interrogare la memoria lunga (SQLite). Senza questa istruzione, Gas potrebbe tentare `read_file("gas_memory.db")` che restituisce binario illeggibile.
- `salva_contatto` / `imposta_stato_contatto` — CRM. Senza menzione, Gas non sa che esistono come tool invocabili.

Nessun crash immediato, ma la lacuna abbassa la probabilità che il modello usi questi tool spontaneamente per le azioni CRM/memoria.

**Opzione fix:** aggiornare `gas_identity.md` con la lista completa dei 6 tool.

---

## Finding F3 — ALTO: REGOLE TASSATIVE ripetono la stessa lista incompleta

**Path:righe:** `gas.py:42`

**Citazione verbatim:**
```
"Usa SEMPRE i tool nativi (read_file, write_file, run_command). "
"Non inventare, descrivere o simulare mai l'output: invocali davvero e aspetta il risultato.\n"
```

**Perché è un problema:** Stessa lacuna di F2, stavolta nel corpo del base prompt. La direttiva "Usa SEMPRE i tool nativi" nomina solo 3 tool; i restanti 3 (`ricorda`, `salva_contatto`, `imposta_stato_contatto`) non compaiono mai nelle REGOLE TASSATIVE. Un modello che legge questa regola non ha motivo di sapere che "invocare sempre i tool nativi" si estende anche a loro.

**Opzione fix:** aggiornare `_GAS_SYSTEM_PROMPT_BASE` con la lista completa, oppure referenziare genericamente "tutti i tool disponibili nello schema".

---

## Finding F4 — MEDIO: Conflitto "non bloccarti" vs "non simulare" senza path d'uscita per tool failure

**Path:righe:** `gas.py:44` vs `gas.py:42-43`

**Citazione A (robustezza):**
```
"Priorità assoluta alla robustezza: se qualcosa fallisce, gestisci l'errore senza bloccarti.\n"
```

**Citazione B (no-simulazione):**
```
"Non inventare, descrivere o simulare mai l'output: invocali davvero e aspetta il risultato.\n"
```

**Citazione C (workaround parziale):**
```
"non stimare mai a mente. Se non puoi verificare un dato, dichiara l'incertezza "
"invece di inventare.\n"
```

**Perché è un problema:** La Citazione C offre un workaround ("dichiara l'incertezza") ma è collocata nella sezione dedicata a "conteggi, misure e calcoli" — non è presentata come policy generale di fallback per qualunque tool failure. Il modello che riceve un diniego da run_command per un caso non coperto dalla Citazione C si trova in vicolo cieco:
- "non bloccarti" → tende a simulare (violando B)
- "non simulare" → tende a bloccarsi (violando A)

La regola C dovrebbe essere una policy globale: "se un tool call è negato e non esiste alternativa, dichiara esplicitamente il limite invece di simulare l'output."

**Opzione fix:** spostare/generalizzare la Citazione C come regola di fallback universale per tool failure, non solo per verifiche numeriche.

---

## Finding F5 — MINORE: Doppia auto-presentazione nel prompt composto

**Path:righe:** `gas_identity.md:1` + `gas.py:39`

**Citazione identity:**
```
Sono Gas, agente AI autonomo e personale, destinato a girare h24 su VPS...
```

**Citazione base:**
```
"Sei Gas, un agente AI autonomo e personale che gira su VPS. "
```

**Perché è un problema:** Quando `gas_identity.md` esiste (caso normale), il prompt composto contiene due auto-presentazioni consecutive: "Sono Gas..." poi "Sei Gas...". Ridondante. Non causa crash, ma occupa token e può confondere il modello su quale delle due rappresentazioni abbia priorità (terza persona "Sei" vs prima persona "Sono"). Finding a bassa priorità.

---

## Finding F6 — MINORE: "echo" in allowlist "sola lettura"

**Path:righe:** `gas.py:49` + `gas.py:875`

**Citazione prompt:**
```
"run_command è confinato: esegue SOLO comandi di sola lettura da una "
"allowlist (ls, cat, head, tail, grep, wc, cut, diff...), SENZA shell. "
```

**SHELL_ALLOWLIST (gas.py:875):**
```python
"ls", "cat", "head", "tail", "wc", "grep", "echo", ...
```

**Perché è un problema:** Il prompt descrive la allowlist come "sola lettura" (comandi che leggono file/stato), ma `echo` è un comando di output puro — non legge nulla. Inconsistenza concettuale. In pratica innocua (senza shell, `echo hello` funziona, `echo $PATH` stampa letteralmente `$PATH` senza espansione variabile). Finding a bassissima priorità.

---

## Riepilogo findings

| ID | Severity | Componente | Tipo |
|----|----------|------------|------|
| F1 | CRITICO | gas.py:46-48 | Istruzione impossibile da eseguire |
| F2 | ALTO | gas_identity.md:3 | Lista tool incompleta — identity |
| F3 | ALTO | gas.py:42 | Lista tool incompleta — base prompt |
| F4 | MEDIO | gas.py:42-44 | Conflitto tra regole senza path d'uscita |
| F5 | MINORE | gas_identity.md:1 + gas.py:39 | Ridondanza semantica |
| F6 | MINORE | gas.py:49 + gas.py:875 | Inconsistenza concettuale innocua |

---

## Conclusione

F1 è il finding più grave: stessa struttura del bug 7×8. Il kernel ordina di eseguire un'azione (calcolo aritmetico) con uno strumento che non può eseguirla. F2 e F3 sono la seconda classe critica: i tool CRM/memoria esistono nel kernel ma il modello non è istruito a sapere che esistono. F4 è un'ambiguità strutturale che rende il comportamento in caso di tool failure imprevedibile.

Nessuna modifica al motore effettuata in questo audit. Ogni fix richiede decisione e scope dall'operatore.
