# Report sessione 2026-06-11 (sera) — Snapshot preventivo dei file (roadmap ALTA, punto 1)

Gas ora fotografa l'intero repo PRIMA di ogni operazione che può alterare i
file. Se la foto non riesce, l'operazione non parte. Il ripristino resta in
mano all'umano. Suite finale: **34 PASS, 0 FAIL** (i 25 storici tutti verdi).

## Cosa fa, in parole semplici

Prima di ogni `write_file` (dopo i guardrail esistenti) e di ogni
`run_command`, il kernel scatta una "foto" dello stato del repo e la mette in
un cassetto di git che non tocca né i commit né l'area di staging
(`refs/gas/snapshots/`). Se Gas si autodistrugge un file — direttamente o via
shell — si torna indietro con due comandi git, documentati nel README.

## Come funziona davvero (fedele al diff)

- **`_snapshot(trigger, target)`** in `gas.py`: indice git temporaneo
  (`GIT_INDEX_FILE` in una tmpdir) → `git add -A` (include i file NON
  tracciati, che `git stash create` ignorerebbe) → `add -f .gas_history.json`
  (la memoria di Gas è gitignorata ma va protetta quanto il codice) →
  `write-tree` → `commit-tree` (parent = HEAD se esiste) → ref
  `refs/gas/snapshots/<timestamp-ns>-<sha8>`. Ritorna lo SHA, `None` se
  qualcosa fallisce.
- **Fail-closed**: `None` = tool result "Operazione negata: snapshot
  preventivo fallito… (fail-closed)", `logging.warning` nella scatola nera,
  loop agentico intatto. Verificato anche il caso subdolo della root annidata
  in un repo esterno (check `rev-parse --show-toplevel == root`, fix della
  riserva R1): senza, lo snapshot sarebbe "riuscito" fotografando il repo
  sbagliato.
- **Scatola nera**: successi via logger dedicato `gas.snapshot` a INFO (solo
  `gas_debug.log`, console pulita, librerie ancora filtrate a WARNING) +
  indice leggibile append-only `reports/snapshots.log`.
- **Retention**: ultimi **100** snapshot, i ref più vecchi vengono potati a
  ogni scatto (timestamp a nanosecondi ⇒ ordine lessicografico = cronologico).
- **Ripristino SOLO umano** (README, "Macchina del tempo"): nessun tool di
  restore esposto a Gas; `git restore --worktree --source <ref> -- <file|.>`,
  con caveat onesti (i file creati dopo lo snapshot non vengono cancellati
  dal ripristino intero; i gitignorati non sono nelle foto).
- **Limite dichiarato**: il finding 🟠 resta APERTO — la shell può ancora
  LEGGERE/esfiltrare fuori root; lo snapshot limita solo i danni delle
  scritture. Lo chiuderà il sandbox/dry-run.

## Test (tests/test_unit_kernel.py, zero token)

8 nuovi check T11a–T11g: snapshot creato prima della write; lo snapshot
contiene la versione PRE-modifica e `git restore` la riporta esatta;
fail-closed su write_file E run_command in root non-git; file non tracciato
incluso; run_command fa scattare lo snapshot; retention pota oltre il limite;
root annidata in repo esterno bloccata. `kernel_tmp` e la root di T10 ora
fanno `git init` (coerente col fail-closed). **Totale: 34 PASS, 0 FAIL.**

## Review #3 (revisore, prima invocazione diretta come tipo registrato)

**Verdetto: APPROVATO CON RISERVE.** Validati esplicitamente: il meccanismo
GIT_INDEX_FILE+commit-tree+ref (corretto, staging/branch intoccati, non
tracciati inclusi), la retention count-based a 100, l'`add -f` sulla memoria,
il logger dedicato (verificato empiricamente: 82 righe snapshot, 0 righe
httpx nel log), l'onestà sul finding 🟠. Riserve:

- **R1** — root annidata in repo esterno: snapshot del repo SBAGLIATO che
  passa invece di bloccarsi (verificata empiricamente dal revisore).
  → **CHIUSA in sessione**: fix `show-toplevel == root` + test T11g.
  **Review #3-bis sul fix: APPROVATO senza riserve.**
- **R2** — ogni run_command, anche read-only, consuma uno slot di retention:
  sessioni shell intense possono ruotare i 100 ref. → finding 🟡 in
  stato_progetto.md (valutare KEEP più alto o count+età minima).
- **R3** — oggetti dei ref potati restano finché non gira `git gc`;
  `snapshots.log` append-only senza rotazione e non gitignorato. → finding 🟡,
  candidato per `gas doctor`.

Il revisore ha aggiunto 3 lezioni datate alla sua memoria persistente
(`git -C` risale ai genitori; pattern logger/handler-level; worst case
retention count-based) — ora 9 lezioni totali.

## Istituzioni

- A) `reports/stato_progetto.md` aggiornato (snapshot chiuso, R2/R3 aperti).
- B) `reports/diff_sessione.md` rigenerato per questa sessione.
- C) Revisore: 2 review in sessione (#3, #3-bis), memoria aggiornata.

## Prossimi passi

1. Sandbox/dry-run per `run_command` (chiude il finding 🟠).
2. `WINDOW_CHAR_CAP` (review #1).
3. Manutenzione snapshot in `gas doctor` (R2/R3).
