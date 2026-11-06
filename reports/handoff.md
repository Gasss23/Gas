# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-06 — Rifiuto di `--effort` riconosciuto in modo stretto + proposta della fetta 3 (compiti lunghi in sottofondo) (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR (numero e URL dalla risposta JSON di `create_pull_request`; `gh` nel cloud non è autenticato), ordinata dall'operatore via M1; merge secondo CLAUDE.md §10.
2. Fetta 3 (compiti lunghi in sottofondo): leggere `reports/proposta_fetta3_sottofondo.md` e decidere se farla, e se lo strumento lo sceglie il modello (consigliato) o parte da solo oltre N giri.

---

## §1 SCOPE & ESITO FETTE

- **Rifiuto di `--effort` stretto** (R-689-1-M2 BASSA e V-1 della verifica esterna #343; R-689-2-M2): `FATTA` — solo «unknown/unrecognized option|argument --effort» su stderr, regex lineare; review #693-M2 (riserve chiuse), #694-M2 APPROVATO.
- **Proposta della fetta 3**: `FATTA` — documento `reports/proposta_fetta3_sottofondo.md` (nessun codice).
- **PR #343 (voce rapida fetta 2)**: `MERGIATA` (e68a951).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  3 +++
 brains/claude_cli.py               | 17 ++++++++++++-----
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/proposta_fetta3_sottofondo.md           | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_claude_cli.py      | 49 ++++++++++++++++++++++++++++++++++++++++---------
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main e68a951.

## §3 GIT LOG --ONELINE (sessione)

```
e51ec67 fix(claude-cli): il rifiuto di --effort si riconosce solo da «unknown/unrecognized option --effort» su stderr (R-689-1/2-M2, ve #343 V-1) (chat M2)
bc91ccb chore(revisore): memoria review #694 — APPROVATO
1a301bd chore(revisore): memoria review #694 — APPROVATO
df3e46e chore(revisore): memoria review #693 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #693-M2 sul primo stage di e51ec67 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #693-M2. Ho letto il diff staged (brains/claude_cli.py e tests/test_unit_claude_cli.py) su feat/voce-v12-m2, base e68a951. Ho fatto le letture obbligatorie: CLAUDE.md è nel contesto; di reports/stato_progetto.md e .claude/agents/memoria_revisore.md ho letto le parti su effort, R-689 e regex/ReDoS (ricerca mirata, come chiede il §11).

**Elementi del diff esaminati**
- `brains/claude_cli.py:276`: `_RIFIUTO_EFFORT` riconosce solo «unknown/unrecognized option/argument» seguito da `--effort`.
  - Rischio esaminato: forme reali della CLI e falsi positivi.
  - Sonde: queste forme danno tutte True: il messaggio di commander con «(Did you mean --verbose?)» sulla riga dopo, il messaggio con codici colore ANSI, le virgolette a backtick, «--effort=low», «unknown option --effort» senza virgolette. «Unknown argument: effort» di yargs (senza trattini) e le virgolette tipografiche ‘…’ danno False, come già con la regola vecchia: per yargs serviva «--effort» nel testo, per le virgolette tipografiche non c'è regressione. Claude Code usa commander, che scrive in ASCII su stderr.
  - Esito: ok, con le riserve R-693-1-M2 e R-693-2-M2 sotto.
- `brains/claude_cli.py:280`: `_effort_rifiutato` controlla prima l'uscita non zero, poi solo lo stderr.
  - Rischio esaminato: una CLI vecchia che scrivesse il rifiuto su stdout non verrebbe più riconosciuta.
  - Conseguenza: nessun nuovo tentativo, stdout non JSON, quindi RuntimeError «uscita non JSON» (riga 368). È un errore dichiarato, gestito come gli altri del provider: niente crash.
  - Il caso è teorico: commander scrive gli errori di opzione con `outputError` su stderr.
  - Esito: ok.
- `brains/claude_cli.py:348`: chiamante (riga non toccata). Il flag permanente si accende solo dentro il try già esistente, con un solo nuovo tentativo. Con la regola stretta il caso «argument 'turbo' is invalid» (valore sbagliato) non spegne più l'effort per tutto il processo. R-689-1-M2 è chiusa. Esito: ok.
- `tests/test_unit_claude_cli.py:507`: il `finally` azzera il flag di classe. R-689-2-M2 è chiusa. Esito: ok.
- `tests/test_unit_claude_cli.py:511`: test parametrico con 4 rifiuti veri e 4 falsi positivi, più l'uscita 0 che dà sempre False. Copre il caso di V-1 della verifica esterna #343 («invalid» insieme a «--effort»). Esito: ok.

**Test**
- tests/test_unit_claude_cli.py: 57 passed, rilanciati da me con il venv dello scratchpad.
- Il mutante «regola vecchia larga» (5 failed) non l'ho rilanciato: mi fido del dato dell'agente, il test parametrico lo uccide per costruzione.

**Riserve**
- **R-693-1-M2 BASSA (ReDoS quadratico)**: la sequenza `\s*[:=]?\s*` (riga 277), quando i due punti mancano, fa fare backtracking quadratico come due `\s*` adiacenti. È la stessa lezione della review #672.
  - Misure: «unknown option» seguito da 10k spazi impiega 0,67 s; con 100k spazi 66 s.
  - Nella pratica lo stderr della CLI non contiene cose così. Ma il server voce resterebbe bloccato sul turno, quindi lo considero un difetto di robustezza.
  - Correzione: `\s*(?:[:=]\s*)?`. Provata: 1 MB in 0,04 s, stessi esiti sugli 8 casi del test.
  - Conviene aggiungere un test di tempo, per esempio 100k spazi sotto 1 s.
- **R-693-2-M2 COSMETICA**: «unknown option '--effort-level'» e «--effort_x» danno True perché `\b` corrisponde prima del trattino. Gas non passa mai quelle opzioni, quindi l'impatto pratico è nullo. Si chiude con `(?![\w-])` al posto di `\b` finale (provato: '--effort-level' e '--effortful' danno False).

**Non verificato**
- Il messaggio reale della CLI `claude` installata sul Mac quando non conosce `--effort`: non è riproducibile qui, non c'è una CLI vecchia nell'ambiente. Il controllo da fare sul Mac resta `claude --help | grep effort`, già nel piano. L'aderenza a commander l'ho dedotta dal suo comportamento noto, non l'ho osservata sul binario.
- gas.py non è toccato dal diff: niente kernel né round-trip agentico da rilanciare. Nessun antipattern del Wall of Shame: niente slicing della history, niente simulazione dei tool.

**Memoria**: riga #693-M2 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con scripts/commit_memoria_revisore.sh (commit df3e46e). La lezione: una regex con `\s*X?\s*`, X opzionale, è quadratica come due `\s*` adiacenti; va sondata col prefisso seguito da 100k spazi e niente altro.

Review #694-M2 (bis di #693-M2) sul commit e51ec67 (verdetto integrale):

## VERDETTO: APPROVATO

Review #694-M2 (seconda passata dopo #693-M2) sul diff staged di feat/voce-v12-m2, con base e68a951. Lo SHA-256 del diff staged comincia con 2b665cb9a2ef. Le due riserve aperte nella #693 sono chiuse e non ho trovato problemi nuovi.

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la parte di reports/stato_progetto.md che riguarda claude_cli e la coda di .claude/agents/memoria_revisore.md, comprese le lezioni #672 e #693 sulle regex quadratiche.

Elementi del diff esaminati:
- `brains/claude_cli.py:276` — `_RIFIUTO_EFFORT` ora usa `\s*(?:[:=]\s*)?`: c'è un solo `\s*` libero, perché il secondo può partire solo dopo `:` o `=`. Rischio esaminato: backtracking quadratico (R-693-1-M2). Ho provato 4 testi di circa 1 MB: «unknown» seguito da spazi, «unknown option» seguito da spazi e poi «:», «unknown option =» seguito da spazi e poi «x», e «unknown option » ripetuto 70k volte. Nessuno supera 0,04 s; con la regex vecchia 100k spazi richiedevano 66 s. Esito: ok.
- `brains/claude_cli.py:282` — `_effort_rifiutato` guarda solo stderr e solo con uscita diversa da zero; la regex finisce con `(?![\w-])`. Rischio esaminato: falsi positivi e falsi negativi (R-693-2-M2). Prove: «--effort-level» e «--effort_x» danno False; «--effort=low», «--effort.», «--effort» fra backtick, seguito da codice ANSI, con «(Did you mean …)» o a fine riga danno True. Esito: ok. Nessuna eccezione può uscire: è regex su stringa con `or ""`, quindi niente crash nel provider.
- `tests/test_unit_claude_cli.py:521` — aggiunto il caso «unknown option '--effort-level'» → False alla tabella dei casi; ogni caso controlla anche l'uscita 0 → False. Rischio esaminato: un test che non distingue la correzione. Esito: ok.
- `tests/test_unit_claude_cli.py:567` — `test_effort_rifiutato_tempo_lineare`: «unknown option» più 100k spazi deve finire sotto 1 s. Rischio esaminato: test fragile sulla CI, oppure test che non separa la regex nuova dalla vecchia. Con la regex nuova ci mette pochi millesimi, con la vecchia circa 66 s, quindi il margine c'è e il test boccerebbe un ritorno indietro. Esito: ok.
- `tests/test_unit_claude_cli.py:507` (contesto già visto in #693) — il `finally` rimette `_effort_non_supportato`. Esito: ok.

Ho rilanciato `tests/test_unit_claude_cli.py` nel venv dello scratchpad: 59 passed. Il diff non tocca la storia né `_get_window`, non simula l'output dei tool e non cambia il cap di 10 iterazioni né quello sull'output.

Cosa NON ho verificato: il testo esatto dell'errore della CLI `claude` reale (versione vecchia senza `--effort`) sul Mac o sulla VPS, perché in questo ambiente non posso riprodurlo. La regex copre i formati di commander e yargs con i trattini; yargs senza trattini («Unknown argument: effort») resta False come con la regola vecchia, già accettato in #693. Non ho rilanciato la suite completa, solo il file toccato.

Memoria: ho aggiunto la riga «#694-M2 — 2026-11-06 — APPROVATO — … Nessuna lezione nuova» in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho salvata con `scripts/commit_memoria_revisore.sh` (commit 1a301bd). Il commit successivo bc91ccb corregge un numero di riga sbagliato in quella riga (521 invece di 522). Il diff staged del motore non è stato toccato.

## §5 DELTA TEST DEL MOTORE

gas.py non toccato. `tests/test_unit_claude_cli.py`: +10 casi (4 rifiuti veri, 5 falsi positivi tra cui «invalid» e «--effort-level», tempo lineare) e `finally` nel test dell'effort: `59 passed` (prima 49). Mutante «regola vecchia larga» → 5 failed.

## §6 STATO CI

`gh` non autenticato nel cloud. I commit della sessione e quello di fine-task sono pushati insieme: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna riserva nuova (R-693-1/2-M2 chiuse in #694-M2). Residuo noto: un rifiuto scritto su stdout o nel formato yargs senza trattini («Unknown argument: effort») non è riconosciuto → il turno va in errore dichiarato (la CLI di Claude Code usa commander su stderr).
