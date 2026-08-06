# Report — 2026-08-06 — Fix refusi + aggiornamento SICUREZZA ElevenLabs in stato_progetto.md

## DECISIONI UMANE RICHIESTE

1. Merge della PR docs/stato-fase3-sonda (branch corrente — merge di fine sessione).

---

## Scope & Esito

**Fetta 1 — Fix "Scop = decisione operatore."**
`SALTATA — il refuso NON esiste nel file. La riga già recitava "Scope = decisione operatore." (verificato byte-per-byte con hex dump Python).`

**Fetta 2 — Fix 'l'esio "6/6 verde"'**
`SALTATA — il refuso NON esiste nel file. La riga già recitava "l'esito \"6/6 verde\"" (verificato).`

**Fetta 3 — Fix "policy device ouput"**
`SALTATA — il refuso NON esiste nel file. La riga già recitava "policy device output" (verificato).`

**Fetta 4 — Sostituzione riga SICUREZZA ElevenLabs (🔴→🟡)**
`FATTA.`
Sostituita la decisione aperta urgente (rotazione immediata) con entry che documenta: esito del `git grep` sulla history (solo env var, nessuna chiave in chiaro committata), scelta consapevole dell'operatore di non ruotare, rischio residuo ACCETTATO con nota onesta.
Commit: `c7b65a4` — branch `docs/stato-fase3-sonda`.

---

## Anomalie riscontrate

I tre refusi descritti nello scope non erano presenti nel file `reports/stato_progetto.md` al momento dell'esecuzione (né nel working tree, né in nessun commit della sessione). Probabile origine: il testo originale dello scope faceva riferimento a una bozza o a un commit mai effettivamente pushato con quei refusi. Nessuna azione correttiva necessaria oltre alla verifica.
