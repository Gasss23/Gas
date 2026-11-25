# Ultimo report — 2026-11-25 — Mani alla voce: piano + fetta F2

Sotto-chat di M1 (session_01FgYcG4uNEqggobeJsbmE93), ramo `claude/mani-voce-piano`.

## DECISIONI UMANE RICHIESTE

1. F1: a voce `richiedi_sviluppo` passa dalla firma su Telegram? (proposta: sì; oggi al cancello è UNCERTAIN e parte senza firma).
2. Canale dell'avviso di fine lavoro: commenti sulla issue letti da Gas sul Mac (proposta) oppure Telegram diretto dal cloud.
3. F5 (esecutore come scheduled task cloud): frequenza e ore (proposta: ogni ora, 8-20, feriali), massimo 2 richieste al giorno, modello.
4. Con `MERGIA #N` mergia l'esecutore (proposta) oppure resta M1.
5. Merge della PR di questa fetta (riserve BASSE del revisore aperte).

## Esito per fetta

- **Piano** (`reports/mani_voce_piano.md`): FATTA. Cosa esiste, cosa manca, fette F1-F5, rischi (iniezioni dalla voce, commenti falsi, spesa, accesso), decisioni. Mandato in sintesi a M1.
- **Punto 4 — compiti non di sviluppo a voce**: FATTA (verifica, nessuna modifica). Il percorso voce → `in_sottofondo` → processo separato → avviso Telegram con la risposta → lettura a voce c'è ed è coperto da `tests/test_unit_sottofondo.py` (154 test con quelli delle richieste, passati). Manca la prova sul Mac.
- **F2 — formato fisso dei commenti ESITO/COMANDO** (`modules/sviluppo/esiti.py`, `tests/test_unit_esiti.py`, 46 test): FATTA. Revisore #864 APPROVATO CON RISERVE → corrette R-864-1 (invisibili), R-864-2 (niente domanda di merge con controlli non verdi), cosmetica 4 → #865 APPROVATO CON RISERVE.
- **Correzione dopo bot e verifica esterna (#409)**: FATTA. Il bot era rosso per due caratteri bidi (U+202E) veri nel file di test: sostituiti con l'escape e aggiunto un test che li vieta. Inoltre VERIFICA_ESTERNA a valori fissi (niente domanda di merge se BOCCIATO), tolti i riempitivi che sembrano vuoti (R-865-1), docstring e piano corretti (`ESITO: ferma`, `MERGIATA` spostato in F5). Revisore #866: APPROVATO. 55 test.
- **F1, F3, F4, F5**: DEFERITE — aspettano il via dell'operatore (toccano voce, credenziali, trigger o spesa ricorrente).

## Anomalie

- Nel container mancavano le dipendenze (`openai`): installate con `pip install -r requirements.txt`; prima 3 test di `test_unit_sottofondo.py` fallivano per questo.
- Riserve aperte: R-864-3 BASSA, cosmetica 5, cosmetica U+200D, verifica esterna #409 V-2 BASSA (in `reports/stato_progetto.md`).
- Verdetti: verifica esterna #409 APPROVATO CON RISERVE (solo BASSE); bot sul primo head: failure per caratteri bidi (corretto).
