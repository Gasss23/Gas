# Diff sessione 2026-09-28 — Fetta 3a lezioni quarantena

## File toccati

| File | Variazione |
|------|-----------|
| `modules/memory/store.py` | +118 righe: tabella `lezioni` (schema DDL), costanti STATI/TRANSIZIONI/LEZIONE_TESTO_MAX, metodi aggiungi/approva/rifiuta/ritira/lista/get_lezioni_approvate |
| `gas.py` | +218 righe: costanti _LEZIONI_DATI_*, regola system prompt, _lezioni_pin(), run_turn (lezioni_pin), lezioni_cmd(), main() dispatch |
| `tests/test_unit_kernel.py` | +130 righe: T68a-T68n (15 test lezioni) |
| `reports/ultimo_report.md` | Riscritto: report Fetta 3a |
| `reports/stato_progetto.md` | Aggiornato: riga motore Fetta 3a + contatore review 106 + suite 361 |
| `reports/handoff.md` | Aggiornato: dossier sessione |

## Cosa è cambiato e perché

- **Tabella `lezioni`**: requisito Fetta 3a — catalogo persistente di lezioni umane che Gas può portarsi nel prompt. Additiva (CREATE IF NOT EXISTS), nessuna modifica a diario/contatti. CHECK a livello DB per sicurezza.
- **CLI `gas lezioni`**: unico punto di ingresso UMANO per aggiungere/approvare/rifiutare/ritirare lezioni. Nessun tool esposto al modello (T68n).
- **`_lezioni_pin()`**: iniezione nel system prompt delle sole lezioni approvate (max 10, escape, fail-safe §9), separata da `_memoria_pin` (`<memoria_dati>`).
- **Test T68a-T68n**: copertura completa dei casi d'uso + edge case (lezione malevola, transizioni vietate, testi invalidi, no-tool).

## Numeri chiave

- Commit: `0c816a9`
- PR: #101
- Suite: 361 PASS, 5 FAIL (F-mac-1 invariati)
- Nuovi test: 15/15 PASS
- Revisore #106: APPROVATO CON RISERVE
