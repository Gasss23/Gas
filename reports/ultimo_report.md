# Ultimo report — 2026-11-05 — Voce V15: pausa a voce, turni di seguito col cervello forte, conferma che non blocca (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #339 (https://github.com/Gasss23/Gas/pull/339), secondo la regola di merge di CLAUDE.md §10.
2. R-675-1-M2 parte storia (MEDIA, il bot ha dato FAILURE su questo): scegliere A) turno «effimero» in gas.py nella #339 (serve il via su gas.py per questa PR) o B) togliere i turni di seguito dalla #339 e rifarli nella fetta 2.

## Esito delle fette

- **Pausa a voce** (contratto rivisto dall'operatore via M1): `FATTA` — «pausa»/«standby»/«basta così» (anche dopo Jarvis/Gas) → «Va bene.» + `X-Gas-Comando: pausa`, niente cervello.
- **Turni di seguito** (`X-Gas-Seguito: 1`): `FATTA` — solo cervello forte (mai i gratuiti); «[NON_PER_ME]» → JSON vuoto, niente voce, `X-Gas-Comando: fine`.
- **V-2 bot #335** (conferma che può bloccare il server): `FATTA` — timeout 5 s, errore in cache 60 s; chiusa anche R-669-1-M2 per la conferma.
- **V-1 bot #335** («Jarvis Gas»): `FATTA` — dichiarato voluto con un test.
- **V-1/V-2 verifica esterna su b0405dc** («forte» dalla stanza pronunciato; segno con aggiunte letto ad alta voce): `FATTA` — review #676-M2 APPROVATO CON RISERVE (R-676-1-M2 BASSA).
- **Bot su b0405dc: FAILURE per una MEDIA** (R-675-1 parte storia: il parlato dei turni di seguito resta nella storia e al turno dopo può andare ai gratuiti; strumenti attivi nel seguito): `IN ATTESA della scelta dell'operatore via M1` — A) turno «effimero» in gas.py in questa PR, B) togliere i turni di seguito dalla #339.
- **C1**: `DEFERITA — prossima fetta` (ordine di M1).
- Test: suite voce 291 passed prima delle ultime due correzioni; dopo, voice_stt + voice_prova_voci 155 passed. Review #675-M2 APPROVATO CON RISERVE (bis, ter).

## Anomalie

- Il contratto della pausa è cambiato durante la fetta (prima «standby profondo», poi «chiude la conversazione»): la review copre l'ultima versione.
- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
