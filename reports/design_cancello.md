# DESIGN: IL CANCELLO — Gate Autonomia GAS

> **Documento di progetto — SOLO DESIGN, ZERO CODICE**  
> Data: 2026-09-29  
> Branch: design/cancello  
> Obiettivo: architettura del meccanismo di controllo per le azioni di GAS  
> Missioni di riferimento: M1 lead autonomi, M2 mail con firma umana, M3 ripresa dopo crash, M4 iniezione durante missione

---

## 1. Inventario azioni e classificazione proposta

### 1a. Tool attuali

| Tool | Cosa fa | Classificazione proposta | Motivazione |
|---|---|---|---|
| `read_file` | Legge file interni alla root | **reversibile-sicuro** | Sola lettura; confinato alla root del progetto; nessun effetto esterno |
| `calcola` | Valuta espressioni matematiche (AST whitelist) | **reversibile-sicuro** | Puro calcolo in-process; nessun effetto su stato o sistemi esterni |
| `ricorda` | Interroga memoria SQLite (sola lettura) | **reversibile-sicuro** | In-process; non muta nulla; ma produce contenuto esterno non fidato (→ §3) |
| `write_file` | Scrive file interni alla root | **reversibile-incerto** | Muta stato locale; snapshot preventivo già presente; sovrascrittura accidentale possibile |
| `salva_contatto` | Upsert anagrafica CRM in SQLite | **reversibile-incerto** | Muta DB contatti; l'upsert è ripetibile ma modifica record esistenti con dati potenzialmente errati |
| `imposta_stato_contatto` | Transizione stato funnel (match esatto chiave) | **reversibile-incerto** | Muta stato funnel lead — scatena comportamenti a cascata (follow-up, priorità) |
| `run_command` | Esegue comandi shell (sandbox bwrap + allowlist) | **reversibile-incerto** | Superficie ampia; sandbox OS e applicativa riducono il danno ma non lo annullano; comandi distruttivi in allowlist possono scrivere su disco |

### 1b. Azioni future note

| Azione | Classificazione proposta | Motivazione |
|---|---|---|
| Notifica Telegram all'utente (output puro) | **reversibile-sicuro** | Output verso utente autenticato; nessun effetto su sistemi terzi |
| Richiesta di approvazione Telegram (meccanismo del cancello stesso) | **reversibile-sicuro** | Parte del gate; non esegue nulla |
| Browser scraping / lettura web | **reversibile-incerto** | Sola lettura ma produce contenuto esterno non fidato (→ §3) |
| Invio email / DM (mail API, LinkedIn, Telegram a terzi) | **irreversibile** — firma umana obbligatoria | Non revocabile dopo invio; impatta relazioni reali; vettore spam/phishing |
| Post sui social / messaggi pubblici | **irreversibile** — firma umana obbligatoria | Visibilità esterna; danno reputazionale non annullabile |
| Push su repository git (branch/tag/main) | **irreversibile** — firma umana obbligatoria | Modifica cronologia condivisa; impatta CI/CD; visibile a terzi |
| Browser automation con submit di form / click su pulsanti | **irreversibile** — firma umana obbligatoria | Può inviare dati a sistemi esterni, acquistare, cancellarsi da servizi |
| Computer use (controllo mouse/tastiera sulla macchina locale) | **irreversibile** — firma umana obbligatoria | Controllo diretto della macchina; superficie di danno enormissima |
| Accesso SSH al VPS | **denylist** | Privilegio incompatibile con autonomia non presidiata; chiavi condivise con bot trading |
| Lettura / modifica di file `.env` / credenziali / secret | **denylist** | Esfiltrazione credenziali; mai eseguire neanche con firma |
| Modifica al file di configurazione del gate (futuro `gate_config.py`) | **denylist** | Auto-modifica dei vincoli di sicurezza = annullamento del cancello |
| Scrittura su `.gas_memory*`, `.gas_history*`, `.gas_knowledge*`, `.gas_vectors*`, `.gas_tokens*` | **denylist** (guardrail esistente — da estendere al gate) | Il kernel gestisce questi file; il modello non deve mai scriverli |

### 1c. Chiarimento sulla distinzione tra classi

- **reversibile-sicuro**: GAS esegue autonomamente, nessuna approvazione.
- **reversibile-incerto**: GAS esegue autonomamente nel caso normale; in turno contaminato (§3) scala a firma umana.
- **irreversibile**: firma umana **sempre**, anche fuori da turni contaminati. La "reversibilità tecnica" (si può rollbackare il DB) non conta — conta l'**impatto esterno**: un'email inviata non si cancella dalla posta del destinatario.
- **denylist**: blocco assoluto, non scalabile a nessun livello di approvazione. Non è una categoria "super-irreversibile" — è fuori dal perimetro di GAS per definizione, e una firma umana non la sblocca.

---

## 2. Classificatore deterministico

### 2a. Principio di funzionamento

Il classificatore è un **dizionario hardcoded in Python** (non un file YAML né una config leggibile da GAS a runtime). La regola è **default-STOP**: se un'azione non appare nell'allowlist, il cancello blocca senza eccezioni.

Il modello non può:
- Aggiungere o modificare entry nell'allowlist.
- Classificare autonomamente un'azione non prevista come "sicura".
- Invocare azioni in denylist anche se l'utente lo chiede esplicitamente.
- Ispezionare la configurazione interna del gate (il file config non è leggibile via `read_file`).

### 2b. Struttura dati proposta

```python
# gate_config.py  — NON modificabile da GAS
from enum import Enum

class GateClass(Enum):
    SAFE         = "reversibile-sicuro"
    UNCERTAIN    = "reversibile-incerto"
    IRREVERSIBLE = "irreversibile"
    DENY         = "denylist"

# Allowlist: tool_name → GateClass
# Tool NON presente → DENY implicita (default-STOP)
GATE_ALLOWLIST: dict[str, GateClass] = {
    "read_file":                GateClass.SAFE,
    "calcola":                  GateClass.SAFE,
    "ricorda":                  GateClass.SAFE,
    "notify_telegram":          GateClass.SAFE,        # futuro: output verso utente
    "write_file":               GateClass.UNCERTAIN,
    "salva_contatto":           GateClass.UNCERTAIN,
    "imposta_stato_contatto":   GateClass.UNCERTAIN,
    "run_command":              GateClass.UNCERTAIN,
    "browser_scrape":           GateClass.UNCERTAIN,   # futuro
    "send_email":               GateClass.IRREVERSIBLE, # futuro
    "send_dm":                  GateClass.IRREVERSIBLE, # futuro
    "git_push":                 GateClass.IRREVERSIBLE, # futuro
    "browser_submit":           GateClass.IRREVERSIBLE, # futuro
    "computer_use":             GateClass.IRREVERSIBLE, # futuro
    # "ssh_vps", "write_env", "modify_gate" NON presenti → DENY implicita
}

# Denylist esplicita su path (prefissi) e tool per nome
GATE_DENY_PATH_PREFIXES = (
    ".gas_memory", ".gas_history", ".gas_knowledge",
    ".gas_vectors", ".gas_tokens", "gate_config",
)
GATE_DENY_TOOLS = frozenset({"ssh", "modify_gate", "write_env"})
```

### 2c. Punto di aggancio in `run_turn`

Il gate si inserisce **prima** di `execute_tool_call`, nel momento in cui il modello produce una tool call. Il gate non è un rung della cascata provider: è un layer imperativo del kernel. Il modello vede solo la risposta al tool call (eseguito, rifiutato, in attesa).

Sequenza logica:

```
modello produce tool call tc
  ↓
gate_classify(tc.function.name, tc.function.arguments)
  ├─ SAFE:                   esegui direttamente (comportamento attuale)
  ├─ UNCERTAIN (non contaminato): esegui direttamente (comportamento attuale)
  ├─ UNCERTAIN (turno contaminato): tratta come IRREVERSIBLE (→ approvazione)
  ├─ IRREVERSIBLE:           enqueue approvazione → Telegram → attendi → esegui / diniego
  └─ DENY (o tool non in allowlist): blocco immediato, log warning,
                              risposta al modello: "Operazione negata: azione
                              non consentita in modalità autonoma."
```

### 2d. Invariante di sicurezza

Il file `gate_config.py` (o il modulo equivalente) non deve essere leggibile via `read_file`. Il percorso va aggiunto alla denylist di `write_file` e non deve essere nella `root` di `GAS_CWD` esposta al modello. Se il modello chiede "quali azioni puoi fare autonomamente?", GAS risponde descrivendo le **categorie** (sicure, incerte, irreversibili) senza esporre il dizionario esatto.

---

## 3. Regola "input non fidato"

### 3a. Definizione di "turno contaminato"

Un turno è **contaminato** se in quel turno GAS ha invocato con successo (output non-KO) almeno uno dei seguenti tool:

| Tool | Perché contamina |
|---|---|
| `ricorda` | Può restituire dati di lead (testo da persone terze) o chunk di knowledge da fonti esterne |
| `read_file` su file non di sistema | File caricati dall'utente, report CRM, testo proveniente da scraping |
| `browser_scrape` (futuro) | Contenuto web non controllato |
| `fetch_email` (futuro) | Contenuto email da mittenti terzi |

I tool SAFE puri (`calcola`, `notify_telegram`) non contaminano il turno anche se eseguiti.

### 3b. Tracciamento nel loop

Si aggiunge un flag per-turno `_turno_contaminato: bool = False` all'inizio di `run_turn`, impostato a `True` quando uno dei tool contaminanti viene eseguito con risposta non-KO:

```python
# Pseudocodice — NESSUNA implementazione in questo documento
UNTRUSTED_INPUT_TOOLS = {"ricorda", "read_file", "browser_scrape", "fetch_email"}

# Dopo execute_tool_call:
if tc.function.name in UNTRUSTED_INPUT_TOOLS:
    if not out.startswith("Operazione negata") and not out.startswith("Errore"):
        _turno_contaminato = True
```

Il flag è **per-turno**: si azzera all'inizio del turno successivo. Non persiste tra conversazioni.

### 3c. Effetto sul gate

Nel classificatore, la contaminazione promuove le azioni UNCERTAIN di un livello:

| Classe base | Turno pulito | Turno contaminato |
|---|---|---|
| SAFE | Esegui | Esegui |
| UNCERTAIN | Esegui | Richiedi approvazione Telegram |
| IRREVERSIBLE | Richiedi approvazione | Richiedi approvazione + avviso contaminazione |
| DENY | Blocca | Blocca |

Il messaggio Telegram per un'azione IRREVERSIBLE in turno contaminato include:
> ⚠️ Attenzione: in questo turno GAS ha letto contenuto esterno (lead, knowledge, file utente). Verifica con attenzione l'azione prima di approvare.

### 3d. Razionale e limiti

La tracciatura è **conservativa** (falsi positivi possibili: un `ricorda` che non ha trovato nulla contamina comunque il turno) ma **mai permissiva** (nessun falso negativo di sicurezza). Il costo sono alcune approvazioni in più su task ibridi; il beneficio è protezione contro la compromissione indiretta, dove un lead con testo malevolo cerca di scatenare azioni CRM attraverso la stessa sessione.

---

## 4. Canale firma: coda approvazioni Telegram

### 4a. Struttura della coda

Tabella `approvals` nel DB di memoria esistente (`.gas_memory.db`):

| Colonna | Tipo | Descrizione |
|---|---|---|
| `id` | INTEGER PK | Autoincrement |
| `turno_id` | TEXT | UUID del turno che ha generato la richiesta |
| `tool_name` | TEXT | Nome esatto del tool da eseguire |
| `tool_args_json` | TEXT | Argomenti verbatim (JSON) — base del read-back |
| `azione_leggibile` | TEXT | Descrizione in italiano generata dal kernel (non dal modello) |
| `stato` | TEXT CHECK | `pending` / `approved` / `rejected` / `expired` |
| `ts_created` | REAL | Unix timestamp creazione |
| `ts_expiry` | REAL | Unix timestamp scadenza (default: `ts_created + 300`) |
| `ts_resolved` | REAL | Quando lo stato è uscito da `pending` |
| `risolto_da` | TEXT | `"telegram_user"` / `"timeout"` / `"kernel_revoca"` |

### 4b. Flusso di approvazione

```
1.  gate_classify → IRREVERSIBLE (o UNCERTAIN promossa per contaminazione)
2.  kernel: INSERT in approvals (stato=pending, ts_expiry=now+300)
3.  kernel → bot Telegram: invia messaggio con:
    - azione_leggibile (descrizione italiana, generata dal kernel)
    - tool_args_json troncati a 500 char (read-back dell'azione esatta)
    - Bottoni inline: [✅ Approva] [❌ Rifiuta]
4.  turno corrente: SOSPESO (yield {"type": "waiting_approval", "approval_id": id})
5.  bot riceve callback:
    ├─ ✅ Approva → UPDATE stato=approved → kernel sblocca il turno → esegue tool
    └─ ❌ Rifiuta → UPDATE stato=rejected → diniego pulito al modello
6.  Se nessuna risposta entro ts_expiry:
    - UPDATE stato=expired
    - Il turno che aspettava riceve: "Approvazione scaduta — azione non eseguita."
    - Bot Telegram: notifica passiva "⏱️ Approvazione scaduta per: [azione_leggibile]"
```

### 4c. Read-back dell'azione esatta

Il messaggio Telegram al punto 3 mostra **verbatim** i `tool_args_json` (troncati), non solo la descrizione in italiano. L'utente vede esattamente cosa sta per essere eseguito. La `azione_leggibile` è generata dal kernel sulla base del nome del tool e degli argomenti grezzi — non è parafrasata dal modello LLM.

Esempio per `send_email`:
```
📧 GAS vuole inviare un'email

Azione: send_email
Destinatario: mario.rossi@example.com
Oggetto: "Follow-up proposta"
Argomenti JSON: {"to": "mario.rossi@example.com", "subject": "Follow-up proposta", "body": "Ciao Mario..."}

[✅ Approva] [❌ Rifiuta]
```

### 4d. Timeout e default-non-eseguire

- **Default timeout**: 5 minuti (env `GAS_APPROVAL_TIMEOUT_SECS`, default 300).
- **Allo scadere**: l'azione **non viene mai eseguita** — mai come side-effect silenzioso.
- GAS informa l'utente nel messaggio finale: "Non ho potuto completare [azione]: nessuna approvazione ricevuta entro 5 minuti."
- La richiesta scaduta resta in tabella per audit. Non viene cancellata automaticamente.
- Un'approvazione arrivata dopo la scadenza viene ignorata (stato già `expired`, non si riesegue).

### 4e. Cosa succede se nessuno risponde

Non eseguire e informare — questo è il contratto. GAS non ha modo di "insistere": non può auto-approvare, non può re-inviare la richiesta automaticamente (per evitare Telegram spam). Se l'utente vuole sbloccare un'azione scaduta, deve iniziare un nuovo turno.

---

## 5. File e path intoccabili da GAS

Il gate estende e formalizza il guardrail `_MEM_FILE_PREFIXES` già presente in `execute_tool_call` (gas.py:1657). I seguenti path sono in **denylist assoluta** per `write_file` e `run_command`:

| Path (prefisso o esatto) | Motivo |
|---|---|
| `.gas_memory.db*` | DB stato kernel + coda approvazioni gate |
| `.gas_history.json` | Cronologia conversazioni |
| `.gas_knowledge.db*` | Knowledge base appresa da fonti esterne |
| `.gas_vectors.db*` | Indice semantico vettoriale |
| `.gas_tokens.jsonl` | Log telemetria token |
| `gas.py` | Il motore stesso |
| `brains/` | Provider e routing |
| `modules/` | Moduli del kernel |
| `.claude/` | Config Claude Code (hook, agenti) |
| `gate_config.py` (futuro) | Config del gate — auto-modifica dei vincoli = annullamento del gate |

Questi file non devono essere leggibili con `read_file` dalla root di GAS (o devono essere esclusi esplicitamente dalla `_safe_path` del kernel). L'obiettivo è che GAS non possa "studiare" la propria configurazione di sicurezza per aggirarla.

---

## 6. Piano a fette e test di accettazione

### Fetta C1 — Scaffolding gate (zero modifica al motore)

- Crea `modules/gate/gate.py` con `GateClass`, `GATE_ALLOWLIST`, funzione `gate_classify(tool_name: str, args: dict) -> GateClass`.
- Logica: tool non in allowlist → `DENY`; path in `GATE_DENY_PATH_PREFIXES` per `write_file` → `DENY`; altrimenti lookup in `GATE_ALLOWLIST`.
- Zero modifiche a `gas.py`.
- **Test C1:** unit test per ogni tool noto → classificazione attesa; tool sconosciuto → `DENY`; `write_file` su `.gas_memory.db` → `DENY`.

### Fetta C2 — Integrazione in `run_turn` (flag contaminazione + gate check)

- Aggiungi `_turno_contaminato: bool = False` a `run_turn`.
- Prima di `execute_tool_call`: chiama `gate_classify`. Gestisci `DENY` con risposta "Operazione negata". Gestisci `IRREVERSIBLE` (o `UNCERTAIN` + contaminato) con `yield {"type": "waiting_approval", ...}` e stub `approved` (coda reale in C3).
- Modifica a `gas.py` — richiede review del revisore.
- **Test C2:** round-trip con tool SAFE passa invariato; tool `DENY` bloccato senza crash; `ricorda` + `salva_contatto` in sequenza → `waiting_approval` (stub approved).

### Fetta C3 — Coda approvazioni SQLite

- Aggiungi tabella `approvals` a `modules/memory/store.py`.
- Metodi: `enqueue_approval(...)`, `resolve_approval(id, stato)`, `get_pending_approvals()`, `expire_stale_approvals()`.
- Zero modifiche a `gas.py` in questa fetta (accesso via `self.memory.*`).
- **Test C3:** INSERT + resolve; scadenza artificiale (ts_expiry = now - 1) → `expired`; tentativo di re-resolve di approvazione già `approved` → no-op (stato immutabile dopo risoluzione).

### Fetta C4 — Bridge Telegram per le approvazioni

- Aggiungi handler nel bot Telegram (`modules/telegram/bot.py`) per ricevere callback da bottoni inline.
- Quando il kernel mette in coda un'approvazione, il bot invia il messaggio con bottoni.
- `/approva <id>` e `/rifiuta <id>` → `resolve_approval(id, stato)` → sblocca il turno in attesa.
- Questa fetta richiede che `run_turn` supporti la sospensione e ripresa (meccanismo da progettare — potrebbe richiedere coroutine o polling periodico).
- Modifica a `gas.py` e `modules/telegram/bot.py` — richiede review del revisore.
- **Test di accettazione M2:** GAS vuole inviare email → gate IRREVERSIBLE → enqueue → Telegram → [utente approva] → email inviata; [utente rifiuta] → "Non ho inviato l'email."

### Fetta C5 — Hardening: scadenza e audit

- Worker periodico (o check all'inizio di ogni turno) per scadere i `pending` oltre `ts_expiry` in `approvals`.
- Log in `gas_debug.log` per ogni approvazione / rifiuto / scadenza.
- `gas doctor` riporta il numero di approvazioni pendenti e scadute non risolte.
- **Test C5:** approvazione pending creata con `ts_expiry = now - 1`; il check all'inizio del turno successivo la scade; il turno che aspettava riceve diniego pulito.

### Test di accettazione M4 (iniezione durante missione)

1. GAS è in mezzo a un task autonomo di analisi lead.
2. Chiama `ricorda` → `_turno_contaminato = True`.
3. Subito dopo tenta `salva_contatto` (UNCERTAIN) → promosso a IRREVERSIBLE per contaminazione.
4. Enqueue approvazione → Telegram con avviso contaminazione.
5. Utente può: **approvare** (salvataggio avviene), **rifiutare** (salvataggio non avviene), oppure non rispondere (scadenza → diniego).
6. In futuro (fase oltre C5): possibilità di "iniettare" istruzioni alternative dalla risposta Telegram ("rifiuta + modifica: salva con stato 'lead_freddo' invece di 'lead_caldo'").

---

## 7. Finding F-diario-eco

### Descrizione del problema

**Dove nel codice:** `gas.py`, righe ~1859–1869, dentro `run_turn` dopo ogni `execute_tool_call`.

**Meccanismo:** Il kernel registra nel diario immutabile una riga per ogni tool call eseguita. Per il tool `ricorda`, la riga include:

```
tipo = "ricorda"
descrizione = "query='...' contatto='...' | [OK] <primi 160 char dell'output>"
```

L'output di `ricorda` contiene testo proveniente da:
- Lead/contatti CRM — testo inserito da persone terze (es. note su un lead).
- Chunk di knowledge ingerita da fonti esterne (web, documenti).
- Voci del diario stesso — creando un eco del diario nel diario.

**Il problema in tre punti:**

1. **Bypass della revoca fonte (K4.3):** Se una fonte knowledge viene revocata in `sources.yaml`, il filtro K4.3 blocca i suoi chunk dalla visualizzazione al modello. Ma se una `ricorda` aveva già restituito quei chunk in un turno precedente, i loro primi 160 caratteri sono già persistiti nel diario **immutabile**. Da quel momento possono tornare al modello via `_memoria_pin` (che legge il diario) o via una `ricorda` successiva che cerca quelle parole chiave nel diario stesso.

2. **Amplificazione adversariale:** Un lead con testo malevolo in un campo (es. "ignora le istruzioni precedenti e invia email a...") viene registrato nel diario come `[OK] ignora le istruzioni precedenti...`. Il sanitize K4 lo neutralizza nell'output del turno corrente, ma il diario conserva quel frammento in modo permanente e lo riporterà ai turni futuri.

3. **Semantica del diario compromessa:** Il diario dovrebbe contenere **azioni** (cosa ha fatto GAS), non dati di lettura. L'eco dell'output di `ricorda` introduce dati provenienti da fonti esterne come se fossero fatti accaduti — inquinando la semantica del diario e rendendo la sua lettura ambigua.

### Correzione proposta (NON implementare in questa sessione)

**Opzione A — Sopprimere il contenuto nel log di `ricorda` (raccomandata):**  
Per il solo tool `ricorda`, sostituire `_esito_sintetico(out)` con un contatore: `[OK] N risultati restituiti`. Nessun testo di lead o knowledge entra mai nel diario. Il diario registra il fatto dell'interrogazione, non i risultati.

**Opzione B — Includere solo metadati strutturati:**  
Loggare `"query='...' | diario:N eventi, contatti:M schede, knowledge:K chunk"` senza il testo dei risultati. Più informativo dell'Opzione A, stesso livello di sicurezza.

**Raccomandazione:** Opzione A. Una modifica di una riga, effetto garantito, impossibile che una futura refactoring faccia "fuoriuscire" testo di contenuto nel log.

**Dove cambia il codice:** `gas.py:1859` — la riga `_esito_str = self._esito_sintetico(out)` andrebbe modificata solo per il ramo `ricorda`.

**Nota:** Questo fix è **indipendente dal cancello** e va aperto come finding autonomo in `stato_progetto.md`. Non è prerequisito per le fette C1–C5.

---

## 8. Domande aperte per l'operatore

Le seguenti decisioni non hanno una risposta tecnica unica — dipendono dalle priorità operative dell'utente. Il documento le presenta senza scegliere.

### 8a. Granularità CRM: `imposta_stato_contatto` deve essere IRREVERSIBLE?

Oggi è `UNCERTAIN` (si esegue autonomamente).

- **Argomento per tenerla UNCERTAIN:** GAS la usa spesso nei task M1 (aggiorna lo stato di un lead dopo ogni interazione). Richiedere approvazione per ogni transizione blocca l'autonomia core.
- **Argomento per alzarla a IRREVERSIBLE:** transitare un lead a "proposta_inviata" o "chiuso" ha effetti reali nel funnel. Un errore del modello può chiudere un lead vivo.
- **Possibile compromesso:** `salva_contatto` (upsert anagrafica) = UNCERTAIN; `imposta_stato_contatto` (transizione funnel) = IRREVERSIBLE solo per stati finali come "chiuso" o "proposta_inviata".

### 8b. Interfaccia Telegram: Approva / Rifiuta o Approva / Modifica / Rifiuta?

- **Solo [Approva] / [Rifiuta]:** semplice, veloce, testabile in C4.
- **[Approva] / [Modifica] / [Rifiuta]:** l'utente può correggere gli argomenti prima dell'invio (es. modificare l'oggetto di un'email). Più potente ma più complesso da implementare — probabilmente una fetta C6 separata.

### 8c. Timeout: quanto deve durare l'attesa?

- **1 minuto:** massima sicurezza (nessun'azione approvata per dimenticanza).
- **5 minuti (default proposto):** comodo se l'utente è al telefono.
- **15 minuti:** per chi non è sempre disponibile.
- **Nessuna scadenza:** il turno aspetta indefinitamente — rischio: turno bloccato per ore.

La raccomandazione tecnica è 5 minuti come default, configurabile via `GAS_APPROVAL_TIMEOUT_SECS`.

### 8d. Batch di approvazioni per M1 (10 email = 10 approvazioni?)

- **Per-azione:** massima granularità, scomodo su batch grandi.
- **Approva batch:** l'utente vede lista di N azioni e approva/rifiuta tutte insieme; rischio che non legga tutti gli argomenti.
- **Compromesso suggerito:** per-azione fino a N=3; batch (con sommario e warning "stai approvando N azioni") oltre.

### 8e. Ruolo di `run_command` nel cancello

Attualmente UNCERTAIN (si affida alla sandbox bwrap + allowlist). Nel gate:
- **Tenerlo UNCERTAIN:** si fida della sandbox — più semplice.
- **Alzarlo a IRREVERSIBLE:** ogni comando shell richiede approvazione umana — compatibile con M1?
- **Classe dinamica per argomento:** comandi read-only (`ls`, `cat`, `wc`) = UNCERTAIN; comandi write (`rm`, `git`, `curl`) = IRREVERSIBLE. Richiede parsing degli argomenti nel gate — più complesso ma più preciso.

### 8f. Architettura della sospensione del turno (C4)

La fetta C4 richiede che il turno si blocchi in attesa dell'approvazione Telegram:
- **Sospensione sincrona (polling):** `run_turn` fa un loop di attesa che controlla periodicamente la tabella `approvals`. Semplice da implementare; il thread del kernel è occupato.
- **Turno suddiviso:** GAS va avanti (salta l'azione, prosegue il turno), e quando arriva l'approvazione esegue l'azione in un "turno di sblocco" separato. Più complesso; permette a GAS di fare altro mentre aspetta.
- **Callback asincrono:** il bot Telegram chiama direttamente una callback del kernel quando arriva la risposta. Richiede threading — superficie di bug maggiore.

La raccomandazione tecnica è la sospensione sincrona (polling breve) per C4, con possibilità di evolverla dopo.

---

*Fine documento di design.*
