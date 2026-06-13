# Diff sessione 2026-06-12 — Sandbox di `run_command`

Riepilogo dei file toccati in questa sessione (la storia completa sta in git).
3 file, +241 / -8 righe.

## `gas.py` (+102 / -... )

- **`import shlex`** in testa.
- **System prompt base** (`_GAS_SYSTEM_PROMPT_BASE`): aggiunta la regola sul
  sandbox — `run_command` è di sola lettura, senza shell; pipe/redirezioni/
  concatenazioni/`$(...)`/interpreti non funzionano; usare le opzioni native
  (`grep -c`, `wc -l`) e `write_file` per creare/modificare file.
- **`__init__`**: nuovo `self.shell_mode` letto da `GAS_SHELL_MODE`
  (`guarded`/`dry_run`, normalizzato; valore ignoto → `guarded` con warning).
  Corretta la descrizione del tool `run_command` nello schema (da "Esegue
  comandi shell" a "comando di sola lettura da una allowlist, senza shell").
- **Nuove costanti/helper** prima di `execute_tool_call`:
  - `SHELL_ALLOWLIST` (frozenset di comandi di sola lettura);
  - `SHELL_ENV_SENSITIVE_MARKERS` + `_sanitized_subprocess_env()` (toglie le
    variabili che somigliano a segreti dall'env dei processi figli);
  - `_vet_command(command, cwd)` (vetting fail-closed a 3 barriere).
- **Ramo `run_command`** riscritto: ordine vetting → (dry-run?) → snapshot →
  esecuzione `shell=False` con env sanificata e `timeout=60`. Eliminato
  l'unico `shell=True`. I comandi negati al vetting non scattano lo snapshot.

## `tests/test_unit_kernel.py` (+94 / -...)

- **Blocco T12** (10 nuovi check): allowlist sì/no, pipe/redirezione/command
  substitution rese innocue, traversal negli argomenti, comando non
  interpretabile, env sanificata, `dry_run`, fallback `guarded`.
- **T11c2 rinforzato**: da `touch` (negato al vetting) a `ls -la` (in
  allowlist), così il test esercita davvero il fail-closed dello *snapshot* in
  una dir senza git, con asserzione esplicita su "snapshot" nel motivo.
- Da 34 a **44 PASS, 0 FAIL**.

## `README.md` (+53)

- Nuova sezione **🔒 Sandbox di `run_command`** dopo "Macchina del tempo":
  le tre barriere, la sanificazione env, le due modalità `GAS_SHELL_MODE`, la
  tabella delle alternative native alle pipeline, e il limite residuo onesto
  (recinzione applicativa, non confinamento OS; chiusura piena = sandbox OS in
  roadmap). La sezione snapshot preesistente è rimasta identica.

## Perché

Chiudere i vettori naïve della falla 🟠 (la shell poteva esfiltrare leggendo
file e usando la rete). Il finding scende da 🟠 a 🟡: la chiusura piena è il
sandbox OS, ora in cima ai prossimi passi.
