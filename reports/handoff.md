# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-20 — Bot di verifica: falso rosso «Non bloccante» sulla PR #388

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa correzione (numero dopo il push). Tocca la macchina del bot: il check `verifica-bot` dà neutral e il merge lo decide l'operatore, che in chat ha scelto questa strada («fai quello, sicurezza massima») e ha detto «ok avvisami quando hai mergiato».
2. Da decidere: aggiungere a `_GRAVI` anche «alto», «severo», «serio», «elevato» (nota del revisore #831, fuori da questo diff).

---

## §1 SCOPE & ESITO FETTE

- **Correzione del falso rosso del bot sulla PR #388**: FATTA, commit 4c982142. Review #831 APPROVATO CON RISERVE (R-831-1 BASSA: test mancanti per punteggiatura e confine di parola), corretta nello stesso diff e rivista in #832 APPROVATO CON RISERVE (R-832-1 COSMETICA).
  - Causa: «Non bloccante:» a inizio frase nella riga di V-1 (BASSA); `_GRAVITA_NEGATA` valeva solo per «non» minuscolo e la regola a parole contava «bloccante» come MEDIA. Prova sul testo reale: main {BASSA, MEDIA}, ora {BASSA}.
  - Correzione: `\bnon` → `\b[Nn]on`. «NON» tutto maiuscolo resta bloccante.
- **Dopo il merge**: nuovo giro del bot sulla PR #388. DEFERITA: dipende dal merge di questa PR.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 reports/diff_sessione.md           |  17 +++++------------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  35 +++++++++++------------------------
 scripts/bot_esito.py               |   4 +++-
 tests/test_unit_verifica_bot.py    |  28 ++++++++++++++++++++++++++++
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base: d03e5bf2 (origin/main).

## §3 GIT LOG --ONELINE (sessione)

```
4c982142 fix(bot): «Non bloccante» a inizio frase non è più letto come gravità MEDIA (falso rosso del bot sulla PR #388); «NON» maiuscolo resta bloccante — review #831 e #832 APPROVATO CON RISERVE
a640fa0a chore(revisore): memoria review #832 — APPROVATO CON RISERVE
7f8b52aa chore(revisore): memoria review #831 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #831-BOT (diff poi committato in 4c982142, con i test aggiunti rivisti in #832)

## VERDETTO: APPROVATO CON RISERVE

Review #831-BOT. Diff staged di 2 file, +27/−1, sha256 del diff `c11998ff…`, sul ramo `claude/fix-bot-non-maiuscolo` partito da d03e5bf2. L'indice coincide con l'albero di lavoro e `git diff --cached --check` è pulito.

Ho fatto le letture obbligatorie: CLAUDE.md sezioni 1, 5, 8 e 10; stato_progetto.md con letture mirate; la mia memoria, dove ho controllato le lezioni #240 e #441 sulla negazione. Il diff non tocca la storia dei messaggi, `_get_window` né i provider: il Wall of Shame non c'entra.

**Elementi del diff esaminati**
- `scripts/bot_esito.py:180` — `\bnon` diventa `\b[Nn]on` in `_GRAVITA_NEGATA`.
  - Rischio esaminato: che un «Non» a inizio frase faccia passare una gravità che il bot sta davvero assegnando.
  - La regex resta senza `re.I`: le parole in mezzo e la gravità restano minuscole.
  - «NON», «NOn», «nON», «Non È grave» e «Non è Alta» bloccano ancora.
  - Ho provato la simmetria su 648.144 frasi generate (0 a 3 parole della lista o fuori lista, 18 gravità, 8 code): «Non …» sullo staged dà sempre lo stesso esito di «non …» su main e di «non …» sullo staged, con 0 differenze.
  - Quindi il diff non introduce casi nuovi: applica a «Non» la stessa regola già accettata dalle review #240 e #441.
  - Esito: ok.
- `scripts/bot_esito.py:263` — dove si usa la negazione: il testo «ripulito» serve solo alla regola delle gravità scritte a parole (`scripts/bot_esito.py:269`).
  - Rischio esaminato: che la negazione nasconda anche gravità in maiuscolo o tra parentesi.
  - Le maiuscole si cercano sul testo non ripulito (`scripts/bot_esito.py:261`). Le parentesi e il campo strutturato restano a parte, uniti in `scripts/bot_esito.py:477`.
  - Ho provato che il caso a capo (`\s+` comprende `\n`) non nasconde nulla: «x Non\n- V-2 (BASSA) — grave» resta MEDIA. Il caso «Non bloccante» seguito da «MEDIA» resta MEDIA.
  - Sul testo reale del bot su #388: main dà {BASSA, MEDIA}, lo staged dà {BASSA}.
  - Esito: ok.
- `tests/test_unit_verifica_bot.py:712` — test del caso reale #388, che deve dare APPROVE.
  - Fail-before rieseguito: col `bot_esito.py` di main ottengo 1 failed, 5 passed (lanciati solo i test #388). Sull'indice tutta la suite fa 627 passed.
  - Esito: ok.
- `tests/test_unit_verifica_bot.py:724` — i 5 casi che devono restare bloccati.
  - Mutanti uccisi: `(?i:non)` (1 failed), `[Nn][Oo][Nn]` (1 failed), parole libere al posto della lista (4 failed). Anche il ritorno a «non» minuscolo è ucciso (1 failed).
  - Due mutanti sopravvivono, vedi R-831-1.
  - Esito: riserva.
- `scripts/bot_esito.py:72` (contesto) — `tests/test_unit_verifica_bot.py` fa parte della macchina del bot. Ho controllato che `tocca_macchina_bot` dia True su questi 2 file: il check `verifica-bot` darà `neutral` e il merge lo decide l'operatore, non l'agente.

**Riserve**
- **R-831-1 BASSA** — già presente su main, ora vale anche per «Non». Nessun test difende due proprietà che il commento della regex dichiara:
  - il confine di parola: il mutante senza `\b` sopravvive (627 passed), quindi un caso come «Canon grave» non è protetto;
  - «niente punteggiatura fra le parole»: il mutante con `[\s:,]+` fra le parole della lista sopravvive (627 passed) e nasconderebbe una gravità vera, «V-1 (BASSA) — Non è più così: grave» (lo staged dà MEDIA, il mutante solo BASSA).
  - Su main entrambi i mutanti sopravvivono già ai test che c'erano: il buco non nasce da questo diff.
  - Rimedio: aggiungere al test parametrizzato «V-1 (BASSA) — Non è più così: grave» e «V-1 (BASSA) — Canon grave», che devono dare COMMENT.

**Nota fuori dal diff (non classificata)**: l'elenco `_GRAVI` non contiene «alto», «severo», «serio», «elevato». «V-1 (BASSA) — rischio alto» dà solo BASSA anche su main. Lo decide l'operatore.

**Rischi esclusi (non verificati)**
- Il comportamento del workflow `verifica-bot` vero sulla PR, cioè quale `bot_esito.py` usa il runner (base o head): non l'ho verificato perché non si riproduce in locale. L'esito `neutral` l'ho dedotto solo da `tocca_macchina_bot`.
- Non ho riesaminato altri verdetti storici del bot per cercare falsi sì nuovi: mi sono basato sulla prova di simmetria, che dimostra che il diff non introduce casi diversi da quelli già accettati per «non».

**Memoria**
- Riga contatore #831-BOT e una lezione aggiunte in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole con `scripts/commit_memoria_revisore.sh` (commit 7f8b52aa).
- Il diff staged è intatto. Come mi hai chiesto, non ho creato `.claude/.review_ok` e non ho committato il diff.
- Il numero 831 l'ho controllato: l'ultima review sul ramo `origin/claude/nifty-galileo-3k7kbm` è #830-CRM.

### Review #832-BOT (commit 4c982142)

## VERDETTO: APPROVATO CON RISERVE

Review #832-BOT. Ho revisionato il diff in staging su `claude/fix-bot-non-maiuscolo`: 2 file, +31/−1, sha256 del diff 2bbba1b7. Prima ho letto CLAUDE.md §5, reports/stato_progetto.md (in testa e con Grep su bot_esito e R-831) e la coda della mia memoria (#831).

**Elementi del diff esaminati**
- `scripts/bot_esito.py:180` — l'unica modifica al codice resta `\bnon` diventato `\b[Nn]on` dentro `_GRAVITA_NEGATA`. Rischio esaminato: che il codice sia cambiato rispetto alla #831. Il diff del file è ancora +3/−1, quindi due righe di commento più la regex. Esito: **ok**, codice uguale alla #831.
- `tests/test_unit_verifica_bot.py:730` — nuovo caso «V-1 (BASSA) — Non è più così: grave», che deve dare COMMENT. Rischio esaminato: che non difenda la regola «niente punteggiatura fra le parole». Il mutante con `[\s:,]+` fra le parole dà 1 failed, proprio questo caso; anche il mutante con `\W+` dà 1 failed. Esito: **ok**.
- `tests/test_unit_verifica_bot.py:731` — nuovi casi «Canon grave» e «canon grave». Rischio esaminato: che non difendano il confine di parola. Il mutante senza `\b` dà 2 failed, esattamente questi due. Esito: **ok**.
- `tests/test_unit_verifica_bot.py:712` — il test positivo del caso reale della PR #388. Con il bot_esito.py di HEAD (7f8b52aa) ho 1 failed, solo questo test: fallisce prima della correzione e passa dopo. I tre casi nuovi passano anche su HEAD: servono a bloccare proprietà già vere, non a dimostrare la correzione. Esito: **ok**.
- Contesto: `scripts/bot_esito.py:263`. La negazione agisce ancora solo sulla regola a parole; le gravità maiuscole e quelle tra parentesi (`scripts/bot_esito.py:261`, `scripts/bot_esito.py:274`) non passano dalla negazione. Esito: **ok**.

**Rieseguito da me**, su una copia dell'indice nella mia cartella temporanea:
- **Suite:** 630 passed.
- **Mutanti uccisi:** senza `\b`, `[\s:,]+` fra le parole, `\W+` fra le parole, ritorno a «non» minuscolo, `(?i:non)` (quest'ultimo lo uccide il caso «NON bloccante»).
- **Codice ripristinato:** 630 passed.

R-831-1 è chiusa per i due mutanti che avevo nominato.

**Riserva**
- **R-832-1 COSMETICA (residuo di R-831-1):** sopravvive il mutante che accetta punteggiatura subito dopo «Non» (`\b[Nn]on[\s:]+` al posto di `\b[Nn]on\s+`): 630 passed. Quel mutante nasconderebbe «V-1 (BASSA) — Non: grave» e «Non, grave». Oggi il comportamento è giusto (verificato: {BASSA, MEDIA}, quindi COMMENT), ma nessun test lo difende. Rimedio: aggiungere «V-1 (BASSA) — Non: grave» al test parametrizzato `test_388_non_maiuscolo_non_nasconde_gravita`. Non blocca: è una lacuna di test e il comportamento è corretto. Va tracciata in reports/stato_progetto.md.

**Rischi esclusi**
- Non ho verificato il comportamento del bot vero dentro GitHub Actions (`.github/workflows/verifica-bot.yml`, verdetto prodotto dal modello): non si riproduce qui. Lo confermerà la run del bot sulla PR.
- Ho rieseguito solo `tests/test_unit_verifica_bot.py`, non l'intera suite pytest: il diff tocca solo bot_esito.py e il suo test.
- La lacuna di `_GRAVI` («alto», «severo», «serio», «elevato») è fuori da questo diff, come hai detto: la porti tu all'operatore.

Non ho creato `.claude/.review_ok` e non ho committato il diff: l'indice è ancora +31/−1 su 2 file.

Riga contatore scritta in /home/user/Gas/.claude/agents/memoria_revisore.md (#832-BOT) e committata da sola con `scripts/commit_memoria_revisore.sh`: commit a640fa0a. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_verifica_bot.py`:** 627 su main d03e5bf2 → 630 passed. `test_388_non_maiuscolo_a_inizio_frase_non_blocca` fallisce col `bot_esito.py` di main (1 failed, 626 passed). I casi di `test_388_non_maiuscolo_non_nasconde_gravita` uccidono i mutanti senza `\b`, con punteggiatura fra le parole, con `(?i:non)`.
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`) e CRM: non toccati.

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - `7f8b52aa`, `a640fa0a`, `4c982142`: run non ancora disponibile alla scrittura dell'handoff. Saranno pushati insieme al commit di fine-task che contiene questo file: una sola run testerà l'albero di testa.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-832-1 (COSMETICA):** nessun test per «V-1 (BASSA) — Non: grave» (punteggiatura subito dopo «Non»): il mutante `\b[Nn]on[\s:]+` sopravvive; oggi il comportamento è giusto (COMMENT).
- **Nota del revisore #831 (non classificata, fuori dal diff):** `_GRAVI` non contiene «alto», «severo», «serio», «elevato» («rischio alto» dà solo BASSA anche su main). Decide l'operatore.
- **Rischio escluso (revisori #831/#832):** il comportamento del bot vero dentro GitHub Actions lo confermerà la run sulla PR; il workflow `pull_request_target` usa gli script di main, quindi la correzione vale per le PR solo dopo il merge.
- **Chiuse in questa sessione:** R-831-1.
