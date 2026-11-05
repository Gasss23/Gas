# Diff della sessione — 2026-11-05 — Fetta bot (chat M2)

- `scripts/bot_esito.py` — `_BLOCCANTE_TECNICO` («read bloccante» non è una gravità), `_CITAZIONE_VERIFICA_PASSATA` (citazione di una verifica passata per SHA non è un titolo), `leggi_verdetto()` (verdetto compresso gzip+base64, tetto 1 MB).
- `.github/workflows/verifica-bot.yml` — output `verdetto_gz` al posto di `verdetto` in chiaro; `VERDETTO_GZ` al job esito; rischio R-671-3-M2 dichiarato nel commento.
- `tests/test_unit_verifica_bot.py` — test sui due verdetti veri, casi avversari delle review #671–#673, verdetto compresso, passo «Raccogli il verdetto» eseguito davvero.
- `tests/dati_verifica_bot/verdetto_336_e619103.txt`, `tests/dati_verifica_bot/verdetto_329_7957a15.txt` — i due verdetti veri del bot.
- `.claude/agents/memoria_revisore.md` — review #671–#673-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/ripartenza_m2.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
