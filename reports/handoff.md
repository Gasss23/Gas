# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — Fetta bot: parser del verdetto (#336, #329) e verdetto compresso fra i job (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #337 (https://github.com/Gasss23/Gas/pull/337). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5179453797","url":"https://github.com/Gasss23/Gas/pull/337"}`); `gh` nel cloud non è autenticato. La PR tocca la macchina del bot: il bot darà neutral e il merge lo decide l'operatore (sì per la fetta già dato via M1), secondo CLAUDE.md §10.

---

## §1 SCOPE & ESITO FETTE

- **(a1) Parser — #336 su e619103 letto come MEDIA**: `FATTA` — «read bloccante» nella descrizione di una BASSA; `_BLOCCANTE_TECNICO` ristretto ai termini di sistema.
- **(a2) Parser — #329 su 7957a15 letto «ambiguo» (3 nov)**: `FATTA` — causa vera: la prosa «- Verifica esterna su 3b92254: …» presa per titolo; il «R-615-4 (MEDIA, preesistente)» era già gestito (R-161-1). `_CITAZIONE_VERIFICA_PASSATA` a lista bianca.
- **(b) Verdetto scartato da GitHub perché contiene il valore di un secret (#335)**: `FATTA` — gzip+base64 fra i job, `leggi_verdetto()`.
- **Rilancio del bot sulla #335 e merge**: `DEFERITA — dopo il merge della #337` (il workflow gira in pull_request_target dalla versione di main).
- **C1, profilo voce, sottofondo**: `DEFERITE — ordine di M1, dopo questa fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md               |   8 ++++++++
 .github/workflows/verifica-bot.yml               |  18 ++++++++++++------
 reports/diff_sessione.md                         |  16 ++++++++--------
 reports/handoff.md                               | n/d
 reports/ripartenza_m2.md                         |   7 ++++---
 reports/stato_progetto.md                        |   3 ++-
 reports/ultimo_report.md                         |  29 ++++++++++++-----------------
 scripts/bot_esito.py                             |  62 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 tests/dati_verifica_bot/verdetto_329_7957a15.txt |  42 ++++++++++++++++++++++++++++++++++++++++++
 tests/dati_verifica_bot/verdetto_336_e619103.txt |  30 ++++++++++++++++++++++++++++++
 tests/test_unit_verifica_bot.py                  | 179 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
fcbb8b4 fix(bot): parser del verdetto (#336 «read bloccante», #329 «Verifica esterna su …») e verdetto compresso fra i job (chat M2)
52653ed chore(revisore): memoria review #673 — APPROVATO
20b2302 chore(revisore): memoria review #673 — APPROVATO CON RISERVE
11643d6 chore(revisore): memoria review #672 — BOCCIATO
0033771 chore(revisore): memoria review #671 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit fcbb8b4 è passato da quattro review sul diff staged (ciascuna sul diff di quel momento; le citazioni path:riga si riferiscono a quella versione).

Review #671-M2 sul primo diff staged (verdetto integrale):

## VERDETTO: BOCCIATO

Review #671-M2: diff in stage su feat/bot-verdetto-m2, base 942e665. Riguarda 5 file: scripts/bot_esito.py, .github/workflows/verifica-bot.yml, i test e due file di dati. Ho preso la versione di HEAD in una copia di prova e ho confrontato vecchio e nuovo parser sugli stessi testi. In 6 casi un verdetto che prima diventava COMMENT (NO) ora diventa APPROVE. Sono proprio l'allentamento che questa fetta non doveva introdurre.

**Elementi del diff esaminati**

- `scripts/bot_esito.py:101` — nuovo `_RIGA_TITOLO`. Una riga scritta in minuscolo conta come titolo solo se dopo «verifica esterna» (ed eventualmente «#N») arriva subito un separatore o una parola di esito. Rischio esaminato: un titolo di NO che non viene più riconosciuto. Esito: **blocco (R-671-1-M2, ALTA)**. Questi testi stanno sotto il titolo canonico «VERIFICA ESTERNA #5 — APPROVATO CON RISERVE», con un V-1 (BASSA). Prima davano COMMENT, ora danno APPROVE:
  - `**Verifica esterna**: BOCCIATO` (il grassetto `**` sta tra le parole e i due punti, e non è nella lista dei separatori)
  - `verifica esterna (seconda lettura) — BOCCIATO`
  - `Verifica esterna, esito: BOCCIATO`
  - `Verifica esterna boccia la PR` («boccia» non corrisponde a «bocciat»)

  Il grassetto in particolare è un formato che un modello produce davvero. Strada suggerita: lasciare fuori solo la forma di #329, cioè una citazione di uno SHA o di un id («su <sha>», «#N:» seguito da elenco V-x). Ogni riga che contiene una parola di esito (approvat, bocciat, boccia, respint, esito, verdetto) resta un titolo. Vanno aggiunti test con i 4 casi sopra.

- `scripts/bot_esito.py:118` — `_BLOCCANTE_TECNICO`, applicata a `scripts/bot_esito.py:216`. Rischio esaminato: omografi che tolgono una gravità vera. Esito: **blocco (R-671-2-M2, MEDIA)**. Con V-1 (BASSA), prima COMMENT e ora APPROVE:
  - «lo giudico io bloccante»: nella lista c'è «io», che in italiano è il pronome.
  - «difetto di processo bloccante per il merge» e «operazione bloccante: va corretto prima del merge»: «processo» e «operazione» sono anche lessico di processo del progetto.
  - Inoltre `\s+` attraversa l'a capo («read\nbloccante» viene tolto).

  Correzione: togliere «io» (resta «i/o»), «processo» e «operazione»; usare `[ \t]+` al posto di `\s+`; aggiungere test negativi.

- `scripts/bot_esito.py:521` — `leggi_verdetto`. Rischio esaminato: bomba di decompressione, troncamenti, testo compresso rotto che ripiega sul testo in chiaro. Esito: **ok**. Il tetto `max_length` sta a `scripts/bot_esito.py:529`, ci sono i controlli su `unconsumed_tail` ed `eof`, base64 usa `validate=True`, un testo compresso rotto dà None (RIPROVA) senza ripiegare sul chiaro, e un JSON che non è un oggetto dà None. I dati in coda dopo il primo blocco gzip vengono ignorati: è innocuo.

- `.github/workflows/verifica-bot.yml:266` — `verdetto_gz` (gzip -9n | base64 -w0) su una sola riga, passato come `VERDETTO_GZ` a `.github/workflows/verifica-bot.yml:336`. Rischio esaminato: troncamento, output vuoto, sicurezza. Esito: **riserva (R-671-3-M2, BASSA)**.
  - La parte tecnica è a posto: con verdetto vuoto si ha RIPROVA, e se la pipe fallisce la decodifica dà None.
  - Ma la compressione aggira anche la rete di sicurezza di GitHub («Skip output … may contain secret»). Un valore di un secret che finisse davvero nel testo ora verrebbe pubblicato nella review, salvo che corrisponda a una delle forme di `_SEGRETO` (sk-ant-, gh*_, github_pat_, -----BEGIN). I secret del job (OAuth sk-ant-, token dell'App ghs_, chiave PEM) rientrano in quelle forme, quindi il rischio è basso. Va però dichiarato nel commento del workflow e in stato_progetto.

- Contesto: `tests/test_unit_verifica_bot.py:1359` — `test_titoli_fuori_formato_restano_ambigui` copre solo le varianti che restano bloccate. Nessuno dei casi di R-671-1 è testato: è per questo che i mutanti dichiarati non hanno visto le regressioni.

Suite eseguita: 545 passed in tests/test_unit_verifica_bot.py (conferma il numero dichiarato). I due testi veri (#336 e #329) passano correttamente.

**Rischi esplicitamente esclusi**

- Non ho verificato quale secret coincidesse con una parola del testo su #335: non è riproducibile in dev e non ho accesso ai log del runner. La diagnosi resta un'affermazione di M2.
- Non ho eseguito il workflow reale su GitHub (il mascheramento delle varianti base64 dei secret e il limite di dimensione degli output dei job non sono verificati).
- Non ho rilanciato le suite hooks, handoff e gasmerge (366 dichiarati).

**Per sbloccare**: correggere R-671-1-M2 e R-671-2-M2 con test che falliscono sul codice attuale, poi chiedere una nuova review. R-671-3-M2 può restare come riserva tracciata.

Memoria aggiornata con la riga #671-M2 più 2 lezioni, committata (0033771, solo .claude/agents/memoria_revisore.md).

File rilevanti:
- /home/user/Gas/scripts/bot_esito.py
- /home/user/Gas/.github/workflows/verifica-bot.yml
- /home/user/Gas/tests/test_unit_verifica_bot.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

Review #672-M2 sul secondo diff staged (verdetto integrale):

## VERDETTO: BOCCIATO

Review #672-M2. Ho esaminato il diff in staging su feat/bot-verdetto-m2 (base 942e665) in una copia dell'indice (`git checkout-index`) e l'ho confrontato con HEAD in una seconda copia. Letture obbligatorie fatte: CLAUDE.md §5, stato_progetto.md (le parti che servono), memoria_revisore.md con la riga #671-M2.

**Riserve di #671 chiuse come chiesto.**
- I 4 casi di #671 danno di nuovo COMMENT. Danno COMMENT anche «Verifica esterna su 3b92254: BOCCIATO» e i test negativi nuovi.
- I due verdetti veri danno APPROVE: #329 (con «R-615-4 (MEDIA, preesistente)» che non blocca) e #336.
- Test: 558 passed sulla copia dell'indice. Su HEAD con i test nuovi: 22 failed, non 21 come dichiarato (R-672-3-M2).

**Il motivo bloccante è nuovo.** L'esenzione di #329 riapre il buco da un'altra parte: è costruita come lista nera di parole di esito. È proprio lo schema che il codice stesso vieta in scripts/bot_esito.py:92-95 («una lista di negazioni non finisce mai»).

**Citazioni dal diff**
- scripts/bot_esito.py:409 — salta le righe «verifica esterna [precedente] su <sha>» che non contengono parole di esito. Rischio: una riga del genere con un esito negativo, accanto al titolo canonico APPROVATO, diventa sì. Esito: **blocco**. Nella copia ho provato `_decidi_verdetto` sul testo «VERIFICA ESTERNA #1 — APPROVATO» più la riga, HEAD contro staged. Queste sono passate da COMMENT ad APPROVE:
  - «Verifica esterna su 3b92254: FALLITA»
  - «- … su 3b92254: KO»
  - «… respinge la PR»
  - «… la nega»
  - «… rigettata»
  - «… non passa»
  - «- … su aaaaaaa: bloccata, da rifare»
  - «… : si» (senza accento)
  - «… : ❌»
  - «Verifica esterna precedente su 3b92254: superata male»
  - «… : FAILED»
  - «… : rejected»
  - «- Verifica esterna su accadde: niente» («accadde» è una parola fatta solo di cifre esadecimali e passa per uno SHA)

  Nessuno SHA viene confrontato con head: la riga può citare anche l'head stessa.
- scripts/bot_esito.py:105 — `_PAROLA_DI_ESITO`, la lista nera (approv, bocci, respint, negat, esito, verdetto, rifiut, promoss, ok, no, sì). Rischio: lessico di esito non elencato, inglese, simboli, «si» senza accento. Esito: **blocco** (è la causa del punto sopra).
- scripts/bot_esito.py:121 — `_BLOCCANTE_TECNICO`. «io», «processo», «operazione», «funzione» e «coda» sono tolti, e il separatore `[ \t]+` non attraversa più l'a capo. «lo giudico io bloccante» dà COMMENT. Lo spazio non separabile (NBSP) non è coperto: resta COMMENT, che è il verso prudente. Esito: **riserva**. Sono NO→sì contro HEAD, su un finding con gravità strutturata BASSA:
  - «V-1 (BASSA): una chiamata bloccante per il merge»
  - «attesa bloccante prima del merge»
  - «Join bloccante del merge»
  - «la lettura bloccante del verdetto: lo considero un problema serio»
  - «lock / pipe / select / sleep bloccante»

  Per #336 basta «read bloccante».
- scripts/bot_esito.py:526 — `leggi_verdetto`. Ok: base64 con validate, tetto a 1 MB sulla decompressione, controllo di eof e unconsumed_tail; illeggibile dà None, cioè RIPROVA.
- .github/workflows/verifica-bot.yml:96-101 — il commento dichiara R-671-3-M2. Ok.
- .github/workflows/verifica-bot.yml:271 — gzip -9n | base64 -w0 su una riga sola. Ok: niente delimitatore heredoc.
- tests/test_unit_verifica_bot.py:1321 — test di #329 sul testo reale. Ok, ma nessun test di #329 copre le varianti di esito fuori lista.

**Finding**
- **R-672-1-M2 (ALTA)** — esenzione a lista nera, scripts/bot_esito.py:105 e scripts/bot_esito.py:409. Fix: lista BIANCA della coda della riga. Il resto può contenere solo id V/R/F, virgole, «e», «;» e «(BASSA|BASSE|COSMETICA|COSMETICHE)». Regex provata: la riga vera di #329 la soddisfa; «: KO», «: V-1 (ALTA)», «: V-1 e rejected» no.
  ```
  ^\W*verifica esterna\s+(?:precedente\s+)?su\s+[0-9a-f]{7,40}\s*[:—–-]\s*(?:(?:[VRF]-\d+|e|,|;|\((?:BASS[AE]|COSMETIC(?:A|HE))\))\s*)+\.?\s*$
  ```
  Facoltativo: escludere lo SHA che è un prefisso di head_analizzata. Aggiungere come test COMMENT le 13 varianti elencate sopra.
- **R-672-2-M2 (BASSA)** — scripts/bot_esito.py:121: lista tecnica troppo ampia (chiamata, attesa, lettura, scrittura, join, lock, wait, sleep). Fix: restringere ai termini di sistema (read, write, recv, send, socket, i/o, select, poll), oppure niente esenzione se dopo viene «per il / del / prima del merge / rilascio». Test sui 4 casi sopra.
- **R-672-3-M2 (COSMETICA)** — il conteggio dichiarato «21 test falliscono su main» è 22 nella mia prova (HEAD + test nuovi).

**Rischio escluso:** non ho eseguito il workflow reale su GitHub. Non ho verificato quindi che GitHub non scarti più l'output compresso, né quanto è lungo l'output su un verdetto vero. Ho controllato solo lo script del job e i test. Non ho provato la cascata dei modelli né la GitHub App. Ho fatto solo sonde e test sulle copie, nessun mutante.

Memoria: riga #672-M2 e una lezione scritte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da scripts/commit_memoria_revisore.sh (11643d6).

Sonda riproducibile: /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/probe.py (si lancia con argomento la cartella scratchpad, che contiene le copie idx/ e head/).

Review #673-M2 sul terzo diff staged (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #673-M2: terza review del diff in staging su feat/bot-verdetto-m2 (base 942e665). Ho rifatto le copie idx/ e head/ partendo dall'indice e da HEAD attuali. Alla sonda /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/probe.py ho aggiunto 17 casi avversari nuovi e la prova di lentezza della regex.

**Elementi del diff esaminati**
- `scripts/bot_esito.py:107` — `_CITAZIONE_VERIFICA_PASSATA` ora è una lista bianca della coda. Rischio esaminato: una frase con un esito che passa da NO a sì. Esito **ok**:
  - le 19 varianti di #671/#672 danno COMMENT sia a HEAD sia nell'indice. Tra queste: FALLITA, KO, respinge, rigettata, non passa, ❌ in coda, FAILED, rejected, «si», «superata male», «accadde», «V-1 (ALTA)», «V-1 e rejected», «**Verifica esterna**: BOCCIATO».
  - danno COMMENT anche «V-1 (MEDIA)», «V-1 (bassa) ma BOCCIATO» e lo spazio a larghezza zero seguito da BOCCIATO.
  - una citazione senza titolo canonico dà COMMENT.
  - titolo canonico BOCCIATO più citazione dà COMMENT.
  - una gravità ALTA altrove nel testo dà COMMENT.
- `scripts/bot_esito.py:107` — prefisso `^\W*` della stessa regex. Rischio: un'emoji di esito davanti alla riga. Esito **riserva** (R-673-1-M2). «❌ Verifica esterna su 3b92254: V-1» e «🚫 Verifica esterna su …: V-1, V-2» passano da COMMENT ad APPROVE.
- `scripts/bot_esito.py:107` — coda `(?:tok\s*)+\.?\s*$`. Rischio: lentezza su testo malevolo. Esito **riserva** (R-673-2-M2). Con 30.000 «V-1 », poi 90.000 spazi, poi «X», il controllo impiega 21 s: il costo cresce col quadrato degli spazi. Il risultato è un timeout del job, quindi niente sì. Con «e » ripetuto 50.000 volte bastano 0,29 s.
- `scripts/bot_esito.py:124` e `scripts/bot_esito.py:220` — `_BLOCCANTE_TECNICO` ristretta. Rischio: parole comuni che cancellano una gravità detta a parole. Esito **ok**:
  - «chiamata/attesa/join/lettura/lock/sleep/pipe/wait bloccante» danno COMMENT.
  - «read bloccante» e «select bloccante» danno APPROVE, come voluto per il caso #336.
  - «thread bloccante» non viene toccato (lo esclude il `\b`).
  - una gravità detta a parole nella stessa riga resta vista.
- `scripts/bot_esito.py:527` — `leggi_verdetto`. Rischio: un input corrotto che porta a un sì. Esito **ok**: c'è il tetto di dimensione, poi il controllo di fine flusso (eof e coda non letta), poi `validate=True`; se qualcosa fallisce il risultato è None, cioè RIPROVA.
- `.github/workflows/verifica-bot.yml:271` — il verdetto viene compresso con gzip e passato come base64. Rischio: chi lo legge non riceve il valore. Esito **ok**: `VERDETTO_GZ` è collegato (`.github/workflows/verifica-bot.yml:339`). Il rischio di aggirare il filtro dei secret di GitHub era già stato dichiarato e accettato in R-671-3-M2.
- `tests/test_unit_verifica_bot.py:1391` — i casi FAILED/rejected sono test COMMENT. Esito **ok**.
- Test: con l'indice 579 passed. Con HEAD più i test nuovi 22 failed, che chiude il conteggio di R-672-3-M2.

**Riserve (da tracciare in stato_progetto.md)**
- **R-673-1-M2 BASSA** — `^\W*` in `scripts/bot_esito.py:107` accetta un'emoji di esito davanti alla citazione. Due interventi:
  - restringere il prefisso ai soli segni di elenco, per esempio `^[\s>*_•-]*`;
  - escludere uno SHA che sia prefisso della head (facoltativo, ma serve davvero solo insieme a questa correzione: oggi il caso ❌ più la head è l'unico NO→sì residuo).
- **R-673-2-M2 BASSA** — rallentamento quadratico sulla coda: due `\s*` uno dopo l'altro prima di `$`. Sostituire la fine con `(?:\.\s*)?$`, perché il ciclo consuma già gli spazi. L'esito non è mai un sì, solo un job lento o in timeout.
- **Cosmetica** — sono accettate code senza senso come «: e», «: ,;», «: (COSMETICA)» e SHA scritti in maiuscolo (DEADBEEF, per `re.I`). Non contengono esiti, quindi nessun rischio.

**Cosa non ho verificato**
- Il percorso reale su GitHub Actions: se `${{ needs.verifica.outputs.verdetto_gz }}` arriva integro e il filtro dei secret non lo scarta. Si può provare solo su una run vera, non qui. Ho verificato solo localmente, con la logica dello script e il test `TestWorkflowVerdettoCompresso`.
- Il diff tocca solo la macchina del bot. Non tocca il motore, `_get_window` o il cap delle iterazioni, quindi non serve un round-trip agentico e il Wall of Shame non si applica: nessuno slicing della history e nessuna simulazione di tool.

**Memoria del revisore**: riga #673-M2 più una lezione, committate da `scripts/commit_memoria_revisore.sh` (commit 20b2302) in /home/user/Gas/.claude/agents/memoria_revisore.md.

Review #673-M2 bis sul diff finale (commit fcbb8b4, verdetto integrale):

## VERDETTO: APPROVATO

Review #673-M2 bis: le correzioni di R-673-1-M2 e R-673-2-M2 sono a posto. Ho rifatto la sonda su una copia dell'indice attuale: ora 582 test passano e il verdetto vero #329 dà ancora APPROVE. Riserve aperte: nessuna.

**Cosa ho controllato nel diff**
- `scripts/bot_esito.py:110` — davanti a «verifica esterna» ora sono ammessi solo i segni di elenco `^[ \t>*_•-]*`. Rischio verificato: un'emoji di esito davanti alla riga che trasforma un NO in sì. Esito **ok**:
  - «❌ Verifica esterna su 3b92254: V-1» e «🚫 … V-1, V-2» ora danno COMMENT, come a HEAD.
  - Ho provato anche altri prefissi. «✅ …», «1. …» e «> **…**» non sono più citazioni, quindi vengono trattati come titoli fuori formato e danno NO (vince il dubbio). «• …» resta una citazione.
- `scripts/bot_esito.py:111` — la riga ora finisce con `(?:\.\s*)?$`. Rischio verificato: la lentezza quadratica. Esito **ok**: con 30.000 «V-1 », poi 90.000 spazi e poi «X» il controllo passa da 21 s a 0,63 s; il caso «e » ripetuto 50.000 volte resta a 0,33 s.
- `tests/test_unit_verifica_bot.py:1395` — i casi ❌ e 🚫 sono test che si aspettano COMMENT. Esito **ok**.
- `tests/test_unit_verifica_bot.py:1474` — `test_citazione_verifica_passata_non_quadratica` controlla che quella riga venga respinta in meno di 2 s. Esito **ok**.
- `tests/dati_verifica_bot/verdetto_329_7957a15.txt:32` — la riga vera «- Verifica esterna su 3b92254: V-1, V-3, V-4, V-5 (BASSE); V-6 e V-7 (COSMETICHE).» viene ancora riconosciuta come citazione, quindi il verdetto #329 dà APPROVE. Esito **ok**.
- I 19 casi con esito di #671/#672 danno ancora tutti COMMENT, sia a HEAD sia nell'indice.

**Cosa non ho verificato**: il tempo massimo di 2 s del test dipende dalla macchina. Su un runner CI lento potrebbe fallire senza un vero difetto: non l'ho misurato su GitHub Actions. Margine misurato qui: circa 3 volte.

**Memoria del revisore**: ho aggiunto la riga #673-M2 bis (nessuna lezione nuova) in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata con lo script (commit 52653ed).

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_verifica_bot.py`: 514 → 582 test (classi `TestVerdettiVeri`, `TestVerdettoCompresso`, `TestWorkflowVerdettoCompresso`, `test_citazione_verifica_passata_non_quadratica`), con i due verdetti veri in `tests/dati_verifica_bot/`. Con lo `scripts/bot_esito.py` di main falliscono 21 test (22 secondo il revisore, con HEAD di allora). Mutanti: senza `_BLOCCANTE_TECNICO` 6 falliscono; col vecchio `_RIGA_TITOLO` 4 falliscono; sulla versione bocciata in #671 falliscono 12 test nuovi. Altre suite toccate dal workflow: hooks + handoff + gasmerge `366 passed in 125.20s`. Motore (`gas.py`, `brains/`, `modules/`) non toccato.

## §6 STATO CI

`gh` non autenticato nel cloud: check lette con l'integrazione GitHub.
- 0033771, 11643d6, 20b2302, 52653ed: nessuna run su questi SHA da soli (pushati insieme a fcbb8b4).
- fcbb8b4 e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (la run sul push finale testerà solo la testa).

## §7 RISERVE APERTE

- R-671-3-M2 BASSA: la compressione aggira anche la rete «may contain secret» di GitHub; un secret vero nel testo resta fermato solo da `_SEGRETO` (dichiarato nel commento del workflow).
- Nota #673-M2 bis: `test_citazione_verifica_passata_non_quadratica` ha un tetto di 2 s con margine ~3×: su un runner lento può dare un falso rosso.
- Cosmetica #673-M2: code senza senso («: e», «: ,;») e SHA maiuscoli accettati come citazione (nessun esito, nessun rischio).
- Non verificato da nessuno: il percorso reale su GitHub Actions (output compresso integro e non scartato): si vedrà al primo giro del bot dopo il merge.
