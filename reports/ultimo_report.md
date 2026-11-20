# Ultimo report — 2026-11-19/20 — CRM: copia cifrata su iCloud Drive, giro 2 volte al giorno, parole vietate

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta. Riserve: R-816-1 COSMETICA. Fetta di sicurezza (cifratura dei dati dei clienti): secondo passaggio nella chat claude.ai col link della PR.
2. Password delle copie cifrate: scriverla nel `.env` del Mac (`GAS_CRM_BACKUP_PASSWORD`, almeno 12 caratteri) e salvarla anche nel gestore di password. Senza di lei le copie su iCloud non si aprono.
3. Controllare che la cartella di Gas sia `~/Gas`, fuori da Scrivania e Documenti: se quelle sono sincronizzate con iCloud, il database in chiaro finirebbe su iCloud.
4. Server gratuito per avere il CRM dal telefono (Tailscale col Mac acceso, oppure Oracle Cloud «Always Free»): da decidere. Per ora il CRM resta sul Mac.

## Esito
- **PR #381 (CRM, fette 1-5)**: MERGIATA il 19-11 (12633cb0), col via dell'operatore. CI verde e bot APPROVATO CON RISERVE senza finding ALTA/MEDIA.
- **Fetta 6 — copia cifrata fuori dal Mac** (decisione del 19-11): FATTA, commit 32282b6f.
  - Nuovo `modules/crm/copia_cifrata.py`: ogni giorno una copia CIFRATA in iCloud Drive (cartella «Gas CRM (copie cifrate)», ultime 30).
    - Cifratura Fernet, con la chiave ricavata dalla password con scrypt n=2^17.
    - Senza password, senza iCloud o senza la libreria `cryptography`: spenta, mai in chiaro.
  - Comando `python -m modules.crm ripristina FILE`:
    - non sovrascrive mai un database esistente;
    - rifiuta se sono rimasti file di lavoro di un crash;
    - ricontrolla l'integrità alla fine.
  - All'avvio, `serve` dice se la copia è ATTIVA o SPENTA. Libreria `cryptography` aggiunta ai requisiti.
  - Review #815 APPROVATO CON RISERVE (R-815-1 MEDIA: ripristino con un file di lavoro rimasto) → #816 APPROVATO CON RISERVE (R-815-1..4 chiuse; R-816-1 COSMETICA).
- **Giro del motore 2 volte al giorno** (decisione del 19-11): FATTA. Default `GAS_CRM_SCAN_MINUTI` = 720. Restano il giro subito a ogni modifica e il pulsante «Scansiona». Il giro non usa token.
- **Parole vietate più ampie** (rimandate alla fetta successiva il 19-11): FATTA. Radici «garant», «assicur», «al sicuro», «alcun/nessun rischio», «ultima occasione», «posti limitati»… Spazi doppi tolti.
- **Docstring del pacchetto CRM** (V-1 del bot): FATTA.
- **Server per il CRM**: DEFERITA. L'operatore non vuole spendere per un server solo per il CRM; alternative gratuite da decidere (punto 4).

## Test
- `tests/test_unit_crm.py`: 125 passed. Su main falliscono i 6 test nuovi o cambiati; `test_r815_*` fallisce anche col `copia_cifrata.py` del giro #815.
- notte, voice_contesto, manutenzione e hooks: 468 passed. mypy: 0 errori in `modules/crm`. Kernel e gas.py non toccati.

## Riserve aperte
- R-816-1 COSMETICA:
  - la password digitata a mano non viene ripulita dagli spazi;
  - il ripiego senza collegamenti fisici non ha un test.
- R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4: vedi `reports/stato_progetto.md`.
