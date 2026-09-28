# Diff sessione — 2026-09-27

**Branch:** fix/r2-sanitize-hardening  
**Task:** R2 Sanitize Hardening — fetta 2b chiusura riserve fetta A

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `gas.py` | `_sanitize_memory_text`: escape universale `<`→`&lt;` e `>`→`&gt;` (non solo tag esatti) + C1 (0x80-0x9F) nella regex — chiude bypass con varianti uppercase/spazi |
| `tests/test_unit_kernel.py` | +7 test T65g: varianti bypass (`</MEMORIA_DATI>`, spazi, uppercase) + C1 + invarianza testo normale — coprono la nuova logica di sanitizzazione |
| `.claude/agents/memoria_revisore.md` | Riga review #105 APPROVATO aggiunta dal subagent revisore |
| `reports/ultimo_report.md` | Report task sessione corrente (punti 1/2/3, verdetto #105 integrale) |
| `reports/stato_progetto.md` | Aggiornato con esito fix/r2-sanitize-hardening + review #105 APPROVATO |
| `reports/handoff.md` | Dossier di fine sessione (questo file) |
| `reports/diff_sessione.md` | Questo file — riepilogo sessione corrente |
