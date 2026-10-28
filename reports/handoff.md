# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — chat Motore: riserve del punto 3 della RIPARTENZA (cervello forte e doctor), PR #290

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #290 (https://github.com/Gasss23/Gas/pull/290): review #542 APPROVATO CON RISERVE, quindi decide l'operatore (CLAUDE.md §10). Numero e URL dalla risposta JSON dello strumento GitHub `create_pull_request` (`gh` non autenticato in questo ambiente).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — R-538-1, GAS_CLAUDE_BIN solo nella shell**: `FATTA` — WARN se manca, è vuota o è diversa nel `.env` di Gas (V-1 ve #290, V-2 bot #290).
- **Fetta 2 — R-538-2 e V-2 bot #287, motivo del forte**: `FATTA` — senza prefisso ripetuto, tetto 300. Correzione (V-3 ve #290): `_MSG_LOGIN` è di 152 caratteri, il vecchio tetto non lo troncava.
- **Fetta 3 — V-1 bot #287, falsi WARN**: `FATTA` per `/usr/local` su Linux e i collegamenti risolti da entrambe le parti (R-540-1, T99z); `DEFERITA — ~/.zshenv`: l'errore va nel verso prudente.
- **Fetta 4 — V-1 e V-3 bot #290, .env di Gas e GAS_CLAUDE_CLI solo nella shell**: `FATTA` — `DOTENV_PATH` unico; WARN «acceso solo nella shell».

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 gas.py                             | 104 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------
 reports/diff_sessione.md           |   7 +++++--
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  15 ++++++++++-----
 tests/test_unit_kernel.py          |  73 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d» e niente riga di totale. Conteggi presi con i report in stage.

## §3 GIT LOG --ONELINE (sessione)

```
a8cde14 fix(doctor): .env di Gas (DOTENV_PATH), valore diverso nel .env e GAS_CLAUDE_CLI solo nella shell → WARN (V-1..V-3 bot #290)
f530158 chore(revisore): memoria review #542 — APPROVATO CON RISERVE
6771320 fix(doctor): .env con GAS_CLAUDE_BIN vuota o virgolette aperte non conta (V-1 ve #290), test .venv collegato (V-2 ve #290)
ae576f9 chore(revisore): memoria review #541 — APPROVATO
ae66740 docs(fine-task): PR #290 — riserve del punto 3, review #540
cceadcc fix(forte): riserve del punto 3 — WARN se GAS_CLAUDE_BIN sta solo nella shell, motivo senza prefisso ripetuto e non troncato, /usr/local su Linux
e6604cb chore(revisore): memoria review #540 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #540 (chat Motore) — sul diff di cceadcc

## VERDETTO: APPROVATO CON RISERVE

Il diff in stage tocca gas.py e tests/test_unit_kernel.py. Ho ripetuto la suite del kernel: 1064 PASS, 0 FAIL. Ho provato tre mutanti e alla fine ho ripristinato gas.py: lo stage è invariato e non ci sono modifiche fuori stage.

Elementi esaminati:
- gas.py:434 — `_motivo_forte` toglie il prefisso «claude-cli: » e conserva «429 », con un tetto di 300 caratteri — rischio esaminato: che cambi la classificazione QUOTA o che lasci uscire dati personali — ok. La classificazione resta su `str(e)` in `_classify_provider_error` (gas.py:4935); il motivo è solo testo mostrato. Resta valida solo la prima riga e il controllo «solo RuntimeError con prefisso fisso» è invariato. Prova diretta: «429 claude-cli: limite» diventa «429 limite». Il messaggio del login arriva intero (lo verifica T99u).
- gas.py:463 — `_chiavi_dotenv` — rischio esaminato: che esponga valori — ok. Restituisce solo i nomi delle chiavi (prova con `SEGRETO=abc123`: esce solo la chiave), non fa log e non carica niente in os.environ. Se il file manca o non si legge restituisce None, senza crash (fail-safe §9).
- gas.py:5022 — WARN «impostata solo nella shell» — rischio esaminato: che scatti a torto — ok. Il mutante che toglie il ramo fa fallire T99w. Il template scripts/notte/com.gas.notte.plist non ha EnvironmentVariables, quindi il caso «.env assente ma GAS_CLAUDE_BIN dal plist» non esiste nel repo. Con un plist personalizzato, oppure con un export in ~/.zshenv (il plist lancia `zsh -c`, che legge ~/.zshenv), il WARN sarebbe falso. È però un falso WARN e non un falso OK, quindi va nel verso prudente e l'exit code resta 0.
- gas.py:455 — /usr/local/bin e /usr/local/sbin contano solo su Linux, con confronto anche a percorsi risolti — ok. Il mutante «sempre Linux» fa fallire T99x.
- tests/test_unit_kernel.py:11216 — ripristino dell'ambiente dopo il test — ok. GAS_NO_DOTENV torna a "1", come lo imposta globalmente tests/test_unit_kernel.py:53. Il `.env` di prova viene cancellato, PATH e GAS_CLAUDE_BIN vengono ripristinati. `gas.sys.platform` torna al valore originale nel `finally` di T99x.

Riserve:
- R-540-1 BASSA — gas.py:460: il mutante che toglie `{os.path.realpath(v) for v in vedute}` sopravvive con la suite verde. T99x mette il collegamento solo dalla parte del binario (lnk99 → /usr/bin); manca un caso col collegamento dalla parte delle cartelle note, per esempio `.venv` collegato altrove.
- R-540-2 BASSA — gas.py:478: `_chiavi_dotenv` conta anche righe che `_carica_dotenv` scarta (virgolette non chiuse). Conta anche `GAS_CLAUDE_BIN=` con valore vuoto. In questi casi rari il doctor dà un falso OK.
- Nota, non bloccante e già presente prima: il doctor cerca il `.env` nella cartella da cui lo lanci (gas.py:4963), mentre `_carica_dotenv` lo legge accanto a gas.py. Se lanci il doctor da un'altra cartella, il WARN può essere falso, sempre nel verso prudente.

Antipattern di CLAUDE.md sez. 5: niente slicing della cronologia (gli slicing nel diff sono solo su stringhe), niente simulazione di tool. Il tetto delle 10 iterazioni e `_get_window` non sono toccati.

Rischio escluso: non ho verificato il comportamento reale su macOS (launchd con `zsh -c` e ~/.zshenv, /bin non collegato): non è riproducibile in questo ambiente Linux. Il caso Mac l'ho visto solo simulando `sys.platform="darwin"` in T99x.

Riga contatore #540 scritta e committata: e6604cb, solo /home/user/Gas/.claude/agents/memoria_revisore.md. Lezione nuova aggiunta: un confronto a collegamenti risolti va provato con un collegamento da ciascuna delle due parti.

### Review #541 (chat Motore) — sul diff di 6771320

## VERDETTO: APPROVATO

Review #541, PR #290 secondo giro. Ho letto CLAUDE.md, reports/stato_progetto.md (le voci R-540) e .claude/agents/memoria_revisore.md. Il diff staged è `gas.py` e `tests/test_unit_kernel.py`.

**Elementi del diff esaminati**
- `gas.py:576` — `_voci_dotenv(testo, avvisa)` è un generator con il corpo identico al vecchio ciclo di `_carica_dotenv`, confrontato riga per riga. Il rischio esaminato era un refactor che cambiasse il comportamento. L'ho provato direttamente su un `.env` di prova:
  - il BOM viene tolto;
  - ` #` apre un commento solo sui valori senza virgolette, `d#nocomm` resta intero;
  - `export` viene tolto;
  - `PATH` già presente non viene sovrascritto;
  - `E1=` vuota viene ancora caricata, come prima;
  - i warning sono `.env riga 2: formato non valido` e `.env riga 3 (B1): virgolette non chiuse`, con numero di riga e senza il valore (il segreto non compare nel log).
  - Esito: ok.
- `gas.py:625` — `_carica_dotenv` ora usa `for chiave, valore in _voci_dotenv(testo)`. Rischio esaminato: il BOM, la gestione di file assente o illeggibile e il ritorno dei nomi caricati. La lettura con `utf-8-sig`, le eccezioni e il ritorno dei nomi sono rimasti invariati. Esito: ok.
- `gas.py:463` — `_chiavi_dotenv` legge con `avvisa=False` e tiene `{chiave … if valore}`. Rischi esaminati: valori che escono e warning doppi. Ritorna solo un set di nomi e non scrive nulla nel log (nel buffer di prova ci sono solo i 2 warning di `_carica_dotenv`). La regex non può sollevare eccezioni, e quelle in lettura del file restano intercettate. Esito: ok.
- `tests/test_unit_kernel.py:11257` — T99y aggiornato con `VUOTA=` e `APERTA="/x`. Mutante che toglie il filtro `if valore`: T99y FAIL con `{'VUOTA', …}`. Il test uccide il mutante. Esito: ok.
- `tests/test_unit_kernel.py:11264` — T99z nuovo: `.venv` collegato a `venv_vero99`. Mutante che toglie il realpath sulle cartelle note in `gas.py:458`: T99z FAIL (1064/1). R-540-1 è chiusa davvero. Esito: ok.
- Contesto (file non toccato in questo giro): `gas.py:5023` resta l'unico chiamante di `_chiavi_dotenv`, e il controllo «è nel .env» lì è coerente con la nuova semantica. Esito: ok.

**Test.** Suite kernel 1065 PASS, 0 FAIL, rieseguita da me. `pytest tests/test_unit_dotenv.py`: 10 passed. Dopo i mutanti `gas.py` è stato ripristinato e il diff unstaged è vuoto.

**Antipattern e guardrail.** Nessuno slicing della history, nessuna simulazione di tool. Il cap delle 10 iterazioni, `_get_window` e la regola fail-safe §9 non sono toccati.

**Riserva COSMETICA, non bloccante**
- R-541-1: `GAS_CLAUDE_BIN="  "` (solo spazi tra virgolette) conta come valorizzata e il doctor darebbe OK. Il caso è teorico.

**Rischio escluso.** Non ho verificato il comportamento reale sul Mac: il `.env` vero dell'operatore e il timer launchd non sono riproducibili qui. Non ho rieseguito nemmeno i pytest di claude_cli e della notte: questo diff non li tocca.

**Memoria.** Riga #541 e una lezione aggiunte a `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole (ae576f9). Il diff staged di `gas.py` e `tests/test_unit_kernel.py` è rimasto in staging, intatto.

### Review #542 (chat Motore) — sul diff di a8cde14

## VERDETTO: APPROVATO CON RISERVE

Revisione n. 542: PR #290, terzo giro, diff in staging su `gas.py` e `tests/test_unit_kernel.py`. Prima di cominciare ho letto CLAUDE.md (sezione 5), la parte di `reports/stato_progetto.md` su #290 (riga 589) e la mia memoria (#539–#541).

**Elementi del diff esaminati**
- `gas.py:580` — `DOTENV_PATH` diventa l'unico percorso del `.env`, accanto a gas.py. Lo usano sia `_carica_dotenv` (`gas.py:630`) sia il doctor (`gas.py:5018`). Rischio esaminato: che il caricamento e il doctor leggano file diversi. Esito: ok nel codice, ma con riserva sui test (R-542-1, sotto).
- `gas.py:463` — `_valori_dotenv` restituisce un dict con i soli valori non vuoti e chiama `_voci_dotenv(..., avvisa=False)`, quindi non scrive nel log. Rischio esaminato: che un valore del `.env` finisca in output o nel log. Esito: ok. I messaggi di WARN alle righe 5022 e 5037 contengono solo `binario`, cioè il percorso in uso preso dall'ambiente o da `which`, mai un valore letto dal `.env`. Il ramo V-2 confronta i valori senza mai stamparli.
- `gas.py:566` / `gas.py:572` — `_env_flag` ora delega a `_flag_vero`. Rischio esaminato: che il comportamento cambi. Esito: ok, l'espressione è identica (strip, lower, insieme 1/true/on/yes/si).
- `gas.py:5018` — se `GAS_NO_DOTENV` è attivo, `_dotenv` vale None e i due controlli V-2 e V-3 si spengono, perché entrambi sono protetti da `_dotenv is not None`. Esito: ok. Il mutante che ignora `GAS_NO_DOTENV` fa fallire T99s.
- `gas.py:5022` — il WARN V-3 sta solo nel ramo `else` di `_env_flag("GAS_CLAUDE_CLI")`, quindi con il forte spento non scatta. Con `.env` assente (dict vuoto) il WARN «acceso solo nella shell» è corretto. Esito: ok. Il mutante senza V-3 fa fallire T99w2.
- `gas.py:5037` — V-2 confronta il `GAS_CLAUDE_BIN` del `.env` con quello in uso. È coerente col caricamento, che non sovrascrive variabili già presenti: se shell e `.env` divergono, di notte vale il `.env`. Esito: ok. Il mutante che torna al controllo sul solo nome fa fallire T99w2.
- `tests/test_unit_kernel.py:11212` — il test salva `gas.DOTENV_PATH` e lo ripristina nel `finally` a `tests/test_unit_kernel.py:11224`, dove rimette anche `GAS_NO_DOTENV=1` e cancella il `.env` di prova. Rischio esaminato: stato globale che resta sporco tra un test e l'altro. Esito: ok.
- Contesto: `tests/test_unit_kernel.py:11205` — il `.env` di prova sta in `_k99.root`, la stessa cartella passata a `gas.doctor(root)`. Esito: **riserva R-542-1**.

**Riserva**
- **R-542-1 BASSA**: il mutante che rimette `root / ".env"` al posto di `DOTENV_PATH` in `gas.py:5018` sopravvive (suite 1066 PASS, 0 FAIL). Nel test il percorso puntato da `DOTENV_PATH` e `root/.env` sono lo stesso file, quindi la correzione V-1 non è coperta. Rimedio: in T99w mettere il `.env` di prova fuori da `_k99.root`, ad esempio in una sottocartella, e puntarci `gas.DOTENV_PATH`.

**Prove eseguite**: suite kernel 1066 PASS, 0 FAIL. Quattro mutanti: tre uccisi (senza V-3, V-2 solo sul nome, `GAS_NO_DOTENV` ignorato), uno sopravvissuto (R-542-1). Dopo i mutanti ho rimesso `gas.py` com'era: è ancora in staging senza modifiche extra.

**Rischi esclusi**
- Comportamento sul Mac reale (launchd con `.env` e `~/.zshrc` diversi) non verificato: non è riproducibile qui.
- Non ho rilanciato la parte pytest (dotenv, claude_cli, notte: 233 passed secondo il chiamante). Il diff non tocca quei moduli.
- Caso limite non coperto, raro e innocuo: `GAS_CLAUDE_BIN=""` esportata vuota nella shell con un valore nel `.env` salta il controllo V-2.

**Memoria**: riga #542 e una lezione nuova («un fix "percorso A invece di B" va provato con A diverso da B nel test») aggiunte a `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate con lo script (f530158).

## §5 DELTA TEST DEL MOTORE

Suite kernel locale: 1061 → 1066 PASS (T99w, T99w2, T99x, T99y, T99z nuovi; T99s, T99u aggiornati), 0 FAIL. Il valore di main è misurato in un worktree a `094eb57`. In CI i conteggi sono 2 in più (V-4 bot #290: test che dipendono dall'ambiente).

```
=== RIEPILOGO: 1066 PASS, 0 FAIL ===
```

pytest (tutti i file tranne la suite kernel), sulla testa `a8cde14`: `2282 passed, 61 skipped in 207.97s (0:03:27)`.

## §6 STATO CI

CI letta con lo strumento GitHub della sessione: `gh run list` non è disponibile (`gh` non autenticato).

Mappatura commit→run:
- `e6604cb`: nessuna run su questo SHA (pushato insieme a `cceadcc`).
- `cceadcc`: `handoff-check` failure (atteso: handoff non ancora riscritto); poi sistemato da `ae66740`.
- `ae66740`: `unit-suite` success, `handoff-check` success, `verifica-bot` success (APPROVATO CON RISERVE, V-1..V-3 BASSE chiuse in `a8cde14`, V-4 COSMETICA).
- `ae576f9`: nessuna run su questo SHA (pushato insieme a `6771320`).
- `6771320`: `verifica-bot` failure (MEDIA: handoff fermo a `cceadcc`, chiusa da questo fine-task).
- `f530158`, `a8cde14`: nessuna run su questi SHA (pushati insieme al commit di fine-task).
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-542-1 BASSA: nel test il `.env` di prova coincide con `root/.env`, quindi un ritorno a `root/.env` non sarebbe preso.
- R-541-1 COSMETICA: `GAS_CLAUDE_BIN="  "` conta come valorizzata.
- V-4 COSMETICA ve #290: «429 429» in un caso non reale.
- Il PATH di `~/.zshenv` non è considerato (falso WARN, verso prudente).
