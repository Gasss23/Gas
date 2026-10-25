# DIFF SESSIONE — 2026-10-25 (chat Mani, fetta 16, PR #268)

- `modules/web/leggi.py`: `con_noscript` calcolato una volta in `_componi` e passato al costruttore di `_Estrattore` (default `True`, verso sicuro), tolto l'override di `feed`, docstring di `_Contesto` aggiornata — R-ve261-6, R-511-1.
- `tests/test_unit_web_leggi.py`: pagine con `<NOSCRIPT>`/`<NoScript>` (R-ve261-3), `</template>` in più a pila vuota (R-ve261-6), test del default del flag (R-512-1), flag esplicito nel test casuale del ripiego.
- `.claude/agents/memoria_revisore.md`: righe delle review #511, #512, #513 (commit del revisore).
- `reports/stato_progetto.md`: intestazione e blocco «Mani — fetta 16».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
