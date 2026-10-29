# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — chat Motore: riserve della PR #293 (PR #295), dopo il merge di main con la PR #292

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #295 (https://github.com/Gasss23/Gas/pull/295): l'operatore ha già detto «mergia #295». La mergio io appena CI e bot sono verdi sul nuovo head. Numero e URL dalla risposta JSON dello strumento GitHub `create_pull_request` (`gh` non autenticato in questo ambiente).
2. Due sessioni «chat Motore» lavorano sullo stesso codice (#292 e #295): conviene tenerne una sola.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — PR #293**: `FATTA` — mergiata.
- **Fetta 2 — V-1 bot #293, GAS_CLAUDE_BIN scavalcato**: `FATTA` dalla PR #292 (confronto col valore del `.env`); il mio WARN dedicato è stato tolto nel merge perché doppione.
- **Fetta 3 — V-1 bot #293 secondo giro, messaggi sul giro del timer**: `FATTA`.
- **Fetta 4 — R-543-1, interruttore come flag**: `FATTA` — `_DOTENV_INTERRUTTORI`.
- **Fetta 5 — R-543-2, GAS_NO_DOTENV dichiarato**: `FATTA` (solo dichiarato: V-1 bot #295 la considera mitigata, non chiusa).
- **Fetta 6 — nota #549 e R-551-1, chiavi ripetute**: `FATTA` — `visti`, combinato col registro dei valori della #292.
- **Fetta 7 — V-4 e V-2 bot #293, test**: `FATTA`.
- **Fetta 8 — Merge di main (PR #292)**: `FATTA` — review #553 APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 gas.py                             |  26 +++++++++++++++++++-----
 reports/diff_sessione.md           |  19 +++++++-----------
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  32 ++++++++++++-----------------
 tests/test_unit_dotenv.py          |  64 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_kernel.py          |   9 ++++++---
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d» e niente riga di totale. Conteggi presi con i report in stage.

## §3 GIT LOG --ONELINE (sessione)

```
5867d54 Merge origin/main (PR #292) in feat/merge-automatico-z1xjx2 (PR #295) — tenuti registro dei valori e visti; GAS_CLAUDE_BIN diverso coperto da _avviso_claude_timer — review #553 APPROVATO
b83e8d2 docs(fine-task): PR #295 — riserve della #293, review #551/#552
d915ec5 fix(doctor): riserve della #293 — GAS_CLAUDE_BIN scavalcato, interruttore come flag, chiavi ripetute, GAS_NO_DOTENV dichiarato, messaggi sul giro del timer
0be9d5a chore(revisore): memoria review #552 — APPROVATO
dbbafe9 chore(revisore): memoria review #551 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #551 (chat Motore) — sul diff di d915ec5 (prima della correzione di R-551-1)

## VERDETTO: APPROVATO CON RISERVE

Review #551 (chat Motore). Diff staged su feat/merge-automatico-z1xjx2: gas.py, tests/test_unit_dotenv.py, tests/test_unit_kernel.py. Prima della review ho letto CLAUDE.md (§5), reports/stato_progetto.md (riga 589: R-543-1, R-543-2, nota #549) e la memoria.

**Cosa ho controllato nel diff**
- `gas.py:631`: se una chiave ripetuta è già in `caricate`, viene saltata. Rischio: cambia il caricamento? No. Il ramo era già un `continue` che non toccava né `caricate` né `os.environ`. Il caricamento non sovrascrive mai, il valore di ritorno è lo stesso, nessun valore viene salvato. Esito: ok. Il salto copre però solo le chiavi che non stavano nella shell (vedi R-551-1).
- `gas.py:633`: confronto con le regole di `_env_flag`, attivo solo se la chiave è in `gas.py:579` `_DOTENV_INTERRUTTORI = frozenset({"GAS_CLAUDE_CLI"})`. Tutte le altre chiavi, compresa GAS_CLAUDE_BIN, restano confrontate come testo. Prove: «1» contro «yes» va in CARICATE; «» contro «0» va in CARICATE; «x» contro «no» va in CARICATE (sono tutti spenti, quindi è corretto). Esito: ok, R-543-1 chiusa.
- `gas.py:5022`: con GAS_NO_DOTENV il doctor aggiunge «(.env non letto: GAS_NO_DOTENV attivo)» sia all'OK «spento» sia al WARN «acceso». Esito: ok, R-543-2 chiusa: l'OK ora dichiara il suo limite.
- `gas.py:5033`: il WARN del ramo «acceso» dice «il .env lo spegne» quando la chiave è in SCAVALCATE. Esito: ok.
- `gas.py:5043`: WARN dedicato per GAS_CLAUDE_BIN scavalcato. Viene prima di `_avviso_claude_timer`, quindi sparisce il consiglio sbagliato «metti … nel .env». Esito: ok, V-1 bot #293 chiusa.
- `tests/test_unit_kernel.py:11229`: T99w/T99x salvano e poi rimettono com'era l'appartenenza ai due insiemi. Esito: ok, V-4 chiusa.
- `tests/test_unit_dotenv.py:151` e `tests/test_unit_dotenv.py:171`: test nuovi, il secondo fa `_carica_dotenv` e poi il doctor sullo stesso `.env`, senza scrivere i set a mano. Mutanti miei:
  - confronto da flag tolto: 2 failed;
  - salto delle chiavi ripetute tolto: 1 failed;
  - gas.py ripristinato in entrambi i casi (nessuna differenza nel working tree).

  Esito: ok.

**Test rifatti da me:** kernel 1063 PASS, 0 FAIL (T99w e T99x PASS); tests/test_unit_dotenv.py 14 passed.

**Riserva**
- **R-551-1 BASSA**: falso OK nel verso NON prudente, che hai chiesto di cercare. Il problema esisteva già prima, ma il fix della nota #549 lo chiude solo in parte. `caricate` contiene solo le chiavi che il `.env` ha messo in `os.environ`. Se la chiave è già nella shell, la seconda riga del `.env` viene confrontata di nuovo. Prova eseguita: shell `GAS_CLAUDE_CLI=1`, `.env` con `GAS_CLAUDE_CLI=0` e poi `GAS_CLAUDE_CLI=1`. Risultato: la chiave finisce sia in CARICATE sia in SCAVALCATE. Il ramo «acceso» guarda solo CARICATE, quindi il doctor non dà nessun WARN. Il giro del timer invece prende la prima riga (0) e il forte resta spento. Nel verso opposto (shell 0, `.env` 1 poi 0) il WARN c'è.
  - Rimedio: un insieme `visti` con le chiavi di questo `.env`, saltate alla seconda comparsa a prescindere dalla shell.
  - Il commento di `gas.py:632` («la shell non c'entra») va corretto di conseguenza.
  - Per GAS_CLAUDE_BIN non succede: il controllo su SCAVALCATE a `gas.py:5043` viene prima.

**Cosa non ho verificato**
- Il comportamento reale di launchd sul Mac con `~/.zshenv`, e del giro lanciato da Telegram che eredita la shell: non si può riprodurre in dev. Ho controllato solo che i messaggi siano coerenti col commento.
- Il doctor con le chiavi vere dei provider: nei test sono tolte.

Wall of Shame: nessuno slicing della history, nessuna simulazione di tool. Le eccezioni dei provider non sono toccate.

Memoria aggiornata: riga #551 più una lezione (sondare la chiave ripetuta con la shell uguale alla seconda riga). Committata con lo script in dbbafe9 (/home/user/Gas/.claude/agents/memoria_revisore.md). Il diff staged è intatto.

### Review #552 (chat Motore) — sul diff finale di d915ec5 (con la correzione di R-551-1)

## VERDETTO: APPROVATO

Review #552 (chat Motore). Ho esaminato il diff staged su feat/merge-automatico-z1xjx2 (3 file: gas.py, tests/test_unit_dotenv.py, tests/test_unit_kernel.py). Prima ho letto CLAUDE.md §5, stato_progetto e la memoria (#551 e la lezione R-551-1).

Elementi del diff esaminati:
- `gas.py:610`: crea l'insieme `visti` dentro `_carica_dotenv`, quindi uno nuovo a ogni chiamata. Rischio esaminato: stato che resta tra una chiamata e l'altra. Esito: ok.
- `gas.py:631`: con `if chiave in visti: continue` si salta la seconda comparsa di una chiave, che sia nella shell o no. Il controllo sta DOPO la validazione della riga: se la prima riga è malformata o ha virgolette non chiuse, non conta come chiave vista e vale la riga valida successiva. Rischio esaminato: un cambio nel caricamento. Esito: ok. Il vecchio `if chiave in caricate` saltava solo le chiavi non presenti nella shell. Per quelle `os.environ` viene scritto solo alla prima comparsa, come prima. `caricate` non riceve mai una chiave due volte, quindi il valore di ritorno non cambia. Nessun valore viene salvato in nessun insieme. L'unico comportamento che cambia è quello voluto: con la chiave nella shell, la seconda riga non viene più confrontata. Il commento («per il timer vale la prima») è corretto.
- `gas.py:635`: il confronto come flag per `_DOTENV_INTERRUTTORI` usa lo stesso insieme di valori di `_env_flag` (`gas.py:566`: 1/true/on/yes/si). Rischio esaminato: le due regole potrebbero divergere. Esito: ok. Parte invariata rispetto a #551.
- `tests/test_unit_dotenv.py:164`: nuovo caso R-551-1. Shell `GAS_CLAUDE_CLI=1`, `.env` con «=0» e poi «=1»: SCAVALCATE vale {GAS_CLAUDE_CLI} e la chiave non è in CARICATE. Rischio esaminato: test che non morde. Esito: ok. Mutante (salto con `visti` disattivato) → `test_interruttori_confrontati_come_flag_e_chiavi_ripetute` FAIL (1 failed, 13 passed). Poi gas.py ripristinato; l'index è invariato e non ci sono modifiche non in staging.
- Resto del diff (WARN del doctor `gas.py:5021-5050`, ripristino degli insiemi in `tests/test_unit_kernel.py:11228`): identico a quanto approvato in #551. Esito: ok.

Esecuzione: tests/test_unit_dotenv.py 14 passed; kernel 1063 PASS, 0 FAIL (rilanciato da me). Wall of Shame: nessuno slicing della history, nessuna simulazione dei tool.

Rischio escluso: non ho verificato il comportamento reale del giro launchd sul Mac (solo `.env` più ~/.zshenv), perché in dev non si riproduce. La frase «per il timer vale la prima» si regge sul fatto che il timer usa lo stesso `_carica_dotenv` senza la variabile nella shell: l'ho dedotto dal codice, non l'ho osservato.

Riga contatore #552 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata (0be9d5a, solo quel file; lo staging resta intatto). Nessuna lezione nuova.

### Review #553 (chat Motore, sessione PR #295) — sul merge di origin/main (PR #292) in 5867d54

## VERDETTO: APPROVATO

Review #553 (chat Motore, sessione PR #295): merge di origin/main dc43ad6 (PR #292) in feat/merge-automatico-z1xjx2. Ho esaminato `git diff --cached HEAD` e `git diff --cached origin/main`.

**Parti del diff controllate**
- `gas.py:651` — `_DOTENV_NEL_FILE.setdefault` è scritto prima del salto con `visti`. Rischio: che il registro del doctor e il loader leggano righe diverse quando una chiave è ripetuta. Il registro tiene la prima riga grazie a `setdefault`. `visti` fa saltare la seconda comparsa prima di toccare `os.environ`, `CARICATE` e `SCAVALCATE`. Quindi l'ordine fra le due righe non conta: la prima riga vince in tutti e due i registri. Le righe malformate vengono scartate prima di entrambe. Esito: ok.
- `gas.py:653` — `visti.add` sta dopo la validazione della riga e dopo il registro, come era nel ramo (#552). Il confronto come interruttore per `_DOTENV_INTERRUTTORI` è rimasto intatto (`gas.py:656`), e così `_DOTENV_CARICATE.update` (`gas.py:666`). Rischio: che una riga della #293 sia andata persa nel merge. Il diff verso main contiene solo le aggiunte del ramo, il diff verso HEAD solo quelle di main. Esito: ok.
- `gas.py:5067` — nel doctor non c'è più il ramo `elif "GAS_CLAUDE_BIN" in _DOTENV_SCAVALCATE`. Al suo posto `_avviso_claude_timer` riceve `_DOTENV_NEL_FILE.get("GAS_CLAUDE_BIN")`. Rischio: un caso non più coperto, oppure rami morti. Il caso «shell diversa dal .env» è coperto da `gas.py:463` («ha un altro valore», col valore del file). Se il valore è uguale non c'è WARN, ed è giusto. `_DOTENV_SCAVALCATE` ora la legge solo GAS_CLAUDE_CLI (`gas.py:5047`, `gas.py:5056`), e il commento di `gas.py:588-591` è aggiornato. Non ci sono rami doppi né morti. Unico caso limite, che c'è già in main: se `which` non trova il binario esce solo il WARN «non trovato», senza «altro valore». Esito: ok.
- `tests/test_unit_dotenv.py:236` — il test dal `.env` al doctor si aspetta «ha un altro valore» e «/vecchio/claude». Rischio: un test che passa per caso, con registri sporchi da un test precedente. Ogni scenario azzera `_DOTENV_NEL_FILE` con monkeypatch (`tests/test_unit_dotenv.py:185`, `tests/test_unit_dotenv.py:197`, `tests/test_unit_dotenv.py:216`). Esito: ok.
- `tests/test_unit_kernel.py:11206` — T99s salva e rimette `_DOTENV_NEL_FILE`, che arriva da main ed è identico. Esito: ok.

**Memoria e stato**
- `.claude/agents/memoria_revisore.md`: non perde nessuna riga di nessuno dei due genitori e non ne ha di inventate.
- `reports/stato_progetto.md`: cambiano solo 2 righe, ed è previsto. La riga 4 è la voce del ramo seguita dalla riga 4 intera di main (verificato confrontando le stringhe). Il punto 3 (riga 589) è il testo di main con aggiunte tre frasi del ramo prima di «Storia:» («PR #293 mergiata…», la voce PR #295 col nuovo testo su V-1 bot #293, «Aperto: ~/.zshenv»).
- Nessun marcatore di conflitto; `git diff --cached --check` è pulito.

**Test rilanciati da me**: suite del kernel 1063 PASS, 0 FAIL; `tests/test_unit_dotenv.py` 17 passed.

**Nota COSMETICA** (non blocca): a `tests/test_unit_dotenv.py:155` c'è una sola riga vuota prima di `def test_nomi_caricati…` (è l'R-551-1 cosmetica dell'altra chat, arrivata da main). La sigla R-551-1 ha due significati nelle due chat: una è chiusa (`visti`), l'altra è aperta (la spaziatura).

**Cosa non ho verificato**: non ho fatto test mutanti in questo merge, perché il codice è identico a quello già passato da mutanti nelle review #548 e #552. Non ho verificato il comportamento reale del timer sul Mac: dal container non si può riprodurre. Non ho rivisto handoff, ultimo_report e diff_sessione: sono la versione del ramo e li riscrive il fine-task.

**Memoria del revisore: il commit è FALLITO per il merge in corso.** La riga #553 è scritta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` (working tree), ma NON è in staging e NON è committata. `scripts/commit_memoria_revisore.sh` ha restituito exit 0 e ha registrato in gas_debug.log «git commit -o … fallito (rc=128): fatal: cannot do a partial commit during a merge». Prima di chiudere il merge serve `git add .claude/agents/memoria_revisore.md`, così la riga entra nel commit di merge.

## §5 DELTA TEST DEL MOTORE

Suite kernel sulla testa `5867d54`: 1063 PASS, 0 FAIL (nessun check nuovo nel kernel in questa PR; il valore di main `dc43ad6` non l'ho rimisurato).

```
=== RIEPILOGO: 1063 PASS, 0 FAIL ===
```

pytest (tutti i file tranne la suite kernel), sulla testa `5867d54`: `2291 passed, 104 skipped in 197.76s (0:03:17)`; `tests/test_unit_dotenv.py` 17 passed.

## §6 STATO CI

CI letta con lo strumento GitHub della sessione: `gh run list` non è disponibile (`gh` non autenticato).

Mappatura commit→run:
- `d915ec5`: nessuna run letta (pushato prima dell'apertura della PR #295).
- `b83e8d2`: `unit-suite`, `handoff-check`, `verifica-bot` success (bot APPROVATO CON RISERVE: V-1 R-543-2 solo dichiarata, V-2 percorso del `.env` non controllato — ora coperto dalla #292, V-3 COSMETICA lista dei valori veri duplicata); verifica esterna APPROVATO CON RISERVE (commento 6484390024).
- `5867d54`: nessuna run su questo SHA (pushato insieme al commit di fine-task).
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-1 bot #295 BASSA: con `GAS_NO_DOTENV` e forte spento il doctor dà OK con la sola nota (R-543-2 mitigata, non chiusa).
- V-3 bot #295 / V-1 ve #295 BASSA: la lista dei valori veri è copiata da `_env_flag` invece di stare in una costante comune.
- V-2 ve #295 BASSA: il confronto «come flag» vale solo per GAS_CLAUDE_CLI, e il commento non lo dice.
- `~/.zshenv` non considerato (falso WARN, verso prudente).
- Sigle R-543-1 e R-551-1 con significati diversi nelle due sessioni «chat Motore» (COSMETICA).
