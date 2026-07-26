# Diff sessione — fix/gasmerge-failopen (2026-07-26)

> Riscritto a ogni sessione. La storia completa sta in git.

## File toccati (BASE c7f6fac..HEAD)

| File | Cosa è cambiato |
|---|---|
| `scripts/gasmerge.sh` | FETTA 1: invariante IP riscritta con filtro 2-passi fail-closed + marker `gasmerge-ip-ok`; FETTA 2: HEAD_SHA catturato pre-prompt, ri-verifica TOCTOU post-read aggiunta |
| `tests/test_unit_gasmerge.py` | FETTE 3: helper `_run_with_stdin`; classe `TestIPAllowlist` (3 test); classe `TestTOCTOU` (1 test); marker `# gasmerge-ip-ok` su righe sorgente con IP |
| `.claude/agents/memoria_revisore.md` | FETTA 0: UNION+RENUMBER conflitto merge (#62/#63 branch intatti, #62 main → #64); review #65 aggiunta dal revisore (APPROVATO CON RISERVE) |
| `reports/stato_progetto.md` | FETTA 4: contatore review 61→65; R-gasmerge-failopen aggiornato con FETTE 1-3 + riserve; collisione #62 documentata; istituzioni di processo C aggiornata |
| `reports/ultimo_report.md` | Fine-task: fonte di verità del task con verdetto verbatim e proof pytest |
| `reports/handoff.md` | Fine-task: dossier autonomo per revisione PR #46 |
| `reports/diff_sessione.md` | Fine-task: questo file |

## Nota sessione

Sessione 2026-07-26 ha gestito due sotto-sessioni a causa di interruzione contesto.
Prima sotto-sessione: interrotta al tentativo di merge conflict (STOP corretto, senza risolvere).
Seconda sotto-sessione: ricetta ESATTA da utente → FETTE 0-4 completate; /fine-task
interrotto prima del commit per esaurimento contesto. Terza invocazione (questo file):
/fine-task completato, commit e push definitivi.
