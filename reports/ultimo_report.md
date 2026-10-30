# Ultimo report — 2026-10-30 — Voce V4: interruzione, «sì» detto subito, riassunto + dettaglio, tetto lato server, test della pagina in CI (chat M2) — PR #313

## DECISIONI UMANE RICHIESTE

1. Merge della PR #313 (https://github.com/Gasss23/Gas/pull/313): la mergia M1 se il bot dà APPROVATO pulito; con riserve M1 chiede il sì all'operatore.
2. Prova col microfono vero sul Mac: interruzione (che la voce di Gas dalle casse NON lo interrompa da sola), un «sì» brevissimo, rumore della TV.

## Esito delle fette

- **V4.1 — interruzione mentre Gas parla** (sì dell'operatore): `FATTA` — in conversazione, mentre Gas parla il microfono resta in ascolto (echo cancellation del browser); sopra la soglia 0,06 per 300 ms Gas si zittisce e la frase parte. `GAS_VOICE_INTERRUZIONE=0` la spegne. Limite dichiarato: i primi ~300 ms della frase che interrompe non vengono registrati. Dopo un'interruzione l'ascolto riparte già «in voce» (una voce media non va persa: R-580-1-M2); un colpo breve (tosse) zittisce Gas ma il clip quasi muto non parte (R-581-1-M2); ogni registrazione ha il suo buffer, così il clip dopo un colpo è un webm valido (R-582-1-M2).
- **V4.2 — «sì» detto subito** (V-1 bot #311 su c3079f4): `FATTA` — rumore di fondo = mediana dei primi 300 ms con un tetto; la voce conta fin dall'inizio.
- **V4.3 — riassunto + dettaglio** (V-1 bot #311 su a1a6a25): `FATTA` — con la pagina del browser l'istruzione chiede 1-3 frasi da dire e il dettaglio dopo una riga vuota; a voce solo il primo paragrafo, il resto a schermo. Senza schermo l'istruzione non parla più dello schermo.
- **V4.4 — bip e microfono** (V-2 bot #311 su a1a6a25): `FATTA` — un solo contesto audio per i bip; microfono chiuso se l'audio del browser fallisce.
- **V4.5 — tetto lato server** (V-2 ve #311 su a1a6a25): `FATTA` — `GAS_VOICE_MAX_TURNI_ORA` (60 turni parlati/ora), oltre → 429, nessun turno.
- **V4.6 — test della pagina in CI** (V-2 bot #311, ok di M1 a ci.yml): `FATTA` — Node + Playwright 1.63.0 + Chromium nel job; i giri della pagina in CI sono obbligatori (`GAS_TEST_BROWSER_OBBLIGATORIO=1`).
- **V-5 bot #311 su c3079f4** (riserve non tracciate): `FATTA` — in stato_progetto.
- **Review**: #580-M2 APPROVATO CON RISERVE (R-580-1-M2 MEDIA soglie in cascata, R-580-2/3-M2) → `FATTA`; #581-M2 APPROVATO CON RISERVE (R-581-1-M2 clip muto dopo un colpo) → `FATTA`; #582-M2 BOCCIATO (R-582-1-M2 MEDIA: clip corrotto dopo un colpo) → `FATTA`; #583-M2 APPROVATO CON RISERVE. Aperte: R-581-2-M2 BASSA («uso» spende Groq senza contare per il tetto), R-583-1-M2 COSMETICA (il controllo dell'header vale solo per webm).
- **gas.py / brains/**: non toccati.

## Prove

- Pagina vera in Chromium headless con microfono finto: 10 giri (normale, riascolto, pausa, tetto, errore, interruzione, interruzione media, colpo, colpo + voce, sì subito); ogni clip inviato deve cominciare con l'header webm. I giri nuovi falliscono sulla pagina precedente e passano sulla nuova.
- Voice suite con browser obbligatorio: 136 passed.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
