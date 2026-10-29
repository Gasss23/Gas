# ULTIMO REPORT — 2026-10-29 — Mani: test del bot dopo la terza verifica esterna su #305 (fetta 29, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #306 (numero nell'handoff §0). Il file dei test fa parte della macchina del bot: il check `verifica-bot` sarà neutral e il merge lo decide l'operatore (anche tramite M1).

## Esito
- **PR #305**: MERGIATA (a5b1c62). Terza verifica esterna su 586b888 (https://github.com/Gasss23/Gas/pull/305#issuecomment-6506958440): APPROVATO CON RISERVE, nessun difetto del bot.
- **V-1 ve #305 (terza) BASSA** (due mutanti sopravvivevano a test verdi): FATTA — test positivo sul titolo con un invisibile (U+200B, U+3164, U+2060, \x1b; niente separatori di riga, R-576-1) e `test_controlli_bidi` con ogni controllo da solo.
- **V-2 ve #305 (terza) BASSA** (falso NO prudente quando il bot cita un invisibile attaccato a parole come «multimedia»): FATTA — registrata come compromesso accettato in stato_progetto, codice invariato (via libera di M1).
- **V-3 ve #305 (terza) COSMETICA** (copia degli intervalli non legata al gate): FATTA — `test_invisibili_come_nel_gate`.
- **V-4 / V-5 ve #305 (terza) COSMETICHE** (report e taglio della review): SALTATE — report superati, resa solo estetica.
- **Review #576 (chat Mani)**: APPROVATO CON RISERVE (R-576-1 BASSA: il test positivo usava \x0b, un separatore di riga, che avrebbe bloccato R-572-1): FATTA, parametro sostituito. **Review #577**: APPROVATO.

## Prove
- `tests/test_unit_verifica_bot.py`: 510 passed.
- Mutanti ora presi: senza lo strip prima del titolo 4 failed; ognuno dei 9 controlli bidi tolto da `_BIDI` 1 failed; un intervallo diverso dal gate 1 failed.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
