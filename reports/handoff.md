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

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  4 ++++
 reports/diff_sessione.md           | 13 ++++++-------
 reports/ripartenza_mani.md         |  2 +-
 reports/stato_progetto.md          |  3 ++-
 reports/ultimo_report.md           | 30 ++++++++++--------------------
 tests/test_unit_verifica_bot.py    | 19 +++++++++++++++++--
```

NB: base = merge-base con origin/main = a5b1c62. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
b692e27 test(bot): titolo con invisibile, ogni controllo bidi da solo, invisibili uguali al gate (terza verifica esterna #305, chat Mani)
0c6c7d1 chore(revisore): memoria review #577 — APPROVATO
19292dd chore(revisore): memoria review #576 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py né a scripts/. `tests/test_unit_verifica_bot.py`: da 500 (main) a 510 passed in locale. Nuovi `test_invisibile_nel_titolo_che_si_legge_uguale` (4 parametri) e `test_invisibili_come_nel_gate`; `test_controlli_bidi` da 4 a 9 parametri, senza U+202C. Suite completa in locale (Python 3.13): `2675 passed, 2 skipped in 192.07s`. Mutanti ora presi: senza lo strip prima del titolo 4 failed; ognuno dei 9 controlli bidi tolto da `_BIDI` 1 failed; un intervallo diverso dal gate 1 failed.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 19292dd, 0c6c7d1 (memoria del revisore) e b692e27: pushati insieme prima dell'apertura della PR #306; nessuna run sulla PR per questi SHA.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-2 ve #305 (terza) BASSA, ACCETTATA come compromesso: il controllo «invisibile accanto a una gravità» vale su tutto il testo e senza confini di parola (falsi NO prudenti).
- V-2 COSMETICA del bot su 586b888: le righe delle riserve minori non hanno un tetto dopo l'escape.
- R-572-1 (chat Mani) BASSA preesistente: i separatori di riga Unicode si tolgono invece di diventare un a capo.
- R-572-2 (chat Mani) BASSA preesistente: segni combinanti visibili e omoglifi dentro una gravità passano.
- R-575-1 (chat Mani) BASSA preesistente: `cmd_esito` non intercetta il RecursionError di json.loads (fail-closed).
- R-575-2 (chat Mani) COSMETICA: `test_annidamento_profondo` non controlla il motivo.
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, V-2/V-3 ve #296, R-546-1: BASSE della chat Mani, invariate (vedi stato_progetto).
