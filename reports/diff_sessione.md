# DIFF DI SESSIONE — 23 novembre 2026, R7 fetta 3 (stato dei lavori ricorrenti)

Questo file si riscrive a ogni sessione; la storia completa sta in git.

- `modules/notte/notte.py`: registro dello stato dei lavori (lettura difensiva, scrittura atomica, pausa di 7 giorni dopo 3 ko di fila, sezione nel riepilogo, `_giorno` senza eccezioni; guasti esterni non contati, sezione con tutti i compiti, avviso col conto reale; «Sempre Opus» come guasto esterno, tetto di 14 guasti esterni di fila, pausa in corso conservata; motivi del lavoro dentro «Pipeline esausta» contati come ko veri).
- `tests/test_unit_notte.py`: 9 test (stati, pausa e rilancio a mano, ok che azzera, prompt cambiato, pausa scaduta o assurda, registro rovinato, potatura, data enorme, catalogo in parte rotto) + 6 delle riserve (4 guasti esterni, saltati per crash, conto dopo la pausa).
- Merge di origin/main (PR #397, chat CRM) in 73277ba0: dopo il merge il punto di partenza del ramo è il main nuovo, quindi i file della #397 non compaiono in questo diff.
- `reports/setup_notte.md`: paragrafo sullo stato dei lavori per l'operatore.
- `.claude/agents/memoria_revisore.md`: righe delle review #839-F3, #842, #843, #844-MERGE, #845-R7…#848-R7, #851-MERGE-R7; più quelle della chat CRM arrivate col merge di main.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
