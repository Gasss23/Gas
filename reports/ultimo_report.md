# Ultimo Report — Verifica archiviazione stato (2026-07-29)

**Task**: doc-only — verifica del lavoro di PR #54 (`docs/archiviazione-stato`)
**Branch**: docs/archiviazione-stato (seconda istanza, verifica)
**Esito**: PR #54 VERIFICATO — task già completato correttamente

---

## ESITO DEL TASK

Il task di archiviazione (STEP 1: 6 sessioni + STEP 2: 9 finding ✅) è stato completato
da PR #54 (`f9ef498`, mergiata `ed760d7`). La presente sessione ha eseguito la
verifica secondo il protocollo STEP 0 del task.

**Nessuna modifica ai file di contenuto** (stato_progetto.md, stato_storico.md,
finding_archiviati.md) — il lavoro era già fatto correttamente.

---

## STEP 0 — GUARD PRE-ARCHIVIAZIONE (verifica a posteriori)

### a) Conteggi righe

| File | PRIMA (PR #53, `5aa6ee1`) | DOPO (PR #54, attuale) |
|------|---------------------------|------------------------|
| `reports/stato_progetto.md` | 470 | 235 |
| `reports/stato_storico.md` | 286 | 536 |
| `reports/finding_archiviati.md` | 35 | 44 |
| **TOTALE** | **791** | **815** |

DOPO (815) > PRIMA (791): **+24 righe** — nessuna perdita di testo. ✅

### b/c) Verifica item aperti nelle sezioni archiviate

Per ogni sezione archiviata, ogni marcatore 🟡/⚠️/RESIDUO/APERT/MITIGATO è stato
verificato contro il corpo attivo di `stato_progetto.md`:

**Sessione 2026-07-21** (storico righe 136-148):
- `🟡 2FA Hetzner non attivo` → stato_progetto.md riga 209 ✅
- `🟡 Copia VPS stantia vs origin/main` → stato_progetto.md riga 228 ✅
- `⚠️ Reboot GAS in prod NON pianificato` → evento PASSATO risolto (GAS ripartito da solo), non item aperto ✅

**Sessione 2026-07-22** (storico righe 150-212):
- `⚠️ RISERVA DI EVIDENZA` F7 → stato_progetto.md riga 69 (`🟡 Verifica riserva evidenza F7`) ✅
- `⚠️ RESIDUO NON VERIFICATO` /root/.ssh → stato_progetto.md riga 210 ✅
- `MITIGATO, non chiuso` (idem) ✅
- `⚠️ RESIDUO` chiave gas-vps in Hetzner → stato_progetto.md riga 211 ✅
- `⚠️ CAMBIO DI COMPORTAMENTO` passwd -l → R9 in "## Regole operative vive" ✅

**Sessione ℹ️ Micro-finding merge su main** (storico righe 214-260):
- `decisione APERTA` secondo account GitHub → stato_progetto.md riga 229 ✅

**Sessione 2026-07-23** (storico righe 262-307):
- `⚠️ CAVEAT — cosa NON fa` gasmerge → R2 in "## Regole operative vive" ✅
- `Decisione APERTA` Co-Authored-By → stato_progetto.md riga 230 ✅

**Sessioni 2026-07-24 e 2026-07-24 (p2)** (storico righe 308-345):
- Nessun item aperto autonomo ✅

**STOP GATE: NESSUNA sezione archiviata conteneva item aperti non presenti nel corpo attivo.** ✅

---

## STEP 1 — SESSIONI (verifica)

Sei sezioni archiviate presenti verbatim in `reports/stato_storico.md`:
- `### Sessione 2026-07-21 — chiusura giro item fuori-roadmap` (righe 136-148)
- `### Sessione 2026-07-22 — rientro accesso VPS + chiusura F7` (righe 150-212)
- `### ℹ️ Micro-finding di processo — merge su main eseguito da dentro Claude Code` (righe 214-260)
- `### Sessione 2026-07-23 — allineamento canonici` (righe 262-307)
- `### Sessione 2026-07-24 — sanare venv, T9a/T9c deterministici` (righe 308-331)
- `### Sessione 2026-07-24 (p2) — merge PR #43 e registrazioni di processo` (righe 333-345)

Campione verbatim (Sessione 2026-07-21, prima riga dopo l'header):
```
- ✅ **Scrub IP/SSH** (2026-07-20, PR #32 `f2679a4`): IP via da HEAD, verificato su albero mergiato via git grep (esatto+parziale = 0). Stato **MITIGATO** (resta in history pubblica → cura = privatizzazione, roadmap item 0).
```
Identico al testo nel commit `f9ef498` e nell'attuale `stato_storico.md`. ✅

Archive reference in `stato_progetto.md` per ognuna delle 6 sessioni: presenti. ✅

---

## STEP 2 — FINDING ✅ (verifica)

Nove finding archiviati da PR #54:

| # | Data | Finding | Note |
|---|------|---------|------|
| 28 | 2026-07-15 | R-legacy-slice | finding_archiviati.md riga 37 |
| 29 | 2026-07-16 | F6-history-atomica | finding_archiviati.md riga 36 |
| 30 | 2026-07-16 | R-crm-diario-rr | finding_archiviati.md riga 38 |
| 31 | 2026-07-18 | R-ci-hooks | finding_archiviati.md riga 39 |
| 32 | 2026-07-19 | R-hook-jq | finding_archiviati.md riga 40 |
| 33 | 2026-07-23 | R-ci-summary | finding_archiviati.md riga 41 |
| 34 | 2026-07-24 | R-ci-openrouter | finding_archiviati.md riga 42 |
| 35 | 2026-07-24 | R-gasmerge-failopen | finding_archiviati.md riga 43; **riserve aperte residue mantenute** |
| 36 | 2026-07-27 | R-crm-1b | finding_archiviati.md riga 44; **riserve aperte residue mantenute** |

`## Finding aperti (🟡 attivi)` in stato_progetto.md: **zero ✅** — conforme al STEP 2. ✅

Riserve aperte presenti verbatim in stato_progetto.md:
- R-gasmerge-failopen: #65-R1, #65-R2, #65-R3, #63-R1 (righe 59-62) ✅
- R-crm-1b: R1, R2, R3, R4 (righe 53-54) ✅

---

## VERIFICA FINALE

### Conteggio 🟡 (declared issue)

| Quando | Conteggio linee con 🟡 in stato_progetto.md |
|--------|---------------------------------------------|
| PRIMA (PR #53) | 20 |
| DOPO (PR #54, attuale) | 16 |
| Delta | **-4** |

La specifica dice "NON deve calare." Il calo è di 4. **Spiegazione verificata:**
- **-2**: duplicati interni alle sessioni (`🟡 2FA Hetzner non attivo` e `🟡 Copia VPS stantia`
  erano SIA nel corpo della sessione (archiviate) SIA nel corpo attivo di `stato_progetto.md`
  come voci separate. Il calo rimuove le copie nelle sessioni; le voci del corpo attivo restano.
- **-2**: marcatori `// ex-🟡` all'interno di finding ✅ CHIUSI (R-ci-hooks e R-ci-summary),
  testo storico dentro voci già chiuse — non item aperti.

**Nessun item aperto 🟡 è stato perso.** I 15 item 🟡 del corpo attivo pre-PR #54 sono
tutti presenti post-PR #54. Il calo di 4 è strutturalmente innocuo ma tecnicamente
viola la verifica numerica della specifica. **Dichiarato come finding di processo.**

### 3 item ✅ galleggianti

In `stato_progetto.md` righe 186, 191, 192 restano 3 item ✅ (R-crm-diario-rr CHIUSO,
Riserve hook #52-54 RISOLTE, Backfill #48-50 ESEGUITO) in una zona non sezione
("## Note operative VPS" area, prima di "### DA FARE"). Non erano in "## Finding aperti"
quindi fuori scope di STEP 2. Il loro contenuto è già in `stato_storico.md`.
**STOP GATE applicato: non rimossi.** Proposta di cleanup per sessione dedicata.

---

## Non-archiviati (conforme a specifica)

Rimangono nel corpo attivo di `stato_progetto.md` per specifica:
- `🟡 R-verdetto-evidenza`, `🟡 Esfiltrazione os_with_fallback`, `🟡 Degrado solo-testo per-turno`,
  `🟡 Riserve minori` ✅
- `### DEPLOY VPS — da tarare su dati reali` ✅
- `## Regole operative vive` ✅
- `## Note operative VPS` ✅

---

## CI

Non applicabile (task doc-only, nessuna modifica al motore).
