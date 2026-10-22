# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 7)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — grezzi autochiusi in testo grezzo (`_GREZZI_AUTOCHIUSI`, `_modo_grezzo`), esenzione dentro svg/math solo per i non nascosti, ripiego allineato; `_commenti_e_cdata_xml` per XHTML; noembed e noframes fra i nascosti; in XHTML commento o CDATA dentro un tag porta via il resto.
- `tests/test_unit_web_leggi.py` — sonde R-453-1, R-454-1, template, XHTML (commenti, CDATA, linearità, ripiego), html.parser vecchio noembed/noframes (192 test).
- `.claude/agents/memoria_revisore.md` — righe #453-#456, #461, #462 (chat Mani), più quelle della chat Motore portate dal merge.
- Dal merge di main (PR #241, chat Motore, non di questa sessione): `gas.py`, `modules/notte/`, `modules/telegram/bot.py`, test kernel e notte, `scripts/notte/catalogo_esempio.yaml`, `reports/roadmap.md`, `reports/da_mergiare.md`.
- `reports/stato_progetto.md` — blocco «Mani — fetta 7».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
