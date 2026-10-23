# ULTIMO REPORT — 2026-10-23 — Chat Mani, fetta 14: tempo riservato alla pulizia, grezzi autochiusi conformi (R6)

Ramo `feat/mani-web-fetta14` da main b3f04d9 (dopo il merge di #255 e #256). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 14: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve252-2 e R-ve255-1 (BASSE, XHTML malformato)**: estendere «il resto della pagina se ne va» a tutto l'XHTML malformato (più sicuro, si perde testo)? Decidi tu.
3. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un vero costruttore HTML5 (es. lexbor): decidi tu.
4. Rete più corta: i siti lenti ora vanno in timeout a 12 s invece che a 15 (per tenere il totale nei 15 s). Se preferisci 15 s di rete e un totale fino a ~18 s, dimmelo.
5. Decisione aperta dell'altra chat (R2, A/B): vedi `reports/stato_progetto.md` e `reports/r2_regole_abbonamento.md` (V-3 bot #255).
6. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **R-ve235-5 (pulizia fuori dai 15 s, BASSA)**: `FATTA` (rete 12 s + 3 s di riserva).
- **R-496-1 (docstring, COSMETICA)**, **R-496-2 (errore della pulizia chiamato tempo superato, BASSA)**: `FATTA`.
- **R-447-1 parte (b)**: chiusa come conforme ai browser, con test.
- **V-2 bot #255 bis (eccezioni dei thread nel test, COSMETICA)**: `FATTA`.
- **R-ve255-1**: registrata (decisione insieme a R-ve252-2).
- **Test**: web suite 383 → 388 (Python 3.13 e 3.11; col parser vecchio 379 passati e 10 saltati apposta). Mutazioni nuove (senza riserva, flag della pulizia mai spento): prese.
- **Review**: #496 APPROVATO CON RISERVE, #497 APPROVATO (chat Mani): verdetti integrali nell'handoff.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…14»).
