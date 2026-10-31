# ULTIMO REPORT — 2026-10-31 — Mani: browser senza schermo dietro il proxy filtrante (R6, fetta 33, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #315 (numero nell'handoff §0): solo con verdetto del bot APPROVATO pulito la faccio io; con riserve serve il sì dell'operatore (anche tramite M1).
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.
3. Il browser resta SPENTO: accenderlo sul VPS (`GAS_WEB_BROWSER=1`) solo dopo l'isolamento bwrap (punto 4 del piano), perché Chromium gira senza sandbox.

## Esito
- **PR #312 (proxy filtrante)**: MERGIATA (01eba0d), auto-merge col sì dell'operatore tramite M1; prima unito main 3a38e75, review #592 APPROVATO.
- **Browser senza schermo** (`modules/web/browser.py`, punti 1, 3, 5, 6, 7 del piano): FATTA (PR #315). Spento per default (`GAS_WEB_BROWSER=1`).
- **Punto 4 (bwrap)**: DEFERITA — fuori scope, dichiarato come limite.
- **«Lo chiede Gas» (parametro dello strumento in gas.py)**: DEFERITA — gas.py lasciato a dopo, decisione di M1.
- **Riserve del proxy**: R-585-4, R-585-5, V-4 bot #312, V-2 bot #312 su 805b4d8 FATTE; V-2 bot #312 su 3a31a99 (numero vecchio nell'handoff) FATTA, l'handoff è riscritto.
- **ci.yml**: FATTA — solo env del passo web, autorizzato da M1.
- **Review #593 (chat Mani)**: APPROVATO CON RISERVE. R-593-1 MEDIA (Chromium vivo dopo il kill del gruppo di node): FATTA. R-593-2..6 BASSE: FATTE (la 3 su https e la 6 dichiarate come limiti).
- **Review #594**: APPROVATO CON RISERVE. R-594-1 (test diretto dell'uccisione) FATTA; R-594-2 DEFERITA — dichiarata; R-594-3 FATTA.
- **Review #595**: APPROVATO CON RISERVE. R-595-1 e R-595-2 BASSE: DEFERITA — registrate.
- **Merge di origin/main 9fdbd2b (PR #314 di M2)**: FATTA — conflitto solo nella memoria. Review #596 APPROVATO CON RISERVE (R-596-1: riserve nello stato, FATTA qui).

- **Gate IP al primo fine-task**: fermo su IP di esempio; FATTA — marcatore nel test (review #597 APPROVATO) e nella memoria, <IP-redatto> nei verdetti incollati nell'handoff.

## Prove
- Browser 25 test, proxy 71 test. Web (`python -m pytest tests/test_unit_web_*.py`): 732 passed, 2 skipped. Web + voce dopo il merge: 870 passed, 2 skipped.
- Mutanti presi: senza `<-loopback>`, senza lo script che spegne WebSocket/RTC, senza il controllo X-Gas-Proxy, senza lo split su «\n», senza i gruppi col segno. Non preso dal test con Chromium: senza la riscrittura della risposta (lo prende il test unitario del proxy).

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
- Chromium qui non riusa la connessione del proxy nemmeno senza la riscrittura: il test end-to-end di R-585-4 da solo non morde.
