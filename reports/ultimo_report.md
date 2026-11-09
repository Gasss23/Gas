# Ultimo report — 2026-11-09 notte — voce via Telegram, fetta 3 (chat Mani)

## DECISIONI UMANE RICHIESTE

1. (Domani) Consegna della voce in un thread a parte, così il bot non si ferma mai: serve allargare la guardia T78p delle firme («un click alla volta»). È un cambio di sicurezza, quindi decide l'operatore. Senza, il bot può restare fermo fino a circa 30 s per vocale.
2. Merge di questa PR: per la regola notturna dell'operatore la mergio da solo se il bot dà solo BASSE/COSMETICHE (il revisore la classifica senza aspetti di sicurezza).

## Esito

- **PR #355 (fetta 2)**: MERGIATA (b827447) col sì dell'operatore.
- **Voce via Telegram, fetta 3**: FATTA.
  - Turno parlato (V-1 bot #355): dopo un vocale, con la voce accesa, il turno riceve l'istruzione del parlato con schermo della voce di casa. Prima una o due frasi da dire, poi i dettagli dopo una riga vuota, che restano solo nel testo.
  - `testo_da_dire`: a voce niente grassetti, codice, titoli o segni degli elenchi; gli indirizzi web diventano «link».
  - Tempi della voce più corti (V-1 ve #355, R-717-4 in parte): sintesi e invio con 15 s invece di 30, quindi un blocco tipico di circa 30 s invece di circa 60.
  - Test: telegram_voce 59 passed; kernel 1099 PASS e 1 FAIL (T31g, ambiente).
- **Consegna in un thread**: DEFERITA. La prima versione è stata BOCCIATA (#720) perché rompeva la guardia T78p delle firme; la decisione spetta all'operatore (punto 1).
- Review #720 BOCCIATO, poi #721 APPROVATO CON RISERVE (solo BASSE/COSMETICHE).
