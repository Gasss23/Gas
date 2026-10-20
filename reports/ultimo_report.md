# ULTIMO REPORT — 2026-10-20 — Firme scadute (C5) e avvisi dei lead raggruppati

Ramo `feat/merge-automatico-z1xjx2`, dopo il merge di #225 (operatore: «mergia 225 e continua con la roadmap»).

## DECISIONI UMANE RICHIESTE

1. Merge della PR (decide l'operatore se il bot non dà un APPROVATO pulito).
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non ha accesso ai file del progetto claude.ai).

## Esito

- **C5 — scadenza delle firme (R1)** — FATTA. Le richieste di firma scadute senza risposta si chiudono da sole (restano nel DB per controllo): il bot Telegram controlla una volta al minuto e manda un avviso una volta sola; il giro notturno le riporta negli avvisi del messaggio del mattino; `gas doctor` mostra quante sono in attesa e quante scadute ancora aperte. Review #381 APPROVATO CON RISERVE (R-381-1/2/3 BASSE, chiuse).
- **Avvisi sui lead dopo una lettura (note del bot su #225)** — FATTA. Un solo messaggio per turno, al massimo 10 lead e comunque sotto il limite di Telegram (gli altri contati); valori lunghi tagliati senza spezzare i caratteri resi visibili e con le lunghezze se il taglio li rende uguali; riga «Lead nuovi creati dopo la lettura: N» da 5 in su. Review #382 BOCCIATO (R-382-1 MEDIA: il messaggio unico poteva superare il limite e non partire, chiusa) → #383 APPROVATO CON RISERVE (R-383-1 BASSA: un «<» nel testo letto taglia il valore mostrato).
- **Riserva rimandata in stato_progetto** (richiesta dell'operatore): «stato_progetto troppo lungo, lo storico va spostato in `stato_storico.md`» — scritta, entrata col merge di #225.
- **Test** — kernel 927 → 941 PASS, 0 FAIL; pytest tests/ 1523 passed.
