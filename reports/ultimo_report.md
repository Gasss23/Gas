# Ultimo report — 2026-11-24 — Dashboard del CRM sempre accesa sul Mac

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta (solo script per il Mac e guida, nessun codice del motore).
2. Sul Mac, una volta sola dopo il merge: `cd ~/Gas && git pull && bash scripts/crm/installa.sh`; poi controllare che l'ultima riga stampata dica «Copia cifrata giornaliera fuori dal Mac: ATTIVA».
3. Da decidere: mettere `scripts/crm/` nel perimetro di review (come `scripts/voce/`), R-852M-2.
4. Dalla chat Voce (#400): controllare nel `.env` del Mac che non ci sia una vecchia `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8`.

## Esito
- **Richiesta dell'operatore** («vorrei mettere da qualche parte questa dashboard… che non dipenda da Claude o dall'IA… accessibile anche offline e in modo facile»): FATTA. `scripts/crm/com.gas.crm.plist` (LaunchAgent: parte all'avvio del Mac, si riavvia se si chiude), `scripts/crm/installa.sh` (controlla Mac, `.venv`, `GAS_CRM_TOKEN` e porta libera, carica il servizio, aspetta la risposta, mette l'icona «CRM Gas» sulla Scrivania senza il token), `scripts/crm/spegni.sh`. Guida aggiornata (`reports/crm/guida.md` §2).
- **Note del bot su 51d446c4** (APPROVATO CON RISERVE, check rosso per V-1 MEDIA): FATTE in 20791587. V-1 MEDIA attesa dopo il bootout e 3 tentativi di bootstrap (come lo script della voce provato sul Mac); V-2 cartella con soli caratteri sicuri; V-3 servizio tolto se la dashboard non parte e stop se `GAS_CRM_BIND` non è 127.0.0.1; V-4 `spegni.sh` toglie l'icona. Guida: il login va rifatto se il CRM si riavvia; controllo della copia cifrata dopo l'installazione.
- **Merge di main (PR #398, #399, #400 di altre chat) nel ramo**: FATTO (f4381a2e, review #852-MERGE APPROVATO CON RISERVE). Codice identico a main; decisioni e riserve della #400 riportate in `reports/stato_progetto.md`.
- La dashboard già non usava l'IA (solo «Riscrivi con Opus») e funziona senza internet.
- **PR #397**: MERGIATA il 23-11 (1b4954e2) col via dell'operatore; sul Mac il codice è aggiornato e il bot Telegram risponde («quanti clienti ho?» → zero, corretto).

## Test
- Nessun codice del motore toccato. `bash -n` sugli script, plist valido, prova del controllo del token e della porta col codice vero del CRM (senza token → stop; con token → porta 8770). Non provato su un Mac vero (launchctl, Scrivania): da qui non è raggiungibile.

## Riserve aperte
- Dalla PR #397: R-848-2 BASSA (il doctor non avvisa che col forte spento Gas resta muto), R-848-3 BASSA (lo «Sempre Opus» provato solo nella suite del kernel), V-3 BASSA della verifica esterna (commento di `importi_nel_testo` impreciso), cosmetiche #848. R-836-1 COSMETICA.
- Ereditate dalla chat Voce (in `reports/stato_progetto.md`).
