# Ultimo Report — chore/hook-fine-task-obbligatorio

**Data:** 2026-10-02
**Branch:** chore/hook-fine-task-obbligatorio
**Task:** hook /fine-task obbligatorio — script deterministico + contatore per sessione

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #110 (https://github.com/Gasss23/Gas/pull/110)

---

## §1 — Esito fette

- **Fetta 0 — SONDA**: `FATTA` — nessuna modifica al codice; confermato che hook/script esistenti non coprono i 5 requisiti della spec.

- **Fetta 1 — scripts/fine_task_finale.sh (nuovo)**: `FATTA` — script deterministico che esegue in sequenza gate A (check_handoff), gate B (check_verdetto), gate IP (per-IP, no falso negativo), push (mai main), guardia HEAD==@{u}, stampa URL_HANDOFF (solo se handoff.md rigenerato nella sessione).

- **Fetta 2 — promemoria_end.sh contatore per sessione**: `FATTA` — contatore ora legge session_id da payload stdin; formato file `session_id:count`; reset implicito su cambio sessione; path counter worktree-safe via `git rev-parse --git-dir`; WARN al 4° tentativo su stderr e gas_debug.log.

- **Fetta 3 — Test reali**: `FATTA` — 49 test totali (erano 47). Aggiunti: T-prom-counter-session (B1), T-finale-3 aggiornato (non disponibile su diff vuoto, B2), T-finale-3b (URL reale su handoff rigenerato), T-finale-4 assert preciso (R3), _read_prom_counter helper per formato session_id:count.

- **Fetta 4 — DOC**: `FATTA` — fine-task.md §4bis chiama `bash scripts/fine_task_finale.sh`; §5 rimuove cat integrale handoff e documenta URL_HANDOFF. CLAUDE.md regola reporting aggiornata.

- **Fetta 5 — Revisore Opus**: `FATTA`
  - Review #122: BOCCIATO (B1 contatore non per-sessione, B2 URL sempre stampato)
  - Fix B1/B2/R1-R5 applicati
  - Review #123: APPROVATO

---

## §2 — Note anomalie

- Review #122 BOCCIATO ha richiesto un secondo ciclo di fix (sessione non si è chiusa prima del completamento grazie all'hook promemoria_end.sh stesso che ha bloccato correttamente).
- CI al momento della scrittura ancora in coda (run 37045838781 su commit 9863352) — §6 handoff aggiornato dopo completamento.
