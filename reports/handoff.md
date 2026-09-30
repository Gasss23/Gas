# Handoff sessione: design/cancello-v2 (v2 + patch 8d + anti-discrepanza)

> Data: 2026-09-30  
> Branch: design/cancello-v2  
> PR: https://github.com/Gasss23/Gas/pull/105

---

## §0 DECISIONI UMANE RICHIESTE

**Nessuna.** Tutte le decisioni §8 del documento `design_cancello.md` sono ora chiuse:
- 8a UNCERTAIN+C-d ✅ | 8b Approva/Rifiuta ✅ | 8c 30 min ✅ | 8d per-azione ✅ | 8e os_strict ✅ | 8f turno suddiviso ✅ | F-diario-eco Opzione A ✅

Prossime decisioni emergeranno all'implementazione:
- §C-pin (fix testo libero nel pin di `_memoria_pin`): finding tecnico aperto, da decidere se affrontarlo prima o dopo le fette C1–C5.

---

## §1 Esito sonda

Nessuna sonda. Sessione doc-only.

---

## §2 GIT DIFF --STAT della sessione (vs main)

```
reports/design_cancello.md | 246 +++++++++++++++++++++++++++------------------
reports/diff_sessione.md   |  37 ++++---
reports/handoff.md         | 109 ++++++++++++--------
reports/stato_progetto.md  |   4 +-
reports/ultimo_report.md   |  61 +++++------
5 files changed, 268 insertions(+), 189 deletions(-)
```

---

## §3 git log commit sessione

```
e3cda69 docs(cancello-v2): §8d chiusa + anti-discrepanza handoff (K-b/K-g/K-h)
6f7cefd docs(cancello-v2): aggiorna §3 handoff con SHA commit e PR #105
6b9ff49 docs(cancello-v2): design gate v2 — correzioni C-a/b/c/d + decisioni operatore 2026-09-29
```

PR: https://github.com/Gasss23/Gas/pull/105

---

## §4 Delta test motore

Zero. Sessione doc-only, nessuna modifica a gas.py/brains/modules/tests/.  
Suite invariata: **392 PASS, 5 FAIL** F-mac-1 (invariati da sessione precedente).

---

## §5 Verdetto revisore

Non richiesto. La sessione non tocca gas.py, brains/, modules/ o tests/: il gate di review obbligatorio non si attiva per commit di soli reports/.

---

## §6 Stato CI

Non applicabile per sessione doc-only. Il check CI `unit-suite` è richiesto per merge PR; si attiverà al momento della PR.

---

## §7 Riepilogo modifiche

### `reports/design_cancello.md` → v2 (464 righe)

**Sessione 1 (correzioni C-a/b/c/d + decisioni 8a/b/c/e/f):**

- §3 contaminazione riscritta come per-finestra: il turno è contaminato se nella finestra inviata al provider c'è un tool result contaminante (non basta l'esecuzione nel turno corrente).
- `_memoria_pin` (gas.py:1239–1295): inietta `prossima_azione` e `descrizione` eventi — testo libero da terze parti. Fatto: oggi ogni turno con pin non vuoto nasce con testo libero di terzi nel system prompt.
- `read_file` contamina sempre (rimossa eccezione "file non di sistema").
- §4 read-back integrale (no troncamento 500 char); se troppo grande → diniego automatico.
- `id` approvazione = UUID casuale monouso (non autoincrement).
- Approvazione legata a hash SHA-256 degli args; kernel esegue args salvati.
- Callback solo da `TELEGRAM_ALLOWED_IDS`.
- Fetta C4 = turno suddiviso (polling sincrono bloccherebbe il thread del bot Telegram).
- C-d: scritture CRM eseguibili in turno contaminato fino a 5 totali; dalla sesta → approvazione.

**Sessione 2 (decisione 8d):**

- §8d: DECISO 2026-09-30 — firma per-azione, niente batch.

**Decisioni §8 chiuse (tutte 8):**

| # | Decisione |
|---|---|
| 8a | `imposta_stato_contatto` UNCERTAIN anche per stati finali; tetto C-d (5 scritture CRM/turno contaminato) |
| 8b | Solo [Approva]/[Rifiuta]; [Modifica] = fetta C6 futura |
| 8c | Timeout 30 min (`GAS_APPROVAL_TIMEOUT_SECS=1800`) |
| 8d | Firma per-azione, niente batch |
| 8e | `run_command` UNCERTAIN solo se `GAS_SANDBOX_MODE=os_strict`; altrimenti IRREVERSIBLE |
| 8f | Turno suddiviso |
| F-diario-eco | Opzione A, fetta autonoma prima di C1; fix vale solo in avanti |

---

## §8 Prossimi passi consigliati

1. **F-diario-eco** (fetta autonoma, prima di C1): `gas.py:~1859`, ramo `ricorda` — sostituire `_esito_sintetico(out)` con `f"[OK] {n} risultati restituiti"`.
2. **C1** — `modules/gate/gate.py`: `GateClass`, `GATE_ALLOWLIST`, `gate_classify()`. Zero modifiche a gas.py.
3. **C2** — integrazione `run_turn`: `_finestra_contaminata`, gate check prima di `execute_tool_call`.
4. **C3** — tabella `approvals` schema v2 (UUID, hash, telegram_user_id).
5. **C4** — bridge Telegram turno suddiviso.
6. **C5** — hardening scadenza e audit.

---

## §9 Output check scripts

```
check_handoff: OK — 5 file dichiarati correttamente.
check_verdetto: §4 non trovata in reports/handoff.md — non applicabile.
```

(check_handoff EXIT: 0, check_verdetto EXIT: 0)
