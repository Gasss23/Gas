# Diff della sessione — 2026-11-19/20 — CRM fetta 6 (copia cifrata su iCloud)

Si riscrive a ogni sessione; la storia completa sta in git. La PR #381 (fette 1-5) è mergiata. Questa fotografia copre il ramo ripartito da main c4c8c31f.

- `modules/crm/copia_cifrata.py` (nuovo): copia giornaliera cifrata fuori dal Mac (iCloud Drive), mai in chiaro; `ripristina` senza sovrascrivere, rifiuta i file di lavoro rimasti, integrità ricontrollata.
- `modules/crm/server.py`: il guardiano lancia la copia cifrata in un thread a parte dopo la copia locale giornaliera.
- `modules/crm/__main__.py`: `backup` fa anche la copia cifrata; nuovo comando `ripristina`; avviso ATTIVA/SPENTA all'avvio; `SCAN_MINUTI_DEFAULT = 720`.
- `modules/crm/scrittore.py`: parole vietate con radici più larghe; spazi doppi tolti.
- `modules/crm/__init__.py`: docstring corretta (file del CRM separato).
- `requirements.txt`: `cryptography>=42.0`.
- `tests/conftest.py`: le suite pytest non scrivono mai nell'iCloud vero.
- `tests/test_unit_crm.py`: test della copia cifrata, del ripristino dopo un crash, del giro 720 e delle parole vietate.
- `reports/crm/guida.md`, `reports/crm/decisioni.md` (punti 12-14), report di fine task, `.claude/agents/memoria_revisore.md`.
