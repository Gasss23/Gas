# Diff della sessione — 2026-11-09 — chat Mani, voce via Telegram fetta 4 (voce in un thread)

File toccati (base main 524ae96, dopo il merge della PR #357):
- `modules/telegram/bot.py`: `_consegna_voce` (coda di un solo thread per sintesi e invio del vocale), `_chiudi_voce` su Ctrl-C, anche nella pausa dopo un errore.
- `tests/test_unit_kernel.py`: guardia T78p allargata solo per la coda della voce e irrobustita (submit/map, funzioni raggiunte dal thread).
- `tests/test_unit_telegram_voce.py`: test di ordine e un-vocale-alla-volta, coda non disponibile, chiusura (da 66 a 70).
- `clients/voice/ascolto.py`: riga di log coi secondi fino alla prima frase di Gas.
- `tests/test_unit_voce_ascolto.py`: test di quella riga.
- `.claude/agents/memoria_revisore.md`: righe #722, #725, #727, #728 e due lezioni.
- `reports/*`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
