# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani, fetta 27: selectolax in requirements, i test lexbor girano in CI (R-ve280-1, chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #303 (https://github.com/Gasss23/Gas/pull/303). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5073049841","url":"https://github.com/Gasss23/Gas/pull/303"}`), perché `gh` nel cloud non è autenticato. Con le riserve il merge lo decide l'operatore: secondo M1 l'operatore ha detto «mergia #303» nella chat di M1, e lo fa M1 a CI verde (la chat Mani non mergia su un sì che non può verificare).
2. Confermare che il coordinamento delle chat è passato a M1 (sessione «Co-Work») e che la chat Mani prende (a) e (c). L'incarico è arrivato con un messaggio da un'altra sessione, non dall'operatore.
3. Prima del `pip install -r requirements.txt` sul VPS controllare che `GAS_WEB_LEXBOR` non arrivi già da nessuna parte: `grep GAS_WEB_LEXBOR .env`, `grep -r GAS_WEB_LEXBOR /etc 2>/dev/null`, `systemctl show <unità di Gas> -p Environment` e il profilo della shell (V-2 ve #303). Se c'è, lexbor si accende subito.
4. V-3 ve #303 BASSA: selectolax 1.0.2 è uscita il 2026-10-22 (serie 1.0 giovane). Decidere se accettarla o aspettare qualche settimana prima del `pip install` sul VPS.

---

## §1 SCOPE & ESITO FETTE

- **Le 2 decisioni chieste da M1 (tempo di rete 12 s, R-ve235-7)**: `SALTATA — già prese dall'operatore il 2026-10-29 e mergiate con la PR #301`; M1 ha confermato.
- **(a) R-ve280-1, selectolax in requirements**: `FATTA` — `selectolax==1.0.2` in `requirements.txt`, allarme in CI `test_selectolax_in_ci`. Lexbor resta SPENTA. Review #564 (chat Mani) APPROVATO.
- **(c) `scripts/bot_esito.py` e i caratteri Cf**: `DEFERITA — una PR per voce sul mio unico branch: parte dopo il merge della #303`. Causa trovata su #297 (0d45b8b): il verdetto del bot citava «/forte@GasBot» + U+200B.
- **(b) libexpat ≥ 2.4 nel doctor (gas.py)**: `DEFERITA — M1 la tiene finché il suo ponte voce, che tocca gas.py, non è mergiato`.
- **Ripartenza e stato**: `FATTA`.
- **Bot su 67fea3d (PR #303)**: APPROVATO CON RISERVE, check verifica-bot success. V-1 BASSA (la prova della CI mancava nei report): `FATTA` — run 40926576413, web 622 passed e 0 skipped, scritta in §6, stato_progetto e ripartenza. V-2 COSMETICA (l'allarme scatta con qualunque valore di CI): `SALTATA — accettata, stesso schema di test_parser_aggiornato_rilevato`.
- **Verifica esterna su 67fea3d (https://github.com/Gasss23/Gas/pull/303#issuecomment-6504641961)**: APPROVATO CON RISERVE. V-1 BASSA (la riserva «Mac Intel senza wheel» della review #564 è falsa): `FATTA` — tolta da §7 e corretta in stato_progetto. V-2 BASSA (controllo sul VPS incompleto): `FATTA` — §0 punto 3 e descrizione della PR. V-3 BASSA (selectolax 1.0.2 uscita il 2026-10-22): `DEFERITA — decide l'operatore` (§0 punto 4). V-4 COSMETICA: `SALTATA — nessuna azione`.
- **Bot su 4e0d1ac (PR #303)**: APPROVATO CON RISERVE, check verifica-bot success. V-1 BASSA (suite web locale «620 passed, 1 skipped»: era la misura di prima del test nuovo): `FATTA` — rimisurata, 620 passed e 2 skipped.
- **Bot su 39f6770 (PR #303)**: APPROVATO CON RISERVE, check verifica-bot success. V-1 BASSA (frase di §5 annidata in sé stessa dalla correzione precedente): `FATTA` — riscritta. V-2 COSMETICA (CI su 39f6770 non finita alla verifica): `FATTA` — §6.
- **Bot su 6a56390 (PR #303)**: APPROVATO CON RISERVE, check verifica-bot success. V-1 COSMETICA (§6, riga di 39f6770 ancora «in corso»): `FATTA` — aggiornata. V-2 COSMETICA (voci del bot fuori ordine, «L'ho detto»): `FATTA` — riordinate e corrette.
- **Merge di origin/main 97776f0 (PR #304 di M2, voce)**: `FATTA` — la #303 era in conflitto (solo report). Tenuti i miei handoff, ultimo_report e diff_sessione; memoria del revisore con le righe di tutti e due i lati; stato_progetto e roadmap uniti in automatico. Review #568 (chat Mani) APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 reports/diff_sessione.md           |  14 +++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   5 +++--
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  40 ++++++++++++++++++++++------------------
 requirements.txt                   |   2 ++
 tests/test_unit_web_lexbor.py      |  10 +++++++++-
```

NB: base = merge-base con origin/main = 97776f0 (PR #304 di M2, dopo il merge di main). Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
9e85c4f Merge origin/main (97776f0, PR #304 di M2) in claude/peaceful-lovelace-0w2b7q (PR #303)
6a56390 docs(fine-task): PR #303, frase di §5 riscritta e CI di 39f6770 (note del bot su 39f6770)
39f6770 docs(fine-task): PR #303, conteggio locale della suite web rimisurato (V-1 bot su 4e0d1ac)
4e0d1ac docs(fine-task): PR #303, note del bot e della verifica esterna su 67fea3d
67fea3d docs(fine-task): Mani fetta 27, selectolax in requirements (PR #303), lavoro passato da M1
57167e5 build(web): selectolax==1.0.2 in requirements, i test lexbor girano in CI (R-ve280-1, chat Mani)
7c39b82 chore(revisore): memoria review #564 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 57167e5 (requirements.txt, tests/test_unit_web_lexbor.py). Verdetto integrale della review #564 (chat Mani):

```
## VERDETTO: APPROVATO

Review #564 (chat Mani). Ho controllato il diff staged (sha256 9fb84387…) su una copia dell'index (`git checkout-index`), senza toccare la tua cartella di lavoro. L'index è rimasto com'era: 2 file, +11/−1.

Letture fatte prima della review: CLAUDE.md (sez. 1, 5, 8, 10), reports/stato_progetto.md (letto per parti: fette lexbor 19-26, hardware del VPS, setup dei Mac) e la memoria del revisore (lezioni su selectolax, export dell'index).

Elementi del diff esaminati:

1. `requirements.txt:9` — aggiunge `selectolax==1.0.2` alle dipendenze di deploy del VPS.
   - Rischio esaminato: la catena di fornitura (dipendenza nativa nuova, dipendenze indirette, wheel mancanti che costringerebbero a compilare dal sorgente).
   - Il pin è esatto. `pip show` riporta `Requires:` vuoto, quindi selectolax non porta dentro altre librerie.
   - `pip download --only-binary=:all:` trova le wheel per cp311, cp312 e cp314 manylinux x86_64 (CI e VPS CX33 x86_64), cp313 aarch64, cp314 mac arm64 e cp312 win_amd64.
   - Installare una wheel non esegue codice.
   - Hai fatto bene a non metterlo anche in requirements-dev.txt: la CI installa entrambi i file (`.github/workflows/ci.yml:52`).
   - Esito: ok.

2. `modules/web/lexbor.py:319` (contesto, file non toccato) — `attivo()` controlla `_DISPONIBILE`, Linux e `GAS_WEB_LEXBOR == "1"`.
   - Rischio esaminato: che lexbor si accenda da sola sul VPS ora che selectolax è installato.
   - Provato su Python 3.11 con la wheel installata:
     - senza `GAS_WEB_LEXBOR`, `attivo()` dà False, nessuna sonda parte e `_FIGLIO_OK` resta None;
     - con «0» dà False;
     - con « 1 » (spazi intorno) dà True: comportamento già esistente e voluto.
   - Il processo di Gas non carica mai la libreria nativa. Fa solo `find_spec` (`modules/web/lexbor.py:37`) e l'import vero sta nel figlio (`modules/web/lexbor.py:67`), con limite di memoria e `-I`.
   - Il punto di chiamata, `modules/web/leggi.py:1582`, è ancora protetto da `attivo()`.
   - Esito: ok.

3. `tests/test_unit_web_lexbor.py:17` — `test_selectolax_in_ci`: si salta fuori dalla CI e in CI fallisce se selectolax manca. Segue lo stesso schema di `tests/test_unit_web_leggi.py:1281`.
   - Rischio esaminato: un allarme che non scatta mai.
   - Prova del guasto: venv 3.11 senza selectolax con `CI=true` → 1 failed (`assert False`, `lexbor._DISPONIBILE`), 22 passed, 112 skipped.
   - Lo step web della CI (`.github/workflows/ci.yml:118`) non ridefinisce l'ambiente, quindi la variabile CI di GitHub Actions arriva al test.
   - Esito: ok.

4. Test che davano per scontata l'assenza di selectolax: nessuno.
   - Nei test, `GAS_WEB_LEXBOR` compare solo in `tests/test_unit_web_lexbor.py`, sempre tramite monkeypatch.
   - `tests/test_unit_web_lexbor.py:477` forza `_DISPONIBILE=False` di proposito.
   - Il kernel e il doctor non nominano selectolax.
   - Risultati:
     - venv 3.11 con la wheel e `CI=true`: `tests/test_unit_web_*.py` → 622 passed, cioè anche i due allarmi girano e passano;
     - 3.13 in locale: test_unit_web_lexbor.py → 134 passed, 1 skipped senza CI e 135 passed con `CI=true`.
   - Esito: ok.

Coerenza col progetto: rispetta "robustezza > potenza". La funzione resta spenta per default e, se selectolax mancasse, Gas usa la lettura di sempre senza crash. Non tocca `_get_window`, il tetto di 10 iterazioni, il tetto di 8k sull'output né i provider. Nessuno slicing della history e nessun output dei tool simulato.

Rischi esplicitamente esclusi:
- **VPS non verificato**: non lo raggiungo da qui. Non so se il `.env` del VPS contiene già `GAS_WEB_LEXBOR=1`: se sì, dopo il `pip install` lexbor si accenderebbe. Basta controllarlo con un `grep GAS_WEB_LEXBOR` sul `.env` del VPS. Il `pip install -r requirements.txt` sul VPS resta un passo manuale dell'operatore.
- **Mac Intel**: per macosx_10_13_x86_64 con Python 3.14 pip non ha trovato wheel, quindi un Mac Intel dovrebbe compilare dal sorgente. Non l'ho approfondito: il Mac dell'operatore usa Homebrew con Python 3.14 e quasi certamente è arm64, dove la wheel c'è (non confermato in sessione).
- **Hash della wheel**: non l'ho verificato a mano (gli altri pin non hanno hash; pip controlla quello che pubblica l'indice).

## Memoria del revisore
Riga #564 scritta in `/home/user/Gas/.claude/agents/memoria_revisore.md`, più una lezione: per una dipendenza nativa nuova si controllano `find_spec` nel processo principale, `pip show` per le dipendenze indirette e `pip download --platform` per le wheel. Committata con `scripts/commit_memoria_revisore.sh` (commit 7c39b82, solo quel file).
```

Commit 9e85c4f (merge di origin/main 97776f0: da main entrano modules/voice/server.py, tests/test_unit_voice_server.py e tests/test_unit_voice_stt.py). Verdetto integrale della review #568 (chat Mani):

```
## VERDETTO: APPROVATO

Review #568 (chat Mani): il merge di origin/main 97776f0 (PR #304 di M2, voce) nel branch claude/peaceful-lovelace-0w2b7q (PR #303, HEAD 6a56390, base comune acd083f). Ho fatto le prove su un export dell'index (`git checkout-index`), non sulla cartella di lavoro.

Prima ho letto CLAUDE.md (sezione 5), reports/stato_progetto.md (solo le parti che servivano) e la coda di .claude/agents/memoria_revisore.md.

Elementi del diff esaminati:
- `modules/voice/server.py:77` — la regex `_PAROLA_FORTE` della voce forte, che entra da main. Rischio: che il merge l'abbia alterata rispetto a quanto revisionato da M2 (#564-M2…#567-M2). `git diff origin/main --cached` su questo file è vuoto, quindi il file è identico a main. Esito: ok.
- `modules/voice/server.py:318` — `_carica_env()` chiamato da `run_server` prima che venga letto GAS_VOICE_TOKEN (V-1 bot #304). Rischio: un hunk perso o duplicato nell'auto-merge. Il file è identico a main. Esito: ok.
- `tests/test_unit_voice_server.py:86` — `monkeypatch.setattr(sys, "path", …)`; lo stesso c'è anche a `tests/test_unit_voice_server.py:528` e `tests/test_unit_voice_server.py:550`. Rischio: che l'isolamento di #567-M2 sia stato perso. Il file è identico a main, e lo è anche `tests/test_unit_voice_stt.py:1`. Esito: ok.
- `requirements.txt:9` — `selectolax==1.0.2`, mia modifica (#564 chat Mani). Rischio: che il merge l'abbia toccata. Verso HEAD il diff è vuoto, così come per `tests/test_unit_web_lexbor.py:17` (l'allarme in CI). Esito: ok.
- `reports/stato_progetto.md:4` — la riga «Ultimo aggiornamento», unico punto in cui l'auto-merge ha dovuto unire i due lati. Rischio: perdere la cronologia di main. Questa riga è uguale a quella di HEAD e contiene per intero la riga 4 di main. La voce «Voce V1» di M2 e il punto 13 corretto («python -m modules.voice.server») ci sono. Esito: ok.
- `.claude/agents/memoria_revisore.md:991` — conflitto risolto a mano: prima la #564 della chat Mani e la sua lezione, poi #564-M2…#567-M2. Rischio: perdere una riga. Verso main e verso HEAD il diff ha zero righe tolte. Esito: ok.

Controlli strutturali:
- I file cambiati dall'una e dall'altra parte tornano. Il risultato differisce da main solo nei file cambiati da HEAD (memoria, diff_sessione, handoff, ripartenza_mani, stato_progetto, ultimo_report, requirements.txt, test_unit_web_lexbor.py). Differisce da HEAD solo nei file cambiati da main (memoria, modules/voice/server.py, roadmap, stato_progetto, i due test della voce). Quindi nessun file è stato perso o alterato da nessuno dei due lati.
- handoff.md, ultimo_report.md, diff_sessione.md e ripartenza_mani.md sono identici a HEAD, come da regola della chat Mani.
- Nella roadmap ci sono solo le aggiunte di main (riga R8 corretta e voce «Cervello forte dalla voce»), nessuna riga tolta.
- Nessun marcatore di conflitto, 0 caratteri Cf nel diff, nessuno slicing della history, nessun output di tool simulato.
- Test sull'export: voice_server + voice_stt + web_lexbor + dotenv, 240 passed e 1 skipped. Con l'insieme diverso dal mio, il tuo conteggio di 247/1 è compatibile.

Rischio escluso: non ho rifatto i mutanti sul codice della voce. Il contenuto è byte per byte uguale a quello già revisionato e mergiato da M2 (#564-M2…#567-M2), e questa review riguarda solo il merge. Non ho fatto girare nemmeno la suite completa, perché il diff verso HEAD tocca solo voce e report. Il comportamento reale del server voce sul Mac o sulla VPS non è verificato: non si può riprodurre qui.

Memoria del revisore: ho aggiunto la riga #568 in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, ma non l'ho committata. L'hook review_gate ha bloccato il comando con `scripts/commit_memoria_revisore.sh`, perché `.claude/.review_ok` non corrisponde al diff staged. In ogni caso durante un merge `git commit -o` non è possibile.

Cosa devi fare:
1. `git add .claude/agents/memoria_revisore.md`, così la riga #568 entra nel merge.
2. `bash scripts/segna_review_ok.sh` DOPO quell'add, altrimenti il marcatore non corrisponde al diff staged.
3. Concludi il merge con `git commit`.

Lezioni nuove: nessuna.
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. Dal merge di main entrano i test della voce di M2, invariati (review #568: voice + lexbor 247 passed, 1 skipped in locale). In tests/ un test nuovo, `test_selectolax_in_ci`, che si salta fuori dalla CI. Locale (Python 3.13, con selectolax): suite completa `2450 passed, 2 skipped in 249.15s`; `tests/test_unit_web_*.py` `620 passed, 2 skipped` (rimisurata dopo il test nuovo, V-1 bot #303 su 4e0d1ac: prima c'era «620 passed, 1 skipped», misura presa prima del test nuovo); `CI=1 pytest tests/test_unit_web_lexbor.py` `135 passed`. In CI (run 40926576413 su 67fea3d) web `622 passed`, 0 skipped. Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 7c39b82: nessuna run su questo SHA (pushato insieme a 57167e5).
- 57167e5: run CI 40926263056. `handoff-check` failure (atteso: l'handoff era ancora quello della PR #301, riscritto in questo commit di fine-task); `unit-suite` in corso alla scrittura dell'handoff. Run 40926358823 del bot: skipped (manca ancora l'etichetta `verifica`).
- 67fea3d (fine-task): run CI 40926576413, `handoff-check` e `unit-suite` success; suite web 622 passed, 0 skipped, `test_selectolax_in_ci` PASSED (letto dalla verifica esterna e dal bot nel log della run). Check `verifica-bot` success, review del bot APPROVATO CON RISERVE (vedi §1).
- 4e0d1ac (fine-task): run CI 40928379166; check `verifica-bot` success, review del bot APPROVATO CON RISERVE (vedi §1). `handoff-check` e `unit-suite` success.
- 39f6770 (fine-task): run CI 40929013013, `handoff-check` e `unit-suite` success. Run del bot 40929017955: check `verifica-bot` success, review APPROVATO CON RISERVE (vedi §1).
- 6a56390 (fine-task): CI verde (check suite completata senza fallimenti); check `verifica-bot` success, review APPROVATO CON RISERVE con 2 COSMETICHE (vedi §1).
- 9e85c4f (merge di origin/main 97776f0): nessuna run su questo SHA (pushato insieme al commit di fine-task che contiene questo file).
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Rischio escluso dalla review #564, allargato da V-2 ve #303: `GAS_WEB_LEXBOR` già nell'ambiente del VPS (`.env`, systemd, /etc, shell): da controllare prima del `pip install`. La riserva «Mac Intel senza wheel» era falsa (V-1 ve #303).
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore.
- V-2 bot / V-4 ve #303 COSMETICHE accettate: l'allarme scatta con qualunque valore di CI e controlla l'installazione, non l'import.
- (c) `scripts/bot_esito.py` boccia ogni carattere Cf, anche quando il bot cita un caso di prova (failure definitivo su #297, 0d45b8b): dopo la #303.
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- R-518-1 (chat Mani) BASSA: guardia `_nascosti_html` nelle chiusure in scope; per canvas fa perdere testo che il browser mostra (da decidere con l'oracolo).
- R-516-1 (chat Mani) BASSA: titolo perso sulle pagine a frame (verso sicuro).
- R-ve277-5 BASSA PREESISTENTE, parte leggi.py: con la lettura di sempre escono riserva di video/audio, testo di meter/progress, figli «light» di un host shadow.
- V-1 ve/bot #288 BASSA: adoption agency che sposta il template dichiarativo (dichiarata in `shadow()`).
- V-2 BASSA della verifica esterna #296 su 336e67c (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485248441), scelta: entità non dichiarata con DOCTYPE esterno non XHTML, Gas taglia come Firefox.
- V-3 BASSA della verifica esterna #296 su 06bc98e (https://github.com/Gasss23/Gas/pull/296#issuecomment-6498712956), scelta: entità HTML5 fuori dal DTD XHTML 1.0 accettate, come whatwg.
- R-546-1 BASSA: numeri delle review doppi tra le chat.
