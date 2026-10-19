# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-19 — Fetta di pulizia (R-345-3, R-bot210-3, test più robusti, terza prova sul Mac)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #217 (https://github.com/Gasss23/Gas/pull/217): lo decide l'operatore domani, se CI, bot e verifica esterna sono positivi. L'agente NON mergia.
2. Branch `fix/crm-idemp-diario` (1 commit di sola documentazione fuori da main, luglio): cancellabile, decide l'operatore.
3. Discussione a voce sulla roadmap: traccia in `reports/roadmap_sintesi.md`.

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Terza prova sul Mac e note di #216 in stato_progetto**: `FATTA`.
- **R-345-3 (tutte le lezioni in attesa su Telegram)**: `FATTA` — più R-359-1 (`max` con quelle del giro).
- **R-bot210-3 (prefisso di copia col punto)**: `FATTA`.
- **Test più robusti (T92d3 finally, T92d4, T91d)**: `FATTA`.
- **Ispezione branch vecchi**: `FATTA` — solo rapporto, niente cancellato.
- **Roadmap in una pagina**: `FATTA`.
- **V-1 verifica esterna #217 (prefissi di copia ripetuti, separatori iniziali)**: `FATTA` — review #361/#362.
- **Secondo giro su fdf001c (copie di .config, riga lezioni nei soli conteggi, T92d3, nomi leggibili)**: `FATTA` — review #363.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 modules/gate/gate.py               |  11 +++++++++--
 modules/notte/notte.py             |  50 ++++++++++++++++++++++++++++++++++++++------------
 reports/diff_sessione.md           |  15 +++++++++------
 reports/handoff.md                 | 264 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------
 reports/roadmap_sintesi.md         |  25 +++++++++++++++++++++++++
 reports/stato_progetto.md          |  15 +++++----------
 reports/ultimo_report.md           |  27 +++++++++++++++------------
 tests/test_unit_gate.py            |  24 ++++++++++++++++++++----
 tests/test_unit_kernel.py          |  39 ++++++++++++++++++++++++++++++---------
 tests/test_unit_notte.py           |  62 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 11 files changed, 358 insertions(+), 179 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
227d5c8 fix(pulizia): copie di .config, riga lezioni anche nei soli conteggi (note bot e verifica #217)
79fff6c chore(revisore): memoria review #363 — APPROVATO
fdf001c docs(fine-task): report e handoff — V-1 verifica esterna #217
5d90626 fix(gate): prefissi di copia ripetuti e separatori iniziali (V-1 verifica esterna #217)
df0bb27 chore(revisore): memoria review #362 — APPROVATO
776a3f4 chore(revisore): memoria review #361 — APPROVATO CON RISERVE
ec644b8 docs(fine-task): report, handoff e roadmap in una pagina — fetta di pulizia #217
44fc4ae fix(pulizia): lezioni in attesa tutte su Telegram, prefisso di copia col punto, test più robusti
9db0883 chore(revisore): memoria review #360 — APPROVATO
ef9456f chore(revisore): memoria review #359 — APPROVATO CON RISERVE
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #359

```
## VERDETTO: APPROVATO CON RISERVE

Review n. 359. La riga contatore è in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata da sola nel commit ef9456f. Lo staging del diff non è stato toccato.

**Cosa ho esaminato nel diff**
- `modules/gate/gate.py:340` — `_COPIA_PREFISSO` ora accetta anche il punto (`[-_ .]+`). Rischi esaminati: falsi positivi e regressioni. Ho fatto una prova di mutazione: rimesso il vecchio `[-_ ]+`, falliscono 4 test del gate. Ho ripristinato il file, l'index è intatto. I falsi positivi coperti dai test (`old.keyboard.md`, `dati/old.keys.md`, `new.tokenizer.json`, `old.keyboard/x.md`) restano liberi. Esito: ok.
- `modules/notte/notte.py:381` — `_lezioni_in_attesa`. Rischio esaminato: memoria rotta. Non solleva mai eccezioni e ritorna None se kernel o memoria mancano. Ma vedi R-359-1. Esito: riserva.
- `modules/notte/notte.py:364` — la frase «(di cui K di stanotte)» compare solo se `0 < nuove < lezioni`. La variante `solo_conteggi` non usa il nuovo conteggio, come dichiarato. Esito: ok.
- `modules/notte/notte.py:528` — il conteggio usa l'ultimo kernel creato nel giro: `kernel` parte da None, quindi senza compiti si ripiega sul conteggio di stanotte. Se l'ultima creazione del kernel fallisce, resta valido il kernel precedente. Il calcolo è dentro il lock, ma è solo una SELECT veloce. Esito: ok.
- `tests/test_unit_kernel.py:9044` — T92d3 ora rimette a posto il file rinominato in un `finally`. T92d4 controlla che un `sources.yaml` malformato resti WARNING, e anche quello viene ripristinato in un `finally`. T91d prova il denominatore max di `_lezione_simile` in entrambi i versi (4 parole su 10 → None, 4 su 5 → id 8). L'assegnazione morta di `_c92_prima` è stata tolta senza effetti: quella che conta, dopo il punto (2b), è rimasta. Esito: ok.
- Antipattern del Wall of Shame: nessuno slicing della history, nessuna simulazione di output dei tool. Il cap delle 10 iterazioni e `_get_window` non sono toccati.

**Test che ho rieseguito**: kernel 893 PASS / 0 FAIL; `tests/test_unit_gate.py` + `tests/test_unit_notte.py` 669 passed. Coincidono con quanto dichiarato.

**Finding**
1. **R-359-1 (BASSA)**: `lista_lezioni` in `modules/memory/store.py` gestisce già da sé gli errori del database e in quel caso ritorna una lista vuota invece di sollevare. Con un database rotto `_lezioni_in_attesa` dà quindi 0, non None. Il ripiego «conta solo quelle di stanotte» non scatta mai, e la riga «Lezioni da approvare» sparisce anche se stanotte sono state proposte lezioni. Il test usa una memoria finta che solleva, cosa che la memoria reale non fa. Lo stesso problema c'è se il totale in attesa è minore di quelle di stanotte (per esempio un'approvazione fatta durante la notte). Rimedio: `lezioni = max(nuove, lezioni_in_attesa)` quando il totale non è None, più un test con un database davvero illeggibile. Va annotata anche in `reports/stato_progetto.md`, perché lì oggi c'è scritto «memoria rotta → conta solo quelle del giro», che non è del tutto vero.
2. **COSMETICA**: il test Telegram con memoria reale copre il caso «3 (di cui 2 di stanotte)». Nessun test con kernel reale copre il caso «solo lezioni vecchie, 0 stanotte» (la riga senza «di cui»). C'è solo il test sulla funzione pura con `lezioni_in_attesa=4`.

**Cosa non ho verificato**
- Invio Telegram reale e notte sul Mac con provider veri: non riproducibili qui, i test usano client e notifiche finti.
- Suite completa `pytest tests/` (1428): non l'ho rieseguita. Mi sono fidato del dato dichiarato per i file fuori dal diff.

Lezione nuova (salvata in memoria): prima di scrivere un ripiego «se la memoria è rotta → None», controllare se il metodo chiamato gestisce già da sé gli errori e restituisce un vuoto. Altrimenti il vuoto si confonde con «zero» e il ripiego non scatta mai.
```

### Review #360

```
## VERDETTO: APPROVATO

Review n. 360: è la ri-review della #359 sul diff staged aggiornato. Nessuna riserva aperta: R-359-1 e la nota cosmetica sono chiuse. Riga contatore aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata da sola (9db0883); il diff in staging non l'ho toccato.

**Cosa ho controllato**
- `modules/notte/notte.py:365` — ora `lezioni = nuove if lezioni_in_attesa is None else max(nuove, lezioni_in_attesa)`. Il rischio era R-359-1: `lista_lezioni` restituisce una lista vuota anche quando il database è rotto, e la riga «Lezioni da approvare» spariva. Adesso il numero non scende mai sotto le lezioni di stanotte. Ho provato a togliere il `max`: 1 test fallisce. Poi ho rimesso il file com'era e l'index è intatto. Esito: ok.
- `modules/notte/notte.py:366` — il «(di cui K di stanotte)» compare solo se `0 < nuove < lezioni`. Col `max` il caso «totale minore delle lezioni di stanotte» non esiste più, quindi la frase non può mai dire una cosa sbagliata. Esito: ok.
- `tests/test_unit_notte.py:1099` (circa) — c'è un nuovo caso con `lezioni_in_attesa=0` e 2 lezioni di stanotte, che deve dare «2». Esito: ok.
- `tests/test_unit_notte.py:1104` (circa) — nuovo `test_telegram_solo_lezioni_vecchie`: kernel reale, una sola lezione vecchia, deve uscire «Lezioni da approvare: 1 —» senza «di cui». La riflessione è spenta dalla fixture comune (`tests/test_unit_notte.py:37` imposta `GAS_RIFLESSIONE_AUTO=0`), quindi il test non dipende da un default implicito. Esito: ok.
- Il resto del diff (gate, test del kernel, stato_progetto) è uguale a quello della #359, già approvato lì. Nessuno slicing della history, nessuna simulazione di output dei tool, guardrail non toccati.

**Test rieseguiti**: notte 64 passed.

**Cosa non ho verificato**
- Non ho rieseguito la suite del kernel (893) né quella del gate, perché i file relativi non sono cambiati dalla #359, dove li avevo già rieseguiti.
- L'invio reale su Telegram e la notte sul Mac con provider veri non si possono riprodurre qui.
- Ho controllato solo con grep che `reports/stato_progetto.md` contenga R-359-1, non ne ho riletto il testo.

Nessuna lezione nuova.
```

### Review #361

```
## VERDETTO: APPROVATO CON RISERVE

Review #361. Diff staged su feat/merge-automatico-z1xjx2 (PR #217): 2 file, +9/-3.

Ho letto prima CLAUDE.md (sez. 5, 8, 10), le voci gate/V-1 in reports/stato_progetto.md e .claude/agents/memoria_revisore.md (le ultime voci, fino alla #360).

Elementi del diff esaminati:
- `modules/gate/gate.py:342`: `_COPIA_PREFISSO = rf"\.?(?:{_PAROLE_COPIA}[-_ .]+)*+"`. Ora i prefissi di copia si possono ripetere e il punto iniziale è opzionale.
  - Rischio di ReDoS (blocco della regex su input costruiti apposta): escluso. Il gruppo esterno è possessivo, le parole di copia hanno già `[0-9]*+` e ogni giro richiede almeno un separatore, quindi non c'è backtracking annidato. Ho provato 7 input avversari fino a 255 caratteri (`old.`×60, `copy_`×50+`keyz`, `. `×120+`keys!`, lunghe serie di separatori): ognuno sotto 1e-5 s. Oltre 255 caratteri il pezzo viene negato prima di arrivare alla regex.
  - Rischio di un falso negativo dovuto al possessivo: escluso. Nessun nome bersaglio (`tokens/keys/passwd/shadow/gh`) comincia con una parola di copia o con un separatore, quindi il prefisso non può mangiarsi il nome.
  - Esito: ok.
- `tests/test_unit_gate.py:651`: 6 nuovi casi negati (`old.old.keys/a`, `old_old_keys/a`, `copy_old.keys/a`, `.old.keys/a`, `.keys/a`, `.tokens/x`).
  - Rischio: test che passano anche col fix tolto. Ho fatto due mutazioni: col vecchio prefisso `(?:…)?` falliscono 6 test, senza `\.?` ne falliscono 3. Il file è stato ripristinato e il diff non staged è vuoto.
  - Esito: ok.
- `tests/test_unit_gate.py:682`: 3 nuovi casi leggibili (`.keyboard.md`, `old.old.keynote.md`, `.tokenizer.json`).
  - Rischio: falsi positivi. Ho sondato anche altri nomi e restano leggibili: `news_keys/a`, `old_keyring/a`, `new.tokens.py`, `dati/.keys.md`, `notes/.keyboard`, `a/.keys/readme.md` (la documentazione dentro una cartella di chiavi resta leggibile), `oldkeys/a`.
  - Esito: ok.
- Contesto: `modules/gate/gate.py:347` `_nome_con_copie` usa il prefisso per tre regex (ultimo pezzo, cartella di chiavi, `.config/gh`).
  - Effetti collaterali: `.config/.gh/hosts.yml`, `.passwd` e `.shadow` come ultimo pezzo ora sono negati. Sono più restrittivi e innocui.
  - Esito: ok.

Numeri riprodotti da me: test del cancello 615 passed; `pytest tests` completo 1438 passed in 147 s.

Il punto iniziale è coerente: `.keys/` e `.tokens/` sono il modo normale di nascondere una cartella di chiavi, quindi negarli rientra nello stesso criterio di D5 (copie di cartelle e file di chiavi). L'ultimo pezzo non perde il punto iniziale, perché `rstrip(". ")` toglie solo punti e spazi finali.

Riserve:
- **R-361-1 (BASSA)**: `..keys/a` e `._keys/a` restano LEGGIBILI (verificato: `lettura_consentita` → True). Il motivo: c'è un solo `\.?` e il `_` subito dopo il punto non è preceduto da una parola di copia. Possibili rimedi:
  - `[-_ .]*` all'inizio al posto di `\.?` (è sempre possessivo, quindi resta lineare), con 2 test;
  - oppure dichiarare il limite.
  
  `._x` sono i file AppleDouble di macOS: contengono solo metadati, quindi il rischio reale è basso. Va tracciata in stato_progetto.md.

Rischio escluso: non ho verificato il comportamento del cancello sul percorso RISOLTO dei symlink nel kernel (`gas.py`), né la suite kernel `tests/test_unit_kernel.py` come script a sé. Il diff non tocca `gas.py` e le funzioni pubbliche (`lettura_consentita`, `livello_scrittura`) mantengono la stessa firma. Non ho verificato nemmeno il comportamento su Mac/VPS, dove i nomi possono differire per normalizzazione Unicode (NFD).

Memoria aggiornata: ho aggiunto la riga #361 con la lezione «quando si rende ripetibile un prefisso, sondare anche le forme degeneri del separatore iniziale (`..x`, `._x`)». È committata con `scripts/commit_memoria_revisore.sh` (commit 776a3f4), file /home/user/Gas/.claude/agents/memoria_revisore.md.

File rilevanti: /home/user/Gas/modules/gate/gate.py, /home/user/Gas/tests/test_unit_gate.py
```

### Review #362

```
## VERDETTO: APPROVATO

Review #362, ri-review della #361 sul diff staged aggiornato (PR #217). R-361-1 è chiusa.

Elementi del diff esaminati:
- `modules/gate/gate.py:342` — `_COPIA_PREFISSO = rf"[-_ .]*+(?:{_PAROLE_COPIA}[-_ .]+)*+"`: ora accetta una serie qualsiasi di separatori iniziali.
  - ReDoS: escluso. I due quantificatori sono possessivi e la parola di copia non comincia con un separatore, quindi non ci sono modi ambigui di dividere la stringa. 4 input avversari fino a 255 caratteri (serie `-_ .`, punti con `old`, underscore con `copy`, `. ` con `keys!`) restano sotto 1e-5 s.
  - Falso negativo dovuto al possessivo: escluso. Nessun nome bersaglio comincia con un separatore.
  - Esito: ok.
- `tests/test_unit_gate.py:654` — aggiunti i casi negati `..keys/a` e `._keys/a`.
  - Mutazione: rimettendo il `\.?` della #361 falliscono 2 test, quindi i casi nuovi servono davvero. File ripristinato, diff non staged vuoto.
  - Esito: ok.
- `tests/test_unit_gate.py:682` — casi leggibili invariati rispetto alla #361.
  - Falsi positivi, sondati a mano. Restano leggibili: `_keyboard.md`, `..keynote.md`, `._readme.md`, `._keys.md`, `news_keys/a`, `old_keyring/a`, `.keyboard.md`, `a/..keys/readme.md`. Sono negati, ed è corretto: `_keys/a`, `-keys/a`, `._old_.keys/a`, `x/_tokens`.
  - Esito: ok.
- Contesto: `modules/gate/gate.py:347` — `_nome_con_copie` applica lo stesso prefisso a ultimo pezzo, cartella di chiavi e `.config/gh`. Su `.config/` l'effetto è più restrittivo (fail-closed), quindi innocuo. Esito: ok.

Numeri riprodotti da me: gate 617 passed; `pytest tests` 1440 passed.

Nota COSMETICA, non bloccante: i tre nomi che dichiari leggibili (`_keyboard.md`, `..keynote.md`, `._readme.md`) li ho verificati solo a mano. Non sono tra i parametri di `test_nomi_simili_a_chiavi_restano_leggibili`, quindi un test non li protegge.

Rischio escluso: non ho verificato la normalizzazione Unicode dei nomi su Mac (NFD) né il percorso del cancello sui symlink risolti in `gas.py`. Il diff non tocca `gas.py` e le firme pubbliche restano uguali.

Memoria: riga #362 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata (df0bb27).

File rilevanti: /home/user/Gas/modules/gate/gate.py, /home/user/Gas/tests/test_unit_gate.py
```

---

### Review #363

```
## VERDETTO: APPROVATO

Review #363, ri-review del diff staged su feat/merge-automatico-z1xjx2 (PR #217, head fdf001c). Ho fatto le letture obbligatorie (CLAUDE.md sez. 5, stato_progetto per la PR #217, memoria fino alla #362).

**Parti del diff esaminate**
- `modules/gate/gate.py:388` — la regola D3 ora riconosce anche le copie della cartella genitore (`old.config`, `.old.config`, `.config.bak`, `.config copy`) prima di `gh`. La cartella `config` senza punto resta esclusa. Rischio esaminato: falsi positivi e input pesanti per la regex. Sonde: `config.bak/gh`, `_config/gh` e `config2/gh` vengono negati, cioè bloccati per prudenza; va bene. `myconfig/gh`, `nconfig/gh`, `.configs/gh/x.md` e `.config/ghost/x` restano leggibili. Il controllo è ancorato con `^…$`. 4 input avversari fino a 255 caratteri restano sotto 5e-6 s. Mutazioni: tornando alla vecchia condizione `a == ".config"` falliscono 5 test; togliendo `a != "config"` fallisce 1 test. — ok
- `modules/gate/gate.py:364` — nuova `_COPIA_CONFIG_RE = _nome_con_copie(r"config")`. Rischio esaminato: il punto nel nome. Senza punto è corretto, perché il prefisso possessivo `[-_ .]*+` assorbe già il punto iniziale. — ok
- `modules/notte/notte.py:338` — la riga «Lezioni da approvare» viene calcolata prima del ramo `solo_conteggi` e compare in entrambe le versioni del messaggio. Il `max(nuove, lezioni_in_attesa)` di R-359-1 resta invariato. Rischio esaminato: la versione corta deve restare sotto il limite di Telegram. Si allunga di circa 70 caratteri; il test esistente col limite a 230 passa. Mutazione: togliendo `riga_lezioni` dai soli conteggi fallisce 1 test di notte. — ok
- `modules/notte/notte.py:425` — `_notifica_telegram` passa `lezioni_in_attesa` anche al messaggio corto di ripiego. Resta dentro il try/except che logga in gas_debug.log, quindi il comportamento senza crash non cambia. — ok
- `tests/test_unit_kernel.py:9087` — T92d3 ora controlla «sources.yaml» per intero su `_c92_prima`. Ho verificato in `tests/test_unit_kernel.py:9051` che `_c92_prima` viene catturata dopo il caso 2a (file assente) e prima del 2c (file malformato): l'ordine è corretto. — ok
- `tests/test_unit_gate.py:655` e `tests/test_unit_gate.py:688` — aggiunti 5 casi negati e 5 leggibili (chiusa anche la COSMETICA della #362). — ok

**Riprodotti**: gate+notte 691 passed, kernel 893 PASS / 0 FAIL, pytest tests/ 1450 passed. Coincidono con i numeri del coordinatore. Dopo le mutazioni il working tree è stato ripristinato (`git diff` vuoto) e lo staged è intatto (5 file, +38/-15).

**Wall of Shame**: nessuno slicing della history, nessuna simulazione di output dei tool, guardrail (10 iterazioni, 8k, `_get_window`) non toccati.

**Rischio escluso**: non ho verificato la consegna reale su Telegram del messaggio corto con la riga lezioni. Serve il bot e un giro notturno reale, non riproducibile in dev; la lunghezza è coperta solo dal test col limite ridotto.

**Note BASSE/COSMETICHE**: nessuna.

Memoria aggiornata con la riga #363 e committata da `scripts/commit_memoria_revisore.sh` (commit 79fff6c, solo `/home/user/Gas/.claude/agents/memoria_revisore.md`). Puoi procedere con `bash scripts/segna_review_ok.sh` e il commit.
```

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 892 → 893 PASS, 0 FAIL (T92d4 nuovo; T91d e T92d3 rafforzati). Blocco reale: `=== RIEPILOGO: 893 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1428 passed in 186.81s (0:03:06)` (prima della fix R-359-1, che aggiunge 1 test notte: notte 64 passed).
tests/test_unit_gate.py: 606 → 627 passed (prefisso col punto, prefissi ripetuti, separatori iniziali, copie di .config); gate+notte 691 passed. pytest `tests/` sul codice finale: `1450 passed in 147.73s (0:02:27)`.

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `44fc4ae` (commit della fetta, PR #217 aperta su questo SHA): run in corso all'apertura.
- `ec644b8` (primo fine-task): unit-suite, handoff-check, smista success; verifica-bot in corso (annullata dal push successivo). Verifica esterna APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/217#issuecomment-6257011328)): V-1 BASSA chiusa in `5d90626`, V-2 BASSA (CI finale non provata dall'handoff) e V-3 COSMETICA (prova sul Mac non riproducibile) dichiarate.
- `fdf001c` (secondo fine-task): unit-suite, handoff-check, smista success; verifica-bot neutral (bot APPROVATO CON RISERVE, la PR tocca la macchina del bot: decide l'operatore); verifica esterna APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/217#issuecomment-6257150782)). Note chiuse nel commit successivo (review #363).
- Commit delle note e commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff. Il merge aspetta unit-suite e verifica-bot su questo SHA.

## §7 RISERVE APERTE

- V-2 bot #217 (COSMETICA): lo stat del §2 è preso prima del commit di fine-task che contiene questo handoff (limite noto del flusso).
- Nuove registrate (BASSE/COSMETICHE, dall'ultimo giro di #216): R-bot216-1, R-bot216-2, R-ve216-2, posizione di `_knowledge_log`.
- Da vedere al primo giro notturno vero: righe «Riflessione:» e «Lezioni da approvare: N» su Telegram.
- Già tracciate: R-ve215-1, COSMETICHE #353/#354, R-bot211-2, R-ve211-1/2, R-ve213-3.
