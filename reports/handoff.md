# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Mani, fetta 2: `leggi_pagina` più robusta (R6, PR #237)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #237 (https://github.com/Gasss23/Gas/pull/237): l'operatore ha chiesto in chat «mergia quando il bot approva»; l'agente la mergia con `verifica-bot` success, CI verde e nessuna riserva ALTA/MEDIA.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Riferimenti numerici enormi (R-ve235-4)**: `FATTA`
- **DNS limitato (R-ve235-7)**: `FATTA`
- **Cane da guardia senza perdite (R-393-1, R-393-2)**: `FATTA`
- **Finti marcatori con trattini (R-392-3)**: `FATTA` in parte (separatori a tetto; R-410-1 aperta)
- **Test mancanti (R-ve235-6)**: `FATTA`
- **Docstring (R-408-2, R-ve235-5)**: `FATTA`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |    3 ++
 modules/web/leggi.py               |   72 ++++++++++++++++++++-----
 reports/diff_sessione.md           |   15 +++---
 reports/handoff.md                 | 1045 ++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |    6 ++-
 reports/ultimo_report.md           |   52 ++++++++----------
 tests/test_unit_web_leggi.py       |  156 ++++++++++++++++++++++++++++++++++++++++++++++++++++-
 7 files changed, 353 insertions(+), 996 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
c9b3672 Merge origin/main in feat/mani-web-fetta2
53c8066 fix(web): fetta 2 chat Mani — riferimenti enormi, DNS limitato, cane senza perdite, test mancanti
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto). I commit di main portati dal merge non sono della sessione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre verdetti, incollati integralmente: #409 (chat Mani, BOCCIATO), #410 (chat Mani), #428 (chat Mani, merge di main).

### Review #409 (chat Mani)

## VERDETTO: BOCCIATO

Review #409 (chat Mani). Ho esaminato il diff STAGED su feat/mani-web-fetta2: modules/web/leggi.py e tests/test_unit_web_leggi.py. Il worktree coincide con l'index.

**Motivo bloccante**

- **B-409-1 (chat Mani), ALTA: la regex dei finti marcatori è quadratica (ReDoS, cioè una regex che si può far lavorare per ore con un input preparato).**
  - `modules/web/leggi.py:70`: il pattern `_FINTO_MARCATORE` ora inizia con `\[?[\s_-]*` e non ha un prefisso letterale. `_pulisci` compatta solo gli spazi (`" ".join(riga.split())`), non i trattini né i trattini bassi.
  - Con una pagina fatta solo di «-» o di «_», a ogni posizione `[\s_-]*` consuma tutta la sequenza e poi torna indietro carattere per carattere.
  - Tempi misurati (regex vecchia sugli stessi input: 0,002–0,009 s):

    | input | regex nuova | `_pulisci` |
    |---|---|---|
    | 5k «-» | 0,42 s | – |
    | 20k «-» | 6,4 s | – |
    | 40k «-» | 26,7 s | 25,6 s |
    | « - » ripetuto 40k volte | 213 s | – |

  - La regex gira in `modules/web/leggi.py:427`, che sta dopo i 15 s: la pulizia è fuori dal tempo massimo, come dichiara la docstring stessa (R-ve235-5). Una pagina ostile da 2 MB di trattini blocca quindi per ore il thread che chiama, cioè il kernel di Gas. È contro il «zero crash / robustezza» di CLAUDE.md §1/§9 e trasforma un limite dichiarato («qualche secondo al massimo su 2 MB») in un'affermazione falsa.
  - Correzione suggerita, già misurata: separatori limitati, cioè `\[?[\s_-]{0,3}(?:fine[\s_-]{1,3}(?:del[\s_-]{1,3})?)?contenuto[\s_-]{1,3}web[\s_-]{1,3}non[\s_-]{0,3}fidato`.
    - 2 MB di «-», di «_» o di « -» passano in circa 0,3 s.
    - Neutralizza ancora `FINE_CONTENUTO_WEB_NON_FIDATO`, `[fine-del-contenuto-web-non-fidato]` e `[CONTENUTO WEB NON FIDATO`.
    - Aggiungere un test con un tetto di tempo su `_pulisci("-" * 2_000_000)`.

**Riserve (da chiudere nello stesso giro)**

- **R-409-2 (chat Mani), MEDIA: tre test nuovi non mordono.** Ho provato tre mutazioni e la suite resta a 95 passed in tutti e tre i casi.
  - **Semaforo tolto** (acquire e i due release): il test in `tests/test_unit_web_leggi.py:651` resta verde. Le chiamate durano 0,2 s e il DNS finto 1 s, quindi alla fine del ciclo i thread nati nel primo secondo sono già morti e ne restano circa 4–5 vivi anche senza semaforo. Correzione: misurare il massimo dei thread vivi DURANTE il ciclo, oppure tenere il DNS lento più a lungo del ciclo intero.
  - **Niente close nel costruttore fallito del cane da guardia**: il test di `tests/test_unit_web_leggi.py:643` resta verde. `pytest.raises` è senza `as`, quindi l'oggetto costruito a metà viene raccolto e `socket.__del__` chiude il fd prima del conteggio. Correzione: tenere un riferimento (`as info`) oppure intercettare il socket creato.
  - **`_RIF_ZERI` tolto**: il test resta verde. In `tests/test_unit_web_leggi.py:591` la condizione `"A" in r["testo"]` è sempre vera per la «A» di «CONTENUTO WEB NON FIDATO». Inoltre `&#0065;` del test sui riferimenti validi ha solo 4 cifre e html.parser lo gestisce anche senza la regex. Correzione: asserire una stringa distintiva, per esempio «xAy».
- **R-409-3 (chat Mani), BASSA: la regex degli zeri tocca anche i riferimenti decimali.** In `modules/web/leggi.py:78`, `_RIF_ZERI` usa un lookahead esadecimale anche per i riferimenti decimali. `&#00a` e `&#0e9;` diventano i letterali «&#a»/«&#e9;», mentre html darebbe U+FFFD seguito dal testo. Riguarda solo input già non validi, ma contraddice «testo valido inalterato». Correzione: due regex separate, `&#0+(?=[0-9])` per i decimali e `&#([xX])0+(?=[0-9a-fA-F])` per gli esadecimali.

**Elementi del diff esaminati**

- `modules/web/leggi.py:157` — prende il semaforo con timeout pari al tempo rimasto. Rischi esaminati: deadlock, doppio rilascio, `Thread.start` fallito. Esito: **ok**.
  - Il rilascio avviene nel `finally` del thread (`modules/web/leggi.py:167`), oppure in `modules/web/leggi.py:173` se `start` solleva: in quel caso il thread non è mai partito, quindi non c'è doppio rilascio. KeyboardInterrupt non è intercettato da `except Exception`, quindi niente doppio rilascio neanche lì.
  - Semaforo pieno = rifiuto per tempo, come dichiarato.
  - Limite: 4 DNS bloccati bloccano tutte le letture finché il resolver di sistema non va in timeout. È un compromesso dichiarato nella docstring; il messaggio «tempo massimo superato» qui è impreciso (nota cosmetica).
  - Nota cosmetica: il costruttore `threading.Thread(...)` sta fuori dal try, quindi un suo fallimento (improbabile) perderebbe un permesso.
- `modules/web/leggi.py:450` — applica `_RIF_ZERI` e poi `_RIF_ENORME` prima del parser. Rischi esaminati: ReDoS e testo valido alterato. Esito: **ok con la riserva R-409-3**.
  - Sonda contro `html.unescape` su `&#0065;`, `&#x0041;`, `&#X00041`, `&#000;`, `&#0001114111;`, `&#01114112;`, `&#x0010FFFF;`, `&#x00110000;`, `&#99999999`, `&amp;#0065;`, `&#0x41;`: semantica identica.
  - 2 MB di `&#`, `&#0`, `&#0000…` e `&#x000…g` passano tutti in 0,07 s o meno.
- `modules/web/leggi.py:457` — ripiego senza parser `<[^<>]*>`. Rischio esaminato: tempo quadratico. Esito: **ok**: 2 MB di «<» in 0,03 s e di «<a» in 0,02 s. Nel ripiego script e style restano nel testo; è accettabile perché il testo sta comunque dentro i marcatori NON FIDATO.
- `modules/web/leggi.py:266` — il costruttore del cane chiude la copia del descrittore se il timer fallisce; prima ancora, `os.close(fd)` se `socket.socket(fileno=fd)` fallisce. Esito: **ok nel codice**, test inefficace (R-409-2).
- `modules/web/leggi.py:70` — regex dei finti marcatori. Esito: **blocco** (B-409-1).
- `tests/test_unit_web_leggi.py:682` — certificato autofirmato sul percorso vero. Esito: **ok**: la mutazione `ssl._create_unverified_context()` viene uccisa. openssl è presente, il test non è saltato.
- Altre mutazioni uccise, quindi i test mordono: `ips[-1]` al posto di `ips[0]`, timeout di connessione senza `min(TIMEOUT_CONNESSIONE, …)`, `ferma()` senza close, `_RIF_ENORME` tolto, ripiego tolto, regex vecchia (per le forme con «_»).
- Test: 95 passed su python3 locale (tests/test_unit_web_leggi.py). Nessuno slicing della history né simulazione di tool: il diff non tocca gas.py. Il cap di 10 iterazioni e `_get_window` non sono toccati.

**Rischio escluso:** non ho riprodotto i 95 passed su 3.11 né con rete e DNS veri bloccati, e non ho rimisurato i 2,0 s di tls_lento: mi fido della dichiarazione del chiamante. Non ho verificato il comportamento del resolver di sistema reale con un DNS bloccato (quanto tiene i permessi del semaforo su VPS): con i resolver finti non si riproduce.

**Memoria:** ho aggiunto la riga «#409 (chat Mani) — 2026-10-21 — BOCCIATO — …» con la lezione in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. Il file NON è committato, come mi hai chiesto: non ho lanciato scripts/commit_memoria_revisore.sh. Va committato con il flusso di fine task. Le sonde sono in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/redos.py, /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/mutare.py, /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/mutare2.py, /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rif.py e /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/fix.py.

### Review #410 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Ho fatto le letture obbligatorie: CLAUDE.md (sezioni 5, 8 e 9), reports/stato_progetto.md (la sezione Mani) e la coda di .claude/agents/memoria_revisore.md, con la #409. Il diff staged e il working tree di modules/web/leggi.py sono identici. Ho eseguito di nuovo la web suite: 96 passed su python 3.13.

Ripristino dopo le mutazioni: ho fatto le mutazioni su una copia in working tree e poi ho ripristinato il file. Ho confrontato il file con l'index: è identico.

**Cosa ho esaminato nel diff**
- `modules/web/leggi.py:72` — `_FINTO_MARCATORE` ora ha i separatori limitati, `{0,3}` in testa e `{1,3}` tra le parole. Rischio esaminato: ReDoS (B-409-1). Ho misurato 2 MB di «-», «_», « -», «_-», «fine-», «contenuto-», «fine_del_», «non_» e «contenuto web non »: tutti tra 0,13 e 0,33 s. Ho anche rifatto la mutazione «`*` in testa»: il test a tempo non finisce in 300 s, quindi la regressione si vede. Esito: ok, B-409-1 chiusa.
- `modules/web/leggi.py:72` — Rischio esaminato: varianti dei finti marcatori che il tetto riapre. Ho fatto una sonda su 128 forme con 16 separatori (anche `\n\n`, tab, U+2028/2029, spazi ideografici e spazi non separabili). Tutti gli spazi sono coperti, perché `_pulisci` li compatta a due caratteri al massimo. Esito: riserva R-410-1 (sotto).
- `modules/web/leggi.py:81` — Le tre regex dei riferimenti numerici (`_RIF_ZERI_DEC`, `_RIF_ZERI_HEX`, `_RIF_ENORME`, righe 81-83). Rischio esaminato: un costo quadratico e l'eccezione di html.parser. Ho misurato 2 MB di «&#0», «&#x0» e «&#» ripetuti: al massimo 0,61 s, quasi tutto tempo di html.parser. «&#»+2M zeri e «&#»+2M cifre danno 0,0 s. Ho verificato che 8 cifre decimali o 7 esadecimali, senza zeri iniziali, superano sempre U+10FFFF. Esito: ok.
- `modules/web/leggi.py:464` — La regex del ripiego `<[^<>]*>`. Ho misurato 0,03 s su 2 MB di «<». L'altra regex del modulo, `modules/web/leggi.py:349` (charset), è limitata a `{1,40}` e lavora su un'intestazione. Esito: ok, nel modulo non ci sono altre regex quadratiche.
- `modules/web/leggi.py:161` — Il semaforo del DNS: acquisizione con il tempo che resta, rilascio nel `finally` del thread (`modules/web/leggi.py:171`) e nel ramo in cui il thread non parte (`modules/web/leggi.py:177`). Rischio esaminato: permessi persi. Non ne ho trovati. Esito: ok.
- `modules/web/leggi.py:256` — Il costruttore del cane da guardia: chiude il descrittore se `socket()` fallisce (`modules/web/leggi.py:261`) e chiude la copia se il timer fallisce (`modules/web/leggi.py:270`). Esito: ok, R-393-2 chiusa.
- `tests/test_unit_web_leggi.py:670` — `massimo == MAX_DNS_IN_CORSO`, contato durante il ciclo. Mutazione «semaforo tolto»: 1 FAIL. Rischio esaminato: il thread residuo del test a `tests/test_unit_web_leggi.py:454` (dorme 2 s) potrebbe falsare il conteggio. Non lo falsa: occupa un permesso ma anche lui si chiama gas-web-dns, quindi il massimo resta 4. Esito: ok.
- `tests/test_unit_web_leggi.py:594` — Il test dei riferimenti validi. Mutazione «ramo esadecimale tolto»: 1 FAIL. Copre anche `&#00a` e `&#0e9;` (R-409-3). Esito: ok.
- `tests/test_unit_web_leggi.py:647` — `pytest.raises(...) as info` tiene vivo l'oggetto a metà. Esito: ok. Ho preso per buona la mutazione «close nel costruttore tolto» riportata da te; io non l'ho rifatta.

**Riserve**
- **R-410-1 (chat Mani), BASSA.** Il tetto `{1,3}` sui separatori tra le parole non serviva per il ReDoS. Lì la ripetizione viene dopo una parola fissa e il costo è lineare. Ho misurato la variante `\[?[\s_-]{0,3}(?:fine[\s_-]+(?:del[\s_-]+)?)?contenuto[\s_-]+web[\s_-]+non[\s_-]*fidato`: 0,47 s su 2 MB di «fine»+«-», 0,39 s su `("non"+"-"*50)*40000`. Il tetto fa invece perdere 8 forme che HEAD neutralizzava: «CONTENUTO WEB NON____FIDATO», «NON - - FIDATO», «NON_-_-_FIDATO», «NON----------FIDATO», ciascuna anche con «FINE DEL». La variante con `+` ne coprirebbe altre 16, nuove anche rispetto a HEAD (per esempio «CONTENUTO____WEB»). La difesa vera resta il codice casuale (R-392-3), quindi non è un blocco. Proposta: limitare solo il prefisso in testa e lasciare `+`/`*` dopo le parole fisse.
- **R-410-2 (chat Mani), COSMETICA.** `tests/test_unit_web_leggi.py:676`: se la regex torna quadratica, il test blocca la suite (ore su 1 M di caratteri) invece di fallire, perché misura il tempo solo a fine chiamata. Morde, ma solo con il timeout del job CI. Si potrebbe eseguire `_pulisci` in un thread o sottoprocesso con `join(3)`.

**Cosa NON ho verificato**
- Non ho rifatto la suite su python 3.11 né l'esecuzione con rete e DNS veri bloccati: mi fido del tuo dato, perché il codice usa solo funzioni presenti in entrambe le versioni.
- Non ho misurato quanto dura davvero il resolver di sistema sulla VPS. Il blocco della funzione quando 4 risoluzioni restano appese è un limite dichiarato (R-ve235-7) e non si può riprodurre in sviluppo.
- La riga di html.parser su 2 MB di «<» (2,1 s) è un costo che esisteva già, dentro R-ve235-5: non l'ho trattata qui.

**Memoria**
Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga «#410 (chat Mani) — 2026-10-21 — APPROVATO CON RISERVE — …», con la lezione: il tetto anti-ReDoS va messo solo dove la ripetizione non è legata a una parola fissa. Come mi hai chiesto NON ho committato, quindi non ho eseguito scripts/commit_memoria_revisore.sh. Il file ora risulta `MM`: la riga #410 è nel working tree ma non è nello staging, quindi va aggiunta con `git add` prima di `segna_review_ok.sh`, perché l'hash del diff staged cambia. Le riserve R-410-1 e R-410-2 vanno tracciate in stato_progetto.md.

### Review #428 (chat Mani)

## VERDETTO: APPROVATO

Review #428 (chat Mani): merge di origin/main 35b55be (59 commit della chat Motore) nel ramo feat/mani-web-fetta2 (HEAD 53c8066, merge-base 0616d3a). Letture obbligatorie fatte: CLAUDE.md, reports/stato_progetto.md (la parte su Mani e R6), coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `modules/web/leggi.py:72`: regex `_FINTO_MARCATORE` della fetta 2, con separatori limitati (correzione della B-409-1). Ho controllato che il merge non l'abbia alterata: `git diff --cached origin/main -- modules/web/leggi.py` è identico byte per byte a `git diff 0616d3a HEAD` (escluse le righe `index`). Esito: ok.
- `modules/web/leggi.py:154`: semaforo `_DNS_IN_CORSO` e costante nuova `MAX_DNS_IN_CORSO`. Ho controllato che la fetta 2 non cambi l'interfaccia pubblica. La firma di `leggi_pagina` è invariata e le chiavi del dict restituito non sono toccate. `modules/web/__init__.py` non cambia. Esito: ok.
- `tests/test_unit_web_leggi.py:656` e `tests/test_unit_web_leggi.py:676`: test del DNS lento e test a tempo coi trattini. Ho controllato che il diff contro main sia uguale a quello del ramo e che non ci siano collisioni con i test di main. Diff identico, `pytest --co -q tests` raccoglie 1807 test senza errori. Esito: ok.
- `.claude/agents/memoria_revisore.md:673-674`: #409 e #410 (chat Mani), inserite dopo #408 (chat Mani) alla `.claude/agents/memoria_revisore.md:672` e prima di #427 (chat Motore). Ho cercato righe perse o duplicate e marcatori rimasti. La versione staged ha 675 righe: le 673 di main più 2. Nessuna riga di HEAD o di main manca. Nessun duplicato e nessuna riga nuova estranea. Nessun `<<<<<<<`, `=======` o `>>>>>>>`. Copia di lavoro uguale all'index. Esito: ok.
- Contesto `.github/workflows/ci.yml:117`: il passo della web suite (`tests/test_unit_web_*.py`) è ancora nel job `unit-suite` dopo il merge. Esito: ok.

**Punto 1, perimetro.** `git diff --cached origin/main --stat` mostra solo 3 file: `modules/web/leggi.py` (+58/-14), `tests/test_unit_web_leggi.py` (+155/-1) e la memoria (+2). Gli altri file staged (gas.py, gate, store, notte, tests kernel/gate/notte, reports/) arrivano interi da main: MERGE_HEAD coincide con origin/main.

**Punto 3, chiamanti.** `git grep` su origin/main trova `leggi_pagina` e `modules.web` solo in `modules/web/` stessi, in `tests/test_unit_web_leggi.py` e nel commento di ci.yml. La chat Motore non ha ancora agganciato `leggi_pagina`. Da 0616d3a main non tocca nessun file di `modules/web/`. Le modifiche della fetta 2 non possono rompere niente su main.

**Suite sull'albero fuso**
- web: 96 passed
- gate + notte: 947 passed
- kernel (`python tests/test_unit_kernel.py`): 966 PASS, 1 FAIL (T31g, vector store). Lo stesso test fallisce allo stesso modo su origin/main pulito, rilanciato in un worktree separato: in questo ambiente manca `sqlite_vec`. Non è colpa del merge.

**Rischio escluso**: non ho rilanciato hooks, handoff_check, gasmerge e voice. Main non li ha toccati da 0616d3a, tranne la suite kernel/gate/notte, che ho lanciato. Non ho verificato la CI reale su GitHub (non riproducibile qui) né il comportamento su VPS o Mac.

**Nota fuori dal perimetro del merge, per /fine-task**: lo `reports/stato_progetto.md` staged è quello di main. Non contiene ancora la fetta 2 Mani né le riserve aperte R-410-1 (BASSA) e R-410-2 (COSMETICA), che vanno aggiunte a fine task.

**Memoria**: aggiunta la riga «#428 (chat Mani) — 2026-10-21 — APPROVATO — …» in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. Non è committata né messa in staging (stato `MM`), come richiesto. Se la riga deve finire nel commit di merge, va fatto `git add` del file. Nessuna lezione nuova.

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 85 → 96 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «96 passed», Python 3.13.16 e 3.11.17; 96 passed anche con rete e DNS veri bloccati via sitecustomize).
- Mutazioni sui test nuovi: semaforo tolto 1 FAIL, close nel costruttore tolto 1 FAIL, regex degli zeri tolta 2 FAIL, regex dei trattini vecchia 2 FAIL.
- Sull'albero fuso (review #428): gate + notte 947 passed; kernel 966 PASS / 1 FAIL (T31g: manca `sqlite_vec` in questo ambiente, fallisce uguale su origin/main pulito).

## §6 STATO CI

- `53c8066`: pushato da solo prima del merge di main; run CI di push non verificata in questa sessione.
- `c9b3672` (merge di main): pushato prima dell'apertura della PR; run non verificata in questa sessione.
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.
- Nota (V-4 verifica esterna #235): sui commit intermedi di una fetta `handoff-check` può essere rosso per costruzione (l'handoff viene aggiornato solo nel commit di fine-task).

## §7 RISERVE APERTE

- Di questa fetta: R-410-1 (BASSA), R-410-2 (COSMETICA), chat Mani.
- Dalla fetta 1, ancora aperte: R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3 (ridotta). Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1» e «Mani — fetta 2».
