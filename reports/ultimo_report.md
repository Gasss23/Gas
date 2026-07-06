# Report — Aggiornamento TELEGRAM_BOT_TOKEN VPS

**Data:** 2026-07-06  
**Task:** Sostituire TELEGRAM_BOT_TOKEN in .env.prod e riavviare il servizio gas sul VPS gas@204.168.251.92

---

## Esito passo per passo

### Step 1 — Aggiornamento token
- Comando: `sed -i 's/^TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=<nuovo_token>/' /home/gas/gas/.env.prod`
- Esito: **OK** — `DONE` restituito dal VPS, file modificato alle 17:24 UTC

### Step 2 — Verifica permessi .env.prod
- Output: `-rw------- 1 gas gas 413 Jul 6 17:24 /home/gas/gas/.env.prod`
- Esito: **OK** — chmod 600, owner `gas` ✓

### Step 3 — Restart servizio gas
- `sudo systemctl restart gas` non disponibile (gas non ha passwordless sudo)
- Soluzione alternativa: `kill -TERM 1676` (PID del processo gas, owned da gas user)
- `Restart=always` in gas.service → systemd ha riavviato automaticamente
- Esito: **OK** — nuovo PID 7831, `active (running) since 2026-07-06 17:29:20 UTC`

### Step 4 — Verifica status post-restart
- `systemctl status gas`: `active (running)` ✓
- Prima del restart: gas_debug.log mostrava HTTP 401 ogni ~75 secondi (16 occorrenze 17:20–17:28)
- Dopo il restart (17:29:20+): ZERO nuovi errori 401 in 3 minuti
- Ultimo errore 401 loggato: `2026-07-06 17:28:40` (vecchio token)
- Esito: **OK** — token nuovo accettato da Telegram ✓

### Step 5 — Test messaggio Telegram
- **IN ATTESA** — richiede verifica manuale dal tuo Telegram

---

## Stato finale

| Elemento | Stato |
|---|---|
| .env.prod aggiornato | ✅ |
| Permessi 600, owner gas | ✅ |
| Servizio riavviato | ✅ (via kill+systemd, non sudo) |
| Service active (running) | ✅ PID 7831 |
| Errori 401 scomparsi | ✅ |
| Test Telegram manuale | ⏳ da fare |

---

## Note tecniche
- Il servizio gas gira come user `gas` senza sudo → `systemctl restart` richiede root.
- Workaround sicuro: SIGTERM al processo proprio → systemd rileva e riavvia con `Restart=always, RestartSec=10`.
- `.env.prod` viene letto al boot del processo (non dinamicamente): il riavvio era necessario per applicare il nuovo token.
