# DIFF DI SESSIONE — 2026-10-12 (fetta gate worktree)

> Fotografia dell'ULTIMA sessione. Si riscrive ogni volta; la storia completa sta in git.

Fetta di **sicurezza** su richiesta dell'operatore: chiudere `R-gate-worktree-1`, cioè il fatto che
il gate deterministico di review fosse **inerte** nelle sessioni che girano in un git worktree.

Sviluppata **nel checkout principale e non in un worktree**, di proposito: è l'unico posto dove il
gate è vivo, e un fix al gate va sviluppato sotto la protezione che sta ripristinando. In un worktree
i commit di questa fetta sarebbero passati senza che l'hook li guardasse — cioè esattamente il
difetto da chiudere.

| File | Cosa è cambiato e perché |
|---|---|
| `.claude/hooks/review_gate.sh` | Non fa più `cd "$CLAUDE_PROJECT_DIR"` incondizionato. Estrae `cwd` dal payload (stesso parser a cascata jq→python3→python→perl) e controlla **ogni checkout candidato** col **proprio** indice e il **proprio** marcatore: radice di `cwd`, bersagli assoluti e letterali dei costrutti che cambiano directory, e spazzata di tutti i worktree quando la directory reale non è deducibile. Sezione «Limiti dichiarati» riscritta: aggiunti i falsi positivi del matcher, l'assenza della directory del comando dal payload e i limiti residui R-299-2/R-299-3. |
| `tests/test_unit_hooks.py` | 31 test nuovi (`TestReviewGateWorktree`): la riproduzione del buco, il marcatore per-worktree, il marcatore del principale che non vale per il worktree, la spazzata senza `cwd`, `cd` assoluto/relativo/con variabile, `GIT_WORK_TREE=`, il doppio `-C`, il `cd` dentro una stringa, il principale sporco che non deve bloccare il worktree, il worktree prunable. |
| `reports/ultimo_report.md` | Report del task: difetto, fix, numeri reali, prove di mutazione, riserve chiuse, non verificato. |
| `reports/stato_progetto.md` | Voce della fetta, `R-gate-worktree-1` chiusa con evidenza, e la correzione di igiene sui nomi. |
| `reports/handoff.md` | Dossier di fine sessione. |
| `.claude/agents/memoria_revisore.md` | Righe dei giri di review, scritte dallo script del revisore. |

**Motore NON toccato**: nessuna riga di `gas.py`, `brains/`, `modules/`. La suite del kernel resta a
**821 PASS, 0 FAIL** per costruzione.

**Numeri reali**: `tests/test_unit_hooks.py` **107 → 138**; `pytest` **1031 → 1062 passed, 1 skipped**.
Contro l'hook di `main` **8 dei 15** test nuovi falliscono (la riproduzione esce `0` dove serve `2`);
contro la versione del primo giro falliscono i quattro aggiunti nel secondo.

**Avvertenza sulla numerazione, con la misura e non con una previsione**: questo ramo parte da `main`
(fino a #298) e usa #299–#303; la PR #195 non mergiata usa #299–#301; l'altra sessione ha gia'
rinumerato le proprie a #302–#307. `git merge-tree` (letto sull'**exit code**, non sulla prima riga
dell'output, che e' l'OID stampato anche in caso di fallimento) dice che ogni ramo e' **pulito**
contro `main` preso da solo, ma che a coppie conflittano: chi mergia **primo** passa liscio, gli
altri due vanno risolti a mano. Il conflitto e' sulla memoria del revisore — e, fra la #195 e il ramo
dell'altra sessione, anche sui quattro file di report. **Correzione a una previsione precedente**:
avevo scritto che il conflitto avrebbe toccato `tests/test_unit_kernel.py`; misurato, su quel file il
merge riesce da se'.

## Cinque giri, due BOCCIATI

Il diff finale e' il risultato di cinque giri di review: **#300** e **#301** sono stati **BOCCIATO**,
sempre sullo stesso punto (il matcher dei costrutti che cambiano directory) e sempre con la suite
**verde col buco dentro** — 122 su 122 il primo, 130 su 130 il secondo. Ha chiuso la questione un
argomento **strutturale** e non un elenco di forme coperte: dopo «coppia di apici ai bordi + rifiuto
dei residui» il bersaglio sopravvissuto e' una sola parola di shell senza espansioni, quindi coincide
per costruzione con quella che userebbe la shell.

Il diff include anche i **lucchetti** sui limiti accettati: restringere `-C` a `git -C` — l'
ottimizzazione ovvia — fa diventare rossi tre test, incluso quello del doppio `-C` che era il
fail-open del primo giro.
