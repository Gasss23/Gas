# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Mani, fetta 36 (R6): strumento avvisa_operatore, notifica su Telegram all'operatore (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #319 (https://github.com/Gasss23/Gas/pull/319). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5113242002","url":"https://github.com/Gasss23/Gas/pull/319"}`), perché `gh` nel cloud non è autenticato. La PR tocca `.github/workflows/ci.yml` (macchina del bot): il merge lo decide l'operatore.
2. Sul VPS lo strumento usa `TELEGRAM_BOT_TOKEN` e `TELEGRAM_ALLOWED_IDS` (già del bot); tetto al giorno con `GAS_NOTIFICHE_GIORNO` (default 5).

---

## §1 SCOPE & ESITO FETTE

- **PR #317 (fetta 35)**: `FATTA` — mergiata (b472fe1) col sì dell'operatore.
- **Piano a M1**: `FATTA` — approvato, con le aggiunte di M1: avvisa_operatore UNCERTAIN nel cancello come richiedi_sviluppo, test del cancello, gas_identity.md e prompt di riserva, conto negli stessi elenchi di `.gas_richieste_uso` e in .gitignore, solo il passo in ci.yml.
- **Strumento avvisa_operatore**: `FATTA` — `modules/telegram/avviso.py` (solo `TELEGRAM_ALLOWED_IDS` via `invia_notifica`, prefisso fisso, max 1000 caratteri, invisibili resi `<U+XXXX>`, tetto al giorno su `.gas_notifiche_uso.json` prenotato prima dell'invio, fail-closed, config controllata prima di prenotare); gas.py (una per turno, diario con la sola lunghezza, conto vietato); cancello (UNCERTAIN, conto in livello 3).
- **Conto sul diario** (primo piano, punto 3): `SALTATA — `diario_per_tipo_dal` in degrado restituisce [] (zero notifiche = tetto aperto); file come le richieste di sviluppo, con l'ok di M1`.
- **Review #611 (chat Mani)**: APPROVATO CON RISERVE. R-611-1 MEDIA (Cf letterali nei test), R-611-2 MEDIA (T102d vacuo), R-611-3 BASSA (standard degli invisibili), R-611-4 BASSA (invio fallito non contato per turno), R-611-5 BASSA (.gitignore): `FATTA`, tutte prima del commit.
- **Review #612 (chat Mani)**: APPROVATO CON RISERVE. R-612-1 COSMETICA e R-612-2 BASSA: `DEFERITA — registrate`; R-612-3 (riserve in stato_progetto): `FATTA` in questo commit di fine-task.
- **Bot su 3db59c2 (https://github.com/Gasss23/Gas/pull/319#pullrequestreview-5731093296)**: APPROVATO CON RISERVE, check verifica-bot neutral (la PR tocca ci.yml), CI verde. V-1 BASSA (il tetto di una per turno non copriva i parcheggi alla firma): `FATTA` in b1d1e45. V-2 COSMETICA (ZWJ e FE0F delle emoji espansi in <U+XXXX>): `DEFERITA — registrata`.
- **Verifica esterna su 3db59c2 (https://github.com/Gasss23/Gas/pull/319#issuecomment-6566521136)**: APPROVATO CON RISERVE. V-1 BASSA (lo stesso del bot): `FATTA`. V-2 BASSA (testo non stringa spedito come repr): `FATTA`. V-3 BASSA (GAS_NOTIFICHE_GIORNO=0 diventava 1): `FATTA` — 0 o meno = spento. V-4 COSMETICA (= R-612-1): `DEFERITA`. V-5 BASSA (righe finte dopo il prefisso, non una firma): `DEFERITA — registrata`.
- **Review #613 (chat Mani)**: APPROVATO CON RISERVE. R-613-1 BASSA (i controlli senza costi valevano solo dopo la firma), R-613-2 BASSA (diario del rifiuto al cancello), R-613-3 COSMETICA (messaggio con valori negativi): `FATTA` in b1d1e45. **Review #614**: APPROVATO CON RISERVE. R-614-1 COSMETICA (un controllo di T102g non prova niente da solo) e R-614-2 BASSA (preesistente: argomenti non dizionario → DENY con `_riassumi_args` grezzo nel diario, per ogni strumento): `DEFERITA — registrate`; R-614-3 (riserve in stato_progetto): `FATTA` in questo commit.
- **Bot su 1e4bc90 (https://github.com/Gasss23/Gas/pull/319#pullrequestreview-5731250289)** e **verifica esterna su 1e4bc90 (https://github.com/Gasss23/Gas/pull/319#issuecomment-6566914211)**: APPROVATO CON RISERVE, CI verde (kernel in CI 1076 PASS, 0 FAIL). V-1 BASSA (bot e ve: col tetto del giorno pieno partiva comunque la richiesta di firma): `FATTA` in 20031e4 — `rifiuto_al_cancello` legge il conto senza scriverlo. V-2 BASSA ve (nessun test sul percorso firmato): `FATTA` — T102j end-to-end col trasporto finto. V-3 COSMETICA ve («off» o «0.0» tornavano a 5): `FATTA` — non intero = spento con warning.
- **Review #617 (chat Mani)**: APPROVATO CON RISERVE. R-617-1 COSMETICA (messaggio «a 0 o meno» anche per un valore non intero), R-617-2 COSMETICA (controlli del conto duplicati), R-617-3 BASSA (`rifiuto_al_cancello` senza try suo, retto da quello del kernel): `DEFERITA — registrate`.
- **Riserve basse del browser**: `DEFERITA — si chiudono quando si toccano di nuovo quei file (M1)`.
- **Voce H24 (R8)**: `DEFERITA — prossima fetta, piano a M1 prima del codice`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |   8 ++++++++
 .github/workflows/ci.yml            |   7 +++++++
 .gitignore                          |   2 ++
 gas.py                              |  72 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 gas_identity.md                     |   3 ++-
 modules/gate/gate.py                |   7 ++++++-
 modules/telegram/avviso.py          | 186 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md            |  23 +++++++++++++----------
 reports/handoff.md                  | n/d
 reports/ripartenza_mani.md          |   2 +-
 reports/roadmap.md                  |   2 +-
 reports/stato_progetto.md           |   1 +
 reports/ultimo_report.md            |  32 ++++++++++++++------------------
 tests/test_unit_avvisa_operatore.py | 218 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_gate.py             |   1 +
 tests/test_unit_kernel.py           | 189 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = b472fe1. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
20031e4 fix(telegram): al cancello anche il tetto del giorno, test della firma end-to-end, valore non intero = spento (bot/ve #319 su 1e4bc90, review #617)
1a13c53 chore(revisore): memoria review #617 — APPROVATO CON RISERVE
1e4bc90 docs(fine-task): fetta 36, PR #319, correzioni bot/ve su 3db59c2, review #613-#614
b1d1e45 fix(telegram): una notifica per turno anche alla firma, testo solo stringa, 0 = spento (bot/ve #319, review #613-#614)
6600af1 chore(revisore): memoria review #614 — APPROVATO CON RISERVE
30aff74 chore(revisore): memoria review #613 — APPROVATO CON RISERVE
3db59c2 docs(fine-task): fetta 36, PR #319, strumento avvisa_operatore, review #611-#612
c67a2d5 feat(telegram): strumento avvisa_operatore — notifica all'operatore con tetto (R6, chat Mani)
4bd1564 chore(revisore): memoria review #612 — APPROVATO CON RISERVE
beb0feb chore(revisore): memoria review #611 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit c67a2d5 (gas.py, modules/gate/gate.py, modules/telegram/avviso.py, tests/, gas_identity.md, .github/workflows/ci.yml, .gitignore). Verdetto integrale della review #611 (chat Mani), sulla prima versione del diff:

```
## VERDETTO: APPROVATO CON RISERVE

Review #611 (chat Mani). Fetta R6, `avvisa_operatore`. Diff staged sha256 4579be04d4420b21 (l'ho ricalcolato prima e dopo, è invariato), base b472fe1. Letture obbligatorie fatte: CLAUDE.md (sezioni 5, 8, 9, 10), le sezioni di reports/stato_progetto.md e la memoria del revisore. Ho applicato in particolare le lezioni #1025 e #1029 (file-contatore in tutte le liste sorelle), #976 e #978 (caratteri invisibili Cf) e #408 (privilegio legato al tipo di firma).

**Elementi del diff esaminati**
- `modules/telegram/avviso.py:108` — controlla la configurazione di Telegram PRIMA di prenotare il posto. Rischio: un posto del giorno consumato senza poter inviare, o un tetto pieno che nasconde l'errore vero (lezione 2026-10-31). Esito: ok. `invia_notifica` ripete comunque il controllo, e un test verifica che il conto non venga creato.
- `modules/telegram/avviso.py:120` — prenota il posto prima dell'invio; se la scrittura fallisce, nessun invio. Rischio: tetto aperto quando la scrittura del conto fallisce (lezione #1025). Esito: ok. Un conto rotto o di tipo sbagliato (bool, negativo, lista) dà diniego. I motivi di `invia_notifica` (modules/telegram/bot.py:300) sono stringhe fisse, quindi il token non arriva al modello.
- `modules/telegram/avviso.py:75` — `pulisci` toglie Cc tranne l'a-capo e i Cf. Rischio: testo iniettato che imita una richiesta di firma. Esito: riserva R-611-3. Un testo non può comunque diventare una firma: le firme passano SOLO dai bottoni con callback `ok:<uuid>` (modules/telegram/bot.py:229) e `invia_notifica` non manda bottoni. Il testo semplice al massimo imita a parole «GAS chiede la tua firma», sotto il prefisso fisso.
- `gas.py:4639` — tetto di 1 notifica per turno, saltato solo con `firmata`. Rischio: aggirare il tetto con la firma o con chiamate parallele. Esito: ok. Le chiamate parallele passano una alla volta, quindi la seconda viene negata. Un'azione firmata la decide l'operatore e paga comunque il tetto del giorno. Dopo un riavvio il conto resta sul file. Riserva R-611-4: il tetto conta solo i «Successo».
- `gas.py:4688` — il contatore si azzera all'inizio di run_turn. L'unico altro chiamante di execute_tool_call è applica_firma (`gas.py:3567`, sempre `firmata=True`). Esito: ok.
- `gas.py:2466` — nel diario va solo la lunghezza del testo (F-diario-eco). Esito: ok, T102b lo prova.
- `modules/gate/gate.py:71` — avvisa_operatore è UNCERTAIN, come richiedi_sviluppo. Non sta in `_LIBERI_DOPO_LETTURA`, quindi a finestra contaminata va alla firma (`gas.py:4918`). La contaminazione si aggiorna anche fra chiamate parallele. Esito: ok.
- `modules/gate/gate.py:112` e `gas.py:2021` — il conto è nelle liste di diniego. Ho provato `.GAS_NOTIFICHE_USO.json`, `./`, `x/../`, `.1.tmp` e il nome senza estensione: tutti danno denylist, livello 3 e lettura negata. Nemmeno `firmata` apre il livello 3. Esito: ok, quindi il conto non si può riscrivere. Manca solo `.gitignore` (R-611-5).
- `tests/test_unit_kernel.py:11492` — T102d, «finestra contaminata → cancello, nessun invio». Esito: riserva R-611-2. Il test è vacuo e l'ho provato con un mutante (sotto).

**Finding**
- **R-611-1 MEDIA**: in `tests/test_unit_avvisa_operatore.py:116` e `tests/test_unit_avvisa_operatore.py:135` ci sono U+200B e U+202E LETTERALI. È l'unico file Python del repo con caratteri Cf (scansione con unicodedata su tests/, modules/ e gas.py). Il U+202E rigira la riga 135 in chi la legge (schema Trojan Source). Se il bot li cita come caratteri veri, `scripts/bot_esito.py` dà COMMENT («controlli bidi nel testo», lezione #976). Correzione: costruire le stringhe con `chr(0x200B)` / `chr(0x202E)`.
- **R-611-2 MEDIA**: T102d non prova il cancello. Mutante «`_libero_dopo_lettura` restituisce True per avvisa_operatore» nel kernel: 1070 PASS e 1 FAIL, lo stesso numero della baseline dichiarata (non ho verificato che il FAIL sia T31g). T102d passa con l'output «Operazione negata: Telegram non configurato», cioè l'azione è stata ESEGUITA libera. Il test passa lo stesso perché, a token spento, anche l'esecuzione libera è «negata» e non invia nulla. I test sul cancello in test_unit_avvisa_operatore coprono `gate_classify` e `libero_dopo_lettura`, ma non come il kernel li collega. Correzione: tenere il token, sostituire il read-back con un finto riuscito e pretendere `cancello == "in_attesa"` più una riga pending con tool avvisa_operatore; poi rilanciare il mutante.
- **R-611-3 BASSA**: `pulisci` lascia passare U+2028/U+2029 (Zl/Zp), NBSP, il riempitivo Hangul U+3164 e i selettori di variante, verificato. `rendi_visibili` del bot è più severa. Il rischio in più è piccolo, visto che l'a-capo è comunque ammesso, ma lo standard non è coerente.
- **R-611-4 BASSA**: il tetto per turno conta solo i «Successo», mentre un invio fallito consuma il posto del giorno. Con Telegram giù il modello può bruciare tutti e 5 i posti in un turno, e l'avviso importante successivo resta bloccato fino a domani. Correzione: contare ogni chiamata che ha prenotato un posto.
- **R-611-5 BASSA**: `.gas_notifiche_uso.json` e `.gas_notifiche_uso.json.*.tmp` mancano dal diff staged (lezione #1029). Nel working tree c'è già una modifica NON staged di `.gitignore` che le aggiunge: va messa nello stage. Lo stage cambia lo sha del diff, quindi servono ri-review e nuovo marcatore.

Consiglio di chiudere R-611-1, R-611-2 e R-611-5 in questa stessa fetta prima della PR: sono correzioni da poche righe. Il codice di produzione non ha difetti che bloccano: zero eccezioni che escono (tutto in try, ogni errore va in log.warning), i guardrail (10 iterazioni, `_get_window`) non sono toccati e nel diff non ci sono slicing della storia né output di tool simulati. Il diff tocca ci.yml (macchina del bot), quindi il merge spetta all'operatore.

**Prove riprodotte da me**
- avvisa + gate: 850 passed.
- Mutante R-611-2 su una copia in `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/m1`: T102d PASS col mutante.

**Rischi esclusi**
- Invio reale a Telegram e resa di U+2028/U+3164 nel client: non verificati, mi mancano token e client.
- Corsa fra due processi (bot e CLI) sul conto: lettura-modifica-scrittura senza lucchetto, come in richieste.py. Non provata. Il superamento è limitato al numero di processi contemporanei.
- Le altre suite (kernel completo senza mutante, richieste, hooks, notte): non rilanciate, mi fido delle prove riferite (1282 passed e 1070/1). Anche la baseline del FAIL T31g su main non l'ho verificata.

**Memoria**: riga #611 e lezione nuova (test del cancello vacuo a canale spento) aggiunte e committate con `scripts/commit_memoria_revisore.sh` (beb0feb, solo /home/user/Gas/.claude/agents/memoria_revisore.md). L'index del diff sotto review è intatto.
```

Verdetto integrale della review #612 (chat Mani), sul diff finale del commit c67a2d5:

```
## VERDETTO: APPROVATO CON RISERVE

Review #612 (chat Mani). È la ri-review della #611 sulla fetta R6 avvisa_operatore. Ho revisionato il diff staged: sha256 57c067730a569ff1…, che coincide col tuo e resta invariato dopo il mio commit. Base b472fe1, branch claude/peaceful-lovelace-0w2b7q.

Letture fatte: CLAUDE.md (sezioni 5, 8, 9 e 10), reports/stato_progetto.md (Grep mirato), .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `tests/test_unit_avvisa_operatore.py:118` — parametri di test_testo_vuoto e test_invisibili_e_controlli_resi_visibili costruiti con chr(). Rischio esaminato: caratteri Cf/bidi letterali, cioè il problema Trojan Source di R-611-1. Ho scansionato tutti i caratteri dei due file nuovi: zero Cf, Cc (escluso l'a-capo), Zl, Zp e Zs diversi dallo spazio. **ok**
- `tests/test_unit_kernel.py:11501` — T102d, a Telegram acceso, sostituisce `invia_read_back` con un finto riuscito e lo ripristina nel finally. Pretende `cancello == "in_attesa"`, 1 read-back e una riga pending col tool avvisa_operatore. Rischio esaminato: test vacuo (R-611-2). Mutante in `gas.py:3118` (`_libero_dopo_lettura` → True per avvisa_operatore) su una copia dell'indice: 1070 PASS, 2 FAIL (T31g, **T102d**). Il patch su `gas._tg_bot` colpisce lo stesso oggetto modulo usato in `gas.py:3409`. **ok**
- `gas.py:4643` e `gas.py:4651` — tetto per turno: si nega se `_avvisi_turno >= 1` e si conta a ogni `prenotato`, solo se l'azione non è firmata. Il contatore si azzera in `gas.py:4690`. L'unico chiamante non firmato è run_turn (`gas.py:4941`); quello firmato è applica_firma (`gas.py:3567`). Rischio esaminato: un Telegram giù che brucia in un turno tutti i posti del giorno (R-611-4). Mutante «conta solo Successo» (`out.startswith("Successo")`): 1070 PASS, 2 FAIL (T31g, **T102e**). **ok**
- `modules/telegram/avviso.py:76` — `pulisci` passa da `rendi_visibili` (vedi `modules/telegram/bot.py:136`). Un testo che non ha nessun carattere che resta uguale a sé stesso dopo `rendi_visibili` diventa vuoto e viene negato. Provato: solo selettori di variante o tag (U+FE0F, U+E0041) → vuoto; solo tab e a-capo → vuoto. Il controllo `avvisa_operatore_esito` (`modules/telegram/avviso.py:107`) rende `prenotato=True` anche dall'except se l'eccezione arriva dopo la prenotazione. Nessuna eccezione esce (§9). **ok**
- `.gitignore:58` — `.gas_notifiche_uso.json` e `.gas_notifiche_uso.json.*.tmp`, verificati con `git check-ignore -v` (R-611-5). **ok**
- Wall of Shame: nessuno slicing della history nelle righe aggiunte; i `[:400]` sono tagli dei messaggi dei check. Nessuna simulazione di tool: il finto invio vive solo nei test. Cap di 10 iterazioni e `_get_window` non toccati. **ok**

**Prove riprodotte** (su un export dell'indice nella cartella di lavoro temporanea)
- avvisa + gate + richieste: 877 passed.
- kernel: 1071 PASS, 1 FAIL (T31g, come dichiarato). T102a–e tutti PASS.

**Finding**
- **R-612-1 COSMETICA**: il limite di 1000 caratteri si misura sul testo già espanso, quindi 200 U+200B più una «a» contano 1601. Il modello riceve «testo oltre 1000 caratteri» per un testo di 201. È fail-closed, ma il messaggio inganna. Correzione possibile: misurare `s` prima di `rendi_visibili`, oppure dire «oltre 1000 caratteri visibili/espansi».
- **R-612-2 BASSA (da dichiarare)**: il conto del giorno (`modules/telegram/avviso.py:64`) è un leggi-poi-scrivi senza lock fra processi, come `.gas_richieste_uso`. Due kernel sulla stessa root (bot e voce) possono superare il tetto di uno con una corsa. Basso rischio per delle notifiche.
- **R-612-3 BASSA**: le riserve R-611-x e R-612-x non sono ancora in reports/stato_progetto.md (Grep su «avvisa_operatore»: nessuna riga). Vanno tracciate prima del commit o della PR, come chiede il gate.

**Rischi esplicitamente esclusi**
- Invio reale su Telegram e formato del messaggio sul client: non provati, nessun token né rete verso Telegram in dev. Ho visto solo che `invia_notifica` viene chiamata (test_invio_vero_usa_invia_notifica).
- Esecuzione firmata (applica_firma → avvisa_operatore con `firmata=True`) end-to-end: non provata con un mutante. Ho verificato solo leggendo il codice che il tetto per turno viene saltato e quello del giorno resta.
- La CI non l'ho guardata: ho controllato solo che il passo nuovo in `.github/workflows/ci.yml` lanci il file di test giusto.

**Nota di processo**: il primo giro di mutanti è girato per errore sulle cartelle m1/m2 rimaste dalla review #611 (`cp -r` ha annidato la copia, quindi la suite girava sul diff vecchio). L'ho scartato e rifatto in cartelle nuove; i risultati sopra sono quelli giusti. La lezione è in memoria.

**Memoria**: aggiunta la riga #612 più una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da `scripts/commit_memoria_revisore.sh` (commit 4bd1564). L'indice staged non è cambiato (sha256 ancora 57c067730a569ff1…).
```

Commit b1d1e45 (gas.py, modules/telegram/avviso.py, tests/: V-1 bot/ve, V-2 e V-3 ve su 3db59c2). Verdetto integrale della review #613 (chat Mani), sulla prima versione:

```
## VERDETTO: APPROVATO CON RISERVE

Review #613 (chat Mani). Ho esaminato il diff staged: lo sha256 inizia per de9968aef5807fae, combacia ed è rimasto uguale anche dopo il commit della memoria. La base è 3db59c2, sul branch claude/peaceful-lovelace-0w2b7q. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (solo le parti che servivano) e .claude/agents/memoria_revisore.md. Ho ignorato il `git stash` (voce H24), come richiesto.

**Elementi del diff esaminati**
- `gas.py:4466`: la costante di classe `_UNA_NOTIFICA_PER_TURNO`, usata sia in `execute_tool_call` (`gas.py:4648`) sia nel ramo del cancello. Rischio esaminato: due messaggi diversi per lo stesso rifiuto, oppure un prefisso che non comincia più con «Operazione negata». Esito: ok, il testo comincia con «Operazione negata».
- `gas.py:4934`: nel ramo del cancello di `run_turn`, `avvisa_operatore` con `_avvisi_turno >= 1` viene negata prima di `_parcheggia_e_notifica`, con `_cancello="negata"`. Rischi esaminati:
  - `self._avvisi_turno` letto senza `getattr`: è sicuro, perché viene azzerato all'inizio di `run_turn` (`gas.py:4693`);
  - un doppione «Azione già in attesa» non conta: non manda niente di nuovo, quindi va bene;
  - due chiamate parallele nella stessa risposta: la seconda viene negata.
  - Esito: ok. Mutante che toglie il controllo (`if False:`): T102f FAIL.
- `gas.py:4944`: un parcheggio riuscito (`in_attesa`) fa salire di 1 il conto del turno. Rischio esaminato: un parcheggio fallito («Operazione negata», per esempio Telegram spento) non conta, e questo è coerente con «niente è partito». Esito: ok. Mutante che toglie l'incremento: T102f FAIL.
- `gas.py:4934` (lato diario): nel ramo «negata» nuovo `_gate_diario` resta None, quindi il diario passa da `_riassumi_args`. Esito: **riserva R-613-2**, vedi sotto.
- `modules/telegram/avviso.py:116`: un testo non stringa viene negato prima di `pulisci` e senza prenotare posti; None continua a dare «serve un 'testo' non vuoto». Ho sondato 0, False, b"", [] (danno «deve essere una stringa») e None, "", "  " (danno «serve un testo»). Esito: ok. Mutante: 5 failed.
- `modules/telegram/avviso.py:45` e `modules/telegram/avviso.py:133`: con `max(0, …)` il valore 0 o negativo significa «spento», con un rifiuto dichiarato e senza invio né file del conto. Ho sondato "0", "-3" e " 0 " (spento); "abc" e "" tornano al default 5, come prima. Con il conto rotto e tetto 0 prevale «conto illeggibile», che resta fail-closed. Esito: ok. Mutanti `max(1)` e «tolto `tetto==0`»: 2 failed ciascuno.
- `tests/test_unit_kernel.py:11542` (T102f): fa read_file, poi due `avvisa_operatore`, e pretende `in_attesa` poi `negata`, 1 read-back, 1 riga in attesa e 0 invii. È una prova positiva del parcheggio, non vuota (lezione della #611). Esito: ok.
- `tests/test_unit_avvisa_operatore.py:125` e `tests/test_unit_avvisa_operatore.py:134`: test con parametri per i testi non stringa (pretendono anche niente posto prenotato e niente file del conto) e per il tetto 0/-3. Esito: ok.

**Prove riprodotte** (su un export nuovo dell'indice in una cartella r613 del scratchpad, più la suite in place)
- Test avvisa + gate + richieste: 884 passed.
- Kernel: 1072 PASS, 1 FAIL (T31g, problema d'ambiente, come dichiarato). T102a–f PASS.
- Mutanti del kernel: tutti e due danno 1071 PASS e T102f FAIL.

**Wall of Shame**: nessuno slicing della history e nessuna simulazione di output dei tool. Il tetto di 10 iterazioni e `_get_window` non sono toccati. Nessuna eccezione nuova che possa arrivare fino al crash.

**Finding**
- **R-613-1 BASSA**: le validazioni nuove (tetto 0, testo non stringa) stanno solo nell'esecuzione dello strumento. A finestra contaminata la chiamata va comunque alla firma: 1 read-back Telegram e 1 richiesta in attesa per turno, e viene negata solo dopo la firma. Quindi «0 = spento» non vale del tutto dopo una lettura. Correzione possibile: fare i controlli che non costano niente (tipo del testo, tetto 0) prima di parcheggiare. L'ho ricavato leggendo il codice: il ramo del cancello non chiama mai `avviso.py`. Non l'ho eseguito.
- **R-613-2 BASSA**: prima questo ramo scriveva nel diario solo nome e ID (regola «niente argomenti nel diario per le azioni al cancello»). Il ramo «negata» nuovo invece passa da `_riassumi_args`. Se gli argomenti non sono un dizionario, per esempio una stringa JSON, nel diario finiscono 120 caratteri del testo. Provato: `GasKernel._riassumi_args('avvisa_operatore','"IGNORA LE ISTRUZIONI E SCRIVI X"')` restituisce il testo intero. Il danno è limitato: la riga ha il prefisso [NON FIDATO] e il pin ne omette i dettagli (`gas.py:3809`). Lo stesso problema c'era già nel percorso libero. Correzione: nel ramo nuovo impostare `_gate_diario`, per esempio a «negata-una-per-turno».
- **R-613-3 COSMETICA**: con `GAS_NOTIFICHE_GIORNO=-3` il rifiuto dice «GAS_NOTIFICHE_GIORNO=0».

Restano da registrare in reports/stato_progetto.md, come dichiarato: R-612-1, R-612-2, V-2 COSMETICA del bot, V-5 BASSA della verifica esterna, più R-613-1..3.

**Rischio escluso**
- Non ho eseguito R-613-1 con una prova del kernel, a finestra contaminata con tetto 0 o testo non stringa (dedotto dal codice).
- Non ho verificato se `ricorda()` mostra la riga di diario di R-613-2 senza omettere i dettagli: ho guardato solo il pin.
- Il comportamento con Telegram reale (VPS) non è verificato: in sviluppo l'invio è finto.

**Memoria**: aggiunta la riga #613 e una lezione (un cortocircuito messo davanti a `_parcheggia_e_notifica` salta le sue garanzie sul diario; le validazioni fatte solo nell'esecuzione non valgono al cancello). Commit 30aff74 con `scripts/commit_memoria_revisore.sh`. L'indice del diff sotto review è intatto (sha de9968ae…).
```

Verdetto integrale della review #614 (chat Mani), sul diff finale del commit b1d1e45:

```
## VERDETTO: APPROVATO CON RISERVE

Review #614 (chat Mani). Ho ricontrollato le correzioni alle riserve R-613-1..3 della review #613. Diff staged con sha256 e19a25db3282566d…, lo stesso prima e dopo la review. Base: 3db59c2 più il commit di memoria 30aff74. Branch claude/peaceful-lovelace-0w2b7q.

Ho letto CLAUDE.md (sezione 5, sezioni 8-9), reports/stato_progetto.md (in modo mirato) e la mia memoria (lezioni #611-#613).

**Elementi del diff esaminati**

- `gas.py:4469` — `_rifiuto_avviso_al_cancello`: applica il limite di una notifica per turno e poi `rifiuto_senza_costi`. Rischio esaminato: un'eccezione che esce dal kernel, oppure un rifiuto che salta la firma per sbaglio. Prove dirette: senza `_avvisi_turno` (AttributeError), con `rendi_visibili` rotto (RuntimeError) e con JSON rotto, il metodo restituisce None, scrive un warning `[GATE]` e la chiamata si parcheggia. Nel dubbio quindi resta la firma. Con `GAS_NOTIFICHE_GIORNO=abc` vale il default 5 (non è spento); con -3 lo strumento risulta spento. — ok
- `gas.py:4954` — ramo del cancello che rifiuta prima di `_parcheggia_e_notifica`. Imposta `_gate_diario="avviso-negato-al-cancello"` e `_cancello="negata"`. Rischio esaminato (lezione #613): un cortocircuito che salta le garanzie del parcheggio. Il diario non porta argomenti e prende comunque il prefisso NON FIDATO. Il controllo "una per turno" ora finisce anch'esso sotto l'etichetta. — ok
- `gas.py:4963` — `self._avvisi_turno += 1` solo per i parcheggi in_attesa. Sta fuori da un try, ma `run_turn` lo inizializza sempre (`gas.py:4709`). Non può crashare. — ok
- `modules/telegram/avviso.py:109` — `rifiuto_senza_costi`: tipo, vuoto, lunghezza, spento. `modules/telegram/avviso.py:132` la richiama dentro il try di `avvisa_operatore_esito`, quindi vale anche dopo la firma. «Spento» ora viene prima della configurazione e del conto. Il messaggio dice «a 0 o meno» (R-613-3 chiusa). — ok
- `modules/telegram/avviso.py:42` — `_max_giorno` con `max(0, …)`. Un valore negativo diventa 0, cioè spento. — ok
- `tests/test_unit_kernel.py:11574` — T102g, ho provato i mutanti in cartelle con nome nuovo:
  - etichetta del diario tolta → T102g FAIL;
  - `rifiuto_senza_costi` tolta dal cancello → T102g FAIL;
  - controllo «spento» tolto → T102g FAIL, più 2 failed in `tests/test_unit_avvisa_operatore.py:134`.
  — ok, ma vedi R-614-1
- Prove rifatte su un export dell'indice:
  - avvisa + gate + richieste: 884 passed;
  - kernel: 1073 PASS, 1 FAIL (T31g, dipende dall'ambiente: fastembed assente).
- Wall of Shame: nessuno slicing della history, nessun output di tool simulato. Il tetto di 10 iterazioni e `_get_window` non sono toccati.

**Riserve**

- **R-614-1 COSMETICA**: in T102g il controllo «SEGRETO-102 assente dal diario» non prova niente. `_riassumi_args` su `{"testo": [...]}` scrive già solo «testo=17 caratteri», quindi il testo non entrerebbe comunque. Il mutante cade solo sul controllo dell'etichetta. Si può lasciare così o aggiungere un caso in cui `_riassumi_args` farebbe davvero uscire il testo.
- **R-614-2 BASSA, problema già esistente e fuori dal diff**: con argomenti che non sono un dizionario, `gate_classify` dà DENY e il diario passa da `_riassumi_args`, che scrive la stringa grezza. L'ho verificato: `_riassumi_args('avvisa_operatore', '"SEGRETO stringa json"')` restituisce il testo intero. Vale per qualunque strumento. Da segnare in stato_progetto.md come finding aperto.
- **R-614-3 BASSA**: le riserve R-611..R-614 non sono ancora in reports/stato_progetto.md (riprende R-612-3). Vanno riportate a fine task.

**Cosa NON ho verificato**: l'invio reale su Telegram e il read-back reale verso il telefono, perché in dev non c'è token. Ho visto solo il canale finto dei test. Non ho controllato nemmeno il comportamento con due kernel sulla stessa root (R-612-2, nessun lock fra processi), perché non è toccato da questo diff.

Riga contatore #614 aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata da sola con `scripts/commit_memoria_revisore.sh` (commit 6600af1, nessuna lezione nuova). L'indice staged è intatto (sha256 ancora e19a25db…). Dopo questo verdetto puoi lanciare `bash scripts/segna_review_ok.sh`.
```

Commit 20031e4 (gas.py, modules/telegram/avviso.py, tests/: V-1 bot/ve, V-2 e V-3 ve su 1e4bc90). Verdetto integrale della review #617 (chat Mani):

```
## VERDETTO: APPROVATO CON RISERVE

Review #617 (chat Mani). Ho esaminato il diff staged su claude/peaceful-lovelace-0w2b7q, sopra 1e4bc90. Lo sha256 inizia per 8b2934ec280632f1 ed era identico prima e dopo il commit della memoria. Prima della review ho letto CLAUDE.md, la parte di reports/stato_progetto.md sulla fetta 36 e la coda di .claude/agents/memoria_revisore.md (review #611-#614).

### Elementi del diff esaminati
- `modules/telegram/avviso.py:132` — `rifiuto_al_cancello(testo, root)` ripete i controlli senza costi, poi legge il conto con `_uso_oggi`. Rischi esaminati: che il cancello prenoti un posto; che un conto rotto lasci passare la richiesta; che il conto scritto al cancello e quello letto all'esecuzione non coincidano. — **ok**. Il conto non viene mai scritto. Conto illeggibile → rifiuto. Il tetto viene ricontrollato anche all'esecuzione firmata, quindi un giorno che si riempie fra parcheggio e firma resta bloccato lì. Il mutante «il cancello prenota il posto» fa fallire T102j (n=2) e il test del modulo (1 failed).
- `gas.py:4469` — `_rifiuto_avviso_al_cancello` ora chiama `rifiuto_al_cancello(..., self.root)`. È la stessa root dell'esecuzione (`gas.py:4669`). Rischio esaminato: un'eccezione nel controllo. — **ok**. Il try esistente la trasforma in un warning e la chiamata va comunque al parcheggio, dove la firma resta il cancello. Il mutante «al cancello solo rifiuto_senza_costi» fa fallire T102i.
- `modules/telegram/avviso.py:42` — `_max_giorno`: con un valore non intero ora restituisce 0 (spento) e scrive un warning; vuoto o di soli spazi → default 5. Rischio esaminato: tool spento per errore. — **riserva cosmetica (R-617-1)**. Ho provato i valori: «off» → 0, «5.0» → 0, « 3 » → 3, «+2» → 2, «1_0» → 10.
- `tests/test_unit_kernel.py:11605` — T102j copre il percorso firmato completo: _TgFinto vero, parcheggio che conta 1 per turno, click con `_clicca77`, sendMessage con PREFISSO, conto a 1. Rischio esaminato: un test vuoto, che passa anche col codice sbagliato. — **ok**. Il mutante «tolto `not firmata and`» (`gas.py:4665`) fa fallire T102j. Un'eccezione dentro il blocco finisce nel check «T102 blocco senza eccezioni», e `_invia_default` e `invia_read_back` vengono ripristinati nei finally.
- `tests/test_unit_kernel.py:11582` — T102i: conto 5/5 e finestra contaminata → negata, 0 read-back, 0 richieste in attesa. Ha senso perché il mutante m1 lo fa cadere. — **ok**.
- `tests/test_unit_avvisa_operatore.py:148` — test del modulo: il conto resta 5, conto rotto → «illeggibile», testo non stringa → rifiuto. — **ok**.

### Prove riprodotte (su una copia dell'indice nel scratchpad, cartelle nuove)
- avvisa + gate + richieste: **890 passed**. Kernel: **1075 PASS, 1 FAIL (T31g, problema d'ambiente)**. Coincide con quanto dichiarato.
- 3 modifiche apposta sbagliate al codice (mutanti), tutte prese (il codice di base fallisce solo T31g):
  - m1: al cancello solo `rifiuto_senza_costi` → T102i FAIL.
  - m2: tolto `not firmata and` → T102j FAIL.
  - m3: il cancello prenota il posto → T102j FAIL + 1 failed pytest.
- Nel diff non ci sono caratteri invisibili Cf/Zl/Zp (lezione R-611-1) né tagli diretti della cronologia.

### Riserve
- **R-617-1 COSMETICA**: con un valore non intero («off», «5.0») il rifiuto dice «GAS_NOTIFICHE_GIORNO a 0 o meno» (`modules/telegram/avviso.py:128`), che è falso. Chi scrive «5.0» intendendo 5 si ritrova lo strumento spento. Resta un blocco sicuro (fail-closed), ma l'unica traccia è il warning nel log.
- **R-617-2 COSMETICA**: i messaggi e la logica di «conto illeggibile» e «tetto raggiunto» sono duplicati fra `rifiuto_al_cancello` (`modules/telegram/avviso.py:139`) e `avvisa_operatore_esito` (`modules/telegram/avviso.py:165`). Rischio: che col tempo divergano.
- **R-617-3 BASSA, da dichiarare**: `rifiuto_al_cancello` non ha un try suo. Può sollevare (Path.exists su EACCES, import fallito). La regge il try del kernel e la chiamata va al parcheggio, quindi niente crash né invio. Però il docstring del modulo, «nessuna eccezione esce», per questa funzione non vale.

### Rischio escluso
Non ho verificato l'invio vero su Telegram, né che il messaggio col prefisso arrivi davvero alla chat di TELEGRAM_ALLOWED_IDS: T102j controlla testo e conto, non il chat_id. Serve un bot reale, non disponibile in dev. Non ho rifatto nemmeno la corsa fra processi sul conto (R-612-2, già aperta).

### Memoria
Riga contatore #617 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con `scripts/commit_memoria_revisore.sh` (commit 1a13c53, solo quel file). Il resto dell'index è intatto. Nessuna lezione nuova.
```

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` (comando della CI `python tests/test_unit_kernel.py`, da root): su main pulito 1066 PASS, 1 FAIL; col diff 1075 PASS, 1 FAIL (+9: T102a-j senza h; T68s ha due voci in più nello stesso check). Il FAIL è T31g («gate env GAS_VECTORS=1 costruisce il vector store»), identico su main in questo container: dipende dall'ambiente, fuori scope. Riepilogo reale:

```
=== RIEPILOGO: 1075 PASS, 1 FAIL ===
  FAIL: T31g gate env GAS_VECTORS=1 costruisce il vector store (lazy, no download)
```

`tests/test_unit_avvisa_operatore.py` (nuovo): 42 passed. Con gate e richieste (`python -m pytest tests/test_unit_avvisa_operatore.py tests/test_unit_gate.py tests/test_unit_richieste.py`): 890 passed. In CI su 1e4bc90 il kernel dà 1076 PASS, 0 FAIL (T31g passa lì). Mutanti presi: niente prenotazione, tetto off-by-one, Cf non tolti, cancello SAFE, giorno ignorato (test del modulo); niente tetto per turno, testo nel diario, avvisa_operatore libero a finestra contaminata, tetto per turno solo sui «Successo», niente tetto per turno al cancello, niente controlli senza costi al cancello, diario del rifiuto senza etichetta (kernel); testo non stringa accettato, «spento» tolto (modulo); al cancello senza il tetto del giorno, tetto per turno anche sulla firma (kernel).

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- beb0feb, 4bd1564 (memoria del revisore), c67a2d5 (fetta 36): pushati insieme prima dell'apertura della PR #319; run 41368996140 su c67a2d5: handoff-check failure (l'handoff era ancora quello della fetta 35, atteso), unit-suite success.
- 3db59c2 (fine-task): run 41369132632 su 3db59c2 success (unit-suite, handoff-check); verifica-bot neutral (la PR tocca ci.yml, bot APPROVATO CON RISERVE).
- 30aff74, 6600af1 (memoria #613, #614), b1d1e45 (correzioni), 1e4bc90 (fine-task): run 41371890790 su 1e4bc90 success (unit-suite, handoff-check); verifica-bot neutral (bot APPROVATO CON RISERVE).
- 1a13c53 (memoria #617), 20031e4 (correzioni) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-612-1 (chat Mani) COSMETICA: il limite di 1000 caratteri si misura sul testo già espanso (<U+XXXX>): messaggio fuorviante, fail-closed.
- R-612-2 (chat Mani) BASSA: il conto del giorno è leggi-poi-scrivi senza lock fra processi (come `.gas_richieste_uso`): due kernel insieme possono superare il tetto di uno.
- V-2 bot su 3db59c2 COSMETICA: ZWJ e FE0F delle emoji legittime arrivano come <U+XXXX> e consumano il limite.
- V-5 ve #319 BASSA: il testo può contenere righe finte dopo il prefisso (non è una firma: le firme passano solo dai bottoni).
- R-614-1 (chat Mani) COSMETICA: in T102g il controllo «testo assente dal diario» non prova niente da solo (cade il controllo dell'etichetta).
- R-614-2 (chat Mani) BASSA, preesistente: argomenti non dizionario → DENY del cancello con `_riassumi_args` grezzo nel diario, per ogni strumento.
- R-617-1 (chat Mani) COSMETICA: con un valore non intero il rifiuto dice «a 0 o meno».
- R-617-2 (chat Mani) COSMETICA: controlli del conto duplicati fra `rifiuto_al_cancello` e `avvisa_operatore_esito`.
- R-617-3 (chat Mani) BASSA: `rifiuto_al_cancello` senza try suo (lo regge quello del kernel: la chiamata va alla firma).
- Invio vero su Telegram non provato (nessun token in sviluppo).
- Del browser (fetta 35, PR #317 mergiata): R-609-1, R-610-1, V-3 ve #317, V-1 c ve #316, V-1 bot su 384bb3a (sonda di node rilanciata a ogni lettura con Playwright rotto), tutte BASSE; prova dal vero sul VPS prima di accendere il browser.
