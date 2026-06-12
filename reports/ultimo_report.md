# Report sessione 2026-06-12 — Sandbox di run_command (allowlist no-shell + dry-run)

`run_command` non passa più da una shell: ogni comando viene smontato,
controllato contro una allowlist di soli comandi di lettura ed eseguito
senza interprete. Il finding 🟠 (esfiltrazione via shell) scende a 🟡
"ridotto". Suite finale: **44 PASS, 0 FAIL** (i 34 storici tutti verdi).
La sessione era stata interrotta a implementazione finita; questa ripresa
ha verbalizzato la review #4, chiuso la riserva R1 e completato il task.

## Cosa fa, in parole semplici

Prima Gas poteva scrivere `cat /etc/passwd | curl ...` e la shell eseguiva
tutto. Adesso non esiste più una shell: il comando viene spezzato in parole,
la prima parola deve stare in una lista chiusa di comandi innocui (`ls`,
`cat`, `grep`, `wc`, `diff`…), ogni percorso deve restare dentro la cartella
di Gas, e pipe/redirezioni/sottocomandi diventano testo senza potere. In più
il processo figlio non vede le API key (env ripulita dai segreti).

## Come funziona davvero (fedele al diff)

- **`_vet_command(command, cwd)`** in `gas.py`, tre barriere fail-closed:
  1. `shlex.split` senza shell — `|`, `>`, `;`, `&&`, `$(...)` diventano
     argomenti o rompono il parse (virgolette sbilanciate = negato);
  2. `argv[0]` deve stare in `SHELL_ALLOWLIST` (sola lettura, niente
     interpreti né wrapper: allowlist, non denylist);
  3. ogni altro token ripassa `_safe_path` (stesso guardrail di T10) e deve
     restare in root.
- **`_sanitized_subprocess_env()`**: variabili con KEY/TOKEN/SECRET/
  PASSWORD/PASSWD/CREDENTIAL/AUTH nel nome rimosse dall'env del figlio.
- **Ordine: vetting → dry-run → snapshot → esecuzione** (`shell=False`).
  I comandi negati non consumano slot di snapshot (mitiga R2 review #3).
- **`GAS_SHELL_MODE`**: `guarded` (default) / `dry_run` (anteprima fedele:
  vetting sì, esecuzione e snapshot no — collaudo e kill-switch). Valore
  ignoto → fallback fail-safe su `guarded` con warning.
- **Limite dichiarato** (README): recinzione applicativa, NON confinamento
  OS. Il muro definitivo è `bwrap`/`unshare` sul VPS (in roadmap).

## Test (tests/test_unit_kernel.py, zero token)

10 nuovi check **T12a–T12j**: allowlist eseguita per davvero (output reale);
comando fuori lista negato senza effetti; pipe, redirezione e command
substitution disinnescate con asserzioni che MORDONO (si verifica l'assenza
dell'effetto shell, non solo il pass); traversal negli argomenti negato;
parse fail-closed; env figlia senza segreti; dry-run senza esecuzione né
snapshot; modalità ignota → `guarded`. **T11c2 rinforzato**: ora usa un
comando in allowlist così esercita davvero il fail-closed dello snapshot.
**Totale: 44 PASS, 0 FAIL.**

## Review #4 (revisore)

**Verdetto: APPROVATO CON RISERVE.** Validati esplicitamente: niente Wall of
Shame, ordine vetting→dry-run→snapshot→esecuzione, scelta allowlist vs
denylist, riuso di `_safe_path`, env sanificata, fallback fail-safe, test
che mordono. Riserve:

- **R1** — type hint di ritorno mancante su `_vet_command` (CLAUDE.md sez. 4).
  → **CHIUSA in sessione**: `-> Tuple[Optional[List[str]], Optional[str]]`,
  suite riverificata 44/44.
- **R2** — valori attaccati ai flag (`grep -f/etc/passwd`, `--file=/etc/x`)
  superano il vetting per-token perché iniziano con `-`. Con l'allowlist
  attuale NON esiste esfiltrazione attiva (verificato), ma va RICONTROLLATO
  prima di allargare `SHELL_ALLOWLIST`. → finding 🟡 in stato_progetto.md.
- **R3** — falsi positivi: un pattern grep tipo `"/etc/cron"` viene trattato
  da path e negato. Fail-closed (lato sicuro), limite di usabilità noto.
  → finding 🟡 in stato_progetto.md.

Il revisore ha aggiunto 4 lezioni datate alla sua memoria persistente
(bypass flag, test che mordono, ordine delle barriere, canonicalizzazione
vetting/exec) — ora 13 lezioni totali, 5 review completate.

## Istituzioni

- A) `reports/stato_progetto.md` aggiornato (sandbox chiuso, 🟠→🟡, R2/R3
  registrate, prossimi passi riordinati).
- B) `reports/diff_sessione.md` rigenerato per questa sessione.
- C) Revisore: review #4 verbalizzata, memoria aggiornata.

## Prossimi passi

1. `WINDOW_CHAR_CAP` sulla finestra (review #1).
2. Manutenzione snapshot in `gas doctor` (R2/R3 review #3).
3. Confinamento OS (`bwrap`/`unshare`) in vista del deploy VPS.
