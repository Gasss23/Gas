# REPORT TASK — R-crm-1b Fette 2+3 + chiusura finding

**Data:** 2026-07-14
**Branch:** feature/crm-dup-detect
**Task:** R-crm-1b — Fetta 2 (idempotenza diario) + Fetta 3 (telefono) + doc-only chiusura finding

---

## DECISIONI UMANE RICHIESTE

Nessuna.

---

## ESITO FETTE

- **Fetta 1 — `gas merge-contacts` + CLI check-dups + fix hint**: `FATTA` (sessione precedente, commit 9515626)
- **Fetta 2 — idempotenza diario**: `FATTA`
  `_append_sospetto` con tag `[ids:X,Y]` + check LIKE idempotente. `rileva_duplicati_email` aggiornata. T59a/b/c.
- **Fetta 3 — telefono normalizzato**: `FATTA`
  `normalizza_telefono` (pura, idempotente, +39/0039/locale), `_is_phone`, `rileva_duplicati_telefono`, `check_dups_cmd` aggiornato. T60a-f.
- **Doc-only chiusura R-crm-1b**: `FATTA`
  R-crm-1b archiviato in `finding_archiviati.md`. Conteggio CI riconciliato: 240 PASS (non 242 — T9a/T9c passano in Codespace ma non in CI).

---

## COMMIT MOTORE

`1d32819` — feat(crm-dup-detect): R-crm-1b Fette 2+3 — idempotenza diario + telefono

File toccati: `gas.py`, `modules/memory/store.py`, `modules/memory/__init__.py`, `tests/test_unit_kernel.py`

---

## SUITE TEST

CI run 29342632131 (commit `83ae3e4`, 2026-07-14): **240 PASS, 0 FAIL** ✅
Pre-sessione (CI run 29336713885): 231 PASS.
Delta: +9 test (T59a/b/c + T60a-f).
NB: locale Codespace: 242 — differenza di 2 sono T9a/T9c con API keys live; CI è fonte autorevole.

---

## VERDETTI REVISORE (review #49)

**Fetta 2 — APPROVATO CON RISERVE**
> Il meccanismo `_append_sospetto` è tecnicamente corretto: tag normalizzato (min,max), LIKE letterale sicuro su SQLite, SELECT+INSERT in connessione unica, exception handler completo. I test T59a/b/c coprono correttamente i tre casi. Riserva: errore di documentazione nel docstring ("LIKE ... sul tipo" invece di "sulla descrizione") — non bloccante.

Riserva applicata prima del commit.

**Fetta 3 — APPROVATO CON RISERVE**
> `normalizza_telefono` è fail-safe e idempotente per tutti gli input realistici; `rileva_duplicati_telefono` è strutturalmente speculare a quella email e usa correttamente `_append_sospetto`. T60a-f coprono normalizzazione, detection, falsi positivi e idempotenza. Riserve: (R1) la regex `[^\d+]` lascia `+` interni su input patologici — `re.sub(r"\D", "", digits)` dopo gestione prefisso; (R2) import ridondanti T60 (cosmetico).

Riserva R1 applicata. R2 non applicata (cosmetica).

---

## ANOMALIE / RISERVE APERTE

- `R-crm-diario-rr` (latente): `INSERT OR REPLACE` diretto sulla PK aggira i trigger di immutabilità del diario (`recursive_triggers` OFF). Codice applicativo usa solo INSERT puro — buco aperto solo a chi accede al file `.db` direttamente. Da hardening futuro.
- `R-legacy-slice` (latente): `brains/claude_brain.py:38` contiene slicing raw `messages[-8:]`. File legacy non wired al kernel attivo.
