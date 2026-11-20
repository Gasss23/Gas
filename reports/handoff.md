# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-20 — CRM fetta 8: note basse di bot e verifica esterna sulla PR #387 (d809f5f1) e riserve del revisore #824–#826

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (numero dopo il push, vedi sotto). Le riserve aperte sono solo BASSE/COSMETICHE; se il bot dà riserve serve il sì dell'operatore in chat (CLAUDE.md §10).
2. Password delle copie cifrate nel `.env` del Mac (`GAS_CRM_BACKUP_PASSWORD`), salvata anche nel gestore di password; poi `pip install -r requirements.txt`.
3. Verificare che la cartella di Gas sia `~/Gas`, fuori da Scrivania e Documenti sincronizzate con iCloud.
4. Secondo passaggio nella chat claude.ai col link della PR #387 e di questa PR (riservatezza delle copie dei clienti).

---

## §1 SCOPE & ESITO FETTE

- **PR #387**: MERGIATA il 20-11 (d03e5bf2) col via dell'operatore: CI verde, bot e verifica esterna (https://github.com/Gasss23/Gas/pull/387#issuecomment-7041110550) APPROVATO CON RISERVE senza ALTA/MEDIA.
- **Fetta 8a — note basse su d809f5f1** (bot V-1 ripristino interrotto in chiaro, bot V-2 motivo «disco non collegato?» per una cartella mai creata, verifica esterna V-2 testo a copia spenta): FATTA, commit d62adafb. Review #824 APPROVATO CON RISERVE (R-824-1 BASSA, R-824-2 COSMETICA), corrette nello stesso diff e riviste in #825 APPROVATO CON RISERVE (R-825-1 COSMETICA, R-825-2 BASSA).
- **Fetta 8b — R-825-1 e R-825-2**: FATTA, commit a9dbf6be. Review #826 BOCCIATO (R-826-1 MEDIA: con una cartella senza «/» le copie finivano nella cartella di lavoro con «ATTIVA» falso), corretto e rivisto in #827 APPROVATO.
- **Non fatte (note del bot e della verifica esterna, BASSE/COSMETICHE):** verifica esterna V-4 (il thread della prova, dopo il tempo massimo, resta vivo: innocuo) — DEFERITA, cosmetica.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 modules/crm/copia_cifrata.py       |  63 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----
 modules/crm/server.py              |  25 +++++++++++++++++++------
 reports/crm/guida.md               |   2 +-
 reports/diff_sessione.md           |  19 ++++++++-----------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  37 ++++++++++++++++---------------------
 tests/test_unit_crm.py             | 101 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base della sessione: d03e5bf2 (origin/main, dopo il merge della PR #387).

## §3 GIT LOG --ONELINE (sessione)

```
a9dbf6be fix(crm): il CRM parte anche con la cartella delle copie scritta male o con iCloud bloccato da macOS; mai copie nella cartella di lavoro; avvisi senza «iCloud» fisso (R-825-1/2, R-826-1/2) — review #827 APPROVATO
49ea2fb7 chore(revisore): memoria review #827 — APPROVATO
68e849ed chore(revisore): memoria review #826 — BOCCIATO
d62adafb fix(crm): ripristino interrotto non lascia il file in chiaro; motivi e avvisi giusti a copia esterna spenta o cartella mai creata (note basse di bot e verifica esterna su #387) — review #824 e #825 APPROVATO CON RISERVE
5d83286f chore(revisore): memoria review #825 — APPROVATO CON RISERVE
5e959f65 chore(revisore): memoria review #824 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #824-CRM (diff poi committato in d62adafb, con le correzioni riviste in #825)

## VERDETTO: APPROVATO CON RISERVE

Review #824-CRM del diff staged (3 file, +83/−6, sopra d809f5f1). Letture obbligatorie fatte: CLAUDE.md §5, §8 e §9, reports/stato_progetto.md (voce CRM fetta 6-7), memoria del revisore. Nel diff non c'è slicing della history e nessun tool viene simulato. Il kernel non è toccato.

**Elementi esaminati**
1. `modules/crm/copia_cifrata.py:284` — `_pulisci_ripristini_interrotti` toglie i temporanei in chiaro rimasti da ripristini interrotti. Rischi esaminati:
   - prenda file di altre destinazioni;
   - segua collegamenti simbolici;
   - tocchi ripristini ancora in corso;
   - sbagli con nomi strani.
   Esito: ok. Il nome deve corrispondere esattamente (fullmatch con `re.escape`, glob con `glob.escape`). Controllato su Python 3.11 e 3.13 con nomi che contengono `[ ] * ?` e con nomi nascosti: il resto morto viene tolto, il nome «vicino» (`crm.dbx.…`) resta. Una cartella che non c'è non dà errore. `unlink` non segue i collegamenti, quindi anche uno scambio con un collegamento fra il controllo e la cancellazione è innocuo.
2. `modules/crm/copia_cifrata.py:274` e `modules/crm/copia_cifrata.py:298` — `_processo_vivo` riceve il PID ricavato dal nome del file. Rischio: un'eccezione che non è OSError. Esito: **riserva R-824-1**, vedi sotto.
3. `modules/crm/copia_cifrata.py:346` — la pulizia gira dopo `decifra`. Rischio: cancellazioni fatte da chi non ha la password. Esito: ok, con la password sbagliata non si tocca niente. La pulizia è idempotente anche al secondo tentativo di `cmd_ripristina`.
4. `modules/crm/copia_cifrata.py:118` — motivo nuovo «non c'è: creala, o collega il disco se è su un disco esterno». Rischio: testi vecchi rimasti in giro. Esito: ok. Nel codice e nei test non resta «disco non collegato» come testo del motivo; restano solo descrizioni storiche in reports/handoff.md, che si riscrive a fine sessione.
5. `modules/crm/server.py:308` — il motivo della copia locale fallita ora dipende da `motivo_spenta()`. Rischi esaminati:
   - un blocco del thread del guardiano: `cartella()` fa solo `is_dir` su iCloud Drive, già usato prima;
   - lo stato rosso perso: `_segna_copia` resta con `spenta=None`, quindi rosso e avviso restano, come voleva R-821-1.
   Esito: ok. Resta però la nota cosmetica R-824-2 su `modules/crm/server.py:284`.
6. `tests/test_unit_crm.py:1799` — il test nuovo. Rischio: il test non prova davvero le due correzioni. Esito: ok.
   - Sul codice CRM di d809f5f1 falliscono 2 test (`test_v1_bot387b…` su `tests/test_unit_crm.py:1822`, `test_ve386c…` su `tests/test_unit_crm.py:1662`); li ho rieseguiti io.
   - Con la copia_cifrata nuova e il server.py vecchio, la parte V-2 fallisce da sola su `tests/test_unit_crm.py:1830`: anche la seconda correzione ha il suo fail-before.
   - Suite CRM staged: 137 passed (rieseguito). mypy: 0 errori in modules/crm. I 78 errori sono in altri file, preesistenti.

**Riserve**
- **R-824-1 BASSA** — `_processo_vivo` (`modules/crm/copia_cifrata.py:274`) intercetta solo OSError. Con un PID oltre 2^31−1 `os.kill` alza OverflowError, che non è un OSError. L'ho provato: un file `rip.db.99999999999-1.ripristino.tmp` accanto alla destinazione fa uscire OverflowError da `ripristina`. È contro il «Mai solleva» della docstring, e il CLI (`modules/crm/__main__.py:421` prende solo ErroreCRM) stamperebbe un traceback. Nessun dato perso: succede prima di scrivere qualsiasi cosa. Rimedio: `[0-9]{1,10}` nella regex, oppure `except (OSError, OverflowError): return True`, più un test con un nome a 11 cifre.
- **R-824-2 COSMETICA** — tre punti:
  - a copia esterna spenta l'avviso Telegram dice ancora «la copia cifrata su iCloud NON è riuscita (…)» (`modules/crm/server.py:284`): è della stessa famiglia di V-2;
  - `\d` accetta anche cifre non ASCII (un «٣» diventa PID 3);
  - la riga `tests/test_unit_crm.py:1667` è lunga 108 caratteri.

**Nota non classificata** (ragionamento, non provato a mano). La pulizia scatta solo al ripristino successivo verso la stessa destinazione, e solo se quella destinazione non c'è ancora. Due casi in cui il resto rimane:
- ripristino ucciso fra `os.link` e il `finally`: la destinazione esiste, quindi il nuovo tentativo si ferma su «esiste già» prima della pulizia. Il resto è un secondo nome dello stesso file della destinazione: nessun dato in più esposto, ma resta;
- ripristino successivo verso un'altra destinazione: il resto vecchio resta.

**Rischi esclusi (non verificati)**
- Comportamento reale su macOS di `os.kill(pid, 0)` e del glob sotto iCloud Drive: qui non c'è un Mac.
- Il ramo PermissionError di `_processo_vivo` e la cartella senza permesso di lettura: il container gira come root, la prova non è significativa.
- Ripristini concorrenti da container o macchine diverse sulla stessa cartella (lì il PID non è visibile e un ripristino in corso verrebbe cancellato): non è un caso del Mac.

**Memoria**: riga `#824-CRM` e una lezione (PID da un nome di file e OverflowError) scritte in /home/user/Gas/.claude/agents/memoria_revisore.md. Committate con `scripts/commit_memoria_revisore.sh`, commit 83aadd8a. L'indice staged dei 3 file è intatto. `.claude/.review_ok` non l'ho creato e il diff non l'ho committato.

### Review #825-CRM (commit d62adafb)

## VERDETTO: APPROVATO CON RISERVE

Review #825-CRM del diff staged: 3 file, +98/−7, sha256 di `git diff --cached` che inizia con c7e9558e0c18986f. Ho letto CLAUDE.md §5/§8/§9, stato_progetto.md (voce CRM fetta 7) e la mia memoria (#815…#824).

**Base cambiata durante la review.** Quando ho iniziato, HEAD era 83aadd8a. Durante la review il ramo `claude/nifty-galileo-3k7kbm` è stato rimesso sopra il merge d03e5bf2 (#387), poi sopra 5e959f65 (memoria #824). I tre blob staged sono identici byte per byte a quelli che ho revisionato, e `modules/crm` e i test non cambiano fra d809f5f1 e 5e959f65. Il delta quindi è lo stesso.

**Elementi del diff esaminati**
1. `modules/crm/copia_cifrata.py:279`: `_processo_vivo` tratta OverflowError come «vivo» (R-824-1). Rischio esaminato: un PID oltre 2^31-1 che faceva uscire un'eccezione da `ripristina`, contro il suo «Mai solleva». Ho verificato che `os.kill(2**40, 0)` solleva OverflowError, che non è un OSError, su 3.11, 3.12 e 3.13. Il mutante senza OverflowError fa diventare rosso il test (riga 276). `_processo_vivo(0)`, `_processo_vivo(2**31)` e `_processo_vivo(9999999999)` danno tutti True, quindi il file non si tocca. **Esito: ok.**
2. `modules/crm/copia_cifrata.py:290`: la regex del PID è `[0-9]{1,10}` con fullmatch, ancorata al nome della destinazione. Rischio esaminato: cifre non ASCII e PID fuori misura. La mia prova diretta, con un nome che contiene `[a]*?`, dà questi risultati:
   - «٣», «٩٩٩٩٩٩٩٩٩» e cifre fullwidth: restano;
   - 10 cifre: resta;
   - «0»: resta;
   - PID morto: tolto.

   Col mutante `\d+` vengono tolti i nove arabi e i fullwidth: il codice è giusto. Gli altri mutanti fanno tutti diventare rosso il test: senza `is_symlink`, senza il nome della destinazione, coi due mutanti combinati. **Esito: ok.**
3. `modules/crm/copia_cifrata.py:347`: la pulizia gira dopo `decifra`. Rischio esaminato: la pulizia salta con la password sbagliata. È un limite accettabile, perché il resto viene tolto al primo ripristino riuscito. **Esito: ok.**
4. `modules/crm/server.py:285`: l'avviso dice «la copia di sicurezza sul Mac» quando la copia esterna è spenta. Rischio esaminato: un'eccezione di `motivo_spenta`. Sta dentro il try/except Exception, quindi §9 è rispettato. Il mutante con l'avviso fisso su iCloud fa diventare rosso il test (`tests/test_unit_crm.py:1841`). **Esito: ok nel codice, riserva cosmetica sul testo (R-825-1).**
5. `modules/crm/server.py:311`: il motivo della copia locale fallita. Rischio esaminato: la chiamata a `motivo_spenta()` sta fuori dal try, nel thread del guardiano (chiamata da `modules/crm/server.py:348`). **Esito: riserva preesistente (R-825-2).**
6. `tests/test_unit_crm.py:1825`: caso «٣». **Esito: riserva (R-825-1).**

**Riesecuzioni**
- Suite CRM: 137 passed.
- Fail-before col `modules/crm` di HEAD e i test nuovi: 2 failed (`test_ve386c…`, `test_v1_bot387b…`) e 135 passed.
- mypy: 0 errori dentro `modules/crm`. Gli altri 78 errori stanno in file fuori dal diff.
- Wall of Shame: nessuno slicing della storia, nessun tool simulato. Kernel e guardrail non toccati.

**Riserve (da tracciare in stato_progetto.md)**
- **R-825-1 COSMETICA**
  - Il caso «٣» (`tests/test_unit_crm.py:1825`) non controlla davvero le cifre non ASCII. «٣» diventa il PID 3, che esiste nel container e sulla CI Linux. Così col mutante `\d+` il test resta verde (provato). Rimedio: usare «٩٩٩٩٩٩٩٩٩», che porta a un PID morto e quindi il mutante lo toglierebbe.
  - Il testo dell'avviso a copia esterna spenta è ridondante: «la copia di sicurezza sul Mac NON è riuscita (la copia sul Mac non è riuscita, la copia fuori dal Mac è spenta)».
- **R-825-2 BASSA, preesistente**
  - Con `GAS_CRM_BACKUP_CIFRATO_DIR` che inizia con «~utente» inesistente, `expanduser` solleva RuntimeError in `cartella()` (`modules/crm/copia_cifrata.py:57`).
  - Di conseguenza `Stato` non si crea (`modules/crm/server.py:122`) e il CRM non parte. Provato: «Stato solleva RuntimeError».
  - La chiamata nuova a `modules/crm/server.py:311` non apre un caso in più, perché l'avvio fallisce prima.
  - Rimedio: in `cartella()` intercettare RuntimeError e restituire un motivo.

**La tua nota non classificata (resto che resta con destinazione già esistente o con un'altra destinazione): per me non è da riserva.**
- Se `dest` esiste perché il processo è morto fra `os.link` e l'unlink, il resto è un collegamento fisico allo stesso file del DB. Non contiene dati in più del DB, che è già in chiaro con permessi 0644; il resto è 0600.
- Con un'altra destinazione siamo nel caso di prima del fix, cioè un limite.
- Basta dichiararlo nello stato.
- Stessa cosa per il riuso dei PID dopo il riavvio del Mac: il resto viene tenuto, che è il verso sicuro.

**Rischio esplicitamente escluso**
- Non ho verificato il comportamento su macOS reale (APFS, PID fino a 99998 e loro riuso dopo un riavvio, permessi su iCloud Drive): il container è Linux.
- Non ho verificato Windows: lì `os.kill(pid, 0)` termina il processo invece di sondarlo. Il CRM però gira solo sul Mac.

**Memoria del revisore**
- Ho aggiunto la riga `#825-CRM` e una lezione: «un test che prova un filtro sull'input deve usare valori che, senza il filtro, portano al ramo distruttivo».
- Ho committato solo `/home/user/Gas/.claude/agents/memoria_revisore.md`: commit 5d83286f, fatto con `scripts/commit_memoria_revisore.sh`.
- Il diff del CRM resta staged e non committato. Non ho creato `.claude/.review_ok`.

### Review #826-CRM (diff bocciato, non committato; corretto e rivisto in #827)

## VERDETTO: BOCCIATO

Review #826-CRM. Ho guardato il diff staged (3 file, +53/−8, sopra d62adafb). Prima ho letto CLAUDE.md sez. 5, 8 e 9, poi stato_progetto.md (solo le righe sul CRM) e la memoria del revisore.

**Elementi del diff esaminati**
1. `modules/crm/copia_cifrata.py:62`: se `expanduser` solleva RuntimeError, il ripiego `return Path(v)` restituisce il percorso così com'è. Ho controllato se un percorso non espanso arriva sempre al «rosso», come dice il commento. **Blocco (R-826-1 MEDIA, regressione introdotta dal diff).** «~nome» non espanso è un percorso RELATIVO alla cartella di lavoro. Con due componenti («~utente/copie», il caso del test) il genitore non esiste e la copia va in rosso. Con UN solo componente (es. `GAS_CRM_BACKUP_CIFRATO_DIR=~GasCopie`, cioè manca la «/») il genitore è «.», che esiste: `_genitore_assente` lascia passare. L'ho provato su Python 3.11 e 3.13: `esito_all_avvio()` → «ATTIVA in ~gascopie_inesistente (prova di scrittura riuscita)» e la cartella `~gascopie_inesistente` viene creata nella cartella di lavoro. La guida dice di avviare con `python -m modules.crm serve`, cioè da ~/Gas: le copie cifrate dei clienti finirebbero dentro il repo (`*.gascrm` non è in .gitignore). Prima di questo diff lo stesso valore impediva al CRM di partire, quindi l'errore si vedeva. Adesso la copia risulta riuscita ma non esce dal Mac: è proprio il guasto che questa fetta combatte da #386 (V-1 bot #387 era MEDIA per un «ATTIVA» falso).
2. `modules/crm/copia_cifrata.py:66`: `except OSError` attorno a `ICLOUD_DRIVE.is_dir()`, che restituisce comunque la cartella di iCloud. Rischi controllati: che sia raggiungibile e che il test morda. **Ok.** Ho letto il sorgente di `Path.is_dir` su 3.11, 3.12 e 3.13: tutte e tre lasciano passare EPERM/EACCES. Con i mutanti «ritorna None» ed «eccezione non presa» `test_r825_2…` va in rosso (provato). Il seguito è corretto: `_genitore_assente` ritrova il PermissionError sul genitore e restituisce un motivo, quindi `ok False` e `spenta False`.
3. `modules/crm/server.py:286`: a copia esterna spenta l'avviso ora dice `{motivo}. Nessuna copia di sicurezza nuova…`. Ho controllato la ripetizione di «non è riuscita» e l'eccezione dentro il try (§9). **Ok** per il caso spento (R-825-1 chiusa).
4. `modules/crm/server.py:290`: ramo con copia esterna ATTIVA. **Riserva R-826-2 COSMETICA, preesistente.** Se fallisce la copia locale, l'avviso (simulato) dice ancora «la copia cifrata su iCloud NON è riuscita (la copia sul Mac non è riuscita, quindi nemmeno quella fuori dal Mac)». Ripete «non è riuscita» e nomina iCloud anche quando la cartella è `GAS_CRM_BACKUP_CIFRATO_DIR`. Nota collegata: la scelta del ramo rilegge `motivo_spenta()` invece di sapere quale copia è fallita; è una scorciatoia, non un bug che si possa riprodurre oggi.
5. `tests/test_unit_crm.py:1826`: nove «٩» al posto di «٣». Ho controllato che il test morda davvero. **Ok, R-825-1 chiusa.** Col mutante `\d{1,10}` nello schema (`modules/crm/copia_cifrata.py:300`) il test cade su `arabo.exists()` (provato).
6. `tests/test_unit_crm.py:1846`: test nuovo `test_r825_2…`. Ho controllato la copertura e che non scriva sull'iCloud vero. **Ok** per i due casi che copre: is_dir viene negato su ICLOUD_DRIVE, quindi anche sul Mac non scrive su iCloud. Però NON copre il caso a un solo componente, ed è per questo che la regressione del punto 1 passa.

**Verifiche rieseguite**
- Suite CRM: 138 passed.
- Fail-before (test staged col codice CRM di HEAD d62adafb): 2 failed (`test_v1_bot387b…`, `test_r825_2…`), 136 passed. L'affermazione del chiamante è confermata.
- mypy: nessun errore in modules/crm (i 76 errori segnalati sono in gate.py, tts.py e gas.py, file non toccati).
- `git diff --cached --check`: pulito.

**Correzione richiesta (già provata in una copia nel mio spazio di lavoro, CRM 138 passed)**
- In `_genitore_assente`, prima del try, rifiutare i percorsi non completi: `if not dest_dir.is_absolute(): return f"la cartella {dest_dir} non è un percorso completo: nessuna copia fuori dal Mac"`. Con `~gascopie_inesistente` l'avvio diventa «NON FUNZIONA (… non è un percorso completo …)» e non viene creata nessuna cartella. Chiude anche il caso già esistente di un valore relativo come «copie».
- Aggiungere al test il caso a un componente: `monkeypatch.chdir(tmp_path)`, valore «~x_inesistente_r826», poi verificare `esito_all_avvio().startswith("NON FUNZIONA")` e che `not (tmp_path / "~x_inesistente_r826").exists()`. Poi verificare che il test cada col codice di questo diff.
- R-826-2 si può chiudere nello stesso giro (testo del ramo attivo senza doppio «non è riuscita» e senza «iCloud» fisso) oppure tracciarla in stato_progetto.md.

**Rischi esclusi esplicitamente**
- Comportamento reale di macOS e iCloud (TCC che nega lo stat di `com~apple~CloudDocs`) NON verificato: non è riproducibile nel container, che gira come root. Mi sono basato sul sorgente di pathlib e sul test con PermissionError simulato.
- Suite pytest su 3.11 e 3.12 NON eseguita: pytest non è installato per quegli interpreti. Su 3.11 ho riprodotto direttamente solo `cartella()` ed `esito_all_avvio()`.
- Non ho controllato se qualche script fa `git add -A` e potrebbe committare una cartella `~nome/` creata nel repo. Il rischio del punto 1 resta comunque: la copia non esce dal Mac.

**Memoria**
- Riga contatore `#826-CRM` e una lezione nuova (un ripiego che lascia un percorso non espanso lo rende relativo: provare il caso a un componente e pretendere is_absolute) aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md.
- Committata con `bash scripts/commit_memoria_revisore.sh` (68e849ed, solo quel file). Il diff staged è intatto (3 file, +53/−8).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #827-CRM (commit a9dbf6be)

## VERDETTO: APPROVATO

Review #827-CRM. È il secondo giro della #826 (BOCCIATO). Ho esaminato il diff staged: 3 file, +86/−12, sopra 68e849ed.

**Letture obbligatorie fatte:** CLAUDE.md (sezioni 5, 8 e 9), reports/stato_progetto.md (le voci del CRM, letto a pezzi), .claude/agents/memoria_revisore.md (dalla #815 alla #826).

**Elementi del diff esaminati:**
1. `modules/crm/copia_cifrata.py:126` — `_genitore_assente` rifiuta per primo un percorso non completo (`not dest_dir.is_absolute()`).
   - Rischio esaminato: la regressione R-826-1, cioè le copie scritte nella cartella di lavoro, con un falso «ATTIVA» all'avvio. `is_absolute()` è un calcolo puro, quindi il «Mai solleva» resta vero.
   - Prove mie su Python 3.11, 3.12 e 3.13 (cryptography presente), dentro una cartella di lavoro vuota:
     - `~gascopie_inesistente`, `~gascopie_inesistente/sub`, `copie`, `./x`, `$HOME/x` e anche `HOME=relhome` con `~/copie`: `esito_all_avvio` dà «NON FUNZIONA (… non è un percorso completo …)», `copia_fuori` dà (None, motivo) e la cartella di lavoro resta vuota.
     - Con un percorso assoluto valido l'esito è ancora «ATTIVA».
   - Esito: **ok**.
2. `modules/crm/copia_cifrata.py:59` — il ripiego sul `RuntimeError` di `expanduser` ora porta al rifiuto. Il commento («`_genitore_assente` lo rifiuta: copia in rosso») corrisponde al comportamento. Esito: **ok**.
3. `modules/crm/server.py:320` e `modules/crm/server.py:288` — `_copia_giornaliera` passa `locale=True` e `_segna_copia` non rilegge più `motivo_spenta()`.
   - Ramo «copia sul Mac fallita»: l'avviso è solo il motivo, con un solo «non è riuscita».
   - Ramo della copia esterna (`modules/crm/server.py:292`): dice «fuori dal Mac», non più «iCloud» fisso.
   - Rischio esaminato: un avviso falso o doppio all'operatore. L'avviso resta dentro `try/except` (§9) e non contiene dati dei clienti.
   - Esito: **ok**.
4. `tests/test_unit_crm.py:1859` e `tests/test_unit_crm.py:1866` — `chdir` in una cartella vuota, i due valori indicati, poi il controllo che la cartella resti vuota. `tests/test_unit_crm.py:1876` controlla il ramo con la copia esterna ATTIVA.
   - Rischio esaminato: test che non mordono. Ho provato i mutanti sull'albero dell'indice:
     - senza `is_absolute`: test rosso;
     - senza `locale=True`: rosso («2 == 1» sul conteggio);
     - con «iCloud» fisso in tutti e due i rami: 2 test rossi.
   - Esito: **ok**.

**Riesecuzioni mie:**
- Suite CRM sull'albero dell'indice: 138 passed.
- Codice CRM di HEAD d62adafb con i test nuovi: 2 failed / 136 passed (`test_v1_bot387b…` e `test_r825_2…`). Torna con la #826.
- mypy: 0 errori in modules/crm.
- Nessun altro modulo importa `copia_cifrata` o `crm.server` (gas.py compreso): il kernel non è toccato.

**Wall of Shame:** nessun taglio diretto della cronologia, nessuna simulazione dell'output dei tool. Lo stub `avvisa` del test sostituisce il notificatore Telegram, non un tool del modello.

**Rischio escluso:** non ho verificato il comportamento sul Mac vero (iCloud Drive con il permesso negato da macOS, `.env` letto da `_carica_chiavi` con valori tra virgolette). In questo ambiente non si riproduce: ho provato solo su Linux con variabili d'ambiente impostate a mano.

**Note cosmetiche (nessuna è una riserva):**
- `reports/crm/guida.md` (riga 117) non dice che `GAS_CRM_BACKUP_CIFRATO_DIR` deve essere un percorso completo; il motivo mostrato all'avvio lo spiega da sé.
- Nel ramo della copia esterna, i motivi di `_genitore_assente` ripetono «nessuna copia fuori dal Mac» dentro «… fuori dal Mac NON è riuscita (…)».

**Memoria del revisore:** riga `#827-CRM — 2026-11-20 — APPROVATO — …` aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con `scripts/commit_memoria_revisore.sh` (commit 49ea2fb7, solo quel file). Il diff staged resta intatto: 3 file, +86/−12. Come richiesto, non ho creato `.claude/.review_ok` e non ho committato il diff.

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_crm.py`:** 136 su main d03e5bf2 → 137 (d62adafb) → 138 passed (a9dbf6be).
  - d62adafb: `test_v1_bot387b_ripristino_interrotto_non_resta_in_chiaro` nuovo e `test_ve386c_note_del_terzo_giro` aggiornato falliscono sul codice di d809f5f1 (2 failed, 135 passed).
  - a9dbf6be: `test_r825_2_cartella_non_valida_o_icloud_negato_il_crm_parte` nuovo e `test_v1_bot387b…` aggiornato falliscono sul codice di d62adafb (2 failed, 136 passed); il caso a un componente fallisce sul diff bocciato #826 (1 failed, 137 passed).
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.
- **mypy:** 0 errori in `modules/crm`.

## §6 STATO CI

`gh run list` non usato: in questa sessione cloud GitHub si interroga con gli strumenti MCP.
- PR #387 mergiata con CI verde su d809f5f1: unit-suite success e handoff-check success (run 44746651994), verifica-bot neutral (run 44746659372, verdetto APPROVATO CON RISERVE).
- Mappatura commit→run:
  - `5e959f65`, `5d83286f`, `d62adafb`, `68e849ed`, `49ea2fb7`, `a9dbf6be`: run non ancora disponibile alla scrittura dell'handoff. Saranno pushati insieme al commit di fine-task che contiene questo file: una sola run testerà l'albero di testa; i commit intermedi non avranno una run propria.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **Rischi non verificabili qui (revisori #825 e #827, non c'è un Mac):** macOS che blocca iCloud Drive (TCC), `os.path.ismount` sui dischi esterni, riuso dei PID dopo un riavvio (il resto viene tenuto: verso sicuro).
- **Limite dichiarato (revisore #825, non riserva):** il temporaneo in chiaro di un ripristino interrotto viene tolto solo al ripristino seguente verso la stessa destinazione e se questa non c'è ancora.
- **Note cosmetiche (revisore #827, non riserve):** il motivo di `_genitore_assente` ripete «nessuna copia fuori dal Mac» dentro l'avviso della copia esterna. La guida ora dice che la cartella deve essere un percorso completo.
- **Verifica esterna #387 V-4 (COSMETICA):** dopo il tempo massimo il thread della prova resta vivo; innocuo.
- **Chiuse in questa sessione:** bot V-1/V-2 e verifica esterna V-2 su d809f5f1; R-824-1, R-824-2, R-825-1, R-825-2, R-826-1, R-826-2. La verifica esterna V-1 (il «sì» dell'operatore non verificabile da file) riguarda #387, già mergiata col via dato in chat; V-3 (§6 senza stato CI) è strutturale.
- **Ancora aperte da prima:** R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4 (vedi `reports/stato_progetto.md`).
