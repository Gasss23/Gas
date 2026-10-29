# Ultimo report — 2026-10-29 — Voce V2: istruzione d'uso a voce, avvio parlante, attesa del forte nel browser (chat M2) — PR #308

## DECISIONI UMANE RICHIESTE

1. Merge della PR #308 (https://github.com/Gasss23/Gas/pull/308): solo se il bot dà APPROVATO pulito; con riserve decide l'operatore (via M1).

## Esito delle fette

- **V2.1 — V-2 verifica esterna #304 («Gas, forte.» da solo dava un 400 confuso, anche con GAS_VOCE_FORTE=1)**: `FATTA` — `modules/voice/server.py`: «forte» PARLATO senza richiesta → risposta 200 da ascoltare (sintetizzata se il client vuole audio, come il browser): «Dopo "forte" dimmi cosa fare, per esempio: "Gas, forte: riassumi i lead di oggi". Non ho avviato nessun lavoro.» Nessun turno, mai ai gratuiti. «/forte» scritto senza richiesta resta 400.
- **V2.2 — V-3 verifica esterna #304 (server muto ~8 s all'avvio)**: `FATTA` — riga «… gas voice: avvio in corso…» stampata subito, prima di caricare Gas. Provata con un `.env` vero temporaneo.
- **V2.3 — in più, per la prova col microfono (detto a M1)**: `FATTA` — `clients/voice/browser_server.py` aspettava il server voce 90 s fissi, ma una chiamata del forte può durare fino a 300 s: il browser avrebbe detto «Voice server non raggiungibile» mentre Gas lavorava. Ora attesa 600 s (`GAS_VOICE_TIMEOUT` per cambiarla), connessione con tetto corto di 10 s (server spento → 502 subito), e a tempo scaduto 504 «Gas non ha risposto entro N s: il lavoro può essere ancora in corso…».
- **Review #568-M2 APPROVATO CON RISERVE**: R-568-1-M2 (nome `timeout` in conflitto con socketserver), R-568-2-M2 (test che poteva restare appeso), R-568-3-M2 (server irraggiungibile scambiato per «ancora in corso») `FATTA` — riviste in #569-M2 (APPROVATO CON RISERVE: R-569-1-M2, test che non distingueva il fix, `FATTA` — rivista in #570-M2, APPROVATO CON RISERVE).
- **R-570-1-M2 COSMETICA** (test del proxy senza `server_close()`): `FATTA` nel secondo giro (0 «unclosed» con `-W always::ResourceWarning`).
- **Secondo giro — bot #308 su 2dff07f (APPROVATA, APPROVATO CON RISERVE)**: V-1 BASSA (proxy a thread singolo bloccato fino a 600 s) `FATTA` — `ThreadingHTTPServer`; V-2 COSMETICA (riga «avvio in corso» anche quando poi l'avvio si ferma) `SALTATA — la parte lenta è l'import di gas, che deve girare prima di leggere il token (può stare nel .env): spostarla lascerebbe muti proprio i secondi lenti; il revisore #571-M2 è d'accordo`.
- **Secondo giro — verifica esterna #308 su 2dff07f (APPROVATO CON RISERVE, [commento](https://github.com/Gasss23/Gas/pull/308#issuecomment-6510176231))**: V-2 BASSA (risposta HTTP rotta → socket chiuso) `FATTA` — 502 JSON «Risposta non valida»; V-1 BASSA (§6 dell'handoff superato) `FATTA` (riscritto); V-3 BASSA (istruzione d'uso senza chiave ElevenLabs → 503) e V-4 BASSA (browser con attese da 600 s) accettate, la seconda da vedere sul Mac.
- **Review #571-M2 APPROVATO CON RISERVE**: R-571-1-M2 (test che si sarebbe bloccato tornando a HTTPServer) e R-571-2-M2 (504 che non diceva della coda) `FATTA` — rivista in #572-M2.
- **gas.py / brains/ / ci.yml**: `SALTATA — fuori dal mandato di M1`, non toccati.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- Non provato con audio vero né col browser vero (Safari/Chrome potrebbero chiudere una richiesta lunga prima dei 600 s): da vedere nella prova sul Mac.
