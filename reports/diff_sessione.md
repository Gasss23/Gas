# 🔀 Diff sessione 2026-06-12

> Riepilogo del diff dell'ultima sessione. Si riscrive a ogni sessione;
> la storia completa sta in git.
> Sessione: **Sandbox di run_command** (roadmap ALTA "dry-run"), in due
> tempi: implementazione (interrotta per uscita accidentale) e ripresa con
> verbalizzazione della review #4, fix R1 e chiusura task.

## File toccati e perché

### `gas.py` (motore)
- **Nuovo metodo `_vet_command(command, cwd)`**: vetting fail-closed in tre
  barriere PRIMA di eseguire o fotografare: (1) `shlex.split` senza shell —
  pipe `|`, redirezioni `>`, concatenazioni `;`/`&&` e `$(...)` diventano
  testo o rompono il parse; (2) `argv[0]` deve stare in `SHELL_ALLOWLIST`
  (solo binari di sola lettura, niente interpreti né wrapper); (3) ogni
  altro token ripassa `_safe_path` (stesso guardrail di T10) e deve restare
  in root. Type hint di ritorno completo (fix riserva R1, review #4).
- **Nuovo metodo `_sanitized_subprocess_env()`**: l'env del processo figlio
  viene ripulita dalle variabili sensibili (marcatori KEY/TOKEN/SECRET/
  PASSWORD/PASSWD/CREDENTIAL/AUTH) — toglie il bersaglio principale
  dell'esfiltrazione anche se restasse un buco a monte.
- **`execute_tool_call("run_command")` riscritto**: ordine **vetting →
  dry-run → snapshot → esecuzione**, con `subprocess.run(argv, shell=False)`.
  I comandi negati non consumano slot di snapshot (mitiga R2 review #3).
- **`GAS_SHELL_MODE`**: `guarded` (default) / `dry_run` (anteprima fedele,
  kill-switch); valore ignoto normalizzato e ricaduto fail-safe su
  `guarded` con warning.
- **System prompt e schema tool aggiornati**: i modelli vengono istruiti
  sulle alternative native alle pipeline (`grep -c X file` invece di
  `grep X file | wc -l`; `write_file` invece delle redirezioni).

### `tests/test_unit_kernel.py`
- **Blocco T12a–T12j** (10 check): comando in allowlist eseguito davvero;
  comando fuori allowlist negato senza effetti; pipe, redirezione e command
  substitution disinnescate con asserzioni che "mordono" (assenza
  dell'effetto shell, non solo il pass); traversal negli argomenti negato;
  parse fail-closed su virgolette sbilanciate; env figlia senza segreti;
  dry-run senza esecuzione né snapshot; fallback su modalità ignota.
- **T11c2 rinforzato**: usa un comando in allowlist (`ls -la`) così il test
  esercita davvero il fail-closed dello snapshot invece di morire prima al
  vetting (falso verde).
- Suite: **44 PASS, 0 FAIL** (i 34 storici tutti verdi).

### `README.md`
- Nuova sezione **"🔒 Sandbox di run_command"**: le tre barriere, tabella
  modalità `GAS_SHELL_MODE`, tabella alternative native alle pipeline,
  limite residuo dichiarato (recinzione applicativa, non confinamento OS —
  il muro definitivo sarà `bwrap`/`unshare` sul VPS).

### `reports/stato_progetto.md`
- Finding 🟠 esfiltrazione via shell **declassato a 🟡 "ridotto"**; riserve
  R2/R3 della review #4 registrate come finding; suite a 44; prossimi passi
  riordinati (WINDOW_CHAR_CAP ora primo).

### `.claude/agents/memoria_revisore.md`
- +4 lezioni datate 2026-06-12 (totale 13): bypass dei valori attaccati ai
  flag; test che mordono; ordine vetting→dry-run→snapshot; canonicalizzazione
  token vetting vs exec.

## Review

**Review #4 (revisore): APPROVATO CON RISERVE.** R1 (type hint) chiusa in
sessione; R2 (valori attaccati ai flag, oggi non esfiltranti con questa
allowlist) e R3 (falsi positivi del path-check su argomenti non-path,
fail-closed) tracciate come finding 🟡.
