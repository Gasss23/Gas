# Ultimo report — 2026-11-24 — Dashboard del CRM sempre accesa sul Mac

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta (solo script per il Mac e guida, nessun codice del motore).
2. Sul Mac, una volta sola dopo il merge: `cd ~/Gas && git pull && bash scripts/crm/installa.sh`.

## Esito
- **Richiesta dell'operatore** («vorrei mettere da qualche parte questa dashboard… che non dipenda da Claude o dall'IA… accessibile anche offline e in modo facile»): FATTA. `scripts/crm/com.gas.crm.plist` (LaunchAgent: parte all'avvio del Mac, si riavvia se si chiude), `scripts/crm/installa.sh` (controlla Mac, `.venv`, `GAS_CRM_TOKEN` e porta libera, carica il servizio, aspetta la risposta, mette l'icona «CRM Gas» sulla Scrivania senza il token), `scripts/crm/spegni.sh`. Guida aggiornata (`reports/crm/guida.md` §2).
- La dashboard già non usava l'IA (solo «Riscrivi con Opus») e funziona senza internet.
- **PR #397**: MERGIATA il 23-11 (1b4954e2) col via dell'operatore; sul Mac il codice è aggiornato e il bot Telegram risponde («quanti clienti ho?» → zero, corretto).

## Test
- Nessun codice del motore toccato. `bash -n` sugli script, plist valido, prova del controllo del token e della porta col codice vero del CRM (senza token → stop; con token → porta 8770). Non provato su un Mac vero (launchctl, Scrivania): da qui non è raggiungibile.

## Riserve aperte
- Dalla PR #397: R-848-2 BASSA (il doctor non avvisa che col forte spento Gas resta muto), R-848-3 BASSA (lo «Sempre Opus» provato solo nella suite del kernel), V-3 BASSA della verifica esterna (commento di `importi_nel_testo` impreciso), cosmetiche #848. R-836-1 COSMETICA.
- Ereditate dalla chat Voce (in `reports/stato_progetto.md`).
