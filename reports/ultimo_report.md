# Ultimo report — 2026-11-09 notte — voce via Telegram, fetta 3 (chat Mani)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #357: decide l'operatore (V-1 MEDIA di processo della verifica esterna #357).
2. Opzioni per la voce del bot in un thread (decisione di sicurezza, R-717-4): (a) lasciare com'è (un solo thread, voce a 15 s, polling fermo circa 30 s per vocale); (b) un thread SOLO per sintesi e invio della voce, che non tocca mai update né firme, con la guardia T78p allargata in modo mirato e un test che lo vieta (consigliata); (c) la voce mandata da un processo separato tramite una coda su file (non tocca il bot, più complessa).

## Esito

- **PR #355 (fetta 2)**: MERGIATA (b827447) col sì dell'operatore.
- **Voce via Telegram, fetta 3**: FATTA.
  - Turno parlato (V-1 bot #355): dopo un vocale, con la voce accesa, il turno riceve l'istruzione del parlato con schermo della voce di casa. Prima una o due frasi da dire, poi i dettagli dopo una riga vuota, che restano solo nel testo.
  - `testo_da_dire`: a voce niente grassetti, codice, titoli o segni degli elenchi; gli indirizzi web diventano «link».
  - Tempi della voce più corti (V-1 ve #355, R-717-4 in parte): sintesi e invio con 15 s invece di 30, quindi un blocco tipico di circa 30 s invece di circa 60.
  - Test: telegram_voce 59 passed; kernel 1099 PASS e 1 FAIL (T31g, ambiente).
- **Consegna in un thread**: DEFERITA. La prima versione è stata BOCCIATA (#720) perché rompeva la guardia T78p delle firme; la decisione spetta all'operatore (punto 1).
- Review #720 BOCCIATO, poi #721 APPROVATO CON RISERVE (solo BASSE/COSMETICHE).
- **V-3 della verifica esterna #357 e R-723-1**: FATTA. Ogni tipo di a capo viene normalizzato prima della voce, così i dettagli non vanno a ElevenLabs. Review #723/#724.
