# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-20 — CRM fetta 8: note basse di bot e verifica esterna sulle PR #387 (d809f5f1) e #388 (0d946f08) e riserve del revisore #824–#829, più le note del bot su 7cd7a2f0

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #388 (https://github.com/Gasss23/Gas/pull/388), aperta dopo il push di 538a8948 con l'etichetta «verifica». Su cfa0156a il bot ha dato failure per un falso positivo del suo classificatore («Non bloccante» letto come MEDIA, verdetto testuale APPROVATO CON RISERVE con il solo V-1 BASSA): corretto nella PR #389, mergiata (09e112f5) col via dell'operatore («fai quello, sicurezza massima», «ok avvisami quando hai mergiato»); main portato nel ramo (merge 7d6a6865) per un nuovo giro del bot. Su 0d946f08: CI verde, bot APPROVATO CON RISERVE (V-1/V-2 BASSE, chiuse da a565c7b6), verifica esterna APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/388#issuecomment-7041948403). Su 7cd7a2f0: bot APPROVATO CON RISERVE (V-1 BASSA, V-2/V-3 COSMETICHE, chiuse da b0174be5), verifica esterna APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/388#issuecomment-7042376753). Le riserve aperte sono solo BASSE/COSMETICHE; senza un verdetto del bot pulito sul nuovo head serve il sì dell'operatore in chat (CLAUDE.md §10).
2. Password delle copie cifrate nel `.env` del Mac (`GAS_CRM_BACKUP_PASSWORD`), salvata anche nel gestore di password; poi `pip install -r requirements.txt`.
3. Verificare che la cartella di Gas sia `~/Gas`, fuori da Scrivania e Documenti sincronizzate con iCloud.
4. Secondo passaggio nella chat claude.ai col link della PR #387 e di questa PR (riservatezza delle copie dei clienti).

---

## §1 SCOPE & ESITO FETTE

- **PR #387**: MERGIATA il 20-11 (d03e5bf2) col via dell'operatore: CI verde, bot e verifica esterna (https://github.com/Gasss23/Gas/pull/387#issuecomment-7041110550) APPROVATO CON RISERVE senza ALTA/MEDIA.
- **Fetta 8a — note basse su d809f5f1** (bot V-1 ripristino interrotto in chiaro, bot V-2 motivo «disco non collegato?» per una cartella mai creata, verifica esterna V-2 testo a copia spenta): FATTA, commit d62adafb. Review #824 APPROVATO CON RISERVE (R-824-1 BASSA, R-824-2 COSMETICA), corrette nello stesso diff e riviste in #825 APPROVATO CON RISERVE (R-825-1 COSMETICA, R-825-2 BASSA).
- **Fetta 8b — R-825-1 e R-825-2**: FATTA, commit a9dbf6be. Review #826 BOCCIATO (R-826-1 MEDIA: con una cartella senza «/» le copie finivano nella cartella di lavoro con «ATTIVA» falso), corretto e rivisto in #827 APPROVATO.
- **Fetta 8c — V-1/V-2 BASSE del bot su #388 (0d946f08)**: FATTA, commit a565c7b6. Review #828 APPROVATO CON RISERVE (R-828-1 BASSA, R-828-2 COSMETICA), corrette nello stesso diff e riviste in #829 APPROVATO CON RISERVE (R-829-1 COSMETICA).
  - V-1: con iCloud Drive negato da macOS il motivo dice cosa fare (avvio, prova, copia del guardiano).
  - V-2: il temporaneo in chiaro di un ripristino interrotto viene tolto anche se la destinazione esiste già.
- **Fetta 8d — note del bot su 7cd7a2f0**: FATTA, commit b0174be5. Review #830 APPROVATO CON RISERVE (R-830-1 BASSA).
  - V-1: resti in chiaro più vecchi di un'ora tolti qualunque PID (riavvio); guida aggiornata.
  - V-2: `_consiglio_icloud` col percorso risolto e casefold. V-3 (= R-829-1): test del disco pieno.
- **Merge di main (PR #389) nel ramo**: FATTO, commit 7d6a6865. Review #833 APPROVATO: codice del CRM identico a cfa0156a, `scripts/bot_esito.py` e il suo test identici a main, conflitti dei report risolti per unione.
- **Non fatte (note del bot e della verifica esterna, BASSE/COSMETICHE):** verifica esterna V-4 (il thread della prova, dopo il tempo massimo, resta vivo: innocuo) — DEFERITA, cosmetica.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  14 +++++++++++
 modules/crm/copia_cifrata.py       | 102 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 modules/crm/server.py              |  25 +++++++++++++++-----
 reports/crm/guida.md               |   4 ++--
 reports/diff_sessione.md           |  17 ++++++++++----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  39 ++++++++++++++++++++++---------
 tests/test_unit_crm.py             | 167 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base della sessione: 09e112f5 (origin/main dopo il merge della PR #389, entrato nel ramo col merge 7d6a6865); i file della #389 escono quindi dal diff.

## §3 GIT LOG --ONELINE (sessione)

```
7d6a6865 Merge origin/main (PR #389, correzione del bot) nel ramo della PR #388 — review #833 APPROVATO
cfa0156a docs(fine-task): CRM fetta 8 — note del bot su 7cd7a2f0 chiuse (review #830); guida sui resti dei ripristini
b0174be5 fix(crm): resti in chiaro di ripristini interrotti tolti anche dopo un riavvio (più vecchi di un'ora); consiglio su iCloud anche via collegamento o con maiuscole diverse; test del disco pieno (note del bot su #388) — review #830 APPROVATO CON RISERVE
cf6a897c chore(revisore): memoria review #830 — APPROVATO CON RISERVE
7cd7a2f0 docs(fine-task): CRM fetta 8 — note basse del bot su #388 chiuse (review #828, #829)
a565c7b6 fix(crm): iCloud Drive negato da macOS dà un motivo che dice cosa fare; ripristino interrotto pulito anche se la destinazione esiste già (V-1/V-2 BASSE del bot su #388) — review #828 e #829 APPROVATO CON RISERVE
19f5fe2d chore(revisore): memoria review #829 — APPROVATO CON RISERVE
ab5d5f81 chore(revisore): memoria review #828 — APPROVATO CON RISERVE
0d946f08 docs(fine-task): handoff — PR #388 aperta con l'etichetta verifica
538a8948 docs(fine-task): CRM fetta 8 — note basse sulla PR #387 chiuse (review #824–#827); PR #387 mergiata
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

### Review #828-CRM (diff poi committato in a565c7b6, con le correzioni riviste in #829)

## VERDETTO: APPROVATO CON RISERVE

Review #828-CRM del diff staged (2 file, +19/−2, sopra 0d946f08). Ho letto prima CLAUDE.md (sez. 1, 5, 8, 9), reports/stato_progetto.md (la parte sul CRM, fette 6-8) e la mia memoria (lezioni #815–#827). L'albero di lavoro è identico all'indice per entrambi i file.

**Elementi del diff esaminati**

- `modules/crm/copia_cifrata.py:148` — se `is_dir` sulla cartella di iCloud solleva OSError e quella cartella contiene la cartella delle copie, il motivo dice «iCloud Drive non è leggibile … dai a Terminale l'accesso … oppure imposta GAS_CRM_BACKUP_CIFRATO_DIR».
  - Rischio esaminato: che il nuovo ramo possa sollevare, contro il «Mai solleva» di `_genitore_assente`; che finiscano percorsi o dati nel motivo; che il confronto funzioni con `ICLOUD_DRIVE` cambiato nei test.
  - Il confronto fra Path non solleva. Il motivo non contiene nessun percorso. Il test va in rosso con la copia_cifrata di HEAD.
  - Esito: ok, con R-828-1 e R-828-2 (sotto).
- `modules/crm/copia_cifrata.py:357` — `_pulisci_ripristini_interrotti(dest)` è ora la prima cosa di `ripristina`, prima di ogni rifiuto e prima di `decifra`.
  - Rischio esaminato: l'ordine diverso rispetto a #824, cioè una pulizia anche con la password sbagliata; un'eccezione della pulizia che uscirebbe prima; la perdita di dati unici.
  - Provato su 3.12 e 3.13 (su 3.11 la libreria cryptography di sistema non si carica in questo ambiente):
    - con la password sbagliata il resto morto viene tolto ed esce ErroreCRM;
    - col segnaposto `.icloud` il resto viene tolto;
    - con dest esistente e un resto collegato a dest, il resto sparisce e dest resta integro (`_integro` True);
    - il resto di un processo vivo resta;
    - dest in una cartella che non esiste, «.» e «/» danno solo ErroreCRM.
  - La pulizia tocca solo temporanei in chiaro di processi morti. La copia cifrata di partenza non si tocca mai, quindi niente di unico va perso. Concordo che sia accettabile.
  - Esito: ok.
- `modules/crm/copia_cifrata.py:303` (contesto, file del diff) — il filtro della pulizia è invariato: PID solo [0-9]{1,10}, OverflowError trattato come vivo, mai collegamenti simbolici.
  - Rischio: ora gira su più chiamate. Il caso già noto di un PID visto come morto da un altro spazio di processi (container) scatta più spesso, ma resta marginale.
  - Esito: ok.
- `tests/test_unit_crm.py:1834` — collega dest al nome di un resto (PID 999999996, morto su Linux e su macOS), poi «esiste già» e il controllo che il resto sia sparito e dest no. Il test morde: con la copia_cifrata di HEAD fallisce.
  - Esito: ok.
- `tests/test_unit_crm.py:1897` — controlla il motivo di iCloud e la variabile suggerita. Morde come sopra.
  - Esito: ok.
- `modules/crm/__main__.py:206` (contesto) — senza `--dest` la destinazione è il DB vero. La pulizia gira quindi nella cartella del repo, solo sui nomi `.gas_memory_crm.db.<pid>-<tid>.ripristino.tmp`.
  - Esito: ok.

**Verifiche rifatte da me**

- Suite CRM sull'albero dell'indice: 138 passed.
- Con la copia_cifrata.py di HEAD e i test nuovi: 2 failed / 136 passed. Falliscono `test_v1_bot387b_ripristino_interrotto_non_resta_in_chiaro` e `test_r825_2_cartella_non_valida_o_icloud_negato_il_crm_parte`.
- mypy: 0 errori in modules/crm. I 78 errori segnalati stanno in altri file importati e c'erano già.
- Il kernel non è toccato: il test di round-trip agentico (§7) non serve. Nessuno slicing della history, nessuna simulazione di tool.

**Riserve**

- **R-828-1 BASSA** — il motivo nuovo compare solo se fallisce lo stat della cartella di iCloud. Se macOS lascia passare lo stat e nega la scrittura (di solito i permessi di macOS sulle cartelle protette fanno così; non verificato su un Mac), il messaggio resta generico:
  - all'avvio: «la cartella … non si può scrivere (PermissionError)» (`modules/crm/copia_cifrata.py:174`);
  - nel guardiano: «copia cifrata non riuscita (PermissionError)».
  - L'ho provato simulando un `mkdir` negato sotto iCloud.
  - Rimedio proposto: lo stesso suggerimento nei rami d'eccezione di `prova_scrittura` e `copia_fuori` quando l'errore è PermissionError e la cartella sta dentro `ICLOUD_DRIVE`.
- **R-828-2 COSMETICA** — se GAS_CRM_BACKUP_CIFRATO_DIR punta già a una cartella dentro iCloud Drive, il motivo dice comunque «oppure imposta GAS_CRM_BACKUP_CIFRATO_DIR». Provato.

**Rischio escluso esplicitamente**

Non ho verificato il comportamento reale dei permessi di macOS su `~/Library/Mobile Documents/com~apple~CloudDocs`, cioè se nega lo stat della cartella o solo il contenuto e la scrittura. Non si può riprodurre nel container Linux. Non ho verificato nemmeno se l'app da autorizzare sia davvero «Terminale» quando il CRM parte da un altro terminale (iTerm o simili). Su 3.11 non ho rifatto le prove a mano, per la libreria cryptography di sistema rotta in questo ambiente.

**Memoria del revisore**

- Ho aggiunto la riga `#828-CRM — 2026-11-20 — APPROVATO CON RISERVE — …` e una lezione nuova (il suggerimento legato a un solo ramo d'eccezione) in /home/user/Gas/.claude/agents/memoria_revisore.md.
- L'ho committata con `bash scripts/commit_memoria_revisore.sh`: commit ab5d5f81, solo quel file. HEAD ora è ab5d5f81 e non più 0d946f08.
- Il diff staged è intatto (2 file, +19/−2). Non ho creato `.claude/.review_ok` e non ho committato il diff.

Le riserve R-828-1 e R-828-2 vanno registrate in reports/stato_progetto.md prima del commit.

### Review #829-CRM (commit a565c7b6)

## VERDETTO: APPROVATO CON RISERVE

Review #829-CRM del diff staged (2 file, +65/−4, sopra ab5d5f81). Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), le righe del CRM in reports/stato_progetto.md e la coda della mia memoria (#821–#828 e le relative lezioni).

**Elementi del diff esaminati**
- `modules/crm/copia_cifrata.py:119`: la nuova `_consiglio_icloud` restituisce None se l'errore non è un PermissionError o se la cartella non è dentro `ICLOUD_DRIVE`. Rischi esaminati: che sollevi un'eccezione (no: il confronto è sul percorso scritto, dentro un try) e che dia il consiglio anche fuori da iCloud (no: il mutante «ogni percorso» fa fallire un test). Esito: ok.
- `modules/crm/copia_cifrata.py:128`: R-828-2, la frase «oppure imposta» compare solo se la variabile non è impostata, con la stessa lettura di `cartella()` (strip). Senza la condizione il test fallisce. Esito: ok.
- `modules/crm/copia_cifrata.py:166`: ramo d'eccezione di `_genitore_assente`, ora solo per PermissionError (prima per ogni OSError). Rischio: perdere il consiglio quando is_dir solleva. Non succede: senza la chiamata un test fallisce. Esito: ok.
- `modules/crm/copia_cifrata.py:191` e `modules/crm/copia_cifrata.py:285`: consiglio nella prova all'avvio e nella copia del guardiano, quindi R-828-1 è chiusa. Rischio: che la scrittura negata non arrivi al ramo. Esito: ok.
  - Togliendo il consiglio da una delle due chiamate, un test fallisce.
  - Prova reale come utente nobody, con permesso negato vero dal sistema e cartella di iCloud finta: sia con la cartella senza scrittura (0555) sia con la cartella delle copie già esistente in sola lettura. Su 3.12 e 3.13 l'avvio, la copia e la prova con la variabile impostata danno il consiglio; una cartella fuori da iCloud dà il motivo generico.
  - Nel log resta solo il tipo dell'errore. Il testo va anche nell'avviso Telegram (`modules/crm/server.py:289`), ma non contiene dati dei clienti.
- `modules/crm/copia_cifrata.py:376`: la pulizia dei ripristini interrotti è già approvata in #828 e non è cambiata. Il test `tests/test_unit_crm.py:1832` funziona (PID 999999996 morto, `dest` intatto). Esito: ok.
- `tests/test_unit_crm.py:1907`: mkdir negato sotto la cartella di iCloud finta, poi variabile impostata (`tests/test_unit_crm.py:1918`). Alla fine (`tests/test_unit_crm.py:1923`) `ICLOUD_DRIVE` resta quella finta, ma `is_dir_negato` la legge dal modulo al momento, quindi la parte finale prova ancora il permesso negato. Esito: ok.

**Riserva**
- **R-829-1 COSMETICA**: il restringimento «solo PermissionError» (`modules/crm/copia_cifrata.py:124`) non ha test. Col mutante «ogni eccezione» la suite resta a 138 passed: per esempio un disco pieno su iCloud direbbe «dai all'app l'accesso ai file». Rimedio: un caso con OSError(ENOSPC) o TimeoutError sotto la cartella di iCloud finta, che pretenda il motivo generico.

**Verifiche rieseguite**
- Suite CRM: 138 passed sull'albero dell'indice (Python 3.13).
- Mutanti: senza consiglio nella prova, nella copia o nel ramo del genitore, «oppure» fisso, ogni percorso: 1 failed ciascuno. Il mutante «ogni eccezione» passa: è R-829-1.
- mypy: 0 errori in modules/crm.
- Non ho rifatto il confronto con l'indice di #828 (non è salvato). I mutanti coprono la stessa prova.

**Note non classificate (già presenti, non vengono da questo diff)**
- Il confronto con `ICLOUD_DRIVE` guarda il percorso così com'è scritto. Una variabile scritta con maiuscole diverse o passando da un collegamento simbolico riceve il motivo generico. Il percorso predefinito corrisponde sempre.
- Con la libreria cryptography rotta (il Python 3.11 di questo container, dove manca `_cffi_backend`), pyo3 solleva un PanicException, che non è un Exception: esce da `copia_fuori`. È un difetto dell'installazione del container, non del Mac.

**Rischi esplicitamente esclusi**
- Il comportamento vero dei permessi di macOS non è verificato perché non si riproduce su Linux: non so se nega lo stat o la scrittura, se l'errore è EPERM o EACCES, né se la voce in Impostazioni di Sistema si chiama così. L'ho simulato con monkeypatch e con un EACCES vero come nobody.
- Python 3.14 non è installato: non ho verificato se lì `Path.is_dir` smette di sollevare e quindi il ramo di `_genitore_assente` cambia motivo.
- La prova reale su 3.11 non si fa: nel container manca un cryptography funzionante per 3.11.

**Memoria**
- Aggiunta la riga #829-CRM e una lezione nuova: quando un diff restringe una condizione serve un test del caso escluso.
- Committata con `scripts/commit_memoria_revisore.sh` (commit 19f5fe2d).
- Il diff staged è intatto: non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #830-CRM (commit b0174be5)

## VERDETTO: APPROVATO CON RISERVE

Review #830-CRM. Diff staged di 3 file (+44/−4) sopra 7cd7a2f0, PR #388. SHA-256 del diff staged: 501ebdea9c033ddfb713925610507439f946bc74b7059840a2d43ad2dc92ccad.

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la voce «CRM fetta 6-8» di reports/stato_progetto.md e la coda della memoria del revisore (fino a #829-CRM, comprese le lezioni su PID, restringimenti e test che mordono).

**Elementi del diff esaminati**
1. `modules/crm/copia_cifrata.py:345`: il controllo «è un collegamento simbolico» viene ora prima di tutto, prima di stat e del PID. Rischio: che l'età letta tramite il collegamento faccia togliere un link o il suo bersaglio. Esito: ok. Tolto questo controllo, il test va in rosso. Nella mia prova su 3.11, 3.12 e 3.13 il link vecchio resta e il bersaglio non viene toccato.
2. `modules/crm/copia_cifrata.py:347`: un resto più vecchio di TMP_VECCHIO_S (1 h) viene tolto qualunque sia il PID. Rischio: togliere il temporaneo di un ripristino ancora in corso. Esito: ok. Il temporaneo nasce con O_EXCL (mtime = adesso) e dopo la creazione restano solo `_integro` e `os.link`, cioè secondi. L'unica finestra è un Mac sospeso a metà ripristino con un secondo ripristino lanciato in parallelo. Anche lì niente danni: `os.link` dà FileNotFoundError, il codice ripiega sulla scrittura esclusiva dai dati in memoria e poi ricontrolla `_integro(dest)`. Mie prove: resto vecchio col PID 1 tolto; resto recente col PID 1 lasciato; mtime nel futuro lasciato (si decide col PID, come prima); hard link vecchio verso il database tolto, con `dest` intatto; una cartella con quel nome lasciata, senza eccezioni.
3. `modules/crm/copia_cifrata.py:128` (confronto a `modules/crm/copia_cifrata.py:130`): `_consiglio_icloud` confronta i percorsi risolti, componente per componente, senza badare alle maiuscole. Rischio: falsi positivi per prefisso di stringa, eccezioni da realpath. Esito: ok. «icloud2/copie» dà None; un byte nullo dà None (finisce nell'except §9); `..` viene normalizzato. Ho provato un link verso iCloud con lstat negato dentro la cartella: il consiglio compare su 3.11, 3.12 e 3.13, perché il realpath non stretto ignora gli OSError. La lista tagliata qui è quella delle parti del percorso, non la cronologia: nessun antipattern.
4. `tests/test_unit_crm.py:1944`, `tests/test_unit_crm.py:1949`, `tests/test_unit_crm.py:1950`: il caso ENOSPC (V-3, R-829-1), il collegamento e le maiuscole. Rischio: test che non mordono (lezione #825). Esito: ok. Ogni mutante manda in rosso un test: senza il controllo PermissionError, senza casefold, senza realpath, con «vecchio» sempre falso o sempre vero, senza is_symlink. Sopravvive solo il mutante senza `pid == os.getpid()`, ed è equivalente: `_processo_vivo(getpid)` dà già True.
5. Prove rifatte da me: suite CRM 138 passed. Con la copia_cifrata di 7cd7a2f0 e i test nuovi: 2 failed / 136 passed. mypy: 0 errori in modules/crm. Nessuna riga oltre i 100 caratteri, `--check` pulito.

**Riserve**
- **R-830-1 BASSA**: resta una parte della V-1. Caso: Mac spento a metà ripristino, riavvio, nuovo tentativo ENTRO un'ora, e il vecchio PID ora appartiene a un processo vivo. Il resto in chiaro rimane anche dopo un ripristino riuscito, e nessun ripristino successivo lo toglierà più. Il comportamento è voluto e il test stesso lo fissa (`tests/test_unit_crm.py:1841`, `vivo.exists()`). La guida però promette «lo toglie il ripristino successivo nello stesso posto» (`reports/crm/guida.md:32`), e proprio nel caso che nomina («Mac spento a metà», riprovo subito, magari su un Mac nuovo appena acceso). Rimedio a scelta:
  - (a) considerare morto ogni resto con mtime anteriore all'avvio del sistema;
  - (b) almeno scrivere nella guida «se dopo il ripristino il file c'è ancora, cancellalo a mano».

  Il danno è limitato: il file è 0600, sta sul Mac e contiene gli stessi dati del database accanto. È della stessa famiglia di R-808-6 (copie con dati completi).

**Rischio escluso esplicitamente**
- Non ho verificato su un Mac vero quanto spesso un PID viene riusato dopo il riavvio, né il comportamento reale di TCC (i permessi di macOS) su lstat e realpath dentro iCloud Drive: non si riproduce in un container Linux. I permessi negati li ho simulati con un lstat finto e come utente nobody.
- Non ho rieseguito la suite del kernel: il diff non tocca gas.py né brains/.

**Note per l'agente principale**
- Memoria aggiornata (riga #830-CRM e una lezione nuova) e committata da sola con `bash scripts/commit_memoria_revisore.sh` (commit cf6a897c). È un commit locale sopra 7cd7a2f0 sul ramo claude/nifty-galileo-3k7kbm, NON pushato. Tienine conto per la regola «non pushare sulla #388 finché non è mergiata»: HEAD adesso è cf6a897c, non più 7cd7a2f0.
- Il diff staged è intatto dopo il commit della memoria (stesso SHA qui sopra). `.claude/.review_ok` non creato, diff non committato.
- In stato_progetto vanno segnate R-829-1 chiusa e R-830-1 aperta.

### Review #833-MERGE (commit 7d6a6865)

## VERDETTO: APPROVATO

Review #833-MERGE: merge in corso di origin/main 09e112f5 (merge della PR #389) nel ramo `claude/nifty-galileo-3k7kbm`, con HEAD cfa0156a (PR #388) e base comune d03e5bf2. Prima della review ho letto CLAUDE.md (sezione 5), `reports/stato_progetto.md` e la mia memoria. Ho applicato la lezione del 2026-11-19: dopo il merge i file arrivati da main escono dal diff della sessione, quindi le citazioni di file del diff sono di codice del ramo.

**Elementi esaminati**
- `modules/crm/copia_cifrata.py:345` — salta i resti del ripristino che sono collegamenti simbolici (codice della review #830). Rischio: il merge altera il codice CRM del ramo. Il blob è identico a HEAD nell'indice (9f87484f42) ed è diverso da main, quindi è la versione del ramo. Esito: ok.
- `modules/crm/copia_cifrata.py:128` — confronta il percorso risolto senza badare a maiuscole in `_consiglio_icloud`. Rischio come sopra. È identico a HEAD. Lo stesso vale per `modules/crm/server.py` (c3b6984745) e `reports/crm/guida.md`. Esito: ok.
- `tests/test_unit_crm.py:1944` — test del disco pieno (ENOSPC, nessun consiglio su iCloud). Rischio: test del ramo persi o mescolati con quelli di main. Il blob è identico a HEAD (36129da12a). Esito: ok.
- Contesto: `scripts/bot_esito.py:180` — la regola che riconosce «non» e «Non» (`\b[Nn]on`) davanti a una gravità. Rischio: la correzione della #389 alterata nel merge. Blob identico a main: indice = main = aa0d4a497c. Rispetto a HEAD cambiano solo `[Nn]on` e le due righe di commento. Esito: ok.
- Contesto: `tests/test_unit_verifica_bot.py:730` — casi R-831-1 («Non è più così: grave», «Canon grave»). Blob identico a main (edb9ad75fb). Esito: ok.
- Merge in generale: nessun conflitto rimasto (`git ls-files -u` vuoto), nessun marcatore di conflitto nei 7 file coinvolti, `git diff --cached --check` pulito. L'albero di lavoro è uguale all'indice. `handoff.md`, `ultimo_report.md` e `diff_sessione.md` sono identici a HEAD, come dichiarato. `git diff --cached origin/main` tocca solo i 9 file della PR #388, gli stessi che il ramo cambia dalla base. Esito: ok.
- Memoria del revisore: ho rifatto il confronto riga per riga in Python. Il risultato è esatto: base + righe #824–#830 del ramo (13) + righe #831–#832 di main (3) = 1640 righe. Nessuna riga persa da nessuno dei due lati, numerazione in ordine. Esito: ok.
- `reports/stato_progetto.md`: l'indice è uguale a main con la riga CRM del ramo inserita dopo la riga «Bot di verifica…». La riga di main è copiata alla lettera, il resto del file non cambia. Esito: ok.
- Test: ho estratto l'indice in una cartella a parte e lanciato `tests/test_unit_verifica_bot.py` + `tests/test_unit_crm.py`: **768 passed**, come nel tuo conteggio.

**Nota per il fine-task (non è una riserva sul merge)**: la riga del bot in `reports/stato_progetto.md` dice ancora «Corretto … sul ramo `claude/fix-bot-non-maiuscolo`». Dopo il merge va scritto «PR #389 MERGIATA il 20-11 (09e112f5)».

**Rischi esclusi**
- Non ho lanciato la suite completa (kernel, voce, gate), solo i due file di test toccati. Main cambia solo `bot_esito.py`, il suo test e i report; il ramo cambia solo il CRM e i report. Non vedo punti di contatto, ma l'albero unito l'ho provato solo su quei due file.
- Non ho verificato che il bot di verifica, rigirando sul nuovo SHA, dia davvero success. Il controllo lo pubblica la GitHub App e qui non si può riprodurre.

**Riga contatore e commit**
- Ho aggiunto la riga `#833-MERGE — 2026-11-20 — APPROVATO — … Nessuna lezione nuova.` in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- Non ho lanciato `scripts/commit_memoria_revisore.sh`: hai chiesto di non committare, e durante un merge git rifiuta il commit di un solo file (lezione #802).
- La riga è solo nell'albero di lavoro (stato `MM`). Prima del commit del merge va messa in staging con `git add .claude/agents/memoria_revisore.md`, poi `bash scripts/segna_review_ok.sh`: il diff staged cambia, quindi il marcatore va creato dopo.
- Non ho creato `.claude/.review_ok` e non ho committato niente.

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_crm.py`:** 136 su main d03e5bf2 → 137 (d62adafb) → 138 passed (a9dbf6be).
  - d62adafb: `test_v1_bot387b_ripristino_interrotto_non_resta_in_chiaro` nuovo e `test_ve386c_note_del_terzo_giro` aggiornato falliscono sul codice di d809f5f1 (2 failed, 135 passed).
  - a9dbf6be: `test_r825_2_cartella_non_valida_o_icloud_negato_il_crm_parte` nuovo e `test_v1_bot387b…` aggiornato falliscono sul codice di d62adafb (2 failed, 136 passed); il caso a un componente fallisce sul diff bocciato #826 (1 failed, 137 passed).
  - a565c7b6: nessun test nuovo (estesi `test_v1_bot387b…` e `test_r825_2…`); col codice di 0d946f08 falliscono quei 2 (136 passed), con la copia_cifrata approvata in #828 fallisce `test_r825_2…` (137 passed). Totale invariato: 138 passed.
  - b0174be5: estesi `test_v1_bot387b…` e `test_r825_2…`; col codice di 7cd7a2f0 falliscono quei 2 (136 passed). Totale 138 passed.
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.
- **mypy:** 0 errori in `modules/crm`.

## §6 STATO CI

`gh run list` non usato: in questa sessione cloud GitHub si interroga con gli strumenti MCP.
- PR #387 mergiata con CI verde su d809f5f1: unit-suite success e handoff-check success (run 44746651994), verifica-bot neutral (run 44746659372, verdetto APPROVATO CON RISERVE).
- PR #388 su 0d946f08: unit-suite success e handoff-check success (run 44752577700), verifica-bot success (run 44752583500, verdetto APPROVATO CON RISERVE); su 538a8948 verifica-bot annullato (head cambiata).
- Mappatura commit→run:
  - `5e959f65`, `5d83286f`, `d62adafb`, `68e849ed`, `49ea2fb7`, `a9dbf6be`: nessuna run su questi SHA (pushati insieme a 538a8948; l'albero testato è quello di 538a8948).
  - `538a8948`: run CI del push (superata dal push di 0d946f08); verifica-bot annullato.
  - `0d946f08`: run CI 44752577700 (unit-suite success, handoff-check success), verifica-bot 44752583500 success.
  - `ab5d5f81`, `19f5fe2d`, `a565c7b6`: nessuna run su questi SHA (pushati insieme a 7cd7a2f0).
  - `7cd7a2f0`: run CI del push (unit-suite e handoff-check), verifica-bot success (verdetto APPROVATO CON RISERVE); esito finale di unit-suite non letto alla scrittura dell'handoff.
  - `cf6a897c`, `b0174be5`: nessuna run su questi SHA (pushati insieme a cfa0156a).
  - `cfa0156a`: run CI 44757988571 (unit-suite success, handoff-check success); verifica-bot failure (falso positivo «Non bloccante», corretto dalla PR #389).
  - `7d6a6865` (merge di main): run non ancora disponibile alla scrittura dell'handoff. Sarà pushato insieme al commit di fine-task che contiene questo file.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **Rischi non verificabili qui (revisori #825 e #827, non c'è un Mac):** macOS che blocca iCloud Drive (TCC), `os.path.ismount` sui dischi esterni, riuso dei PID dopo un riavvio (il resto viene tenuto: verso sicuro).
- **Limite dichiarato (revisore #825, ridotto in a565c7b6):** il temporaneo in chiaro di un ripristino interrotto viene tolto al ripristino seguente verso la stessa destinazione (ora anche se questa esiste già); con un'altra destinazione resta.
- **Note cosmetiche (revisore #827, non riserve):** il motivo di `_genitore_assente` ripete «nessuna copia fuori dal Mac» dentro l'avviso della copia esterna. La guida ora dice che la cartella deve essere un percorso completo.
- **R-830-1 (BASSA):** dopo un riavvio, con un nuovo ripristino entro un'ora e il vecchio PID riassegnato a un processo vivo, il resto in chiaro rimane; la guida dice di cancellarlo a mano. Stessa famiglia di R-808-6.
- **Note non classificate (revisore #829):** il confronto con `ICLOUD_DRIVE` guarda il percorso scritto (maiuscole diverse o collegamenti simbolici danno il motivo generico); una cryptography rotta che solleva PanicException esce da `copia_fuori` (difetto dell'installazione del container).
- **Verifica esterna #387 V-4 (COSMETICA):** dopo il tempo massimo il thread della prova resta vivo; innocuo.
- **Chiuse in questa sessione:** bot V-1/V-2 e verifica esterna V-2 su d809f5f1; R-824-1, R-824-2, R-825-1, R-825-2, R-826-1, R-826-2; bot V-1/V-2 su 0d946f08 (#388); R-828-1, R-828-2; R-829-1; bot V-1/V-2/V-3 su 7cd7a2f0 (V-1 in parte: vedi R-830-1). Verifica esterna #388 (V-1 CI non conclusa: ora verde su 0d946f08; V-2 strutturale; V-3 = limite chiuso da a565c7b6). La verifica esterna V-1 (il «sì» dell'operatore non verificabile da file) riguarda #387, già mergiata col via dato in chat; V-3 (§6 senza stato CI) è strutturale.
- **Ancora aperte da prima:** R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4 (vedi `reports/stato_progetto.md`).
