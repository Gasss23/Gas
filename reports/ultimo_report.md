# Report: doc-only — archiviazione stato_progetto.md (2026-07-29)

**Branch**: `docs/archiviazione-stato`
**Tipo**: doc-only (nessun revisore richiesto)
**Scope**: STEP 0 guard + STEP 1 sessioni + STEP 2 finding ✅

---

## ESITO: COMPLETATO ✅

### Fette

- **STEP 0 — Guard pre-archiviazione**: FATTO. Tutte le 6 sessioni archiviabili.
- **STEP 1 — Archivia sessioni**: FATTO. 6 sezioni → stato_storico.md, rinvii al posto.
- **STEP 2 — Archivia finding ✅**: FATTO. 9 finding → storico (testo integrale) + finding_archiviati.md (one-liner); riserve residue mantenute VERBATIM.

---

## STEP 0 — Guard pre-archiviazione

Sonda sistematica su tutti i marcatori 🟡, 🔴, ⚠️, APERT, RESIDUO, NON VERIFICATO, MITIGATO
nelle 6 sezioni da archiviare. Ogni occorrenza verificata contro il corpo attivo (## Finding aperti + ### DA FARE).

**Risultato: tutte le 6 sessioni sono archiviabili. Nessun blocco.**

Dettaglio verifiche:
- 🟡 2FA Hetzner (s21 riga 306) → in DA FARE riga 276 ✅
- 🟡 Copia VPS stantia (s21 riga 310) → in DA FARE riga 295 ✅
- ⚠️ RESIDUO /root/.ssh, gas-vps Hetzner (s22) → in DA FARE righe 277-278 ✅
- ⚠️ CAMBIO DI COMPORTAMENTO passwd -l gas (s22) → coperto da R9 in ## Regole operative vive ✅
- ⚠️ RISERVA DI EVIDENZA F7 (s22) → in DEPLOY VPS come 🟡 Verifica riserva evidenza F7 ✅
- APERT secondo account GitHub (mf) → in DA FARE riga 296 ✅
- APERT trailer Co-Authored-By (s23) → in DA FARE riga 297 ✅
- ⚠️ Reboot GAS in prod (s21 riga 305) → nota storica evento concluso, non azione aperta ✅

---

## STEP 1 — Sessioni archiviate

6 sezioni rimosse da `stato_progetto.md` (sostituite con rinvio) e appese VERBATIM a
`reports/stato_storico.md` § Changelog sessioni (cronologico):

| Sezione | Righe originali (0-indexed) | Linee |
|---|---|---|
| Sessione 2026-07-21 | sp[298:312] | 14 |
| Sessione 2026-07-22 | sp[312:376] | 64 |
| ℹ️ Micro-finding 2026-07-22 | sp[376:424] | 48 |
| Sessione 2026-07-23 | sp[424:470] | 46 |
| Sessione 2026-07-24 | sp[224:249] | 25 |
| Sessione 2026-07-24 (p2) | sp[249:263] | 14 |
| **TOTALE** | | **211 righe** |

---

## STEP 2 — Finding ✅ archiviati

9 finding ✅ rimossi da `## Finding aperti` di `stato_progetto.md`.
Testo integrale → `reports/stato_storico.md` § Finding chiusi (archiviati).
One-liner → `reports/finding_archiviati.md`.

**Eccezioni (riserve aperte residue mantenute in stato_progetto.md):**

- **R-crm-1b**: corpo archiviato; riserve R1–R4 mantenute VERBATIM.
- **R-gasmerge-failopen**: corpo archiviato; riserve #65-R1, #65-R2, #65-R3, #63-R1 mantenute VERBATIM.

---

## VERIFICA FINALE

| Check | Risultato |
|---|---|
| sum righe AFTER >= BEFORE (791) | 815 >= 791 ✅ |
| 🟡 corpo attivo non calato | 16 (corpus attivo invariato) ✅ |
| Campione s21 (14 righe) byte-identico in storico | ✅ |
| Campione R-gasmerge (24 righe) byte-identico in storico | ✅ |
| Campione s23 (46 righe) byte-identico in storico | ✅ |
| Nessun ✅ residuo in ## Finding aperti | ✅ |
| Riserve residue presenti (R-crm-1b + R-gasmerge) | ✅ |
| 6 rinvii presenti in stato_progetto.md | ✅ |

**Nota 🟡 count 20→16**: le 4 🟡 archiviate erano duplicati (2FA Hetzner + Copia VPS
stantia già in DA FARE) o riferimenti storici `ex-🟡` in testo di finding ✅ già chiusi.
Il corpus attivo delle 🟡 (16 voci) è rimasto invariato.
