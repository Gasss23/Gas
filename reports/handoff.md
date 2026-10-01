# Handoff sessione — feat/cancello-c2 — 2026-10-01

## §DECISIONI UMANE RICHIESTE

Nessuna decisione umana urgente per questa sessione.

Prossima fetta raccomandata: **C3** — coda approvazioni SQLite (`approvals` table, schema §4a del design). Prima di C3, valutare se affrontare F-controlli-auto (fix check_verdetto).

---

## §1 — Esito sonda

C1 era su origin/main (PR #107, `abb7aae`). Branch `feat/cancello-c2` creato da origin/main.

Spec letta: `reports/design_cancello.md` §C2 + §R-nw-1.

Cosa C2 doveva fare (citazione spec §6):
- Aggiungi calcolo `_finestra_contaminata` prima di ogni chiamata provider.
- Prima di `execute_tool_call`: chiama `gate_classify`. DENY → "Operazione negata". IRREVERSIBLE (o UNCERTAIN + contaminata) → stub approved.
- **Test C2:** round-trip con tool SAFE passa invariato; tool DENY bloccato senza crash; `ricorda` + `salva_contatto` in sequenza → stub approved.

R-nw-1: `resolve(strict=False)`, confinamento prima denylist, casefold, fail-closed.

---

## §2 — git diff --stat reale della sessione

```
.claude/agents/memoria_revisore.md |   5 +
gas.py                             |  99 ++++++++++++++++----
modules/gate/gate.py               |   6 ++
tests/test_unit_kernel.py          | 183 +++++++++++++++++++++++++++++++++++++
4 files changed, 274 insertions(+), 19 deletions(-)
```

---

## §3 — git log commit della sessione

```
c388c0f feat(cancello-c2): C2 gate integration + R-nw-1 path hardening
b5b99d6 chore(revisore): memoria review #119 — APPROVATO CON RISERVE
1759355 chore(revisore): memoria review #118 — APPROVATO CON RISERVE
```

---

## §4 — Verdetti revisore (VERBATIM)

### Review #118 — APPROVATO CON RISERVE

Ambito: diff staged su feat/cancello-c2 (fetta C2 + R-nw-1): gas.py, modules/gate/gate.py, tests/test_unit_kernel.py.

Letture obbligatorie fatte: CLAUDE.md sez. 5, 8 e 10; reports/stato_progetto.md; .claude/agents/memoria_revisore.md. Ho controllato anche reports/design_cancello.md §3a/§3b/§6 Fetta C2: l'implementazione segue la spec.

Verifiche eseguite:
- Suite kernel: 415 PASS, 5 FAIL. I 5 FAIL sono T11c2/T11e/T12a/T12c/T12e, cioè F-mac-1 (bwrap assente su macOS), già noti. Tutti i T71 e T72 passano.
- Suite gate (pytest): 74 PASS.
- Prova diretta di _safe_path su una root temporanea reale.

Elementi del diff esaminati:

1. gas.py:948 — ciclo denylist for part in path.parts sul path risolto.
   Rischio: root dentro cartella gas_history_proj_* blocca ok.txt — il blocco è prudente ma non tocca la root prod.
   Esito: riserva R-c2-1. Va usato path.relative_to(root_resolved).parts.

2. gas.py:941 + gas.py:954 — resolve(strict=False), except Exception → None.
   T71f e T71g non crashano.
   Esito: ok, con nota R-c2-6.

3. gas.py:920 — _SAFE_PATH_DENY_PREFIXES.
   backup_gas_history.txt ora consentito (era negato prima). Due denylist divergenti.
   Esito: riserve R-c2-2 e R-c2-5.

4. gas.py:1897 — _finestra_contaminata su _get_window(). Niente slicing. Campo name presente.
   Esito: ok.

5. gas.py:1934 — ramo DENY e stub. DENY restituisce diniego reale. Stub esegue tool vero.
   Esito: ok.

6. tests/test_unit_kernel.py:4956 — T72c non distingue stub da ramo normale.
   Esito: riserva R-c2-3.

7. modules/gate/gate.py:67 — UNTRUSTED_INPUT_TOOLS identico al design §3b.
   Esito: ok.

Riserve: R-c2-1 (minore), R-c2-2 (minore), R-c2-3 (minore), R-c2-4 (cosmetica), R-c2-5 (minore architetturale), R-c2-6 (osservabilità).
Rischi esclusi: Linux/VPS bwrap; contaminazione pin sistema; provider LLM reali.
Commit consentito: sì.

---

### Review #119 — APPROVATO CON RISERVE (ri-review)

Ambito: stesso diff staged dopo fix R-c2-1 e R-c2-3.

Letture obbligatorie fatte: CLAUDE.md sez. 5, 8 e 10; reports/stato_progetto.md; .claude/agents/memoria_revisore.md, compresa la lezione della #118.

Elementi del diff esaminati:

1. gas.py:959 — path.relative_to(root_resolved).parts.
   Verificato con root dentro .../gas_history_host/root: a.txt consentito, .gas_history.json negato.
   L'ordine è giusto: confinamento gas.py:952 viene prima.
   Esito: ok, R-c2-1 CHIUSA.

2. gas.py:937 — _finestra_e_contaminata puro, no side-effect.
   _add_to_history("tool", ..., name=...) a gas.py:1970 imposta il campo name.
   Esito: ok, R-c2-3 CHIUSA.

3. gas.py:967 — except logga {_e}, fail-closed invariato.
   Esito: ok, R-c2-6 chiusa in parte.

4. tests/test_unit_kernel.py:4971 — T72e, 5 check diretti sul metodo puro.
   Esito: ok.

5. Wall of Shame — nessuno slicing, nessun output simulato, cap range(10) intatto.
   Esito: ok.

Riserve residue: R-c2-7 (test regressione R-c2-1 assente nel diff — aggiunto come T71h), R-c2-2/R-c2-4/R-c2-5/R-c2-6 residuo tracciate in stato_progetto.md.
Nessuna regressione: 420 PASS, 5 FAIL (F-mac-1). Gate 74 PASS.
Commit consentito: sì.

---

## §5 — Delta test del motore

| Suite | Prima | Dopo | Delta |
|---|---|---|---|
| Kernel (`test_unit_kernel.py`) | 400 PASS, 5 FAIL | 423 PASS, 5 FAIL | +23 PASS |
| Gate pytest (`test_unit_gate.py`) | 74 PASS | 74 PASS | invariato |

I 5 FAIL sono F-mac-1 (bwrap macOS), invariati.

---

## §6 — Stato CI

PR non ancora creata (branch da pushare). CI attesa verde: su Linux i test bwrap passano, quindi attesi 423 PASS, 0 FAIL (Linux non ha F-mac-1).
