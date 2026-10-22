# ULTIMO REPORT — 2026-10-22 — Chat Mani, fetta 7: note dell'ultimo giro della PR #243 (R6, PR #244)

Ramo `feat/mani-web-fetta7` da main dopo il merge di #243. Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. PR #244 (https://github.com/Gasss23/Gas/pull/244). Fetta di sicurezza. Operatore: «procedi con la fetta 7».

## DECISIONI UMANE RICHIESTE

1. Merge della PR #244: vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
2. Fetta 8 per V-2 e V-3 della verifica esterna #244 (MEDIA preesistenti, testo nascosto in casi particolari)?
3. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
4. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

## Esito

- **R-453-1 (MEDIA, preesistente, trovata dalla review #453)**: `FATTA` — in HTML `<title/>`, `<script/>` e gli altri grezzi autochiusi aprono il testo grezzo fino a `</tag>` come nei browser (`set_cdata_mode`; se html.parser è vecchio e non accetta `escapable`, senza): un `</template>`/`</object>` scritto lì dentro non chiude più il contenitore. Chiude anche V-2 ve #243 bis.
- **R-454-1 (regressione del primo giro, review #454 BOCCIATO)**: `FATTA` — l'esenzione «dentro svg/math ogni `<x/>` è vuoto» apriva una fuga nei punti di integrazione HTML; ora vale solo per i tag non nascosti.
- **V-1 bot #243 (`<title/>` in template)**: `FATTA` — resta nascosto: il testo grezzo tiene aperto il template.
- **V-2 bot #243 (XHTML, commenti e CDATA dentro script/style)**: `FATTA` — `_commenti_e_cdata_xml` prima del parser, solo per `application/xhtml+xml`; lineare (test in sottoprocesso).
- **V-1 verifica esterna #243 bis (test)**: `FATTA` — propagazione del modo XHTML al ripiego dentro `_componi`.
- **V-1 bot #244 (noembed/noframes)**: `FATTA` — fra i nascosti nel parser e nel ripiego: `<noembed/>` (regressione di questa PR) e `<noembed>X</noembed>` (preesistente) non portano più al modello testo che i browser non mostrano. **V-2 bot #244** (COSMETICA): docstring del test.
- **Merge di main (PR #241 della chat Motore)**: `FATTA` — conflitti solo su report e memoria del revisore, risolti come da `reports/lavoro_parallelo.md`; review #461 (chat Mani) APPROVATO.
- **Verifica esterna #244** ([commento](https://github.com/Gasss23/Gas/pull/244#issuecomment-6340143206)): APPROVATO CON RISERVE. V-1 MEDIA (PR in conflitto con main): chiusa col merge. V-4 = V-1 bot #244, chiusa. V-5 COSMETICA: §6 aggiornato. **V-2 MEDIA** (XHTML, script annidati con lo stesso nome) e **V-3 MEDIA** (CDATA in HTML): preesistenti, `DEFERITA — registrate, proposte per la fetta 8`.
- **R-454-2, R-453-2, R-456-1, R-456-2**: `DEFERITA — BASSE/COSMETICHE, registrate in stato_progetto`.
- **Test**: web suite 174 → 192 (Python 3.13 e 3.11, anche con rete e DNS veri bloccati). Fuzz differenziale 0 fughe (HTML, XHTML); fuzz con oracolo html5lib del revisore: 0 casi in cui il nuovo codice mostra più di HEAD un testo che i browser nascondono. Mutazioni in copie isolate: tutte prese.
- **Review**: #453 (chat Mani) APPROVATO CON RISERVE (R-453-1 MEDIA, R-453-2 BASSA) → #454 BOCCIATO (R-454-1 MEDIA, regressione mia) → #455 APPROVATO CON RISERVE (R-454-2 BASSA preesistente) → #456 APPROVATO CON RISERVE (R-456-1 BASSA verso sicuro, R-456-2 COSMETICA).

## Anomalie

- Un primo tentativo (esenzione larga dentro svg/math) ha introdotto una fuga: presa dalla review #454 prima del commit.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…7»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata.
