# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani, fetta 27: selectolax in requirements, i test lexbor girano in CI (R-ve280-1, chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #303 (https://github.com/Gasss23/Gas/pull/303). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5073049841","url":"https://github.com/Gasss23/Gas/pull/303"}`), perché `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore, che può arrivare anche tramite M1.
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
- **Bot su 39f6770 (PR #303)**: APPROVATO CON RISERVE, check verifica-bot success. V-1 BASSA (frase di §5 annidata in sé stessa dalla correzione precedente): `FATTA` — riscritta. V-2 COSMETICA (CI su 39f6770 non finita alla verifica): `FATTA` — §6.
- **Bot su 4e0d1ac (PR #303)**: APPROVATO CON RISERVE, check verifica-bot success. V-1 BASSA (suite web locale «620 passed, 1 skipped»: era la misura di prima del test nuovo): `FATTA` — rimisurata, 620 passed e 2 skipped.
- **Verifica esterna su 67fea3d (https://github.com/Gasss23/Gas/pull/303#issuecomment-6504641961)**: APPROVATO CON RISERVE. V-1 BASSA (la riserva «Mac Intel senza wheel» della review #564 è falsa): `FATTA` — tolta da §7 e corretta in stato_progetto. V-2 BASSA (controllo sul VPS incompleto): `FATTA` — §0 punto 3 e descrizione della PR. V-3 BASSA (selectolax 1.0.2 uscita il 2026-10-22): `DEFERITA — decide l'operatore` (§0 punto 4). V-4 COSMETICA: `SALTATA — nessuna azione`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 reports/diff_sessione.md           | 11 +++++++----
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |  5 +++--
 reports/stato_progetto.md          |  3 ++-
 reports/ultimo_report.md           | 40 ++++++++++++++++++++--------------------
 requirements.txt                   |  2 ++
 tests/test_unit_web_lexbor.py      | 10 +++++++++-
```

NB: base = merge-base con origin/main = acd083f. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. In tests/ un test nuovo, `test_selectolax_in_ci`, che si salta fuori dalla CI. Locale (Python 3.13, con selectolax): suite completa `2450 passed, 2 skipped in 249.15s`; `tests/test_unit_web_*.py` `620 passed, 2 skipped` (rimisurata dopo il test nuovo, V-1 bot #303 su 4e0d1ac: prima c'era «620 passed, 1 skipped», misura presa prima del test nuovo); `CI=1 pytest tests/test_unit_web_lexbor.py` `135 passed`. In CI (run 40926576413 su 67fea3d) web `622 passed`, 0 skipped. Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 7c39b82: nessuna run su questo SHA (pushato insieme a 57167e5).
- 57167e5: run CI 40926263056. `handoff-check` failure (atteso: l'handoff era ancora quello della PR #301, riscritto in questo commit di fine-task); `unit-suite` in corso alla scrittura dell'handoff. Run 40926358823 del bot: skipped (manca ancora l'etichetta `verifica`).
- 67fea3d (fine-task): run CI 40926576413, `handoff-check` e `unit-suite` success; suite web 622 passed, 0 skipped, `test_selectolax_in_ci` PASSED (letto dalla verifica esterna e dal bot nel log della run). Check `verifica-bot` success, review del bot APPROVATO CON RISERVE (vedi §1).
- 4e0d1ac (fine-task): run CI 40928379166; check `verifica-bot` success, review del bot APPROVATO CON RISERVE (vedi §1). `handoff-check` e `unit-suite` success.
- 39f6770 (fine-task): run CI 40929013013, `handoff-check` success, `unit-suite` in corso alla scrittura dell'handoff (da rileggere prima del merge). Run del bot 40929017955: check `verifica-bot` success, review APPROVATO CON RISERVE (vedi §1).
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
