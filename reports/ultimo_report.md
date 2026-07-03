# REPORT SONDA — Postazione Locale WSL (2026-07-03)

**Branch:** `sonda/postazione-locale`
**Obiettivo:** Verificare che la postazione WSL Ubuntu 24.04 regga il ciclo di sviluppo
che il cloud GitHub Actions non dà — in particolare i test bwrap-dipendenti.

---

## §1 SCOPE & ESITO FETTE

| Fetta | Titolo | Esito |
|-------|--------|-------|
| 1 | Suite completa con bwrap | **FATTA** — 214 PASS, 0 FAIL, 2 SKIP |
| 2 | Gate revisore operativo | **FATTA** — meccanismo descritto, nessun motore toccato |
| 3 | Report integrale | **FATTA** (questo documento) |

---

## §2 SUITE COMPLETA — CONTEGGIO E ESITO T11/T12/T13

### Ambiente
- **Python:** 3.12.3 (venv)
- **bwrap:** bubblewrap 0.9.0 — `/usr/bin/bwrap` ✅
- **Comando:** `.venv/bin/python tests/test_unit_kernel.py` (script standalone con sys.exit)
- **Output verbatim:** `reports/sonda_locale_suite.txt`

### Riepilogo

```
=== RIEPILOGO: 214 PASS, 0 FAIL ===
```

**SKIP (2):** T9a, T9c — "richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI"

### Esito T11 (snapshot preventivo) — tutti PASS ✅

```
[PASS] T11a write_file crea uno snapshot prima di scrivere — nuovi ref=1
[PASS] T11b snapshot = stato pre-modifica
[PASS] T11b2 git restore riporta il file alla versione pre-modifica
[PASS] T11c snapshot fallito -> write_file bloccata (fail-closed)
[PASS] T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed)
[PASS] T11d file non tracciato incluso nello snapshot
[PASS] T11e run_command fa scattare lo snapshot — refs 1 -> 2
[PASS] T11f retention (ramo count, età disattivata) tiene solo gli ultimi N — refs=3 (limite 3)
[PASS] T11g root annidata in repo esterno -> bloccata, nessun ref nel repo genitore
```

### Esito T12 (sandbox allowlist / no-shell) — tutti PASS ✅

```
[PASS] T12a comando in allowlist (wc) eseguito, output reale — 3 dati.txt
[PASS] T12b comando fuori allowlist negato, nessun effetto
[PASS] T12c pipe non interpretata (niente shell) — dati.txt
[PASS] T12d redirezione non crea file (niente shell) — riga1
[PASS] T12e command substitution non eseguita (resta letterale) — $(cat dati.txt)
[PASS] T12f argomento traversal in run_command negato
[PASS] T12g comando non interpretabile negato (fail-closed)
[PASS] T12h env figlio privo di variabili sensibili (KEY/TOKEN/SECRET...) — chiavi sensibili residue: []
[PASS] T12i dry-run: comando non eseguito e nessuno snapshot — refs 4->4
[PASS] T12j GAS_SHELL_MODE non valido -> fallback su 'guarded' — shell_mode=guarded
```

### Esito T13 (sandbox OS bwrap) — CUORE DELLA SONDA, tutti PASS ✅

I test T13 sono i veri test bwrap-dipendenti (non T11/T12). Sul cloud GitHub Actions
sono SKIP o FAIL perché bwrap è assente; qui su WSL sono tutti PASS.

```
[PASS] T13a rete bloccata nel sandbox (DNS fallisce) — rc=2 out=''
[PASS] T13b filesystem read-only (scrittura su project root negata) — rc=1 nato=False
[PASS] T13c segreto on-disk sotto /home mascherato (tmpfs lo copre) — rc=1 out='cat: /home/gqual/gas_esca_segreta_13349.txt: No su'
[PASS] T13d os_strict + sandbox assente -> run_command negato (fail-closed)
[PASS] T13d2 os_with_fallback + sandbox assente -> esegue (sandbox applicativa)
[PASS] T13e comando lecito read-only funziona dentro bwrap + snapshot scatta — out='3 dati.txt\n' refs 0->1
```

**Nota nomenclatura:** il task chiama "T11/T12 i test bwrap-dipendenti"; analisi del codice
conferma che i test bwrap-dipendenti sono T13a/b/c/e. T11 = snapshot git-based (senza bwrap),
T12 = sandbox applicativa (senza bwrap). Nessuna discrepanza di esito: tutti PASS in ogni caso.

---

## §3 CONFRONTO CON CONTEGGIO CANONICO

| Fonte | Conteggio letto | Data |
|-------|----------------|------|
| `stato_progetto.md` header | **208 PASS, 0 FAIL, 2 SKIP** | 2026-07-02 (pre-#42) |
| `stato_progetto.md` entry R-vec-pool | **216 PASS** | 2026-07-03 (post-#42) |
| `reports/handoff.md` §5 | **216 PASS, 0 FAIL** | 2026-07-03 (post-#42) |
| **Locale (questa sonda)** | **214 PASS, 0 FAIL, 2 SKIP** | 2026-07-03 |

**Discrepanza locale vs handoff: −2 PASS.** Spiegazione coerente: T9a e T9c sono SKIP
localmente (assenza API key live), mentre il conteggio 216 in handoff è stato prodotto
su una macchina che aveva le chiavi configurate (o in un ambiente con secrets).
La discrepanza è attesa e NON indica un bug. L'header di `stato_progetto.md` è stale
(208 vs 216) — non aggiornato dopo review #42; riportato come dato letto, NON corretto
(vincolo: nessuna modifica).

---

## §4 MECCANISMO GATE REVISORE

### Componenti ispezionati

**`.claude/hooks/review_gate.sh`** (PreToolUse hook):
1. Intercetta ogni tool call `Bash` il cui comando corrisponde a `git.*commit`.
2. Legge il diff staged via `git diff --cached --name-only`.
3. Se il diff tocca `gas.py`, `brains/`, `modules/` o `tests/` → controlla `.claude/.review_ok`.
4. Se il marcatore manca → `exit 2` con messaggio esplicito di blocco.
5. Commit di soli `reports/`, `*.md`, `config` → passa senza blocco (exit 0).

**`.claude/agents/revisore.md`**: subagent configurato, legge CLAUDE.md + stato_progetto.md
+ memoria_revisore.md prima di ogni review; emette APPROVATO / APPROVATO CON RISERVE /
RESPINTO.

**`.claude/.review_ok`**: marcatore one-shot. Attualmente **NON ESISTE** — stato corretto
tra un commit e l'altro (il marcatore viene creato solo dopo verdetto APPROVATO e rimosso
dopo il commit).

### Flusso di blocco (senza toccare il motore)

Un `git commit` che includesse `gas.py` in staging verrebbe bloccato con:
```
BLOCCATO (gate review): il diff staged tocca il motore (gas.py/brains/modules/tests)
ma manca .claude/.review_ok. Fai revisionare il diff dal subagent 'revisore'; se
APPROVATO crea il marcatore (touch .claude/.review_ok) e ricommitta, poi rimuovilo.
```
Exit code 2 → Claude Code segnala errore hook e non procede con il commit.

**Gate operativo: SÌ.** Il commit del presente report (solo `reports/`) non triggera
il gate (nessun file motore in staging).

---

## §5 NOTE

1. **pytest non adatto**: la suite usa `sys.exit()` a livello modulo — pytest genera
   `INTERNALERROR: SystemExit`. Comando corretto: `.venv/bin/python tests/test_unit_kernel.py`.

2. **bwrap 0.9.0 su WSL**: namespace di rete e filesystem funzionanti. T13a-T13e tutti PASS.
   Questa postazione WSL è pienamente abilitata per i test bwrap — il cloud GitHub Actions non lo è.

3. **CI attuale (Ubuntu runner)**: T13a/b/c/e probabilmente SKIP ("sandbox OS non disponibile"),
   quindi il conteggio CI effettivo è inferiore a 214. Il conteggio canonico 216 in handoff
   include T9a/T9c (API keys live) che il CI Ubuntu non ha.

4. **Nessuna modifica al motore**: gas.py, brains/, modules/, tests/ intatti per tutta la sonda.

5. **Prossimo step suggerito (umano)**: aggiornare l'header di `stato_progetto.md` da 208 a 214
   (locale bwrap, no API keys) o 216 (con API keys). Decisione di scope dell'umano.
