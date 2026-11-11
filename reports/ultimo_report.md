# Ultimo report — 2026-11-11 notte — voce: prima frase in anticipo e tempi del forte (chat M2)

## DECISIONI UMANE RICHIESTE

1. PR dello streaming: con verdetto del bot APPROVATO pulito e CI verde la mergia la chat; con riserve resta per il mattino.
2. Sul Mac, dopo il merge e il riavvio del server voce: `grep "tempi claude-cli" gas_debug.log | tail -5` e incollare il risultato (dice dove vanno i 6–7 s del cervello).

## Esito

- **Prima frase in anticipo**: FATTA. Nei turni a voce `claude -p` scrive a flusso; la voce della prima frase si prepara mentre la CLI finisce e si usa solo se identica alla risposta finale. Dal vivo: prima frase pronta ~1,2 s prima.
- **Tempi del forte nel log**: FATTI (riga `tempi claude-cli:` in gas_debug.log, solo numeri).
- **B3 dell'audit notturno 2** (byte non UTF-8 della CLI → errore senza costo né riconoscimento di limite/login): CORRETTA (e9b05e5, review #781/#782-M2).
- **V-1 del bot su 87c5ff3** (l'anticipo poteva mandare a ElevenLabs testo che non verrebbe detto): CORRETTA (c8c5f8f) — solo primo paragrafo ed entro il tetto della parte parlata (review #783-M2).
- Review #773-M2 APPROVATO CON RISERVE (R-773-1/3 chiuse in #778, R-773-2 BASSA aperta), #778 e #779 (merge di main) APPROVATO.
- Test: kernel 1136 PASS, 1 FAIL T31g (fastembed assente, come su main); claude_cli + voice_server 290 passed.
- **Niente schema strumenti a voce e processo CLI caldo**: DEFERITI in attesa dei tempi del Mac.

## Anomalie

Nessuna.
