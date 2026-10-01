# Report FETTA C2 + R-nw-1

**Data:** 2026-10-01  
**Branch:** feat/cancello-c2  
**Commit motore:** c388c0f  
**Commit memoria revisore:** #118 → 1759355, #119 → b5b99d6

---

## §0 — Sonda

- C1 confermato su origin/main (PR #107, commit `abb7aae`).
- Branch creato: `feat/cancello-c2` da origin/main.
- Spec letta: `reports/design_cancello.md` §C2 + §R-nw-1.

## §1 — Cosa C2 doveva fare (dalla spec)

Dal design §6 "Fetta C2":
- Aggiungere calcolo `_finestra_contaminata` prima di ogni chiamata provider, scansione `_get_window()` per tool result contaminanti.
- Prima di `execute_tool_call`: chiamare `gate_classify`. DENY → "Operazione negata". IRREVERSIBLE (o UNCERTAIN + contaminata) → stub approved (coda reale in C3).

R-nw-1 (spec passo 1):
- (a) `Path(...).resolve(strict=False)`
- (b) Confinamento `is_relative_to` PRIMA della denylist
- (c) Denylist case-insensitive (`casefold`) sul nome
- (d) fail-closed: eccezione = diniego

## §2 — Implementazione

**modules/gate/gate.py:**
- Aggiunto `UNTRUSTED_INPUT_TOOLS: frozenset` = {ricorda, read_file, browser_scrape, fetch_email} (§3b design)

**gas.py:**
- Aggiunto import `gate_classify, GateClass, UNTRUSTED_INPUT_TOOLS` da modules/gate/gate
- Aggiunto `_SAFE_PATH_DENY_PREFIXES` (class attribute, con varianti con e senza dot)
- Aggiunto `_deny_part(part, prefixes)` (metodo statico)
- Aggiunto `_finestra_e_contaminata(window)` (metodo statico puro, §3b)
- Modificato `_safe_path`: `resolve(strict=False)`, confinamento, denylist su `path.relative_to(root_resolved).parts`, fail-closed con log eccezione
- Rimosso check inline denylist in `execute_tool_call`/write_file (consolidato in `_safe_path`)
- In `run_turn` agentic loop: calcolo `_finestra_contaminata = self._finestra_e_contaminata(_window)` ad ogni iterazione; gate check prima di `execute_tool_call`

**tests/test_unit_kernel.py:**
- T71a-T71h: R-nw-1 (symlink dentro root → .gas_memory.db negato; symlink fuori root negato; traversal ../; case-insensitive .GAS_MEMORY; write consentito file nuovo; symlink rotto/ciclico senza crash; regressione root con prefisso gas_history_)
- T72a-T72e: C2 (SAFE passa invariato; DENY bloccato senza crash; ricorda+salva_contatto stub approved; UNTRUSTED_INPUT_TOOLS; finestra_e_contaminata puro)

## §3 — Test

**Baseline (prima di C2):** 400 PASS, 5 FAIL (F-mac-1 bwrap macOS)  
**Dopo C2 + R-nw-1:** 423 PASS, 5 FAIL (F-mac-1 invariati, +23 nuovi test tutti PASS)  
**Gate suite (pytest):** 74 PASS, 0 FAIL

Tutti i test T71 e T72 passano. Nessuna regressione.

## §4 — Verdetto revisore (VERBATIM)

### Review #118 — APPROVATO CON RISERVE

Ambito: diff staged su feat/cancello-c2 (fetta C2 + R-nw-1): gas.py, modules/gate/gate.py, tests/test_unit_kernel.py.

Letture obbligatorie fatte: CLAUDE.md sez. 5, 8 e 10; reports/stato_progetto.md; .claude/agents/memoria_revisore.md. Ho controllato anche reports/design_cancello.md §3a/§3b/§6 Fetta C2: l'implementazione segue la spec.

Verifiche eseguite:
- Suite kernel: 415 PASS, 5 FAIL. I 5 FAIL sono T11c2/T11e/T12a/T12c/T12e, cioè F-mac-1. Tutti i T71 e T72 passano.
- Suite gate (pytest): 74 PASS.

Elementi del diff esaminati:

1. gas.py:948 — ciclo della denylist for part in path.parts sul path risolto.
   Rischio esaminato: symlink, maiuscole/minuscole, falsi positivi.
   Però il ciclo controlla tutti i componenti del path assoluto, comprese le cartelle sopra la root. Ho creato una root sotto una cartella chiamata gas_history_proj_*: ok.txt viene negato. Il blocco è prudente e non tocca la root di produzione /home/gas/gas.
   Esito: riserva R-c2-1. Va usato path.relative_to(root_resolved).parts.

2. gas.py:941 + gas.py:954 — resolve(strict=False) sulla root e sul path, except Exception restituisce None.
   T71f e T71g non crashano.
   Esito: ok, con nota per R-c2-6.

3. gas.py:920 — _SAFE_PATH_DENY_PREFIXES, che sostituisce il vecchio controllo inline su write_file.
   backup_gas_history.txt prima era negato, ora viene consentito (verificato).
   Esito: riserve R-c2-2 e R-c2-5.

4. gas.py:1897 — calcolo di _finestra_contaminata su _window = self._get_window().
   Niente slicing: si usa _get_window() e lo stesso _window va nel payload.
   Esito: ok.

5. gas.py:1934 — ramo DENY e stub approved del gate.
   DENY restituisce un messaggio di diniego reale. Lo stub esegue il tool vero: non c'è output simulato.
   Esito: ok.

6. tests/test_unit_kernel.py:4956 — T72c.
   Il ramo stub e il ramo else eseguono lo stesso codice, e il test non controlla né il flag né il log [GATE-C2-STUB].
   Esito: riserva R-c2-3.

7. modules/gate/gate.py:67 — UNTRUSTED_INPUT_TOOLS.
   Set è {ricorda, read_file, browser_scrape, fetch_email}, identico alla tabella del design.
   Esito: ok.

Riserve:
- R-c2-1 (minore): denylist va su relative parts, non assoluti.
- R-c2-2 (minore): backup_gas_history.txt ora passa.
- R-c2-3 (minore): T72c non distingue stub dal ramo normale.
- R-c2-4 (cosmetica): messaggio "esce dalla root" anche per dinieghi da denylist.
- R-c2-5 (minore, architetturale): due denylist divergenti.
- R-c2-6 (osservabilità): except non logga dettaglio; run_command IRREVERSIBLE sempre in non-os_strict.

Rischi esplicitamente esclusi: comportamento su Linux/VPS; contaminazione dal pin di sistema; provider LLM reali.

Commit consentito: sì. Le riserve R-c2-1…R-c2-6 vanno tracciate in reports/stato_progetto.md.

---

### Review #119 — APPROVATO CON RISERVE (ri-review dopo fix R-c2-1 + R-c2-3)

Ambito: stesso diff staged, dopo le correzioni.

Letture obbligatorie fatte: CLAUDE.md sez. 5, 8 e 10; reports/stato_progetto.md; .claude/agents/memoria_revisore.md, compresa la lezione della #118.

Elementi del diff esaminati:

1. gas.py:959. Ora la denylist scorre path.relative_to(root_resolved).parts.
   Ho verificato con root temporanea dentro .../gas_history_host/root: a.txt e sub/b.txt sono consentiti; .gas_history.json e sub/GAS-History.txt sono negati; ../x è negato per traversal.
   L'ordine è giusto: il confinamento a gas.py:952 viene prima.
   Esito: ok, R-c2-1 CHIUSA.

2. gas.py:937. Il metodo statico _finestra_e_contaminata è puro e non ha effetti collaterali.
   Esito: ok, R-c2-3 CHIUSA.

3. gas.py:967. L'except di _safe_path ora logga {_e} e resta fail-closed.
   Esito: ok, R-c2-6 chiusa solo in parte.

4. tests/test_unit_kernel.py:4971. Blocco T72e contiene 5 check diretti sul metodo. Le asserzioni positive e negative sono separate.
   Esito: ok.

5. Wall of Shame. Nessuno slicing della history: la finestra arriva solo da _get_window(). Nessun output di tool simulato. Il cap for _ in range(10) è intatto.
   Esito: ok.

Riserve:
- R-c2-7 (minore, nuova): il diff non ha un test di regressione per R-c2-1 (aggiunto come T71h nello stesso commit).
- R-c2-2 / R-c2-4 / R-c2-5 / R-c2-6 residuo: ancora aperte, tracciate in stato_progetto.md.

Cosa non verificato: path con symlink (coperto da T71a-T71g però); provider LLM reali e Linux con bwrap.

Commit consentito: sì.

## §5 — Stato CI

In attesa di push — la PR verrà creata dopo il push del branch. CI verde prevista: i test su Linux non includono i 5 FAIL bwrap macOS (F-mac-1), quindi atteso 423 PASS su Linux (i bwrap test passano su Linux).
