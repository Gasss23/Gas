# ULTIMO REPORT — 2026-10-30 — Mani: proxy filtrante per il browser senza schermo (R6, fetta 32, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #312 (numero nell'handoff §0): l'operatore ha detto «mergia #312» (riferito da M1); la PR era in conflitto con main dopo la #313, ora unita (826a9b1). M1 fa il merge appena la CI è verde.
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.

## Esito
- **PR #310**: MERGIATA (15c4da8). V-1 bot #310 BASSA (manca il test https sulla porta 80): FATTA (`test_https_sulla_porta_80`).
- **Proxy filtrante** (`modules/web/proxy.py`, prima fetta del browser senza schermo, piano approvato dall'operatore tramite M1): FATTA (PR #312).
- **Review #585 (chat Mani)**: BOCCIATO. B-585-1 MEDIA («CONNECT sito.test:80/:443» apriva un tunnel verso la porta 80): FATTA — «/?#\» rifiutati e porta riletta dopo urlsplit. R-585-2 (testa un byte alla volta), R-585-3 (`ferma()` non chiudeva i tunnel), R-585-6 (502 invece di 403): FATTE. R-585-4 e R-585-5 (confini della risposta; Chromium e il loopback, QUIC, WebRTC, prefetch): DEFERITE — fetta del browser.
- **Review #586**: APPROVATO CON RISERVE. R-586-1 BASSA (timeout corto della testa rimasto sul tunnel): FATTA. **Review #587**: APPROVATO.

- **Verifica esterna su 6ebecba (https://github.com/Gasss23/Gas/pull/312#issuecomment-6529640125)**: APPROVATO CON RISERVE, nessun bypass dei filtri. V-1 BASSA (§6 dell'handoff inesatto): FATTA. V-2 BASSA (PR in conflitto con main): FATTA — merge di main 1e8aff8, review #588 APPROVATO CON RISERVE. V-3 BASSA (client muto tenuto 10 s): FATTA — test nuovo, review #589 APPROVATO. V-4 COSMETICA (controllo irraggiungibile, difesa in profondità): SALTATA — voluto.

- **Bot su eea0ea0 (PR #312)**: APPROVATO CON RISERVE, check success. V-1 BASSA (a tetto dei byte superato, una richiesta nuova usciva ancora con URL e intestazioni): FATTA in b838f4d. V-2 BASSA (invii con timeout propri, oltre la scadenza del proxy): FATTA in b838f4d. V-3 COSMETICA (conteggi dei test nella descrizione): FATTA — descrizione e §5 aggiornati. V-4 COSMETICA (hop-by-hop nominati in «Connection» non tolti; non è un bypass): DEFERITA — registrata.
- **Review #590 (chat Mani)**: APPROVATO CON RISERVE (R-590-1 COSMETICA motivo del timeout, R-590-2 BASSA testa contata dopo l'apertura): FATTA tutte e due. **Review #591**: APPROVATO.
- **Bot su 805b4d8 (PR #312)**: APPROVATO CON RISERVE, check success, CI verde. V-1 BASSA (CI in corso alla verifica): FATTA — poi verde. V-2 COSMETICA (testa del CONNECT e risposta 200 fuori dal tetto dei byte, docstring «nei due versi»): DEFERITA — registrata.
- **Merge di origin/main 3a38e75 (PR #313 di M2, voce V4)**: FATTA in 826a9b1 — conflitti solo nei log di sessione e nella memoria. Review #592 (chat Mani) APPROVATO.

## Prove
- `tests/test_unit_web_proxy.py`: 55 passed (più run di fila); web 691 passed, 2 skipped. Web e voce dopo il merge di main: 815 passed, 2 skipped (review #588). Dopo il merge di main 3a38e75 (review #592): web 557 passed 1 skipped, voce 138 passed, browser 16 passed, hook 211 passed, kernel 1062 PASS / 1 FAIL (T31g, come su main).
- Mutanti presi: IP interni, tunnel su ogni porta e «:80/:443», upgrade, metodi, tetto dei byte, https in chiaro, Proxy-*, tempo della testa, `ferma()`, timeout rimasto.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
