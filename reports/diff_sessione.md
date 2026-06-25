# Diff sessione — 2026-06-25 R-reidx-3 + Token accounting

> Si riscrive a ogni sessione. La storia completa sta in git.

## File toccati

| File | Cosa |
|---|---|
| `modules/memory/vectors.py` | `REINDEX_BATCH_SIZE=256` + `ricostruisci_da_diario` riscritto a batch |
| `gas.py` | `TOKEN_LOG_FILENAME`, `_log_tokens`, `tokens_cmd`, dispatch `gas tokens` |
| `tests/test_unit_kernel.py` | T35a, T35b, T36a, T36b, T36c (5 nuovi test) |
| `.gitignore` | `.gas_tokens.jsonl` aggiunto |
| `reports/stato_progetto.md` | Review count 28→30, R-reidx-3 aggiornato, CLI gas tokens |
| `.claude/agents/memoria_revisore.md` | Lezione review #30 |
| `reports/ultimo_report.md` | Report task corrente |
| `reports/diff_sessione.md` | Questo file |

## Cosa è cambiato e perché

**R-reidx-3 (batch reindex):** Il metodo `ricostruisci_da_diario` materializzava
l'intero diario in RAM (numpy array full-size) prima del DELETE. Ora legge il diario
pagine di 256 righe via `diario_dopo`, i numpy array sono transitori per batch, e
l'atomic swap avviene solo se tutti i batch riescono. Invariante di sicurezza mantenuta.

**Token accounting:** GAS non aveva alcuna visibilità sui token spesi per provider.
`_log_tokens` scrive una riga JSONL per ogni API call in `run_turn`; `gas tokens [N]`
aggrega e stampa la tabella. Zero token LLM, fail-safe, gitignorato.

**Review #30:** APPROVATO CON RISERVE. Riserve R30-1 (gitignore) e R30-2 (int ValueError)
chiuse prima del commit. R30-3 e R30-4 dichiarate in stato_progetto e memoria_revisore.
