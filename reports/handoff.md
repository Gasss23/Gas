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
- **Riserve basse del browser**: `DEFERITA — si chiudono quando si toccano di nuovo quei file (M1)`.
- **Voce H24 (R8)**: `DEFERITA — prossima fetta, piano a M1 prima del codice`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |   4 ++++
 .github/workflows/ci.yml            |   7 +++++++
 .gitignore                          |   2 ++
 gas.py                              |  27 +++++++++++++++++++++++++--
 gas_identity.md                     |   3 ++-
 modules/gate/gate.py                |   7 ++++++-
 modules/telegram/avviso.py          | 145 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md            |  23 +++++++++++++----------
 reports/handoff.md                  | n/d
 reports/ripartenza_mani.md          |   2 +-
 reports/roadmap.md                  |   2 +-
 reports/stato_progetto.md           |   1 +
 reports/ultimo_report.md            |  29 +++++++++++------------------
 tests/test_unit_avvisa_operatore.py | 181 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_gate.py             |   1 +
 tests/test_unit_kernel.py           |  87 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = b472fe1. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` (comando della CI `python tests/test_unit_kernel.py`, da root): su main pulito 1066 PASS, 1 FAIL; col diff 1071 PASS, 1 FAIL (+5: T102a-e; T68s ha due voci in più nello stesso check). Il FAIL è T31g («gate env GAS_VECTORS=1 costruisce il vector store»), identico su main in questo container: dipende dall'ambiente, fuori scope. Riepilogo reale:

```
=== RIEPILOGO: 1071 PASS, 1 FAIL ===
  FAIL: T31g gate env GAS_VECTORS=1 costruisce il vector store (lazy, no download)
```

`tests/test_unit_avvisa_operatore.py` (nuovo): 29 passed. Con gate e richieste (`python -m pytest tests/test_unit_avvisa_operatore.py tests/test_unit_gate.py tests/test_unit_richieste.py`): 877 passed. Mutanti presi: niente prenotazione, tetto off-by-one, Cf non tolti, cancello SAFE, giorno ignorato (test del modulo); niente tetto per turno, testo nel diario, avvisa_operatore libero a finestra contaminata, tetto per turno solo sui «Successo» (kernel).

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- beb0feb, 4bd1564 (memoria del revisore), c67a2d5 (fetta 36): pushati insieme prima dell'apertura della PR #319. Run 41368996140 su c67a2d5: handoff-check failure (l’handoff era ancora quello della fetta 35: atteso, lo corregge questo commit), unit-suite in corso alla scrittura dell’handoff; verifica-bot skipped (etichetta non ancora messa).
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-612-1 (chat Mani) COSMETICA: il limite di 1000 caratteri si misura sul testo già espanso (<U+XXXX>): messaggio fuorviante, fail-closed.
- R-612-2 (chat Mani) BASSA: il conto del giorno è leggi-poi-scrivi senza lock fra processi (come `.gas_richieste_uso`): due kernel insieme possono superare il tetto di uno.
- Invio vero su Telegram non provato (nessun token in sviluppo).
- Del browser (fetta 35, PR #317 mergiata): R-609-1, R-610-1, V-3 ve #317, V-1 c ve #316, V-1 bot su 384bb3a (sonda di node rilanciata a ogni lettura con Playwright rotto), tutte BASSE; prova dal vero sul VPS prima di accendere il browser.
