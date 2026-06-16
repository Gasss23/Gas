# 📄 REPORT — Memoria FASE 2: chiusura DOC + FETTA 2a (aggancio scrittura)

**Data:** 2026-06-16 · **Commit motore:** `7a75368` · **Suite:** 90/90, 0 FAIL (era 85)
**Review:** #13 — **APPROVATO CON RISERVE** (R1, R2 tracciate in `stato_progetto.md`)

---

## Esito in breve

Il diario della memoria è ora **agganciato al loop di `run_turn`, SOLO LATO SCRITTURA**.
Per ogni tool call eseguita, il kernel scrive UNA riga di diario in-process, esito
negativo incluso, in modo **fail-safe** (la memoria che non scrive non ferma mai il
turno). Il lato lettura/iniezione (fetta 2b) **NON è implementato**: è solo PROPOSTO nel
§FINALE. La blindatura del loop (`for _ in range(10)`, ordine fasi, finestra) è intatta.

---

## PARTE 1 — DOC (no motore)

1. **`CLAUDE.md` §10 FASE 2 → voce "Backup della memoria"**: il DB di memoria (file
   SQLite singolo, fuori da git) è il dato più prezioso e meno rimpiazzabile; la macchina
   del tempo snapshot NON lo copre (solo repo git, e il DB è gitignorato). `backup()`
   produce copia `.bak` LOCALE (protegge dall'auto-corruzione, NON dalla morte del disco);
   il backup OFF-MACHINE è da FASE 5/deploy VPS, banale perché DB = file singolo.
2. **`reports/stato_progetto.md`**: voce "fetta 2a ATTIVA" + decisioni di design
   **A** (diario logga OGNI tool call, esito incluso; filtro in LETTURA non in scrittura;
   contatti non scritti dal loop) e **B** (iniezione always-on = contatti attivi + pochi
   eventi recenti filtrati, budget ~3000 char DENTRO `WINDOW_CHAR_CAP`, diario profondo
   via tool `ricorda()`). Riserve R1/R2 review #13 registrate.

---

## PARTE 2 — BUILD fetta 2a (motore, lato scrittura)

- **`gas.py` `__init__`**: `self.memory = MemoryStore(default_db_path(self.root))`, doppia
  cintura fail-safe (degrado `available=False` o init fallita → `self.memory=None`); il
  resto del kernel funziona comunque, mai crash.
- **Loop `run_turn`**: per OGNI tool call, DOPO l'esecuzione (cattura l'esito), una riga di
  diario in-process via `_diario_log` → `MemoryStore.append_diario`. `tipo` = nome tool;
  `descrizione` = sintesi argomenti + esito sintetico (`[OK]`/`[KO]`).
- **Vincoli**: contatti non toccati dal loop; scrittura IN-PROCESS (bypassa correttamente
  il sandbox bwrap); fail-safe §9 (append fallita → warning, turno CONTINUA); `for _ in
  range(10)` invariato; nessuna simulazione di tool, nessuno slicing grezzo.

---

## VERIFICHE (eseguite dal vivo, output integrale)

### A. Suite completa — 90 PASS, 0 FAIL (era 85 → +5 T20)

```
[PASS] T19i DB assente -> creato e operativo
[PASS] T19j DB corrotto -> degrada senza crash
[PASS] T20a round-trip multi-tool: 1 riga/diario per tool, ordine giusto — n=3 tipi=['write_file', 'write_file', 'read_file'] final=1
[PASS] T20b esiti positivi marcati [OK] — esiti=['[OK] Successo: File uno.txt aggiornato.', '[OK] Successo: File due.txt aggiornato.', '[OK] 1']
[PASS] T20c tool fallito -> diario [KO] e turno NON interrotto — diario=path='non_esiste.txt' | [KO] Errore eseguendo read_file: [Errno 2] No such file  final=1
[PASS] T20d memoria degradata -> round-trip OK, turno non interrotto — available=False final=1
[PASS] T20e memoria None -> nessun crash, turno completato

=== RIEPILOGO: 90 PASS, 0 FAIL ===
```

### B. Round-trip agentico (§7 — punto critico, test REALI zero token)

1. **Multi-tool → una riga per ogni tool nell'ordine giusto** (T20a): script con 3 tool in
   un solo messaggio assistant (write `uno.txt`, write `due.txt`, read `uno.txt`) → diario
   con 3 righe, tipi `['write_file','write_file','read_file']` in ordine cronologico, +1
   evento `final`. **PASS.**
2. **Tool che FALLISCE → diario registra l'esito negativo E il loop prosegue** (T20c):
   `read_file` su file inesistente → riga diario `[KO] Errore eseguendo read_file...`,
   1 evento `final`, 0 errori di pipeline. **PASS.**
3. **Memoria degradata → il round-trip funziona comunque** (T20d, DB corrotto →
   `available=False`; T20e, `self.memory=None`): in entrambi il turno arriva a `final`, il
   file viene scritto, il diario resta `[]` ma **nessun crash**. **PASS.**

### C. Prova-di-scope (commit motore `7a75368`)

```
 gas.py                    |  65 +++++++++++++++++++++++++++++
 tests/test_unit_kernel.py | 102 ++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 167 insertions(+)
```

- `git show 7a75368 -- gas.py | grep` sulle funzioni sensibili →
  **NESSUNA riga +/- tocca** `_get_window`, `_cap_window_chars`, `_bwrap_prefix`,
  `_snapshot`, `_vet_command`, `providers`.
- `store.py` **NON toccato** → schema memoria fetta 1 INVARIATO.
- **167 inserzioni, 0 cancellazioni**: il diff è puramente additivo → pipeline provider,
  sandbox, snapshot e la finestra sono INVARIATI. **Scope rispettato.**

### D. Prova-che-il-diario-si-popola (dump reale dopo un round-trip)

Round-trip con 4 tool (write, read OK, read KO, run_command in bwrap) → dump di
`diario_recente` (più recente prima):

```
EVENTI: ['tool_res', 'tool_res', 'tool_res', 'tool_res', 'final']

  id=4  tipo=run_command   command='wc -l piano.txt' | [OK] 0 piano.txt
  id=3  tipo=read_file     path='manca.txt' | [KO] Errore eseguendo read_file: [Errno 2] No such file or directory: '.../manca.txt'
  id=2  tipo=read_file     path='piano.txt' | [OK] lead Mario
  id=1  tipo=write_file    path='piano.txt' | [OK] Successo: File piano.txt aggiornato.
```

Una riga per tool, esiti OK/KO reali, incluso `run_command` eseguito davvero in sandbox
bwrap (rete chiusa, fs read-only) — la scrittura del diario è in-process e lo bypassa.

---

## §FINALE — PROPOSTA fetta 2b (lato lettura/iniezione) — NON implementata

> Solo design per la prossima fetta. Nessun codice scritto, nessun cablaggio.

### (1) Cosa entra nell'iniezione always-on
- **Contatti ATTIVI** (stato NON in `STATI_CHIUSI`, da `lista_contatti` filtrata):
  per ciascuno pochi campi essenziali e ad alto valore → `nome`/`chiave`, `stato`,
  `prossima_azione`, `ultimo_contatto` (data). NON le `note` lunghe né l'anagrafica
  completa (vanno pescate on-demand). Cap al numero di contatti (es. i ~10 più recenti per
  `aggiornato_il`) per non sfondare il budget.
- **Pochi eventi diario RECENTI** (es. ultimi 5–8 da `diario_recente`), **filtrati per
  escludere il rumore di lettura**: scartare `tipo` ∈ {`read_file`, `run_command` di sola
  consultazione} e gli esiti `[KO]` ripetitivi; tenere gli eventi "che cambiano il mondo"
  (write, transizioni di stato, messaggi inviati). NB: il filtro vive QUI (lettura), non in
  scrittura — il diario resta completo a monte (decisione A), così niente informazione persa.

### (2) Come comporre il messaggio-memoria pinnato con `WINDOW_CHAR_CAP=24000`
- Il blocco memoria è un **messaggio di sistema/contesto PINNATO**, budget ~3000 char,
  costruito a parte (non passa dal diario grezzo).
- Vincolo "la finestra parte sempre da un `role:user` coerente": il pin **NON deve entrare
  nello scarto** di `_cap_window_chars` né rompere l'allineamento iniziale. Proposta:
  iniettarlo come blocco separato (es. appeso al `system_prompt`, già fuori dalla finestra
  conversazionale, oppure come messaggio dedicato a monte) **e sottrarre i suoi char dal
  cap** prima di chiamare `_cap_window_chars`, così il tetto reale della finestra
  conversazionale diventa `WINDOW_CHAR_CAP - len(pin)`. Punto d'inserimento: **a valle di
  `_get_window`/`_cap_window_chars`** (che restano INVARIATI), in fase di assemblaggio del
  `payload`, prima di `client.chat.completions.create`. Mai dentro `_get_window`: si evita
  di toccare la logica blindata e si tiene il pin fuori dallo scarto/riallineamento.
- **Rischio da gestire**: se il pin gonfia troppo, va capato lui stesso PRIMA (troncamento a
  granularità di campo/evento, mai slicing grezzo §5), non rosicchiando la conversazione.

### (3) Tool `ricorda()` di sola lettura
- **Firma proposta**: `ricorda(query: Optional[str]=None, contatto: Optional[str]=None,
  n: int=10) -> str` (tool esposto nello `tools_schema`, accanto a read_file/run_command).
- **Cosa pesca**: il diario PROFONDO on-demand (`diario_recente`/`diario_di_contatto`) e/o
  i dettagli completi di un contatto (`get_contatto`/`lista_contatti`) — ciò che NON sta
  nell'iniezione always-on. È SOLA LETTURA: nessuna scrittura, nessuna mutazione.
- **Come evita di gonfiare la finestra**: l'output passa per `_cap_tool_output` come ogni
  altro tool (già capato a 8000 char); inoltre `ricorda` ritorna un riassunto compatto
  (campi essenziali, `n` limitato) invece del dump integrale. È pull esplicito del modello,
  non push permanente → la profondità non resta pinnata.

### (4) Rischi sul round-trip da cablare con cura nella lettura (2b)
- **Coerenza della finestra / Gemini 400**: il pin va inserito senza creare tool result
  orfani né spostare il `role:user` iniziale; va testato che `_get_window` + pin non
  produca sequenze che fanno 400 (replicare i test T3/T4 col pin attivo).
- **Budget**: doppio conteggio char (pin + finestra) → garantire `pin + window ≤ cap`
  sempre, anche quando il pin è grande (capare il pin per primo).
- **Loop a 10 iterazioni**: il pin viene ricostruito a ogni iterazione (la memoria può
  cambiare mid-turn se un tool scrive) → costo di query ripetute; valutare di costruire il
  pin UNA volta per turno o con cache breve, senza rompere l'aggiornamento.
- **Auto-riferimento del diario**: gli eventi scritti DURANTE il turno corrente potrebbero
  rientrare subito nell'iniezione → eco/rumore; il filtro per `tipo`/recency deve evitarlo.
- **Fail-safe**: lettura degradata (DB assente/corrotto) → il pin deve diventare vuoto e il
  turno proseguire (stesso principio §9 della scrittura). Da testare come T20d/e ma in lettura.

---

## Stato finale
- **Fetta 2a (aggancio scrittura): ATTIVA.** Fetta 2b (lettura/iniezione): **PROPOSTA, non
  implementata.** Suite 90/90. Review #13 APPROVATO CON RISERVE (R1/R2 in stato_progetto).
