# ULTIMO REPORT — 2026-10-20 — Roadmap aggiornata con le decisioni del 19 ottobre (PR #220)

Ramo: `feat/merge-automatico-z1xjx2`. Compito solo documentale, nessun codice. PR #220 (https://github.com/Gasss23/Gas/pull/220), NON mergiata.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #220: lo decide l'operatore.
2. **Da chiarire** (scritto così nella roadmap, R2): il freno di giorno all'80% della finestra delle 5 ore, in conflitto con «conta solo il consumo di Gas».
3. Proposte NON applicate (vedi sotto): approvarle una per una.

## Cosa ho cambiato, voce per voce

Fonte: la roadmap completa dell'11 ottobre (allegato dell'operatore), salvata come `reports/roadmap.md` al posto della vecchia (ferma al 21 settembre). Struttura, simboli e sigle mantenuti. Intestazione: «Aggiornata il 19 ottobre 2026», `main` = `2536ffd` (verificato, PR #219).

**A) Avanzamenti**
- R0 ✅ fatto 11-13 ott — tabella cap. 0, titolo e «Fatto/Resta» in R0, cap. 2 (Autonomia), cap. 3 (strumenti: 11, nessun comando di sistema).
- R2 fetta 1 ✅ (12 ott) — cap. 0, cap. 2, R2.
- R9 riflessione automatica + recap pertinente ✅ (PR #211/#213/#215/#216, provati sul Mac) — cap. 0, cap. 2, R9.
- G-3 ✅ (14 ott) — cap. 2 «Controlli», §5.7.
- Test: 895 del motore + 1450 (cap. 2).

**B) Decisioni del 19 ottobre**
1. Ordine confermato, server a R5; tolto «vale solo se la confermi» — cap. 0.
2. Firma 24 ore di notte, 30 minuti di giorno — cap. 3, R1.
3. Autonomia (supera C-d e R-203-2), principio di Gas — cap. 0, R1, §5.2.
4. R2 riscritto (abbonamento Max 5x, 20% settimanale solo sul consumo di Gas, niente freno notturno, «da chiarire» freno all'80%, tetto → gratuiti/coda + riflessione R9, crediti non usati, dubbio sul limite residuo, «Claude Code sul server» riaperto, proposta su CLAUDE.md) — R2, cap. 11.
5. Regola dei modelli (solo forti per lavori importanti e dati di clienti; coda; etichetta da regola o operatore) — cap. 0; supera la voce «fornitori che si allenano» in R6; nota in §5.6 (Mistral).
6. R3: niente connettori, nessun merge di notte e report del mattino, priorità, 80/20, ultimi giri entro le 05:00, costruisce Claude Code in cloud; tolto il merge automatico dopo N notti — R3, cap. 11.
7. R4: backup cifrato su iCloud Drive (`.gas_memory.db`, `.env`, `.gas_history.json`), repo privato rimandato con le tre protezioni gratuite prima di R3, revisione esterna aggiornata — R4.
8. R5: Netcup KVM x86 ~8 GB, prerequisiti dell'acquisto, Ollama tolto — R5, cap. 8.
9. R6: ordine web → mail → social → notifiche; regole fisse scritte dall'operatore; allarme gratuito (ntfy), Twilio scartato, motivi e tetto da decidere — R6, cap. 9, cap. 11.
10. R7: solo lavoro tecnico, adatto al turno di notte — R7.
11. R8: voce da scegliere all'ascolto (Piper IT, «Jarvis» solo privato, clone), niente imitazioni, ElevenLabs a pagamento non scelto; voce fronte principale e Telegram per firme/report/fuori casa (chiude «fronte o ponte»); firme a voce «Procedi/Annulla», bottoni per sicurezza/codice madre/irreversibili; chiuse D1-ter, D2-audio, F0, R-client4a-1 — R8.
12. R9: lezioni 4-6 da rivedere a testo; video senza decisione — R9.
13. R10: bozza del recinto approvata; lista per valore, max 10 PR a notte, «importante» oltre il limite — R10.
14. Ollama rimosso, sblocco OpenRouter rimandato, OmniRoute come sonda fuori dal motore — §5.6, cap. 2 (nota sulla cascata), cap. 11.
15. Codice che applica cancello e firma: resta livello 2 con doppia verifica, firma solo coi bottoni, mai di notte — §5.2.
16. Scritture (R-223-2): lista dei vietati + segnalazione solo per file nuovi delicati — §5.3.
17. R11: Gas-Python, n8n piano B, Make scartato — R11, cap. 10, cap. 11.
18. Bot di trading rimosso — R5, cap. 8, cap. 9 (Mirage), cap. 10, cap. 12.
19. GAS WEB OS in roadmap dopo Gas, alta ambizione, blueprint presto — R11, cap. 10.
20. Pulizia settimanale di rami e PR — §5.7, cap. 7.
21. Regola di merge nel codice + `fine-task.md`: solo segnata come lavoro per il turno di notte — R3, §5.7.
22. Istruzioni del progetto claude.ai ⏳ 👤 (§5.9); vecchio PC ⏳ 👤 (R4); account «macchina» scartato (cap. 11); firma dei commit dell'agente aperta (cap. 6).

**C) Non discusse il 19 ottobre** — cap. 6, marcate «non discussa 19 ott»: PR #158/#109/#141/#87; regole del bot; GDPR; tetto della voce; Mistral/Cerebras a pagamento; quando Gas riflette (con nota: la riflessione automatica copre il caso principale); lista azioni del PC; TradeGasFX; firma dei commit.

**D) Cap. 6 riordinato**: solo le voci aperte, più i 3 punti aperti del 19 ottobre (allarme, voce, lezioni 4-6) e il «da chiarire» di R2.

## Proposte che NON ho applicato (servono il tuo ok)

1. `CLAUDE.md` §2: «Claude NON è un rung runtime» va cambiata (R2 lo rende un gradino via abbonamento).
2. `CLAUDE.md` §2: la cascata cita ancora Ollama (rimosso dal piano); va tolto quando si toglie dal codice.
3. `.claude/commands/fine-task.md`: «non mergiare» da allineare alla regola di merge (lavoro per il turno di notte, decisione 21).
4. `reports/stato_progetto.md`: aggiornarlo con le decisioni del 19 ottobre (oggi ha solo la riga della regola «fonte unica»).
5. `reports/roadmap_sintesi.md` (pagina del 19 ottobre) è superata dalla roadmap nuova: cancellarla.
6. `README.md` e `gas_identity.md` citano la cascata vecchia (già in §5.9).

## Anomalie

- Il file sorgente stava solo nel progetto claude.ai: è arrivato come allegato al secondo tentativo.
