# Report — Sessione doc-only hygiene stato/roadmap
**Data**: 2026-07-28
**Branch**: docs/stato-roadmap-hygiene
**Tipo**: DOC-ONLY — nessuna modifica a motore/test/script/hooks/agenti

---

## Esito per punto

### A1 — Bonifica branch remoti: aggiornamento da 4 a 3 NON mergiati ✅ FATTO
- `feature/crm-dup-detect` rimosso dall'elenco dei branch ancora esistenti.
- Elenco aggiornato: `fix/crm-idemp-diario`, `fix/review44-riserve-AC`, `claude/phone-gas-development-10svqc`. Totale head = 4 (main + 3).
- Nota storica mantenuta (detect superato da rewrite PR #47 ed eliminato da origin) ma spostata FUORI dall'elenco dei branch attivi.

### A2 — Lezione push --delete ✅ FATTO
- Aggiunta come riga separata subito dopo la voce "Bonifica branch remoti":
  `git push origin --delete` non rifiuta branch non-fully-merged (a differenza di `git branch -d`). Ha funzionato per esito su crm-dup-detect, non per meccanismo. REGOLA: verifica a mano con `git branch --merged origin/main` o grep prima di cancellare.

### A3 — Potatura CI line ✅ FATTO
- `reports/stato_progetto.md`: riga CI trimma a PR #44–#49 (6 voci). Aggiunto puntatore "storico PR #23–#43 → `reports/stato_storico.md` § CI storica".
- `reports/stato_storico.md`: aggiunto heading "## CI storica (run su main, PR #23–#43)" con le 13 voci verbatim (PR #43, #41, #40, #37, #36, #35, #34, #33, #32, #27, #25, #24, #23). Nessun dato inventato.
- Conteggio: 19 voci originali → 6 in attivo + 13 in storico = 19 (coerente).

### A4 — Cross-reference R-verdetto-evidenza ✅ FATTO
- Aggiunta riga: "**Cross-ref (stessa classe D)**: barriera solo disciplinare in attesa di enforcement strutturale/meccanico — identica alla famiglia dei gate 'regola di forma' del progetto (main-lock rete = structural; revisore.md obbligo-evidenza = disciplinare). Il check specifico mancante: verificare automaticamente che ogni path:riga dichiarato nel verdetto esista davvero nel diff sottoposto."

### B1 — Nota origine blueprint FASE 4 in roadmap.md ✅ FATTO
- Aggiunto blocco di note sotto il FASE 4 header in `reports/roadmap.md` con puntatore esplicito a `reports/roadmap_da_valutare.md`.
- Nota: il commit "2 idee" (PR #49) conteneva 2 documenti distinti: il blueprint operativo di 169 righe (`roadmap_da_valutare.md`) + un singolo bullet in "💡 Idee da valutare". Etichetta PR poco descrittiva, contenuto autonomo.

### B2 — Caveat GDPR accanto al blueprint ✅ FATTO
- Aggiunta nota GDPR nel blocco FASE 4 di `reports/roadmap.md`: dati lead su Make/HubSpot/Airtable = privacy-sensitive; provider senza no-training-tier ESCLUSI dal CRM; vincolo già nei canonici ("TRIGGER DATI").

### B3 — Biforcazione architetturale aperta ✅ FATTO
- Aggiunta nota: la scelta tra GAS-motore-Python e orchestrazione no-code Make è una decisione di architettura NON PRESA — aperta da decidere prima di sviluppare qualsiasi fetta FASE 4. Non scritta come scelta già fatta.

---

## File toccati

| File | Modifica |
|------|----------|
| `reports/stato_progetto.md` | A1+A2 (bonifica branch), A3 (CI line trim), A4 (cross-ref R-verdetto), "Ultimo aggiornamento" |
| `reports/stato_storico.md` | A3: aggiunto heading "## CI storica (run su main, PR #23–#43)" + 13 voci verbatim |
| `reports/roadmap.md` | B1+B2+B3: blocco note FASE 4 blueprint con origine, GDPR, biforcazione architetturale |

## File NON toccati (STOP GATE rispettato)

gas.py, brains/, modules/, tests/, scripts/, .claude/hooks/, .claude/agents/memoria_revisore.md — nessuna modifica.

## Punti fuori-scope NON eseguiti

Nessuno. Tutti e 7 i punti della sessione eseguiti. Nessun out-of-scope rilevato che richiedesse la fermata prevista dal gate.

## Note di processo

- Il blueprint FASE 4 vive in `reports/roadmap_da_valutare.md` (file aggiunto da PR #49). Le note B1/B2/B3 sono state aggiunte in `reports/roadmap.md` nella sezione FASE 4 come puntatore annotato.
- stato_progetto.md post-modifica: 418 righe (era 417 — CI trim risparmia ~13 voci condensate in 1 riga, lezione push --delete aggiunge 2 righe).
- stato_storico.md post-modifica: 286 righe (era 278 — +8 righe heading + nota + CI storica).
- roadmap.md post-modifica: 228 righe (era 220 — +8 righe blocco note FASE 4).
