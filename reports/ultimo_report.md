# Ultimo report — 2026-10-30 — Voce V3: conversazione filata (chat M2) — PR #311

## DECISIONI UMANE RICHIESTE

1. Merge della PR #311 (https://github.com/Gasss23/Gas/pull/311): la mergia M1 se il bot dà APPROVATO pulito; con riserve M1 chiede il sì all'operatore.
2. Prova dal vero sul Mac (microfono e casse veri): soglia del volume, eco, voce di sistema italiana per la frase d'attesa. In headless non si possono provare.

## Esito delle fette

- **V3.1 — modalità conversazione nel browser**: `FATTA` — `clients/voice/browser_client.html`: un clic e poi si parla; la frase parte da sola a fine voce (silenzio di 1,2 s); dopo la risposta il microfono resta aperto `GAS_VOICE_FINESTRA` s (default 12, letta da `GET /config` del proxy); se resti zitto la conversazione si chiude con bip e scritta. Spuntando via «conversazione continua» resta il vecchio premi-e-parla.
- **V3.2 — «due secondi o ci sto ragionando»**: `FATTA` — dopo 2 s senza risposta il browser dice una frase d'attesa con la voce di sistema (gratis, immediata), interrotta quando arriva la risposta.
- **V3.3 — risposte a voce brevi**: `FATTA` — `gas.py`: `run_turn(..., istruzione_turno=...)` (ok di M1), un'istruzione che vale solo per quel turno, nel messaggio system, fuori dalla cronologia; il server voce la passa solo ai turni parlati («1-3 frasi, parere subito, domanda secca»). In più, con la pagina del browser, a voce va solo l'inizio corto (≤3 frasi, ≤400 caratteri, «Il resto è a schermo») e il testo intero si legge a schermo; senza chiave ElevenLabs il testo arriva lo stesso.
- **V-1 bot #308 (su 2507621)**: `FATTA` — il 504 del proxy dice di NON ripetere la richiesta.
- **V3.4 — interruzione mentre Gas parla**: `SALTATA — va tolta dal parcheggio: serve prima l'ok di M1/operatore`.
- **Review #574-M2 BOCCIATO** (R-574-1-M2 MEDIA: un riascolto dal player faceva partire un turno non chiesto; più R-574-2/3/4/5-M2): `FATTA` — rivisto in #575-M2 (APPROVATO CON RISERVE: R-575-1-M2 pausa dal player, R-575-2-M2 permesso del microfono → `FATTA`), poi #576-M2 APPROVATO CON RISERVE.
- **Secondo giro — bot #311 su 17beb97: NON approvata (V-1 MEDIA)**: la modalità conversazione, attiva di default, non aveva un tetto: un rumore continuo (TV, altre persone) poteva far partire turni veri senza fine, anche a operatore assente. `FATTA` — dopo `GAS_VOICE_MAX_TURNI` turni di fila (default 5, contando quello del clic) la conversazione si chiude e serve un clic; voce minima 250 ms (un «sì» secco passa: R-577-1-M2). V-2 BASSA (i test del browser in CI si saltano: niente Node/Playwright nel job) `DEFERITA — riserva aperta, cambiare ci.yml è fuori da questa fetta`. R-576-2-M2 (audio rotto a metà) `FATTA` col secondo giro (`player.onerror`). Verifica esterna #311 su 17beb97: APPROVATO CON RISERVE, solo BASSE/COSMETICHE ([copia del verdetto](https://github.com/Gasss23/Gas/pull/311#issuecomment-6527391973)). Review #577-M2 APPROVATO CON RISERVE (R-577-1/2-M2 chiuse), #578-M2.
- **R-576-1-M2 BASSA** (guardia del permesso senza test), **R-576-3-M2 COSMETICA** (la pausa senza conversazione dice «conversazione chiusa»): `DEFERITA — fuori dal giro, una fetta piccola dopo la prova sul Mac`.

## Prove

- Test della pagina vera in Chromium headless con microfono finto (WAV): giro normale, riascolto a metà finestra e pausa dal player, 1 sola richiesta, 0 errori nella pagina. Il caso riascolto fallisce sulla pagina di #574 e passa sulla nuova. In CI si salta (niente Node/Playwright).
- Suite kernel 1063 PASS (T101 round-trip di `istruzione_turno`); voce + notte 322 passed.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
