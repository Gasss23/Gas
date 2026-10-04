# ULTIMO REPORT — 2026-10-04 — Promemoria di gasmerge dal perimetro, ref completi, .gitignore audio

Branch `fix/gasmerge-perimetro-gitignore` · PR #122 · commit `03e01f8` · review #145 + #146 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #122 (variante A: `gasmerge 122`), dopo la verifica esterna.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? Oggi la difesa sono i ref completi negli script.
3. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review?
4. Poi la prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub). Ti serviranno i passi per creare la chiave API.

## Esito per step

- **V-1 verifica #121** (gasmerge con regex propria: gas_identity.md, requirements*, tools/, clients/, .github/workflows/ risultavano "doc-only"): FATTA. Il promemoria legge `.claude/perimetro_review.txt` (main ∪ branch).
- **R-144-1** (ref abbreviato in gasmerge.sh e promemoria_end.sh; messaggio di fine-task.md): FATTA.
- **V-2 verifica #121** (R-143-4 parziale): FATTA. `.gitignore`: `*.wav`, `*.mp3`, `clients/**/*_output.{wav,mp3,txt,json}`.
- **R-145-1** (rename e nomi non-ASCII sparivano dal promemoria): FATTA nella stessa fetta.
- **R-145-2** (pattern `*_output.*` nascondeva anche i sorgenti): FATTA nella stessa fetta.
- **Correzioni stato_progetto**: FATTA. R-143-4 → PARZIALE (completata qui); R-143-1 → chiusa solo dopo il merge di #121.
- **Tracciamento V-3 e V-5 (verifica #121)**: FATTA (stato_progetto, aperte: decisione operatore).
- **V-B vera**: DEFERITA — è la prossima fetta.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 275 → **281 passed**.
- Controprova: con il gasmerge.sh di main, `-k "Perimetro or DiffGuard"` dà 5 failed, 2 passed (passano doc-only e DiffGuard, per costruzione).
- Kernel non rilanciato: la fetta non tocca gas.py, brains/ o modules/.

## Riserve aperte

- Riserve minori #146: le righe `clients/**/*_output.{wav,mp3}` sono ridondanti con `*.wav`/`*.mp3`; eventuali fixture audio in tests/ vanno aggiunte con `git add -f`.
- Test non-ASCII verificato solo su macOS; lo confermerà la run CI su Linux.

## Anomalie

- La PR è stata creata con `--title/--body` invece di `--fill` (sempre non interattiva): il numero viene comunque da `gh`.
- Nel primo tentativo di commit, `segna_review_ok.sh` e `git commit` erano nello stesso comando: il gate (PreToolUse) l'ha bloccato, com'è giusto. Rifatto in due comandi.
