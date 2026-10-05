# ULTIMO REPORT — 2026-10-05 — gasmerge: mktemp casuale (R-153-2) + test IP a inizio riga (verifica #128 V-1)

Branch `fix/gate-ip-inizio-riga-mktemp` · commit `33f7f47` (script + test) + `a0afeb4` (memoria revisore) · review #157 **APPROVATO**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #129 (https://github.com/Gasss23/Gas/pull/129), variante A (`gasmerge 129; exit`), dopo la verifica esterna.
2. **R-155-3** (operativa, aperta): Codex e Claude Code nella stessa cartella `~/Gas`; nella worktree `.claude/worktrees/gate-ip-ottetti` l'hook `review_gate.sh` non protegge. Codex in una cartella sua, o hook consapevole delle worktree?
3. Residui V-2 / V-3 della verifica esterna #127 (secondo fetch senza `--prune`; `HEAD_SHA` catturato dopo il gate IP): fissarli prima della variante B del merge?
4. V-3 / V-5 della verifica #121: ancora aperte.
5. Poi la fetta PRIORITARIA: V-B "vera" (bot di revisione su GitHub).

## Esito per step

- **Merge PR #128**: FATTO (`gasmerge 128`, confermato dall'operatore; main `08a9d51`). Il primo lancio era uscito subito per R-153-2 (residuo `/tmp/gaspr.XXXXXX.json` lasciato da un processo ucciso): file vuoto rimosso, rilancio riuscito.
- **R-153-2** (mktemp BSD): FATTA. `mktemp "${TMPDIR:-/tmp}/gaspr.XXXXXX"` + guardia; `TestFileTemporaneo` (2 test, falliscono sullo script di main).
- **V-1 verifica #128** (`^` della testa non coperto nel finale): FATTA. Casi IP a inizio riga, inizio riga + `.dominio`, file senza newline in `test_finale_4p_*`; inizio riga + `.dominio` anche in gasmerge.
- **V-2 verifica #128** (formula "solo allargamenti fail-closed"): FATTA, corretta in stato_progetto in "nei mutanti testati".
- **R-156-1**: CHIUSA dalla CI ubuntu della PR #128.
- **Sessione "Verificatore"** (ferma dal 3 ottobre, sostituita dall'agente nuovo a ogni verifica): ARCHIVIATA dall'operatore.
- **Residui V-2 / V-3 verifica #127, latin1 su glibc, R-150-1**: DEFERITI.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 338 → **344 passed**.
- Mutation in sequenza (harness esteso con `noCaret`, `noCaret2`, `noEOL`, `noDotEOL`, `mktemp_suffisso`, `mktemp_noguard`): **142 KILLED, 12 SURVIVED**, tutte equivalenti (8 allargamenti della grep allowlist; 4 `^` irraggiungibili della grep -qE).

## Anomalie

- Il primo sweep è stato fermato dal limite di tempo del runner e ha lasciato `fine_task_finale.sh` mutato: ripristinato da HEAD (questa fetta non lo modifica), sweep del finale rilanciato a parte.
- Consumo: 28% del limite settimanale Pro a metà settimana; cause e rimedi spiegati all'operatore (modello Opus, contesto lungo, subagenti, notifiche del monitor).
