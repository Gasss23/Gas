# Allowlist IP privati gasmerge — aggiunta token gasmerge-ip-ok

**Branch:** `feature/voice-probe`
**Data:** 2026-08-02
**Task:** Aggiunta token `gasmerge-ip-ok` su ogni riga con IP privato bloccata dal guard `scripts/gasmerge.sh`.

---

## DECISIONI UMANE RICHIESTE

1. **Merge PR #59 (`feature/voice-probe`):** la PR di sessione non è ancora mergiata su main — da fare dopo CI verde.

---

## §SCOPE & ESITO FETTE

| Fetta | Stato | Note |
|-------|-------|------|
| Analisi righe con IP privato da marcare | **FATTA** | Lettura di 5 file; IP target: 0.0.0.0, 127.0.0.1, 172.28.16.1, 172.20.137.213 |
| `probe_bridge_server.py` righe 9, 11, 70 | **FATTA** | Token `# gasmerge-ip-ok` aggiunto in coda a ciascuna riga |
| `win_bridge_test.py` righe 14, 15, 54, 86 | **FATTA** | Token `# gasmerge-ip-ok` aggiunto in coda a ciascuna riga |
| `reports/diff_sessione.md` riga 12 | **FATTA** | Token `<!-- gasmerge-ip-ok -->` aggiunto in coda alla riga |
| `reports/handoff.md` riga 20 | **FATTA** | Token `<!-- gasmerge-ip-ok -->` aggiunto in coda alla riga |
| `reports/ultimo_report.md` righe 24, 41 | **FATTA** | Token `<!-- gasmerge-ip-ok -->` aggiunto in coda a ciascuna riga |
| Verifica finale `git grep` | **FATTA** | Zero righe con IP privato senza token — output grezzo verificato |

---

## §ESITO VERIFICA

`git grep -nE '\b[0-9]{1,3}(\.[0-9]{1,3}){3}\b'` — ogni riga restituita porta `gasmerge-ip-ok`.
Righe già coperte (non toccate): `reports/stato_storico.md:503`, `tests/test_unit_gasmerge.py:282,298,364,369,389,399,407,417`.

---

## §NOTE OPERATIVE

- Nessun file motore toccato (`gas.py`, `brains/`, `modules/`, `tests/`) — revisore non richiesto.
- Il token `# gasmerge-ip-ok` nelle righe 9 e 11 di `probe_bridge_server.py` cade dentro il docstring; il guard `gasmerge.sh` cerca la stringa letterale sulla riga e la trova correttamente.
