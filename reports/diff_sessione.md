# DIFF SESSIONE — 2026-10-03 — C4b-2 (feat/cancello-c4b2)

| File | Cosa è cambiato e perché |
|---|---|
| `gas.py` | `applica_firma`: è il turno di sblocco che esegue gli args salvati dopo la firma, al massimo una volta e in modo fail-closed. Il read-back ora passa l'ID per i bottoni. |
| `modules/memory/store.py` | Tabella `approval_esecuzioni` (reclamo + esito, con trigger) e i metodi `reclama_esecuzione`, `registra_esito_esecuzione`, `get_esecuzione`. |
| `modules/telegram/bot.py` | Bottoni di firma, `gestisci_callback`, ripresa delle approvazioni orfane, messaggio di esito, `allowed_updates` con `callback_query`. |
| `tests/test_unit_kernel.py` | T75c adeguato al payload con `reply_markup`; nuovi T77a-t. |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #131 e #132. |
| `reports/stato_progetto.md` | C4b-1 verificato dal vivo; voce C4b-2; F-c4a-eco chiusa; riserve R-c4b2-*. |
| `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` | Report di fine task. |

La storia completa sta in git.
