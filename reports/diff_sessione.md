# Diff Sessione — 2026-08-02

Sessione: Allowlist IP privati gasmerge — aggiunta token `gasmerge-ip-ok` su ogni riga con IP privato.

---

## File toccati (da `git diff --cached --stat BASE` dopo stage)

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `clients/voice/probe/probe_bridge_server.py` | Token `# gasmerge-ip-ok` aggiunto in coda alle righe 9, 11, 70 (IP: 127.0.0.1, 0.0.0.0) per superare il guard `gasmerge.sh`. <!-- gasmerge-ip-ok --> |
| `clients/voice/probe/win_bridge_test.py` | Token `# gasmerge-ip-ok` aggiunto in coda alle righe 14, 15, 54, 86 (IP: 127.0.0.1, 172.28.16.1) per superare il guard `gasmerge.sh`. <!-- gasmerge-ip-ok --> |
| `reports/diff_sessione.md` | Questo file — riepilogo sessione (si riscrive a ogni sessione). |
| `reports/handoff.md` | Dossier sessione aggiornato; token `<!-- gasmerge-ip-ok -->` anche su riga 20 (IP: 127.0.0.1, 172.20.137.213). <!-- gasmerge-ip-ok --> |
| `reports/ultimo_report.md` | Report canonico task; token `<!-- gasmerge-ip-ok -->` su righe 24, 41 (IP: 127.0.0.1, 172.20.137.213). <!-- gasmerge-ip-ok --> |

---

## Note

- Nessun file motore (`gas.py`, `brains/`, `modules/`, `tests/`) toccato — revisore non richiesto.
- Verifica finale: `git grep -nE '\b[0-9]{1,3}(\.[0-9]{1,3}){3}\b'` — ogni riga restituita porta `gasmerge-ip-ok`.
- La storia completa sta in git; questo file è fotografia dell'ultima sessione.
