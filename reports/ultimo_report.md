# Ultimo report — 2026-11-25 — Dashboard del CRM anche dal telefono

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta (tocca `scripts/` e il codice del CRM: il bot dà `neutral`, decide l'operatore). È una fetta di sicurezza: secondo passaggio consigliato nella chat claude.ai.
2. Sul Mac, dopo il merge: installare l'app **Tailscale** (Mac App Store) e accedere; sul telefono la stessa app con lo **stesso account**; poi `cd ~/Gas && git pull && bash scripts/crm/telefono.sh`. La prima volta Tailscale può stampare un link per attivare HTTPS: aprirlo, premere «Enable» e rilanciare. Sul telefono aprire l'indirizzo stampato, inserire il token e salvarlo con Condividi → «Aggiungi alla schermata Home».
3. Restano da fare dalla fetta di ieri: `bash scripts/crm/installa.sh` sul Mac (se non già fatto) e il controllo del `.env` della voce (`GAS_ASCOLTO_SOGLIA_INTERRUZIONE`).

## Esito
- **Richiesta dell'operatore** («sì fallo, voglio vederla anche dal telefono. magari qua sul mac mettimi pure un collegamento diretto al desktop»): FATTA, decisione 21 in `reports/crm/decisioni.md`.
  - `scripts/crm/telefono.sh` (accendi / `spegni` / `stato`): collega il CRM alla rete privata Tailscale con `tailscale serve` (HTTPS, solo i dispositivi dell'account). Controlla che non ci sia un funnel pubblico e che la porta 443 non la usi altro; scrive `GAS_CRM_NOME_TAILSCALE` nel `.env`; riavvia il CRM; se qualcosa non va rimette tutto com'era.
  - `modules/crm/server.py`: oltre a localhost e IP accetta SOLO il nome `*.ts.net` del Mac, solo sulla 443; rifiuta ogni richiesta arrivata dal funnel (internet); cookie `Secure` da lì. Il CRM continua ad ascoltare solo su 127.0.0.1.
  - `scripts/crm/spegni.sh` spegne anche l'accesso dal telefono.
  - Il collegamento sulla Scrivania del Mac c'è già: l'icona «CRM Gas» la crea `installa.sh`.
  - Guida aggiornata (`reports/crm/guida.md` §2 e §6).
- Comandi di Tailscale controllati sul suo codice sorgente (v1.106.1): flag di `serve`, formato di `serve status --json`, Host conservato dal proxy, header del funnel.

## Test
- `pytest tests/test_unit_crm.py`: 173 → 195 passed (nomi Tailscale ammessi e rifiutati, funnel e porte rifiutati, cookie Secure, 20 casi di `telefono.sh`/`spegni.sh` con un Tailscale finto). Mutanti dei controlli di sicurezza tutti presi dai test.
- Non provato con un Tailscale vero, con launchd vero né con la bash 3.2 del Mac.

## Riserve aperte
- R-862-1 BASSA: manca un test per il ramo «configurazione illeggibile» dello spegni.
- COSMETICHE #860/#861/#862 (in `reports/stato_progetto.md`).
- Dalla PR #404: V-1/V-2 BASSE e V-3 COSMETICA del bot, V-1 BASSA della 3ª verifica esterna, R-859-1 BASSA, R-859-2 COSMETICA, R-854-2 BASSA (in `reports/stato_progetto.md`).
