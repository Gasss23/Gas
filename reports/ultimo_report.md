# Report di fine task — 2026-10-11 — merge #175 + giro notturno senza la conversazione dell'operatore (PR #176)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #176 (https://github.com/Gasss23/Gas/pull/176). Tocca il motore (`gas.py`, `modules/notte`): merge autonomo dell'agente solo con verdetto testuale del bot `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. Metodo di protezione del cancello: (A) scrittura solo in cartelle permesse (proposta dell'agente) o (B) lista di nomi vietati che si allunga. Finché non c'è la scelta, l'agente non tocca più la lista dei nomi (V-1 verifiche esterne #175: `ruff.toml`, `pyrightconfig.json`, `*.js`, `.bashrc` ancora scrivibili).
3. Aperte da prima: archivio verifiche esterne (a/b), roadmap (voce 2 e F1 da segnare FATTE), costo del bot di verifica (Fable), V-2 bot #163, V-2 verifica esterna #172, prova sul Mac.

## Esito per fetta

- **Merge di #175**: `FATTA` — su richiesta esplicita dell'operatore, dopo il verdetto del bot (`neutral`, decide l'operatore); merge commit `d92e874`.
- **R-220-2 — il giro notturno legge (e se corrotta rinomina) la conversazione dell'operatore**: `FATTA` — `GasKernel(carica_storia=False)` usato da `notte_cmd` (percorso reale di `gas notte`) e dalla fabbrica di default di `esegui_notte`.
- **Test**: `FATTA` — 3 nuovi (storia corrotta intatta, fabbrica di default, percorso reale `notte_cmd`); notte 49 → 52; pytest 859 → 862 passed; kernel 715 PASS / 0 FAIL in locale. Mutation verificata su entrambi i percorsi.
- **Lista dei nomi vietati del cancello**: `SALTATA` — in attesa della scelta (A)/(B) dell'operatore.

## Revisore

Review #252 BOCCIATO (la prima versione proteggeva solo la fabbrica di default, che in produzione non gira: `notte_cmd` passa una sua fabbrica); #253 APPROVATO dopo la correzione. Verdetti integrali in `reports/handoff.md` §4.

## Anomalie

- `gh` nel container non è autenticato: la PR si apre e si legge con lo strumento GitHub collegato.
- Prima versione della fetta incompleta (percorso di produzione non coperto), fermata dal revisore prima del commit.
