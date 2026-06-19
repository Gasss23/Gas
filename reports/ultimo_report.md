# 📋 ULTIMO REPORT — Comando CLI `gas reindex` (review #25)

**Data:** 2026-06-19
**Esito:** ✅ COMMIT ESEGUITO — revisore APPROVATO CON RISERVE, fix R-reidx-2 incluso, suite 155/155, `reindex` confermato solo-CLI.

---

## Cosa è stato fatto

1. **Comando CLI `gas reindex`** (`gas.py`: funzione `reindex()` + dispatch in `main()`):
   ricostruisce da zero l'indice vettoriale `.gas_vectors.db` a partire dal diario.
   Manutenzione UMANA (post cambio modello embedding / diario grosso da indicizzare /
   indice sospetto incoerente). Sicuro: tocca solo la cache derivata, mai il diario;
   calcola gli embedding prima di svuotare → un fallimento non distrugge l'indice buono.
   Exit code 0 OK / 1 in degrado. Zero token LLM (solo embedding locali).

2. **Test T32a-c** (`tests/test_unit_kernel.py`): ricostruzione dal diario, idempotenza
   (svuota+ripopola, non duplica), fail-safe (vector store degradato → rc=1, nessun crash).

3. **Fix R-reidx-2** (commento di T32c): corretto per allinearlo a ciò che il test
   esercita davvero (parte da sidecar GIÀ corrotto → si ferma al check `vs.available`,
   NON esercita "calcola gli embedding prima di svuotare"; quella barriera è coperta da T30c).

---

## Verifiche dal vivo (richieste esplicitamente)

### 1) Dipendenze + suite reale
- Installate nel venv: **numpy 2.4.6**, **fastembed 0.8.0**, **onnxruntime 1.27.0**.
- Wheel `onnxruntime` su arch del Codespace (**x86_64**): installata **senza problemi**.
- Suite COMPLETA `python tests/test_unit_kernel.py`: **155 PASS, 0 FAIL**.
- I blocchi **T30/T31/T32** girano DAVVERO (prima saltati per `ModuleNotFoundError: numpy`,
  la suite si fermava a riga ~1612). Incluso l'embedding REALE T30e (dim=384, norma=1.0000).
- **Download modello:** il progetto usa `paraphrase-multilingual-MiniLM-L12-v2` (qdrant onnx-Q),
  cache su disco **~241 MB** (`/tmp/gas_vec_model_cache`). Cold embed (primo embed reale,
  include il load lazy del modello): **~1.83 s**.
- **NB:** fastembed avvisa che questo modello ora usa **mean pooling invece di CLS embedding**
  → cambio di comportamento dell'embedding tra versioni di fastembed. È esattamente il caso
  d'uso di `gas reindex` (re-indicizzare se i vettori storici diventano incompatibili).

### 2) Conferma `reindex` SOLO-CLI
- `reindex` **NON** è in `tools_schema` (gas.py:337-344, che elenca solo i 6 tool:
  run_command, write_file, read_file, ricorda, salva_contatto, imposta_stato_contatto).
- `reindex` **NON** è nel dispatcher del loop `execute_tool_call` (gas.py:1079-1180):
  ogni nome non gestito cade nel ramo `else → "Tool non trovato."` (gas.py:1180).
- È invocabile SOLO da CLI: dispatch in `main()` (gas.py:1556-1557, `gas reindex`).
- → Fuori dalla mano del modello, stessa classe di `unisci_contatti`/restore-snapshot/`git gc`
  (operazione irreversibile = manutenzione umana). **Conferma: solo-CLI.**

### 3) Fix R-reidx-2
- Eseguito (commento di T32c riscritto). Suite rieseguita dopo il fix: **155 PASS, 0 FAIL**.

---

## VERDETTO INTEGRALE DEL REVISORE (review #25)

> **File revisionati:**
> - `/workspaces/Gas/gas.py` — nuova funzione `reindex()` (righe ~1512-1550) + dispatch in `main()`
> - `/workspaces/Gas/tests/test_unit_kernel.py` — blocco T32 (T32a/b/c, righe ~1847-1881)
>
> **VERDETTO: APPROVATO CON RISERVE**
>
> Riserve da tracciare in `reports/stato_progetto.md`:
> - **R-reidx-1 (principale):** verifica dal vivo della suite (T30-T32, claim 152→155) NON eseguibile in questo ambiente — numpy/fastembed assenti sia nel python di sistema sia nel venv `/workspaces/Gas/venv`, la suite si ferma a riga 1612 (`ModuleNotFoundError: numpy`) prima del blocco vettori. Logica corretta per ispezione, ma l'esecuzione reale (e il conteggio suite) va fatta nell'ambiente con le dipendenze prima di chiudere la fetta.
> - **R-reidx-2 (minore):** il commento di T32c sovra-dichiara la barriera che morde — parte da sidecar già corrotto, quindi non esercita "calcola gli embedding prima di svuotare" (gas vectors.py:318). Allineare il commento o aggiungere un caso con indice popolato + embedder che degrada a metà.
> - **R-reidx-3 (informativa, eredita R-vec-3):** `reindex` materializza tutti gli embedding in RAM prima del DELETE — picco memoria da validare al deploy VPS 1GB su diario grande.
>
> Nessun antipattern del Wall of Shame, fail-safe §9 integro, cache derivata mai dato di verità, invarianti motore intatte. Non ho committato nulla. Memoria del revisore aggiornata in `/workspaces/Gas/.claude/agents/memoria_revisore.md`.

---

## Stato delle riserve dopo questa sessione

- **R-reidx-1 → ✅ CHIUSA:** dipendenze installate, suite reale **155/155**, conteggio verificato (non a memoria).
- **R-reidx-2 → ✅ CHIUSA:** commento di T32c corretto.
- **R-reidx-3 → 🟡 voce CHECKLIST pre-deploy VPS** (picco RAM di reindex su diario grande, VPS 1GB).
- **R-reidx-deps → 🟡 NUOVO:** la suite vettoriale non girava nel Codespace (numpy/fastembed assenti);
  ora installati; verificare che restino in `requirements.txt` e nell'ambiente del deploy.

---

## Note di processo
Il fix R-reidx-2 è una correzione di SOLO COMMENTO in un test, che implementa esattamente la
riserva sollevata dal revisore; non altera il comportamento del motore né la logica dei test.
La revisione del motore (verdetto sopra) resta valida; il commit è stato autorizzato
esplicitamente dall'utente in base alle tre condizioni vincolanti (suite reale verde,
T30/T31/T32 0 FAIL, reindex solo-CLI), tutte soddisfatte.
