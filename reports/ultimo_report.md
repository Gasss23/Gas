# ULTIMO REPORT — 2026-10-05 — Gate IP: IP adiacente a un punto (R-155-1)

Branch `fix/gate-ip-ip-adiacente-punto` · commit `afc36ca` (scripts + tests) + `d4806d1` (memoria revisore) · review #156 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #128 (https://github.com/Gasss23/Gas/pull/128), variante A (`gasmerge 128; exit`), dopo la verifica esterna.
2. **R-155-3** (operativa, aperta): Codex e Claude Code nella stessa cartella `~/Gas`. Questa fetta e la #127 sono state fatte nella worktree `.claude/worktrees/gate-ip-ottetti`, dove l'hook `review_gate.sh` NON protegge (legge lo stage di `~/Gas`). Decidere: Codex in una cartella sua, oppure hook consapevole delle worktree.
3. Residui V-2 / V-3 della verifica esterna #127 (secondo fetch senza `--prune`; `HEAD_SHA` catturato dopo il gate IP): fissarli prima della variante B del merge?
4. V-3 / V-5 della verifica #121: ancora aperte.
5. Poi la fetta PRIORITARIA: V-B "vera" (bot di revisione su GitHub).

## Esito per step

- **Merge PR #127**: FATTO (`gasmerge 127`, confermato dall'operatore; main `7ded2a4`).
- **R-155-1** (MEDIA-BASSA, allargata dalla verifica #127 V-1: fine frase, `<IP>.dominio`, `dominio.<IP>`): FATTA. Nuove ancore nelle 6 regex del gate IP; test speculari `test_ip_adiacente_a_un_punto_blocca` / `test_cinque_componenti_non_e_un_ip` (gasmerge) e 4p / 4q (finale).
- **Redazione in `memoria_revisore.md`** (riga #155: IP a fine frase non marcato, ora visibile al gate): FATTA, committata col commit di memoria della review #156.
- **Residui V-2 / V-3 verifica #127**: DEFERITI — annotati in stato_progetto, decisione operatore (punto 3).
- **R-153-2, latin1 su glibc, R-150-1**: DEFERITE (fuori scope).

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 320 → **338 passed**.
- Mutation in sequenza (harness `mut_sweep.py` esteso con ancore nuove, ritorno alle vecchie, punto senza vincolo di cifra): **120 KILLED, 8 SURVIVED**. Sopravvissute: solo allargamenti della terza regex (grep allowlist) nei due script, fail-closed.
- Scansione dell'albero con la regex nuova + filtro loopback: unica occorrenza era la riga #155 di memoria_revisore, redatta.

## Riserve aperte

- **R-156-1 (bassa)**: regex nuove provate solo con BSD grep/git su macOS; la CI ubuntu esegue i test nuovi.
- Da ora un IP non marcato seguito da un punto blocca anche i branch di altre sessioni (fail-closed).
