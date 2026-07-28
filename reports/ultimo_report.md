# Report — Sessione doc-only hygiene stato/roadmap
**Data**: 2026-07-28
**Branch**: docs/stato-roadmap-hygiene
**Tipo**: DOC-ONLY — nessuna modifica a motore/test/script/hooks/agenti

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR `docs/stato-roadmap-hygiene` (hygiene stato/roadmap — 7 punti doc).

---

## Esito per punto

### A1 — Bonifica branch remoti: 4 → 3 NON mergiati — FATTA
- `feature/crm-dup-detect` rimosso dall'elenco branch attivi.
- Elenco aggiornato: `fix/crm-idemp-diario`, `fix/review44-riserve-AC`, `claude/phone-gas-development-10svqc`. Totale head = 4 (main + 3).
- Nota storica (detect superato da rewrite PR #47, poi eliminato da origin) spostata FUORI dall'elenco dei branch ancora esistenti.

### A2 — Lezione push --delete — FATTA
- Aggiunta come riga separata adiacente alla voce "Bonifica branch remoti":
  `git push origin --delete` non rifiuta branch non-fully-merged. Funzionato per esito (detect superato), non per meccanismo. REGOLA: verificare `git branch --merged origin/main` o grep del codice chiave prima di cancellare.

### A3 — Potatura CI line — FATTA
- `reports/stato_progetto.md`: riga CI trimma a PR #44–#49 (6 voci). Aggiunto puntatore a stato_storico.md.
- `reports/stato_storico.md`: aggiunto heading "## CI storica (run su main, PR #23–#43)" + 13 voci verbatim (PR #43, #41, #40, #37, #36, #35, #34, #33, #32, #27, #25, #24, #23).
- Conteggio di integrità: 19 voci originali → 6 in attivo + 13 in storico = 19 ✅.

### A4 — Cross-reference R-verdetto-evidenza — FATTA
- Aggiunta riga: "**Cross-ref (stessa classe D)**: barriera solo disciplinare in attesa di enforcement strutturale/meccanico — identica alla famiglia dei gate 'regola di forma' del progetto (main-lock rete = structural; revisore.md obbligo-evidenza = disciplinare). Il check specifico mancante: verificare automaticamente che ogni path:riga dichiarato nel verdetto esista davvero nel diff sottoposto."

### B1 — Nota origine blueprint FASE 4 — FATTA
- Blocco di note aggiunto in `reports/roadmap.md` sotto FASE 4 header, con puntatore a `reports/roadmap_da_valutare.md`.
- Il commit "2 idee" (PR #49) conteneva 2 documenti distinti: blueprint operativo 169 righe + singolo bullet "💡 Idee da valutare". Etichetta fuorviante, contenuto autonomo e strutturato.

### B2 — Caveat GDPR accanto al blueprint — FATTA
- Nota aggiunta in blocco FASE 4 di `reports/roadmap.md`: dati lead su Make/HubSpot/Airtable = privacy-sensitive; provider senza no-training-tier ESCLUSI dal CRM; vincolo già nei canonici ("TRIGGER DATI").

### B3 — Biforcazione architetturale aperta — FATTA
- Nota aggiunta: la scelta tra GAS-motore-Python e no-code Make è una decisione di architettura NON PRESA — aperta, da decidere prima di sviluppare qualsiasi fetta FASE 4. Non scritta come scelta già fatta.

---

## File toccati

| File | Modifica |
|------|----------|
| `reports/stato_progetto.md` | A1+A2 (bonifica branch + lezione push --delete), A3 (CI line trim), A4 (cross-ref R-verdetto), "Ultimo aggiornamento" |
| `reports/stato_storico.md` | A3: heading "## CI storica (run su main, PR #23–#43)" + 13 voci verbatim |
| `reports/roadmap.md` | B1+B2+B3: blocco note FASE 4 blueprint (origine, GDPR, biforcazione) |

## STOP GATE rispettato

Nessuna modifica a: gas.py, brains/, modules/, tests/, scripts/, .claude/hooks/, .claude/agents/memoria_revisore.md.

## Punti fuori-scope NON eseguiti

Nessuno — tutti e 7 i punti eseguiti. Nessun out-of-scope rilevato che richiedesse la fermata prevista dal gate.
