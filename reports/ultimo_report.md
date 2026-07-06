# Report — Riallineamento CLAUDE.md sez. 10 (FASE 2.5 + FASE 5)

**Data:** 2026-07-06  
**Scope:** doc-only, sez. 10 CLAUDE.md — SOLO lista fasi (2 righe). Nessuna modifica al motore. Niente revisore, niente test.  
**Branch:** `docs/riallineamento-sez10-fase25-fase5`

---

## Fonti consultate (live)

- `reports/stato_progetto.md` — fonte primaria (aggiornato 2026-07-04)
- `reports/roadmap.md` — fonte secondaria

---

## Modifiche apportate

### 1. FASE 2.5 — da "futura" a ✅ CHIUSA

**Prima:**
```
- FASE 2.5 — Summarizzazione cronologia (compressione .gas_history.json h24) — futura
```

**Dopo:**
```
- FASE 2.5 — Summarizzazione cronologia (compressione .gas_history.json h24) — ✅ CHIUSA (2026-06-27, review #39, commit 65c4c7b)
```

**Fonte:** `stato_progetto.md` riga 12: `✅ FASE 2.5 compressione history (2026-06-27, review #39, commit 65c4c7b)`  
**Valori attesi dall'utente:** review #39 ✅, nessuna divergenza.

---

### 2. FASE 5 — da "futura" a 🟡 IN CORSO

**Prima:**
```
- FASE 5 — Deploy VPS Hetzner h24 + backup off-machine + process management (systemd + self-healing) — futura
```

**Dopo:**
```
- FASE 5 — Deploy VPS Hetzner h24 + backup off-machine + process management (systemd + self-healing) — 🟡 IN CORSO (S1 ✅ 2026-07-04, S1b ✅ 2026-07-04, prossimo S2)
```

**Fonte:** `stato_progetto.md` header riga 4 + riga 76:  
- Header: `Ultimo aggiornamento: 2026-07-04 (S1 ✅, S1b ✅)`  
- Riga 76: `FASE 5 S1 ✅ e S1b ✅ completati (2026-07-04) → prossimo S2 (decide operatore)`

---

## Discrepanza rilevata nel file canonico (SEGNALAZIONE — nessuna azione)

`stato_progetto.md` contiene un'incoerenza interna su S1b:
- **Riga 4 (header) e riga 76 (prossimi passi):** `S1b ✅` — confermato completato il 2026-07-04
- **Riga 118 (Note operative VPS):** `"S1b: da confermare in dettaglio — dati da integrare"`

La riga 118 suggerisce che S1b sia stato eseguito ma non ancora documentato nella sezione dettagli VPS. Si è scelto di usare lo stato della riga 76 per CLAUDE.md. Nessuna correzione apportata a `stato_progetto.md` (fuori scope).

**Divergenza vs atteso dall'utente:** l'utente indicava "S1b ✅ swap+systemd" come contenuto atteso — il file canonico non specifica i dettagli di S1b nella riga di sintesi (solo `S1b ✅`). I dettagli "swap+systemd" NON compaiono nella riga di sintesi. Si è usato solo `S1b ✅ 2026-07-04` senza aggiungere dettagli non verificabili dalla riga di sintesi.

---

## Derive rilevate FUORI SCOPE (proposte per l'umano)

Rilevate ma **non corrette** — decisione all'umano:

**A. `reports/roadmap.md` — FASE 2.5 ancora descritta come futura**  
Sezione `🟡 PROSSIMI PASSI` riga 32 elenca ancora FASE 2.5 come da fare. Sezione dettaglio `🗂️ FASE 2.5` (righe 44-52) non ha marcatura ✅. Va riallineata.

**B. `reports/roadmap.md` — paragrafo `Completati (storico)` non include FASE 2.5 né S1/S1b di FASE 5.**

**C. `stato_progetto.md` riga 118 — S1b "da confermare in dettaglio"**  
Incoerenza interna: header + riga 76 dicono S1b ✅, riga 118 dice "da confermare". Andrebbe aggiornata con i dati reali di S1b.

**D. CLAUDE.md sez. 10 — "Item aperti TOP" potenzialmente non aggiornati**  
Item 1 (spesa token) e item 2 (Telegram) nella lista non riflettono la riclassificazione 🔴/🟡 di `stato_progetto.md`. Fuori scope (la consegna vieta di toccare quella lista).

---

## Verifica finale

Righe toccate in CLAUDE.md: **2** — solo le due righe della lista fasi in sez. 10.  
Lista "Item aperti TOP": **non toccata**.  
Altre sezioni: **non toccate**.
