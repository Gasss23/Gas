# ULTIMO REPORT — 2026-10-22 — Chat Mani, fetta 10: annotation-xml e autochiusi nel contenuto estraneo (R6, correzione dopo la verifica esterna #246)

Ramo `feat/mani-web-fetta10` da main 17c0cfc (dopo il merge di #246). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. Merge di questa PR: vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore. Chiude una fuga ALTA oggi su main (V-1 ve #246 bis).
2. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; chiuderla bene richiede un vero costruttore HTML5 (es. lexbor): decide l'operatore.
3. Sul Mac e sulla VPS: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` (dalla cartella di Gas) deve dire True.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **V-1 ve #246 bis (ALTA, regressione della fetta 9)**: `FATTA` — annotation-xml è un punto di integrazione solo con encoding HTML (come i browser); nel ripiego la pila diventa incerta.
- **B-473-1 (ALTA, aggiramento della prima correzione con spazi o attributo doppio)**: `FATTA`.
- **V-2 ve #246 bis (MEDIA preesistente)**: `FATTA` — `<script/>` & co. nel contenuto estraneo sono vuoti davvero.
- **V-4 ve #246 bis (MEDIA, test)**: `FATTA`.
- **R-ve246b-5 (BASSA, perdita di testo)**: `DEFERITA — registrata`.
- **Test**: web suite 291 → 303 (Python 3.13 e 3.11). Enumerazione esaustiva con oracolo lexbor (37 atomi, parser e ripiego, nuovo contro main): 4 atomi, 1,87 M pagine, 0 regressioni e 0 fughe; 5 atomi: in corso alla scrittura dell'handoff.
- **Review**: #473 BOCCIATO, #474 APPROVATO (chat Mani).

## Anomalie

- La verifica esterna di #246 sul commit finale è arrivata dopo il merge (fatto al via del bot, come chiesto dall'operatore) e ha trovato una regressione ALTA: questa fetta la chiude.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…10»).
