# ULTIMO REPORT — 2026-10-21 — Chat Mani, fetta 4: note della PR #238 (R6, PR #239)

Ramo `feat/mani-web-fetta4` (da main dopo il merge di #238, poi merge di main). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. PR #239 (https://github.com/Gasss23/Gas/pull/239). Fetta di sicurezza. Operatore: «procedi con la fetta 4».

## DECISIONI UMANE RICHIESTE

1. Merge della PR #239: per questa fetta l'operatore non ha (ancora) ripetuto «mergia quando il bot approva»; vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), altrimenti decide l'operatore.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

## Esito

- **Nome del tag intero (V-1 bot #238, R-431-1)**: `FATTA` — in apertura (`_INIZIO_TAG` più il controllo del carattere dopo il nome) e in chiusura (`_chiusura`): `<styled-box>`, `<script_x>`, `<style.x>`, `</scriptx>` non sono blocchi nascosti.
- **Ripiego alla pari col parser (V-2 ve #238)**: `FATTA` — stesso insieme `_TAG_NASCOSTI` per parser e ripiego; commenti tolti anche se contengono «>». Il ripiego non conta l'annidamento (dichiarato, R-431-3).
- **`embed` (R-431-2)**: `FATTA` — tolto dai tag con contenuto: è un elemento vuoto e nascondeva il resto della pagina anche nel percorso normale (difetto presente dalla fetta 1).
- **Test (V-1/V-4 ve #238, V-2/V-3 bot #238)**: `FATTA` — contenuti riconoscibili (SEGRETO_*) per tutti i tag nascosti e il commento, chiusura con attributi, unescape che solleva, stderr del sottoprocesso nei test a tempo, attesa dei thread DNS prima del test del semaforo.
- **Test**: web suite 105 → 107 passed (Python 3.13 e 3.11, anche con rete e DNS veri bloccati). Mutazioni eseguite in copie isolate, ciascuna presa da almeno un test: commenti ignorati, insieme a 4 tag, confine della chiusura tolto, apertura per prefisso, except di unescape tolto, embed rimesso, chiusura senza «>».
- **Review**: #431 (chat Mani) APPROVATO CON RISERVE (R-431-1/2 BASSE, R-431-3 COSMETICA: corrette nello stesso giro) → #432 (chat Mani) APPROVATO CON RISERVE (R-432-1 COSMETICA) → #438 (chat Mani, merge di main) APPROVATO.

## Anomalie

- Durante una prova di mutazione l'agente ha usato `git checkout -- modules/web/leggi.py` per annullarla e ha riportato il file alla versione di main, perdendo le modifiche non ancora in staging; le ha riapplicate subito (stesso script) e i test le confermano. Da qui in poi le mutazioni si fanno solo in copie isolate.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1/2/3/4»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata.
