# Ultimo report — 2026-11-02 — Cervello forte: difesa contro il futuro default `--bare` di `claude -p` (chat M2) — PR #321

## DECISIONI UMANE RICHIESTE

1. Merge della PR #321 (https://github.com/Gasss23/Gas/pull/321): stanotte niente merge (M1); decide l'operatore.
2. Sul Mac: `python3 gas.py doctor` e controllare la riga «Cervello forte · login» (deve dire «login dell'abbonamento»).

## Esito delle fette

- **1. Figlio senza chiavi API (fail-closed)**: `FATTA` — già vero con la lista di variabili permesse; ora un test lo fissa (niente ANTHROPIC_*, *_API_KEY, CLAUDE_CODE_SIMPLE, BEDROCK; sì CLAUDE_CODE_OAUTH_TOKEN; niente `--bare` né `--settings`). Se `claude -p` diventa bare, fallisce col login invece di addebitare.
- **2. Flag per restare non-bare**: `FATTA (nessuno)` — lette headless, cli-reference, authentication: nessun flag o variabile documentata. Scritto nel docstring di `brains/claude_cli.py`.
- **3. Riga «login» nel doctor**: `FATTA` — `stato_abbonamento()` in `brains/claude_cli.py` (`claude --version` + `claude auth status`, stesso ambiente del figlio ma senza i suoi flag: è un'indicazione, WARN in più possibili, mai un OK falso; zero token, mai eccezioni); in `gas.py` 3 righe autorizzate da M1.
- Review #632-M2 BOCCIATO (crash del doctor con output vuoto o non UTF-8 della CLI) → corretto → #633-M2 APPROVATO CON RISERVE (BASSE: nipote che tiene le pipe/attesa max ~30 s; `errors="replace"` senza test dedicato, coperto dal ramo ValueError).
- **V-1 verifica esterna su d0a0035** («abbonamento» anche con CLI non loggata): `FATTA` — OK solo con exit 0 (regola poi stretta a «loggedIn booleano vero o assente», vedi sotto); review #634-M2 APPROVATO.
- **V-1 bot su 5e784c3** (i test T99 della suite kernel lanciavano il `claude` vero della macchina dal doctor): `FATTA` — in `_doc99` la riga «login» usa un finto; review #635-M2 APPROVATO CON RISERVE. **R-635-1** (con `GAS_CLAUDE_CLI=1` esportato nella shell altri doctor della suite lo lanciavano ancora): `FATTA` — la suite toglie l'interruttore in testa; review #636-M2 APPROVATO. V-2 bot (handoff e stato_progetto non allineati): `FATTA` in questo giro di report.
- **V-1 verifica esterna su c83032f** (`loggedIn` come stringa "false" dava OK): `FATTA` — «loggato» solo col booleano vero o col campo assente; review #637-M2 CON RISERVE (commento, chiusa) → #638-M2 APPROVATO. V-2 ve / V-1 bot (conteggio 42 → 44 nell'handoff): `FATTA`.
- **V-1 bot su 6c0cf68** (riga «login» sulla CLI della shell anche col WARN del timer): `FATTA` — il dettaglio lo dice. **V-1 ve su 36f790f** (test di dotenv che lanciavano il `claude` vero): `FATTA`. Review #639-M2 APPROVATO. V-2 ve (maiuscolo CLAUDE.AI, resta WARN): COSMETICA, nessun fix.
- **Bot su 36f790f**: V-2 (il controllo «login» non usa i flag del figlio) `FATTA` correggendo l'affermazione nel commento, review #640-M2 APPROVATO; V-3 (formulazione nei report) `FATTA`.
- Test: claude_cli + dotenv 65 passed; anche con GAS_CLAUDE_CLI=1 e un `claude` spia (mai chiamata); kernel 1063 PASS 0 FAIL, anche con `GAS_CLAUDE_CLI=1` e un `claude` spia nel PATH (spia mai chiamata).

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- Non verificato con una CLI `claude` vera e loggata (qui non c'è): il campo `authMethod` viene dalla documentazione.
