# 📄 REPORT FINE TASK — Sandbox a livello OS (bwrap) per `run_command`

**Data:** 2026-06-14 · **Esito:** ✅ COMPLETATO · **Review:** #6 APPROVATO CON RISERVE · **Suite:** 52 PASS, 0 FAIL

---

## Chiarimenti richiesti (in testa, come da consegna)

### P0 — Forma dell'auto-commit SessionEnd in `5cc609b`
È **add SELETTIVO non-motore**, NON rimozione totale. L'hook `SessionEnd`
(`.claude/settings.json`) esegue:
`git add reports/ '*.md' .gas_history.json` (mai `git add -A`), poi commit+push
solo del cached.
`gas.py`, `brains/`, `modules/`, `tests/` **non** sono nella add-list →
**non possono essere auto-committati** dal SessionEnd. Verificato: `git show
5cc609b` tocca solo `.claude/*`, `.gitignore`, `CLAUDE.md` (nessun file motore).

### Riserve del revisore #5 (ribadite e tracciate come gli altri finding)
Già in `stato_progetto.md` (sezione Finding aperti), confermate:
- **R1 #5** — modello free hardcoded/volatile (`meta-llama/llama-3.3-70b-instruct:free`
  può sparire lato OpenRouter; `gas doctor` dovrebbe verificare l'ESISTENZA del
  modello, non solo la presenza della chiave). 🟡
- **R2 #5** — degrado a solo-testo del modello free non rilevato a runtime (se il
  modello non supporta i tool, il loop perde read_file/write_file; oggi solo
  dichiarato in commento). 🟡
- **R3 #5** — duplicazione costanti provider (URL/modelli) tra `run_turn` e
  `doctor`. Manutenibilità, non sicurezza. 🟡

Nessuna riserva #5 indebolisce i guardrail.

---

## Cosa è stato fatto

Implementata la **FASE 1 punto 1** della roadmap (chiusura piena del finding
esfiltrazione): `run_command` gira, dove l'host concede i namespace, dentro un
sandbox **bwrap**.

### Sonda preliminare dell'ambiente (OBBLIGATORIA da roadmap, eseguita PRIMA di progettare)
Codespace = **bwrap 0.9.0** presente, namespace concessi. Quattro barriere
validate empiricamente prima di scrivere codice: rete isolata (`getent` rc=2),
project root re-bind RO leggibile, scrittura su project root negata (RO), **esca
segreta sotto /home NON leggibile** (tmpfs). Confermati i due casi limite:
project root sotto `/tmp` (test) e sotto `/home` (deploy VPS).

### Decisioni §6 implementate
- **§6.1 PROFILO bwrap** (`_bwrap_prefix`): `--unshare-net --unshare-pid --proc
  /proc --new-session --die-with-parent --ro-bind / / --tmpfs /home --tmpfs
  /root --tmpfs /run --ro-bind <root> <root> --chdir <cwd> --clearenv` +
  `--setenv` di ogni var GIÀ sanificata. Le tmpfs MASCHERANO le home (chiavi,
  token, ~/.ssh, ~/.config); il re-bind RO della project root è PER ULTIMO (così
  funziona anche con root sotto /home). Chiude R2 (review #4) **anche in lettura**.
  *Deviazione consapevole:* `/tmp` non riceve tmpfs (§6.1 elenca solo
  /home,/root,/run) → resta RO come tutto `/`, più severo della parentesi del test.
- **§6.2 NIENTE GAS_ENV**: `GAS_SANDBOX_MODE` ∈ {`os_strict` (default),
  `os_with_fallback`}; valore ignoto → fail-safe su `os_strict` (la prod è
  protetta di default). `doctor`: sandbox assente + os_strict = FAIL; +
  os_with_fallback = WARN.
- **§6.3 ORTOGONALITÀ**: `GAS_SANDBOX_MODE` (dove) e `GAS_SHELL_MODE` (se)
  separati. Ordine `run_command`: vetting → dry_run? → snapshot → check sandbox
  (per mode) → exec in bwrap. `doctor` sonda la sandbox SEMPRE.

### Modifiche `gas.py`
`_probe_os_sandbox` (sonda reale + cache di processo), parse `GAS_SANDBOX_MODE` e
cache disponibilità in `__init__`, `_bwrap_prefix`, check sandbox per mode nel
ramo `run_command`, sezione 6 "Sandbox OS" in `doctor`, descrizione tool +
system prompt aggiornati.

---

## Test che MORDONO (zero token LLM) — risultato REALE

```
[PASS] T13a rete bloccata nel sandbox (DNS fallisce) — rc=2 out=''
[PASS] T13b filesystem read-only (scrittura su project root negata) — rc=1 nato=False
[PASS] T13c segreto on-disk sotto /home mascherato (tmpfs lo copre) — rc=1
[PASS] T13d os_strict + sandbox assente -> run_command negato (fail-closed)
[PASS] T13d2 os_with_fallback + sandbox assente -> esegue (sandbox applicativa)
[PASS] T13e comando lecito read-only funziona dentro bwrap + snapshot scatta

=== RIEPILOGO: 52 PASS, 0 FAIL ===
```

Ognuno fallisce se la barriera corrispondente viene tolta. La suite storica (46)
resta verde: T12a/c/d/e e T11e ora passano attraverso bwrap. `gas doctor`:
`[OK] Sandbox OS bwrap+namespace — bwrap + namespace net/pid OK (mode=os_strict)`.

---

## Verdetto revisore (review #6): APPROVATO CON RISERVE

Sul finding: con T13a (rete chiusa) + T13c (esca /home mascherata) + T13b (fs RO)
+ env sanificata, il revisore conferma **esplicitamente** che:
- il finding 🟠→🟡 **esfiltrazione si chiude a livello OS** in os_strict + sandbox
  disponibile;
- **R2 (valori attaccati ai flag, review #4) si declassa/neutralizza** in os_strict
  (anche con buco nel vetting, il file sotto /home è mascherato e la rete chiusa).

**Caveat onesto:** entrambe le chiusure valgono SOLO in os_strict con sandbox
disponibile; in `os_with_fallback` su host senza namespace si ricade nella sola
sandbox applicativa → tracciato come declassamento **condizionato**, non assoluto.

### Riserve #6 tracciate in `stato_progetto.md` (nessuna bloccante, nessuna indebolisce i guardrail)
- **R1 #6** — snapshot sprecato in os_strict quando il sandbox manca (check dopo
  snapshot per decisione §6.3; mitigazione possibile: anticipare il check in
  os_strict). 🟡
- **R2 #6** — trappola `--chdir` con `GAS_CWD` fuori dalla project root (fail-closed,
  ma limite di usabilità sul VPS: documentare che cwd deve stare dentro la root). 🟡
- **R3 #6** — `doctor` ridetermina `GAS_SANDBOX_MODE` invece di riusare
  l'attributo del kernel (manutenibilità). 🟡

---

## File toccati
- `gas.py` (motore, revisionato) — +134 righe
- `tests/test_unit_kernel.py` (revisionato) — +90 righe (blocco T13)
- `reports/stato_progetto.md`, `reports/diff_sessione.md`, `reports/ultimo_report.md`
- `.claude/agents/memoria_revisore.md` (lezioni nuove dal revisore)

## Prossimi passi
1. WINDOW_CHAR_CAP sulla finestra (review #1).
2. R1 #6 — anticipare il check sandbox prima dello snapshot in os_strict.
3. Manutenzione snapshot in `gas doctor` (conteggio ref, gc, rotazione snapshots.log).
4. R3 #5/#6 — estrarre costanti provider e parse `GAS_SANDBOX_MODE` in punti unici.
