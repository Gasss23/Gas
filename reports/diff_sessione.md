# Diff della sessione — 2026-11-20 — CRM fetta 8 (note basse sulle PR #387 e #388)

Si riscrive a ogni sessione; la storia completa sta in git. Le PR #381, #386 e #387 sono mergiate; questa fotografia copre il ramo ripartito da main d03e5bf2.

- `modules/crm/copia_cifrata.py`:
  - `_pulisci_ripristini_interrotti` e `_processo_vivo`: tolgono i temporanei in chiaro dei ripristini di processi morti;
  - `_genitore_assente`: rifiuta i percorsi non completi; motivo «creala, o collega il disco»;
  - `cartella()`: non solleva più con «~utente» inesistente o con iCloud bloccato;
  - `_consiglio_icloud`: permesso negato su iCloud Drive → motivo che dice cosa fare (avvio, prova, copia);
  - `ripristina`: la pulizia dei ripristini interrotti è la prima cosa, prima di ogni rifiuto.
- `modules/crm/server.py`: `_segna_copia(locale=…)`; motivi e avvisi giusti a copia esterna spenta o con copia sul Mac fallita.
- `tests/test_unit_crm.py`: due test nuovi e due asserzioni aggiornate.
- `reports/crm/guida.md` (percorso completo), `reports/stato_progetto.md`, report di fine task, `.claude/agents/memoria_revisore.md`.
