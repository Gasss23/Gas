# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 pomeriggio — Decisioni dell'operatore: avviso Flash-lite, tetto per turno, nomi dei lead mai ai modelli non forti (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #370 (https://github.com/Gasss23/Gas/pull/370). Numero e URL dall'output di `create_pull_request` dello strumento GitHub (gh assente).
2. R-753-M1-A: DECISA dall'operatore il 2026-11-10 notte («blocco esteso dei nomi sì»): si implementa in una PR successiva. Testo originale della domanda: estendere il blocco dei nomi dei clienti anche ai risultati di `ricorda`/`salva_contatto` nella storia, al testo dell'operatore, a `recap_pin` e alla riflessione di fine task (ve #370 V-1) verso i modelli non forti? sì/no

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — (a) primo cervello non configurato = ripiego dichiarato**: FATTA — solo test T113a4 (nessun cambio di codice, sì dell'operatore).
- **Fetta 2 — (b) Flash-lite dichiarato**: FATTA — `RUNG_VERSIONE_LEGGERA`, riga nel testo (mai a voce).
- **Fetta 3 — tetto di 10 chiamate per turno**: FATTA — `MAX_CHIAMATE_TURNO`.
- **Fetta 5 — merge di origin/main (#368 di Mani)**: FATTA — review #757-M1 APPROVATO.
- **Fetta 4 — nomi dei lead mai ai modelli non forti**: FATTA per il pin; DEFERITA per storia/recap (R-753-M1-A, §0 punto 2).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 gas.py                             | 164 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------
 modules/telegram/bot.py            |   2 +-
 reports/diff_sessione.md           |  15 +++++++--------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  21 ++++++++++-----------
 tests/test_unit_kernel.py          | 247 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 tests/test_unit_notte.py           |   4 +++-
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
05184a94 merge: origin/main (#368) nella #370 (review #757-M1 APPROVATO)
e9b74f59 docs(fine-task): handoff #370 aggiornato (R-753-M1-A estesa, CI)
fabf2e9a docs(stato): R-753-M1-A estesa alla riflessione (ve #370 V-1) e buchi noti del pin anonimo
e761eefc docs(fine-task): decisioni dell'operatore del 2026-11-10 (Flash-lite, tetto per turno, pin anonimo)
d5773ec1 fix(kernel): decisioni dell'operatore 2026-11-10 — Flash-lite dichiarato, tetto di 10 chiamate per turno, pin senza dati dei lead ai non forti (review #753-M1)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

# Review #753-M1 — 1° giro

## VERDETTO: APPROVATO CON RISERVE

Revisione #753-M1 del diff in stage sul branch `feat/merge-automatico-z1xjx2` (PR #366). Prima ho letto CLAUDE.md (§5, §8, §2), `reports/stato_progetto.md` (righe 378-379) e la mia memoria. Non ho committato nulla.

**Le prove dell'autore, rifatte da me**
- `tests/test_unit_kernel.py`: **1131 PASS, 0 FAIL**, confermato.
- Telegram e notte con pytest: 273 passed.
- Ho provato 4 mutanti miei, cioè versioni del codice rotte apposta per vedere se i test se ne accorgono:
  - tolto il controllo su `contatto_id` nel pin: i test lo scoprono (T114f fallisce);
  - tolta la ricerca dei nomi dei lead nel testo del diario: i test lo scoprono (T114f fallisce);
  - il secondo tentativo dopo un errore 400 di Gemini non conta come chiamata: **i test non se ne accorgono**;
  - il secondo tentativo ignora il tetto di 10: **i test non se ne accorgono**.

**Righe del diff esaminate**
- `gas.py:5199` — controllo del tetto all'inizio di ogni cervello. Se le 10 chiamate sono già finite, scrive il motivo e chiude il giro. Rischio esaminato: passare al cervello dopo anche a tetto finito. Ho seguito anche il caso in cui la decima chiamata fallisce: si torna qui, il giro si chiude e arriva «Pipeline esausta» col motivo. — ok
- `gas.py:5261` — controllo del tetto dentro il giro di un cervello, dopo il controllo del budget e prima della chiamata. Rischio esaminato: un tetto che scatta dopo l'altro e ne consuma il posto (lezione del 2026-11-09). Il contatore sale solo quando la chiamata parte davvero (`gas.py:5269`). Alla fine si arriva a «Pipeline esausta» (`gas.py:5499`). Non c'è nessun taglio diretto della storia. — ok
- `gas.py:5284` — il secondo tentativo dopo un 400 di Gemini conta nel tetto: rinuncia se il tetto è pieno e altrimenti aumenta il contatore (`gas.py:5296`). Rischio esaminato: si potrebbe superare il tetto di 1. La logica è giusta, ma nessun test la copre. — riserva (R-753-M1-1)
- `gas.py:480-502` — `_info_ripiego` con `versione_leggera`. Il caso «risposta da una riserva» vince su «versione leggera». Il cervello forte (claude-cli) è escluso. Per i compiti semplici `_cascata_provider` (`gas.py:1040`) mette Flash-lite al primo posto, quindi non è un ripiego ma viene dichiarato. Rischio esaminato: l'avviso detto a voce. Sia la CLI (`gas.py:6725`) sia Telegram (`modules/telegram/bot.py:951`) lo scrivono solo come riga di testo. Il test notte che si aspettava solo «42» è stato aggiornato (`tests/test_unit_notte.py:2229`). — ok
- `gas.py:5230` — `_pin_rung`: il pin con i dati dei lead va solo a `claude-cli`, quello anonimo a tutti gli altri. Le due versioni si calcolano una volta per turno (`gas.py:5149`), dentro il messaggio di sistema. `_get_window` e la finestra non sono toccati. — ok
- `gas.py:3955-4007` — versione anonima del pin. Al posto dei lead mostra solo quanti sono. Le righe del diario legate a un lead perdono i dettagli: quelle degli strumenti dei contatti, quelle con `contatto_id` e quelle che contengono un nome o un dato di un contatto. Si confronta col testo originale, prima della sostituzione per i turni contaminati, e col `tipo` originale. Gli identificativi si prendono da tutti i contatti, anche chiusi. Rischio esaminato: un nome che passa lo stesso. Un nome di 1–2 lettere non viene cercato (limite dichiarato in stato_progetto). Le parole comuni, tipo «info», nascondono troppo, ma è un errore nel verso sicuro. In caso di errore restituisce `"", ""`, come prima. — ok
- `gas.py:4222` — contesto, file non toccato: `rifletti` chiama ancora `_memoria_pin()`, che ora restituisce la versione piena. Solo il segnale `_pin_non_fidato` cambia, ed è identico per le due versioni. — ok

**Riserve**
- **R-753-M1-1 (BASSA)**: «anche il secondo tentativo dopo un 400 di Gemini conta» è una decisione esplicita dell'operatore, ma nessun test la prova. Gli ultimi due mutanti dell'elenco sopra passano tutti i 1131 test. Serve un test con Gemini che risponde 400 alla decima chiamata: il secondo tentativo non deve partire e il tetto deve essere dichiarato.
- **R-753-M1-2 (BASSA)**: `recap_pin` (`gas.py:5152`, il riassunto delle sessioni precedenti) va ancora a tutti i cervelli gratuiti. Può contenere nomi di lead se la riflessione ne parlava. È lo stesso problema della riserva aperta R-753-M1-A: va annotato lì insieme.
- **R-753-M1-3 (COSMETICA)**: dopo che il tetto è scattato, i cervelli seguenti non configurati aggiungono ancora «… non impostata» ai motivi, perché il `continue` di `gas.py:5196` arriva prima del `break`. Il messaggio di «Pipeline esausta» diventa più rumoroso.

**Cosa NON ho verificato**
- Il comportamento con Gemini, Groq o OpenRouter veri e con `claude -p` reale: i test usano client finti e qui non ci sono chiavi.
- Il server voce e il sottofondo: non sono nel diff. Ho controllato solo che la CLI e Telegram non leggano l'avviso a voce.
- Le suite `gate`, `manutenzione` e `voice_server`: non le ho rilanciate.

La riga #753-M1 e una lezione nuova sono in `.claude/agents/memoria_revisore.md`, messe in stage. Non ho lanciato `commit_memoria_revisore.sh`, perché mi avevi chiesto di non committare.

# Review #753-M1 — 2° giro

## VERDETTO: APPROVATO

Revisione #753-M1, 2° giro, sul diff in stage del branch feat/merge-automatico-z1xjx2 (PR #366). Prima della revisione ho riletto CLAUDE.md (sez. 5 e 8), la riga del 1° giro in memoria e la voce R-753-M1 in `reports/stato_progetto.md`.

**Parti del diff esaminate**

1. `gas.py:5196` — nel giro esterno i due controlli del tetto (`_tetto_turno` e `_chiamate_turno >= MAX_CHIAMATE_TURNO`) ora vengono prima del controllo della chiave (`gas.py:5202`).
   - Rischio esaminato: un rung saltato in modo sbagliato, o «non impostata» ancora aggiunta dopo il tetto.
   - Esito: **ok**. Se il primo cervello finisce le sue 10 iterazioni esattamente a 10 chiamate, il controllo esterno sul rung seguente aggiunge «tetto … e successivi non provati» e si ferma. L'ordine vecchio (rimesso da me) produceva «groq: GROQ_API_KEY non impostata; openrouter…; ollama…» e non arrivava mai al tetto, quindi T114c4 falliva.
2. `gas.py:5285` — il retry del 400 di Gemini parte solo se `_chiamate_turno < MAX`, e la nuova chiamata conta (`gas.py:5298`).
   - Rischio esaminato: un'undicesima chiamata.
   - Esito: **ok**. Se il 400 arriva alla decima chiamata, l'errore passa al gestore esterno e il rung seguente dichiara il tetto. Se arriva alla nona, il retry è la decima e il controllo interno (`gas.py:5263`) ferma il turno. Il controllo del budget prima del retry resta.
3. `tests/test_unit_kernel.py:12801` — T114c2, T114c3 e T114c4.
   - Rischio esaminato: test che passano anche col codice sbagliato.
   - Esito: **ok**. Ho rieseguito io i tre mutanti dichiarati e ognuno fa fallire il test previsto:
     - retry che ignora il tetto → T114c2 FAIL (11 chiamate);
     - retry non contato → T114c3 FAIL (11 chiamate);
     - ordine vecchio dei controlli → T114c4 FAIL.
   - `gas.py` è tornato identico a quello in stage dopo ogni mutante.
4. `reports/stato_progetto.md:378` — R-753-M1-1 e R-753-M1-3 chiuse con i test che le provano; R-753-M1-2 (recap_pin ai cervelli gratuiti) annotata dentro la riserva aperta R-753-M1-A.
   - Esito: **ok**. Coerente con quanto chiesto nel 1° giro.

**Esecuzione**
- `tests/test_unit_kernel.py`: 1134 PASS, 0 FAIL.
- `git diff --cached --check`: pulito.
- Nessun taglio diretto della cronologia e nessuna simulazione dell'output dei tool. La finestra passa sempre da `_get_window` (`gas.py:5228`). La barriera `for _ in range(10)` per cervello resta (§8).

**Cosa non ho verificato**
- La suite pytest di telegram, voce, notte, sottofondo, gate, manutenzione e voice_server (1448 passed secondo l'autore) non l'ho rilanciata. Il delta di questo giro tocca solo `gas.py` nel ciclo della cascata e i test del kernel; quei moduli non sono cambiati rispetto al 1° giro.
- Il comportamento reale del 400 di Gemini in produzione non è verificato: in sviluppo non si riproduce, i test usano un client finto.

**Memoria**: la riga «#753-M1 (2° giro)» è aggiunta in coda a `.claude/agents/memoria_revisore.md` e in stage. Come da tua istruzione non ho committato, quindi non ho lanciato `commit_memoria_revisore.sh`.

### Review #757-M1 (merge di origin/main #368)

## VERDETTO: APPROVATO

Review #757-M1. Il numero che mi avevi indicato, #754-M1, è già usato: nella memoria fusa le righe #754, #755 e #756-M1 vengono dalla chat di Mani, che usa anche lei la sigla M1. Anche #753-M1 compare due volte, una per lato.

Ho verificato il merge staged di origin/main 904d9d6 (PR #368) in feat/merge-automatico-z1xjx2 (HEAD e9b74f5, PR #370).

Elementi del diff esaminati:
- `clients/voice/ascolto.py:724` — `_voce_subito`, la richiesta detta d'un fiato, e il suo uso a :793 con `registra(subito, subito=True)`. Rischio: perdere o alterare righe di Mani nel merge. Il file staged è identico a MERGE_HEAD (diff di 0 righe). Dal merge-base a0c200c il nostro lato non tocca ascolto.py, quindi i due lati sono disgiunti. Esito: ok.
- `tests/test_unit_voce_ascolto.py:2719` — l'ultimo test aggiunto da #368 (voce verso la fine della tolleranza). Rischio: test persi o un file a metà tra i due lati. Il file è identico a MERGE_HEAD. Ho rieseguito la suite: 314 passed. Esito: ok.
- `scripts/voce/LEGGIMI.md:1` — le 8 righe aggiunte da Mani. Il file è identico a MERGE_HEAD. Esito: ok.
- `reports/stato_progetto.md:697` — la voce «Mani — richiesta d'un fiato (PR #368)». Rischio: perdere la nostra voce delle decisioni dell'operatore (#366) o quella di Mani. Ci sono entrambe e la riga #361 modificata da Mani è presa dal suo lato. Esito: ok.
- `.claude/agents/memoria_revisore.md:1484` — unione delle due code di memoria. Rischio: righe perse. Il diff contro MERGE_HEAD aggiunge solo le 3 righe nostre (#753-M1 + lezione + 2° giro), quello contro HEAD solo le 5 di Mani. Non si perde nulla. Esito: ok, con la sola nota sulla numerazione doppia, che è di processo e non tocca il codice.

Controlli meccanici:
- `git ls-files -u` è vuoto.
- `git diff --cached --check` è pulito.
- Nessun marcatore di conflitto in reports, .claude, clients, tests e scripts.
- MERGE_HEAD è 904d9d6.
- Il merge non tocca `_get_window`, il tetto di 10 iterazioni né i provider.

Cosa non ho verificato:
- Il test kernel (1134 PASS) e il pytest su voce, telegram_voce e notte (583 passed) non li ho rieseguiti: mi fido del tuo numero. Il nostro lato di codice (gas.py, bot.py) è fuori da questo merge e ha già avuto la sua review (#753-M1, 2° giro).
- Il comportamento dal vivo della voce sul Mac non è riproducibile qui.
- handoff.md, ultimo_report.md e diff_sessione.md presi dal nostro lato non li ho controllati riga per riga, perché li riscrive /fine-task.

Memoria: ho aggiunto la riga #757-M1 in fondo a `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho messa in stage, senza committare come richiesto. Contiene una lezione nuova: dopo un merge della memoria, il numero della review si prende dalla coda del file fuso, non da quella del proprio lato.

### Review #757-M1 — verdetto RIEMESSO dal revisore per il gate check_verdetto (stesso esito; l'originale sopra non citava file del diff di sessione)

## VERDETTO: APPROVATO

Review #757-M1, riemessa per il gate. Ho verificato il merge staged di origin/main 904d9d6 (PR #368 di Mani) in feat/merge-automatico-z1xjx2 (HEAD e9b74f5, PR #370). Il numero #754-M1 che mi era stato indicato è già occupato: le righe #754, #755 e #756-M1 vengono dalla chat di Mani, che usa anche lei la sigla M1.

Elementi esaminati:
- `gas.py:5198` — controllo del tetto MAX_CHIAMATE_TURNO nel giro esterno di run_turn (costante a `gas.py:2023`, barriera §8 da 10 per cervello a `gas.py:5224`). Rischio: che il merge abbia alterato il nostro lato. Il diff staged contro HEAD su gas.py è di 0 righe: il file non è toccato dal merge e il guardrail §8 è intatto. Esito: ok.
- `modules/telegram/bot.py:951` — commento §8 sulla riga di riserva o versione leggera, mai detta a voce, dentro `_turno_con_finale` (`modules/telegram/bot.py:952` passa `avviso_ripiego` nel testo). Rischio: perdita della modifica nostra (bot #366 V-1) nella risoluzione. Il diff staged contro HEAD è di 0 righe e il diff contro 904d9d6 contiene solo la modifica nostra. Esito: ok.
- `tests/test_unit_kernel.py` e `tests/test_unit_notte.py` — diff staged contro HEAD di 0 righe, quindi invariati dal merge. Esito: ok.
- Contesto, file arrivati da main e ora identici a main: `clients/voice/ascolto.py:724` (`_voce_subito`, usato a `clients/voice/ascolto.py:793` con subito=True), `tests/test_unit_voce_ascolto.py:2719` e `scripts/voce/LEGGIMI.md`. Sono identici a MERGE_HEAD (diff di 0 righe). Dal merge-base a0c200c i due lati di codice sono disgiunti. Ho rieseguito `tests/test_unit_voce_ascolto.py`: 314 passed. Esito: ok.
- `reports/stato_progetto.md:697` — c'è la voce «richiesta d'un fiato (PR #368)» di Mani e c'è anche la nostra voce delle decisioni dell'operatore (#366). Esito: ok.
- `.claude/agents/memoria_revisore.md:1484` — unione delle due code di memoria. Il diff contro MERGE_HEAD aggiunge solo le 3 righe nostre, quello contro HEAD solo le 5 di Mani: non si perde nulla. Esito: ok. Resta una nota di processo: la numerazione #753-M1 è doppia tra i due lati.

Controlli meccanici:
- `git ls-files -u` è vuoto.
- `git diff --cached --check` è pulito.
- Nessun marcatore di conflitto.
- MERGE_HEAD è 904d9d6.
- Nessun tocco a `_get_window`, ai provider o ai guardrail.

Cosa non ho verificato:
- Il test kernel (1134 PASS) e il pytest su voce, telegram_voce e notte (583 passed) non li ho rieseguiti: mi fido del numero dell'agente. Il codice del nostro lato ha già avuto la review #753-M1 (2° giro).
- Il comportamento dal vivo della voce sul Mac non è riproducibile qui.
- handoff.md, ultimo_report.md e diff_sessione.md presi dal nostro lato non li ho controllati riga per riga, perché li riscrive /fine-task.

Memoria: la riga #757-M1 è già in fondo a `/home/user/Gas/.claude/agents/memoria_revisore.md` ed è in stage, non committata. Non ho aggiunto una riga nuova: questa è la stessa review riemessa, non una review nuova.

## §5 DELTA TEST DEL MOTORE

- Kernel (`PYTHONUTF8=1 python tests/test_unit_kernel.py`): 1119 PASS / 0 FAIL (main a0c200c, container) → 1134 PASS / 0 FAIL (rilanciato da M1 dopo il commit d5773ec1 e di nuovo dopo il merge di #368). Dopo il merge: `python -m pytest -q tests/test_unit_voce_ascolto.py tests/test_unit_telegram_voce.py tests/test_unit_notte.py -k "not browser"` → 583 passed.
- `python -m pytest -q tests/test_unit_telegram_voce.py tests/test_unit_notte.py tests/test_unit_sottofondo.py tests/test_unit_gate.py tests/test_unit_manutenzione.py tests/test_unit_voice_server.py -k "not browser"` → 1448 passed, 30 deselected.

```
=== RIEPILOGO: 1134 PASS, 0 FAIL ===
```

Fuori scope: SKIP del kernel e test con «browser» (mancano bwrap, browser ed embedding nel container). Sul Mac T74b5 fallisce per PATH_MAX di macOS (preesistente, test con percorsi da ~960 byte): non toccato qui.

## §6 STATO CI

CI NON VERIFICATA (gh assente) con `gh run list`; check run letti con lo strumento GitHub sulla PR #370:
- e9b74f59: unit-suite, handoff-check, verifica-bot success (check suite completata).
- e761eefc: handoff-check e verifica-bot success; check suite completata.
- d5773ec1, fabf2e9: nessuna run propria (pushati insieme al commit di testa successivo).
- Merge di #368 e commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-753-M1-A (decisione dell'operatore) — storia, testo dell'operatore, `recap_pin` e riflessione di fine task (ve #370 V-1 MEDIA, aggiunta qui) possono ancora portare nomi di clienti ai modelli non forti.
- Ve #370 V-2 / bot #370 V-1/V-2 BASSE — buchi del pin anonimo: lapidi dei lead fusi, parole di prossima_azione/note, nomi corti.
- Bot #370 V-3 COSMETICA — commento a gas.py ~4002 non corrisponde al codice.
- Limite noto del pin anonimo: nel testo del diario non si cercano nomi più corti di 3 caratteri né parole più corte di 4.
- Numerazione delle review: la chat di Mani usa anch'essa il suffisso «-M1» (#754-#756-M1); #753-M1 compare due volte (una per chat). Processo, nessun effetto sul codice.
- Riserve precedenti ancora aperte (R-744-M1-1..4, R-750-M1-2/3, ve #366 V-2/V-3): in reports/stato_progetto.md.
