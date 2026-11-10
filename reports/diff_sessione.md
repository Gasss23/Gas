# Diff della sessione — 2026-11-10 — chat Mani, richiesta d'un fiato

File toccati (base main a0c200c, dopo il merge della PR #361):
- `clients/voice/ascolto.py`: `_voce_subito` (SUBITO_S 0,6 s, SUBITO_VOCE_S 0,4 s) prima della conferma; `subito_s` nel costruttore (default 0) e in main; log della richiesta con voce e volume; `registra(subito=True)` invia solo se dopo i blocchi iniziali arriva altra voce continua (V-1 verifica esterna #368).
- `tests/test_unit_voce_ascolto.py`: 9 test nuovi e il controllo di main.
- `scripts/voce/LEGGIMI.md`: paragrafo «Richiesta d'un fiato».
- `.claude/agents/memoria_revisore.md`: righe #753-M1, #754-M1, #755-M1 e lezione.
- `reports/*`: report di fine task e voce in stato_progetto.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
