# ULTIMO REPORT — 2026-10-07 — R-200-2: run_command conta come input esterno

## Riassunto

Chiuso un buco del cancello: dopo un `run_command` (es. `cat`, `ls`) Gas poteva scrivere file
o cambiare contatti senza chiedere conferma, perché quel tool non era nella lista degli input
esterni. Ora lo è. Prima di sbloccare la #149, come deciso dall'operatore.

## Cosa ho fatto

1. Trovato il punto: `UNTRUSTED_INPUT_TOOLS` in `modules/gate/gate.py` non conteneva `run_command`.
2. Aggiunto `run_command` alla lista — una riga.
3. Test: T72d/T72e, prova di giro completo T72f (sandbox os_strict: `ls` poi scrittura → in attesa di conferma, file non creato); T78e invertito (fissava il buco).
4. Prova: kernel 658 PASS / 0 FAIL; senza la correzione 4 FAIL e il file viene scritto senza conferma.
5. Review #203 APPROVATO CON RISERVE (R-203-1 ALTA preesistente sulla compressione, R-203-2 meno autonomia) — PR di questa fetta.

## Cosa NON ho fatto da solo

- R-203-1 non corretta: è un buco diverso (la compressione della cronologia "lava" l'input esterno), va fatta come fetta propria.
- Nessun merge senza il sì del bot.

## Cosa devi fare tu

1. Niente subito: se il bot dice sì, faccio il merge e poi aggiorno la #149 da main.
2. Decidere più avanti R-203-2: dopo un `run_command` in sandbox, le azioni successive devono chiedere conferma? (oggi sì).
