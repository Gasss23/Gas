# ULTIMO REPORT — 2026-10-23 — Chat Mani, fetta 13: riserve minori della #252, titolo XHTML annidato (R6)

Ramo `feat/mani-web-fetta13` da main 0d70e82 (dopo il merge di #252 e #253). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 13: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve252-2 (BASSA, preesistente)**: estendere «il resto della pagina se ne va» a tutto l'XHTML malformato (più sicuro, si perde testo)? Decidi tu.
3. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un vero costruttore HTML5 (es. lexbor): decidi tu.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **V-2 bot #252 / V-4 ve #252 (avviso del parser vecchio, COSMETICA)**: `FATTA`.
- **V-1 ve #252 quater (test sulle virgolette nel DOCTYPE, BASSA)**: `FATTA`.
- **R-456-2 (commento, COSMETICA)**: `FATTA`.
- **R-ve245-5 (titolo XHTML annidato, BASSA)**: `FATTA`.
- **Test**: web suite 377 → 380 (Python 3.13 e 3.11; col parser vecchio 371 passati e 10 saltati apposta). Mutazioni nuove (titolo booleano, avviso sempre scritto, virgolette fuori dichiarazione): tutte prese.
- **Review**: #492 APPROVATO (chat Mani): verdetto integrale nell'handoff.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…13»).
