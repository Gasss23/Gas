# HANDOFF — Dossier di fine sessione

**Sessione:** 23 novembre 2026 — R7 fetta 2: ripresa al boot del compito in sottofondo (sotto-chat di M1) — quarto giro: merge di main (PR #397) e V-1 MEDIA del bot su ea78c51b

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #398 (https://github.com/Gasss23/Gas/pull/398), etichetta «verifica». Tocca il motore: merge autonomo solo con verdetto testuale del bot APPROVATO senza finding V-x, CI verde e niente conflitti; altrimenti decide l'operatore. Verdetti del bot: eafdb49a BOCCIATO (V-1 MEDIA, corretta nel 2° giro); e9a08526 APPROVATO CON RISERVE, check neutral; ea78c51b BOCCIATO (V-1 MEDIA: senza `claude` nel PATH di launchd il compito ripreso finiva «ko»), corretto in 3ad51b10. La PR tocca `.claude/perimetro_review.txt` (macchina del bot): il merge lo decide comunque l'operatore.
2. (Facoltativo) Installare sul Mac `scripts/sottofondo/com.gas.sottofondo.plist` (istruzioni nel commento del file; serve `~/Gas/.venv`).

Numero e URL della PR presi dall'output di `gh api repos/Gasss23/Gas/pulls` (POST, creazione): `398`, `https://github.com/Gasss23/Gas/pull/398` (`gh pr` non disponibile in questo ambiente, solo REST).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 2 R7 — ripresa al boot**: FATTA. `riprendi_al_boot` (riusa `controlla`, stessi guardrail della fetta 1, nel terminale solo id e stato), comando `python gas.py sottofondo-riprendi`, plist launchd solo RunAtLoad che pretende `~/Gas/.venv`, `scripts/sottofondo/` nel perimetro, 8 test nuovi. Review #839 → correzioni R-839-1/R-839-2 → review #840.
- **Correzioni del 1° verdetto del bot sulla PR #398 (eafdb49a, BOCCIATO)**: FATTA. V-1 MEDIA: `riprendi_al_boot` aspetta la rete (TCP verso uno dei servizi usati, tetto `GAS_SOTTOFONDO_ATTESA_RETE` 120 s, max 600) e senza rete non tocca la coda (ripresa al primo turno, come prima). V-2 BASSA documentata nel codice (solo testo). V-3 BASSA: riavvio non partito → exit 1. R-840-1 (commento del plist) corretta. 5 test nuovi (126). Review #841.
- **Merge di origin/main (PR #397, chat CRM) nel ramo (terzo giro)**: FATTO (4114b631) per il conflitto sui report: tenuti i report di questo ramo (regola 3 di `reports/lavoro_parallelo.md`; riserve CRM già in `stato_progetto.md`). Review #849-MERGE-R7 APPROVATO CON RISERVE (R-849-1 BASSA: con «Sempre Opus» il compito ripreso al boot va solo a Opus, serve `GAS_CLAUDE_BIN` nel `.env` se `claude` non è nel PATH di launchd). Test: sottofondo 126 passed, kernel «=== RIEPILOGO: 1208 PASS, 0 FAIL ===».
- **V-1 MEDIA del bot su ea78c51b (quarto giro)**: FATTA (3ad51b10). Con «Sempre Opus» il compito ripreso va solo a `claude`: al boot, se `claude` non si trova (GAS_CLAUDE_BIN o PATH, come brains/claude_cli.py), la coda non si tocca e la frase dice di mettere GAS_CLAUDE_BIN nel `.env` (istruzioni anche nel plist). In più attese e controlli solo se il compito è ancora aperto (verifica esterna V-1). 3 test nuovi (129). Review #850-R7 APPROVATO CON RISERVE.
- **Fetta 3 R7 — lista dei lavori ricorrenti con stato**: FATTA in un'altra PR (#399, ramo `claude/r7-lavori-ricorrenti`).
- **Fetta 4 R7 — tetti di tempo duri**: DEFERITA — dopo la 3.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — dopo la 4.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md          |   9 +++++
 .claude/perimetro_review.txt                |   2 +
 gas.py                                      |   5 +++
 modules/sottofondo/__init__.py              | 115 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md                    |  22 +++++------
 reports/handoff.md                          | n/d
 reports/stato_progetto.md                   |   3 +-
 reports/ultimo_report.md                    |  53 ++++++++++-----------------
 scripts/sottofondo/com.gas.sottofondo.plist |  39 ++++++++++++++++++++
 tests/test_unit_sottofondo.py               | 188 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso. La CI confronta solo i path. Dopo il merge di main (4114b631) la base del ramo è il main nuovo (1b4954e2).

## §3 GIT LOG --ONELINE (sessione)

```
3ad51b10 fix(sottofondo): bot #398 V-1 — al boot senza cervello forte trovabile la coda non si tocca; niente attese per compiti già finiti
e9030add chore(revisore): memoria review #850 — APPROVATO CON RISERVE
ea78c51b docs(fine-task): PR #398 terzo giro — merge di main (PR #397), review #849-MERGE-R7
4114b631 Merge origin/main (PR #397, CRM) nel ramo della PR #398 — review #849-MERGE-R7 APPROVATO CON RISERVE
e9a08526 docs(fine-task): PR #398 secondo giro — correzioni del verdetto del bot, review #841
c87c9467 fix(sottofondo): verdetto bot #398 — al boot aspetta la rete, senza rete non tocca la coda
a469161a chore(revisore): memoria review #841 — APPROVATO CON RISERVE
eafdb49a docs(fine-task): R7 fetta 2 — report, handoff con review #839/#840, stato_progetto
8b12f585 feat(sottofondo): R7 fetta 2 — ripresa al boot (gas.py sottofondo-riprendi + plist launchd)
94189a8b chore(revisore): memoria review #840 — APPROVATO CON RISERVE
48aacb44 chore(revisore): memoria review #839 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 8b12f585 (motore): due verdetti sullo stesso diff, #839 sul primo staged e #840 dopo le correzioni di R-839-1 e R-839-2. Commit c87c9467 (motore, correzioni del verdetto del bot): review #841. Merge 4114b631: review #849-MERGE-R7. Commit 3ad51b10 (motore): review #850-R7. Incollati integrali.

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

### Review #841 (commit c87c9467)

## VERDETTO: APPROVATO CON RISERVE

Review n. 841. Oggetto: il diff staged in /home/user/Gas398, sul ramo claude/r7-ripresa-al-boot (base eafdb49a). Tocca 3 file, +120/−10. Lo SHA-256 del diff è 2df9a2ac…. Ho letto prima CLAUDE.md (§5, §8, §9), il punto R7 di reports/stato_progetto.md (riga 400) e la memoria del revisore (#839, #840).

**Elementi del diff esaminati**
1. `modules/sottofondo/__init__.py:371`: chiama `_aspetta_rete` solo se c'è un compito attivo. Lo fa PRIMA di leggere «prima» (riga 375) e PRIMA di chiamare `controlla`, quindi senza rete la coda non viene toccata, non si consuma nessuna ripresa e non parte nessun avviso. Rischio esaminato: il compito chiuso «ko» per sempre quando al boot manca la rete. Esito: **ok**, V-1 chiusa. Lettura di «prima» dopo l'attesa: se nei 120 s il primo turno riprende il compito, il boot risponde «ancora in corso» e non lo avvia una seconda volta.
2. `modules/sottofondo/__init__.py:337`: il tetto dell'attesa è `min(600, max(0, _numero_env(...)))`. Con inf, nan o testo non numerico `_numero_env` torna al default (`modules/sottofondo/__init__.py:98`), con valori negativi l'attesa è 0. Rischio esaminato: un valore dell'ambiente che blocca il boot. Esito: **ok**.
3. `modules/sottofondo/__init__.py:323`: `_rete_pronta` apre una connessione TCP diretta verso 3 servizi, timeout di 3 s, `OSError` intercettato e nessun dato inviato. Rischio esaminato: proxy, DNS, copertura dei test. Esito: **riserva R-841-1**.
4. `modules/sottofondo/__init__.py:393`: V-3, se il riavvio non parte («ripresa non avviata», scritto da `annulla` alla riga 466) il comando esce con 1. Gli altri casi «ko» (riprese finite, compito fermato, durata superata) restano exit 0. Esito: **ok**.
5. `modules/sottofondo/__init__.py:383`: il commento V-2 è corretto. Il doppio avvio resta impedito dal lock di `_riprendi`, quindi l'errore possibile riguarda solo il testo. Esito: **ok**.
6. `scripts/sottofondo/com.gas.sottofondo.plist:4`: il commento ora dice `python gas.py` (venv) e la riga 7 documenta l'attesa della rete. Esito: **ok**, R-840-1 chiusa.
7. `tests/test_unit_sottofondo.py:1300`: senza rete i file della coda restano identici byte per byte, nessun avviso parte e al primo turno il compito riparte. Gli altri test: `tests/test_unit_sottofondo.py:1317` (la rete arriva al terzo tentativo, attese [5, 5]), `tests/test_unit_sottofondo.py:1326` (tetto con un orologio finto), `tests/test_unit_sottofondo.py:1336` (nessuna attesa senza compito), `tests/test_unit_sottofondo.py:1343` (V-3). Esito: **ok**.
8. Contesto, `gas.py:7156`: il chiamante passa solo `Path.cwd()`, quindi in produzione si usano il controllo vero della rete e la vera attesa. I test che esistevano già e chiamano senza `rete=` (righe 1260-1271) escono prima dell'attesa, quindi non toccano la rete. Esito: **ok**.

**Verifiche eseguite**
- tests/test_unit_sottofondo.py: 126 passed, rieseguito da me.
- Mutanti che fanno fallire almeno un test (rosso):
  - attesa tolta;
  - attesa anche senza compito;
  - tetto tolto;
  - V-3 sempre `True`;
  - `dormi(0)`.
- Mutante che sopravvive: «`_rete_pronta` sempre True», nessun test se ne accorge (vedi R-841-1).
- Il modulo è stato ripristinato e la worktree coincide con l'index (controllato con `git diff --quiet`).

**Antipattern (§5, §8, §9)**: niente slicing della history, niente simulazione dei tool, il limite di 10 iterazioni e `_get_window` non sono toccati. La regola «mai eccezioni» resta rispettata: c'è l'`except Exception` esterno e `_rete_pronta` intercetta `OSError`. R-839-3 (rete al login) è chiusa da questa fetta.

**Riserve**
- **R-841-1 BASSA**: `_rete_pronta` (`modules/sottofondo/__init__.py:323`) apre un socket diretto e ignora `HTTPS_PROXY`. Su una macchina che esce su internet solo tramite proxy (per esempio la VPS futura) dà sempre «no rete»: la ripresa al boot non parte mai, ogni avvio aspetta 120 s ed esce con 1. Il danno resta contenuto perché il compito riparte comunque al primo turno, come prima di questa fetta. Inoltre la risoluzione DNS di `create_connection` non rispetta il timeout di 3 s, quindi l'attesa può superare un po' il tetto, e `_rete_pronta` non ha test (il mutante «sempre True» sopravvive). Da riguardare quando si costruisce l'unità systemd per il server.
- **R-841-2 COSMETICA**: l'attesa della rete avviene anche quando il processo del compito è ancora vivo (nuovo login senza riavvio). Offline il comando risponde «Rete non pronta…» ed esce con 1 anche se non c'era niente da riprendere. Effetto innocuo: compare solo nel log di launchd.

**Rischi esclusi (non verificati)**
- Comportamento reale sotto launchd sul Mac (rete al login, DNS offline, tempi reali): non è riproducibile in questo ambiente Linux.
- La connessione TCP vera verso i tre servizi: qui l'uscita passa da un proxy, quindi la connessione diretta non è indicativa.
- Il percorso systemd sulla VPS: non esiste ancora.

**Memoria del revisore**: aggiunta la riga #841 e una lezione (il controllo «c'è rete?» fatto con socket diretto ignora il proxy). Committata da sola con `scripts/commit_memoria_revisore.sh` in /home/user/Gas398, commit a469161a. Il diff staged del motore non è stato toccato: index ancora 3 file, +120/−10.

### Review #849-MERGE-R7 (merge 4114b631)

## VERDETTO: APPROVATO CON RISERVE

Review #849-MERGE-R7. Oggetto: il merge in corso di origin/main (PR #397, che porta il CRM e «Sempre Opus») nel ramo claude/r7-ripresa-al-boot (PR #398), nella worktree /home/user/Gas398. Ho letto: CLAUDE.md (§5, §8, §9, roadmap), la riga «Ultimo aggiornamento» e la sezione motore di reports/stato_progetto.md, e la coda della memoria del revisore.

**Elementi del diff esaminati**
- `gas.py:7347` — il ramo `sottofondo-riprendi` in main(). È l'unica differenza di gas.py rispetto a MERGE_HEAD (+5 righe). Sta dopo `_carica_dotenv()` (`gas.py:7297`) e dopo `sottofondo-ferma`. Rischio esaminato: righe di main perse o duplicate nell'auto-merge di gas.py. L'AST si legge, l'albero di lavoro coincide con l'indice e `git diff --cached MERGE_HEAD -- gas.py` mostra solo queste 5 righe. Esito: ok.
- `gas.py:385` — `_solo_opus_sempre()`, acceso di default. In `gas.py:403`, `_finestra_ha_dati_lead` diventa vero quando nella finestra c'è un messaggio user. Il kernel del compito in sottofondo (`gas.py:5254`, `per_sottofondo`) riceve il compito come messaggio user, quindi ogni compito ripreso al boot va SOLO a claude-cli. Se Opus non c'è, il turno finisce con l'errore di `gas.py:6134` («Rispondo solo con Claude Opus… non disponibile») e non ripiega su Gemini. Rischio esaminato: la ripresa da launchd. Esito: riserva (R-849-1, sotto).
- `gas.py:3847` — `crm_modifica` è negata con `nel_sottofondo`, e `gas.py:5594` azzera il testo dell'operatore del turno nel sottofondo. Rischio esaminato: un compito ripreso al boot che cambia il CRM senza firma. Esito: ok, il CRM di main non si apre al sottofondo.
- `modules/sottofondo/__init__.py:53` — `HOST_RETE` controlla prima api.anthropic.com, poi googleapis, poi telegram. Rischio esaminato: con «Sempre Opus», l'host del cervello usato deve essere tra quelli controllati. Esito: ok, Anthropic è il primo. Resta aperto il limite del controllo via socket con il proxy, già registrato in #841.
- `scripts/sottofondo/com.gas.sottofondo.plist:23` — il plist usa `/bin/zsh -c` senza login, quindi il PATH è quello minimo di launchd. `brains/claude_cli.py:556` (contesto) cerca il binario così: GAS_CLAUDE_BIN, poi `shutil.which("claude")`, poi "claude". Esito: riserva (R-849-1).
- `tests/conftest.py:15` — imposta `GAS_SOLO_OPUS="0"` per tutta la suite. Rischio esaminato: i test di R7 cambiano con «Sempre Opus»? No: la suite gira con la cascata spenta-Opus come prima. Il mio rerun di tests/test_unit_sottofondo.py dà 126 passed. Esito: ok. Effetto collaterale: nessun test prova la ripresa al boot con «Sempre Opus» acceso, già segnalato in #848-CRM per gli altri canali.

**Conflitti**
- `git ls-files -u` è vuoto, `git diff --check --cached HEAD` è pulito, 0 marcatori di conflitto.
- reports/handoff.md, ultimo_report.md e diff_sessione.md hanno lo stesso blob di HEAD: tenuti dal tuo ramo come vuole la regola 3. Le riserve CRM restano nella riga del motore di stato_progetto.md.
- La riga «Ultimo aggiornamento» è unita: R7 #398, CRM #397, funnel #396, voce/bacheca 22-11.
- La memoria del revisore ha entrambi i lati: #839-CRM…#848-CRM di main e #839/#840/#841 del ramo. I numeri si ripetono, ma i suffissi li distinguono e le righe restano univoche.
- `git diff --cached MERGE_HEAD` sul perimetro contiene solo le aggiunte R7: gas.py, modules/sottofondo, plist, test, perimetro_review e memoria. Nessuna modifica di main è andata persa.

**Riserve**
- **R-849-1 BASSA**: prima di #397, se `claude` non era nel PATH, il compito ripreso da launchd ripiegava sui gratuiti. Con «Sempre Opus» acceso fallisce, a meno che il .env abbia GAS_CLAUDE_BIN. Il .env viene caricato prima del comando, quindi una voce lì basta, e il giro notturno la richiede già: per questo la riserva è BASSA. Correzione: una riga nel commento del plist e nella guida («serve GAS_CLAUDE_BIN nel .env, come per la notte»). In alternativa, `gas.py doctor` può già segnalarlo. Va tracciata in stato_progetto.md.

**Rischi esclusi**
- La ripresa reale da launchd sul Mac non l'ho verificata: qui non c'è macOS né il binario `claude`.
- Non ho rieseguito tests/test_unit_kernel.py (mi fido del tuo «1208 PASS, 0 FAIL»).
- Non ho rivisto il codice CRM di #397: è già passato da #839-#848-CRM, e qui ho controllato solo che arrivasse intatto.

**Memoria**: le righe #849-MERGE-R7 e una lezione nuova sono in coda a /home/user/Gas398/.claude/agents/memoria_revisore.md, solo nel working tree e non in stage. Non ho lanciato `scripts/commit_memoria_revisore.sh` perché c'è un merge in corso. Mettila in stage e committala tu col merge, o subito dopo.

### Review #850-R7 (commit 3ad51b10)

## VERDETTO: APPROVATO CON RISERVE

Review #850-R7. Diff staged in /home/user/Gas398 (branch claude/r7-ripresa-al-boot, PR #398): 3 file, +82/−2, sha256 del diff `e52938b9…`. Ho letto prima CLAUDE.md (sezione 5), reports/stato_progetto.md (R7 fetta 2) e la mia memoria. La riga della memoria è committata (e9030add, solo quel file) e l'index del diff è rimasto com'era.

**Cosa ho controllato nel diff**

1. `modules/sottofondo/__init__.py:349` — `_forte_trovabile()`: con GAS_SOLO_OPUS spento risponde True. Altrimenti usa GAS_CLAUDE_BIN; se contiene un separatore controlla che il file esista e sia eseguibile, se no lo cerca con `shutil.which`. Ho confrontato la ricerca con quella del cervello in `brains/claude_cli.py:556`: segue lo stesso ordine (prima GAS_CLAUDE_BIN, poi which). Riconosce gli stessi valori di «spento» di `gas.py:378` (`_solo_opus_sempre`). Un'eccezione restituisce False, cioè la scelta sicura: la coda non si tocca. — **ok**
2. `modules/sottofondo/__init__.py:392` — la variabile `aperto` si basa sullo stato `in_coda`/`in_corso`, letto fuori dal lock. Se lo stato cambia nel frattempo non succede nulla di grave, perché la ripresa vera resta protetta dal lock di `_riprendi`. Il controllo del cervello forte viene PRIMA dell'attesa di rete, quindi non si perdono 120 secondi inutili. Un compito già «ok» o «ko» non aspetta e va dritto a `controlla`, che non usa la rete: la V-1 BASSA della verifica esterna è chiusa. — **ok**
3. `modules/sottofondo/__init__.py:396` — la frase di uscita contiene solo l'id del compito, mai il testo. Viene scritto un `logging.warning` e il comando esce con codice 1, come per il caso «senza rete». — **ok** (vedi R-850-2)
4. `scripts/sottofondo/com.gas.sottofondo.plist:9` — spiega di mettere GAS_CLAUDE_BIN nel .env. Il .env viene davvero caricato prima del comando `sottofondo-riprendi`: in `gas.py:7297` c'è `_carica_dotenv()` e lo smistamento dei comandi viene dopo, in `gas.py:7347`. — **ok**
5. `tests/test_unit_sottofondo.py:1357`, `tests/test_unit_sottofondo.py:1373` e `tests/test_unit_sottofondo.py:1390` — 129 PASS rieseguiti da me. Ho ragionato su cosa succederebbe col codice vecchio. Senza il controllo del forte, con 2 riprese ammesse, `_avvia_ripresa` verrebbe chiamata e la lista `_niente_riprese_vere` non sarebbe vuota: il test cade. Con l'attesa non condizionata, la lambda `rete` verrebbe chiamata: anche l'altro test cade. Ho anche verificato che `tests/conftest.py:15` imposti `GAS_SOLO_OPUS=0` per i test vecchi, come dichiarato. — **ok**

**Riserve**

- **R-850-1 BASSA**: `_forte_trovabile` controlla solo il binario. Non vede l'interruttore GAS_CLAUDE_CLI (la regola della cascata «forte» in `gas.py:1309` vuole GAS_CLAUDE_CLI=1) né il tetto giornaliero del forte. Con «Sempre Opus» acceso e GAS_CLAUDE_CLI spento, il compito ripreso al boot finirebbe comunque «ko». Non è un problema solo del boot (la ripresa alla prima interazione fallirebbe allo stesso modo), quindi non blocca. Basterebbe aggiungere il controllo dell'interruttore, letto dal .env.
- **R-850-2 COSMETICA**: la frase dice «claude non è nel PATH di questo avvio» anche quando GAS_CLAUDE_BIN c'è ma punta a un file inesistente o non eseguibile. Meglio distinguere i due casi.

**Cosa NON ho verificato**

- Il comportamento reale sotto launchd sul Mac (PATH minimo, AbandonProcessGroup): non si può riprodurre in questo ambiente Linux.
- La suite completa del kernel: non l'ho rieseguita, perché il diff non tocca gas.py né brains/.
- I valori di GAS_CLAUDE_BIN con `~` (tilde): falliscono sia qui sia nel cervello, quindi in modo coerente, ma non li ho provati.

Lezione aggiunta in memoria: un controllo «prerequisito trovabile» che copia la ricerca di un altro modulo va tenuto allineato a quella, e il .env deve essere caricato prima del comando che usa il controllo.

File: /home/user/Gas398/modules/sottofondo/__init__.py, /home/user/Gas398/scripts/sottofondo/com.gas.sottofondo.plist, /home/user/Gas398/tests/test_unit_sottofondo.py, /home/user/Gas398/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_sottofondo.py`: 113 → 129 (8 della ripresa al boot + 5 + 3 delle correzioni del bot), tutti verdi in locale: `129 passed in 6.36s`.
- `tests/test_unit_kernel.py` (round-trip agentico, kernel non toccato salvo il comando nuovo in `main`), eseguito in locale, riga reale:

```
=== RIEPILOGO: 1187 PASS, 0 FAIL ===
```

Nessun FAIL. Rieseguito DOPO il merge di main (4114b631): «=== RIEPILOGO: 1208 PASS, 0 FAIL ===»; sottofondo dopo il merge: 126 passed (129 dopo 3ad51b10, che tocca solo `modules/sottofondo/`, i suoi test e il plist). La suite `pytest tests/` completa in locale è stata fermata dopo ~5 minuti senza esito (non conclusa); la CI esegue le suite per file.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura (righe di un altro ramo):

```
in_progress		R7 fetta 3: stato dei lavori ricorrenti del giro di notte	verifica-bot	claude/r7-lavori-ricorrenti	pull_request_target	45221379881	3m9s	2026-11-23T16:52:30Z
in_progress		docs(fine-task): PR #399 terzo giro — merge di main, «Sempre Opus», V…	CI	claude/r7-lavori-ricorrenti	push	45221370319	3m12s	2026-11-23T16:52:27Z
completed	success	R7 fetta 3: stato dei lavori ricorrenti del giro di notte	verifica-bot	claude/r7-lavori-ricorrenti	pull_request_target	45218772891	3m10s	2026-11-23T16:38:24Z
```

Run di questo branch (`gh api .../actions/runs?branch=claude/r7-ripresa-al-boot`, output reale):

```
45217975784 e9a08526 verifica-bot pull_request_target completed/success
45217965677 e9a08526 CI push completed/success
45216004004 eafdb49a verifica-bot pull_request_target completed/success
45215981231 eafdb49a verifica-bot pull_request_target completed/skipped
45215968921 eafdb49a CI push completed/success
45215689561 8b12f585 verifica-bot pull_request_target completed/skipped
45215603377 8b12f585 CI push completed/failure
```

Mappatura commit→run:
- 8b12f585: CI 45215603377 failure (atteso: commit di codice senza handoff, handoff-check rosso; unit-suite verde); verifica-bot 45215689561 skipped.
- eafdb49a: CI 45215968921 success; verifica-bot 45216004004: check `verifica-bot` failure sullo SHA (1° verdetto BOCCIATO, V-1 MEDIA corretta in c87c9467); 45215981231 skipped.
- e9a08526: CI 45217965677 success; verifica-bot 45217975784: check neutral (2° verdetto APPROVATO CON RISERVE senza ALTA/MEDIA; la PR tocca la macchina del bot).
- 48aacb44, 94189a8b, a469161a, c87c9467, 4114b631: nessuna run propria (pushati insieme al commit di testa o non ancora pushati).
- ea78c51b: CI 45222037744 in_progress alla scrittura; verifica-bot 45222047615: il job è success, il check `verifica-bot` pubblicato sullo SHA è failure (3° verdetto BOCCIATO, V-1 MEDIA corretta in 3ad51b10).
- e9030add, 3ad51b10: nessuna run propria (pushati col commit di fine-task di questo giro).
- Commit di fine-task di questo giro: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- 1° verdetto del bot su PR #398 (eafdb49a, BOCCIATO): V-1 MEDIA (al boot senza rete il compito veniva chiuso «ko» per sempre) CORRETTA; V-2 BASSA («prima» letto fuori dal lock, solo testo) DOCUMENTATA nel codice; V-3 BASSA (riavvio non partito con exit 0) CORRETTA. Serve il verdetto del bot sul nuovo head.
- Verifica esterna sulla PR #398 (eafdb49a, [commento](https://github.com/Gasss23/Gas/pull/398#issuecomment-7107123430)): V-1 = R-839-3 CHIUSA da questo giro; V-2 = R-840-1 CHIUSA; V-3 COSMETICA (`TUO_UTENTE` nei log del plist, documentato) aperta; V-4 BASSA («ancora in corso» con lock non disponibile, solo testo) aperta.
- R-841-1 BASSA — `_rete_pronta` apre un socket diretto e ignora `HTTPS_PROXY`: su una macchina che esce solo via proxy la ripresa al boot non parte mai (il compito riparte al primo turno); DNS fuori dal timeout; nessun test della funzione. Da rivedere con l'unità systemd del server. Aperta.
- V-1 MEDIA del bot su ea78c51b (= R-849-1 rivalutata): CHIUSA (3ad51b10, #850-R7): senza forte trovabile la coda non si tocca.
- R-850-1 BASSA — `_forte_trovabile` controlla solo il binario, non l'interruttore GAS_CLAUDE_CLI né il tetto del giorno del forte (stesso limite della ripresa al primo turno). Aperta.
- R-850-2 COSMETICA — la frase dice «non nel PATH» anche con GAS_CLAUDE_BIN sbagliato. Aperta.
- Verifica esterna su ea78c51b ([commento](https://github.com/Gasss23/Gas/pull/398#issuecomment-7107946940)): V-1 BASSA (attese anche per compiti già finiti) CHIUSA; V-2 BASSA (captive portal: rete «pronta» senza servizio) = R-841-1, aperta; V-3 = R-849-1, chiusa.
- Verifica esterna su e9a08526 ([commento](https://github.com/Gasss23/Gas/pull/398#issuecomment-7107364671)): V-1 = R-841-1; V-2 = R-841-2; V-3 COSMETICA (NB doppio nel §2) corretta. Bot su e9a08526: V-1 COSMETICA (descrizione della PR ferma al primo giro) corretta; V-2 COSMETICA (attesa della rete anche con .ferma/riprese finite, frase «riparte» falsa in quel caso) aperta, parte di R-841-2.
- R-841-2 COSMETICA — attesa della rete anche col processo ancora vivo: offline «Rete non pronta» ed exit 1 senza niente da riprendere. Aperta.
- R-839-1, R-839-2, R-839-3, R-840-1: CHIUSE.
- Riserve delle altre chat: in `reports/stato_progetto.md`, non toccate qui.
