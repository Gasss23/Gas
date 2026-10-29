# DIFF SESSIONE — 2026-10-29 — Mani fetta 25 (PR #296)

File toccati rispetto a main dc43ad6 (dopo il merge di main con la PR #292):
- `modules/web/leggi.py` — `_PUBBLICI_XHTML`, `_dtd_entita()`, `_taglio_xml()` (XHTML letto fino al primo errore XML); in `_componi` il taglio prima di `_commenti_e_cdata_xml`, con warning nella scatola nera.
- `tests/test_unit_web_leggi.py` — helper `_radice` per i frammenti dei test XHTML vecchi; test nuovi sull'XHTML malformato, troncato, bomba di entità, expat vecchio, tempi.
- `tests/test_unit_web_lexbor.py` — tabella dei punti d'integrazione e malignmark (V-1 ve #294).
- `.claude/agents/memoria_revisore.md` — righe delle review #550–#552 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 25» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — PR #296, punto e) in parte fatto.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
