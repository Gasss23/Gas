# Ultimo report — 2026-11-20 — CRM fetta 7: note basse della PR #386 chiuse

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta (numero nell'handoff dopo l'apertura).
2. Password delle copie cifrate nel `.env` del Mac (`GAS_CRM_BACKUP_PASSWORD`, almeno 12 caratteri), salvata anche nel gestore di password; poi `pip install -r requirements.txt` una volta.
3. Controllare che la cartella di Gas sia `~/Gas` (`pwd`), fuori da Scrivania e Documenti sincronizzate.

## Esito
- **PR #386 (copia cifrata su iCloud)**: MERGIATA il 20-11 (0aa26672) col via dell'operatore. CI verde e bot APPROVATO CON RISERVE senza finding ALTA/MEDIA.
- **Fetta 7 — note basse del bot e della verifica esterna sull'ultimo commit di #386, più R-820-1**: FATTA.
  - Disco esterno non collegato: non si crea più la cartella sul Mac (copia «riuscita» falsa).
  - Una copia locale rovinata non sostituisce la copia buona del giorno.
  - Temporaneo del ripristino con nome unico e creazione esclusiva: non segue collegamenti simbolici.
  - File di lavoro come collegamento pendente: rifiutati.
  - Prove di scrittura interrotte: ripulite.
  - Se fallisce la copia sul Mac, l'indicatore lo dice e parte l'avviso.
  - Prova all'avvio con un tempo massimo di 5 secondi.
  - Guida: niente promessa «spariscono dopo 30 giorni».
- **Regola nuova in CLAUDE.md** (operatore, 20-11): non fermarsi ad aspettare il merge; mentre una PR aspetta si prosegue col lavoro.

## Test
- `tests/test_unit_crm.py`: 133 passed. I 2 test nuovi falliscono sul codice di main 0aa26672.
- mypy: 0 errori in `modules/crm`. Kernel non toccato.

## Riserve aperte
- R-810-2 (filtro delle parole vietate: falsi allarmi e forme non in lista), R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4: vedi `reports/stato_progetto.md`.
