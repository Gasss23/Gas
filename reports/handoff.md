# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-27/28 — Mani fetta 21 con secondo giro: riserve basse di #277 chiuse, lettura con lexbor sempre spenta, chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #280 (https://github.com/Gasss23/Gas/pull/280). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5037069764","url":"https://github.com/Gasss23/Gas/pull/280"}`); `gh` nel cloud non è autenticato. Bot e verifica esterna su d78843f: APPROVATO CON RISERVE; merge AUTORIZZATO dall'operatore il 2026-10-28 («mergia 280»), lo fa l'agente con CI verde e senza conflitti. Il merge non accende niente.
2. Accensione: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`; poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Shadow DOM dichiarativo: nascondere i figli «light» di un host con `<template shadowrootmode>` toglierebbe anche il contenuto negli slot delle pagine vere. Decisione dell'operatore.
4. Poi, una alla volta: R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7. Per ripartire dopo il `/clear` basta una riga: «Sei la chat Mani di Gas: leggi reports/ripartenza_mani.md e segui le istruzioni.»

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #277**: `FATTA` — richiesta dell'operatore («mergia»), merge fb1f54b.
- **Riserve basse di #277 (fetta 21)**: `FATTA`.
  - V-1 ve #277 su 6a58806 (`size` enorme), V-3 ve (test mancanti), R-bot277-4 (soglia in secondi), R-ve277-5 parte lexbor (video/audio/meter/progress), V-2 bot (docstring), docstring di R-ve277-4: `FATTA`.
  - R-531-1, R-531-2 (cosmetiche della review #531): `FATTA`.
  - Shadow DOM dichiarativo: `DEFERITA — decisione dell'operatore`.
  - Bot V-1 (test del figlio saltati in CI): `DEFERITA — serve la chat Motore (requirements-dev)`.
  - Cosmetiche R-ve277-3, R-ve277-4 (`sys.platform`), R-529-1, R-528-3, R-526-1, R-520-4: `DEFERITA — cosmetiche, verso sicuro`.
- **Secondo giro (bot e verifica esterna su ae588e6, APPROVATO CON RISERVE; commento ve: https://github.com/Gasss23/Gas/pull/280#issuecomment-6447071730)**:
  - V-1 ve MEDIA (conflitto con main) → merge di 24ed87d in 7b6bc24, review #533: `FATTA`; R-533-1 cosmetica: `FATTA`.
  - V-2 ve (confine 2**31) → c23e6c6, review #534: `FATTA`.
  - V-1 bot (riga morta di misura_web.py, strumento dichiarato fuori dal perimetro di review), V-2 bot su c5b69f3 (docstring del file di test), V-4 ve / V-2 bot (numeri): `FATTA`.
  - V-3 ve (test nuovi saltati in CI): `DEFERITA — chat Motore`. V-5 ve: coincide con V-1 bot.
- **Terzo giro (2026-10-28)**: verdetti su d78843f APPROVATO CON RISERVE (commento ve: https://github.com/Gasss23/Gas/pull/280#issuecomment-6447473176); riserve segnate DA SISTEMARE su richiesta dell'operatore (R-ve280-1/2/3, R-bot280-1/2): `FATTA`. PR di nuovo in conflitto → merge di main 52fc615 in 465ba13, review #535: `FATTA`; R-535-1 cosmetica: `FATTA`. Ripartenza ridotta a una riga da incollare: `FATTA`. Nessun codice nuovo della chat Mani: niente verifica esterna nuova. Bot su fe8992f: V-1 MEDIA (PR di nuovo in conflitto: main era avanzato con la PR #282, solo report) → merge di bc4befb in 1cfc9ab, niente perimetro, niente review; V-2 cosmetica (descrizione della PR coi numeri vecchi) → descrizione aggiornata: `FATTA`.
- **Riassunto e ripartenza dopo il `/clear`** (richiesta dell'operatore): `FATTA` — `reports/ripartenza_mani.md`, strumento di misura in `reports/strumenti_mani/misura_web.py`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md   |   6 ++++++
 modules/web/leggi.py                 |   5 +++--
 modules/web/lexbor.py                |  21 +++++++++++++--------
 reports/diff_sessione.md             |  12 +++++++++---
 reports/handoff.md                   | n/d (commit finale)
 reports/ripartenza_mani.md           |  36 ++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md            |   4 +++-
 reports/strumenti_mani/misura_web.py | 137 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ultimo_report.md             |  43 ++++++++++++++++++++++++++++++++++++++-----
 tests/test_unit_web_lexbor.py        |  39 ++++++++++++++++++++++++++++++++++-----
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat bc4befb` preso con i report in stage, prima del commit finale. BASE = `git merge-base origin/main HEAD` = bc4befb (dopo i merge di main 465ba13 e 1cfc9ab): gas.py, modules/memory/store.py, tests/test_unit_kernel.py, CLAUDE.md e i report della notte arrivano da main e non sono nel diff.

## §3 GIT LOG --ONELINE (sessione)

```
1cfc9ab Merge origin/main (bc4befb, PR #282) in claude/peaceful-lovelace-0w2b7q (PR #280)
fe8992f docs(fine-task): PR #280 dopo il merge di main 52fc615 — riserve da sistemare, ripartenza in una riga, review #535
465ba13 Merge origin/main (52fc615, PR #281) in claude/peaceful-lovelace-0w2b7q (PR #280)
d78843f docs(fine-task): PR #280 dopo il merge di main 24ed87d — verdetti su ae588e6, review #533-#534
c23e6c6 test(web): confine 2**31 del size fissato da test, docstring allineata (PR #280)
e0521bd chore(revisore): memoria review #534 — APPROVATO
7b6bc24 Merge origin/main (24ed87d, PR #279) in claude/peaceful-lovelace-0w2b7q (PR #280)
ae588e6 docs(fine-task): Mani fetta 21 — report, handoff, stato, ripartenza dopo il clear (PR #280, review #531-#532)
c5b69f3 fix(web): riserve basse di #277 — size enorme, test mancanti, video/audio/meter/progress (fetta 21 Mani)
a2518f1 chore(revisore): memoria review #532 — APPROVATO
8a0d0d5 chore(revisore): memoria review #531 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore c5b69f3: review #531 sul primo diff e #532 dopo la chiusura di R-531-1/2. Merge 7b6bc24 (da main entrano gas.py e tests/test_unit_kernel.py): review #533. Commit motore c23e6c6: review #534. Merge 465ba13 (da main entrano gas.py, modules/memory/store.py, tests/test_unit_kernel.py): review #535. Verdetti integrali:

### Review #531 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #531 (chat Mani), fetta 21 lexbor: chiude le riserve BASSE della PR #277. Diff in stage: modules/web/lexbor.py, modules/web/leggi.py, tests/test_unit_web_lexbor.py. Prima della review ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (le voci su lexbor) e la mia memoria.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:97` — `intero()` tiene al massimo 11 cifre significative, salta gli zeri in testa e accetta il valore solo se è sotto 2**31. Rischio esaminato: il figlio cade (era il ValueError di int() con più di 4300 cifre), un valore oltre il tetto viene preso per valido, il ciclo diventa lento. Prove con valori limite fatte da me: 21474836470 e 2147483648 danno la tendina; 2147483647, `+0003` e `   +12x` danno la lista; 0 e 00 danno la tendina; 2 milioni di zeri prima di un 5 vengono letti in 0,23 s (lineare). Ogni numero con 11 o più cifre significative supera 2**31-1, quindi il troncamento è corretto. — ok
- `modules/web/lexbor.py:65` — video, audio, meter e progress aggiunti ai tag nascosti del figlio. Rischio esaminato: si nasconde testo che il browser mostra. Il browser non disegna mai il contenuto di riserva di video e audio né l'interno di meter e progress. Lo stesso insieme vale in `opzioni_visibili`, cosa innocua. Mutanti presi: tutti e quattro tolti (1 failed), solo video tolto (1), solo meter tolto (1). La lettura di sempre resta diversa ed è dichiarato. — ok
- `modules/web/lexbor.py:178` — ritorno anticipato di `attivo()` quando la sonda è già riuscita. Il test `tests/test_unit_web_lexbor.py:169` lo fissa tenendo il lock preso. Rischio esaminato: il test non prende il mutante, oppure lascia sporco lo stato globale. Col mutante che toglie il ritorno anticipato: 1 failed. `_FIGLIO_OK` è ripristinato dal monkeypatch del fixture `acceso` e il lock viene rilasciato nel `finally`. — ok
- `tests/test_unit_web_lexbor.py:162` — il test del size enorme chiama `testo_visibile` direttamente e controlla il valore esatto. Così non può passare grazie al ripiego, e la lezione della review #528 è applicata. Mutanti: senza tetto sulle cifre 2 failed, senza tetto 2**31 2 failed, tetto 2**40 2 failed, senza togliere il «+» 1 failed, zeri in testa contati 1 failed. — ok
- `tests/test_unit_web_lexbor.py:153` — tolta la soglia di 2 s, resta `is not None`. Rischio esaminato: il test non prende più la risalita quadratica. Ho riscritto io il mutante quadratico (`css("option")` più risalita agli antenati): 1 failed, perché supera TEMPO_MAX e il figlio restituisce None. — ok
- `modules/web/leggi.py:34` — la docstring ora descrive le sonde ripetute. Confrontata con MAX_SONDE=3 e RIPROVA_SONDA=600 di modules/web/lexbor.py: torna. — ok

**Riserve (entrambe COSMETICHE, da tracciare in stato_progetto)**
- R-531-1 (chat Mani): il mutante «tetto a 10 cifre» (`len(cifre) > 9`) SOPRAVVIVE con 60 passed. Con quel mutante `size=21474836470` verrebbe troncato a 2147483647 e letto come lista. Manca un caso parametrico a 11 cifre con le prime 10 sotto 2**31 (per esempio `size=21474836470` deve dare la tendina). Il codice di oggi è corretto: l'ho verificato con le prove sopra.
- R-531-2 (chat Mani): il commento in testa al codice del figlio (`modules/web/lexbor.py:52`) elenca ancora solo «datalist e rp» fra le cose che il browser non mostra. Video, audio, meter e progress sono spiegati solo accanto alla riga 65.

**Prove rifatte da me**
- Lexbor: 60 passed su 3.13 con selectolax 1.0.2; 3 passed e 57 skipped su 3.11 (senza selectolax).
- Test web (`-k web`): 502 passed, 1 skipped su 3.13. Il riepilogo diceva 501; la differenza è con ogni probabilità nel filtro `-k`.
- Wall of Shame: niente slicing della history, niente simulazione di tool, cap e `_get_window` non toccati, lettura con lexbor sempre spenta per default.

**Rischi esclusi (non verificati)**
- Il comportamento esatto di Chrome e Firefox al confine 2**31 (overflow uguale a valore non valido, quindi size di default) l'ho preso dalla conoscenza dei sorgenti di Blink, non l'ho verificato in un browser: qui non è riproducibile.
- La suite vecchia con GAS_WEB_LEXBOR=1 (11 failed, dichiarati uguali a prima) e il parser vecchio forzato (491/11) non li ho rifatti.
- Il caso dello shadow DOM dichiarativo resta aperto, come dichiarato.

**Memoria**
- Riga #531 (chat Mani) aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, insieme a una lezione nuova: un tetto sulla lunghezza delle cifre va provato col mutante «tetto meno uno».
- Committata da sola con lo script: commit 8a0d0d5. Lo stage non è stato toccato: restano i 3 file, 42 righe aggiunte e 11 tolte.

### Review #532 (chat Mani) — diff committato in c5b69f3

## VERDETTO: APPROVATO

Ri-review #532 (chat Mani): fetta 21 lexbor dopo la #531. Ho letto CLAUDE.md, stato_progetto e la mia memoria. Diff in stage: `git diff --cached`, 3 file, +47/-14.

Elementi del diff esaminati:
- `tests/test_unit_web_lexbor.py:99`: è il nuovo caso `<select size=21474836470>`, che deve dare la tendina (W1 visibile, W2 no). Rischio esaminato: il mutante «tetto meno uno» sopravviveva (R-531-1). Ho applicato il mutante `len(cifre) > 9` a `modules/web/lexbor.py:103`: 1 failed, 60 passed. Poi ho ripristinato il file (`git diff` non in stage è vuoto). Esito: ok, R-531-1 chiusa.
- `modules/web/lexbor.py:103`: `intero()` tiene al massimo 11 cifre significative, salta gli zeri in testa e accetta solo valori < 2**31. Rischio esaminato: le 11 cifre sono esattamente quelle che servono per distinguere 2147483647|0 dal massimo. Esito: ok.
- `modules/web/lexbor.py:52`: il commento in testa al figlio ora elenca anche video, audio, meter e progress, come l'insieme `nascosti` del figlio. Rischio esaminato: commento non allineato al codice (R-531-2). Le righe 48-55 sono tutte da 95 caratteri o meno. Esito: ok, R-531-2 chiusa.
- `modules/web/leggi.py:34`: la docstring dice che la sonda riparte «al più altre 2 volte a 600 s l'una dall'altra». Rischio esaminato: incoerenza con le costanti. Ho controllato con `modules/web/lexbor.py:38` (RIPROVA_SONDA=600.0) e `modules/web/lexbor.py:39` (MAX_SONDE=3, cioè la prima più altre 2). Esito: ok.

Prove che ho rifatto io:
- lexbor: 61 passed (Python 3.13);
- tutta la suite web: 502 passed, 1 skipped (3.13);
- mutante tetto-1: 1 failed, 60 passed.

Rischi esclusi:
- Non ho rifatto la suite su Python 3.11 (444/59 dichiarato dall'agente): selectolax c'è solo su 3.13, quindi su 3.11 i test lexbor sono quasi tutti skippati e non provano nulla di nuovo.
- Il comportamento sul VPS non è verificato: non è riproducibile in dev.
- Nota COSMETICA, non è una riserva: la riga `modules/web/lexbor.py:66` (insieme `nascosti` nel codice del figlio) è lunga 114 caratteri. Viene dalla fetta già vista nella #531.

Memoria: ho aggiunto la riga #532 (chat Mani) in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola con lo script (commit a2518f1). Lo stage non l'ho toccato: resta 3 file, +47/-14.

### Review #533 (chat Mani) — merge di origin/main 24ed87d in 7b6bc24

## VERDETTO: APPROVATO CON RISERVE

Review #533 (chat Mani). È il merge di origin/main 24ed87d (PR #279) in claude/peaceful-lovelace-0w2b7q (PR #280, HEAD ae588e6, base fb1f54b). Il merge è ancora in corso: MERGE_HEAD c'è e tutti i conflitti sono risolti.

Prima della review ho letto CLAUDE.md (sezioni 1, 5, 8, 10), la coda di `.claude/agents/memoria_revisore.md` e la riga «Ultimo aggiornamento» di `reports/stato_progetto.md`.

Elementi esaminati:
- `modules/web/lexbor.py:98` — intero(): legge l'attributo size con il tetto sulle cifre. Rischio: il merge poteva sovrascrivere il file con la versione di main. Esito: ok. Il blob nell'indice e nel working tree è uguale a quello di HEAD. Nessun file di modules/web/ cambia rispetto a HEAD, e i file di modules/web restano nel diff MERGE_HEAD --cached come diff della sessione.
- `tests/test_unit_web_lexbor.py:99` — il caso size=21474836470 → tendina (chiude R-531-1). Rischio: un test perso nel merge. Esito: ok. Il blob è uguale a HEAD e `pytest tests/test_unit_web_lexbor.py` dà 61 passed (Python 3.13).
- `tests/test_unit_web_lexbor.py:166` — test_size_enorme_non_fa_cadere_il_figlio: chiama testo_visibile direttamente. Rischio: un ritocco nella risoluzione del merge. Esito: ok, il file è invariato.
- `gas.py:4011` — _trova_contatto passa a leggi_contatti e restituisce la nota «NON letta» (arriva da main, già revisionato in #527/#528 chat Motore). Rischio: il kernel chiama un metodo assente sul branch. Esito: ok. `modules/memory/store.py:1225` definisce leggi_contatti, e il blob di gas.py è uguale a MERGE_HEAD (1bc0d5e). Anche tests/test_unit_kernel.py (c63b990) e CLAUDE.md (0c33fc1) sono uguali a MERGE_HEAD, sia nell'indice sia nel working tree.
- `.claude/agents/memoria_revisore.md` — risolto a mano. Rischio: righe di review perse o duplicate. Esito: ok. L'unione base/ours/theirs, contata riga per riga con le ripetizioni, coincide con lo stage: 0 righe perse, 0 in più.
- `reports/stato_progetto.md:4` — riga «Ultimo aggiornamento» unita a mano. Rischio: perdita di informazione. Esito: **riserva**. A parte questa riga, tutto il file coincide con l'unione. La riga è la voce Mani della fetta 21 seguita dalla riga intera di main. Il confronto carattere per carattere tra il resto della nostra riga e quella di main mostra una sola differenza: si perde «, PR #277 mergiata» nella voce della fetta 20.

Altri controlli:
- Marcatori di conflitto: 0 nei file in stage.
- Kernel: 1042 PASS, 1 FAIL rifatto da me. È T31g, che manca di sqlite_vec in questo ambiente: è già noto e non dipende dal merge.
- Nessun antipattern del Wall of Shame (slicing della history, simulazione dei tool) entra con questo merge: il codice motore che arriva da main è già stato revisionato.

Riserve:
- R-533-1 (chat Mani) COSMETICA: in `reports/stato_progetto.md:4` si perde l'annotazione «, PR #277 mergiata» della voce fetta 20 (resta la versione di main). Si corregge aggiungendo a mano quelle tre parole.

Cosa non ho verificato:
- Non ho rifatto la suite web completa (502/1): ho rifatto solo la suite lexbor. Tutti i file web sono byte per byte uguali a HEAD e nessun file di modules/web cambia da main, quindi il risultato non può cambiare.
- Non ho verificato la suite su Python 3.11.
- Non ho rifatto i mutanti sul codice di main, perché li hanno già provati le review #527/#528 (chat Motore).

Memoria:
- Ho aggiunto la riga «#533 (chat Mani) …» in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, solo nel working tree. Non l'ho messa in stage, non ho committato e non ho lanciato commit_memoria_revisore.sh, perché il merge è in corso. Lo stage non l'ho toccato: `git status` mostra «MM» solo su quel file.
- Nessuna lezione nuova.

### Review #534 (chat Mani) — diff committato in c23e6c6

## VERDETTO: APPROVATO

Review #534 (chat Mani). PR #280, branch claude/peaceful-lovelace-0w2b7q, HEAD 7b6bc24. Ho esaminato il diff in stage (`git diff --cached`), cioè solo tests/test_unit_web_lexbor.py (+3/-1).

Prima della review ho letto: CLAUDE.md (sez. 5, 8, 10), reports/stato_progetto.md (riga 4 e voci fetta 19-21 di Mani) e la coda di .claude/agents/memoria_revisore.md, con le lezioni #531 sul mutante tetto-1 e #528 sui test diretti.

**Elementi esaminati**
- tests/test_unit_web_lexbor.py:100 — nuovo caso `size=2147483647`, il più grande valore ammesso: si aspetta la lista, con W1 e W2 visibili — rischio: il confine di 2**31 non fissato (V-2 della verifica esterna #280) — ok. Il mutante `<= 1 << 31` → 1 failed, 62 passed.
- tests/test_unit_web_lexbor.py:101 — nuovo caso `size=2147483648`, il primo valore non ammesso: si aspetta la tendina, con W2 nascosto — rischio: un confine spostato in su o in giù resta verde — ok. Ho rifatto io i mutanti su modules/web/lexbor.py:106. `< (1 << 31) - 1` → 1 failed, 62 passed. Ne ho aggiunto un terzo, `< 1 << 32` → 1 failed, 62 passed. Dopo ogni mutante ho ripristinato lexbor.py con `git checkout`: il working tree è pulito e lo stage è intatto.
- modules/web/lexbor.py:98 — contesto, file non toccato dal diff: `intero()` accetta al massimo 11 cifre significative e scarta gli zeri in testa. I due casi nuovi hanno 10 cifre, quindi provano solo il confronto col massimo e non il tetto sulle cifre, già fissato dal caso alla riga 99 — ok.
- tests/test_unit_web_lexbor.py:1 — la docstring passa da «in prova» a «spenta per default, fette 19-21» — rischio: doc non allineata al codice (V-2 del bot #280, cosmetica) — ok. È coerente con modules/web/lexbor.py:177, dove la lettura con lexbor si accende solo con `GAS_WEB_LEXBOR == "1"`.
- Antipattern della sez. 5 di CLAUDE.md (slicing della history, output dei tool simulati) e guardrail (cap 10 iterazioni, `_get_window`): non toccati dal diff, che modifica solo dati di test — ok.

**Prove rifatte (Python 3.13.16, selectolax 1.0.2)**
- Test lexbor: 63 passed.
- Suite web (`tests/test_unit_web*.py`): 504 passed, 1 skipped, come dichiarato. Con `-k web` su tutta la cartella i test diventano 505: il conteggio dipende solo dal comando, non è una discrepanza.

**Rischio escluso**
Non ho girato i test su Python 3.11 senza selectolax, cioè la configurazione della CI. Lì il test parametrico si salta perché richiede la libreria. I due casi nuovi sono righe di dati dello stesso test, quindi non cambiano la parte di suite che gira lì: lo dimostrerà la CI della PR.

**Riserve:** nessuna.

**Memoria:** ho aggiunto la riga #534 (chat Mani) a /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola con `scripts/commit_memoria_revisore.sh` (commit e0521bd). Nessuna lezione nuova. Lo stage non è stato toccato: dentro c'è ancora solo tests/test_unit_web_lexbor.py.

### Review #535 (chat Mani) — merge di origin/main 52fc615 in 465ba13

## VERDETTO: APPROVATO CON RISERVE

Review #535 (chat Mani): merge di origin/main 52fc615 (PR #281, chat Notte) in claude/peaceful-lovelace-0w2b7q (PR #280, HEAD d78843f, base 24ed87d), con MERGE_HEAD presente.

Letture fatte: CLAUDE.md (sez. 5, 8, 10), stato_progetto (riga 4 e le zone della fusione), coda di memoria_revisore.md (#526–#534 delle tre chat, lezioni 2026-10-27 e 2026-10-28).

**Elementi del diff esaminati**
- `modules/web/lexbor.py:107` — `intero()` con il tetto `< 1 << 31` (fetta 21, resta nel diff di sessione). Rischio: che la risoluzione del merge abbia preso la versione di main e annullato la fetta. Indice, working tree e HEAD hanno lo stesso blob; nessuna differenza da HEAD su `modules/web/` (anche `modules/web/leggi.py`). Esito: ok.
- `tests/test_unit_web_lexbor.py:100` — caso limite `size=2147483647` → lista (con `tests/test_unit_web_lexbor.py:101` → tendina). Rischio: test web persi o regrediti nel merge. Il blob è identico a HEAD; la suite web dà 504 passed e 1 skipped (rifatta da me). Esito: ok.
- `gas.py:3542` — recupero del segno «esito in storia» (fetta di main, già revisionata in #531/#532 chat Notte). Rischio: un'unione a mano che mescola le due versioni. Il blob di gas.py è uguale a MERGE_HEAD in indice e working tree, e lo stesso vale per `modules/memory/store.py` e `tests/test_unit_kernel.py`. Il kernel dà 1052 PASS e 1 FAIL (rifatto da me). L'unico FAIL è T31g, ambientale: ho verificato che `import sqlite_vec` dà ModuleNotFoundError. Esito: ok.
- `reports/stato_progetto.md:4` — la riga «Ultimo aggiornamento» unita a mano. Rischio: voci perse. Ho confrontato il file con `git merge-file` (base/ours/theirs): l'unica differenza è la riga 4. Questa riga è la voce fetta 21 di HEAD più la riga intera di main; la voce fetta 20 ha di nuovo «, PR #277 mergiata», quindi R-533-1 è chiusa. Nessuna voce di HEAD manca. Esito: riserva cosmetica (sotto).
- `.claude/agents/memoria_revisore.md` — unione delle righe dei due lati. Rischio: righe perse o duplicate. Il confronto a multinsieme (righe contate con le ripetizioni) dà: atteso = ours + (theirs − base), contro l'indice 0 perse e 0 in più; la base non ha righe tolte da nessuno dei due lati. Esito: ok.
- Altri controlli:
  - `reports/handoff.md`, `reports/ultimo_report.md`, `reports/diff_sessione.md` e `reports/ripartenza_mani.md` sono uguali a HEAD.
  - `reports/coda_notte.md` e `reports/report_notte.md` sono uguali a MERGE_HEAD.
  - Nessun marcatore di conflitto, nessun file non risolto (`ls-files -u` vuoto), `diff --cached --check` pulito.
  - Nessuno slicing della history e nessuna simulazione di tool introdotti: il codice del motore entrato è byte per byte quello di main.

**Riserve**
- R-535-1 (chat Mani), COSMETICA: in `reports/stato_progetto.md:4` la voce in testa «Ultimo aggiornamento: **2026-10-27**» è seguita da «prima: **2026-10-28**», quindi le date sono in ordine inverso. Basta mettere la data 2026-10-28 sulla voce fetta 21 quando aggiorni lo stato a fine task, oppure accettare l'ordine. Va tracciata in stato_progetto come le altre riserve.

**Rischi esplicitamente esclusi**
- Non ho rifatto la review del contenuto della fetta di main (segno DB, T78r–T78u): è coperta da #531/#532 (chat Notte). Ho verificato solo che i blob siano identici e che la suite passi.
- Non ho eseguito T31g con sqlite_vec installato, perché il modulo manca in questo ambiente.
- Non ho controllato CI e VPS: il merge non è ancora committato.

**Memoria**
- La riga `#535 (chat Mani) — 2026-10-28 — APPROVATO CON RISERVE — …` è in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree (stato `MM`).
- Come richiesto, non l'ho messa in stage, non l'ho committata e non ho lanciato `commit_memoria_revisore.sh`.
- Non ho toccato lo stage: `git diff` mostra solo quella riga in più.
- Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati dalla sessione), codice c5b69f3 e poi c23e6c6:
- `python3 -m pytest -q tests/test_unit_web_*.py`: main fb1f54b `494 passed, 1 skipped` → ramo `502 passed, 1 skipped in 33.43s` (3.13.16, con selectolax); `444 passed, 59 skipped in 26.07s` (3.11 locale, senza selectolax). `tests/test_unit_web_lexbor.py` da 53 a 61 test (`61 passed in 6.71s`). Su 3.11 nella CI (run 40536717337, job unit-suite): 445 passed / 58 skipped (scarto di ambiente col locale).
- Dopo c23e6c6: `63 passed in 6.99s` (lexbor), web suite `504 passed, 1 skipped in 32.80s`. Dopo il merge 7b6bc24: `python3 tests/test_unit_kernel.py` → `=== RIEPILOGO: 1042 PASS, 1 FAIL ===`; dopo il merge 465ba13: `=== RIEPILOGO: 1052 PASS, 1 FAIL ===` e web `504 passed, 1 skipped in 34.55s` (`FAIL: T31g gate env GAS_VECTORS=1 costruisce il vector store`: sqlite_vec assente nell'ambiente, fallisce identico su main pulito, fuori scope).
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin), prima dell'ultimo caso a 11 cifre: `491 passed, 11 skipped in 31.16s`.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (test lexbor esclusi): `11 failed, 430 passed, 1 skipped, 60 deselected in 43.49s` su c5b69f3 prima dell'ultimo caso (gli stessi 11 di prima; con i 61 test lexbor i deselezionati sono 61, come misurato dalla verifica esterna).
- Mutanti (uscita di pytest sui test lexbor): senza tetto alle cifre `2 failed, 58 passed`; senza tetto 2**31 `2 failed, 58 passed`; senza removeprefix `1 failed, 59 passed`; zeri in testa contati `1 failed, 59 passed`; hidden=false visibile `1 failed, 59 passed`; senza ritorno anticipato in attivo() `1 failed, 59 passed`; video/audio/meter/progress visibili `1 failed, 59 passed`; risalita quadratica `1 failed, 59 passed`; tetto meno uno (dopo R-531-1) `1 failed, 60 passed`; confine `<= 1 << 31` `1 failed, 62 passed`; confine `< (1 << 31) - 1` `1 failed, 62 passed`.

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, workflow ci.yml, branch claude/peaceful-lovelace-0w2b7q, evento push). Istantanea al momento della scrittura: lo stato aggiornato è sulla PR.

```
40539680295  CI  push  completed  success  d78843f  2026-10-27T16:18:54Z
40536997549  CI  push  completed  success  ae588e6  2026-10-27T16:02:40Z
40536717337  CI  push  completed  failure  c5b69f3  2026-10-27T16:00:58Z
```

Mappatura commit→run:
- `8a0d0d5`, `a2518f1`: nessuna run su questo SHA (pushati insieme a `c5b69f3`).
- `c5b69f3` → run 40536717337, failure: solo handoff-check (l'handoff arriva col commit dopo); unit-suite verde.
- `ae588e6` → run 40536997549, success.
- `7b6bc24`, `e0521bd`, `c23e6c6`: nessuna run su questo SHA (pushati insieme a `d78843f`).
- `d78843f` → run 40539680295, success.
- `465ba13`: nessuna run su questo SHA (pushato insieme a `fe8992f`).
- `fe8992f` → run 40679080827 (unit-suite e handoff-check); verifica-bot failure per V-1 (conflitto con main).
- `1cfc9ab`: nessuna run su questo SHA (pushato insieme al commit di fine-task).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Shadow DOM dichiarativo (figli «light» di un host con `<template shadowrootmode>`): decisione dell'operatore.
- R-ve277-3 COSMETICA (con R-529-1): opzione dentro un sotto-albero `hidden` o un `optgroup disabled` nella scelta automatica.
- R-ve277-4 COSMETICA: fuori da Linux 3 sonde prima di spegnere (`sys.platform` in `attivo()`).
- R-528-3, R-526-1, R-520-4 COSMETICHE.
- Bot V-1 #277 / V-3 ve #280 / R-ve280-1: test del figlio saltati in CI finché selectolax non è in requirements-dev (chat Motore).
- DA SISTEMARE (operatore, 2026-10-28): R-ve280-2 e R-ve280-3 (numeri dell'handoff), R-bot280-1 (`intero("0")` dà None), R-bot280-2 (riga ripetuta in §7, unita in questo giro).
- Nota cosmetica del revisore #532 (non riserva): la riga dell'insieme `nascosti` del figlio è lunga 114 caratteri.
- Restano decisioni dell'operatore: R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s.
