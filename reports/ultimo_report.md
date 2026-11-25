# Ultimo report — 2026-11-25 — Scheda clienti da leggere offline

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta (codice del CRM e `requirements.txt`; il bot dà `neutral` se tocca la sua macchina, altrimenti decide il verdetto).
2. Sul Mac, dopo il merge: `cd ~/Gas && git pull && source .venv/bin/activate && pip install -r requirements.txt`; nel `.env` aggiungere `GAS_CRM_SCHEDA_PASSWORD=` con una password NUOVA di almeno 16 caratteri (diversa da quella delle copie) e salvarla nel gestore di password; poi `python -m modules.crm scheda --forza`.
3. Sull'iPhone: app File → iCloud Drive → «Gas CRM (copie cifrate)» → tieni premuto «Scheda clienti.pdf» → «Mantieni scaricato»; aprirla una volta con la password per provarla.
4. Dalla fetta di ieri (se non già fatto): `bash scripts/crm/installa.sh` e `bash scripts/crm/telefono.sh` con l'app Tailscale su Mac e telefono.
5. Dalla chat Voce (#405, regola 3): scelta tra modello italiano e hey_jarvis, licenza CC BY-NC-SA, prova sul Mac (in `reports/stato_progetto.md`).

## Esito
- **Richiesta dell'operatore** («per forza tailscale? … posso accederci eventualmente offline … mi serve solo un dato al volo»; scelte: «Sì, fai la scheda» e «Scheda ora, modifiche col server»): FATTA, decisione 22.
  - `modules/crm/scheda.py` (nuovo): «Scheda clienti.pdf» protetta da password (AES-256) nella cartella iCloud delle copie cifrate; per cliente contatti, servizi e capitale, profitto del mese, ultimi 3 movimenti, promemoria. PDF scritto senza librerie esterne, cifrato con `pypdf`.
  - Si rifà solo quando cambiano i dati (impronta del contenuto), zero token; il server la rifà 2 minuti dopo l'ultimo cambio e la ricontrolla una volta al giorno, in un thread a parte.
  - Password solo sua (`GAS_CRM_SCHEDA_PASSWORD`, almeno 16 caratteri, diversa da quella delle copie: R-864-1 MEDIA chiusa), riletta dal `.env` a ogni scrittura (R-865-1 MEDIA chiusa).
  - Comando `python -m modules.crm scheda [--forza]`; guida e decisione 22 aggiornate.
- **Modifiche fatte senza connessione** (l'operatore le vuole salvate «al 100% senza errori»): NON in questa fetta, per scelta dell'operatore; si costruiscono col server di Gas (coda sul telefono, identificativo unico, rifiuti mostrati e mai persi).
- **Merge di main** (PR #405 Voce e #406): ramo riallineato con avanzamento veloce, nessun conflitto; riserve dell'ultimo verdetto del bot sulla #405 riportate in `reports/stato_progetto.md`.

## Test
- `pytest tests/test_unit_crm.py`: 195 → 211 passed (cifratura, nessun dato in chiaro nel file, password propria e diversa, rilettura del `.env`, riscrittura solo su cambio, temporanei, stornati e movimenti futuri esclusi, guardiano: riprova, mai due insieme, ricontrollo giornaliero). Mutanti dei punti critici presi dai test.
- Non provato su un iPhone vero né su iCloud vero.

## Riserve aperte
- R-866-1 BASSA, R-866-2 BASSA, R-864-7 BASSA, cosmetiche #864–#866 (in `reports/stato_progetto.md`).
- Dalle fette precedenti e dalle altre chat: in `reports/stato_progetto.md`.
