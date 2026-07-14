# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-14 — R-crm-1b Fette 2+3: idempotenza diario + telefono

---

## §0 DECISIONI UMANE RICHIESTE

Nessuna.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — comando CLI `gas merge-contacts <da> <verso>`**: `FATTA` (sessione precedente)
- **Fetta 2 — idempotenza diario**: `FATTA`
  Helper `_append_sospetto` con tag `[ids:X,Y]` in descrizione + check LIKE idempotente prima di scrivere nel diario. `rileva_duplicati_email` aggiornata per usarlo.
- **Fetta 3 — telefono**: `FATTA`
  `normalizza_telefono` (pura, idempotente, +39/0039/locale), `_is_phone`, `rileva_duplicati_telefono` (speculare email), `check_dups_cmd` aggiornato. Idempotente via `_append_sospetto`.

---

## §2 GIT DIFF --STAT (sessione, rigenerato)

```
 gas.py                     |  27 +++++++---
 modules/memory/__init__.py |   2 +
 modules/memory/store.py    | 143 ++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_kernel.py  | 122 +++++++++++++++++++++++++++++++++++++++
 4 files changed, 280 insertions(+), 14 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
83ae3e4 docs(crm-dup-detect): aggiorna report — R-crm-1b fette 2+3, review #49, 242 PASS
1d32819 feat(crm-dup-detect): R-crm-1b Fette 2+3 — idempotenza diario + telefono
```

---

## §4 VERDETTI DEL REVISORE (review #49)

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

## §5 DELTA TEST (per fetta)

**Fetta 2 — T59:**
- T59a: idempotenza email — stesso sospetto 2 volte → 1 sola riga diario ✅
- T59b: sospetti email diversi → righe distinte ✅
- T59c: tag `[ids:X,Y]` nella descrizione ✅

**Fetta 3 — T60:**
- T60a: normalizza_telefono — 5 forme diverse → stesso canonico `393331234567` ✅
- T60b: stesso numero normalizzato → coppia segnalata + riga diario ✅
- T60c: numeri diversi → nessun falso positivo ✅
- T60d: contatti senza numero → nessun falso positivo ✅
- T60e: idempotenza diario telefono — 2 run → 1 riga ✅
- T60f: check_dups_cmd include risultati telefono ✅

**Suite totale: 242 PASS, 0 FAIL** (da 231 pre-sessione)

---

## §6 STATO CI

CI pre-sessione: run 29336713885 (2026-07-14): **231 PASS** ✅  
CI post-sessione: run **29342632131** (2026-07-14, feature/crm-dup-detect, commit 83ae3e4): **SUCCESS** ✅ — unit-suite in 52s.

---

## §7 FINDING APERTI / STATO R-crm-1b

**R-crm-1b: CHIUSO** — tutte e 3 le fette completate.

**Finding aperti correlati:**
- `R-crm-diario-rr` (INSERT OR REPLACE aggirava trigger) — LATENTE, da hardening futuro, NON toccato in questa sessione (STOP GATE 2 rispettato).
