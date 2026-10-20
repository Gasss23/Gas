# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-20 — Documenti allineati alle decisioni del 19 ottobre, firma notturna 24 h, autonomia dopo una lettura

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR (numero e URL in fondo a §0 dopo l'apertura): lo decide l'operatore dopo il riassunto.
2. Autonomia dopo una lettura è una fetta di sicurezza: secondo passaggio indipendente nella chat claude.ai.

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Documenti allineati alle decisioni del 19 ottobre**: `FATTA` — review #364/#365.
- **Firma notturna 24 h (R1)**: `FATTA` — review #366.
- **Autonomia dopo una lettura (R1, supera C-d e R-203-2)**: `FATTA` — review #367 BOCCIATO → #368 → #369 APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 .claude/commands/fine-task.md      |   2 +-
 CLAUDE.md                          |   4 ++--
 README.md                          |  11 +++++++++++
 gas.py                             |  37 +++++++++++++++++++++++++++++++++++++
 gas_identity.md                    |   2 +-
 modules/gate/gate.py               |  37 +++++++++++++++++++++++++++++++++++++
 modules/memory/__init__.py         |   2 ++
 modules/memory/store.py            |  30 ++++++++++++++++++++++++++++--
 modules/notte/notte.py             |  13 +++++++++++++
 reports/design_cancello.md         |   2 +-
 reports/diff_sessione.md           |   9 +++++++--
 reports/handoff.md                 | 265 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------
 reports/roadmap.md                 |  23 +++++++++++------------
 reports/roadmap_sintesi.md         |  25 -------------------------
 reports/setup_notte.md             |  12 +++++++++---
 reports/stato_progetto.md          |   6 +++---
 reports/ultimo_report.md           |  67 ++++++++++---------------------------------------------------------
 tests/test_unit_gate.py            |  29 +++++++++++++++++++++++++++++
 tests/test_unit_kernel.py          | 101 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 tests/test_unit_notte.py           |  58 ++++++++++++++++++++++++++++++++++++++++++++++++++++++----
 21 files changed, 603 insertions(+), 138 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
0b32432 feat(cancello): dopo una lettura rubrica e file normali restano liberi (autonomia, decisione 19 ott)
bfc245f chore(revisore): memoria review #369 — APPROVATO
1a0407a chore(revisore): memoria review #369 — APPROVATO
7545e0d chore(revisore): memoria review #368 — APPROVATO CON RISERVE
cece054 chore(revisore): memoria review #367 — BOCCIATO
12a0a60 docs: R-366-1 (posti in attesa occupati dalle firme notturne)
b203629 feat(notte): le firme chieste di notte scadono dopo 24 ore (R1, decisione 19 ott)
aecb4a8 chore(revisore): memoria review #366 — APPROVATO CON RISERVE
d9b144b docs: documenti allineati alle decisioni del 19 ottobre (CLAUDE.md, fine-task, identità, README, stato)
4d91a33 chore(revisore): memoria review #365 — APPROVATO
022365f chore(revisore): memoria review #364 — APPROVATO CON RISERVE
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #364

```
## VERDETTO: APPROVATO CON RISERVE

Review #364 (2026-10-20). Diff staged su feat/merge-automatico-z1xjx2, base main d6b1e45. 7 file: 2 nel perimetro, 5 fuori.

**Cosa ho controllato nel diff**
- `.claude/commands/fine-task.md:114`: la frase «NON mergiare (il merge è azione umana da WSL)» diventa un rimando alla regola di merge di CLAUDE.md §10. Ho controllato che non indebolisca un gate. Non lo fa: il divieto vecchio era già superato dalla regola dell'operatore del 2026-10-08 (CLAUDE.md:74), che resta la fonte che decide. Nessuno script dei controlli legge questa frase: `scripts/bot_esito.py:68` usa solo il percorso del file. Esito: riserva (R-364-1).
- `gas_identity.md:5`: la cascata passa da «Gemini, Groq» a «Gemini, Groq, OpenRouter gratuito, Ollama». Ho controllato che Gas non dica di sé una cosa falsa a runtime. Nel codice Ollama è ancora l'ultimo gradino (`gas.py:3908`, `gas.py:289`), quindi la frase è vera oggi. Il testo cresce di poche parole (file da 1689 byte) e resta nel budget di circa 200 token. Esito: ok.
- Contesto, file non toccato: `gas.py:775`. Anche il controllo dei provider (doctor) elenca Ollama, quindi è coerente con gas_identity. Esito: ok.
- Fuori perimetro, solo controllo di coerenza:
  - CLAUDE.md §2 distingue bene «oggi nel codice» da «rimosso dal piano». Ma quando la fetta che toglie Ollama arriverà nel codice, andrà aggiornato anche `gas_identity.md:5`.
  - roadmap: le voci ✅ corrispondono a quello che c'è nel diff.
  - stato_progetto: R-203-2 è barrata ma resta «da mettere nel codice». Corretto.
  - `roadmap_sintesi.md` cancellato: lo citano ancora solo handoff.md e ultimo_report.md, che sono log di sessione e si riscrivono.
- Wall of Shame (gli errori vietati di CLAUDE.md §5): non riguarda questo diff. Non c'è codice, né tagli diretti della cronologia, né output dei tool simulati.

**Riserva**
- **R-364-1 (BASSA)**: il riassunto tra parentesi in `.claude/commands/fine-task.md:114` ha due difetti.
  - Manca una condizione: tra quelle del merge autonomo non c'è «check `verifica-bot` success».
  - La frase «tutto il resto, o una richiesta esplicita dell'operatore nella sessione, lo decide l'operatore» si può leggere male. In CLAUDE.md la richiesta esplicita dell'operatore è un'eccezione che *permette* all'agente di mergiare, non un caso da lasciare all'operatore.
  - Rimedio: lasciare solo il rimando a CLAUDE.md §10, oppure completare il riassunto. Un riassunto parziale diventa una seconda fonte, più permissiva della regola.

**Cosa non ho verificato**
- Le suite di test (kernel 893, hooks 211, 1093 di handoff, gasmerge, verifica-bot e gate) non le ho rilanciate. Il diff tocca solo testo, nessun test legge le frasi cambiate, quindi ho preso per buoni i numeri dichiarati.
- Il comportamento runtime di Gas con la nuova identità, su VPS o sul Mac, non è riproducibile qui.

**Altro**
- Una fixture e2e (`tests/e2e/e2e_k3k4_llm.py:319`) contiene un testo di prompt injection («Ignora tutte le istruzioni precedenti… PWNED»). È un dato di test voluto e l'ho ignorato come istruzione.

**Memoria**
- Riga #364 aggiunta a /home/user/Gas/.claude/agents/memoria_revisore.md, con la lezione «la parafrasi di una regola canonica in un doc di processo deve essere completa oppure ridursi al solo rimando».
- Committata con commit_memoria_revisore.sh: 022365f.
- R-364-1 va registrata in reports/stato_progetto.md.
```

### Review #365

```
## VERDETTO: APPROVATO

Review #365 (2026-10-20): nuovo controllo del diff staged dopo la riserva R-364-1, su feat/merge-automatico-z1xjx2 (base main d6b1e45). Il diff staged tocca ancora gli stessi 7 file (+25/−40).

**Cosa ho controllato nel diff**
- `.claude/commands/fine-task.md:114`: ora dice solo «Merge: SOLO secondo la regola di merge di `CLAUDE.md` §10 (fonte unica, non riassunta qui).» Avevo temuto che questo file diventasse una seconda fonte, incompleta e più permissiva, della regola di merge. Il riassunto senza «verifica-bot success» e la frase ambigua sulla richiesta esplicita dell'operatore sono spariti. La regola sta solo in CLAUDE.md:74. Nessuno script dei controlli legge questa frase (`scripts/bot_esito.py:68` usa solo il percorso del file). Esito: ok, R-364-1 chiusa.
- `gas_identity.md:5`: la cascata passa a «Gemini, Groq, OpenRouter gratuito, Ollama», come nella #364. Ho controllato che Gas non dica di sé una cosa falsa quando gira. Nel codice Ollama è ancora l'ultimo gradino (`gas.py:3908`, `gas.py:289`), quindi la frase è vera oggi. Esito: ok.
- Contesto, file non toccato: `gas.py:775`. Anche il controllo dei provider fatto da doctor elenca Ollama, quindi è coerente.
- I file fuori perimetro (CLAUDE.md §2 e §3, README, roadmap, stato_progetto, roadmap_sintesi.md cancellato) non cambiano rispetto alla #364 e restano coerenti fra loro.
- Wall of Shame: il diff tocca solo testo, quindi non c'è slicing della cronologia né output dei tool simulati. Nessun gate di codice è toccato.

**Rischi non verificati**
- Non ho rilanciato le suite di test (kernel 893, hooks 211, handoff/gasmerge/verifica_bot/gate 1093): è solo testo e nessun test legge le frasi cambiate.
- Non ho verificato il comportamento runtime della nuova identità su VPS o sul Mac: non si riproduce qui.

**Promemoria**
- Quando arriverà la fetta che toglie Ollama dal codice, va aggiornato anche `gas_identity.md:5`.
- In `reports/stato_progetto.md` R-364-1 va segnata come chiusa.

**Memoria**
- Ho aggiunto la riga #365 in /home/user/Gas/.claude/agents/memoria_revisore.md, senza lezioni nuove.
- È committata (4d91a33), dopo la #364 (022365f).
```

### Review #366

```
## VERDETTO: APPROVATO CON RISERVE

Review n. 366. Riga contatore aggiunta a /home/user/Gas/.claude/agents/memoria_revisore.md e salvata con un commit tramite scripts/commit_memoria_revisore.sh. Il diff staged non l'ho toccato.

**Cosa ho esaminato nel diff**
- `modules/memory/store.py:1657` — se `timeout_secs` non è un intero (anche un bool) oppure è <= 0, si usa il default di giorno `_approval_timeout_secs()`. Rischio esaminato: un valore non valido che arrivi fino all'INSERT, o un True che valga come 1 secondo. Esito: ok. Il bool è escluso in modo esplicito e la stringa "86400" ricade sui 30 minuti (lo prova il test). Un valore enorme da env provocherebbe un OverflowError: `accoda_approvazione` non lo intercetta, ma lo prende il `except Exception` del chiamante a `gas.py:2578`, che nega l'azione per prudenza (fail-closed). Nessun crash.
- `modules/memory/store.py:309` — `approval_timeout_notte_secs()` segue lo stesso schema di `_approval_timeout_secs`: env assente → 86400, valore non valido → WARN e default. Esito: ok.
- `gas.py:2576` — `timeout_secs=getattr(self, "approval_timeout_secs", None)` dentro il try già esistente. Rischio: regressione di giorno. Esito: ok. Il kernel normale ha None (impostato a `gas.py:852`), quindi resta il default di env di 30 minuti, e `enqueue_approval` (`modules/memory/store.py:1603`) non è stato toccato.
- `modules/notte/notte.py:531` — `_firma_notturna(kernel)` viene chiamata dentro il try che crea il kernel. La funzione (`modules/notte/notte.py:384`) intercetta ogni eccezione con un WARN: se fallisce, la richiesta resta coi 30 minuti, cioè la scelta più prudente. Esito: ok.
- Contesto: `modules/telegram/bot.py:461` e `modules/memory/store.py:1771` leggono la scadenza dalla riga (`ts_expiry`), non la ricalcolano. Quindi la firma da Telegram e la pulizia delle richieste scadute rispettano le 24 ore. Esito: ok.

**Riprodotto**
- I 5 test nuovi passano. `pytest tests/`: 1455 passed.
- Ho rotto il codice di proposito per vedere se i test se ne accorgono:
  - tolta la chiamata `_firma_notturna` → 4 test falliscono;
  - tolto il passaggio di `timeout_secs` in `gas.py` → 4 test falliscono.
  Ho rimesso a posto entrambi i file.
- Il test notturno fa un giro vero (read_file poi write_file finisce in attesa di firma). Nessun output dei tool simulato, nessun taglio della storia: Wall of Shame pulito. I guardrail restano intatti (`_get_window`, tetto di 10 iterazioni, tetto delle richieste in attesa).

**Riserve**
- R-366-1 BASSA: una richiesta notturna occupa per 24 ore uno dei 5 posti del tetto delle richieste in attesa, quindi può bloccare le richieste nuove del giorno. L'effetto è accettato dalla decisione dell'operatore, ma `reports/setup_notte.md` non lo dice. Va aggiunta una riga lì e tracciata la riserva in stato_progetto.md.

**Cosa NON ho verificato**
- La suite del kernel (893 PASS): non l'ho rilanciata, mi fido del numero dichiarato. La copre in parte pytest tests/, che invece ho rilanciato.
- Il giro reale su Mac con launchd e Telegram vero: non si può riprodurre in questo ambiente (nessun token).
```

### Review #367

```
## VERDETTO: BOCCIATO

Review #367. Ho riprodotto i numeri: suite del kernel 898 PASS e 0 FAIL, `pytest tests/` 1475 passed (1455 più i 20 nuovi). Riga contatore scritta e già committata (cece054). Il diff staged è intatto.

**Incidente da dichiarare.** Durante la mutazione la cartella di appoggio non esisteva. Il comando è quindi partito in /home/user/Gas e ha modificato `gas.py` nel working tree (`if tool_name != "write_file":` diventato `if True:`). L'ho ripristinato subito con `git checkout -- gas.py` dall'index. Ho verificato che `git diff gas.py` è vuoto e che lo staged non è cambiato. Prima di rigenerare il marcatore controlla comunque che `git status` mostri solo `M ` sui 9 file.

### Elementi del diff esaminati

- `modules/gate/gate.py:470` — `libero_dopo_lettura`: lascia liberi rubrica e write_file di livello 1, tranne quando il primo pezzo del percorso (normalizzato e casefold) inizia con «reports» o «knowledge».
  - Rischio esaminato: aggirare il controllo sul nome.
  - Sonde negate correttamente: `Reports/`, `rEpOrTs/`, `reportſ/`, `ｒeports/`, `.reports/`, `..reports/`, `dati/../reports/a`, `./././reports/a`, `ＫＮＯＷＬＥＤＧＥ/x`, `KNOWLEDGE.bak/x`.
  - Risultano liberi `​reports/`, `re​ports/`, `\treports/`, `rеports/` (cirillico), `reportś/`. Non sono bypass: sul disco sono cartelle diverse da `reports/`, e il kernel ricontrolla comunque il file vero.
  - Esito: ok.
- `modules/gate/gate.py:487` — `primo = parts[0].strip(". ")` seguito da `startswith`.
  - Rischio esaminato: punti e spazi in testa o in coda.
  - Il prefisso nega per eccesso anche `reportsx/` e `knowledgebase/`: è fail-closed e accettabile.
  - Esito: ok.
- `gas.py:2487` — `_libero_dopo_lettura`: rifà il calcolo sul percorso risolto (GAS_CWD e symlink via `_file_rel_root`) e nega se ci sono chiavi riservate.
  - Rischio esaminato: un nome libero che punta a reports/.
  - Mutazione: con `if True: return True` (niente controllo sul file vero né sulle chiavi) falliscono 3 test: T74b3 ×2 e T82i. Il controllo è quindi coperto dai test.
  - Nessuna eccezione può risalire: la funzione del gate non solleva mai, `_ha_chiavi_riservate` non solleva mai, il resto sta in try con ritorno False.
  - Esito: ok.
- `gas.py:3836` — la condizione UNCERTAIN più finestra contaminata manda al cancello solo se l'azione non è libera.
  - Rischio esaminato: indebolire IRREVERSIBLE o il livello 2.
  - La promozione a IRREVERSIBLE di `_write_livello2` avviene prima, e l'esecuzione ricalcola livello 3 e livello 2 e controlla gli hard link (`gas.py:3572`).
  - Il tetto di 10 iterazioni e `_get_window` non sono toccati. Nessuno slicing della history e nessuna simulazione di tool.
  - Esito: ok.
- `gas.py:1498` (contesto) — la foto di sicurezza usa `git("add", "-A")` su un indice temporaneo, quindi rispetta `.gitignore`. Solo `.gas_history.json` viene aggiunto forzato. Esito: **blocco** (vedi R-367-1).
- `tests/test_unit_notte.py:229` e i test del kernel T72f, T72g, T74b, T84i spostati su reports/: continuano a provare il ramo del cancello. Esito: ok.

### Motivo bloccante

**R-367-1 (MEDIA)**: i file ignorati da git sono di livello 1, ma la foto di sicurezza non li copre. Sovrascriverli è quindi irreversibile, e dopo una lettura ora è libero senza firma.
- Sonda: `gas_debug.log`, `gas_debug.log.1` e `snapshots.log` risultano di livello 1 e liberi. In `.gitignore` ci sono anche `gas_debug.log`, `gas_debug.log.*`, `logs/`, `*.bak`, `snapshots/`, `test_sandbox/`.
- Scenario: un testo letto contiene un'iniezione che fa riscrivere `gas_debug.log`. È la scatola nera prevista dal §9 di CLAUDE.md, cioè una prova di sicurezza. Il contenuto è perso senza recupero; nel diario resta solo la traccia della chiamata.
- Questo contraddice la decisione del 19 ottobre («irreversibili alla firma»). Rende falsa anche la frase della roadmap «write_file sui file normali (livello 1, con foto di sicurezza)».
- Correzione proposta:
  - In `_libero_dopo_lettura`, restituire False se il file risolto è ignorato da git (`git check-ignore -q`, con False anche su qualunque errore). In alternativa, come minimo, aggiungere `gas_debug`, `logs`, `snapshots`, `test_sandbox` e il suffisso `.bak` all'elenco che resta alla firma.
  - Aggiungere un test round-trip: read_file, poi write_file su `gas_debug.log` → l'azione va alla firma.

### Riserve non bloccanti

- **R-367-2 (BASSA)**: con la rubrica libera dopo una lettura, un'iniezione diventa persistente. Il pin la reinserisce nel messaggio system a ogni turno e a ogni sessione, anche di notte. È attenuata da sanificazione, delimitatori `<memoria_dati>` e tetto `MEMORY_PIN_CHAR_CAP`. Inoltre `salva_contatto` può riscrivere l'indirizzo di un lead reale. Quando arriverà il funnel (FASE 4), la firma degli invii dovrà mostrare l'indirizzo di destinazione letto dal DB. Da tracciare in stato_progetto.md.

### Cose controllate e a posto

- Sonde su file che toccano la sicurezza: `.github/workflows/`, `.gitattributes` e `.envrc` sono livello 3. `.vscode/tasks.json`, `.pre-commit-config.yaml`, `package.json`, `Dockerfile`, `gas_identity.md`, `*.pth`, `sitecustomize.py` e `.python-version` sono livello 2. Nessuno è libero.
- Il catalogo notturno sta fuori dalla root, quindi non è scrivibile.

### Rischi non verificati

- Comportamento su macOS/APFS, che non distingue maiuscole e minuscole e tollera forme Unicode diverse: non riproducibile qui. Per costruzione il casefold e l'NFKC del gate negano per eccesso, e il ricontrollo sul file vero usa il percorso risolto.
- Non ho controllato la qualità della sanificazione del pin oltre ai delimitatori: è stata già revisionata in fette precedenti.
- Non ho provato il giro notturno reale con Telegram.

Memoria: /home/user/Gas/.claude/agents/memoria_revisore.md (riga #367, commit cece054)
```

### Review #368

```
## VERDETTO: APPROVATO CON RISERVE

Seconda review (#368) dopo la bocciatura #367. R-367-1 è chiusa. Ho riprodotto i numeri: suite del kernel 899 PASS e 0 FAIL, `pytest tests/` 1475 passed. Riga contatore committata (7545e0d), diff staged intatto. Per la #367 resta valido il rapporto già consegnato (BOCCIATO, commit cece054).

Le mutazioni le ho fatte su una copia nella cartella di appoggio. Ho verificato che `git diff gas.py` nel repo è vuoto.

### Elementi del diff esaminati

- `gas.py:2505`: `git -C root check-ignore -q --no-index -- <rel>` sul percorso già risolto (cartella di lavoro e symlink).
  - Rischio esaminato: che il controllo e la foto di sicurezza (`git add -A`, `gas.py:1498`) vedano in modo diverso cosa è ignorato. Usano le stesse regole di ignore, quindi sono coerenti.
  - `--no-index` tratta come ignorati anche i file tracciati che corrispondono a un pattern: va alla firma, cioè blocca per eccesso, e va bene.
  - Una root senza git dà 128, quindi firma: anche lo snapshot fallirebbe comunque.
  - Esito: ok.
- `gas.py:2511`: `return ign.returncode == 1`. Esito 0, 128, timeout di 10 s o eccezione portano tutti alla firma: è fail-closed.
  - Mutazione: con `return True` fallisce 1 test (T74b2 R-367-1: `gas_debug.log` sovrascritto, `logs/a.txt` e `dati/c.bak` creati).
  - Esito: ok.
- `tests/test_unit_kernel.py`: T74b2 R-367-1 è un vero test di andata e ritorno: read_file, poi 4 write_file, poi la risposta finale.
  - Verifica che la scatola nera resti intatta e che la controprova `dati/libero2.md` venga scritta.
  - Esito: ok.
- `gas.py:3844`: ramo del cancello invariato rispetto alla #367.
  - IRREVERSIBLE, livello 2 e livello 3 restano ricalcolati all'esecuzione.
  - `_get_window` e il tetto di 10 iterazioni non sono toccati. Nessuno slicing della storia e nessuna simulazione di strumenti.
  - Esito: ok.
- `modules/gate/gate.py:470`: `libero_dopo_lettura` invariato rispetto alla #367 (sonde su maiuscole, Unicode e punti già fatte). Esito: ok.

### Riserve (da tracciare in stato_progetto.md)

- **R-368-1 (COSMETICA)**: senza `GIT_LITERAL_PATHSPECS=1`, un percorso che inizia con «:» viene letto da git come pathspec magico. `--` non lo impedisce.
  - Prova in una cartella di appoggio: `:x.md` viene controllato come `x.md` ed esce 1 anche se un pattern `:*` lo ignorerebbe. Le forme `:(literal)`, `:!` e `:(glob)` danno 128, quindi firma.
  - Un bypass richiede un pattern di .gitignore che colpisca «:nome» ma non «nome». Oggi non ce n'è nessuno, e .gitignore è livello 3, quindi Gas non può scriverlo.
  - Rimedio: `env={**os.environ, "GIT_LITERAL_PATHSPECS": "1"}` nella chiamata.
- **R-367-2 (BASSA)**: già tracciata in stato_progetto.md. La rubrica libera dopo una lettura permette un'iniezione persistente tramite il pin; in futuro serve anche l'indirizzo di invio mostrato nella firma.

### Rischi non verificati

- Comportamento su macOS/APFS con `core.ignorecase=true`: non riproducibile qui. Il controllo e `git add -A` leggono la stessa configurazione, quindi restano coerenti tra loro.
- Le esclusioni globali dell'operatore (`core.excludesFile` sul Mac) non le vedo. Valgono sia per il controllo sia per lo snapshot, quindi non creano incoerenze.
- Costo di una chiamata a git per ogni write_file libera dopo una lettura: non misurato. Il timeout è 10 s.

Memoria: /home/user/Gas/.claude/agents/memoria_revisore.md (riga #368, commit 7545e0d). Dopo il verdetto il marcatore va rigenerato con `bash scripts/segna_review_ok.sh`.
```

### Review #369

```
## VERDETTO: APPROVATO

Review #369, terza di questa fetta. R-368-1 è chiusa. Il rimedio che avevo proposto nella #368 (`GIT_LITERAL_PATHSPECS=1`) era sbagliato: `check-ignore` lo rifiuta con 128, quindi ogni scrittura finiva alla firma. Il «./» davanti al percorso che hai usato è la soluzione giusta.

Ho riprodotto la suite del kernel: 900 PASS, 0 FAIL. I 1475 di `pytest tests/` sono quelli che ho riprodotto nella #368: da allora non li ho rilanciati. Dopo la #368 il diff tocca solo `gas.py` e `tests/test_unit_kernel.py`, che pytest non esegue (la suite del kernel gira con `python3`).

### Elementi del diff esaminati

- `gas.py:2511`: `"./" + risolto[1]` passato a `git -C root check-ignore -q --no-index --`.
  - Rischio esaminato: un nome che inizia con «:» letto da git come pathspec magico.
  - Sonde in una cartella di appoggio, con `.gitignore` = `gas_debug.log`, `logs/`, `*.bak`, `:*`:
    - Danno 0 (ignorati, quindi alla firma): `./:x.md`, `./:(literal)c.bak`, `./:!c.bak`, `./:/a.md`, `./dati/:y`, `./gas_debug.log`, `./logs/a`.
    - Danno 1 (liberi): `./dati/libero.md`, `./-x.md`.
  - `risolto[1]` è sempre relativo alla root (`_file_rel_root`), quindi «./» con `-C root` punta allo stesso file.
  - Esito: ok.
- `gas.py:2513`: `return ign.returncode == 1`. Invariato e fail-closed: 0, 128, timeout ed eccezioni portano tutti alla firma. Esito: ok.
- `tests/test_unit_kernel.py:5724`: check T74b2 R-368-1. Con `.gitignore` uguale a `:*`, `_libero_dopo_lettura` su `:x.md` deve dare False.
  - Il controllo sul nome da solo darebbe True, quindi il False viene davvero da `check-ignore`.
  - Mutazione su una copia (senza «./») → 1 FAIL, proprio questo check.
  - Il test ripristina `.gitignore` subito dopo. `_libero_dopo_lettura` non solleva mai eccezioni, quindi il ripristino avviene sempre.
  - Esito: ok.

### Cosa NON ho verificato

- macOS/APFS con `core.ignorecase` e le esclusioni globali dell'operatore: non riproducibili qui. Valgono allo stesso modo per il controllo e per la foto di sicurezza (`git add -A`).
- Costo in tempo di una chiamata a git per ogni write_file libera dopo una lettura: non misurato. Il timeout è 10 s.

Resta aperta R-367-2 (BASSA), già tracciata in stato_progetto.md: un testo letto può scrivere in rubrica e da lì rientrare a ogni turno nel blocco di memoria che il kernel aggiunge al prompt di sistema.

Memoria: `/home/user/Gas/.claude/agents/memoria_revisore.md`, riga #369 (commit bfc245f). Il diff staged è intatto. Ora va rigenerato il marcatore con `bash scripts/segna_review_ok.sh`.
```

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 893 → 900 PASS, 0 FAIL (T74b2, T74b3; T72f/T72g/T74b/T84i spostati su `reports/`). Blocco reale: `=== RIEPILOGO: 900 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1475 passed in 185.31s (0:03:05)` (+5 notte, +20 gate).

## §6 STATO CI

- Commit della sessione pushati prima dell'apertura della PR: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-366-1 (BASSA, dichiarata in setup_notte.md): una richiesta notturna occupa fino a 24 h uno dei 5 posti in attesa.
- R-367-2 (BASSA): iniezione persistente via rubrica (pin sanitizzato e delimitato); con gli invii (FASE 4) la firma dovrà mostrare l'indirizzo letto dal DB.
- Già tracciate: R-bot217-1, R-bot217-2, R-ve217-1.
