# REPORT — stato_progetto.md: chiusura canonica R-crm-1b

**Data:** 2026-07-27
**Task:** Aggiornamento canonico `reports/stato_progetto.md` — 4 modifiche circoscritte post-merge PR #47

---

## DECISIONI UMANE RICHIESTE

1. **Merge PR `docs/stato-crm1b-chiuso-finale`** (aperta, doc-only, CI deve essere verde).
2. **Finding line 244** — la riga `🔴 R-crm-1b fetta 3 (telefono) — codice ESISTE ma NON è su main` con `DECISIONE APERTA (operatore)` è ora stale (risolto dal merge PR #47). Valutare se marcarla ✅ CHIUSO nella prossima sessione (fuori scope di questo task per STOP GATE).

---

## ESITO FETTE

**Fetta 1 — R-crm-1b con PR #47 reference**: `FATTA`
- Aggiunto `merge PR #47 \`d67b12a\` 2026-07-27` nell'opening del finding.
- Chiarita sequenza: email+merge+idempotenza+telefono fetta 3 review #67 + esposizione fetta 4 review #68.

**Fetta 2 — DECISIONE APERTA dedup doctor/CLI: CHIUSA**: `FATTA`
- Aggiunta nota esplicita nel finding R-crm-1b: esposto email+telefono in `gas doctor` (sez. CRM) + `gas duplicati`, sola lettura, nessuna funzione di scrittura esposta al modello.

**Fetta 3 — Traccia 4 riserve R1-R4**: `FATTA`
- Rimossi i due gruppi separati "Riserve #67 R1/R2" e "Riserve #68 R1/R2" (counter che ripartiva da R1 per ogni review).
- Sostituiti con etichette continue: R1 `int(r["id"])` fuori try/except (#67); R2 `chiave_norm` non coperto da T60 (#67); R3 commento `# 11 CRM` fuori sequenza (cosmetico, #68); R4 T61d `or "Duplicati"` sempre vera (#68).

**Fetta 4 — Correggi meta-nota contatore (#65 → #68)**: `FATTA`
- Il "contatore" era il doppio set R1/R2 interno al finding (ripartiva per ogni review). Ora R1-R4 unificati. I campi globali (Stato motore, Istituzione C) erano già a #68.

---

## ANOMALIE

- Nessuna anomalia tecnica.
- Segnalato: line 244 (`🔴 R-crm-1b fetta 3...`) è stale — non toccata per STOP GATE, proposta in §0.
