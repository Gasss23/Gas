# ULTIMO REPORT — 2026-10-22 — Chat Mani, fetta 11: tag con virgolette aperte, annotation-xml speciale, chiusure di blocco in scope (R6)

Ramo `feat/mani-web-fetta11` da main 2d20ec0 (dopo il merge di #248). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. Merge di questa PR: vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
2. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; chiuderla bene richiede un vero costruttore HTML5 (es. lexbor): decide l'operatore.
3. Sul Mac e sulla VPS: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` (dalla cartella di Gas) deve dire True.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **R-ve248-3 (fuga preesistente, tag con virgolette aperte)**: `FATTA`.
- **V-1 bot #248 (perdita, annotation-xml)**: `FATTA`.
- **R-ve246b-5 (perdita su HTML valido in svg/math)**: `FATTA` per le chiusure di blocco in scope; restano incerti (verso sicuro) i casi con confini, formattanti o elementi che il browser chiude da solo (p, li, dd, dt, h1–h6, tabelle).
- **B-476-1 (ALTA, trovata dal revisore nella prima versione)**, **R-476-1 (BASSA)**: `FATTA`.
- **Test**: web suite 304 → 318 (Python 3.13 e 3.11). Oracolo lexbor, nuovo contro main: 0 fughe nuove e 0 perdite nuove su circa 9 milioni di pagine (enumerazioni esaustive e campioni).
- **Review**: #476 BOCCIATO, #477 APPROVATO (chat Mani).

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…11»).
