# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Turno di notte: segno nel DB per l'esito delle firme (voce 6 di `reports/coda_notte.md`), fetta di sicurezza

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #281 (https://github.com/Gasss23/Gas/pull/281). Numero e URL dalla risposta JSON di `gh api -X POST repos/Gasss23/Gas/pulls` (GraphQL non disponibile). Il turno di notte non mergia mai. Fetta di sicurezza (firma umana): secondo passaggio nella chat claude.ai col link della PR prima del merge.
2. Testo dell'attività programmata «Turno di notte Gas»: invariato; se l'operatore lo vuole cambiare, deve chiederlo in questa sessione.

---

## §1 SCOPE & ESITO FETTE

- **Voce 0**: `SALTATA — già fatta dalla chat Motore (PR #279, review #528), spostata in «Fatte»`.
- **Fetta 1 — Voce 6, segno nel DB per l'esito delle firme**: `FATTA` — `modules/memory/store.py`, `gas.py`, test T78q–T78u; review #531 BOCCIATO → #532 APPROVATO CON RISERVE.
- **Voci 7a, 7, 8**: `SALTATA — al massimo una voce del motore a notte`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |  30 ++++++++++++++++++++++++---
 modules/memory/store.py            |  60 +++++++++++++++++++++++++++++++
 reports/coda_notte.md              |   4 ++--
 reports/diff_sessione.md           |  14 ++++++++------
 reports/handoff.md                 | n/d (commit finale)
 reports/report_notte.md            |  28 +++++++++++++++++-----------
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  18 +++++++-----------
 tests/test_unit_kernel.py          | 123 ++++++++++++++++++++++++++++++
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d». Gli altri conteggi vengono da `git diff --cached --stat` preso prima del commit finale, con le barre accorciate; il diff reale della PR fa fede.

## §3 GIT LOG --ONELINE (sessione)

```
fbbfb86 fix(firma): segno nel DB per l'esito già in storia, esito nel DB prima della storia (coda notte voce 6)
b9a9ae4 chore(revisore): memoria review #532 — APPROVATO CON RISERVE
a0d6393 chore(revisore): memoria review #531 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #531 (chat Notte) — sul primo diff staged, BOCCIATO e poi corretto

## VERDETTO: BOCCIATO

Review #531 (chat Notte), diff staged in /home/user/Gas sul ramo notte/2026-10-28 (voce 6 della coda notte, firma umana C4b). Ho letto CLAUDE.md (sez. 5, 8, 9), stato_progetto (le parti sulla firma) e la memoria.

**Elementi del diff esaminati**
- `modules/memory/store.py:289`: tabella nuova `approval_esiti_in_storia`, con chiave esterna verso approvals e trigger che vietano UPDATE e DELETE. Rischi esaminati: DB vecchi senza la tabella, e il caso di approvazione inesistente. Esito **ok**. `_init_schema` esegue `_SCHEMA` a ogni apertura, quindi la tabella viene creata anche sui DB vecchi. `_connect` attiva le chiavi esterne (`PRAGMA foreign_keys = ON`) e INSERT OR IGNORE non ignora le violazioni di chiave esterna, quindi un ID inesistente dà False (T78t). Le approvazioni non vengono mai cancellate, quindi la chiave esterna non blocca nulla.
- `modules/memory/store.py:1987` / `modules/memory/store.py:2004`: `segna_esito_in_storia` e `esito_in_storia`. Rischio esaminato: eccezioni o memoria degradata. Esito **ok**: tornano False o None, l'errore va nel log, e con None il kernel ripiega sulla cronologia.
- `gas.py:3505`: l'esito viene scritto nel DB prima della storia (R-445-3). Rischi esaminati: effetto su `res` e sul diario, crash fra i due passi. Esito **ok**. `res` e il diario vengono impostati dopo, come prima. Se Gas cade fra DB e storia, l'esito vero resta nel DB e `recupera_esito_firma` lo scrive come «eseguita» (T78r; con il vecchio ordine T78r fallisce).
- `gas.py:3388`: il segno si mette solo se `_save_history()` ritorna True. La logica è corretta, ma **riserva**: il mutante «segna sempre, a prescindere dal salvataggio» passa l'intera suite (1051 PASS, 0 FAIL).
- `gas.py:3540`: **BLOCCO**, vedi R-531-1.
- `tests/test_unit_kernel.py:8239` (T78q), `tests/test_unit_kernel.py:8301` (T78s) e `tests/test_unit_kernel.py:8323` (T78t) coprono: comportamento dopo `clear`, firme vecchie, migrazione, divieti di modifica, fail-safe. Esito **ok**.

**Motivo bloccante**
- **R-531-1 (ALTA, regressione rispetto a main).** A `gas.py:3540` `recupera_esito_firma` mette il segno quando trova l'esito nella cronologia **in memoria**. Questo vale anche se il salvataggio di quella storia era fallito. Contraddice la regola scritta nel commento a `gas.py:3386` («il segno solo con la storia su disco»). Sonda riprodotta (`/tmp/claude-0/-home-user-Gas/1e2c21b2-c183-5a9e-8222-ab7058554773/scratchpad/r531/sonda.py`): la scrittura della storia fallisce, poi un nuovo click su Approva porta a `recupera` → None e segno True. Poi Gas va in crash e riparte, e un nuovo click dà ancora None: l'esito non è su disco e **non viene mai più scritto**. Su main, dopo il riavvio, l'esito veniva riscritto. Conseguenze: il modello non saprà mai che l'azione è stata eseguita, e il bridge risponde «Nessuna modifica», quindi l'esito resta nascosto. È proprio il rischio che hai chiesto di guardare.
  - Correzione: a `gas.py:3540` metti il segno solo se `self._save_history()` ritorna True, oppure non metterlo affatto in quel ramo (le firme vecchie restano coperte dalla scansione). Aggiungi un test che riproduca la sonda: salvataggio fallito → click → riavvio → click → esito scritto.

**Riserve non bloccanti**
- **R-531-2 (BASSA).** La condizione a `gas.py:3388` non ha un test: serve un caso con `_salva_storia_su_file` che fallisce e la verifica `esito_in_storia(...) is False`. Lo stesso test può chiudere anche R-531-1.
- **R-531-3 (BASSA).** Più processi: se il REPL finisce nel ramo «copia conflitto» di `_unisci_storia_altrui` (`gas.py:1201`) e sovrascrive il file principale, l'esito scritto dal bot resta solo nella copia. Il DB però ha il segno, quindi dopo un riavvio del bot non c'è recupero; su main il recupero avveniva. È un caso stretto (conflitto, poi riavvio, poi nuovo click). Basta dichiararlo in stato_progetto.
- Sulla tua domanda («al posto della scansione»): tenere la cronologia come ripiego è la scelta giusta (DB degradato, firme vecchie). Il difetto non è il ripiego, ma che il ripiego **scrive** il segno senza prova che l'esito sia su disco.

**Rischio escluso:** non ho provato due processi reali (bot e REPL) in parallelo sullo stesso file: R-531-3 viene da lettura del codice, non da una prova. Non ho provato nemmeno un DB ripristinato da un backup più vecchio della storia (segno assente → si ricade sulla cronologia, lettura del codice).

**Misure:** suite del kernel sul ramo 1051 PASS, 0 FAIL, rifatta. `gas.py` è stato ripristinato dopo il mutante (nessuna differenza fra file di lavoro e versione staged).

Memoria: riga #531 e una lezione nuova («un segno persistente "X è su disco" si mette solo dopo una scrittura riuscita osservata nello stesso percorso») committate con lo script, commit a0d6393. L'indice staged del motore non è stato toccato.

File rilevanti: /home/user/Gas/gas.py, /home/user/Gas/modules/memory/store.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #532 (chat Notte) — sul diff committato in fbbfb86

## VERDETTO: APPROVATO CON RISERVE

Review #532 (chat Notte), secondo giro della voce 6 della coda notte: il segno nel DB che dice «l'esito della firma è già scritto nella storia». Ho esaminato il diff staged (3 file: gas.py, modules/memory/store.py, tests/test_unit_kernel.py). Prima della review ho letto CLAUDE.md (sez. 5), stato_progetto e la mia memoria.

**Elementi del diff esaminati**
- `gas.py:3543` — nel ramo «esito già in storia» di `recupera_esito_firma` il segno si mette solo se manca nel DB e `_save_history()` ritorna True adesso. Rischio esaminato: l'esito c'è solo nella cronologia in memoria ma il salvataggio fallisce. Se il DB non si legge (None) si tenta il salvataggio e poi il segno, che fallisce senza conseguenze. Mutante senza la condizione sul salvataggio → T78u FAIL. Esito: ok, **R-531-1 CHIUSA**.
- `gas.py:3388` — in `_storia_esito_firma` il segno si mette solo se `_save_history()` riesce. Mutante «segna sempre» (sopravvissuto al #531) → ora T78u FAIL (2 FAIL). Esito: ok, **R-531-2 CHIUSA**.
- `tests/test_unit_kernel.py:8306` — T78u riproduce la mia sonda: salvataggio forzato a False → `applica_firma` esegue senza segno → click senza segno → riavvio → nuovo click riscrive l'esito «eseguita» senza eseguire e mette il segno. Altri mutanti, tutti presi: recupero che non mette mai il segno → T78s FAIL; vecchio ordine (storia prima del DB) → T78r FAIL. Esito: ok.
- `modules/memory/store.py:1987` — `segna_esito_in_storia`: tabella in cui si può solo inserire, UPDATE e DELETE bloccati da trigger. Sugli errori ritorna False e logga, mai eccezioni. Già esaminata nel #531. Esito: ok.
- `gas.py:1352` (contesto, file nel diff ma funzione non toccata) — `_save_history` ritorna False anche quando l'unione con la storia di un altro processo è rimandata. Quindi niente segno: è il verso sicuro.

**Misure rifatte da me:** test del kernel 1053 PASS, 0 FAIL. Dopo i mutanti il working tree è tornato pulito.

**Riserve**
- **R-532-1 BASSA:** con il salvataggio rimandato o fallito, il segno non viene più messo quando la storia arriva davvero su disco a fine turno. Lo mette solo un click successivo. Il verso è sicuro: al massimo, dopo un `clear`, un click scrive di nuovo la notizia; mai una nuova esecuzione. Va tracciata o accettata.
- **R-532-2 BASSA:** R-531-3 (copia «conflitto» fra più processi più il segno) non è ancora scritta in reports/stato_progetto.md, perché il file non è nel diff staged. Va scritta lì prima del commit insieme a R-532-1, come previsto dal gate.

**Non verificato:** il comportamento con due processi Gas veri in concorrenza (bot e giro notturno sullo stesso DB e sulla stessa storia) e con Telegram reale. Non si riproduce nel container senza token; resta coperto solo dalla dichiarazione di R-531-3. Non ho rifatto `pytest -q tests/` per intero: ho rifatto solo la suite del kernel, l'unica toccata dal diff di test.

Memoria aggiornata con la riga #532 e committata da sola con lo script (b9a9ae4). File: /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: main `=== RIEPILOGO: 1043 PASS, 0 FAIL ===` → ramo `=== RIEPILOGO: 1053 PASS, 0 FAIL ===` (T78q–T78u). Con lo store nuovo e il `gas.py` di main: `1046 PASS, 5 FAIL` (T78q×2, T78r×2, T78s).
- `python -m pytest -q tests/`: `2265 passed, 51 skipped` sia su main sia sul ramo (skip preesistenti dell'ambiente). Nessun FAIL.

## §6 STATO CI

```
completed	skipped	Turno di notte 2026-10-28: segno nel DB per l'esito delle firme (coda voce 6)	verifica-bot	notte/2026-10-28	pull_request_target	40606743507	8s	2026-10-28T00:07:44Z
in_progress		fix(firma): segno nel DB per l'esito già in storia, esito nel DB prim…	CI	notte/2026-10-28	push	40606738717	33s	2026-10-28T00:07:42Z
```

Mappatura commit→run:
- `a0d6393`, `b9a9ae4`: nessuna run su questo SHA (pushati insieme a `fbbfb86`).
- `fbbfb86` → run CI 40606738717 (push), in corso alla scrittura dell'handoff.
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-531-3 (chat Notte)** BASSA: più processi, esito rimasto nella copia «conflitto» con il segno nel DB → nessun recupero dopo un riavvio (da codice, non provato).
- **R-532-1 (chat Notte)** BASSA: con il salvataggio rimandato il segno si mette solo al click successivo (verso sicuro).
- Non provati due processi Gas veri né Telegram reale.
