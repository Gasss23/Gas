# Ultimo report — 2026-11-10 — Analisi notturna di Gas e correzioni dei bug riprodotti (M1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #366 (https://github.com/Gasss23/Gas/pull/366) quando bot e CI sono verdi: tocca il messaggio di firma (solo la vista), quindi è una PR di sicurezza.
2. R-750-M1-1: se il primo cervello della cascata non è configurato (es. VPS senza GEMINI_API_KEY), la riga «↪ risposta da … (riserva)» compare a ogni risposta. Contarlo come ripiego? sì/no.
3. Tetto delle 10 iterazioni per turno invece che per cervello (un turno ha fatto 40 chiamate)? sì/no.
4. Nome dei lead nel promemoria della memoria che arriva ai modelli gratuiti: bloccarlo? sì/no.

## Esito
- **Merge notturni (sì dell'operatore «mergia tutto quello che il bot ha approvato»)**: FATTO — #362, #361, #364 mergiate da M1; #363 e #365 mergiate da M2.
- **Analisi notturna (4 agenti: motore, firme/notte/Telegram, voce, memoria/web/conoscenza)**: FATTA — 19 bug riprodotti, report in `reports/test_mattina.md`.
- **Fix motore B1–B3, memoria/conoscenza B1–B4, notte/bot B2–B4**: FATTA — commit d9346212, review #744-M1 APPROVATO CON RISERVE.
- **Firme B1 (`.gas_sottofondo` scrivibile senza firma)**: FATTA da M3 nella #364 (mergiata).
- **Bug della voce B1–B5 + miglioramenti**: FATTA da M2 nella PR #367 (aperta, la mergia M2 dopo la #366).
- **Kernel B4 (§8, ripiego dichiarato)**: FATTA — f4979c13, review #750-M1 APPROVATO CON RISERVE; riga «↪ risposta da …» in CLI e Telegram (non a voce).
- **Kernel B5–B6**: DEFERITA — BASSE, annotati in stato_progetto.
- **Merge di origin/main (#363, #365)**: FATTA — 769df833, review #751-M1 APPROVATO.
- **Bot #366 V-1 (handoff), V-2 (id duplicati), V-3 (exit code ingest)**: FATTA — questo handoff, rinomina #744-M1/#748-M1, commit 69c26619 (review #749-M1).
- **`reports/test_mattina.md`**: FATTO — prove manuali sul Mac per area.

## Test
Kernel 1119 PASS / 0 FAIL; notte+ingest_fonti+sottofondo+gate+telegram_voce+manutenzione 1285 passed; con voice_server 1419 passed (prima del merge di #363/#365).

## Anomalie
Ogni merge su main fa andare in conflitto le altre PR aperte (report condivisi): da qui la scelta di far mergiare M2 da sola.
