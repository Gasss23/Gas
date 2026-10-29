# ULTIMO REPORT — 2026-10-29 — Mani: decisioni dell'operatore su R-ve235-7 e tempo di rete 12 s (R6, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (numero nell'handoff §0): solo report; lo faccio io con verdetto del bot APPROVATO pulito, con riserve aspetto il tuo OK.
2. Prossimi argomenti della chat Mani: da scegliere. Restano tre riserve BASSE aperte (R-518-1, R-516-1, R-ve277-5 parte leggi.py, in stato_progetto e in ripartenza_mani).
3. Proposta di coordinamento della chat Motore 1 (scritta in stato_progetto, blocco «Mani — fetta 26»): da confermare.

## Esito
- **PR #300**: MERGIATA su richiesta dell'operatore («mergia 300», ed777ef). Bot su 69fd75e APPROVATO CON RISERVE: V-1 COSMETICA (l'handoff della #300 diceva la V-1 della verifica esterna #298 corretta «in ultimo_report e in stato_progetto», ma in stato_progetto non c'era niente da correggere): FATTA — la correzione dei «sei casi» sta solo in `reports/ultimo_report.md` della #300.
- **R-ve235-7**: CHIUSA come accettata (decisione dell'operatore: «chiudi R-ve235-7 come accettata»). Il DNS di sistema non si interrompe: compromesso dichiarato.
- **Tempo di rete 12 s**: CONFERMATO (decisione dell'operatore: «tempo di rete 12 s va bene»).
- **Ripartenza e stato**: FATTA — `reports/ripartenza_mani.md` e `reports/stato_progetto.md` aggiornati.
- **Bot su 251b0c2 (PR #301)**: APPROVATO CON RISERVE. V-1 BASSA («nessun lavoro aperto» falso: restano R-518-1, R-516-1, R-ve277-5 parte leggi.py e il punto b della ripartenza) → FATTA: elencate in ripartenza_mani, stato_progetto e handoff §7. V-2 COSMETICA (la proposta di coordinamento non stava nel repo) → FATTA: scritta in stato_progetto.
- **Bot su 604edcb (PR #301)**: APPROVATO CON RISERVE. V-1 BASSA (descrizione della PR vecchia) → FATTA, descrizione aggiornata. V-2 COSMETICA (mancavano V-1 ve/bot #288 e R-546-1 nella lista delle aperte) → FATTA.
- **Codice**: nessuna modifica.

## RICHIESTE ALLA CHAT MOTORE
1. `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (R-ve280-1), poi `GAS_WEB_LEXBOR=1` sul VPS.
2. R-546-1: numeri delle review doppi tra le chat.
3. `scripts/bot_esito.py` boccia il verdetto quando il bot stesso scrive un carattere Cf citando il codice.
4. Sul VPS serve libexpat ≥ 2.4 perché il taglio dell'XHTML sia attivo; un controllo nel doctor.

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
