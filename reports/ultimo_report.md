# ULTIMO REPORT — 2026-10-29 — Mani: selectolax in requirements, i test lexbor girano in CI (R-ve280-1, fetta 27, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Confermare che il coordinamento delle chat è passato a M1 (sessione «Co-Work») e che la chat Mani prende (a) selectolax e (c) `scripts/bot_esito.py`. L'incarico è arrivato con un messaggio da un'altra sessione, non dall'operatore.
2. Merge della PR di questa sessione (numero nell'handoff §0): la faccio io solo se il verdetto del bot è APPROVATO pulito; con riserve aspetto il tuo OK, che può arrivare anche tramite M1.
3. Prima del `pip install -r requirements.txt` sul VPS: `grep GAS_WEB_LEXBOR .env`. Se la variabile c'è già, lexbor si accende subito.

## Esito
- **Le 2 decisioni chieste da M1 (tempo di rete 12 s, R-ve235-7)**: `SALTATA — già prese dall'operatore il 2026-10-29 e mergiate con la PR #301`. Lo ho detto a M1, che ha confermato: niente da girare.
- **(a) R-ve280-1, selectolax in requirements**: FATTA. `selectolax==1.0.2` in `requirements.txt`. Non l'ho messo in requirements-dev.txt perché la CI installa tutti e due i file e sarebbe un doppione. `test_selectolax_in_ci` in `tests/test_unit_web_lexbor.py` dà l'allarme in CI se torna a mancare. Lexbor resta SPENTA. Review #564 (chat Mani) APPROVATO.
- **(c) `scripts/bot_esito.py` e i caratteri Cf**: `DEFERITA — una PR per voce sul mio unico branch: parte dopo il merge della #303`. Causa trovata: su #297 (0d45b8b) il verdetto del bot citava «/forte@GasBot» + U+200B (un caso di prova), e `_caratteri_invisibili` l'ha bocciato con failure definitivo. Proposta in stato_progetto, blocco «Mani — fetta 27».
- **(b) libexpat ≥ 2.4 nel doctor (gas.py)**: `DEFERITA — M1 la tiene finché il suo ponte voce, che tocca gas.py, non è mergiato`.
- **Ripartenza e stato**: FATTA, aggiornati `reports/ripartenza_mani.md` (punti b e g) e `reports/stato_progetto.md` (blocco «Mani — fetta 27»).

## Prove
- Suite completa in locale (Python 3.13, con selectolax): 2450 passed, 2 skipped.
- `tests/test_unit_web_*.py`: 620 passed, 1 skipped; con `CI=1`, `test_unit_web_lexbor.py` dà 135 passed.
- Il revisore ha verificato che il test fallisce davvero senza selectolax (venv 3.11, `CI=true`: 1 failed) e che le wheel cp311 e cp312 manylinux x86_64 esistono.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
