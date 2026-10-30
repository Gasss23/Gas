# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani, fetta 29: test del bot dopo la terza verifica esterna su #305 (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #306 (https://github.com/Gasss23/Gas/pull/306). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5076464675","url":"https://github.com/Gasss23/Gas/pull/306"}`), perché `gh` nel cloud non è autenticato. Il file dei test fa parte della macchina del bot: il check `verifica-bot` sarà neutral e il merge lo decide l'operatore.

---

## §1 SCOPE & ESITO FETTE

- **PR #305**: `FATTA` — mergiata (a5b1c62). Terza verifica esterna su 586b888 (https://github.com/Gasss23/Gas/pull/305#issuecomment-6506958440): APPROVATO CON RISERVE, nessun difetto del bot.
- **V-1 ve #305 (terza) BASSA** (due mutanti sopravvivevano): `FATTA` — test positivo sul titolo con un invisibile, `test_controlli_bidi` con ogni controllo da solo.
- **V-2 ve #305 (terza) BASSA** (falso NO prudente sugli invisibili attaccati a parole come «multimedia»): `FATTA` — registrata come compromesso accettato in stato_progetto, codice invariato.
- **V-3 ve #305 (terza) COSMETICA**: `FATTA` — `test_invisibili_come_nel_gate`.
- **V-4 / V-5 ve #305 (terza) COSMETICHE**: `SALTATA — report superati, resa solo estetica`.
- **Review #576 (chat Mani)**: APPROVATO CON RISERVE (R-576-1 BASSA: \x0b nel test positivo avrebbe bloccato R-572-1): `FATTA`. **Review #577**: APPROVATO.
- **Bot su 204a6c1 (PR #306)**: APPROVATO CON RISERVE, check verifica-bot neutral («decide l'operatore»). V-1 BASSA (il test «uguali al gate» lega solo gli intervalli, non `_CATEGORIE_INVISIBILI`): `DEFERITA — riserva, alla prossima fetta sui test del bot`. V-2 COSMETICA (import di modules.gate solo dalla radice del repo): `DEFERITA — come tests/test_unit_gate.py, va bene in CI`.
- **Verifica esterna su 204a6c1 (https://github.com/Gasss23/Gas/pull/306#issuecomment-6510340226)**: APPROVATO CON RISERVE. V-1 BASSA (la stessa V-1 del bot): `DEFERITA`. V-2 BASSA (import da radice): `DEFERITA`. V-3 BASSA (§6 diceva «nessuna run» per b692e27, che ha la run 40966074777 con handoff-check failure intermedio): `FATTA` — §6 corretto qui. V-4 COSMETICA (§3 senza 14c4983): `FATTA` — §3 rigenerato dalla nuova base. V-5 COSMETICA (invisibili del titolo solo a metà parola): `SALTATA — nessun rischio`. Nota: chiede che l'operatore confermi lui il via libera di M1 su V-2 ve #305 come compromesso.
- **Merge di origin/main 52c113b (PR #307 di M1)**: `FATTA` — la #306 era in conflitto (solo report). Review #578 (chat Mani) APPROVATO. Il sì dell'operatore al merge della #306 («mergia #306») è arrivato a M1, che la mergia.
- **Merge di origin/main 7ab6fc4 (PR #308 di M2, voce)**: `FATTA` — nuovo conflitto, solo report e memoria. Review #579 (chat Mani) APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 reports/diff_sessione.md           |  14 +++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  35 ++++++++++++++++++-----------------
 tests/test_unit_verifica_bot.py    |  19 +++++++++++++++++--
```

NB: base = merge-base con origin/main = 7ab6fc4. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
a6976f2 Merge origin/main (7ab6fc4, PR #308 di M2) in claude/peaceful-lovelace-0w2b7q (PR #306)
88427e8 docs(fine-task): PR #306 dopo il merge di main (#307), note del bot e della verifica esterna su 204a6c1
9ceea27 Merge origin/main (52c113b, PR #307 di M1) in claude/peaceful-lovelace-0w2b7q (PR #306)
204a6c1 docs(fine-task): PR #306, riga di reports/handoff.md in §2
14c4983 docs(fine-task): Mani fetta 29, test del bot dopo la terza verifica esterna su #305 (PR #306)
b692e27 test(bot): titolo con invisibile, ogni controllo bidi da solo, invisibili uguali al gate (terza verifica esterna #305, chat Mani)
0c6c7d1 chore(revisore): memoria review #577 — APPROVATO
19292dd chore(revisore): memoria review #576 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; i commit di fine-task precedenti della sessione sì.

## §4 VERDETTO DEL REVISORE (per commit motore)

NB: i caratteri invisibili citati alla lettera nei verdetti sono trascritti come «<U+XXXX>».

Commit b692e27 (tests/test_unit_verifica_bot.py). Verdetto integrale della review #576 (chat Mani), sul diff prima della correzione di R-576-1:

```
## VERDETTO: APPROVATO CON RISERVE

Review #576 (chat Mani). Ho esaminato il diff staged di `tests/test_unit_verifica_bot.py` (+16/-2), che fa parte della macchina del bot: il merge lo decide l'operatore. Ho letto prima CLAUDE.md (sez. 1, 5, 8, 10), `reports/stato_progetto.md` (le parti che servivano) e la memoria del revisore. Nessun antipattern del Wall of Shame: il diff tocca solo test, senza slicing della history e senza output simulati di tool.

**Elementi del diff esaminati**
- `tests/test_unit_verifica_bot.py:254`: il parametro ora copre ogni controllo bidi da solo, U+202A–202E e U+2066–2069, senza U+202C in coda. Il rischio era un test che non distingue i mutanti di `_BIDI`. Ho rifatto i mutanti su una copia del repo, togliendo un elemento alla volta da `scripts/bot_esito.py:222`: tutti e 9 danno 1 failed. Col file di test di HEAD, il mutante senza 202E e 2069 dà 0 failed (500 passed): il vecchio test era davvero cieco. — ok
- `tests/test_unit_verifica_bot.py:272`: nuovo test positivo, «APPRO<inv>VATO» col campo APPROVATO dà APPROVE. Mutante senza lo strip prima del titolo (`scripts/bot_esito.py:377`): 3 failed, uno per parametro, come dichiarato. — riserva R-576-1 sul parametro `\x0b`
- `tests/test_unit_verifica_bot.py:280`: uguaglianza tra `be._INVISIBILI_NON_CF` e quella di `modules/gate/gate.py:172`. Mutante con un intervallo diverso: 1 failed. — ok, con una nota: l'import di `modules.gate` funziona solo se si lancia dalla radice del repo. Lanciato da /tmp il test fallisce. È lo stesso schema di `tests/test_unit_gate.py:15`, e in CI va bene perché ci.yml lancia `python -m pytest` dalla radice.
- Contesto: `scripts/bot_esito.py:369`, il blocco bidi gira sul testo grezzo prima dello strip, quindi il nuovo test bidi colpisce quel controllo e non `_invisibili_su_gravita` (in «ATLA» non c'è nessuna parola di gravità). — ok

Suite del bot: **509 passed**, riprodotto.

**Domanda di merito (APPROVE o COMMENT per un invisibile nel titolo)**: fissare APPROVE è giusto. Lo strip toglie solo caratteri invisibili e non può aggiungere testo visibile. Quindi la lettura ripulita coincide con quella che vede l'operatore, e il titolo è solo un controllo di coerenza col campo strutturato. Le sonde confermano che le forme pericolose restano un NO:
- «APPROVATO<U+200B> CON RISERVE» col campo APPROVATO dà COMMENT.
- «BOCCI<U+200B>ATO» dà COMMENT.
- «APPROVATO<U+2028>CON RISERVE» e il tag U+E0020 al posto dello spazio danno COMMENT, perché la riga esce dal formato del protocollo.

COMMENT non aggiungerebbe sicurezza: produrrebbe solo falsi NO, cioè il problema già visto col bot #297.

**Riserve**
- **R-576-1 (chat Mani) BASSA**: il parametro `\x0b` del test positivo fissa APPROVE su un separatore di riga. Anche U+2028 dà APPROVE (provato). La riserva aperta R-572-1 dice che questi caratteri vanno letti come «a capo» e non come vuoto. Quando la si chiude, «APPRO\x0bVATO» diventa due righe e quindi COMMENT, e questo test bloccherebbe proprio il fix. Correzione: sostituire `\x0b` con un invisibile che non è un separatore di riga, per esempio `\x1b` o U+2060. Il mutante resta discriminante.

**Rischio escluso**: non ho verificato come GitHub mostra davvero `\x0b`, U+2028 e U+3164 nel titolo pubblicato (se come a capo, come spazio o per niente). Non si riproduce in dev senza pubblicare un commento. Il giudizio di merito si basa sulla lettura del testo dopo lo strip, non sul rendering reale.

V-2 (falso NO sugli invisibili attaccati a parole come «multimedia») registrata come compromesso: va bene. È nel verso prudente ed era già stata accettata nella review #572.

**Memoria**
- Riga contatore #576 aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md`, con due lezioni: un test positivo va confrontato con le riserve aperte; nei mutanti `a | b - {x}` toglie x solo da b, servono le parentesi.
- Commit atomico fatto: 19292dd. Il diff staged del test resta intatto nell'index.
```

Verdetto integrale della review #577 (chat Mani), sul diff finale del commit b692e27:

```
## VERDETTO: APPROVATO

Review #577 (chat Mani), ri-review della #576. Ho esaminato il diff staged su `tests/test_unit_verifica_bot.py` (+17/-2). Tocca solo la macchina del bot, quindi il merge lo decide l'operatore. Rispetto alla #576 cambiano solo i parametri del test positivo. La riserva R-576-1 è chiusa e il test resta discriminante.

**Elementi esaminati**
- `tests/test_unit_verifica_bot.py:273` — parametri `<U+200B>`, `ㅤ`, `<U+2060>`, `\x1b` al posto di `\x0b`. Rischio: che il test fissi APPROVE su un separatore di riga, cioè il comportamento che R-572-1 vuole cambiare. Ho provato `splitlines()` su «A\x1bB» e su «A<U+2060>B»: dà una sola riga in entrambi i casi, quindi nessuno dei due è un separatore. Il commento a `tests/test_unit_verifica_bot.py:272` rimanda a R-572-1. Esito: ok, R-576-1 chiusa.
- `scripts/bot_esito.py:377` (contesto, non toccato) — lo strip degli invisibili prima del confronto del titolo. Rischio: che il nuovo test non colga più la mancanza dello strip. Ho rifatto il mutante «senza strip» su una copia del repo: 4 failed su 510, uno per parametro (prima erano 3). Esito: ok.
- `tests/test_unit_verifica_bot.py:254` e `tests/test_unit_verifica_bot.py:283` — il test bidi su ogni carattere da solo e l'uguaglianza degli intervalli con il gate. Ho controllato che siano identici a quelli rivisti nella #576 (mutanti già rifatti lì). Esito: ok.

Suite del bot: **510 passed** (riprodotto).

**Rischio escluso**: non ho verificato come GitHub mostra davvero U+2060 e `\x1b` nel titolo pubblicato. Non si può riprodurre in sviluppo senza pubblicare un commento.

**Memoria**: aggiunta la riga #577 in `/home/user/Gas/.claude/agents/memoria_revisore.md`, nessuna lezione nuova. È già committata da sola (0c6c7d1); il diff staged è rimasto intatto nell'index.
```

Commit 9ceea27 (merge di origin/main 52c113b: da main entrano gas.py, modules/gate/gate.py, modules/sviluppo/, tests/test_unit_gate.py, tests/test_unit_kernel.py, tests/test_unit_richieste.py, .github/workflows/ci.yml, gas_identity.md, già revisionati da M1). Verdetto integrale della review #578 (chat Mani):

```
## VERDETTO: APPROVATO

Review #578 (chat Mani). Oggetto: il merge non ancora committato di origin/main 52c113b (PR #307 di M1, ponte voce → sviluppo) nel branch claude/peaceful-lovelace-0w2b7q (PR #306). Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (le righe che servivano, con Grep) e la memoria del revisore.

**Elementi del diff esaminati**
- `tests/test_unit_verifica_bot.py:281`: `test_invisibili_come_nel_gate` confronta `be._INVISIBILI_NON_CF` con `gate._INVISIBILI_NON_CF`. Rischio guardato: che main avesse cambiato gli intervalli nel gate. In `git diff a5b1c62 origin/main -- modules/gate/gate.py` la parola INVISIBILI compare 0 volte, quindi il test resta valido e passa. **Esito: ok.**
- `modules/gate/gate.py:176`: la tupla `_INVISIBILI_NON_CF` è identica a quella della base. **Esito: ok.**
- `modules/gate/gate.py:108` e `modules/gate/gate.py:305`: main aggiunge `.gas_richieste_uso` a `_DENY_PREFIXES` e a `_LIVELLO3_PREFISSI`, più `richiedi_sviluppo` come UNCERTAIN in `GATE_ALLOWLIST`. Rischio guardato: che la risoluzione del merge le perdesse. Sono presenti, con le liste sorelle allineate: `gas.py:2016`, `tests/test_unit_gate.py:466`, `.gitignore:56`. **Esito: ok.**
- `.github/workflows/ci.yml:166`: il passo «Run richieste suite» di main è entrato intatto. **Esito: ok.**

**Integrità del merge**
1. `git diff origin/main --cached --stat` riporta solo 7 file: `.claude/agents/memoria_revisore.md`, `reports/diff_sessione.md`, `reports/handoff.md`, `reports/ripartenza_mani.md`, `reports/stato_progetto.md`, `reports/ultimo_report.md` e `tests/test_unit_verifica_bot.py`. Nessun file del motore entra diverso da main.
2. `git diff --cached HEAD` è vuoto su handoff, ultimo_report, diff_sessione, ripartenza_mani e test_unit_verifica_bot: i tuoi file restano come a HEAD.
3. Memoria del revisore: ci sono le righe di tutti e due i lati, #576 e #577 (chat Mani) più #557-M1…#559-M1 con le loro lezioni.
4. stato_progetto.md: la riga 4 è risolta come hai detto (la voce «fetta 29» davanti a quella di M1). Il blocco «COORDINAMENTO DELLE CHAT» di main è stato mantenuto e la voce «fetta 29» è entrata nello storico delle fette.
5. Nessun marcatore di conflitto rimasto in reports/ né nella memoria.

**Test sull'albero del merge**
- test_unit_verifica_bot + test_unit_gate + test_unit_richieste: 1356 passed.
- pytest completo: 2702 passed, 2 skipped.
- Kernel (`tests/test_unit_kernel.py`): 1060 PASS, 1 FAIL (T31g, che costruisce il vector store con GAS_VECTORS=1). Su un worktree pulito di origin/main il risultato è identico, quindi dipende dall'ambiente (manca la parte dei vettori) e non dal merge. Nota: il 1065 PASS dichiarato da M1 era stato misurato in un altro ambiente.

**Rischio escluso**
- Non ho rifatto la review di merito del ponte (`modules/sviluppo/richieste.py`, le modifiche a gas.py): è già stata fatta da M1 nelle review #557-M1…#559-M1 ed è su main, e questo merge non ne cambia una riga.
- Non ho verificato la CI su GitHub: il merge non è ancora committato né pushato.

**Riga contatore e commit della memoria**
- La riga #578 è aggiunta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, ma non è in staging.
- `bash scripts/commit_memoria_revisore.sh` non è partito: l'hook `review_gate.sh` ha bloccato il comando (marcatore `.review_ok` non allineato al diff staged). Comunque con un merge in corso git non permette il commit parziale (`-o`).
- Cosa devi fare: `git add .claude/agents/memoria_revisore.md`, poi `bash scripts/segna_review_ok.sh` (l'add cambia lo SHA del diff staged), poi il commit di merge. La riga aggiunta è solo memoria e non cambia niente del diff revisionato.
```

Commit del merge di origin/main 7ab6fc4 (PR #308 di M2: da main entrano clients/voice/browser_server.py, modules/voice/server.py, tests/test_unit_voice_server.py, tests/test_unit_voice_stt.py, già revisionati da M2). Verdetto integrale della review #579 (chat Mani):

```
## VERDETTO: APPROVATO

Review #579 (chat Mani): merge di origin/main 7ab6fc4 (PR #308 M2, voce V2) nel branch claude/peaceful-lovelace-0w2b7q (PR #306). Ho controllato lo stage, che non è ancora stato committato.

Prima della review ho letto CLAUDE.md §5, la struttura di reports/stato_progetto.md (le sezioni Finding aperti e Prossimi passi) e la coda di .claude/agents/memoria_revisore.md.

**Citazioni (file del diff sotto review):**
1. `clients/voice/browser_server.py:93` — `_proxy_voice` del proxy browser, uno dei punti su cui interviene la V2 di main. Rischio esaminato: che la risoluzione del merge alteri il codice di M2. Esito: **ok**. Il delta staged-vs-HEAD è identico al delta merge-base 52c113b → origin/main, e `git diff --cached origin/main` su questo file è vuoto.
2. `modules/voice/server.py:1` — server voce di M2, entrato da main. Stesso rischio. Esito: **ok**. Delta identico a quello di main e nessuna differenza con origin/main. Ho fatto lo stesso controllo su tests/test_unit_voice_server.py, tests/test_unit_voice_stt.py e reports/roadmap.md: tutti identici a main.
3. `reports/stato_progetto.md:4` — riga «Ultimo aggiornamento». Rischio: che si perda la voce di main. Esito: **ok**. La riga 4 nello stage è identica a HEAD. Main non aveva toccato la riga 4: il suo unico contributo è la voce «Voce V2 (PR #308)» intorno alla riga 598, che è presente. Contro HEAD e contro origin/main non manca nessuna riga.
4. `.claude/agents/memoria_revisore.md:1031` — fusione della memoria. Rischio: che si perdano righe di un lato. Esito: **ok**. Contro HEAD ci sono solo aggiunte (da #568-M2 a #573-M2, con le loro lezioni). Contro origin/main ci sono solo aggiunte (#576, #577, #578 e le loro lezioni). Nessuna riga tolta.
5. `tests/test_unit_verifica_bot.py:281` — il tuo test del bot. Rischio: che venga alterato dal merge. Esito: **ok**, identico a HEAD. Lo stesso vale per reports/handoff.md, reports/ultimo_report.md e reports/diff_sessione.md.

**Altri controlli:**
- Nessun marcatore di conflitto nei file in stage.
- `git diff --cached HEAD --check` è pulito.
- `git diff origin/main --cached --stat` mostra solo i tuoi 7 file: memoria, diff_sessione, handoff, ripartenza_mani, stato_progetto, ultimo_report e tests/test_unit_verifica_bot.py.
- Ho rieseguito io i test voice_server, voice_stt e verifica_bot: **606 passed**, lo stesso numero dichiarato da te.
- Nessun antipattern del Wall of Shame introdotto: il merge non aggiunge codice nuovo rispetto a quello già revisionato da M2.

**Nota (non è una riserva):** con la risoluzione «tengo la mia versione» il branch scarta i report di sessione di main (handoff, ultimo_report, diff_sessione di M2). È la convenzione del progetto, perché sono fotografie dell'ultima sessione e lo storico resta in git. Non si perde niente del motore né dello stato vivo.

**Rischi esplicitamente esclusi:**
- Non ho eseguito la suite completa né il kernel (`gas.py`). Il merge non tocca gas.py, brains/ né modules/ fuori da voice, e la #578 aveva già girato il completo sul merge precedente. Restano da verificare con la CI (`unit-suite`, `handoff-check`).
- Non ho provato il comportamento reale del server voce o del browser con un microfono: in questo ambiente non si può riprodurre, ed è coperto dalle review M2 fino a #573-M2.

**Memoria:**
- Ho aggiunto la riga `#579 (chat Mani) — 2026-10-30 — APPROVATO — … Nessuna lezione nuova.` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, dopo #573-M2.
- Come chiesto non l'ho committata né messa in stage: va messa in stage prima del commit di merge.
- Inciampo: il mio primo tentativo di aggiungere la riga via Bash è stato bloccato dal PreToolUse `review_gate.sh` («.review_ok non corrisponde al diff staged»). Probabilmente il gate scatta sulla parola «commit» nel testo del comando. Ho scritto la riga con Edit: il file è cambiato solo nella working tree, lo stage è intatto.
- Ricorda di rigenerare il marcatore con `bash scripts/segna_review_ok.sh` dopo aver messo in stage la memoria, altrimenti il gate bloccherà il commit di merge.
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py né a scripts/. `tests/test_unit_verifica_bot.py`: da 500 (main) a 510 passed in locale. Nuovi `test_invisibile_nel_titolo_che_si_legge_uguale` (4 parametri) e `test_invisibili_come_nel_gate`; `test_controlli_bidi` da 4 a 9 parametri, senza U+202C. Suite completa in locale (Python 3.13) dopo il merge di main: `2702 passed, 2 skipped in 204.23s (prima del merge della #308; dopo: voice + bot 606 passed)` (review #578: kernel 1060 PASS / 1 FAIL, T31g, identico su main pulito: dipende dall'ambiente). Mutanti ora presi: senza lo strip prima del titolo 4 failed; ognuno dei 9 controlli bidi tolto da `_BIDI` 1 failed; un intervallo diverso dal gate 1 failed.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 19292dd, 0c6c7d1 (memoria del revisore): nessuna run (pushati insieme a b692e27).
- b692e27: run push 40966074777, `unit-suite` success e `handoff-check` failure (l'handoff era ancora quello della #305; V-3 ve #306), superata dai commit di fine-task.
- 14c4983 (fine-task, §2 senza la riga dell'handoff): nessuna run letta (pushato insieme a 204a6c1).
- 204a6c1 (fine-task): run CI 40966602638, `unit-suite` e `handoff-check` success; check `verifica-bot` neutral, review del bot APPROVATO CON RISERVE (vedi §1).
- 9ceea27 (merge di main #307): nessuna run (pushato insieme a 88427e8).
- 88427e8 (fine-task): run non letta alla scrittura dell'handoff (superata dal merge della #308).
- Merge di main #308 e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-2 ve #305 (terza) BASSA, ACCETTATA come compromesso: il controllo «invisibile accanto a una gravità» vale su tutto il testo e senza confini di parola (falsi NO prudenti).
- V-2 COSMETICA del bot su 586b888: le righe delle riserve minori non hanno un tetto dopo l'escape.
- V-1 bot / V-1 ve #306 BASSA: `test_invisibili_come_nel_gate` lega solo gli intervalli, non `_CATEGORIE_INVISIBILI`.
- V-2 bot / V-2 ve #306: l'import di modules.gate nel test funziona solo dalla radice del repo (come tests/test_unit_gate.py).
- R-572-1 (chat Mani) BASSA preesistente: i separatori di riga Unicode si tolgono invece di diventare un a capo.
- R-572-2 (chat Mani) BASSA preesistente: segni combinanti visibili e omoglifi dentro una gravità passano.
- R-575-1 (chat Mani) BASSA preesistente: `cmd_esito` non intercetta il RecursionError di json.loads (fail-closed).
- R-575-2 (chat Mani) COSMETICA: `test_annidamento_profondo` non controlla il motivo.
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, V-2/V-3 ve #296, R-546-1: BASSE della chat Mani, invariate (vedi stato_progetto).
