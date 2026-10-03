# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-03 — FETTA C4b-1: notifica Telegram di read-back + anti-doppioni + tetto + R-c3-3/R-c3-4 (branch `feat/cancello-c4b1`)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #113 (https://github.com/Gasss23/Gas/pull/113). Merge vietato all'agente: lo fa l'operatore con gasmerge.
2. Test manuale reale Telegram NON fatto: `TELEGRAM_BOT_TOKEN` e `TELEGRAM_ALLOWED_IDS` assenti sia in `.env` sia nell'ambiente. Per farlo vanno aggiunti a `.env`, MA prima va chiusa R-c4b1-1 (con il token esportato la suite manda circa 40 read-back reali).

---

## §1 SCOPE & ESITO FETTE

- **PASSO 0 — revisore su Opus**: `FATTA` — `model: opus` nel frontmatter, commit separato `b8bf2ef`, solo `.claude/agents/revisore.md`.
- **PASSO 1 — sonda**: `FATTA` — nessun conflitto bloccante col design. Riferimenti: `reports/design_cancello.md:211` (§4b), `:259` (§4c), `:291` (§4e), `:298` (§4f); enqueue `gas.py:1952` e bot `modules/telegram/bot.py:40` sul codice di partenza `4284a9c` (dettaglio in ultimo_report.md).
- **PASSO 2 — anti-doppioni + tetto**: `FATTA` — `accoda_approvazione` atomica, doppione → stesso ID, tetto `GAS_APPROVAL_MAX_PENDING` (default 5).
- **PASSO 3 — read-back (solo invio)**: `FATTA` — niente parse_mode, args integrali, oltre 4096 / config mancante / invio fallito → revoca + diniego; diario senza args.
- **PASSO 4 — R-c3-3 / R-c3-4**: `FATTA` — chiuse.
- **Test a)–g)**: `FATTA` — T75a-f (51 check), T74a-g verdi.
- **Test manuale reale Telegram**: `SALTATA — token e ID Telegram assenti in .env e nell'ambiente`.
- **Bottoni/callback, esecuzione post-approvazione, worker di scadenza, tetto CRM C-d**: `DEFERITA — fuori scope per prompt (C4b-2 / C5 / C-d)`.

C4b-1 fatto, C4b-2 (bottoni + esecuzione) NON fatto, deploy autonomo ancora vietato.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 .claude/agents/revisore.md         |   1 +
 gas.py                             | 120 +++++++++-----
 modules/memory/store.py            | 149 +++++++++++++++--
 modules/telegram/bot.py            |  91 +++++++++--
 reports/diff_sessione.md           |  57 ++-----
 reports/handoff.md                 | 161 ++++++------------
 reports/stato_progetto.md          |  17 +-
 reports/ultimo_report.md           | 130 +++++++++------
 tests/test_unit_kernel.py          | 324 +++++++++++++++++++++++++++++++++++--
 10 files changed, 775 insertions(+), 277 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
e3b8459 chore(revisore): memoria review #128 — APPROVATO CON RISERVE
db964b2 feat(cancello-c4b1): read-back Telegram + anti-doppioni + tetto pending + R-c3-3/R-c3-4 — review #128 APPROVATO CON RISERVE
b8bf2ef chore(revisore): model: opus nel frontmatter (decisione operatore 2026-10-01)
```

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore `db964b2` — review #128 — verdetto INTEGRALE incollato:

## Verdetto review #128 — FETTA C4b-1 (feat/cancello-c4b1, diff STAGED, 4 file)

**ESITO: APPROVATO CON RISERVE**

Letture fatte: CLAUDE.md (§5, §8, §9), reports/stato_progetto.md (Grep mirato su C4/cancello/R-c3), .claude/agents/memoria_revisore.md (ultime 40 righe, contatore a #127).

### Conteggi riprodotti
- `.venv/bin/python tests/test_unit_kernel.py`: **552 PASS / 5 FAIL**. I 5 FAIL sono T11c2, T11e, T12a, T12c, T12e (F-mac-1, bwrap su macOS), come dichiarato.
- pytest (escluso test_unit_kernel.py ed e2e): **227 passed**.

### Elementi del diff esaminati (file:riga)
1. `gas.py:1261` — `_parcheggia_e_notifica` chiama `accoda_approvazione` dentro try/except. Le eccezioni portano a "errore" e quindi a un diniego fail-closed. `self.memory is None` porta a un diniego prima della chiamata. Rischio esaminato: eccezione del provider/store che arriva al loop (§9), oppure tool eseguito al cancello. **ok**: nessun ramo chiama `execute_tool_call`, e T74e/T74f restano verdi.
2. `gas.py:1287` / `gas.py:1297` / `gas.py:1303` — controllo della lunghezza in unità UTF-16 prima dell'invio. Se il motivo non è vuoto, la richiesta viene revocata con `revoca_approval`, sempre dentro try. Se la revoca fallisce resta un WARN (scelta 6). Rischio esaminato: una pending di cui l'operatore non sa niente. **ok**: tutti i percorsi di fallimento (oltre 4096, token mancante, ID mancanti, eccezione, ok=False) portano a rejected/kernel_revoca, verificato da T75d/T75e. Il residuo della scelta 6 è accettabile perché la riga non è approvabile senza bottoni e scade.
3. `modules/memory/store.py:1551` e `:1558` — la query del doppione viene PRIMA del COUNT del tetto, tutte e due dentro la stessa transazione `BEGIN IMMEDIATE`, con `now` letto dopo il lock. Rischio esaminato: race tra controllo e INSERT, oppure un doppione negato a tetto pieno. **ok**: è atomico. T75b ("doppione a tetto pieno → stesso ID") copre l'ordine.
4. `modules/memory/store.py:1628` / `:1633` — R-c3-3: `approved` solo con `risolto_da="telegram_user"`. R-c3-4: `rejected` solo con un int o con None (bool escluso). Tutte e due le verifiche avvengono PRIMA della connessione, quindi senza scritture. **ok**: R-c3-3 e R-c3-4 sono CHIUSE, con T75f che verifica lo stato del DB invariato.
5. `modules/memory/store.py:1686` — `revoca_approval`, un wrapper che può solo rifiutare. Ho fatto `grep resolve_approval gas.py` e non trova nulla, quindi l'invariante T73f resta vero senza modificarlo. **ok**: è la scelta 2, ed è giusta. Il kernel non ha alcun percorso che porti ad 'approved'.
6. `modules/telegram/bot.py:118`–`:141` — `invia_read_back`. Il payload contiene solo `{chat_id, text}`, quindi niente parse_mode. Il messaggio è considerato riuscito se almeno un destinatario risponde ok=True. Il dettaglio delle eccezioni va solo nel log. **ok, ma con la riserva R-c4b1-2** (anteprima dei link).
7. `tests/test_unit_kernel.py:4777` e seguenti — `_TgFinto` sostituisce SOLO `bot._tg_post` e salva e ripristina l'env. **ok**, ma vedi R-c4b1-1.

### Riserve
- **R-c4b1-1 (da chiudere prima del deploy su VPS): la suite non è ermetica.** L'ho misurato con un sitecustomize che sostituisce `_tg_post` e con `TELEGRAM_BOT_TOKEN=REALE TELEGRAM_ALLOWED_IDS=999` nell'env. Durante la suite partono **40 sendMessage FUORI da `_TgFinto`**, tutti read-back di `run_command`, che vengono dai test esistenti T11/T12 e simili che passano dal cancello. In dev e in CI il token non c'è, quindi oggi è innocuo: questi test passano dal ramo di revoca. Ma se la suite gira dove il token è esportato (VPS/systemd o shell dello sviluppatore), l'operatore riceve 40 richieste di firma reali, con fino a 15 s di timeout ciascuna. Fix: in testa a test_unit_kernel.py, `os.environ.pop` di TELEGRAM_BOT_TOKEN e TELEGRAM_ALLOWED_IDS, più un `_tg_post` che fallisce di default.
- **R-c4b1-2 (sicurezza del read-back, minore): l'anteprima dei link non è disabilitata.** Senza `link_preview_options={"is_disabled": true}` (o `disable_web_page_preview`), un URL di terzi dentro `tool_args_json` diventa una card con titolo, descrizione e immagine scelti da chi controlla l'URL. La card appare dentro il messaggio di firma. È lo stesso rischio che ha motivato il divieto di parse_mode: contenuto che altera la presentazione del read-back. Quando si chiude, va aggiornato anche T75c (`set(_pl75c) == {"chat_id","text"}`).
- **R-c4b1-3 (osservabilità/latenza, minore):** l'invio è sincrono dentro run_turn, con `timeout=15` per ogni ID. Se Telegram non risponde, il turno resta bloccato fino a 15 s × N destinatari. Non è un crash, ma va tenuto presente per il bot h24.
- **R-c4b1-4 (minore, fail-closed):** se una riga corrotta ha `ts_expiry` TEXT, `ts_expiry > ?` dà sempre vero (in SQLite un TEXT è maggiore di un REAL). La riga quindi conta nel tetto e partecipa al doppione finché `expire_stale_approvals` non la scade, e oggi nessuno la chiama dal loop. È raggiungibile solo con SQL grezzo e va nella direzione del diniego, quindi non blocca.

### Giudizio sulle 8 scelte implementative
1. Il metodo separato `accoda_approvazione` con `enqueue_approval` lasciato senza dedup è corretto. T73a e F-c4a-dedup restano invariati e misurano ancora la primitiva. Il doppione controllato prima del tetto è giusto.
2. `revoca_approval` è preferibile a modificare T73f: l'invariante resta meccanico.
3. Basta un destinatario: accettabile, ed è il comportamento coperto da T75e.
4. Il conteggio UTF-16 con il confine 4096 incluso è corretto e testato (emoji = 2, 4096 ammesso, 4097 no).
5. Non restituire il testo delle eccezioni al modello è giusto, e T75e verifica che il token non compaia mai nell'esito.
6. Il residuo della revoca fallita è accettabile, dichiarato e loggato.
7. `parse_allowed_ids` è un refactor equivalente: i WARN di run_bot restano.
8. Il diario non contiene mai gli args su nessun ramo del cancello. Su gate-fail-closed è un miglioramento rispetto a prima.

### Test esistenti modificati: adeguamento LEGITTIMO, non li indebolisce
- **T70f, T70g, T72c, T74a, T74b** (es. `tests/test_unit_kernel.py:5002`, `:5429`): con `with _TgFinto():` lo store, la composizione e `invia_read_back` restano codice reale, e viene sostituito solo il trasporto HTTP. Le asserzioni sono invariate e continuano a verificare il percorso "pending". Senza il finto, la nuova semantica corretta è la revoca. Il wrapper riallinea il test al percorso che il test voleva coprire e non maschera nulla.
- **T74e**: spostare il monkeypatch su `accoda_approvazione` è necessario, perché il kernel ora chiama quel metodo. Lasciarlo su `enqueue_approval` renderebbe il test vacuo. Le asserzioni sono invariate. Legittimo.
- I nuovi test T75a-f sono discriminanti: verificano lo stato del DB, il numero di chiamate HTTP e il payload esatto. Non ho ripetuto le mutazioni già fatte dall'operatore. Leggendo il codice, T75f cadrebbe se si rimuovessero le verifiche di `:1628`/`:1633`, e T75b ("doppione a tetto pieno") cadrebbe se si invertisse l'ordine doppione/tetto.

### Rischio esplicitamente escluso
- Non ho verificato il comportamento reale verso l'API Telegram (consegna effettiva, rendering del testo, conteggio della lunghezza lato server, anteprime): richiederebbe un token e una chat reali, che non sono disponibili in dev.
- Non ho verificato la concorrenza reale tra due processi (bot e CLI) su `BEGIN IMMEDIATE`: in un solo processo non si riproduce. Per costruzione, l'atomicità è garantita dal lock RESERVED di SQLite.

### Wall of Shame
Nessuna violazione. Nessuno slicing della history: il diff non tocca `_get_window` o `_cap_window_chars`. Nessuna simulazione dell'output dei tool: `_TgFinto` è un finto trasporto HTTP nei test, non l'output di un tool dato al modello. Il cap di 10 iterazioni non è toccato.

### Memoria
Ho aggiunto la riga contatore #128 e una lezione datata in coda a `/Users/gas/Gas/.claude/agents/memoria_revisore.md`. Come da tua istruzione NON l'ho committata (non ho eseguito `scripts/commit_memoria_revisore.sh`): il commit spetta a te.

## §5 DELTA TEST DEL MOTORE

Locale (macOS): **501 PASS / 5 FAIL → 552 PASS / 5 FAIL** (+51 = T75a-f). I 5 FAIL sono fuori scope e identici prima e dopo: F-mac-1 (bwrap assente su macOS).

```
=== RIEPILOGO: 552 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

pytest (escluso test_unit_kernel.py ed e2e): 227 passed prima e dopo.

Test esistenti modificati (giudicati dal revisore "adeguamento LEGITTIMO, non li indebolisce"): T70f, T70g, T72c, T74a, T74b (aggiunto `with _TgFinto():`, asserzioni invariate); T74e (monkeypatch spostato su `accoda_approvazione`, asserzioni invariate).

## §6 STATO CI

```
completed	success	chore(revisore): memoria review #128 — APPROVATO CON RISERVE	CI	feat/cancello-c4b1	push	37087223516	1m3s	2026-10-03T01:44:07Z
completed	success	Merge pull request #112 from Gasss23/feat/cancello-c4a	CI	feat/cancello-c4b1	push	37086286553	52s	2026-10-03T01:29:28Z
completed	success	Merge pull request #112 from Gasss23/feat/cancello-c4a	CI	main	push	37084935616	53s	2026-10-03T01:08:26Z
```

Mappatura commit → run:
- `e3b8459` (testa del push) → run 37087223516, **success** (headSha `e3b845922287fe04092cbdc528ec6b73b044218f`). Log: `=== RIEPILOGO: 561 PASS, 0 FAIL ===` (ubuntu, bwrap attivo: smoke-test 2 BWRAP_OK); hook 51 passed, voice 19 passed, gate 74 passed.
- `db964b2` → nessuna run su questo SHA (pushato insieme a `e3b8459`; il suo albero è incluso in quello testato).
- `b8bf2ef` → nessuna run su questo SHA (pushato insieme a `e3b8459`).
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-c4b1-1** (review #128, da chiudere prima del deploy e prima del token in `.env`): suite non ermetica. Con il token reale esportato partono circa 40 sendMessage reali dai test esistenti che passano dal cancello.
- **R-c4b1-2** (minore): anteprima dei link non disabilitata nel read-back.
- **R-c4b1-3** (minore): invio sincrono nel turno, 15 s × N ID nel caso peggiore.
- **R-c4b1-4** (minore, fail-closed): una riga corrotta con ts_expiry TEXT conta nel tetto e nel doppione.
- Finding registrati dalla verifica C4a: F-c4a-eco, R-c4a-1 sottostimata (ora coperta), handoff C4a §6 errato, R-c3-1b "mitigata", scrivi_rep.sh su main, messaggio SessionEnd "Auto-commit...", /agents rimosso (dettaglio in stato_progetto.md).
