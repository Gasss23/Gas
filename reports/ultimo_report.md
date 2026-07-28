# Ultimo report — doc-only: regole operative vive + item aperti sepolti
**Data**: 2026-07-29  
**Branch**: docs/regole-e-aperti  
**Task**: Estrazione sezione "Regole operative vive" e riemersione item aperti sepolti nelle sezioni-sessione di `reports/stato_progetto.md`. Solo aggiunte, zero cancellazioni.

---

## § 1 — FETTE ESEGUITE

| Fetta | Esito |
|-------|-------|
| PARTE 1 — Sezione "## Regole operative vive" | FATTA |
| PARTE 2 — Scan item aperti nelle sezioni-sessione | FATTA |
| PARTE 2 — Aggiunta item non in corpo attivo | FATTA |
| reports/ultimo_report.md | FATTA |
| Commit + PR | FATTA |

---

## § 2 — PARTE 1: Regole operative vive

Sezione inserita subito **dopo** `## Istituzioni di processo` (riga 142 del file risultante), **prima** di `## Note operative VPS`. Ogni regola in forma imperativa, con data e puntatore alla sezione d'origine letta nel file.

### Mapping R1-R10 → origine nel file

| Regola | Trovata? | Riga fonte (main pre-edit) | Sezione d'origine |
|--------|----------|---------------------------|-------------------|
| **R1** | ✅ | 349-350 | `### ℹ️ Micro-finding merge su main (2026-07-22)` |
| **R2** | ✅ | 388-398 | `### Sessione 2026-07-23`, sezione SEQUENZA DI MERGE OBBLIGATORIA |
| **R3** | ✅ | 214, 162, 224 | `### Sessione 2026-07-24`, sezione "Deviazione di gate"; nota VPS §6 |
| **R4** | ✅ | 177-178 | micro-finding verdetto parafrasato + test post-review (2026-07-16) |
| **R5** | ✅ | 175 | micro-finding handoff diff --stat riciclato (2026-07-13) |
| **R6** | ✅ | 242 (riga ⛔) | `### DA FARE`, sezione "Bonifica branch remoti ESEGUITA" |
| **R7** | ✅ | 259, 318-320 | `### Sessione 2026-07-21` ℹ️ chiave SSH; confermato `### Sessione 2026-07-22` |
| **R8** | ✅ | 279-280 | `### Sessione 2026-07-22`, rettifica "ACCESSO SSH AL VPS PERSO era una DIAGNOSI ERRATA" |
| **R9** | ✅ | 311-312 | `### Sessione 2026-07-22`, ⚠️ CAMBIO DI COMPORTAMENTO |
| **R10** | ✅ | 222 | `### Sessione 2026-07-24 (p2)`, 🔴→✅ "~/bin/gasmerge NON era un symlink" |

Nessun "R\<n\> NON TROVATA". Tutte e 10 le regole erano presenti nel file.

---

## § 3 — PARTE 2: Scan item aperti nelle sezioni-sessione

### Sezioni scansionate

1. `### Sessione 2026-07-24 — sanare venv, T9a/T9c deterministici` (righe 188-211 pre-edit)
2. `### Sessione 2026-07-24 (p2) — merge PR #43 e registrazioni di processo` (righe 213-225)
3. `### Sessione 2026-07-21 — chiusura giro item fuori-roadmap` (righe 247-259)
4. `### Sessione 2026-07-22 — rientro accesso VPS + chiusura F7` (righe 261-323)
5. `### ℹ️ Micro-finding di processo — merge su main eseguito da dentro Claude Code (2026-07-22)` (righe 325-371)
6. `### Sessione 2026-07-23 — allineamento canonici (azioni senza traccia in git)` (righe 373-418)

### Lista completa righe con flag trovate per sezione

#### § Sessione 2026-07-24 (righe 188-225)
Nessuna riga con 🟡, 🔴, ⚠️, ⛔, APERT, NON VERIFICATO, RESIDUO, non decisa, MITIGATO.
→ Nessun item aperto.

#### § Sessione 2026-07-21 (righe 247-259)
- Riga 253: `⚠️ Reboot GAS in prod NON pianificato` — evento passato, GAS ripartito da solo, nessun danno, risolto. **Non item aperto da tracciare.**
- Riga 254: `🟡 2FA Hetzner non attivo` — **GIÀ nel corpo attivo** (DA FARE riga 239). Non aggiunto.
- Riga 258: `🟡 Copia VPS stantia vs origin/main` — **NON nel corpo attivo** → **AGGIUNTO** a DA FARE.

#### § Sessione 2026-07-22 (righe 261-323)
- Riga 266: `⚠️ RISERVA DI EVIDENZA` (F7 .gitignore) — **GIÀ nel corpo attivo** (DEPLOY VPS riga 97, "Verifica riserva evidenza F7"). Non aggiunto.
- Riga 294: `⚠️ RESIDUO NON VERIFICATO: /root/.ssh/authorized_keys` — **GIÀ nel corpo attivo** (DA FARE riga 240). Non aggiunto.
- Riga 298: `⚠️ RESIDUO: chiave gas-vps in Hetzner Security` — **GIÀ nel corpo attivo** (DA FARE riga 241). Non aggiunto.
- Riga 311: `⚠️ CAMBIO DI COMPORTAMENTO: passwd -l gas` — fatto documentato sul comportamento attuale del VPS, non item da tracciare. **Non aggiunto.**

#### § ℹ️ Micro-finding merge su main (righe 325-371)
- Riga 359: `decisione APERTA, non impegnata` (secondo account GitHub) — **NON nel corpo attivo** → **AGGIUNTO** a DA FARE.

#### § Sessione 2026-07-23 (righe 373-418)
- Riga 382: `⚠️ CAVEAT — cosa NON fa gasmerge` — limitazione documentata, non item da tracciare. **Non aggiunto.**
- Riga 414: `Decisione APERTA (non impegnata)` (trailer Co-Authored-By) — **NON nel corpo attivo** → **AGGIUNTO** a DA FARE.

---

## § 4 — Verifica item noti dal task

| Item | Trovato? | In corpo attivo? | Azione |
|------|----------|------------------|--------|
| 🟡 2FA Hetzner non attivo | ✅ riga 254 (sess. 2026-07-21), riga 269 (DA FARE) | ✅ DA FARE riga 239 | Nessuna (già presente) |
| ⚠️ /root/.ssh/authorized_keys non ispezionato (MITIGATO) | ✅ riga 294 (sess. 2026-07-22) | ✅ DA FARE riga 240 | Nessuna (già presente) |
| 🟡 chiave gas-vps in Hetzner Security (non decisa) | ✅ riga 298 (sess. 2026-07-22) | ✅ DA FARE riga 241 | Nessuna (già presente) |
| ⚠️ RISERVA DI EVIDENZA F7 | ✅ riga 266 (sess. 2026-07-22) | ✅ DEPLOY VPS riga 97 | Nessuna (già presente) |
| 🟡 copia VPS stantia vs origin/main (FASE 5 S2) | ✅ riga 258 (sess. 2026-07-21) | ❌ assente | **AGGIUNTO** a DA FARE |

---

## § 5 — Item aggiunti al corpo attivo (PARTE 2)

Aggiunti al fondo di `### DA FARE — sviluppo/processo`:

1. `🟡 Copia VPS stantia vs origin/main` (2026-07-21) — verbatim dalla riga 258 della sessione 2026-07-21.
2. `⚠️ Decisione APERTA — Secondo account GitHub` (2026-07-22) — dalla decisione APERTA nella sezione ℹ️ Micro-finding merge su main.
3. `⚠️ Decisione APERTA — Trailer Co-Authored-By` (2026-07-23) — dalla decisione APERTA nella sessione 2026-07-23.

---

## § 6 — STOP GATE

- **Nessuna riga cancellata**: file cresciuto da 418 a 470 righe (+52). Le due operazioni sono state entrambe additive.
- **Nessuna regola inventata**: tutte le R1-R10 trovate nel file e copiate dal testo reale (non scritte a memoria).
- **Nessuna archiviazione anticipata**: item dubbi trattati come aperti.
- **File toccati**: solo `reports/stato_progetto.md` e `reports/ultimo_report.md`.
- **Revisore**: NON invocato (doc-only, come da istruzioni).
- **Merge**: NON eseguito.
