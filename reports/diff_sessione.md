# Diff della sessione — 2026-11-11 notte — blocco esteso dei nomi (M1)

Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py`: finestra con dati di lead → solo il forte (anche a metà turno), recap/lezioni filtrati per i non forti, riflessione con dati di lead solo al forte, confronto dei nomi con NFKD, lapidi, cifre dei telefoni, parole corte a parola intera, tipo della riga di diario.
- `modules/memory/store.py`: `leggi_contatti(includi_lapidi=...)`.
- `tests/test_unit_kernel.py`: T115a-e, round-trip, `forte_finto` negli helper per i round-trip con ricorda/salva_contatto.
- `reports/stato_progetto.md`, `.claude/agents/memoria_revisore.md`: R-753-M1-A chiusa, riserve R-766-1..4, riga #766-M1coord.
- `reports/handoff.md`, `reports/ultimo_report.md`, `reports/diff_sessione.md`: report di fine sessione.

## Merge di main (2026-11-11 sera)
Commit 366cfcc7: unione di origin/main 9844b1f nella #375; conflitti solo nei report (stato_progetto: aggiunta riga «Audit 11 nov»; memoria_revisore: unione). Review #788-M1coord APPROVATO.

Commit 6a7ca7eb: gas.py `_contiene_identificativo`/`_identificativi_contatti` (parola intera; nome attaccato; «contenuto in» dentro email/domini/file), test T115a3b/c/d, stato_progetto. Motivo: bot #375 V-1 MEDIA (falsi positivi «Conte»→«contesto»).
