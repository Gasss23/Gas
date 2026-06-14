# 🔧 DIFF DI SESSIONE — 2026-06-14

> Fotografia dell'ultima sessione (la storia completa è in git).
> Tema: **FASE 2 / FASE 1 punto 1 — Sandbox a livello OS (bwrap) per `run_command`**.

## File toccati

### `gas.py` (motore — revisionato, review #6 APPROVATO CON RISERVE)
- **`_GAS_SYSTEM_PROMPT_BASE`**: aggiunta una riga — dove disponibile,
  `run_command` gira in sandbox OS con rete isolata e filesystem read-only.
- **`_probe_os_sandbox(force=False) -> Tuple[bool, str]`** (nuova funzione di
  modulo, cache di processo `_OS_SANDBOX_CACHE`): sonda REALE (non simulata) —
  `shutil.which("bwrap")` + creazione di un namespace minimale ed esecuzione di
  `true`. Riusata da `__init__` e da `doctor`.
- **`GasKernel.__init__`**: parse di `GAS_SANDBOX_MODE` ∈ {`os_strict` (default),
  `os_with_fallback`} con normalizzazione e fail-safe su `os_strict`; cache di
  `self.os_sandbox_available` / `self._os_sandbox_detail`. Aggiornata la
  `description` del tool `run_command`.
- **`GasKernel._bwrap_prefix(cwd) -> List[str]`** (nuovo helper): costruisce il
  prefisso bwrap del profilo §6.1 (rete chiusa, pid ns, fs RO, tmpfs di
  mascheramento su /home·/root·/run, re-bind RO della project root PER ULTIMO,
  `--clearenv` + `--setenv` dell'env sanificata). Esposto come metodo così i
  test esercitano il profilo direttamente.
- **`execute_tool_call` (ramo `run_command`)**: inserito il check sandbox per
  mode DOPO lo snapshot (§6.3). os_strict + assente → "Operazione negata"
  (fail-closed, niente exec). Disponibile → exec con `_bwrap_prefix(cwd) + argv`.
  os_with_fallback + assente → warning + exec applicativo. Unica `subprocess.run`.
- **`doctor`**: nuova sezione 6 "Sandbox OS" — sonda SEMPRE; OK se disponibile,
  FAIL se os_strict+assente, WARN se os_with_fallback+assente.

### `tests/test_unit_kernel.py` (revisionato insieme al motore)
- Nuovo blocco **T13** (6 check): T13a rete bloccata (`getent` rc≠0), T13b
  filesystem read-only (touch su project root negato), T13c segreto on-disk
  sotto /home mascherato (tmpfs), T13d/T13d2 fallback per `GAS_SANDBOX_MODE`
  (deterministico, forza `os_sandbox_available=False`), T13e comando lecito
  read-only dentro bwrap + snapshot scatta. Helper `skip()` per host senza
  namespace. Risultato reale: **52 PASS, 0 FAIL**.

### Documentazione / processo
- `reports/stato_progetto.md`: sandbox OS ATTIVO; finding esfiltrazione e R2
  declassati (chiusura **condizionata** a os_strict + sandbox disponibile);
  riserve review #6 (R1 snapshot-prima-del-check, R2 caveat `--chdir`/cwd, R3
  duplicazione mode in doctor); suite 52; prossimi passi riordinati.
- `.claude/agents/memoria_revisore.md`: lezioni nuove datate 2026-06-14
  (aggiunte dal subagent revisore).
- `reports/ultimo_report.md`: report di fine task (fonte di verità sull'esito).

## Verifiche eseguite (reali, in questo Codespace)
- Sonda ambiente PRIMA di progettare (roadmap): bwrap 0.9.0, namespace concessi.
- 4 barriere validate empiricamente: rete rc=2, project root RO leggibile,
  scrittura su root negata, esca segreta sotto /home NON leggibile.
- Suite completa: **52 PASS, 0 FAIL**.
- `gas doctor`: riga "Sandbox OS" = `[OK] bwrap + namespace net/pid OK (mode=os_strict)`.
