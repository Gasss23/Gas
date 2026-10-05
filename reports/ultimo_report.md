# ULTIMO REPORT — 2026-10-05 — Gate IP: ottetti a 2-3 cifre, tree remoto, secondo fetch (verifica esterna #126)

Branch `test/gate-ip-ottetti-ref-tree` · commit `4babba9` (solo test) + `dd15215` (memoria revisore) · review #155 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #127 (https://github.com/Gasss23/Gas/pull/127), variante A (`gasmerge 127; exit`), dopo la verifica esterna.
2. **R-155-1** (MEDIA-BASSA, preesistente): un IP seguito dal punto di fine frase ("connect to 8.8.8.8.") passa il gate IP in entrambi gli script. Micro-fetta di fix prima della V-B? (consigliato: sì)  # gasmerge-ip-ok
3. **R-155-3** (nuova, operativa): Codex e Claude Code hanno lavorato nella stessa cartella `~/Gas` (Codex ha cambiato branch e messo in stage i suoi report). Questa fetta è stata chiusa in una worktree separata, dove l'hook `review_gate.sh` NON protegge (guarda lo stage di `~/Gas`). Decidere: Codex in una cartella sua, oppure rendere l'hook consapevole delle worktree.
4. V-3 / V-5 della verifica #121 (tag `origin/*` nel ruleset; `.gitignore`, `knowledge/`, `CLAUDE.md` nel perimetro): ancora aperte.
5. Poi la prossima fetta PRIORITARIA: V-B "vera" (bot di revisione su GitHub).

## Esito per step

- **V-1 verifica #126** (MEDIA: `{1,3}`→`{1,2}` su 3° e 4° ottetto delle 3 regex di `fine_task_finale.sh` sopravviveva): FATTA. Test `test_finale_4o_ottetti_a_piu_cifre_bloccano` (4 casi), uccide tutte e 6 le mutation.
- **V-2 verifica #126** (gasmerge: tree da `refs/heads` invece di `refs/remotes/origin`): FATTA. Test `test_branch_locale_pulito_non_maschera_origin_con_ip`.
- **V-3 verifica #126** (gasmerge: secondo `git fetch --prune` dopo l'attesa CI): FATTA. Stub gh con `on_watch` e test `test_push_durante_attesa_ci_visto_dal_gate`.
- **V-4 verifica #126** (ancore delle regex): CHIUSA COME FAIL-CLOSED, senza test. Le 12 rimozioni di ancora allargano il match e non possono far passare un IP; un test che le uccidesse congelerebbe la lacuna R-155-1 (review #155).
- **Harness `mut_sweep.py`** esteso con matrice ottetti `{1,2}`, ref del tree locale, secondo fetch, ancore: FATTO.
- **V-5 / V-6 verifica #126** (cosmetiche sul vecchio handoff §6 e §4): SUPERATE, l'handoff è riscritto.
- **R-153-2** (mktemp BSD), **latin1 su glibc**, **R-150-1**: DEFERITE (fuori scope).

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 314 → **320 passed** (nella worktree).
- Mutation (in sequenza, scripts/ ripristinati e puliti a fine run): **92 KILLED, 12 SURVIVED**. Le 12 sopravvissute sono tutte rimozioni di ancora (6 per script), fail-closed.
- Nessuno script modificato: diff solo in tests/.

## Anomalie

- Una sessione Codex ("Preview servizi TradeGasFX") lavorava nella stessa cartella `~/Gas`: ha riscritto i 4 report, li ha messi in stage e ha spostato il branch su `codex/tradegasfx-redesign` mentre questa fetta era in corso. Su indicazione dell'operatore i suoi file non sono stati toccati; questa fetta è stata spostata nella worktree `.claude/worktrees/gate-ip-ottetti` (copia dei report Codex salvata nella scratchpad).
- Nella worktree l'hook `review_gate.sh` non ha bloccato un `git commit --dry-run` senza marcatore: legge lo stage di `CLAUDE_PROJECT_DIR` (`~/Gas`). La review #155 c'è comunque, sullo stesso diff; il marcatore è stato scritto nella worktree. → R-155-3.
