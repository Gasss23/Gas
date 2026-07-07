# Ultimo report

## Task
Doc-only, una fetta: registrare due nuovi item aperti in `reports/roadmap.md`.
Nessuna modifica a gas.py, brains/, modules/, tests/.

## Esito
✅ Fatto. Prima ho letto `reports/roadmap.md` per rispettarne struttura/formato, poi ho cercato
duplicati (grep su "openrouter|rung|config-drift|hardcod" in roadmap.md e stato_progetto.md):
trovato solo `R-ci-openrouter` in stato_progetto.md, ma è un item diverso (fragilità test CI T9a
sulla presenza di OPENROUTER_API_KEY), non un duplicato delle due voci richieste. Nessun blocco.

Aggiunte due voci come item 7 e 8 nella sezione "🟡 PROSSIMI PASSI (in ordine di priorità)":

7. **Rung 4 OpenRouter in degrado** — `meta-llama/llama-3.3-70b-instruct:free` soggetto a rate
   limit upstream crescenti; diversi modelli free-tier OpenRouter hanno perso l'accesso gratuito
   a giugno 2026. Da investigare: modello free alternativo stabile o declassare rung 4 a
   best-effort dichiarato. Stato: APERTO, priorità media.
8. **Config-drift stringhe modello** — stringhe modello hardcoded in `claude_brain.py` e
   `gemini_brain.py`, fuori dalla definizione della cascata. Serve single source of truth;
   attenzione: se i brains importano da gas.py, rischio import circolare. Fetta separata futura,
   solo registrazione. Stato: APERTO, priorità media.

## Nota tecnica: divergenza remota durante il push
Al push iniziale, origin/main aveva 18 commit non presenti in locale (sessione doc-only del
2026-07-06: riallineamento FASE 2.5/FASE 5, puntatore sez.10, deprecazione Groq) che avevano
rinumerato la stessa lista "PROSSIMI PASSI" da 1-5 a 1-6. Ho fatto `git fetch` + `git rebase
origin/main`, risolto il conflitto in `reports/roadmap.md` reinserendo le mie due voci come
item 7-8 in coda alla lista rinumerata del remoto (nessuna voce remota persa), e in
`reports/ultimo_report.md` ho tenuto la mia versione (il file riflette solo l'ultimo task per
convenzione, non si aggrega tra sessioni).

## Stop gate
Rispettato: solo l'aggiunta delle due voci richieste, nessuna correzione adiacente, nessun
riallineamento o refactor del file oltre alla risoluzione tecnica del conflitto di rebase
(preservazione, non modifica, del contenuto remoto). Non propongo altro in questo momento.

## File toccati
- `reports/roadmap.md` (2 item aperti aggiunti, come item 7-8)
- `reports/ultimo_report.md` (questo file)
