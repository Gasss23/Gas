# Ultimo report — 2026-11-10 — voce: seguito più severo e risposte più brevi (chat M2)

## DECISIONI UMANE RICHIESTE

1. PR #365: merge da solo solo con verdetto del bot APPROVATO pulito; altrimenti serve il sì dell'operatore (via M1).
2. PR #363 (terminale A, sicurezza): merge all'operatore; bot su 860c751 APPROVATO CON RISERVE (solo BASSE, check neutral).

## Esito

- **PR #360 (cache frasi fisse divise)**: MERGIATA (447195f) col sì dell'operatore riferito da M1.
- **PR #363 (terminale A)**: pubblicata, merge di main (#359, #360) fatto, verifica esterna V-1 MEDIA (conflitto) chiusa; resta all'operatore.
- **Seguito più severo**: FATTA — nel seguito i frammenti di una parola fuori elenco chiudono senza chiamare il cervello; istruzione «nel dubbio non è per te».
- **Risposte più brevi e veloci**: FATTA — a voce UNA frase breve; tetto del parlato senza schermo 1500 → 800.
- Review #744-M2 APPROVATO CON RISERVE (R-744-1 MEDIA: «Continua.», numeri e giorni scartati → CHIUSA), #746-M2 APPROVATO CON RISERVE (BASSE).
- Test: voice_server, stt, tts, contesto, telegram_voce, voce_ascolto, sottofondo con -k "not browser": 743 passed.
- **Prova sul Mac** (il modello rispetta le istruzioni più severe e più corte): DEFERITA — si fa dal vero.

## Anomalie

Nessuna. `istruzione_turno_voce(True)` vale anche per i vocali di Telegram (chat Mani): lì cambia solo il testo dell'istruzione.
