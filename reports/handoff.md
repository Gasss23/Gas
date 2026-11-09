# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 — Sottofondo e voce: chiusura delle riserve BASSE aperte (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: con riserve BASSE serve il sì dell'operatore via M1 (CLAUDE.md §10).
2. Prova sul Mac: compito lungo a voce → avviso Telegram → «Gas» → Gas dice per primo il compito finito.

---

## §1 SCOPE & ESITO FETTE

- **PR #352** (riserve BASSE della #350): `MERGIATA` (3084979) col sì dell'operatore via M1 (9 nov); Mani avvisato per la #353.
- **Fetta BASSE aperte di sottofondo e voce**: `FATTA` — segno di lettura dei compiti dopo l'invio riuscito anche nei rami JSON (R-711-2-M2); regola unica: con schermo i compiti sono consegnati quando arriva il testo (anche se la voce fallisce), senza schermo solo se detti (bot #352 V-1 su f6de3e6); test di sintesi fallita nei rami MP3 unico e audio/mpeg e di «Dimmi.» a testo (R-711-1-M2, bot #352 V-1 su 893b863); compiti «in_coda»/«in_corso» vecchi senza posto cancellati dalla pulizia (bot #349 V-1 su a9a17a5, R-707-1-M2); pulizia oraria con orologio monotono (bot #349 V-2). Review #713-M2 APPROVATO CON RISERVE (R-713-1/2-M2 BASSE).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 +
 modules/sottofondo/__init__.py     | 18 +++++++--
 modules/voice/server.py            | 29 ++++++++++-----
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_sottofondo.py      | 35 +++++++++++++++++-
 tests/test_unit_voice_server.py    | 76 ++++++++++++++++++++++++++++++++++++--
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main 3084979 (merge della #352).

## §3 GIT LOG --ONELINE (sessione)

```
760f0a9 fix(voce+sottofondo): riserve BASSE aperte — segno di lettura dopo l'invio, regola unica schermo/senza schermo, compiti aperti vecchi puliti, pulizia oraria monotona, test mancanti (sì dell'operatore via M1)
cc9d3ab chore(revisore): memoria review #713 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #713-M2 sul commit 760f0a9 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #713-M2: diff staged su feat/voce-v12-m2 (base 3084979), 4 file, +139/−19. Ho letto CLAUDE.md, stato_progetto (righe 615 e 672) e la memoria. Ho usato una copia dell'index via `git checkout-index`, senza stash: 206 passed. `git diff --cached --check` è pulito. Nel diff non c'è slicing della history, non ci sono output di tool simulati e i guardrail non sono toccati.

**Elementi del diff esaminati**
- `modules/voice/server.py:674`: il segno di lettura in `do_POST` a testo ora parte dopo `_send_json`. Rischio esaminato: segno anche quando il client chiude. `_send_json` scrive sul socket senza buffer e solleva se il client è chiuso, quindi il segno non parte. Esito: ok. Stesso schema a `modules/voice/server.py:726` (`_rispondi_senza_turno`) e `modules/voice/server.py:811` (`consegnati`, poi segno dopo l'invio): ok.
- `modules/voice/server.py:778`: `schermo = not _vuole_righe_senza_schermo()`. Il ramo senza chiave (`modules/voice/server.py:784`) segna solo con schermo. Il ramo MP3 unico segna sempre: lì si arriva solo col formato audio+testo, perché pezzi e pezzi+voce escono prima, quindi lo schermo c'è sempre. Esito: ok.
- `modules/voice/server.py:856`: la condizione `aperto and (schermo and i == 0 or errore is None and n_prefisso and i + 1 == n_prefisso)` è corretta. In Python `and` lega più di `or`. Con schermo il segno parte quando la prima riga, che contiene il `content`, è stata scritta, anche se porta `errore_voce`. Senza schermo parte solo quando l'ultima frase dei compiti è stata inviata senza errore. Se il prefisso c'è, `n_prefisso` è almeno 1, perché `_compiti_finiti` fa strip. Esito: ok. Riserva sulla copertura (R-713-1-M2, sotto).
- `modules/sottofondo/__init__.py:240` e `modules/sottofondo/__init__.py:254`: un compito «in_coda» o «in_corso» si cancella solo se è più vecchio del limite (almeno 1 giorno) e se il posto (attivo.json) non è suo. Rischio esaminato: cancellare un compito ancora vivo. Il posto si toglie solo in `_ripulisci`/`annulla`, cioè quando il processo è morto o è oltre la durata massima (default 1 h), oppure dopo 120 s se il posto è illeggibile. Un compito vivo che ha il posto quindi resta: lo prova il test nuovo `tests/test_unit_sottofondo.py:800`, ed è stato preso il mutante che toglie il controllo del posto. Un compito appena accodato senza file è protetto dall'età del file. Esito: ok, con il caso residuo R-713-2-M2.
- `modules/sottofondo/__init__.py:263`: `_ultima_pulizia` vale `None` all'avvio e usa `time.monotonic()`. Il test è `tests/test_unit_sottofondo.py:814`. Il mutante che toglie il controllo su None è preso: `None` produce un TypeError, intercettato, e quindi nessuna pulizia. Esito: ok.
- Test nuovi in `tests/test_unit_voice_server.py`: `tests/test_unit_voice_server.py:1828` (con schermo e voce fallita, parametrizzato su audio+testo+pezzi e audio+testo), `tests/test_unit_voice_server.py:1932` (audio/mpeg risponde 502 e i compiti restano non letti), `tests/test_unit_voice_server.py:1976` («Dimmi.» a testo). `tests/test_unit_voice_server.py:1815` ora gira in audio+pezzi. Esito: ok.

**Mutanti** (test mirati `-k "f32 or pulizia"`)
- Presi:
  - errore ignorato senza schermo
  - pezzi senza `schermo=True`
  - ramo MP3 unico che non segna mai (2 test falliti)
  - segno prima della sintesi in audio/mpeg
  - pulizia senza controllo del posto
  - `None` tolto dal limite orario
- Non presi:
  - in audio+pezzi senza chiave TTS i compiti vengono segnati letti
  - `aperto` tolto dalla condizione dei pezzi (client chiuso)
  - segno spostato prima di `_send_audio` o `_send_json`

**Riserve**
- R-713-1-M2 (BASSA): mancano tre test.
  - Senza chiave TTS col formato senza schermo, i compiti non devono risultare letti (`modules/voice/server.py:784`). Il comportamento era già presente a HEAD e già non testato.
  - Client chiuso nei pezzi con schermo: la condizione `aperto` a `modules/voice/server.py:856`.
  - Ordine invio→segno nei rami JSON e MP3: un mutante che anticipa il segno passa.
- R-713-2-M2 (BASSA, caso residuo): se attivo.json risulta illeggibile per un attimo, `_leggi` restituisce None e `posto` diventa `{}`. In quel momento un compito vivo più vecchio del limite in giorni perderebbe il file. Serve un file corrotto o un errore di lettura passeggero, più `GAS_SOTTOFONDO_MAX_MIN` maggiore di `GAS_SOTTOFONDO_GIORNI`×1440, perché con la durata di default il compito viene fermato molto prima. È improbabile, ma va dichiarato in stato_progetto.

**Privacy e §9**: nessun log nuovo con dati dell'operatore. La pulizia scrive nel log solo il nome del file. Tutto resta dentro try/except con `logging.warning`, senza crash.

**Non verificato**:
- Non ho provato con un client vero sul Mac (pagina, riprendi.sh, H24). Non è riproducibile qui: resta da fare la prova sul Mac già in elenco.
- Non ho controllato il caso in cui `_send_json` riesce ma il client chiude prima di leggere: è un limite di HTTP, non del diff.

**Memoria**: riga #713-M2 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da `commit_memoria_revisore.sh` (cc9d3ab). L'index del diff in review non è stato toccato: 4 file restano staged.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py` + `tests/test_unit_sottofondo.py`: 206 passed (intere). Nuovi: con schermo e voce fallita i compiti sono letti (audio+testo+pezzi, audio+testo — falliscono col codice di main); audio/mpeg con 502 → non letti; «Dimmi.» a testo senza TTS; test esistente «sintesi fallita» ora senza schermo (audio+pezzi, ha preso un mio errore durante lo sviluppo). Sottofondo: compito «in_corso» vecchio senza posto cancellato, quello col posto no; pulizia oraria con `time.monotonic`. `gas.py` non toccato.

## §6 STATO CI

`gh` non autenticato nel cloud. I commit sono pushati insieme a questo report: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-713-1-M2 BASSA: mancano test per: senza chiave TTS e senza schermo (non letti), client chiuso nei pezzi con schermo, ordine invio→segno nei rami JSON/MP3 (mutanti non presi).
- R-713-2-M2 BASSA: se attivo.json è illeggibile per un attimo e la durata massima supera i giorni di conservazione, un compito vivo potrebbe perdere il file (improbabile coi default).
- Restano: R-709-1/2-M2, R-708-1-M2, R-706-1-M2, R-701-3-M2, R-703-2-M2, R-696-1-M2; doppia lettura con due richieste contemporanee.
- Non verificato in dev: client vero sul Mac, ElevenLabs vero.
