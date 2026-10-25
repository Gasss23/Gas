# DIFF SESSIONE — 2026-10-25 (chat Mani, fetta 16, PR #268, due giri)

- `modules/web/leggi.py`: `con_noscript` calcolato una volta in `_componi` e passato al costruttore di `_Estrattore`, e da lì a `_Contesto` (default `True` in tutti e due, verso sicuro); il ripiego lo passa al costruttore; tolto l'override di `feed`; docstring di `_Contesto` aggiornata — R-ve261-6, R-511-1, V-1 bot #268.
- `tests/test_unit_web_leggi.py`: pagine con `<NOSCRIPT>`/`<NoScript>` (R-ve261-3), `<noscript class=x>` e noscript dopo 3000 caratteri (V-3 ve #268), `</template>` in più a pila vuota (R-ve261-6), test del default di `_Estrattore` e `_Contesto` (R-512-1, V-1 bot #268), flag esplicito nel test casuale del ripiego.
- `.claude/agents/memoria_revisore.md`: righe delle review #511-#514 (commit del revisore).
- `reports/stato_progetto.md`: intestazione, blocco vecchio annotato, blocco «Mani — fetta 16» col secondo giro e la descrizione corretta del frameset.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
