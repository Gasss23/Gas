# Ultimo report — 2026-11-20 — CRM fetta 8: note basse sulle PR #387 e #388 chiuse

## DECISIONI UMANE RICHIESTE
1. Merge della PR #388 (dopo il nuovo giro del bot sul merge di main 7d6a6865): le riserve aperte sono solo BASSE o cosmetiche. Il bot aveva dato APPROVATO CON RISERVE su 0d946f08 e su 7cd7a2f0 (note chiuse in a565c7b6 e b0174be5): serve il sì dell'operatore in chat, salvo un verdetto del bot pulito sul nuovo head.
2. Password delle copie cifrate nel `.env` del Mac (`GAS_CRM_BACKUP_PASSWORD`, almeno 12 caratteri), salvata anche nel gestore di password; poi `pip install -r requirements.txt` una volta.
3. Controllare che la cartella di Gas sia `~/Gas` (`pwd`), fuori da Scrivania e Documenti sincronizzate.
4. Secondo passaggio nella chat claude.ai col link della PR #387 e di questa PR (riservatezza delle copie dei clienti).

## Esito
- **PR #389 (correzione del bot)**: MERGIATA il 20-11 (09e112f5). Il bot sulla #388 aveva dato rosso per errore: leggeva «Non bloccante» come gravità MEDIA. Main portato nel ramo della #388 (merge 7d6a6865, review #833 APPROVATO) per un nuovo giro del bot.
- **PR #387**: MERGIATA il 20-11 (d03e5bf2) col via dell'operatore («mergia quando è tutto verde»): CI verde, bot e verifica esterna APPROVATO CON RISERVE senza finding ALTA/MEDIA.
- **Correzione #824/#825 — note basse di bot e verifica esterna su d809f5f1**: FATTA (d62adafb, review #824 e #825 APPROVATO CON RISERVE).
  - Un ripristino interrotto (kill, Mac spento) non lascia più per sempre il file in chiaro accanto alla destinazione: al ripristino seguente si tolgono quelli dei processi morti. Mai i collegamenti simbolici, mai quelli di altre destinazioni.
  - Cartella delle copie mai creata: il motivo dice «creala, o collega il disco», non più solo «disco non collegato?».
  - A copia esterna spenta, motivo e avviso non parlano più di «fuori dal Mac» o «iCloud».
- **Correzione #826/#827 — riserve #825**: FATTA (a9dbf6be). Review #826 BOCCIATO, poi #827 APPROVATO.
  - Con `GAS_CRM_BACKUP_CIFRATO_DIR` scritta male («~utente» inesistente) o con iCloud Drive bloccato da macOS il CRM ora parte; la copia si vede in rosso.
  - La bocciatura #826: con una cartella senza «/» le copie sarebbero finite nella cartella di lavoro. Ora i percorsi non completi vengono rifiutati.
  - Avviso della copia sul Mac fallita: solo il motivo, senza «iCloud» fisso né «non è riuscita» ripetuto.
- **Guida**: `GAS_CRM_BACKUP_CIFRATO_DIR` deve essere un percorso completo.
- **Correzione #828/#829 — note BASSE del bot sulla PR #388 (0d946f08)**: FATTA (a565c7b6, review #828 e #829 APPROVATO CON RISERVE).
  - Se macOS nega a Gas la lettura o la scrittura di iCloud Drive, il motivo (all'avvio, in dashboard e nell'avviso) dice cosa fare: dare l'accesso ai file all'app da cui si avvia il CRM, oppure impostare un'altra cartella.
  - Il file in chiaro di un ripristino interrotto viene tolto anche quando la destinazione esiste già.
  - R-829-1 (test per gli errori diversi dal permesso negato) chiusa in b0174be5.
- **Correzione #830 — note del bot sulla PR #388 (7cd7a2f0)**: FATTA (b0174be5, review #830 APPROVATO CON RISERVE).
  - I resti in chiaro di un ripristino interrotto più vecchi di un'ora si tolgono qualunque sia il numero del processo (dopo un riavvio può essere riassegnato).
  - Il consiglio su iCloud vale anche se la cartella ci arriva da un collegamento o con maiuscole diverse.
  - Resta R-830-1 BASSA: entro un'ora dal riavvio il resto può restare; la guida dice di cancellarlo a mano.

## Test
- `tests/test_unit_crm.py`: 136 su main d03e5bf2 → 138 passed (i test di a565c7b6 estendono quelli esistenti). I test nuovi falliscono sul codice di prima della loro correzione.
- mypy: 0 errori in `modules/crm`. Kernel non toccato.

## Riserve aperte
- Non verificabili qui (non c'è un Mac): comportamento vero di macOS che blocca iCloud Drive e di `os.path.ismount` sui dischi esterni.
- R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4: vedi `reports/stato_progetto.md`.
