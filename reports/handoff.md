# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-24 — Chat Motore: R2 via B fetta 4 (costi grandi contati, forte ancora spento)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #264 (https://github.com/Gasss23/Gas/pull/264): tocca il motore, review #507 APPROVATO CON RISERVE.
2. Prova del login sul Mac prima di accendere il forte (R-496-3).
3. Testo nuovo dell'attività di notte da chiedere nella sessione fissa; 3 lezioni da approvare sul Mac.

---

## §1 SCOPE & ESITO FETTE

- **Costo grande riportato dalla CLI (V-1 ve #262)**: `FATTA`.
- **Limite dei processi in parallelo dichiarato (V-1 bot #262)**: `FATTA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 brains/claude_cli.py               |  16 ++++++++++------
 gas.py                             |   5 ++++-
 reports/diff_sessione.md           |  15 ++++++---------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  21 ++++++++-------------
 tests/test_unit_claude_cli.py      |  12 ++++++++++++
```

NB: regola «n/d» — la riga di `reports/handoff.md` è n/d e la riga di totale è tolta; le altre righe sono prese con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
cf158dd fix(r2): fetta 4 — un costo grande riportato dalla CLI conta e ferma il forte
f6e9066 chore(revisore): memoria review #507 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare nel log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore: cf158dd `fix(r2): fetta 4`.

## VERDETTO: APPROVATO CON RISERVE

Review #507 (chat Motore), 2026-10-24. Diff staged: R2 via B fetta 4, con V-1 della verifica esterna #262 e V-1 del bot #262 al secondo giro. Prima della review ho letto CLAUDE.md (sezioni 5, 8, 9), `reports/stato_progetto.md` (le parti che servivano) e `.claude/agents/memoria_revisore.md`.

**Elementi del diff esaminati**
- `brains/claude_cli.py:204` — `float(v)` dentro `try`; con OverflowError ora `v = inf` invece di nan. Rischio esaminato: un intero enorme non deve diventare un costo zero o la stima. Esito: ok per `+10**400`, che vale 1e6 (provato).
- `brains/claude_cli.py:211` — `max(min(v, _COSTO_MASSIMO), pavimento)` quando `v > 0` e non è nan. Rischio esaminato: un costo grande scartato a favore della stima. Ho provato 999.9, 1000, 1e308, +inf e 10**400: si ottiene il valore stesso fino a 1e6, oltre resta 1e6. Restano scartati e passano alla stima col pavimento 0.0015: nan, -inf, -5, 0, -0.0, 1e-9, True, '5' e None. Esito: ok, ma vedi la riserva R-507-1.
- `gas.py:1648` (contesto, `_registra_uso_claude_cli`) — 1e6 è finito, quindi supera `isfinite` e viene sommato. Prova diretta su una cartella temporanea: dopo `_registra_uso_claude_cli(1e6)` la lettura del conto dà 1000000.0, `_forte_senza_conto` resta False e `_tetto_claude_cli_superato` restituisce `(1000000.0, 4.6)`, quindi il tetto scatta. Esito: ok.
- `gas.py:981` (contesto, `_leggi_uso_claude_cli`) — rifiuta `usd ≥ 1e9`. Rischio esaminato: che il valore massimo renda il conto illeggibile e così si perda il conteggio. 1e6 sta sotto 1e9. Per arrivare a 1e9 servirebbero circa 1000 chiamate da 1e6 nello stesso giorno, il che non può succedere: il tetto si può alzare al massimo a 1000. Anche in quel caso il valore conta come illeggibile (None), cioè forte fermo e non conto azzerato. Nessun percorso porta a perdere il conto. Esito: ok.
- `gas.py:4690` e `gas.py:4722` (contesto) — sono gli unici due punti che usano `costo_equivalente_usd`: il ramo d'errore e quello riuscito, ed entrambi passano da `_registra_uso_claude_cli`. Non c'è un altro percorso che trasformi un valore enorme in perdita di conto. Esito: ok.
- `gas.py:1687` — solo docstring: dichiara che il controllo avviene prima della chiamata e fuori dal lucchetto, quindi due processi in parallelo possono sforare il tetto di al massimo una chiamata ciascuno. È coerente col codice: il lucchetto copre solo la lettura, la somma e la scrittura della registrazione. Esito: ok.
- `tests/test_unit_claude_cli.py:323` — il test nuovo copre 1000, 5e7, inf, 10**400, -5 e nan. Esito: ok. Non copre un negativo enorme (vedi la riserva).

**§9:** `_costo_equivalente` non solleva eccezioni: OverflowError è gestito e min/max su float finiti o infiniti non rompono. Gli errori di `_registra_uso_claude_cli` restano intercettati e scritti nel log, con il forte fermo (`finally`). Nessuno slicing della history, nessun output di tool simulato, cap a 10 iterazioni non toccato.

**Riserve**
- R-507-1 (BASSA): `total_cost_usd = -10**400` va in OverflowError come +10**400, diventa inf e conta 1e6, invece di essere scartato come gli altri negativi. La direzione è sicura (il forte si ferma), quindi non blocca. Però docstring e test dicono «negativo scartato». Correzione proposta: nel ramo OverflowError `v = float("inf") if v > 0 else float("nan")` (confrontando l'int originale), più un caso `-10**400` nel test.

**Rischio escluso:** non ho verificato il comportamento con la CLI `claude` vera, perché il forte è spento e qui `claude` non è installato. Non ho rilanciato la suite kernel completa (1039) né pytest completo (2144): mi fido dei numeri dichiarati. Ho rilanciato solo `tests/test_unit_claude_cli.py`: 23 passed.

**Memoria:** aggiunta la riga #507 e una lezione nuova (controllare il segno dell'input quando un ramo d'eccezione assegna un valore estremo). Committata con `scripts/commit_memoria_revisore.sh` (commit f6e9066, solo `/home/user/Gas/.claude/agents/memoria_revisore.md`). L'index del diff sotto review non è stato toccato.

**Cosa devi fare tu:**
1. Scrivi R-507-1 in `/home/user/Gas/reports/stato_progetto.md`, oppure correggila subito con la modifica proposta sopra.
2. Poi `bash scripts/segna_review_ok.sh` e commit.

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: 1039 → 1039 PASS, 0 FAIL (nessun test kernel nuovo).
  `=== RIEPILOGO: 1039 PASS, 0 FAIL ===`
- `pytest tests/test_unit_claude_cli.py`: 22 → 23 passed.
- `pytest tests/` completo: `2144 passed, 1 skipped in 194.48s (0:03:14)`.

## §6 STATO CI

`gh run list -L 3` alle 23:58 UTC:

```
queued		fix(r2): fetta 4 — un costo grande riportato dalla CLI conta e ferma …	CI	feat/merge-automatico-z1xjx2	push	40144841180	1s	2026-10-24T23:58:14Z
completed	success	feat(web): fetta 15 Mani — </template> sopra svg/math come il browser (R6)	verifica-bot	feat/mani-web-fetta15	pull_request_target	40144552184	4m33s	2026-10-24T23:53:35Z
completed	success	docs(reports): fetta 15 chat Mani — verdetto #505 riemesso per il gate B	CI	feat/mani-web-fetta15	push	40144551374	2m52s	2026-10-24T23:53:34Z
```

Mappatura: f6e9066 e cf158dd pushati insieme (run sulla testa cf158dd); commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-507-1** (BASSA): un `total_cost_usd` negativo enorme conta come 1e6 invece di essere scartato (direzione sicura).
- **R-496-3** (BASSA): prova del login vero sul Mac/VPS.
- Le altre riserve del forte restano in `reports/stato_progetto.md`.
