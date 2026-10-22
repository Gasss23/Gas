# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 10)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `_Contesto`: annotation-xml punto di integrazione solo con encoding HTML (`_cima_punto`, `_metti(..., punto)`, `apri(..., html_dentro)`), incerta nel ripiego; `_esito_autochiuso`: vuoto nel contenuto estraneo; `_Estrattore._html_dentro` (primo encoding, valore esatto, maiuscole ASCII).
- `tests/test_unit_web_leggi.py` — sonde V-1/V-2 della verifica esterna #246 bis, B-473-1, controprova con encoding HTML, test di tempo (303 test).
- `.claude/agents/memoria_revisore.md` — righe #473, #474 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 10».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
