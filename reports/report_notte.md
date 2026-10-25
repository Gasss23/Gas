# Report del turno di notte — 2026-10-25

Ramo `notte/2026-10-25`, PR #263 (https://github.com/Gasss23/Gas/pull/263). Nessun merge (regola del turno).
Seconda notte (la PR #259 della prima è mergiata): al massimo UNA voce del motore. Presa la voce 3; le voci 4 e 5 toccano anche loro il motore e restano alle prossime notti.

## Voce 3 — Comando `/clear` su Telegram — FATTA
- **Cosa**: in `modules/telegram/bot.py` il comando `/clear` fa come `clear` nel terminale: riflessione sul task (se c'è storia e `GAS_RIFLESSIONE_AUTO` non è 0), poi cronologia pulita in ogni caso. Funziona solo dalle chat in `TELEGRAM_ALLOWED_IDS`. Risposta: prima riga «✓ Cronologia pulita.» (o «✗ … NON pulita»), poi esito della riflessione, lezioni proposte con gli id, e il recap intero in messaggi a parte.
- **Perché / cosa migliora**: da telefono si può chiudere un task e ripartire pulito senza il terminale; le lezioni proposte arrivano con l'id da approvare.
- **Controlli**: 19 test nuovi (round-trip col kernel vero con due tool call, `/clear`, turno nuovo da zero; un giro con la riflessione vera). pytest 2140 → 2159 passed; kernel 1031 PASS 0 FAIL. Review #502 APPROVATO CON RISERVE (una MEDIA: recap tagliato, a differenza del terminale), corretta; review #503 APPROVATO CON RISERVE.
- **Rischi**: la riflessione può durare minuti e intanto il bot non risponde ad altri messaggi (come per un turno normale); l'indicatore «sta scrivendo» sparisce dopo pochi secondi. Riserve aperte: R-503-1 BASSA (conteggio in caratteri, non in unità UTF-16, solo per testi pieni di emoji), R-503-2 COSMETICA. Non provato col Telegram vero.

## Verifiche su #263
- Bot: APPROVATO CON RISERVE. V-1 BASSA (`/clear` da un messaggio modificato cancellava la cronologia) e V-2 COSMETICA (recap vuoto) corrette; l'indicatore «sta scrivendo» resta mandato una volta sola.
- Verifica esterna ([commento](https://github.com/Gasss23/Gas/pull/263#issuecomment-6390800357)): APPROVATO CON RISERVE, nessuna ALTA/MEDIA. V-1 BASSA («/clear» con testo su una riga nuova andava al modello) corretta.
- Review #504 sul secondo giro: APPROVATO CON RISERVE. Nuova R-504-1 BASSA preesistente: `/notte` e `/compito` partono ancora da un messaggio modificato (da fare in una voce futura).

- Terzo giro (dopo le correzioni): bot e [verifica esterna](https://github.com/Gasss23/Gas/pull/263#issuecomment-6390966722) APPROVATO CON RISERVE, CI verde. Solo note BASSE, registrate in `stato_progetto.md` e non corrette stanotte per non riaprire un altro giro: «/clear@AltroBot» eseguito se all'avvio il bot non conosce il proprio nome; riflessione che blocca il polling; marcatore di continuazione del recap; kernel 1037 in CI contro 1031 nella misura locale.

## Cosa deve decidere l'operatore
1. Merge della PR #263 (il turno di notte non mergia).
2. Prova dal vero: bot acceso (`python3 gas.py telegram`), qualche messaggio, poi `/clear`.
3. Se mettere in coda R-504-1 (`/notte` da messaggio modificato) e la nota «/clear@AltroBot» (fix di una riga).
4. Il testo dell'attività programmata: la chat Motore ha chiesto il 24 ottobre di cambiarlo, dicendo che l'avevi approvato. Non l'ho fatto: serve la tua richiesta in questa sessione.
