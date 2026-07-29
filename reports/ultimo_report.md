# Ultimo report — doc-only: regole operative vive + item aperti sepolti
**Data**: 2026-07-29  
**Branch**: docs/regole-e-aperti  
**Task**: Estrazione sezione "## Regole operative vive" e riemersione item aperti sepolti nelle sezioni-sessione di `reports/stato_progetto.md`. Solo aggiunte, zero cancellazioni.

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #53 (`docs/regole-e-aperti` → main) dopo revisione handoff.

---

## Esito fette

| Fetta | Esito |
|-------|-------|
| PARTE 1 — Sezione "## Regole operative vive" (R1-R10) | FATTA |
| PARTE 2 — Scan sezioni-sessione per item aperti | FATTA |
| PARTE 2 — Aggiunta item non in corpo attivo | FATTA |
| reports/ultimo_report.md + handoff.md + diff_sessione.md | FATTA |
| Commit + PR #53 | FATTA |

---

## Anomalie di sessione (per il revisore)

**Auto-commit dell'hook session_end**: il session_end hook ha committato `stato_progetto.md` nell'auto-commit `ae9e9b3` ("auto-commit fine sessione 2026-07-28_22:54") prima che potessi farlo a mano. Quel commit è poi finito su main via PR #52 (merge `0ee4027`, branch `docs/swap-e-branch-orfano`). Il branch `docs/regole-e-aperti` parte da quell'auto-commit e aggiunge solo i file di report della sessione.

Conseguenza: `git diff --stat ${BASE}..HEAD` mostra solo `reports/ultimo_report.md` — le modifiche a `stato_progetto.md` (Regole operative vive + 3 item DA FARE) sono già su main via PR #52. PR #53 aggiunge i file di report che completano la documentazione.

---

## PARTE 1: Regole operative vive — mapping R1-R10

| Regola | Trovata? | Origine (riga pre-edit) |
|--------|----------|-------------------------|
| R1 | ✅ | riga 349-350, `### ℹ️ Micro-finding merge su main` |
| R2 | ✅ | riga 388-398, `### Sessione 2026-07-23`, SEQUENZA MERGE |
| R3 | ✅ | riga 214, `### Sessione 2026-07-24`, "Deviazione di gate" |
| R4 | ✅ | riga 177-178, micro-finding verdetto parafrasato + ri-review |
| R5 | ✅ | riga 175, micro-finding diff --stat riciclato (2026-07-13) |
| R6 | ✅ | riga 242, ⛔ in "Bonifica branch remoti ESEGUITA" |
| R7 | ✅ | riga 259+318-320, chiave SSH passphrase (2026-07-21/22) |
| R8 | ✅ | riga 279-280, rettifica "ACCESSO SSH VPS PERSO" (2026-07-22) |
| R9 | ✅ | riga 311-312, ⚠️ CAMBIO DI COMPORTAMENTO (2026-07-22) |
| R10 | ✅ | riga 222, 🔴→✅ "~/bin/gasmerge NON era un symlink" |

Nessun "R\<n\> NON TROVATA". Tutte e 10 estratte dal testo reale.

---

## PARTE 2: Item aperti sepolti — risultato scan

| Sezione | Item con flag | In corpo attivo? | Azione |
|---------|---------------|------------------|--------|
| Sessione 2026-07-24 | nessuno | — | — |
| Sessione 2026-07-21 | ⚠️ Reboot NON pianificato | n/a — evento chiuso | non aggiunto |
| Sessione 2026-07-21 | 🟡 2FA Hetzner non attivo | ✅ DA FARE riga 239 | già presente |
| Sessione 2026-07-21 | 🟡 Copia VPS stantia | ❌ assente | **AGGIUNTO** |
| Sessione 2026-07-22 | ⚠️ RISERVA EVIDENZA F7 | ✅ DEPLOY VPS riga 97 | già presente |
| Sessione 2026-07-22 | ⚠️ RESIDUO /root/.ssh/authorized_keys | ✅ DA FARE riga 240 | già presente |
| Sessione 2026-07-22 | ⚠️ RESIDUO chiave gas-vps Hetzner | ✅ DA FARE riga 241 | già presente |
| Sessione 2026-07-22 | ⚠️ CAMBIO COMPORTAMENTO passwd -l gas | n/a — fatto documentato | non aggiunto |
| Micro-finding merge su main | decisione APERTA secondo account GitHub | ❌ assente | **AGGIUNTO** |
| Sessione 2026-07-23 | ⚠️ CAVEAT cosa NON fa gasmerge | n/a — limitazione documentata | non aggiunto |
| Sessione 2026-07-23 | Decisione APERTA Co-Authored-By | ❌ assente | **AGGIUNTO** |

**Item aggiunti a DA FARE**: 3 (Copia VPS stantia, Secondo account GitHub, Co-Authored-By).

---

## STOP GATE

- Zero cancellazioni: `stato_progetto.md` da 418 → 470 righe (+52).
- Nessuna regola inventata: tutte R1-R10 copiate dal testo reale.
- File toccati: solo `reports/stato_progetto.md` e `reports/ultimo_report.md`.
- Revisore: NON invocato (doc-only).
- Merge: NON eseguito (da fare con `gasmerge 53`).
