# Diff della sessione — 2026-11-09 — chat Mani, voce via Telegram fetta 4 (voce in un thread)

File toccati (base main 567beb7, cioè dopo i merge delle PR #357 e #358, unite in questa PR):
- `modules/telegram/bot.py`: `_consegna_voce` (coda di un solo thread per sintesi e invio del vocale) e `_chiudi_voce` su Ctrl-C, anche nella pausa dopo un errore. Docstring della chiusura corretta.
- `tests/test_unit_kernel.py`: guardia T78p allargata solo per la coda della voce e trasformata in allow-list (bot e verifica esterna #359, review #725–#733).
- `tests/test_unit_telegram_voce.py`: test di ordine e un-vocale-alla-volta, coda non disponibile, chiusura, Ctrl-C nella pausa (da 66 a 71).
- `clients/voice/ascolto.py`: riga di log coi secondi fino alla prima frase di Gas.
- `tests/test_unit_voce_ascolto.py`: test di quella riga.
- `.claude/agents/memoria_revisore.md`: righe #722, #725, #727–#733, #735 e le lezioni; righe di M2 arrivate col merge di main.
- `reports/*`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
