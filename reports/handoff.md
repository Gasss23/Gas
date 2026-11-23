# HANDOFF — Dossier di fine sessione

**Sessione:** 23 novembre 2026 — R7 fetta 2: ripresa al boot del compito in sottofondo (sotto-chat di M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #398 (https://github.com/Gasss23/Gas/pull/398), etichetta «verifica». Tocca il motore: merge autonomo solo con verdetto testuale del bot APPROVATO senza finding V-x, CI verde e niente conflitti; altrimenti decide l'operatore.
2. (Facoltativo) Installare sul Mac `scripts/sottofondo/com.gas.sottofondo.plist` (istruzioni nel commento del file; serve `~/Gas/.venv`).

Numero e URL della PR presi dall'output di `gh api repos/Gasss23/Gas/pulls` (POST, creazione): `398`, `https://github.com/Gasss23/Gas/pull/398` (`gh pr` non disponibile in questo ambiente, solo REST).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 2 R7 — ripresa al boot**: FATTA. `riprendi_al_boot` (riusa `controlla`, stessi guardrail della fetta 1, nel terminale solo id e stato), comando `python gas.py sottofondo-riprendi`, plist launchd solo RunAtLoad che pretende `~/Gas/.venv`, `scripts/sottofondo/` nel perimetro, 8 test nuovi. Review #839 → correzioni R-839-1/R-839-2 → review #840.
- **Fetta 3 R7 — lista dei lavori ricorrenti con stato**: DEFERITA — prossima PR (una fetta per PR).
- **Fetta 4 R7 — tetti di tempo duri**: DEFERITA — dopo la 3.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — dopo la 4.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md          |   3 +++
 .claude/perimetro_review.txt                |   2 ++
 gas.py                                      |   5 +++++
 modules/sottofondo/__init__.py              |  38 ++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md                    |  19 +++++++++----------
 reports/handoff.md                          | n/d
 reports/stato_progetto.md                   |   3 ++-
 reports/ultimo_report.md                    |  26 +++++++++++---------------
 scripts/sottofondo/com.gas.sottofondo.plist |  34 ++++++++++++++++++++++++++++++++++
 tests/test_unit_sottofondo.py               |  80 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
8b12f585 feat(sottofondo): R7 fetta 2 — ripresa al boot (gas.py sottofondo-riprendi + plist launchd)
94189a8b chore(revisore): memoria review #840 — APPROVATO CON RISERVE
48aacb44 chore(revisore): memoria review #839 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 8b12f585 (motore). Due verdetti sullo stesso diff: #839 sul primo staged, #840 dopo le correzioni di R-839-1 e R-839-2. Incollati integrali.

### Review #839

## VERDETTO: APPROVATO CON RISERVE

Review #839, sul diff in staging del ramo claude/r7-ripresa-al-boot (5 file, +144 righe). Prima di giudicare ho letto CLAUDE.md §5, ho cercato in reports/stato_progetto.md le voci su R7 e sul sottofondo e ho consultato la memoria del revisore. Ho rilanciato io i test di tests/test_unit_sottofondo.py: 120 passano. Wall of Shame: nessuna storia tagliata a mano, nessun output di tool simulato. Il tetto di 10 iterazioni e `_get_window` non sono toccati.

**Elementi del diff esaminati**
- `modules/sottofondo/__init__.py:318` — `riprendi_al_boot` chiama la stessa `controlla` dell'inizio turno. Non c'è una seconda strada per far ripartire un compito: lock, tetto di riprese, tempo contato dalla prima creazione e marcatore `.ferma` restano quelli della fetta 1. Rischio esaminato: un secondo motore di ripresa che aggira i guardrail. Esito: ok. Tutto il corpo è dentro `try/except`, che scrive un `logging.warning` e restituisce False (§9 rispettato); il test a riga 1264 lo prova.
- `modules/sottofondo/__init__.py:335` e `modules/sottofondo/__init__.py:342` — la funzione legge il numero di riprese prima e dopo `controlla` e dice «ripreso» solo se è salito. Rischio esaminato: messaggio falso, oppure doppio avvio se il comando parte due volte (al boot e al primo turno). Esito: ok. Il test a riga 1216 copre il secondo lancio e prova che non c'è un secondo avvio. Una ripresa avviata male finisce nel ramo «ko» con il motivo, che `annulla` scrive come frase fissa: nel terminale finiscono solo id e stato, mai il testo del compito. Unico caso limite: se un altro processo fa ripartire il compito nello stesso istante, il messaggio può attribuirsi la ripresa. È solo una questione di testo, il lock in `_riprendi` impedisce comunque il doppio avvio.
- `gas.py:7154` — il nuovo comando `sottofondo-riprendi` viene dopo `_carica_dotenv()` (contesto: `gas.py:7104`). Quindi, anche lanciato da launchd senza la shell dell'utente, vede `TELEGRAM_BOT_TOKEN` e `GAS_SOTTOFONDO_RIPRESE` del `.env`. Il nome non si scontra con il ramo `sottofondo <id>`, che chiede `argv > 2` e un nome esatto. Esito: ok.
- `scripts/sottofondo/com.gas.sottofondo.plist:20` — `zsh -c` attiva `.venv` o `venv`, poi esegue `python3 gas.py sottofondo-riprendi`. C'è solo RunAtLoad, niente KeepAlive. AbandonProcessGroup è una cautela in più, perché `avvia` crea già una sessione propria per il figlio. Nessuno script lo installa. Esito: riserva R-839-1.
- `.claude/perimetro_review.txt:33` — aggiunge `scripts/sottofondo/` al perimetro di review, come già fatto per `scripts/voce/`. Esito: ok, il gate protegge anche il servizio di avvio.
- `tests/test_unit_sottofondo.py:1271` — il test lancia il comando vero in una cartella senza coda: exit 1, frase «cartella di Gas», nessun traceback. Esito: ok.

**Riserve (da registrare in stato_progetto.md)**
1. R-839-1 BASSA — Se non trova `.venv` né `venv`, il plist usa senza dirlo il `python3` di sistema che vede launchd, su macOS di solito `/usr/bin/python3`, senza le dipendenze di Gas. I plist della voce invece si fermano se `.venv` manca. Rischio: il comando parte, `avvia` lancia il figlio con lo stesso interprete, il figlio fallisce, il compito va in «ko» e una ripresa è consumata. Correzione proposta: pretendere il venv (`source .venv/bin/activate && exec python …`, come `scripts/voce/com.gas.voce.server.plist`) oppure uscire con un errore visibile nel log.
2. R-839-2 BASSA — Due rami di `riprendi_al_boot` non hanno test: «già finito» e «stato non leggibile» (`modules/sottofondo/__init__.py:350`). Il secondo scatta se il file del compito è sparito: `annulla` restituisce False e il comando esce con 1.
3. R-839-3 BASSA — Al login la rete può non essere ancora pronta. L'avviso Telegram della ripresa può andare perso (resta solo in gas_debug.log, non viene ritentato) e il compito ripreso può fallire subito sui provider, consumando una ripresa. Il danno è contenuto dal tetto di riprese.

**Rischi esplicitamente esclusi (non verificati)**
- Il comportamento reale di launchd su macOS non l'ho potuto verificare: siamo su Linux, quindi niente prove pratiche su caricamento del plist, AbandonProcessGroup, log in `~/Library/Logs` o `TUO_UTENTE` lasciato non sostituito.
- systemd sul server: citato nella docstring, ma in questa fetta non esiste.
- La suite completa del motore: ho rilanciato solo tests/test_unit_sottofondo.py.
- Prove a mutanti: non ne ho rilanciate. Nell'analisi statica, mettere la condizione `_riprese(job) > prima` a vero fa fallire il test a riga 1216.

Memoria aggiornata con la riga #839 e una lezione nuova (comandi lanciati da launchd/systemd: interprete del venv o errore visibile; `.env` caricato prima del ramo del comando). Committata da sola con `scripts/commit_memoria_revisore.sh` (commit 48aacb44). Il diff in staging è intatto: va ancora segnato con `bash scripts/segna_review_ok.sh` prima del commit.

File:
- /home/user/Gas/modules/sottofondo/__init__.py
- /home/user/Gas/gas.py
- /home/user/Gas/scripts/sottofondo/com.gas.sottofondo.plist
- /home/user/Gas/tests/test_unit_sottofondo.py
- /home/user/Gas/.claude/perimetro_review.txt
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #840 (#839-bis)

## VERDETTO: APPROVATO CON RISERVE

Seconda review (#839-bis, numero #840 in memoria) del diff in staging sul ramo claude/r7-ripresa-al-boot: 5 file, +159 righe. Ho rilanciato tests/test_unit_sottofondo.py: 121 test passano. Il codice di modules/sottofondo e di gas.py non è cambiato rispetto alla #839. Wall of Shame (CLAUDE.md §5): nessuna violazione, e i guardrail del §8 (tetto di 10 giri, `_get_window`) non sono toccati.

**Elementi del diff esaminati**
- `scripts/sottofondo/com.gas.sottofondo.plist:23` — il comando ora pretende `~/Gas/.venv`. Se manca, scrive «STOP: manca ~/Gas/.venv …» ed esce con 1; altrimenti attiva il venv ed esegue `exec python gas.py sottofondo-riprendi`. Rischio esaminato: che launchd ricada sul python di sistema, senza le dipendenze di Gas (R-839-1). Prova: ho estratto il comando con `plistlib`, che conferma anche che il file è un plist valido, e l'ho eseguito in bash con una HOME finta. Senza venv stampa STOP con exit 1; con un `activate` finto arriva a `python gas.py sottofondo-riprendi`. Esito: ok, R-839-1 CHIUSA. Il comportamento ora è lo stesso dei plist della voce (contesto: `scripts/voce/com.gas.voce.server.plist:15`).
- `tests/test_unit_sottofondo.py:1279` — nuovo test `test_boot_compito_gia_finito_e_file_sparito`. Copre il caso del compito «ok» con il posto ancora occupato: `_riprendi` restituisce False, `annulla` non lo tocca, la frase è «già finito», nessun avvio. Copre anche il file del compito sparito: risultato False, frase «stato non leggibile» (`modules/sottofondo/__init__.py:350`), nessun avvio. Rischio esaminato: rami senza test (R-839-2). Esito: ok, R-839-2 CHIUSA.
- `modules/sottofondo/__init__.py:318` e `gas.py:7154` — identici alla #839 e già approvati lì: riuso di `controlla`, confronto delle riprese prima/dopo, eccezioni intercettate con `logging.warning` e fallback (§9), `.env` caricato prima del comando. Esito: ok.

**Riserve aperte (da tenere in stato_progetto.md)**
1. R-839-3 BASSA (resta aperta, come dichiarato) — al login la rete può non essere ancora pronta. L'avviso su Telegram della ripresa può perdersi (resta solo nel log) e il compito ripreso può fallire subito, consumando una ripresa. Il tetto di riprese limita il danno.
2. R-840-1 COSMETICA — il commento del plist (riga 4) dice ancora che lancia `python3 gas.py sottofondo-riprendi`, ma il comando vero è `python` del venv. Va allineato quando capita.

**Rischi esplicitamente esclusi (non verificati)**
- launchd e zsh veri su macOS: questo ambiente è Linux senza zsh. Ho simulato il comando in bash, dove la sintassi `{ …; }`, `||` e `exit` è la stessa. Non ho provato il caricamento reale del plist né il log in `~/Library/Logs` con `TUO_UTENTE` lasciato non sostituito.
- La suite completa del motore: ho rilanciato solo tests/test_unit_sottofondo.py.

Memoria aggiornata con la riga #840 (nessuna lezione nuova) e committata da sola con `scripts/commit_memoria_revisore.sh` (commit 94189a8b). Il diff in staging è intatto: per il commit va prima eseguito `bash scripts/segna_review_ok.sh`.

File:
- /home/user/Gas/scripts/sottofondo/com.gas.sottofondo.plist
- /home/user/Gas/tests/test_unit_sottofondo.py
- /home/user/Gas/modules/sottofondo/__init__.py
- /home/user/Gas/gas.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_sottofondo.py`: 113 → 121 (8 test nuovi della ripresa al boot), tutti verdi in locale: `121 passed in 7.33s`.
- `tests/test_unit_kernel.py` (round-trip agentico, kernel non toccato salvo il comando nuovo in `main`), eseguito in locale, riga reale:

```
=== RIEPILOGO: 1187 PASS, 0 FAIL ===
```

Nessun FAIL. La suite `pytest tests/` completa in locale è stata fermata dopo ~5 minuti senza esito (non conclusa); la CI esegue le suite per file.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura:

```
completed	skipped	R7 fetta 2: ripresa al boot del compito in sottofondo	verifica-bot	claude/r7-ripresa-al-boot	pull_request_target	45215689561	2s	2026-11-23T16:22:05Z
in_progress		feat(sottofondo): R7 fetta 2 — ripresa al boot (gas.py sottofondo-rip…	CI	claude/r7-ripresa-al-boot	push	45215603377	1m32s	2026-11-23T16:21:37Z
in_progress		Gas usa il CRM: comandi da Telegram e voce, con firma e solo Opus	verifica-bot	claude/nifty-galileo-3k7kbm	pull_request_target	45215520653	2m0s	2026-11-23T16:21:09Z
```

Mappatura commit→run:
- 8b12f585 (motore): run CI 45215603377 in corso alla scrittura (esito non ancora disponibile); verifica-bot 45215689561 skipped (PR aperta senza etichetta, l'etichetta «verifica» si mette dopo questo commit).
- 94189a8b e 48aacb44 (memoria del revisore): nessuna run su questi SHA (pushati insieme a 8b12f585, la run testa solo l'albero di testa).
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-839-3 BASSA — al login la rete può non essere pronta: avviso Telegram della ripresa perso (solo nel log) e ripresa consumata; danno limitato dal tetto di riprese. Aperta.
- R-840-1 COSMETICA — commento del plist (riga 4) dice `python3`, il comando usa `python` del venv. Aperta.
- R-839-1 e R-839-2: CHIUSE (review #840).
- Riserve delle altre chat: in `reports/stato_progetto.md`, non toccate qui.
