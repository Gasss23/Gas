# Ultimo report — 2026-11-20 — CRM fetta 7: note della PR #386 e del bot sulla PR #387 chiuse

## DECISIONI UMANE RICHIESTE
1. Merge della PR #387: l'operatore ha già dato il via («mergia quando è tutto verde»). La mergia l'agente con CI verde e bot senza finding ALTA/MEDIA.
2. Password delle copie cifrate nel `.env` del Mac (`GAS_CRM_BACKUP_PASSWORD`, almeno 12 caratteri), salvata anche nel gestore di password; poi `pip install -r requirements.txt` una volta.
3. Controllare che la cartella di Gas sia `~/Gas` (`pwd`), fuori da Scrivania e Documenti sincronizzate.
4. Secondo passaggio nella chat claude.ai col link della PR #387 (fetta che tocca la riservatezza delle copie dei clienti).

## Esito
- **PR #386 (copia cifrata su iCloud)**: MERGIATA il 20-11 (0aa26672) col via dell'operatore.
- **Fetta 7 — note basse del bot e della verifica esterna sull'ultimo commit di #386, più R-820-1**: FATTA (99e0dcb8, review #821 APPROVATO CON RISERVE).
  - Disco esterno non collegato: non si crea più la cartella sul Mac (copia «riuscita» falsa).
  - Una copia locale rovinata non sostituisce la copia buona del giorno.
  - Temporaneo del ripristino con nome unico e creazione esclusiva; file di lavoro come collegamento pendente rifiutati; prove interrotte ripulite.
  - Prova all'avvio con un tempo massimo di 5 secondi.
  - Guida: niente promessa «spariscono dopo 30 giorni».
- **Correzione #822 — R-821-1 e punto di mount vuoto**: FATTA (4a442c4f, review #822 APPROVATO).
  - Se fallisce la copia sul Mac, l'indicatore diventa rosso e parte l'avviso anche con la copia esterna spenta.
  - Un disco esterno staccato il cui punto di mount resta in `/Volumes` come cartella vuota viene riconosciuto («non è collegato»).
- **Correzione #823 — V-1 MEDIA e V-2 del bot su #387 (b098adf1)**: FATTA (2b4d32f2, review #823 APPROVATO).
  - Permesso negato sulla cartella delle copie (es. macOS che blocca iCloud Drive): non rompe più la copia e non fa più dire «ATTIVA» all'avvio.
  - Il controllo di integrità apre il database in sola lettura: un percorso sbagliato non crea più un file vuoto.
  - Collegamento simbolico verso `/Volumes` o «/volumes» minuscolo: ora controllati (nota del revisore #822).
- **Regola nuova in CLAUDE.md** (operatore, 20-11): non fermarsi ad aspettare il merge.

## Test
- `tests/test_unit_crm.py`: 131 su main 0aa26672 → 136 passed. Ogni test nuovo fallisce sul codice di prima della sua correzione.
- mypy: 0 errori in `modules/crm`. Kernel non toccato.

## Riserve aperte
- Non verificabili qui (non c'è un Mac): comportamento vero di `os.path.ismount` sui dischi esterni di macOS e del blocco dei permessi su iCloud Drive.
- R-810-2 (filtro delle parole vietate: falsi allarmi e forme non in lista), R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4: vedi `reports/stato_progetto.md`.
