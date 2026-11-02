# Ultimo report — 2026-11-02 — Cervello forte: difesa contro il futuro default `--bare` di `claude -p` (chat M2) — PR #321

## DECISIONI UMANE RICHIESTE

1. Merge della PR #321 (https://github.com/Gasss23/Gas/pull/321): stanotte niente merge (M1); decide l'operatore.
2. Sul Mac: `python3 gas.py doctor` e controllare la riga «Cervello forte · login» (deve dire «login dell'abbonamento»).

## Esito delle fette

- **1. Figlio senza chiavi API (fail-closed)**: `FATTA` — già vero con la lista di variabili permesse; ora un test lo fissa (niente ANTHROPIC_*, *_API_KEY, CLAUDE_CODE_SIMPLE, BEDROCK; sì CLAUDE_CODE_OAUTH_TOKEN; niente `--bare` né `--settings`). Se `claude -p` diventa bare, fallisce col login invece di addebitare.
- **2. Flag per restare non-bare**: `FATTA (nessuno)` — lette headless, cli-reference, authentication: nessun flag o variabile documentata. Scritto nel docstring di `brains/claude_cli.py`.
- **3. Riga «login» nel doctor**: `FATTA` — `stato_abbonamento()` in `brains/claude_cli.py` (`claude --version` + `claude auth status`, stesso ambiente del figlio, zero token, mai eccezioni); in `gas.py` 3 righe autorizzate da M1.
- Review #632-M2 BOCCIATO (crash del doctor con output vuoto o non UTF-8 della CLI) → corretto → #633-M2 APPROVATO CON RISERVE (BASSE: nipote che tiene le pipe/attesa max ~30 s; `errors="replace"` senza test dedicato, coperto dal ramo ValueError).
- Test: claude_cli + dotenv 61 passed; kernel 1063 PASS 0 FAIL (prima della correzione di #632, che tocca solo `stato_abbonamento`).

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- Non verificato con una CLI `claude` vera e loggata (qui non c'è): il campo `authMethod` viene dalla documentazione.
