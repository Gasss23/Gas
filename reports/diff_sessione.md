# DIFF SESSIONE — 2026-10-29 — Mani fetta 26

File toccati rispetto a main f8b35ae (PR #296 mergiata):
- `modules/web/leggi.py` — `_taglio_xml`: le entità che html.parser non sa espandere (della pagina, esterne, sconosciute col DTD XHTML) fermano la lettura prima del riferimento, posizione presa nel gestore; seconda lettura senza rinvio dei token grandi; `_componi`: riga di avviso quando l'XHTML si taglia.
- `tests/test_unit_web_leggi.py` — casi di taglio sulle entità, entità di parametro non lette, avviso nel testo, token di 3 MB, test R-553-1 riscritto con un ATTLIST.
- `.claude/agents/memoria_revisore.md` — riga della review #560 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 26» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — PR #296 mergiata, fetta 26.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
