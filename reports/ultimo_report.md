# ULTIMO REPORT — 2026-10-29 — Mani: test del bot dopo la terza verifica esterna su #305 (fetta 29, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #306: secondo M1 l'operatore ha detto «mergia #306» e la mergia M1 a CI verde (macchina del bot, check neutral).
2. Confermare il via libera di M1 ad accettare V-2 ve #305 come compromesso (la verifica esterna #306 non può provarlo dal repo), e decidere il rimedio proposto: istruire il bot a scrivere gli invisibili come «<U+XXXX>» (PROMPT in .github/workflows/verifica-bot.yml).

## Esito
- **PR #305**: MERGIATA (a5b1c62). Terza verifica esterna su 586b888 (https://github.com/Gasss23/Gas/pull/305#issuecomment-6506958440): APPROVATO CON RISERVE, nessun difetto del bot.
- **V-1 ve #305 (terza) BASSA** (due mutanti sopravvivevano a test verdi): FATTA — test positivo sul titolo con un invisibile (U+200B, U+3164, U+2060, \x1b; niente separatori di riga, R-576-1) e `test_controlli_bidi` con ogni controllo da solo.
- **V-2 ve #305 (terza) BASSA** (falso NO prudente quando il bot cita un invisibile attaccato a parole come «multimedia»): FATTA — registrata come compromesso accettato in stato_progetto, codice invariato (via libera di M1).
- **V-3 ve #305 (terza) COSMETICA** (copia degli intervalli non legata al gate): FATTA — `test_invisibili_come_nel_gate`.
- **V-4 / V-5 ve #305 (terza) COSMETICHE** (report e taglio della review): SALTATE — report superati, resa solo estetica.
- **Review #576 (chat Mani)**: APPROVATO CON RISERVE (R-576-1 BASSA: il test positivo usava \x0b, un separatore di riga, che avrebbe bloccato R-572-1): FATTA, parametro sostituito. **Review #577**: APPROVATO.

- **Bot su 204a6c1 (PR #306)**: APPROVATO CON RISERVE, check verifica-bot neutral («decide l'operatore»). V-1 BASSA (il test «uguali al gate» lega solo gli intervalli, non _CATEGORIE_INVISIBILI): DEFERITA — riserva, alla prossima fetta sui test del bot. V-2 COSMETICA (import di modules.gate solo dalla radice del repo): DEFERITA — come tests/test_unit_gate.py, va bene in CI.
- **Verifica esterna su 204a6c1 (https://github.com/Gasss23/Gas/pull/306#issuecomment-6510340226)**: APPROVATO CON RISERVE. V-1 BASSA (la stessa V-1 del bot): DEFERITA. V-2 BASSA (import da radice): DEFERITA. V-3 BASSA (§6 diceva «nessuna run» per b692e27, che ha la run 40966074777 con handoff-check failure intermedio): FATTA — §6 corretto qui. V-4 COSMETICA (§3 senza 14c4983): FATTA — §3 rigenerato dalla nuova base. V-5 COSMETICA (invisibili del titolo solo a metà parola): SALTATA — nessun rischio. Nota: chiede che l'operatore confermi lui il via libera di M1 su V-2 ve #305 come compromesso.
- **Merge di origin/main 52c113b (PR #307 di M1)**: FATTA — la #306 era in conflitto (solo report). Review #578 (chat Mani) APPROVATO. Il sì dell'operatore al merge della #306 («mergia #306») è arrivato a M1, che la mergia.
- **Merge di origin/main 7ab6fc4 (PR #308 di M2, voce)**: FATTA — nuovo conflitto, solo report e memoria. Review #579 (chat Mani) APPROVATO.

## Prove
- `tests/test_unit_verifica_bot.py`: 510 passed.
- Mutanti ora presi: senza lo strip prima del titolo 4 failed; ognuno dei 9 controlli bidi tolto da `_BIDI` 1 failed; un intervallo diverso dal gate 1 failed.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
