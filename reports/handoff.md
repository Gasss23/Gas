# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-14 — R-crm-1b Fette 2+3: idempotenza diario + telefono

---

## §0 DECISIONI UMANE RICHIESTE

Nessuna.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — `gas merge-contacts` + CLI check-dups + fix hint**: `FATTA` (sessione precedente, commit 9515626)
- **Fetta 2 — idempotenza diario**: `FATTA`
  `_append_sospetto` con tag `[ids:X,Y]` in descrizione + check LIKE idempotente prima di scrivere nel diario. `rileva_duplicati_email` aggiornata per usarlo. T59a/b/c.
- **Fetta 3 — telefono**: `FATTA`
  `normalizza_telefono` (pura, idempotente, +39/0039/locale), `_is_phone`, `rileva_duplicati_telefono` (speculare email), `check_dups_cmd` aggiornato per email+telefono. T60a-f.
- **Doc-only chiusura R-crm-1b**: `FATTA`
  R-crm-1b spostato da finding aperti a `finding_archiviati.md`. Conteggio CI riconciliato: 240 PASS (non 242).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +
 gas.py                             |  27 ++++---
 modules/memory/__init__.py         |   2 +
 modules/memory/store.py            | 143 ++++++++++++++++++++++++++++++++++-
 reports/diff_sessione.md           |  33 +++++----
 reports/finding_archiviati.md      |   1 +
 reports/handoff.md                 | 100 +++++++++++++------------
 reports/stato_progetto.md          |   8 +-
 reports/ultimo_report.md           | 148 +++++++++++++++++++++----------------
 tests/test_unit_kernel.py          | 122 ++++++++++++++++++++++++++++++
 10 files changed, 440 insertions(+), 147 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
0935efc docs(crm-dup-detect): chiusura R-crm-1b — archivia finding, corregge conteggio CI 240 PASS
759d12f docs(crm-dup-detect): handoff — CI run 29342632131 SUCCESS, 242 PASS
83ae3e4 docs(crm-dup-detect): aggiorna report — R-crm-1b fette 2+3, review #49, 242 PASS
1d32819 feat(crm-dup-detect): R-crm-1b Fette 2+3 — idempotenza diario + telefono
7f17c08 auto-commit fine sessione 2026-07-14_14:20 [solo reports/doc/history, motore escluso]
a58757f docs(crm-dup-detect): aggiorna stato_progetto — R-crm-1b fette 1+2, finding R-crm-diario-rr, 48 review, 231 PASS CI
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `1d32819` tocca `gas.py`, `modules/memory/store.py`, `modules/memory/__init__.py`, `tests/test_unit_kernel.py`.
Revisore invocato (subagent `revisore`, review #49) prima del commit. Verdetti integrali:

### FETTA 2 — idempotenza diario

> **APPROVATO CON RISERVE**
>
> Il meccanismo `_append_sospetto` è tecnicamente corretto: tag normalizzato (min,max), LIKE letterale sicuro su SQLite, SELECT+INSERT in connessione unica, exception handler completo. I test T59a/b/c coprono correttamente i tre casi (idempotenza, sospetti distinti, presenza del tag). L'unica riserva è un errore di documentazione nel docstring ("LIKE ... sul tipo" invece di "sulla descrizione") — non bloccante.

Riserva applicata prima del commit (docstring corretto).

### FETTA 3 — telefono

> **APPROVATO CON RISERVE**
>
> `normalizza_telefono` è fail-safe e idempotente per tutti gli input realistici; `rileva_duplicati_telefono` è strutturalmente speculare a quella email e usa correttamente `_append_sospetto`. I test T60a-f coprono normalizzazione, detection, falsi positivi e idempotenza. Due riserve non-bloccanti: (R1) la regex `r"[^\d+]"` lascia eventuali `+` interni in `digits` su input patologici — da correggere in hardening con `re.sub(r"\D", "", digits)` dopo la gestione del prefisso; (R2) import ridondanti nei test T60 (cosmetico).

Riserva R1 applicata prima del commit. R2 (cosmetica) non applicata.

---

## §5 DELTA TEST DEL MOTORE

Pre-sessione: 231 PASS (CI run 29336713885, feature/crm-dup-detect).
Post-sessione: **240 PASS** (CI run 29342632131, feature/crm-dup-detect).
Delta: **+9 test** — T59a, T59b, T59c, T60a, T60b, T60c, T60d, T60e, T60f.

```
=== RIEPILOGO: 240 PASS, 0 FAIL ===
```

NB: locale Codespace conta 242 — differenza di 2 sono T9a/T9c che passano con API keys live in Codespace ma vengono skippati in CI. Comportamento noto e documentato. CI è la fonte autorevole.

---

## §6 STATO CI

```
completed	success	docs(crm-dup-detect): chiusura R-crm-1b — archivia finding, corregge …	CI	feature/crm-dup-detect	push	29343210527	49s	2026-07-14T14:58:02Z
completed	success	docs(crm-dup-detect): handoff — CI run 29342632131 SUCCESS, 242 PASS	CI	feature/crm-dup-detect	push	29342729272	44s	2026-07-14T14:51:34Z
completed	success	docs(crm-dup-detect): aggiorna report — R-crm-1b fette 2+3, review #4…	CI	feature/crm-dup-detect	push	29342632131	56s	2026-07-14T14:50:14Z
```

CI run su commit motore (`1d32819`, via push `83ae3e4`): run **29342632131** — **SUCCESS** ✅ (56s).
CI run su HEAD sessione (`0935efc`): run **29343210527** — **SUCCESS** ✅ (49s).

---

## §7 RISERVE APERTE

- `R-crm-diario-rr` (latente, debito): `INSERT OR REPLACE` diretto sulla PK in `contatti` aggira i trigger di immutabilità del diario con `recursive_triggers` OFF. Codice applicativo usa solo INSERT puro — buco aperto solo ad accesso diretto al file `.db`. Da hardening futuro.
- `R-legacy-slice` (latente): `brains/claude_brain.py:38` slicing raw `messages[-8:]`. File legacy non wired al kernel, inerte. Diventa bloccante solo se ri-agganciato.
