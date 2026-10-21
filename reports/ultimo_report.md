# ULTIMO REPORT — 2026-10-21 — Chat Mani, fetta 3: note della PR #237 (R6, PR #238)

Ramo `feat/mani-web-fetta3` (da main dopo il merge di #237). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. PR #238 (https://github.com/Gasss23/Gas/pull/238). Fetta di sicurezza. Operatore: «procedi con la fetta 3», «mergia quando il bot approva».

## DECISIONI UMANE RICHIESTE

1. Merge della PR #238: l'operatore ha chiesto in chat «mergia quando il bot approva»; l'agente la mergia con `verifica-bot` success, CI verde e nessuna riserva ALTA/MEDIA. (La regola di CLAUDE.md §10 per il merge autonomo senza richiesta vuole APPROVATO pieno; qui vale la richiesta esplicita dell'operatore.)
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

## Esito

- **Finti marcatori con separatori lunghi (R-410-1, V-1 bot #237)**: `FATTA` — tetto `{0,3}` solo sul prefisso; dopo le parole fisse `+`/`*` (lineari). Tornano neutralizzate «NON____FIDATO» e simili.
- **Ripiego senza parser (V-2 bot #237, R-429-1)**: `FATTA` — via anche script, style, noscript e template (algoritmo lineare; minuscole solo ASCII perché `lower()` cambia la lunghezza con «İ»); riferimenti interpretati con html.unescape dentro un try. Il titolo nel ripiego si perde (dichiarato).
- **DNS saturo (V-3 bot #237)**: `FATTA` — motivo «troppe risoluzioni DNS in corso: tempo massimo superato».
- **Test a tempo veri (R-410-2, R-429-2)**: `FATTA` — eseguiti in un sottoprocesso con timeout: una regressione quadratica fa fallire il test in ~10 s invece di bloccare la suite (un thread con join non basta: la regex tiene il GIL).
- **Test dei rami difensivi (V-1 verifica esterna #237)** e **`server_close` (V-4 bot #237)**: `FATTA`.
- **R-ve235-5**: `DEFERITA` — resta un limite DICHIARATO, non chiuso (nel report della fetta 2 era scritto «chiusa»: corretto qui e in `reports/stato_progetto.md`).
- **Test**: web suite 96 → 105 passed (Python 3.13 e 3.11, anche con rete e DNS veri bloccati). Mutazioni fatte: release nell'except, os.close, regex col tetto vecchio, blocchi nascosti, unescape, motivo vecchio, ReDoS in testa (fallisce in ~10 s), lower(): ciascuna fa fallire almeno un test.
- **Review**: #429 (chat Mani) APPROVATO CON RISERVE (R-429-1 BASSA, R-429-2 BASSA: corrette nello stesso giro) → #430 (chat Mani) APPROVATO.

## Anomalie

- La fetta 2 aveva dichiarato «mutazioni sui test nuovi tutte prese»: la verifica esterna #237 ha trovato due rami difensivi senza test (ora coperti). Qui l'elenco delle mutazioni è quello effettivamente eseguito.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1/2/3»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata.
