# 📄 REPORT FINE TASK — Reporting/hook SessionEnd + sfoltimento doc + note VPS

**Data:** 2026-06-15 · **Esito:** ✅ COMPLETATO · **Revisore:** APPROVATO (TASK 1) ·
**Suite motore:** 75 PASS, 0 FAIL (invariata, zero token LLM) · **Test hook:** 8 PASS, 0 FAIL
(repo usa-e-getta) · **Motore (gas.py/brains/modules/tests):** INVARIATO

---

## DECISIONI UMANE RICHIESTE
Nessuna. Nessuno STOP è scattato: nessuna proprietà di sicurezza è stata indebolita
(gate di review intatto, hook solo additivo, motore mai committato, niente git
distruttivi). Resta UNA verifica da fare ma NON oggi (registrata in TASK 3): se gli
snapshot della "macchina del tempo" siano davvero persistiti tra sessioni (doctor
mostra 0 ref permanenti).

---

## TASK 1 — Hook SessionEnd: rumore nel log + sovrascrittura

### Diagnosi dei DUE meccanismi (verificata, non assunta)

**(i) Rumore nel log.** L'hook `SessionEnd` (inline in `.claude/settings.json`)
faceva `git add reports/ '*.md' .gas_history.json` e committava
`"auto-commit fine sessione …"` ogni volta che c'era staged: i deliverable
dell'agente (report) finivano dentro commit anonimi a messaggio generico, mescolati
a `.gas_history.json`. (NB onesto: il grosso del rumore VISIBILE nel log sono in
realtà i commit `scrivi rep` del *Stop hook* `scrivi_rep.sh`, che è una feature
separata e autorizzata, FUORI scope da TASK 1.)

**(ii) Sovrascrittura.** Il commit `7005517` ("report: test sicurezza isolamento
sandbox") ha sovrascritto `reports/ultimo_report.md` (−113/+56), sostituendo il
report dell'engine-change **bwrap** (`8b42f97`) con il report di un collaudo
read-only; ripristino manuale in `412714f`. **Causa primaria onesta:** `7005517` è
un commit **ESPLICITO dell'agente** sotto la convenzione "ultimo_report.md = unica
fonte di verità" → l'agente ha riusato il file canonico per un altro task. **L'hook
NON fa git distruttivi** (verificato: solo `git add`/`commit`/`push`, non può
sovrascrivere il working tree), quindi non è la causa materiale; è
l'**amplificatore**: auto-committava+pushava `reports/` senza checkpoint d'intento,
per cui una sovrascrittura presente nel working tree sarebbe stata persistita e
pushata in automatico e silenziosa.

### Fix applicato (giustificato dalla diagnosi)
1. **Procedurale (la vera cura):** CLAUDE.md §3 — l'agente committa+pusha DA SÉ i
   propri report/doc in UN commit a fine task, con messaggio descrittivo. Non
   delega all'hook. Ripristina il checkpoint d'intento perso.
2. **Hook additivo+condizionale:** `.claude/hooks/session_end.sh` (NUOVO, estratto
   da inline a script testabile, coerente con `scrivi_rep.sh`/`review_gate.sh`):
   - stage del SOLO allowlist (`reports/`, `*.md`, `.gas_history.json`); MAI
     `git add -A`/`.`;
   - **invariante di sicurezza**: se un file del motore fosse in staging, lo toglie
     con `git restore --staged` (additivo: NON tocca il working tree);
   - se nulla è in staging → **exit senza commit** (niente commit vuoti = fine del
     rumore);
   - commit+push fail-safe; nessun git distruttivo;
   - `GAS_REPO_DIR` override SOLO per i test (default `/workspaces/Gas`).
   - `.claude/settings.json`: `SessionEnd` ora chiama lo script.
   - Steady-state: l'agente committa i report → a fine sessione l'hook non trova
     `reports/` da committare (no-op), persiste solo `.gas_history.json`.

### Verifica REALE rosso→verde (output integrale, repo usa-e-getta, mai sul repo vero)

```
================ RED — bug sovrascrittura col VECCHIO comportamento ================
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.
--- HEAD:reports/ultimo_report.md dopo il VECCHIO hook ---
# REPORT B — collaudo read-only (sovrascrittura accidentale)
--- log ---
0f79bb2 auto-commit fine sessione 09:53:04 [vecchio]
d407ee6 report bwrap (canonico)
4ab5451 init
[PASS] RED riprodotto: vecchio hook ha persistito la sovrascrittura (A->B) in automatico, senza intento

================ GREEN — nuovo workflow (agente committa) + nuovo hook ================
--- HEAD:reports/ultimo_report.md dopo il NUOVO hook ---
# REPORT A — engine change bwrap (canonico)
--- commit prima=2 dopo=2 ---
[PASS] GREEN: nuovo hook NON crea un commit (report gia' committato dall'agente -> no-op su reports/)
[PASS] GREEN: report canonico A INTATTO, nessuna sovrascrittura silenziosa

================ SCENARIO 2 — nulla da committare -> nessun commit ================
--- log (invariato) ---
4ab5451 init
[PASS] Nulla in staging -> nessun commit creato (log invariato: 1==1)

================ SCENARIO 3 — modifica solo in reports/ -> 1 commit pulito ================
--- file nel commit di fine sessione ---
reports/stato_progetto.md
[PASS] Esattamente 1 commit creato
[PASS] Commit contiene SOLO path allowlist (fuori-allowlist: 'nessuno')

================ SCENARIO 4 — motore nel working tree -> MAI committato ================
--- file nel commit ---
reports/ultimo_report.md
[PASS] 4a: motore NON committato (gas.py/brains/ assenti dal commit)
--- file nel commit (con gas.py pre-staggiato) ---
reports/ultimo_report.md
[PASS] 4b: gas.py pre-staggiato -> invariante lo rimuove dallo staging, NON committato

=== RIEPILOGO HOOK: 8 PASS, 0 FAIL ===
```
(Le righe `fatal: 'origin'…` sono il *vecchio* hook che tenta il push nel repo
usa-e-getta privo di remote: atteso, innocuo, swallowed; il commit RED avviene
comunque.) Suite del motore ri-eseguita: **75 PASS, 0 FAIL** (invariata).

### Verdetto revisore (1e) — APPROVATO
APPROVATO senza riserve bloccanti. Verificato a mano: `git add '*.md'` è ricorsivo
(prende anche .md sotto le cartelle motore) MA l'invariante li ributta fuori prima
del commit → nessun file motore può sfuggire; niente commit vuoti; gate PreToolUse
INTATTO. **Riserve minori (non bloccanti, tracciate in stato_progetto.md):**
(1) path `/workspaces/Gas` hardcoded nello script — da rendere configurabile sul
VPS; (2) l'invariante motore è una RETE, non la difesa primaria (che resta
l'allowlist esplicita). Lezioni aggiunte a `memoria_revisore.md`.

### CLAUDE.md §3 (1f)
Aggiornata: regola "commit esplicito dei report" + descrizione hook
additivo/condizionale + nota di chiusura del bug di sovrascrittura.

**Commit TASK 1:** `8a6066b` (hook + settings + CLAUDE.md), dopo verde test e
verdetto revisore.

## TASK 2 — Sfoltimento `stato_progetto.md` (solo doc)
Creato `reports/finding_archiviati.md`: **12 finding chiusi** (✅) compressi a UNA
riga datata ciascuno (T10, snapshot preventivo, sandbox/dry-run, snapshot sprecato
os_strict, test `_cap_window_chars`, cap finestra, modello free, costanti provider,
parse `GAS_SANDBOX_MODE`, retention snapshot, manutenzione snapshot, + bug hook
TASK 1). Nessuna info distrutta (dettaglio in git). In `stato_progetto.md` la
sezione "Finding aperti" tiene INTEGRI i soli finding ATTIVI (🟡): esfiltrazione,
valori-attaccati-ai-flag, copertura `_cap_window_chars`, `WINDOW_CHAR_CAP` env,
trappola `--chdir`, falsi-positivi path-check, riserve TASK C, degrado solo-testo
runtime, riserve TASK B, + nuova riserva TASK 1. **Commit TASK 2:** `e1c8ed4`.

## TASK 3 — Note operative VPS (NON agire oggi)
Aggiunta sezione "Note operative VPS — non per oggi" in `stato_progetto.md`:
1. `gas doctor`: **0 ref snapshot permanenti + ~4427 oggetti loose** → pianificare
   `git gc` OPT-IN prima della VPS **e VERIFICARE se gli snapshot sono davvero
   persistiti** (macchina del tempo armata in steady-state o solo intra-sessione?).
2. **OpenRouter free ~28 s** (4° rung, degradato) → rafforza il piano
   **ollama-su-VPS**; dimensionare il VPS per **`qwen2.5:7b-instruct`** (RAM/CPU).
**Commit TASK 3:** `405fa30`.

## File toccati
- `.claude/hooks/session_end.sh` (NUOVO), `.claude/settings.json`, `CLAUDE.md` §3
- `reports/finding_archiviati.md` (NUOVO), `reports/stato_progetto.md`,
  `reports/diff_sessione.md`, `reports/ultimo_report.md`
- `.claude/agents/memoria_revisore.md` (lezioni review hook)
- Test: `/tmp/test_session_end_hook.sh` (usa-e-getta, non versionato)

## Conteggio finale
Suite motore **75 PASS, 0 FAIL** · Test hook **8 PASS, 0 FAIL** · Motore INVARIATO.

## Prossimi passi
1. (VPS) Verificare la persistenza degli snapshot + pianificare `git gc` OPT-IN.
2. (VPS) Dimensionare il VPS per `qwen2.5:7b` (ollama 5° rung offline).
3. Rilevamento PER-TURNO del degrado a solo-testo (metà aperta R2 #5).
4. Rendere configurabili via env i path/soglie hardcoded (`GAS_REPO_DIR`,
   `GAS_WINDOW_CHAR_CAP`, `GAS_SNAPSHOT_KEEP_DAYS`) al passaggio su VPS.
