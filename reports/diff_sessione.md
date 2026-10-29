# DIFF SESSIONE — 2026-10-29 — Mani fetta 25 (PR #296)

File toccati rispetto a main 4e8eb9f (dopo i merge di main con le PR #292 e #295):
- `modules/web/leggi.py` — `_PUBBLICI_XHTML`, `_dtd_entita()`, `_taglio_xml()` (XHTML letto fino al primo errore XML, DTD delle entità letto una volta per pagina); in `_componi` il taglio prima di `_commenti_e_cdata_xml`, con warning nella scatola nera.
- `tests/test_unit_web_leggi.py` — helper `_radice` per i frammenti dei test XHTML vecchi; test nuovi sull'XHTML malformato, troncato, bomba di entità, expat vecchio, DTD letto una volta, lunghezza esatta del taglio, tempi; commenti e CDATA provati anche senza taglio.
- `tests/test_unit_web_lexbor.py` — tabella dei punti d'integrazione e malignmark (V-1 ve #294).
- `.claude/agents/memoria_revisore.md` — righe delle review #550–#555 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 25» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — PR #296, punto e) in parte fatto.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
