# ULTIMO REPORT — 2026-10-22 — Chat Mani, fetta 9: nodo corrente dentro svg/math come i browser (R6, PR #246), secondo giro

Ramo `feat/mani-web-fetta9`, PR #246 (https://github.com/Gasss23/Gas/pull/246). La PR #245 (fetta 8) è mergiata e main è entrata in questo ramo. Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. **R-ve246-5 (MEDIA, già presente su main)**: un elemento HTML speciale dentro `<canvas>` o `<object>` fa arrivare al modello testo che il browser nasconde. Per chiudere bene questa famiglia serve un vero costruttore dell'albero HTML5 (per esempio lexbor, via selectolax): è una dipendenza nuova, quindi decide l'operatore.
2. Merge della PR #246: l'operatore ha chiesto di mergiarla quando il bot approva.
3. Sul Mac e sulla VPS: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` (dalla cartella di Gas) deve dire True.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **Primo giro** (R-463-1, R-450-1, V-2 ve #243, R-ve245-1, R-456-1; B-467-1/2, R-468-1/2): `FATTA` (review #467–#469).
- **V-1 ve #246 (ALTA, `</p>`/`</br>`)**: `FATTA` — escono dal contenuto estraneo come vuole lo standard.
- **V-2 ve #246 (ALTA, antenati HTML) e R-vb246-2**: `FATTA` — dove l'esito dipende da quello che la pila non vede, la pila diventa incerta e il resto della pagina si nasconde (warning nel log).
- **V-3 ve #246 (ALTA, costo quadratico)**: `FATTA` — strutture O(1), 20k annidamenti in meno di 5 s.
- **B-470-1 (ALTA, `<font>` con attributi)**, R-470-1/2, R-471-1/2: `FATTA`.
- **R-ve246-5 (MEDIA preesistente, canvas/object)**: `DEFERITA — decisione dell'operatore (costruttore HTML5)`.
- **Test**: web suite 264 → 291 (Python 3.13 e 3.11). Fuzz con oracolo lexbor contro fetta 8 e main (8×20k): 0 regressioni; le fughe rimaste sono tutte R-ve246-5, uguali o meno della fetta 8. Fuzz html5lib e ripiego: 0 (le «regressioni» per html5lib sono tutte `</p>`/`</br>`, dove html5lib non segue lo standard e lexbor sì).
- **Review**: #467 BOCCIATO, #468 e #469 APPROVATO CON RISERVE, #470 BOCCIATO, #471 APPROVATO CON RISERVE, #472 APPROVATO (chat Mani).

## Anomalie

- Dalle 15:15 alle 17:23 UTC GitHub non ha elaborato i push di questa sessione (ref aggiornati, PR e CI ferme): la verifica esterna e il bot hanno lavorato su head senza CI. Poi tutto è ripartito da solo.
- Ho provato «grezzi sempre testo grezzo nel contenuto estraneo»: il fuzz lexbor ha trovato una regressione (CDATA vero dentro iframe in math), quindi sono tornato alla semantica del browser con la pila incerta.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…9»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata; richiesta su `scripts/bot_esito.py` (MEDIA preesistenti citate come V-x contate come nuove, blocco «Mani — fetta 7»).
