# ULTIMO REPORT — 2026-10-27 — Mani fetta 20, secondo giro: lettura con lexbor pronta per l'accensione, ancora spenta (R6, chat Mani, PR #277)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #277 (https://github.com/Gasss23/Gas/pull/277): la mergio da solo solo con APPROVATO pulito del bot sull'head, altrimenti serve il tuo OK. Il merge non accende niente.
2. **Accensione**: serve la chat Motore (vedi RICHIESTE ALLA CHAT MOTORE). Dopo, sul VPS (Linux): `GAS_WEB_LEXBOR=1`.
3. Poi, una alla volta: R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.

## Esito
- **Primo giro (ab5eb1d)**: preparazione dell'accensione FATTA (sonda con lock e riprova, solo Linux, stderr nel warning, stima dei tempi, select/datalist/rp/hidden/dialog chiusi nascosti). Review #525 e #526 APPROVATO CON RISERVE.
- **Bot e verifica esterna #277 (primo giro)**: APPROVATO CON RISERVE. Chiuse in questo giro:
  - V-1 ve (MEDIA, di processo): conflitto con main → merge di c75f462 (solo roadmap.md, niente perimetro): FATTA.
  - V-2 ve: `hidden` su body o html → testo vuoto: FATTA.
  - V-3 bot e ve: ogni sonda fallita si riprova dopo 600 s, spenta dopo 3: FATTA.
  - V-1 bot / V-4 ve: del select si legge l'opzione scelta (tutte con `multiple` o `size` > 1), testo dell'opzione dalla stessa visita del body: FATTA.
  - V-2 bot / V-5 ve: details chiuso → solo il primo summary: FATTA.
- **Review #527** APPROVATO CON RISERVE: R-527-1 (test delle guardie sulle opzioni), R-527-2 (raccolta delle opzioni da quadratica a lineare), R-527-3 (`size` e scelta come il browser), R-527-4 (commento sui select annidati) → FATTE.
- **Review #528** APPROVATO CON RISERVE: R-528-1 (test dei commenti dentro il select), R-528-2 (l'opzione `hidden` conta per la scelta automatica, come lo standard) → FATTE; R-528-3 COSMETICA (option dentro option) → DEFERITA, dichiarata.
- **Review #529** APPROVATO CON RISERVE: R-529-1 COSMETICA (opzione dentro `<optgroup disabled>` non considerata disabilitata: si legge l'opzione sbagliata, mai testo nascosto) → DEFERITA.
- Restano aperte anche R-526-1 e R-520-4 (cosmetiche).
- **Accensione vera**: DEFERITA — serve la chat Motore.

## Prove (codice finale 0418f37)
- Web suite: 494 passed, 1 skipped su 3.13.16 con selectolax; 444 passed, 51 skipped su 3.11 senza selectolax (50 dei 53 test lexbor saltati). Parser vecchio forzato: 484 passed, 11 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1`: ancora 11 FAIL, gli stessi della fetta 19.
- Mutanti di questo giro, presi (1 failed su 53 ciascuno): senza guardia sui commenti; scelta automatica che salta anche le hidden; scelta automatica senza filtro disabled.
- Oracolo html5lib su 60 mila pagine senza template/svg/math: fughe con lexbor 0 (oggi 129). Con i casi nuovi (body/html hidden, details, option, dialog): 2 casi su 60 mila, entrambi `<title>` dentro `<select>`, dove html5lib segue il select vecchio.
- 131 pagine di documentazione locali: 125 con le stesse parole; le 2 pagine COPYRIGHT di Rust perdono le licenze dentro 2.659 `<details>` chiusi (il browser mostra solo i summary).

## RICHIESTE ALLA CHAT MOTORE
1. Per accendere la lettura con lexbor (decisione dell'operatore: «prepara l'accensione»):
   - aggiungere `selectolax==1.0.2` a `requirements-dev.txt`, così in CI girano i 50 test lexbor oggi saltati (isolamento del figlio compreso);
   - aggiungerlo a `requirements.txt` del VPS;
   - mettere `GAS_WEB_LEXBOR=1` nell'ambiente di Gas sul VPS (Linux). Sul Mac resta spenta da sola.

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
- Il revisore #529 dice che in `.claude/agents/memoria_revisore.md` la riga #528 compare due volte: falso, c'è una sola riga #528 (riga 901); niente da correggere.
