# ULTIMO REPORT — 2026-10-30 — Mani: proxy filtrante per il browser senza schermo (R6, fetta 32, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #312 (numero nell'handoff §0): solo con verdetto del bot APPROVATO pulito la faccio io; con riserve serve il sì dell'operatore (anche tramite M1).
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.

## Esito
- **PR #310**: MERGIATA (15c4da8). V-1 bot #310 BASSA (manca il test https sulla porta 80): FATTA (`test_https_sulla_porta_80`).
- **Proxy filtrante** (`modules/web/proxy.py`, prima fetta del browser senza schermo, piano approvato dall'operatore tramite M1): FATTA (PR #312).
- **Review #585 (chat Mani)**: BOCCIATO. B-585-1 MEDIA («CONNECT sito.test:80/:443» apriva un tunnel verso la porta 80): FATTA — «/?#\» rifiutati e porta riletta dopo urlsplit. R-585-2 (testa un byte alla volta), R-585-3 (`ferma()` non chiudeva i tunnel), R-585-6 (502 invece di 403): FATTE. R-585-4 e R-585-5 (confini della risposta; Chromium e il loopback, QUIC, WebRTC, prefetch): DEFERITE — fetta del browser.
- **Review #586**: APPROVATO CON RISERVE. R-586-1 BASSA (timeout corto della testa rimasto sul tunnel): FATTA. **Review #587**: APPROVATO.

- **Verifica esterna su 6ebecba (https://github.com/Gasss23/Gas/pull/312#issuecomment-6529640125)**: APPROVATO CON RISERVE, nessun bypass dei filtri. V-1 BASSA (§6 dell'handoff inesatto): FATTA. V-2 BASSA (PR in conflitto con main): FATTA — merge di main 1e8aff8, review #588 APPROVATO CON RISERVE. V-3 BASSA (client muto tenuto 10 s): FATTA — test nuovo, review #589 APPROVATO. V-4 COSMETICA (controllo irraggiungibile, difesa in profondità): SALTATA — voluto.

## Prove
- `tests/test_unit_web_proxy.py`: 51 passed (più run di fila). Web e voce dopo il merge di main: 815 passed, 2 skipped (review #588).
- Mutanti presi: IP interni, tunnel su ogni porta e «:80/:443», upgrade, metodi, tetto dei byte, https in chiaro, Proxy-*, tempo della testa, `ferma()`, timeout rimasto.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
