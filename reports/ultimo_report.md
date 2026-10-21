# ULTIMO REPORT — 2026-10-21 — Chat Mani, fetta 4: note delle PR #238 e #239 (R6, PR #239)

Ramo `feat/mani-web-fetta4` (da main dopo il merge di #238, poi merge di main). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. PR #239 (https://github.com/Gasss23/Gas/pull/239). Fetta di sicurezza. Operatore: «procedi con la fetta 4», poi «a, correggi e mergia quando il bot approva».

## DECISIONI UMANE RICHIESTE

1. Merge della PR #239: autorizzato dall'operatore quando il bot approva (`verifica-bot` success sull'head, niente ALTA/MEDIA), con CI verde e senza conflitti.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

## Esito

- **Nome del tag intero (V-1 bot #238, R-431-1)**: `FATTA` — `<styled-box>`, `<script_x>`, `<style.x>`, `</scriptx>` non sono blocchi nascosti.
- **Ripiego alla pari col parser (V-2 ve #238)**: `FATTA` — stesso insieme `_TAG_NASCOSTI` per parser e ripiego; commenti tolti anche con «>».
- **`embed` (R-431-2)**: `FATTA` — è un elemento vuoto: nascondeva il resto della pagina anche nel percorso normale (dalla fetta 1).
- **Test (V-1/V-4 ve #238, V-2/V-3 bot #238)**: `FATTA`.
- **Note bot e verifica esterna #239**: `FATTA` — nel ripiego un tag finisce al suo «>» fuori dai valori fra virgolette («</script>» dentro un attributo non chiude il blocco), titolo tolto dal testo, «/» dopo il nome, tag senza fine che porta via il resto (si perde testo, non esce contenuto nascosto), commenti vuoti `<!-->`/`<!--->` e chiusura `--!>` (lineare, con cache delle posizioni), math e object nascosti anche nel parser.
- **R-439-1, R-440-1, R-441-1**: `FATTA` — la fine del tag segue il tokenizzatore HTML: resto del nome del tag fino a spazio, «/» o «>»; le virgolette aprono un valore solo dopo un «=» che segue un nome; un valore senza virgolette si prende «=» e virgolette. Regex possessiva, lineare (2 MB avversari ≤0,3 s). **R-439-2** (test sulla prima chiusura fra «-->» e «--!>») e **R-439-3** (`dict[str, int]`): `FATTA`.
- **R-442-1, R-442-2**: `DEFERITA` — famiglia diversa (contenuto dei blocchi nascosti non grezzi e commenti fasulli `<!`, `<?`, CDATA): serve un contatore come quello del parser, fetta successiva. BASSE: il ripiego si usa solo se html.parser solleva un errore, e con pagine vere non succede.
- **Test**: web suite 105 → 137 passed (Python 3.13 e 3.11, anche con rete e DNS veri bloccati). Mutazioni in copie isolate, tutte prese da almeno un test.
- **Review**: #431 → #432 → #438 (merge di main) sul primo giro; #439 → #440 → #441 → #442 (chat Mani), tutte APPROVATO CON RISERVE, sul secondo giro (ciascuna ha chiuso le riserve della precedente, restano R-442-1/2).

## Anomalie

- Durante una prova di mutazione del primo giro l'agente ha usato `git checkout -- modules/web/leggi.py` e ha perso le modifiche non in staging; le ha riapplicate subito. Da allora le mutazioni si fanno solo in copie isolate.
- Il ripiego imita il tokenizzatore HTML a pezzi: ogni review ha trovato un caso nuovo della stessa famiglia (R-439-1 → R-440-1 → R-441-1). Il fuzz differenziale della #442 non trova più differenze sulla fine del tag di apertura.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1/2/3/4»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata.
