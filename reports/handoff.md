# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-30 — Mani, fetta 30: gli invisibili citati dal bot come <U+XXXX> (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #309 (https://github.com/Gasss23/Gas/pull/309). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5084571647","url":"https://github.com/Gasss23/Gas/pull/309"}`), perché `gh` nel cloud non è autenticato. Tocca la macchina del bot: il check `verifica-bot` sarà neutral e il merge lo decide l'operatore.

---

## §1 SCOPE & ESITO FETTE

- **PR #306**: `FATTA` — mergiata (95be7b1) dopo due merge di main (#307, #308), review #578 e #579 APPROVATO.
- **Invisibili citati dal bot come <U+XXXX>** (via libera dell'operatore tramite M1): `FATTA` — regola nel PROMPT di `.github/workflows/verifica-bot.yml`, assert nel test.
- **Review #580 (chat Mani)**: APPROVATO CON RISERVE. R-580-1 BASSA (nessun test sulla regola): `FATTA`. R-580-2 BASSA (gravità maiuscola nuda citata nella sezione FINDING dà ancora NO): `DEFERITA — limite dichiarato`. **Review #581**: APPROVATO.
- **Bot su 7d57b26 (PR #309)**: APPROVATO CON RISERVE, check neutral. V-1 BASSA (l'assert non fissava «in qualunque campo»): `FATTA` in 0b7782a. V-2 COSMETICA («di controllo» comprende a capo e tab): `FATTA` — «a capo e tab restano normali».
- **Verifica esterna su 7d57b26 (https://github.com/Gasss23/Gas/pull/309#issuecomment-6523271160)**: APPROVATO CON RISERVE. V-1 BASSA (una credenziale spezzata da una citazione «<U+200B>» non era riconosciuta, e il PROMPT spinge proprio verso quella forma): `FATTA` in 0b7782a — `_senza_citazioni` in `contiene_segreti`. V-2 COSMETICA (R-580-2 senza test): `SALTATA — limite dichiarato`. V-3 COSMETICA (test del gate con `-I`): `SALTATA — già registrata (V-2 #306)`.
- **Review #582 (chat Mani)**: APPROVATO CON RISERVE (R-582-1 BASSA: citazione annidata o lettera visibile citata non riconosciute; R-582-2 COSMETICA: l'assert del PROMPT a pezzi separati). Registrate in stato_progetto.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 .github/workflows/verifica-bot.yml |   4 ++++
 reports/diff_sessione.md           |  12 +++++++-----
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  26 +++++++++++---------------
 scripts/bot_esito.py               |  12 +++++++++++-
 tests/test_unit_verifica_bot.py    |  16 ++++++++++++++++
```

NB: base = merge-base con origin/main = 95be7b1. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
0b7782a fix(bot): credenziali spezzate da una citazione <U+XXXX>, regola del PROMPT precisata (V-1 ve #309, V-1/V-2 bot #309, chat Mani)
c98edfd chore(revisore): memoria review #582 — APPROVATO CON RISERVE
7d57b26 docs(fine-task): Mani fetta 30, invisibili citati dal bot come <U+XXXX> (PR #309)
4799155 chore(bot): nel PROMPT del bot gli invisibili citati si scrivono come <U+XXXX> (V-2 ve #305, chat Mani)
9c8a880 chore(revisore): memoria review #581 — APPROVATO
bfb487a chore(revisore): memoria review #580 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 4799155 (.github/workflows/verifica-bot.yml, tests/test_unit_verifica_bot.py). NB: i caratteri invisibili citati nei verdetti sono trascritti come «<U+XXXX>». Verdetto integrale della review #580 (chat Mani), sul diff prima della correzione di R-580-1:

```
## VERDETTO: APPROVATO CON RISERVE

Review #580 (chat Mani). Ho esaminato il diff staged: 1 file, `.github/workflows/verifica-bot.yml`, +4 righe, solo il PROMPT del bot. `git diff --cached --check` è pulito. Ho letto CLAUDE.md (sez. 5, 8, 10), le parti di reports/stato_progetto.md che riguardano i casi #297/#305 e la memoria del revisore.

**Elementi esaminati**
- `.github/workflows/verifica-bot.yml:150` — è la nuova regola (righe 150-153): citare gli invisibili come `<U+XXXX>`, mai col carattere vero. Rischio esaminato: rompere il blocco `|` o l'interpolazione di GitHub Actions. Le 4 righe hanno lo stesso rientro di 8 spazi del blocco iniziato a `.github/workflows/verifica-bot.yml:120`. Non contengono `${{`, `$` o backtick. Il file ha 0 caratteri Cf. `yaml.safe_load` restituisce il PROMPT con il testo atteso. Esito: ok.
- `.github/workflows/verifica-bot.yml:210` — il PROMPT entra come input dell'action (`prompt: ${{ env.PROMPT }}`, uguale alle righe 226 e 242), non in una shell, quindi `<` e `>` non hanno effetti. Rischio esaminato: iniezione o rottura dell'interpolazione. Esito: ok.
- `scripts/bot_esito.py:103` (`_PAROLA_BLOCCANTE`), `scripts/bot_esito.py:98` (`_FINDING_GRAVITA`), `scripts/bot_esito.py:172` (`_RISERVA_REGISTRATA`) e `scripts/bot_esito.py:86` (`_SEGRETO`) — citazioni di contesto. Rischio esaminato: che il testo `<U+XXXX>` scritto dal bot inneschi una regola. Non ne innesca nessuna: dopo `U` viene `+` e non `-`, quindi non sembra un id di finding né una riserva R-; le cifre esadecimali non formano nessuna parola di gravità; non c'è nessuna forma di credenziale; non nasce nessuna riga di titolo. L'ho provato chiamando davvero `_decidi_verdetto`: un verdetto con «<U+200B>», «<U+202E>», «<U+FEFF>», «<U+00A0>» e «ME<U+200B>DIA» nella sezione FINDING risulta APPROVE. Esito: ok.
- `scripts/bot_esito.py:249` (`_invisibili_su_gravita`) e `scripts/bot_esito.py:270` (`_mostra_invisibili`) — citazioni di contesto. Il controllo severo resta com'è, come rete di sicurezza. La notazione chiesta al bot è la stessa che `_mostra_invisibili` usa già nella review pubblica, quindi è coerente. Esito: ok.
- Protocollo `.claude/verifica_esterna.md`: non dice nulla su invisibili, Unicode o citazioni letterali, quindi la regola non lo contraddice. Esito: ok.
- Suite del bot riprodotta: `tests/test_unit_verifica_bot.py` 510 passed.

**Riserve (da tracciare in stato_progetto.md)**
- R-580-1 (BASSA): nessun test fissa la nuova riga nel PROMPT. Le regole vicine sono fissate da assert in `tests/test_unit_verifica_bot.py:1283` (righe 1283-1285). Se un ritocco futuro toglie la regola, nessun test se ne accorge. Rimedio: un assert tipo `"<U+XXXX>" in prompt`.
- R-580-2 (BASSA): se il bot cita un caso di prova che contiene una gravità maiuscola nuda, per esempio «BASSA<U+200B>MEDIA», nella sezione FINDING, il risultato è ancora NO: la sonda dà `COMMENT, finding MEDIA`. Non lo causa l'invisibile ma `_PAROLA_BLOCCANTE` (MEDIA maiuscola). La regola nuova toglie solo il NO dovuto a un invisibile vero, non questo. Il PROMPT dice già di usare ALTA/MEDIA solo per le gravità reali. Il limite resta e va dichiarato.

**Rischio escluso esplicitamente**: non ho verificato che il modello del bot rispetti davvero la regola in una run reale. Si vede solo con un giro del bot su una PR con l'etichetta `verifica`, che non si può riprodurre in locale. Non ho nemmeno verificato la run della CI su GitHub.

Wall of Shame: non riguarda questo diff (nessun motore, nessuna history, nessuna simulazione di tool). I guardrail non sono toccati.

**Memoria**: ho aggiunto la riga contatore #580 e una lezione nuova in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata con `scripts/commit_memoria_revisore.sh` (bfb487a). Il diff staged del workflow resta intatto nell'index.

Promemoria: il file è nella macchina del bot, quindi il merge lo decide l'operatore. Il marcatore va creato con `bash scripts/segna_review_ok.sh` solo dopo questo verdetto.
```

Verdetto integrale della review #581 (chat Mani), sul diff finale del commit 4799155:

```
## VERDETTO: APPROVATO

Review #581 (chat Mani) è la ri-review del diff staged dopo la #580. Il diff staged ora tocca 2 file, +6 righe, e `git diff --cached --check` è pulito. La R-580-1 è chiusa. Il verdetto #580 (APPROVATO CON RISERVE, consegnato prima) è superato da questo per quanto riguarda la R-580-1.

**Elementi esaminati**
- `tests/test_unit_verifica_bot.py:1287` — è il nuovo assert in `test_schema_coerente_con_lo_script`. Controlla che il PROMPT, letto con yaml, contenga «SEMPRE come <U+XXXX>» e «mai il carattere vero». Rischio esaminato: un test che non morde. Ho riprodotto io il mutante: con `<U+XXXX>` cambiato in `<U+YYYY>` nel workflow ottengo 1 failed e 509 passed; poi ho rimesso il file com'era e il working tree è pulito. Le due frasi controllate stanno ciascuna su una sola riga fisica del workflow, quindi gli a capo del blocco `|` non le spezzano. Il commento rimanda a R-580-1, come fanno le regole vicine. Esito: ok.
- `.github/workflows/verifica-bot.yml:151` — la regola nel PROMPT (righe 150-153). Rischio esaminato: un cambiamento rispetto a quanto revisionato nella #580. Il diff del file è sempre di 4 righe, con lo stesso testo e lo stesso rientro. Valgono quindi le verifiche della #580: blocco `|` valido, nessun `${{`, 0 caratteri Cf, PROMPT passato come input `with: prompt` e non a una shell, nessuna regola di `scripts/bot_esito.py:103` o `scripts/bot_esito.py:98` innescata da `<U+XXXX>`. Esito: ok.
- Suite del bot riprodotta: 510 passed.

**Rischio escluso esplicitamente**: non ho verificato che il modello del bot rispetti davvero la regola in una run reale. Si vede solo con un giro del bot su una PR con l'etichetta `verifica`, che non si può riprodurre in locale.

**Riserva rimasta**: R-580-2 (BASSA) resta un limite dichiarato, come hai deciso. Se il bot cita un caso di prova con una gravità maiuscola nuda nella sezione FINDING, per esempio «BASSA<U+200B>MEDIA», `_PAROLA_BLOCCANTE` dà ancora NO.

**Memoria**: ho aggiunto la riga contatore #581 in `/home/user/Gas/.claude/agents/memoria_revisore.md`, senza lezioni nuove, e l'ho committata con lo script (9c8a880). I 2 file staged restano intatti nell'index.

Promemoria: il marcatore va creato con `bash scripts/segna_review_ok.sh` su questo diff staged. Il file è nella macchina del bot, quindi il merge lo decide l'operatore.
```

Commit 0b7782a (scripts/bot_esito.py, tests/test_unit_verifica_bot.py, .github/workflows/verifica-bot.yml: note di bot e verifica esterna su 7d57b26). Verdetto integrale della review #582 (chat Mani):

```
## VERDETTO: APPROVATO CON RISERVE

Review #582 (chat Mani), PR #309. Ho esaminato il diff in stage (3 file, +29/−5). Nessun antipattern del Wall of Shame: il diff non tocca la history né simula l'output dei tool. Nessun guardrail del motore indebolito.

**Elementi del diff esaminati**
1. `scripts/bot_esito.py:302` — il controllo stringa per stringa ora usa `_senza_citazioni` invece di `_senza_invisibili`. Ho cercato una credenziale che prima veniva fermata e ora passerebbe: non c'è (ok). Le due condizioni su `grezzo` restano uguali. Poi `_senza_citazioni` applica prima `_senza_invisibili` e solo dopo toglie le citazioni, quindi trova tutto quello che trovava la vecchia pulizia. Un testo riconosciuto da `_SEGRETO` contiene solo lettere, cifre, `_` e `-`, mai `<`, `+` o `>`, quindi non può accavallarsi con una citazione. Togliere le citazioni non spezza nessun caso trovato prima. L'eccezione resta intercettata (fail-closed, cioè `True`).
2. `scripts/bot_esito.py:307` — la regex `<U\+[0-9A-F]{4,6}>` con `re.I`. Rischio esaminato: falsi NO. Sonda: `ligh<U+00A0>s_On` e `high<U+200B>s_A` danno True. È la stessa classe di falso NO che già esiste (anche `highs_A` senza citazione dà True), solo estesa al punto in cui sta la citazione. Nel testo italiano normale è improbabile (riserva accettabile).
3. `scripts/bot_esito.py:307` — sonde sui casi limite, tutte con risultato False:
   - citazione annidata `gh<U+2<U+200B>00B>p_Zz9`: `sub` fa una sola passata e lascia una `<U+200B>` valida;
   - lettera visibile citata `gh<U+0070>_Zz9`;
   - 7 cifre `<U+0000200B>`;
   - citazione con spazio `<U+200B >`.

   Il testo pubblicato non contiene la credenziale leggibile, ma una persona la ricostruisce facilmente. Questo è R-582-1 (riserva).
4. `tests/test_unit_verifica_bot.py:226` — 4 casi (minuscolo `<u+feff>`, 5 cifre `<U+E0041>`), sia su `decidi` (testo) sia su `contiene_segreti` (descrizione di un finding) (ok). Mutante riprodotto da me, cioè la riga 302 riportata a `_senza_invisibili`: 4 failed. File ripristinato, nessuna differenza tra working tree e stage.
5. `tests/test_unit_verifica_bot.py:1300` — l'assert ora cerca «SEMPRE come» e «<U+XXXX>» separati, perché la riga del PROMPT è andata a capo. È più debole: non prova che i due pezzi siano vicini. Questo è R-582-2 (cosmetica). Ho verificato che il nuovo assert alla riga 1301 regge: «in qualunque campo» e «a capo e tab restano normali» stanno sulla stessa riga fisica, `.github/workflows/verifica-bot.yml:151` (ok).
6. `.github/workflows/verifica-bot.yml:150` — regola del PROMPT riformulata. `yaml.safe_load` ok, indentazione invariata (ok).

Suite del bot: 514 passed, riprodotti da me.

**Risposte alle domande**
- **Falsi NO?** Solo quando la citazione unisce «gh» a «[pousr]_» seguito da una lettera o cifra (`high<U+200B>s_A`). È la stessa classe di falsi NO che la regex produce già senza citazioni. C'è anche un caso noto: se il bot cita alla lettera il nuovo test (`gh<U+200B>p_Zz9abc`) dà NO. Anche questo esisteva già, perché lo stesso file di test contiene «sk-ant-oat01-abcdef», «ghp_Zz9» e «-----BEGIN» in chiaro (righe 506 e 521).
- **Pubblica una credenziale che prima non pubblicava?** No, per il ragionamento del punto 1. Restano non visti i casi di offuscamento (R-582-1), che però non venivano visti nemmeno prima.
- **Applicarlo anche al JSON grezzo?** Non serve. Il controllo stringa per stringa copre tutti i valori e tutte le chiavi (`_stringhe`). Nel JSON grezzo una corrispondenza a cavallo di due stringhe è impossibile, perché le virgolette e `": "` non fanno parte di `_SEGRETO`. Il grezzo aggiungerebbe solo il rischio di riunire pezzi di stringhe diverse.

**Riserve (da tracciare in stato_progetto.md)**
- **R-582-1 (BASSA):** la citazione annidata e la lettera visibile citata non vengono riconosciute. Si chiude con poco:
  - ripetere `_CITAZIONE_INVISIBILE.sub` fino a quando il testo non cambia più (o finché non resta nessuna citazione);
  - e/o controllare anche una versione con le citazioni decodificate (`chr(int(hex,16))`, poi `_senza_invisibili`).

  L'offuscamento in generale (base64, lettere separate da spazi) resta un limite di qualunque filtro a regex.
- **R-582-2 (COSMETICA):** l'assert del PROMPT a `tests/test_unit_verifica_bot.py:1300` è a pezzi separati. Si può normalizzare gli spazi (`" ".join(prompt.split())`) e cercare «SEMPRE come <U+XXXX>» intero.

**Rischio escluso:** non ho verificato come si comporta davvero il bot (il modello nel workflow GitHub). Non so se rispetta «a capo e tab restano normali» né se usa `<U+XXXX>` in tutti i campi: in questo ambiente non si può riprodurre senza un run reale su PR con etichetta `verifica`. Per lo stesso motivo non ho provato la pubblicazione reale della review.

Memoria: riga #582 e una lezione aggiunte in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole con `scripts/commit_memoria_revisore.sh` (commit c98edfd). Il diff in stage è rimasto intatto.
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. `tests/test_unit_verifica_bot.py`: da 510 (main) a 514 passed (assert sul PROMPT, `test_credenziale_spezzata_da_una_citazione` con 4 casi). Mutanti: regola cambiata in <U+YYYY> 1 failed; `contiene_segreti` senza `_senza_citazioni` 4 failed. Suite completa non rilanciata: il diff tocca solo il bot (PROMPT, `contiene_segreti`) e il suo test.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- bfb487a, 9c8a880 (memoria del revisore) e 4799155: pushati insieme prima dell'apertura della PR #309; nessuna run sulla PR per questi SHA.
- 7d57b26 (fine-task): check `verifica-bot` neutral, review del bot APPROVATO CON RISERVE (vedi §1); `handoff-check` success.
- c98edfd (memoria del revisore) e 0b7782a: pushati insieme; run non letta alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-582-1 (chat Mani) BASSA: una citazione annidata («gh<U+2<U+200B>00B>p_…») o una lettera visibile citata («gh<U+0070>_…») non vengono riconosciute da `contiene_segreti`.
- R-582-2 (chat Mani) COSMETICA: l'assert del PROMPT cerca i pezzi della regola separati.
- R-580-2 (chat Mani) BASSA, limite dichiarato: una gravità maiuscola nuda citata nella sezione FINDING dà ancora NO (`_PAROLA_BLOCCANTE`).
- Rischio escluso (#580/#581): che il modello rispetti davvero la regola si vede solo al primo giro reale del bot.
- V-1 bot / V-1 ve #306 BASSA: `test_invisibili_come_nel_gate` lega solo gli intervalli, non `_CATEGORIE_INVISIBILI`.
- V-2 bot / V-2 ve #306: l'import di modules.gate nel test funziona solo dalla radice del repo.
- V-2 COSMETICA del bot su 586b888 (#305): righe delle riserve minori senza tetto dopo l'escape.
- R-572-1, R-572-2, R-575-1 BASSE e R-575-2 COSMETICA (chat Mani), preesistenti.
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, V-2/V-3 ve #296, R-546-1: BASSE della chat Mani, invariate (vedi stato_progetto).
