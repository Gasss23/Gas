# Report diagnosi — snapshot refs vs oggetti loose (Codespace)

**Data:** 2026-06-15 · **Tipo:** SOLA DIAGNOSI (nessuna modifica a gas.py/brains/modules/tests, nessun gc/prune/comando distruttivo).

## (a) VERDETTO: **(A)** — il path snapshot NON è esercitato in questo Codespace, lo 0 ref è atteso. NESSUN BUG.

Prove:
- `git for-each-ref refs/gas/snapshots/` → **0 ref**; `.git/refs/gas/` esisteva ma **vuota** (mancava persino `snapshots/`); niente in `.git/packed-refs`.
- `git count-objects -v` → **4495 loose**, solo 3 in-pack (size 27556 KB loose).
- `git fsck --unreachable --no-reflogs` → 4133 blob, **4 commit**, 4 tree unreachable.
- Dei 4 commit unreachable, **3 sono di `git stash`** (autore Gasss23: "index on main…", "untracked files on main…", "WIP A+B … da ripristinare") e **solo 1 è un vero snapshot GAS** (autore `gas-snapshot`: "gas snapshot [write_file] prova.txt", 2026-06-11 16:29). Quindi il path snapshot è girato qui **una sola volta, in un test** (file `prova.txt`).
- In sviluppo si pilota Claude Code, NON il runtime agentico di GAS: `_snapshot()` è chiamato solo da `run_command`/`write_file` del kernel agentico (gas.py:639, 672), che qui non viene esercitato → 0 ref è il valore atteso.
- Nessun hook rimuove i ref: grep su `.claude/hooks/` (`review_gate.sh`, `scrivi_rep.sh`, `session_end.sh`) per `refs/gas`, `update-ref -d`, `gc`, `prune`, `for-each-ref` → **nessun riscontro**. Esclude cleanup/retention fuori posto.

Escluse (B) e (C):
- **(B) ref non persiste / rimosso** → ESCLUSA dal test dal vivo (§b).
- **(C) retention svuota tutto** → ESCLUSA: `_snapshot_retention` (gas.py:212-230) tiene l'UNIONE di (ultimi `SNAPSHOT_KEEP=100`) e (più giovani di `SNAPSHOT_KEEP_DAYS=7`). Con 0/1 ref non droppa nulla; `drop` è non-vuoto solo con >100 ref E più vecchi di 7 giorni — non può svuotare i recenti. Inoltre l'unico snapshot reale (4 giorni fa) sarebbe stato TENUTO, non rimosso.

## (b) Il path scrive ref PERSISTENTI? **SÌ — provato dal vivo.**

`_snapshot` (gas.py:463-473): `write-tree` → `commit-tree` → **`update-ref refs/gas/snapshots/<ts>-<sha8>`**. Il ref è su disco; l'indice temporaneo (`GIT_INDEX_FILE`) serve solo a non sporcare la staging area dell'utente, NON è dove finisce lo snapshot.

Test eseguito: istanziato `GasKernel()` e chiamato `k._snapshot('diagnosi','diagnosi')`.
- PRIMA: `for-each-ref refs/gas/snapshots/` = 0.
- Ritorno: sha `ad85632cfc813c7311921cd09d96b514cdc5ab21`.
- DOPO: ref **comparso e persistito** → `.git/refs/gas/snapshots/20260615-175559.305167693-ad85632c` (creata anche la dir `snapshots/`).
- Ref di test poi rimosso con `git update-ref -d` (non distruttivo; l'oggetto resta recuperabile). Baseline ripristinata a 0 ref.

→ Il meccanismo è CORRETTO: quando il path parte, il ref nasce e resta su filesystem.

## (c) I ~4427/4495 loose: snapshot recuperabili o spazzatura? **Quasi tutta spazzatura git normale.**

- Tra TUTTI gli oggetti unreachable, i veri snapshot GAS sono **2 commit usa-e-getta**: `prova.txt` (2026-06-11) e il `diagnosi` appena creato dal test — entrambi senza valore.
- Il resto è detrito git ordinario: 3 commit di `git stash` (+1 stash attivo: "snapshot-autonomo … da riprendere in TASK C"), 4133 blob e i tree associati, frutto di churn di sviluppo (add superati, stash, `git add -A` dello snapshot orfano).
- NON è una riserva di snapshot utente recuperabili: è materiale recuperabile solo finché non gira `git gc`, ma di valore trascurabile.

## (d) Raccomandazione su `git gc`: **a basso rischio QUI, ma è decisione umana (irreversibile).**

- `git gc` è IRREVERSIBILE (CLAUDE.md §10; gas.py:910-916 lo tiene fuori dal doctor apposta).
- In questo Codespace è sicuro nella pratica perché: (1) ci sono **0 ref snapshot live** da proteggere — `gc` non tocca mai oggetti raggiungibili da un ref; (2) gli unici snapshot orfani sono test (`prova.txt`, `diagnosi`); (3) il grosso è detrito di stash/churn. Recupererebbe spazio senza perdere nulla di valore.
- Cautela: eseguirlo SOLO dopo aver verificato che nessuno snapshot GAS orfano serva (qui nessuno). Se in futuro esistono ref snapshot live, `gc` li preserva comunque. Non eseguito in questo task (sola diagnosi): la chiamata resta all'utente.

## (e) Nota pre-deploy VPS

Essendo (A), questo NON è un bug ma un **check di pre-deploy VPS**: in dev il runtime agentico non gira, quindi 0 ref è normale. Sul VPS h24 il kernel eseguirà `run_command`/`write_file` e gli snapshot nasceranno davvero; lì la sez.7 del doctor (0 ref + molti loose) diventa un segnale significativo da rivalutare. Da tenere come voce di checklist pre-deploy, non come difetto attuale.
