# Ultimo report — 2026-10-29 — Voce V1: cervello forte dalla voce (chat M2, PR #304)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #304 (https://github.com/Gasss23/Gas/pull/304): solo se il bot dà APPROVATO pulito; con riserve decide l'operatore (via M1).
2. Se vuoi tutta la voce sul cervello forte: `GAS_VOCE_FORTE=1` nel `.env` del Mac (spento di default); il server voce si avvia con `python -m modules.voice.server` dalla cartella di Gas e lo conferma a schermo.

## Esito delle fette

- **V1.1 — giro vocale verificato e proposta a M1**: `FATTA` — microfono → Groq Whisper (`modules/voice/stt.py`) → `kernel.run_turn` → ElevenLabs (`tts.py`); il forte passava solo con «/forte», che a voce non si detta. M1 ha scelto «entrambe» (parola chiave + interruttore).
- **V1.2 — parola chiave parlata**: `FATTA` — `cervello_voce()` in `modules/voice/server.py`: «forte …»/«Gas forte …» (anche «Gus», come trascrive Whisper) all'inizio del parlato vale «/forte»; senza richiesta → 400 d'uso; «fortemente», «forte» a metà frase, «Gasforte» → turno normale. Solo sul testo trascritto: lo scritto usa «/forte».
- **V1.3 — `GAS_VOCE_FORTE`**: `FATTA` — 1/true/on/yes/si (come `_env_flag`): ogni richiesta al server voce va al forte; forte fermo → errore dichiarato del kernel (500), mai i gratuiti. Documentato nella docstring del server (posto naturale delle variabili della voce); doctor non toccato (è in gas.py).
- **V1.4 — test della voce nei test automatici**: `FATTA` — già in CI dalla PR #229 (la riga R8 era vecchia, corretta). Chiusa R-384-1 (chat Voce): opener urllib senza proxy; prima 26 test fallivano con `http_proxy` impostato e `no_proxy` vuoto, ora 104/104 in entrambi i casi.
- **V1.5 — finding del bot #304 su 274f131 (NON approvata)**: V-1 MEDIA `FATTA` — il server voce non caricava il `.env`, quindi `GAS_VOCE_FORTE` scritto lì restava spento senza segnale: ora `run_server` carica il `.env` come la CLI (prima di leggere token e porta), stampa una riga se l'interruttore è acceso, e si avvia con `python -m modules.voice.server` (gas.py non ha un comando `voice`). Provato con un `.env` vero temporaneo.
- **V1.6 — verifica esterna #304 (APPROVATO CON RISERVE)**: V-2 BASSA `FATTA` (saluto prima di «Gas»: «Ehi/Ok/Ciao Gas, forte …» vale «/forte»); V-3 COSMETICA `FATTA` (richiesta vuota → «uso»); V-1 BASSA `FATTA` come dichiarazione (falsi positivi «forte-forte», «forte: …» nel commento e in roadmap); V-4 COSMETICA (26 vs 25 test falliti prima del fix: dipende dall'ambiente, io ne misuro 26 con `http_proxy` e `no_proxy` vuoti, la verifica 25) `SALTATA — numero di un test su codice vecchio, il punto (R-384-1 reale e chiusa) è confermato`.
- **Review #565-M2** APPROVATO CON RISERVE → R-565-1-M2 (test che lasciava kernel/token sulla classe) e nota «sì» con l'accento chiuse, rivisto in #566-M2.
- **gas.py / brains/**: `SALTATA — fuori dal mandato di M1`, non toccati.

## Anomalie

- `gh` non autenticato nel cloud: PR creata con l'integrazione GitHub.
- Il commit di memoria del revisore (f2e68c7) dice «#564» senza il suffisso «-M2» (messaggio generato dallo script).
- Non provato con audio vero (niente microfono né chiave Groq nel cloud): prova dal vivo sul Mac da fare.
