# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — chat Motore: motivo vero dell'errore del cervello forte e avviso doctor per il PATH della notte (punto 3 della RIPARTENZA)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #286 (https://github.com/Gasss23/Gas/pull/286): review #538 APPROVATO CON RISERVE, quindi decide l'operatore (CLAUDE.md §10). Numero e URL dalla risposta JSON dello strumento GitHub `create_pull_request` (`gh` non autenticato in questo ambiente).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Motivo vero dell'errore del forte nel report della notte**: `FATTA` — `ErroreClaudeCli` (testi fissi) in `brains/claude_cli.py`; il «Pipeline esausta» ne mostra il testo, gli altri errori solo il tipo.
- **Fetta 2 — `gas doctor` avvisa se `claude` sta solo nel PATH del terminale**: `FATTA` — WARN «comando claude (notte)» con il rimedio `GAS_CLAUDE_BIN=<percorso>`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  1 +
 brains/claude_cli.py               | 29 ++++++++++++++++++-----------
 gas.py                             | 13 ++++++++++++-
 reports/diff_sessione.md           | 10 ++++++----
 reports/stato_progetto.md          |  6 +++---
 reports/ultimo_report.md           | 12 +++++++-----
 tests/test_unit_kernel.py          | 48 ++++++++++++++++++++++++++++++++++++++++++++++++
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d» e niente riga di totale. Conteggi presi con i report in stage.

## §3 GIT LOG --ONELINE (sessione)

```
8ce1561 fix(forte): motivo vero dell'errore del cervello forte nel report e avviso doctor per il PATH della notte
933c4b9 chore(revisore): memoria review #538 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #538 (chat Motore) — sul diff di 8ce1561

## VERDETTO: APPROVATO CON RISERVE

Review #538 (chat Motore). Prima della review ho letto CLAUDE.md (sez. 5), la sezione «RIPARTENZA» di reports/stato_progetto.md e la mia memoria. Il diff staged è su brains/claude_cli.py, gas.py e tests/test_unit_kernel.py. Ho rifatto la suite kernel: **1062 PASS, 0 FAIL**.

**Elementi del diff esaminati**
- `brains/claude_cli.py:169` — la nuova `ErroreClaudeCli(RuntimeError)`. Rischio: un messaggio con testo esterno o della conversazione. Ho controllato uno per uno tutti i punti in cui il client solleva l'errore (righe 323, 326, 336, 337, 341, 351, 364, 365, 369, 373, 375):
  - i testi sono fissi;
  - `self.timeout` è la costante del kernel;
  - `proc.returncode` è un intero;
  - `tipo` (`brains/claude_cli.py:360`) è filtrato a `[a-z_]` e tagliato a 40 caratteri;
  - `_prefisso_limite` (`brains/claude_cli.py:185`) restituisce solo «429 » oppure una stringa vuota;
  - `from e` non finisce dentro `str(e)`.

  Esito: **ok**.
- `brains/claude_cli.py:346` — il blocco `except RuntimeError: raise` ripassa le eccezioni di `_risposta`. Rischio: una `RuntimeError` che non è `ErroreClaudeCli` (per esempio una `RecursionError`) mostrata come testo. Non è `ErroreClaudeCli`, quindi run_turn mostra solo il nome del tipo. Esito: **ok**.
- `gas.py:4888` — `str(e)[:300]` solo se `isinstance(e, ErroreClaudeCli)`, altrimenti il nome del tipo; l'HTTP status resta prioritario. Rischio: testo grezzo nel «Pipeline esausta». Ho provato il mutante `if True` (testo mostrato sempre): **T99x FAIL** (1061/1), quindi il test lo prende. Nel codice nessun altro punto controlla il nome "RuntimeError". Esito: **ok**.
- `gas.py:4881` — `_classify_provider_error`, invariato. Rischio: cambio della classificazione QUOTA/429. Tutti i messaggi sono identici a prima, tranne «non trovato», che non contiene «429». La prefissazione con «429 » resta uguale. Esito: **ok**.
- `gas.py:4961` — il WARN «comando claude (notte)» con `shutil.which(..., path=PATH_TIMER_NOTTE)`.
  - Se `GAS_CLAUDE_BIN` contiene una barra, `which` ignora `path`: un percorso assoluto non fa scattare il WARN (lo prova T99z).
  - Un nome nudo diverso da `claude` fa scattare il WARN col rimedio giusto.
  - Il plist (`scripts/notte/com.gas.notte.plist:11`) lancia `zsh -c` non interattivo più il venv: non c'è un PATH personalizzato, quindi l'ipotesi del PATH di launchd è corretta sul Mac.

  Esito: **riserva** (R-538-1).
- `tests/test_unit_kernel.py:11119` (T99v–T99x) e `tests/test_unit_kernel.py:11218` (T99y–T99z) — rischio: test che passano anche col codice sbagliato. Il mutante sopra viene preso. PATH e `GAS_CLAUDE_BIN` vengono ripristinati nel `finally`. Esito: **ok**, con una nota cosmetica (R-538-2).

**Riserve**
- **R-538-1 BASSA**: `PATH_TIMER_NOTTE` è il PATH di default di launchd. Su un futuro VPS Linux con timer systemd, che include `/usr/local/bin`, il WARN può scattare a torto se `claude` sta in `/usr/local/bin`. Il danno è limitato: è solo un WARN, l'uscita resta 0 e il rimedio suggerito è innocuo. Da rivedere quando il giro di notte arriva sul VPS.
- **R-538-2 COSMETICA**: T99y non cancella la cartella creata con `mkdtemp` (sta sotto la cartella temporanea della run).

**Cosa NON ho verificato**
- Il comportamento reale di launchd sul Mac (PATH effettivo con `zsh -c` e `~/.zshenv`): non si riproduce in questo ambiente Linux. Il giro del 29 ottobre resta la prova vera.
- La CLI `claude` vera: tutti i test usano runner finti.

**Memoria**: aggiunta la riga #538 in .claude/agents/memoria_revisore.md e committata con lo script (commit 933c4b9). Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

Suite kernel: 1057 → 1062 PASS (T99v, T99w, T99x, T99y, T99z nuovi), 0 FAIL.

```
=== RIEPILOGO: 1062 PASS, 0 FAIL ===
```

pytest (tutti i file tranne la suite kernel): `2265 passed, 61 skipped in 203.49s (0:03:23)`.

## §6 STATO CI

CI letta con lo strumento GitHub della sessione: `gh run list` non è disponibile (`gh` non autenticato: «Failed to log in to github.com using token (GH_TOKEN)»).

Mappatura commit→run:
- `933c4b9`: nessuna run su questo SHA (pushato insieme a `8ce1561`).
- `8ce1561` → run 40736243983: `handoff-check` failure (atteso: l'handoff non era ancora stato riscritto per questa sessione); `unit-suite` in corso alla scrittura. Run 40736281751 (`verifica-bot`): in corso alla scrittura.
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-538-1 BASSA: sul VPS con timer systemd il WARN «comando claude (notte)» può scattare a torto se `claude` sta in `/usr/local/bin`.
- R-538-2 COSMETICA: T99y non cancella la cartella creata con `mkdtemp`.
