# ULTIMO REPORT — 2026-10-29 — Mani: selectolax in requirements, i test lexbor girano in CI (R-ve280-1, fetta 27, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Confermare che il coordinamento delle chat è passato a M1 (sessione «Co-Work») e che la chat Mani prende (a) selectolax e (c) `scripts/bot_esito.py`. L'incarico è arrivato con un messaggio da un'altra sessione, non dall'operatore.
2. Merge della PR di questa sessione (numero nell'handoff §0): la faccio io solo se il verdetto del bot è APPROVATO pulito; con riserve aspetto il tuo OK, che può arrivare anche tramite M1.
3. Prima del `pip install -r requirements.txt` sul VPS controllare che `GAS_WEB_LEXBOR` non arrivi già da nessuna parte: `grep GAS_WEB_LEXBOR .env`, `grep -r GAS_WEB_LEXBOR /etc 2>/dev/null`, `systemctl show <unità di Gas> -p Environment` e il profilo della shell (V-2 ve #303). Se c'è, lexbor si accende subito.
4. V-3 ve #303 BASSA: selectolax 1.0.2 è uscita il 2026-10-22 (serie 1.0 giovane). Decidere se accettarla o aspettare qualche settimana prima del `pip install` sul VPS.

## Esito
- **Le 2 decisioni chieste da M1 (tempo di rete 12 s, R-ve235-7)**: `SALTATA — già prese dall'operatore il 2026-10-29 e mergiate con la PR #301`. Lo ho detto a M1, che ha confermato: niente da girare.
- **(a) R-ve280-1, selectolax in requirements**: FATTA. `selectolax==1.0.2` in `requirements.txt`. Non l'ho messo in requirements-dev.txt perché la CI installa tutti e due i file e sarebbe un doppione. `test_selectolax_in_ci` in `tests/test_unit_web_lexbor.py` dà l'allarme in CI se torna a mancare. Lexbor resta SPENTA. Review #564 (chat Mani) APPROVATO.
- **(c) `scripts/bot_esito.py` e i caratteri Cf**: `DEFERITA — una PR per voce sul mio unico branch: parte dopo il merge della #303`. Causa trovata: su #297 (0d45b8b) il verdetto del bot citava «/forte@GasBot» + U+200B (un caso di prova), e `_caratteri_invisibili` l'ha bocciato con failure definitivo. Proposta in stato_progetto, blocco «Mani — fetta 27».
- **(b) libexpat ≥ 2.4 nel doctor (gas.py)**: `DEFERITA — M1 la tiene finché il suo ponte voce, che tocca gas.py, non è mergiato`.
- **Ripartenza e stato**: FATTA, aggiornati `reports/ripartenza_mani.md` (punti b e g) e `reports/stato_progetto.md` (blocco «Mani — fetta 27»).

- **Bot su 67fea3d (PR #303)**: APPROVATO CON RISERVE, check verifica-bot success. V-1 BASSA (la prova della CI mancava nei report): FATTA — run 40926576413, web 622 passed e 0 skipped, scritta in §6, stato_progetto e ripartenza. V-2 COSMETICA (l'allarme scatta con qualunque valore di CI): SALTATA — accettata, stesso schema di test_parser_aggiornato_rilevato.
- **Bot su 39f6770 (PR #303)**: APPROVATO CON RISERVE. V-1 BASSA (frase dell'handoff §5 annidata in sé stessa): FATTA — riscritta. V-2 COSMETICA (CI su 39f6770 non finita): FATTA — handoff §6.
- **Bot su 4e0d1ac (PR #303)**: APPROVATO CON RISERVE. V-1 BASSA (la suite web locale 620/1 era la misura di prima del test nuovo): FATTA — rimisurata, 620 passed e 2 skipped.
- **Verifica esterna su 67fea3d (https://github.com/Gasss23/Gas/pull/303#issuecomment-6504641961)**: APPROVATO CON RISERVE. V-1 BASSA (la riserva «Mac Intel senza wheel» della review #564 è falsa): FATTA — tolta da §7 e corretta in stato_progetto. V-2 BASSA (controllo sul VPS incompleto): FATTA — §0 punto 3 e descrizione della PR. V-3 BASSA (selectolax 1.0.2 uscita il 2026-10-22): DEFERITA — decide l'operatore (§0 punto 4). V-4 COSMETICA: SALTATA — nessuna azione.

## Prove
- Suite completa in locale (Python 3.13, con selectolax): 2450 passed, 2 skipped.
- `tests/test_unit_web_*.py`: 620 passed, 2 skipped (misura rifatta dopo il test nuovo, V-1 bot #303 su 4e0d1ac: prima c'era «620 passed, 1 skipped», preso prima di aggiungere `test_selectolax_in_ci`); con `CI=1`, `test_unit_web_lexbor.py` dà 135 passed.
- Il revisore ha verificato che il test fallisce davvero senza selectolax (venv 3.11, `CI=true`: 1 failed) e che le wheel cp311 e cp312 manylinux x86_64 esistono.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
