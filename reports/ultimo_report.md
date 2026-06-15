# 🧠 REPORT — FASE 2, fetta 1: fondamenta dello storage della memoria di GAS

**Data:** 2026-06-15
**Esito:** ✅ COMPLETATO — modulo di persistenza nuovo, suite **75 → 85** (0 FAIL, zero token), revisore **APPROVATO CON RISERVE** (review #12).
**Commit del motore:** `8de2b0c`

---

## 1. Cosa è stato costruito

Un modulo di memoria nuovo, **`modules/memory/`** (stile `modules/marketing/`), che contiene
SOLO il livello di persistenza. **Nessun aggancio a `run_turn`** in questa fetta: il
cablaggio al loop agentico è solo PROPOSTO (vedi §FINALE), non implementato.

- `modules/memory/__init__.py` — facciata del package (espone `MemoryStore`, gli stati, `default_db_path`).
- `modules/memory/store.py` — la classe `MemoryStore` e lo schema.

### Collocazione e motivazione
`modules/memory/` accanto a `modules/marketing/`: la memoria (diario + rubrica lead) è
funzionale ai moduli di business (FASE 4), quindi vive nella stessa famiglia di moduli.
Resta disaccoppiata dal kernel: `MemoryStore(db_path)` non importa nulla da `gas.py`, così
è testabile in isolamento e cablabile dopo senza dipendenze circolari.

### Il database — SQLite, FILE SINGOLO (vincolo non negoziabile)
- Un solo file `.db`. **Niente WAL** di proposito: WAL creerebbe file collaterali
  `-wal`/`-shm` e romperebbe il vincolo "backup = copia di un file". Si resta sul journal
  di rollback di default, transitorio → il `.db` è autoconsistente per la copia.
- **Vive FUORI da git**: `.gas_memory.db` (+ eventuali `-wal`/`-shm`) aggiunti a `.gitignore`,
  insieme a `*.bak` (le copie di backup, già coperte). Motivo: è dato mutabile e personale
  (mesi di relazioni coi lead), non codice — non va versionato.
- Path di default: `<project_root>/.gas_memory.db` via l'helper `default_db_path(root)`.

### Le due tabelle
1. **`diario`** — log append-only di tutto ciò che GAS fa. Colonne: `id`, `ts` (ISO8601 UTC),
   `tipo`, `descrizione` (testo libero), `contatto_id` (riferimento opzionale a un lead).
   **MAI UPDATE, MAI DELETE.**
2. **`contatti`** — una riga per lead, upsert-abile. Colonne: `id`, `chiave` (UNIQUE, identità
   del lead per l'upsert), `nome`, `contatto`, `stato`, `ultimo_contatto`, `prossima_azione`,
   `note`, `creato_il`, `aggiornato_il`. Stati ammessi:
   `nuovo · contattato · risposto · interessato · rifiutato · chiuso`.

## 2. Invariante di design (incisa nel codice e qui)

- **Il diario è IMMUTABILE** — la storia non si riscrive. L'immutabilità è imposta **a livello
  di DB** da due trigger `BEFORE UPDATE` e `BEFORE DELETE` che fanno `RAISE(ABORT)`: vale anche
  contro SQL grezzo, non è solo una convenzione applicativa (T19f lo dimostra).
- **I contatti sono MUTABILI per natura** — lo stato cambia nel tempo e **invalida i fatti
  vecchi**: quando un lead passa a `rifiutato`/`chiuso` (insieme `STATI_CHIUSI`), GAS non deve
  più inseguirlo. È la regola **aggiorna/invalida** che impedisce alla memoria di mentire.
- **Separazione dei ruoli** (per non confondere identità e ciclo di vita):
  `upsert_contatto` aggiorna SOLO l'anagrafica e in conflitto **non tocca lo stato**; la
  **transizione di stato passa SOLO da `update_stato_contatto`** (T19c lo verifica).

## 3. API minima

- **Scrittura:** `append_diario(tipo, descrizione, contatto_id=None)`,
  `upsert_contatto(chiave, nome=, contatto=, stato=, prossima_azione=, note=)`,
  `update_stato_contatto(contatto_id, nuovo_stato, prossima_azione=)`.
- **Lettura:** `diario_recente(n)`, `get_contatto(id)`, `lista_contatti(filtro_stato=None)`,
  `diario_di_contatto(id)`.
- **Backup:** `backup(dest_dir=None)` — copia timestampata `.bak` usando l'API nativa
  `sqlite3 .backup()` (copia COERENTE anche con scritture in volo). Banale perché file singolo.

### Scelta intenzionale: scritture IN-PROCESS, non via `run_command`
Le scritture passano per `sqlite3` direttamente nel processo del kernel. Questo **bypassa
correttamente il sandbox bwrap**: la memoria è codice FIDATO del kernel, non un comando
esterno non fidato. Far passare la memoria da `run_command` sarebbe sbagliato due volte —
girerebbe in un sandbox con filesystem read-only (non potrebbe scrivere il `.db`) e
tratterebbe come ostile un'operazione di fiducia. Decisione documentata e voluta.

## 4. Robustezza (fail-safe §9)

- **DB mancante** → creato automaticamente (le directory mancanti con `mkdir parents`).
- **DB corrotto** → `MemoryStore` NON crasha all'init: l'errore è loggato come `warning` nella
  scatola nera, `available=False`, e ogni metodo degrada ai valori sicuri (scritture→`None`/`False`,
  letture→`[]`/`None`). Verificato da T19j su un file di spazzatura binaria.
- Ogni metodo è blindato in `try/except (sqlite3.Error, OSError)`. Type hints rigorosi ovunque (§4).
- **Estensibilità**: lo schema è una tupla di DDL idempotenti (`CREATE ... IF NOT EXISTS`).
  Aggiungere registri futuri (lista lavori, regole fisse, metriche) = aggiungere DDL a `_SCHEMA`,
  senza rifare le fondamenta.

## 5. Test (zero token, tutto locale) — suite 75 → 85

Aggiunti `T19a–T19j` in `tests/test_unit_kernel.py` (DB su dir temporanee, nessuna chiamata LLM):
- T19a append + lettura diario · T19b upsert crea+aggiorna senza duplicare · T19c upsert non
  resetta lo stato · T19d transizione di stato + filtro + invalidazione · T19e stato non valido
  respinto · **T19f IMMUTABILITÀ diario (UPDATE e DELETE bloccati dai trigger)** · T19g
  `diario_di_contatto` lega gli eventi al lead · T19h backup → copia leggibile con gli stessi dati ·
  T19i fail-safe DB assente (creato e operativo) · T19j fail-safe DB corrotto (degrada, no crash).
- **Risultato: 85 PASS, 0 FAIL.**

## 6. Cosa NON è stato toccato
`run_turn`, pipeline provider, sandbox, snapshot, `_get_window`: tutti INVARIATI. `gas.py` non
toccato. Wall of Shame §5 rispettata (nessuna simulazione di tool, nessuno slicing grezzo).

## 7. Verdetto del revisore (review #12) — APPROVATO CON RISERVE
- **R1 (🟡 minore)**: i trigger di immutabilità coprono UPDATE/DELETE ma NON `INSERT OR REPLACE`
  sulla PK con i default SQLite (`recursive_triggers` OFF). Portata reale limitata: `append_diario`
  fa solo INSERT puro; il buco si apre solo a chi ha già accesso diretto al file `.db`. Docstring
  precisata col caveat. Da blindare alla passata di hardening (terzo trigger `BEFORE INSERT` o
  `recursive_triggers ON`).
- **R2 (🟡 minore)**: costanti hardcoded (`DEFAULT_DB_FILENAME`, `timeout=10`, `n=20`), coerente con
  la prassi del progetto; valutare override `GAS_MEMORY_DB` al cablaggio su VPS.
Entrambe tracciate in `reports/stato_progetto.md`. Nessuna indebolisce un guardrail.

---

## §FINALE — Proposta (NON implementata) di aggancio a `run_turn`

Da rivedere insieme PRIMA di cablare, perché tocca il loop agentico blindato.

**1) QUANDO GAS scrive su diario/contatti?**
- **Diario**: una riga **per ogni tool call eseguita**, scritta in-process subito dopo l'esecuzione
  del tool nel loop di `run_turn` (lo stesso punto dove oggi scatta lo snapshot). `tipo` = nome del
  tool, `descrizione` = sintesi argomenti + esito sintetico. Granularità per-evento = il "ricorda
  tutto". Si scrive ANCHE l'esito negativo di un tool fallito (serve la storia).
- **Contatti**: NON scritti automaticamente dal loop in questa fase. Le `upsert/update_stato`
  avvengono per **intento esplicito** (un futuro tool dedicato tipo `salva_contatto`/`aggiorna_lead`,
  o il modulo marketing), non a ogni turno. Così evitiamo che il loop inventi/sporchi la rubrica.

**2) QUANDO/COSA innesca la LETTURA dalla memoria?**
- **Sempre, ma in piccolo**: all'INIZIO di `run_turn`, prima di costruire la finestra, si inietta
  un **blocco-memoria compatto** = ultimi `k` eventi del diario + sintesi dei contatti ATTIVI
  (`lista_contatti` escludendo `STATI_CHIUSI`).
- **A richiesta, in profondità**: un tool di sola lettura `ricorda(query)` per pescare eventi/lead
  specifici quando serve, senza appesantire ogni turno.

**3) COME iniettare il ricordato SENZA sforare `WINDOW_CHAR_CAP = 24000`?**
- **Budget dedicato e rigido**: `MEMORY_CHAR_BUDGET ≈ 3000` caratteri (~750–1000 token) per il
  blocco-memoria sempre-iniettato. Un `_build_memory_context()` costruisce il blocco e lo
  **tronca a livello di voce** (mai a metà parola/record) per stare nel budget.
- **Composizione col cap**: il blocco va contato DENTRO i 24000, non in aggiunta. Due opzioni da
  decidere: (a) iniettarlo nel system prompt (già passato a ogni chiamata) riservandogli il budget;
  (b) come singolo messaggio "memoria" pinnato, escluso dallo scarto di `_cap_window_chars` ma
  **sottratto dal cap** (cap effettivo finestra = 24000 − dimensione blocco-memoria). Preferenza:
  (b), così la memoria non viene mai potata per prima ma non può comunque sfondare il tetto.

**4) DOVE va l'aggancio nel codice?**
- **Istanza**: `self.memory = MemoryStore(default_db_path(self.root))` in `GasKernel.__init__`
  (fail-safe: se degrada, il resto del kernel funziona comunque).
- **Scrittura diario**: nel punto del loop di `run_turn` dove il tool viene eseguito (vicino allo
  snapshot), un `self.memory.append_diario(...)` in-process.
- **Lettura/iniezione**: una nuova fase `_inject_memory()` chiamata all'inizio di `run_turn`,
  PRIMA di `_get_window()`/`_cap_window_chars`, che rispetti il budget del punto 3.
- **Tool `ricorda`**: nuovo entry nello schema dei tool + ramo nel dispatcher, sola lettura.

> Nota di prudenza: i punti 1 e 4 toccano il ciclo `for _ in range(10)` blindato (§8). Il cablaggio
> sarà una fetta a sé, con i suoi test di round-trip agentico, dopo l'OK su questa proposta.

---

## PARK (note registrate, non urgenti)
1. **Retention del diario** — cresce per sempre (stessa classe della retention snapshot). Non urgente;
   da affrontare quando il volume lo richiederà (strategia: archiviazione/export+rotazione del file
   storico, mai DELETE — violerebbe l'immutabilità).
2. **GDPR / dati personali dei lead** (UE) — terreno legale da guardare a FASE 4 (lead generation),
   non risolto ora: consenso, diritto all'oblio (in tensione con l'immutabilità del diario),
   minimizzazione dei dati. Solo registrato.
