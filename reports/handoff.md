# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-23 — Chat Motore: R2 via B, fetta 2 (protezioni e tetto del cervello forte, ancora spento)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #258 (https://github.com/Gasss23/Gas/pull/258) — verdetto revisore APPROVATO CON RISERVE: decide l'operatore (CLAUDE.md §10).
2. Prima di accendere `GAS_CLAUDE_CLI`: chiudere o accettare R-496-1/2, provare il login (R-496-3).

---

## §1 SCOPE & ESITO FETTE

- **Codice casuale per chiamata nei tag (R-494-1/2)**: `FATTA`.
- **Variabili d'ambiente permesse (V-2 ve #256)**: `FATTA`.
- **Tetto giornaliero del forte (V-1 bot #256)**: `FATTA`.
- **Errori: limite in testo semplice, niente testo di Claude, argomenti non validi (V-2/V-3/V-4 bot #256)**: `FATTA`.
- **Dicitura del tetto nella via B (V-3 ve #256)**: `FATTA`.
- **Catalogo notturno, opzione CLI, doctor, setup Mac**: `DEFERITA — prossime fette`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 .gitignore                         |   2 ++
 brains/claude_cli.py               | 132 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------
 gas.py                             |  79 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  20 +++++++++-----------
 reports/handoff.md                 | 224 +++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/r2_regole_abbonamento.md   |   2 ++
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  21 +++++++++++----------
 tests/test_unit_claude_cli.py      |  96 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------
 tests/test_unit_kernel.py          |  32 +++++++++++++++++++++++++++++++-
 12 files changed, 353 insertions(+), 263 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
cf58065 feat(r2): fetta 2 del cervello forte — codice per chiamata, ambiente permesso, tetto
f7f3c62 chore(revisore): memoria review #496 — APPROVATO CON RISERVE
```

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore: cf58065 `feat(r2): fetta 2 del cervello forte — codice per chiamata, ambiente permesso, tetto`.

## VERDETTO: APPROVATO CON RISERVE

Review #496 (chat Motore). Diff staged: R2 via B, fetta 2. Il rung claude-cli resta spento.

Letture obbligatorie fatte: CLAUDE.md §5, §8 e §9; reports/stato_progetto.md, la voce R2 fetta 1 con R-494-1/2; la memoria del revisore. Il numero più alto in memoria era #495, quindi questa review è la #496.

**Elementi del diff esaminati**
- brains/claude_cli.py:106 — `_nuovo_codice` usa `secrets.token_hex(8)` per ogni chiamata, cioè 64 bit da una fonte crittografica. Rischio esaminato: che un contenuto possa indovinare o riusare il codice. Il codice nasce dentro `create`, dopo che i messaggi, i risultati degli strumenti e il pin esistono già. Le risposte vecchie del modello possono contenere al massimo il codice di una chiamata precedente, che ora non vale più. — ok
- brains/claude_cli.py:110 — `_senza_codice` lascia il contenuto intatto e toglie solo il codice: chiude R-494-1 (sosia Unicode ed entità diventano solo testo) e R-494-2 (niente più `‹` che corrompeva i file). Ho verificato che `.format(codice=...)` su `_ISTRUZIONI_FORMATO` non trovi altre graffe: sono 7 aperte e 7 chiuse, tutte `{codice}`. Il prompt che ne esce è corretto. — ok
- brains/claude_cli.py:46 — lista delle variabili permesse. Sonda con `_ambiente_pulito`: GH_PAT, AWS_SESSION, ANTHROPIC_API_KEY e CLAUDE_CODE_USE_BEDROCK restano fuori; CLAUDE_CODE_OAUTH_TOKEN, HOME e LC_ALL passano. Il confronto è esatto sul nome, quindi `lc_x` resta fuori. Il login funziona con HOME (Linux, file `~/.claude`), con HOME e USER (portachiavi del Mac) o con OAUTH_TOKEN (VPS). Mancano ALL_PROXY e all_proxy: è cosmetico. — riserva R-496-3 (sotto)
- brains/claude_cli.py:254 e brains/claude_cli.py:263 — il messaggio d'errore porta solo il subtype ripulito con `[a-z_]` e al massimo 40 caratteri; il «429» si cerca anche in result e stderr senza copiarli (V-3). Argomenti che non sono un oggetto JSON → errore, non più `{}` in silenzio (V-4). — ok
- brains/claude_cli.py:174 — `_costo_equivalente`: usa `total_cost_usd` della CLI se è un numero valido tra 0 e 1000 (NaN escluso), altrimenti stima dai token ai prezzi Sonnet 3/15. — ok
- gas.py:4625 — controllo del tetto prima di OGNI create, solo per il rung claude-cli: dentro `for _ in range(10)` (il tetto delle 10 iterazioni resta), dopo il controllo del budget. Toglie il rung dai «tentati» se non era stato chiamato e si ferma con un errore dichiarato, senza ripiego. La riflessione notturna (gas.py:3828) usa la classe "complesso", che non contiene il forte, quindi il tetto non si aggira da lì. — ok
- gas.py:1602 e gas.py:1623 — conto in `.gas_claude_cli_uso.json`, scritto in modo atomico (tmp + os.replace). Se il file è illeggibile o non è un dizionario si ha None → forte fermo e file non riscritto. Bloccare qui è coerente con §9: nessun crash, errore dichiarato. È anche coerente con la regola dei modelli: i lavori importanti aspettano e non vanno ai gratuiti. Aggiramento da parte del modello: il file è nascosto, quindi scriverlo richiede la firma dell'operatore (contesto: modules/gate/gate.py:623). La variabile d'ambiente del tetto non è raggiungibile dal modello. — ok
- gas.py:4670 — l'uso si registra solo dopo una create riuscita. — riserva R-496-1
- tests/test_unit_kernel.py:10898 e tests/test_unit_kernel.py:10905 — T99h (tetto raggiunto: nessuna chiamata) e T99i (conto illeggibile: forte fermo, file intatto). Rieseguiti da me: tests/test_unit_claude_cli.py 18 passed, kernel 1033 PASS / 0 FAIL. — ok

**Wall of Shame (§5)**: nessuno slicing della history; la finestra resta `_get_window()` a gas.py:4602. Nessuna simulazione di output dei tool: Claude restituisce chiamate che `run_turn` esegue davvero. — ok

**Riserve (tutte BASSE, da tracciare in stato_progetto.md prima di accendere `GAS_CLAUDE_CLI`)**
- R-496-1: il costo si conta solo sulle risposte riuscite. Una risposta d'errore della CLI (`is_error`, che spesso porta comunque `total_cost_usd`), una risposta senza formato o un timeout dopo il consumo non entrano nel conto: il tetto sottostima. Rimedio: registrare anche nel ramo d'errore, per esempio esponendo il costo sull'eccezione.
- R-496-2: due processi in parallelo (bot e turno di notte) possono perdere un aggiornamento del conto, perché lettura, somma e scrittura avvengono senza lock. Rischio già dichiarato dall'agente; sottostima piccola.
- R-496-3: il login reale con la lista delle variabili permesse non è stato provato (vedi sotto). Va provato con `claude -p` vero sul Mac e sulla VPS prima di accendere il rung.

**Rischio escluso esplicitamente**: non ho verificato il login reale di `claude -p` con l'ambiente ridotto, né sul Mac (portachiavi) né su Linux/VPS (CLAUDE_CODE_OAUTH_TOKEN). Il comando esiste in questo ambiente, ma una chiamata vera consuma l'abbonamento e qui le credenziali non sono quelle di Gas: non riproducibile in dev. Non ho fatto nemmeno una prova a mutante su T99g-j.

**Memoria**: riga #496 più una lezione nuova (un contatore di spesa agganciato solo al ramo di successo sottostima), committata con scripts/commit_memoria_revisore.sh (commit f7f3c62, solo `/home/user/Gas/.claude/agents/memoria_revisore.md`).

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: 1029 → 1033 PASS (T99g, T99h, T99i, T99j nuovi; T99d rafforzato), 0 FAIL.
  `=== RIEPILOGO: 1033 PASS, 0 FAIL ===`
- `pytest tests/test_unit_claude_cli.py`: 12 → 18 passed.
- `pytest tests/` completo: `2132 passed, 1 skipped in 193.19s (0:03:13)`.
- Prova vera dell'adattatore (`claude -p` con l'ambiente ridotto, in questo ambiente Linux): risposta `'ok'`, costo equivalente `0.0003846`.

## §6 STATO CI

`gh run list -L 3` alla scrittura:

```
completed	skipped	R2 via B fetta 2: codice per chiamata, ambiente permesso, tetto del cervello forte	verifica-bot	feat/merge-automatico-z1xjx2	pull_request_target	39996334939	2s	2026-10-23T17:35:34Z
in_progress		feat(r2): fetta 2 del cervello forte — codice per chiamata, ambiente …	CI	feat/merge-automatico-z1xjx2	push	39996329497	18s	2026-10-23T17:35:32Z
in_progress		feat(web): fetta 14 Mani — tempo riservato alla pulizia, grezzi autochiusi conformi (R6)	verifica-bot	feat/mani-web-fetta14	pull_request_target	39996169035	1m27s	2026-10-23T17:34:23Z
```

Mappatura: f7f3c62 (memoria) e cf58065 (motore) pushati insieme: una run sul push, che testa la testa cf58065; f7f3c62 non ha run propria. Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-496-1** (BASSA): il costo si conta solo sulle risposte riuscite; errori o timeout dopo il consumo non entrano nel tetto.
- **R-496-2** (BASSA): due processi in parallelo possono perdere un aggiornamento del conto (niente lock).
- **R-496-3** (BASSA): login reale col portachiavi del Mac e con `CLAUDE_CODE_OAUTH_TOKEN` sulla VPS da provare con l'ambiente ridotto.
