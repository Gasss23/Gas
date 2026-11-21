# ULTIMO REPORT — Funnel community: analisi competitor, funnel v2, tasto collaboratori

**Data:** 21 novembre 2026
**Branch:** claude/funnel-community

## DECISIONI UMANE RICHIESTE

1. **Scegliere la bozza del funnel**: A (video/vocale di Gaspare + 3 domande, consigliata), B (solo messaggi, 4 domande) o test A/B — dettagli e copy pronti in `reports/funnel/funnel_v2.md`.
2. **Se scegli A**: registrare UN video-messaggio (o vocale) di 30–45 s col copione proposto in `funnel_v2.md`.
3. **Consegnare le specifiche a chi mantiene il bot** «Inizia Ora · Accesso» (non è nel repo Gas): `reports/funnel/tasto_collaboratori.md` (comando /linkmiei con i 2 link per agente) e la bozza scelta del funnel.
4. Merge della PR di questa sessione (vedi handoff §0).

## Esito fette

- **Fetta 1 — Mappatura funnel attuale (bot Inizia Ora · Accesso)**: FATTA. Ricostruito dal test del 18/11 nella cronologia: presentazione, 7 domande, ultimo passo, scheda lead, guida agenti, /pannello. Il pannello web (mini app) non si apre dall'automazione: non bloccante.
- **Fetta 2 — Analisi competitor su Telegram**: FATTA (9 canali della cartella «Competitor»: LEO TRADING, Cedric Fx, Luke World, ALE STARK, IN MOMO VERITAS, DISTRICT AUREX, The Edge, Nick and Leonard/Callisto FX, La vita di Shmek). Risultato in `reports/funnel/analisi_competitor.md`.
- **Fetta 3 — Due bozze di funnel migliorato (vocale vs messaggi)**: FATTA. Copy completo in `reports/funnel/funnel_v2.md`.
- **Fetta 4 — Tasto con i 2 link per i collaboratori**: FATTA COME SPECIFICA (`reports/funnel/tasto_collaboratori.md`). Il codice del bot non è né sul Mac né nei repo GitHub dell'account: l'implementazione va fatta da chi mantiene il bot.
- **Fetta 5 — Scrivere ai competitor fingendosi clienti**: SALTATA — limite di sicurezza dell'agente: niente messaggi a persone reali sotto falsa identità. Compensata con: bot automatici dei competitor + cronologia GIÀ esistente delle chat dell'operatore (quella con LEO SUPPORTO contiene il loro intero processo di vendita). Nessun messaggio inviato; le bozze precompilate trovate nei composer sono state lasciate/ripulite senza inviare.

## Anomalie

- Il bottone «Pannello» (mini app Telegram) non si apre con l'automazione in background; per i dati del pannello serve l'operatore o il comando /mielead.
- Nella chat «LEO SUPPORTO» c'è una bozza non inviata nel campo messaggio (già presente); lasciata com'era.
