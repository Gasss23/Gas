# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-23 — Chat Motore: R2 via B, fetta 2 (protezioni e tetto del cervello forte, ancora spento)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #258 (https://github.com/Gasss23/Gas/pull/258) — verdetto revisore APPROVATO CON RISERVE: decide l'operatore (CLAUDE.md §10).
2. Prima di accendere `GAS_CLAUDE_CLI`: chiudere o accettare R-497-1/2 e R-496-2, provare il login (R-496-3).

---

## §1 SCOPE & ESITO FETTE

- **Codice casuale per chiamata nei tag (R-494-1/2)**: `FATTA`.
- **Variabili d'ambiente permesse (V-2 ve #256)**: `FATTA`.
- **Tetto giornaliero del forte (V-1 bot #256)**: `FATTA`.
- **Errori: limite in testo semplice, niente testo di Claude, argomenti non validi (V-2/V-3/V-4 bot #256)**: `FATTA`.
- **Dicitura del tetto nella via B (V-3 ve #256)**: `FATTA`.
- **Note del bot e della verifica esterna #258 (costo 0, conto rovinato, LC_*, R-496-1)**: `FATTA` (19213c0, review #497).
- **Catalogo notturno, opzione CLI, doctor, setup Mac**: `DEFERITA — prossime fette`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 .gitignore                         |   2 ++
 brains/claude_cli.py               | 158 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------
 gas.py                             |  91 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  21 ++++++++++-----------
 reports/handoff.md                 | 243 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/r2_regole_abbonamento.md   |   2 ++
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  22 ++++++++++++----------
 tests/test_unit_claude_cli.py      | 119 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------
 tests/test_unit_kernel.py          |  54 +++++++++++++++++++++++++++++++++++++++++++++++++++++-
 12 files changed, 473 insertions(+), 249 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
19213c0 fix(r2): note del bot e della verifica esterna #258 sul tetto del forte
85f74d7 chore(revisore): memoria review #497 — APPROVATO CON RISERVE
a6d9261 docs(fine-task): report R2 via B fetta 2, riserve R-496
cf58065 feat(r2): fetta 2 del cervello forte — codice per chiamata, ambiente permesso, tetto
f7f3c62 chore(revisore): memoria review #496 — APPROVATO CON RISERVE
```

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore: cf58065 (review #496, sotto) e 19213c0 (review #497, più in basso). Commit cf58065: `feat(r2): fetta 2 del cervello forte — codice per chiamata, ambiente permesso, tetto`.

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

### Review #497 (commit 19213c0: note del bot e della verifica esterna #258)

## VERDETTO: APPROVATO CON RISERVE

Review #497 (chat Motore). È la nuova revisione della #496 sul diff in staging della PR #258 (R2 via B fetta 2, rung claude-cli dormiente). Ho letto la coda della memoria e la voce R2 in reports/stato_progetto.md; CLAUDE.md §5 e §8–9 li avevo già nel contesto.

Elementi del diff esaminati:
- `brains/claude_cli.py:180`: `_costo_equivalente` accetta solo int/float non booleani con 0 < v < 1000. Con 0, True, inf, NaN, valori negativi o stringhe usa la stima dai token. Rischio: un tetto che non scatta mai con un costo pari a 0. Esito: ok, chiude V-1 bot/ve #258. Il test copre 0, 0.0 e True.
- `brains/claude_cli.py:46`: l'elenco `_ENV_PERMESSE` ora contiene i nomi LC_* scritti per esteso e non usa più prefissi (`brains/claude_cli.py:104`). Rischio: una variabile segreta che passa con un prefisso. Esito: ok, `LC_TOKEN_SECRET` viene escluso e il test lo verifica (chiude V-2 ve #258).
- `brains/claude_cli.py:252`: il tempo scaduto porta `costo_equivalente_usd`, stimato sui caratteri d'ingresso diviso 4. Gli errori della CLI e il formato sbagliato usano `_costo_dati` (`brains/claude_cli.py:190`), che gestisce un `usage` assente o non numerico. Rischio: consumo non contato. Esito: riserva R-497-1 (sotto).
- `gas.py:1615`: `_uso_claude_cli` controlla prima usd (numero non booleano, finito, ≥0) e poi il giorno (strptime, mai nel futuro). Solo dopo lo confronta con oggi. Rischio: un conto rovinato ma in JSON valido azzererebbe l'uso. Esito: ok. Una lista, `giorno` None, usd stringa o booleano, una data futura o la chiave mancante danno sempre None, cioè forte fermo (T99k). Un giorno passato e valido dà 0.0 (T99j).
- `gas.py:4646`: nell'`except` attorno alla create la registrazione avviene solo se `name == "claude-cli"`. `_registra_uso_claude_cli` (`gas.py:1631`) non solleva mai, e il `raise` nudo che segue rilancia `e` (il contesto dell'eccezione esterna viene ripristinato). Rischio: cambiare il fallback degli altri provider o il retry Gemini 400. Esito: ok. Per i nomi gemini* il ramo non entra. Il forte non ripiega sui gratuiti: T99l non produce nessun final e l'uso registrato è 0.5.
- `gas.py:1642`: un file .tmp con il pid per ogni processo. Il .gitignore è allineato al nuovo nome. Esito: ok, ma il lock manca ancora (R-496-2, dichiarato).

§5: niente slicing diretto della history e niente simulazione dei tool. §8: il limite di 10 iterazioni non è toccato. §9: le eccezioni restano intercettate e il fallback non cambia. Il blocco in caso di dubbio (fail-closed) è coerente con la regola dei modelli: quando il conto è dubbio, il forte resta fermo e non passa ai gratuiti.

Test rilanciati da me: claude_cli 19 passed; kernel 1035 PASS, 0 FAIL (T99k e T99l PASS).

Riserve, tutte BASSE:
- **R-497-1**: alcuni rami non portano ancora il costo: uscita non JSON (`brains/claude_cli.py:259`), JSON che non è un oggetto, chiamata o argomenti non validi (`brains/claude_cli.py:284`, su una risposta riuscita e quindi pagata), `usage` non numerico nel successo (int() solleva ValueError). Correzione semplice: racchiudere il parsing dopo il runner e, se `dati` è un oggetto JSON, attaccare `_costo_dati(dati)` a qualunque eccezione.
- **R-497-2**: se la data nel conto è futura (cambio di fuso o orologio tornato indietro), il forte resta fermo fino a quel giorno. È in linea con il blocco in caso di dubbio e si risolve da solo, ma va annotato nella documentazione o nel doctor.
- **R-496-2** resta aperta: manca il lock tra processi (corsa lettura-somma-scrittura).

Rischio escluso: non ho verificato il comportamento reale della CLI `claude` (se riporta davvero `total_cost_usd` sugli errori e sul tempo scaduto, e il login con il nuovo elenco esplicito di LC_*), perché non si può riprodurre senza l'abbonamento e il Mac/VPS. Non ho lanciato il pytest completo (2133 secondo l'agente): ho rieseguito solo le due suite toccate.

Memoria: riga #497 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da `scripts/commit_memoria_revisore.sh` (85f74d7).

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: 1029 → 1035 PASS (T99g-l nuovi; T99d rafforzato), 0 FAIL.
  `=== RIEPILOGO: 1035 PASS, 0 FAIL ===`
- `pytest tests/test_unit_claude_cli.py`: 12 → 19 passed.
- `pytest tests/` completo: `2133 passed, 1 skipped in 192.34s (0:03:12)`.
- Prova vera dell'adattatore (`claude -p` con l'ambiente ridotto, in questo ambiente Linux): risposta `'ok'`, costo equivalente `0.0003846`.

## §6 STATO CI

`gh run list -L 3` alla scrittura:

```
completed	success	R2 via B fetta 2: codice per chiamata, ambiente permesso, tetto del cervello forte	verifica-bot	feat/merge-automatico-z1xjx2	pull_request_target	39996402478	3m46s	2026-10-23T17:36:04Z
completed	skipped	R2 via B fetta 2: codice per chiamata, ambiente permesso, tetto del cervello forte	verifica-bot	feat/merge-automatico-z1xjx2	pull_request_target	39996390596	2s	2026-10-23T17:35:59Z
completed	success	docs(fine-task): report R2 via B fetta 2, riserve R-496	CI	feat/merge-automatico-z1xjx2	push	39996388617	2m51s	2026-10-23T17:35:58Z
```

Mappatura: f7f3c62+cf58065 pushati insieme (run sulla testa cf58065); a6d9261 (report): CI verde sul suo push (unit-suite, handoff-check, verifica-bot success). 85f74d7 (memoria) e 19213c0 (correzioni) e il commit di fine-task che li segue: run non ancora disponibile alla scrittura dell'handoff (una sola run per il push, sulla testa).

## §7 RISERVE APERTE

- ~~R-496-1~~ chiusa in 19213c0 (errori, formato sbagliato e tempo scaduto entrano nel tetto).
- **R-497-1** (BASSA): alcuni rami d'errore non portano ancora il costo (uscita non JSON, chiamata/argomenti non validi su risposta pagata, \`usage\` non numerico).
- **R-497-2** (BASSA): una data futura nel conto ferma il forte fino a quel giorno (fail-closed).
- **R-496-2** (BASSA): due processi in parallelo possono perdere un aggiornamento del conto (niente lock).
- **R-496-3** (BASSA): login reale col portachiavi del Mac e con `CLAUDE_CODE_OAUTH_TOKEN` sulla VPS da provare con l'ambiente ridotto.
