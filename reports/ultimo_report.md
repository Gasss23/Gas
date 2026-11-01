# ULTIMO REPORT — 2026-11-01 — Mani: sandbox del browser con radice vuota ed elenco di cartelle permesse (R6, fetta 35, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #317 (numero nell'handoff §0): solo con verdetto del bot APPROVATO pulito la faccio io; con riserve serve il sì dell'operatore (anche tramite M1).
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.
3. Il browser resta SPENTO. Per accenderlo sul VPS manca la seconda condizione della roadmap: una prova dal vero sul VPS (bwrap con --size, AppArmor, node, Playwright, HTTPS).

## Esito
- **PR #316 (bwrap per il browser)**: MERGIATA (87f576c) col sì dell'operatore.
- **Radice vuota ed elenco di cartelle permesse** (prima condizione della roadmap): FATTA (PR #317).
- **V-6 ve e V-2 bot #316** (cartelle non nascoste leggibili): FATTA. **V-1 bot #316** (~/.local): FATTA. **R-605-1**: FATTA. **R-601-1/2**: FATTA. **R-603-1/2/3**: FATTA. **V-1 d ve #316** (routeWebSocket): FATTA.
- **V-1 c ve #316** (serviceWorkers 'block' senza test): SALTATA — nella prova la pagina non diventa sicura (navigator.serviceWorker non c'è), il test passerebbe a vuoto; resta dichiarata.
- **Review #607 (chat Mani)**: APPROVATO CON RISERVE. R-607-1 MEDIA (il test accettava tutto /gas/), R-607-2 e R-607-3 BASSE: FATTE. **Review #608**: APPROVATO.
- **Bot e verifica esterna su 427e57d**: APPROVATO CON RISERVE. V-1 MEDIA ve (/dev scrivibile senza tetto) e V-2 ve / V-1 bot (permessa-collegamento): FATTE (505479f, review #609 APPROVATO CON RISERVE). V-3 BASSA ve: SALTATA — dichiarata. R-609-1/2: DEFERITA — registrate.

## Prove
- Prototipo provato prima del codice: Chromium parte con l'elenco.
- Browser 43 test (anche da utente nobody), web (`python -m pytest tests/test_unit_web_*.py`): 751 passed, 2 skipped.
- Mutanti presi: 14 (vedi handoff §5).

## Anomalie
- Nel container restano due cartelle di prova di una verifica esterna precedente (/home/runnerx, /data/gashome), la cui rimozione è stata bloccata da un controllo di sicurezza; il nuovo test le copre: fuori dall'elenco non si vedono.
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
