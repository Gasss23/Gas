# Ultimo report — 2026-08-06
## Task: Sanare stato_progetto.md — sonda F0, scope-creep #59, decisioni aperte

**Data:** 2026-08-06
**Branch:** docs/stato-fase3-sonda
**Commit di sessione:** 4c41b6b

---

## DECISIONI UMANE RICHIESTE

1. **Merge PR docs/stato-fase3-sonda** su main (dopo ispezione).
2. **🔴 Ruotare subito la chiave ElevenLabs** esposta in chat (registrata in stato_progetto.md §SICUREZZA). Verificare che non sia hardcoded in nessun file sotto `clients/`.

---

## §1 SCOPE & ESITO FETTE

**Fetta 1 — Annotare sonda F0 in "Prossimi passi" §4**: `FATTA`
- Aggiunta riga sotto il punto FASE 3: sonda atterrata su main (PR #59, merge 5323b9b, 2026-08-02), 6 script in `clients/voice/probe/`, con nota esplicita che sonda ≠ pipeline e FASE 3 resta DA COSTRUIRE.

**Fetta 2 — Note datate 2026-08-02 in "Note operative / finding"**: `FATTA`
- (a) Scope-creep PR #59: branch feature/voice-probe ha mescolato sonda voce F0 + allowlist gasmerge-ip; recidiva classe 2026-07-08.
- (b) Esito "6/6 verde" non verificato nel §1 del handoff (solo nel subject di commit 4056c97); da riconfermare prima di Fetta 1 FASE 3.

**Fetta 3 — Registrare decisioni aperte D1-ter / D2-audio / SICUREZZA**: `FATTA`
- D1-ter: IP WSL instabile tra reboot.
- D2-audio: load_dotenv override + policy device output.
- SICUREZZA: chiave ElevenLabs esposta in chat — 🔴 ruotare subito.

---

## Anomalie

- Nessun file motore toccato → revisore non richiesto.
- Solo `reports/stato_progetto.md` modificato (+8 righe, -1).
