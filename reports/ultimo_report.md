# ULTIMO REPORT — 2026-10-24 — Chat Mani, fetta 15: </template> sopra svg/math come il browser (R6)

Ramo `feat/mani-web-fetta15` da main 172c2d7 (dopo il merge di #257). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 15: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve252-2 e R-ve255-1 (BASSE, XHTML malformato)**: estendere «il resto della pagina se ne va» a tutto l'XHTML malformato? Decidi tu.
3. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un vero costruttore HTML5 (es. lexbor): decidi tu. Con questa fetta si vede anche dopo un template chiuso.
4. Rete a 12 s invece di 15 (fetta 14): confermi?
5. **R-ve235-7**: proposta di chiuderla come compromesso accettato (il DNS di sistema non si può interrompere; al massimo 4 risoluzioni appese).
6. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **R-469-1 (`</template>` sopra svg/math, perdita)**: `FATTA`, con **B-500-1** (ALTA, trovata dal revisore nella prima versione): `FATTA`.
- **V-1 ve #257 (test dei redirect rotti, BASSA)**: `FATTA`.
- **V-1 bot / V-2 ve #257 (commento di TIMEOUT_TOTALE, COSMETICA)**: `FATTA`.
- **Test**: web suite 388 → 405 (Python 3.13 e 3.11; col parser vecchio 396 passati e 10 saltati apposta). Oracolo lexbor su ~5 milioni di pagine: 0 perdite nuove, 0 fughe nuove (4 casi R-ve246-5 resi visibili, già su main senza prefisso). Mutazioni: tutte prese.
- **Review**: #500 BOCCIATO, #501 APPROVATO (chat Mani): verdetti integrali nell'handoff.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…15»).
