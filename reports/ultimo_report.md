# Ultimo report — 2026-11-05 — Voce V15: pausa a voce, turni di seguito col cervello forte, conferma che non blocca (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #339 (https://github.com/Gasss23/Gas/pull/339), secondo la regola di merge di CLAUDE.md §10.
2. Decidere se i turni di seguito giudicati «per Gas» vanno scritti nella storia vera (cambia la scelta A; chiesto via M1). Sì al merge della #339 già dato (CI verde, bot/verifica esterna senza ALTA/MEDIA).

## Esito delle fette

- **Pausa a voce** (contratto rivisto dall'operatore via M1): `FATTA` — «pausa»/«standby»/«basta così» (anche dopo Jarvis/Gas) → «Va bene.» + `X-Gas-Comando: pausa`, niente cervello.
- **Turni di seguito** (`X-Gas-Seguito: 1`): `FATTA` — solo cervello forte (mai i gratuiti); «[NON_PER_ME]» → JSON vuoto, niente voce, `X-Gas-Comando: fine`.
- **V-2 bot #335** (conferma che può bloccare il server): `FATTA` — timeout 5 s, errore in cache 60 s; chiusa anche R-669-1-M2 per la conferma.
- **V-1 bot #335** («Jarvis Gas»): `FATTA` — dichiarato voluto con un test.
- **V-1/V-2 verifica esterna su b0405dc** («forte» dalla stanza pronunciato; segno con aggiunte letto ad alta voce): `FATTA` — review #676-M2 APPROVATO CON RISERVE (R-676-1-M2 BASSA).
- **Bot su b0405dc e 3581f6f: FAILURE per una MEDIA** (parlato dei turni di seguito nella storia, poi ai gratuiti; strumenti attivi nel seguito): `FATTA` con la scelta A dell'operatore (via su gas.py per questa PR): `run_turn(effimero=True)` — solo forte, nessuno strumento offerto (uno chiesto non si esegue), storia su copia e ripristinata nel finally, niente salvataggio; il server chiude subito il turno (R-677-1-M2). Test T103a-e (round-trip §7). Review #677-M2 APPROVATO CON RISERVE (chiuse), #677-M2 bis APPROVATO.
- **V-2 verifica esterna su a87d273** (il seguito non sapeva di non avere strumenti): `FATTA` — istruzione del seguito, review #678-M2.
- **Conflitto con main** (#338/#340 di Mani, solo report) e test d'integrazione di Mani col finto senza `**kw`: `FATTA` — merge di main, riga del test autorizzata da M1, review #679-M2.
- **V-1 (b) bot su a87d273** (strumento chiesto nel seguito → silenzio): `FATTA` — «Per farlo ripetimelo dicendo prima Hey Jarvis.», review #680-M2.
- **V-1 (a) bot su a87d273** (i seguiti veri non entrano nella storia): `IN ATTESA della decisione dell'operatore` (cambia la scelta A).
- **R-676-3** (review di Mani: nel seguito una trascrizione incerta diceva «Non ho capito»): `FATTA` — trascrizione incerta o vuota nel seguito → fine, niente voce.
- **C1**: `DEFERITA — prossima fetta` (ordine di M1).
- Test: suite kernel 1077 PASS 0 FAIL; voice_stt 104 passed; suite voce 293 passed (prima di R-676-3/R-677); in precedenza suite voce 291 passed prima delle ultime due correzioni; dopo, voice_stt + voice_prova_voci 155 passed. Review #675-M2 APPROVATO CON RISERVE (bis, ter).

## Anomalie

- Il contratto della pausa è cambiato durante la fetta (prima «standby profondo», poi «chiude la conversazione»): la review copre l'ultima versione.
- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
