# Handoff sessione: design/cancello-v2

> Data: 2026-09-30  
> Branch: design/cancello-v2

---

## §0 DECISIONI UMANE RICHIESTE

**Nessuna.** Tutte le decisioni §8 del documento `design_cancello.md` sono state chiuse con le scelte dell'operatore 2026-09-29. Le prossime decisioni richieste emergeranno all'implementazione:

- §8d (batch approvazioni M1) rimane aperta — da valutare dopo C4 quando il volume reale è misurabile.
- §C-pin (fix testo libero nel pin di `_memoria_pin`) è un finding tecnico aperto: da decidere se affrontarlo prima o dopo le fette C1–C5.

---

## §1 Esito sonda

Nessuna sonda in questa sessione. Sessione doc-only.

---

## §2 git diff --stat della sessione

```
reports/design_cancello.md | 246 +++++++++++++++++++++++++++------------------
reports/diff_sessione.md   |  25 +++--
reports/stato_progetto.md  |   4 +-
reports/ultimo_report.md   |  75 +++++++-------
4 files changed, 203 insertions(+), 147 deletions(-)
```

---

## §3 git log commit sessione

(da compilare dopo il commit)

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

### `reports/design_cancello.md` → v2

Aggiornato con correzioni tecniche C-a/b/c/d e decisioni operatore 2026-09-29:

**C-a §3 contaminazione:**
- Verificato nel codice (gas.py:1239–1295): `_memoria_pin` inietta `prossima_azione` e `descrizione` eventi — testo libero da terze parti. Fatto documentato: oggi ogni turno con pin non vuoto nasce con testo libero di terzi nel system prompt.
- Contaminazione riscritta come per-finestra (non per-turno): il turno è contaminato se nella finestra inviata al provider c'è un tool result contaminante.
- `read_file` contamina sempre (rimossa eccezione "file non di sistema").

**C-b §4 read-back integrale:**
- `tool_args_json` mostrato integralmente (no troncamento 500 char). Se troppo grande → diniego automatico.
- `id` approvazione = UUID casuale monouso (non autoincrement).
- Approvazione legata a hash SHA-256 degli args; kernel esegue args salvati.
- Callback solo da `TELEGRAM_ALLOWED_IDS`.

**C-c §8f + Fetta C4 — turno suddiviso:**
- Architettura: azione parcheggiata in DB, turno si chiude; su Approva nuovo turno di sblocco.
- Motivazione: bot Telegram su singolo thread — polling sincrono bloccherebbe il thread.

**C-d CRM in turno contaminato:**
- `salva_contatto`/`imposta_stato_contatto` eseguibili fino a 5 scritture CRM/turno contaminato; dalla sesta → approvazione.

**Decisioni §8 chiuse (tutte):**
- 8a: UNCERTAIN+tetto C-d | 8b: solo Approva/Rifiuta | 8c: 30 min | 8e: os_strict determina classe | 8f: turno suddiviso | F-diario-eco: Opzione A prima di C1.

---

## §8 Prossimi passi consigliati

1. **F-diario-eco** (fetta autonoma, prima di C1): modificare `gas.py:~1859` per il solo ramo `ricorda` — sostituire `_esito_sintetico(out)` con `f"[OK] {n} risultati restituiti"`.
2. **C1** — scaffolding `modules/gate/gate.py`: `GateClass`, `GATE_ALLOWLIST`, `gate_classify()`. Zero modifiche a gas.py.
3. **C2** — integrazione in `run_turn`: flag `_finestra_contaminata`, gate check prima di `execute_tool_call`.
4. **C3** — coda approvazioni SQLite: tabella `approvals` con schema v2 (UUID, hash, telegram_user_id).
5. **C4** — bridge Telegram turno suddiviso.
6. **C5** — hardening scadenza e audit.
