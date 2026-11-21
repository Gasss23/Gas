# ULTIMO REPORT — Funnel community: analisi competitor, funnel v2, tasto collaboratori

**Data:** 21 novembre 2026
**Branch:** claude/funnel-community

## DECISIONI UMANE RICHIESTE

1. **Consegnare le specifiche a chi mantiene il bot** «Inizia Ora · Accesso» (non è nel repo Gas): `reports/funnel/funnel_v2.md` (Bozza B, scelta dall'operatore il 21/11 in chat) e `reports/funnel/tasto_collaboratori.md` (comando /linkmiei con i 2 link per agente).
2. **Far controllare i testi del funnel a un esperto di promozione finanziaria/privacy** prima dell'uso (raccomandazione della verifica esterna #392).
3. Merge della PR di questa sessione (vedi handoff §0).

## Esito fette

- **Fetta 1 — Mappatura funnel attuale (bot Inizia Ora · Accesso)**: FATTA. Ricostruito dal test del 18/11 nella cronologia: presentazione, 7 domande, ultimo passo, scheda lead, guida agenti, /pannello. Il pannello web (mini app) non si apre dall'automazione: non bloccante.
- **Fetta 2 — Analisi competitor su Telegram**: FATTA (9 canali della cartella «Competitor»: LEO TRADING, Cedric Fx, Luke World, ALE STARK, IN MOMO VERITAS, DISTRICT AUREX, The Edge, Nick and Leonard/Callisto FX, La vita di Shmek). Risultato in `reports/funnel/analisi_competitor.md`.
- **Fetta 3 — Due bozze di funnel migliorato (vocale vs messaggi)**: FATTA. Copy completo in `reports/funnel/funnel_v2.md`.
- **Fetta 4 — Tasto con i 2 link per i collaboratori**: FATTA COME SPECIFICA (`reports/funnel/tasto_collaboratori.md`). Il codice del bot non è né sul Mac né nei repo GitHub dell'account: l'implementazione va fatta da chi mantiene il bot.
- **Fetta 5 — Scrivere ai competitor fingendosi clienti**: SALTATA — limite di sicurezza dell'agente: niente messaggi a persone reali sotto falsa identità. Compensata con: bot automatici dei competitor + cronologia GIÀ esistente delle chat dell'operatore (quella con LEO SUPPORTO contiene il loro intero processo di vendita). Nessun messaggio inviato. Precisione (V-6 bot): l'unica bozza cancellata è quella che il link «ENTRA ORA» di Luke World ha generato da sé nel campo messaggio quando l'ho aperto (creata dal mio stesso clic, mai inviata); la bozza preesistente nella chat «LEO SUPPORTO» è stata lasciata com'era.
- **Fetta 7 — Secondo passaggio su Telegram (richiesta dell'operatore)**: FATTA. (a) Il NOSTRO funnel rifatto DAL VIVO con /cancellami + /start: due fasi (community: lingua+18enni, interessi, conto; candidatura VIP: 5 passaggi), tutte le opzioni di risposta catturate — «Li avrò a breve» e il consenso esplicito esistono GIÀ; bozze e analisi corrette di conseguenza. (b) Altri funnel competitor visti: Gold Signals, LTD-CAPITAL, CNS VIP, Shmek, Invest360; il bot di ALE STARK provato dal vivo: dopo il «Sì» subentra un umano («aspetta che ti faccio un audio» → vocale di 1:08 → «dimmi il tuo nome»), lì mi sono fermato (regola: niente conversazioni con umani sotto falsa identità). (c) Il vecchio bot «Inizia Ora – welcome REF» non risponde più a /links e /stats: i link dei collaboratori vanno nel bot nuovo.
- **Fetta 6 — Scelta della bozza e correzioni della verifica esterna**: FATTA. L'operatore ha scelto la Bozza B (messaggi). Corretti i finding MEDI del bot sulla PR #392: V-1 (tolta la scarsità finta dal sollecito +72 h; regola «solo numeri veri» estesa), V-2 (avviso di rischio e trasparenza sul compenso in presentazione, ultimo passo e card dei collaboratori), V-3 (consenso esplicito agli aggiornamenti con bottoni Sì/No), V-4 (merge di main nel branch, review #834-MERGE APPROVATO).

## Anomalie / cose da sapere

- Il test dal vivo ha usato /cancellami: lo stato dell'operatore nel bot ora è «Candidato — pronto per la VIP» (prima era «accesso attivo»). Per rimettere lo stato di prima: bottoni «Conto aperto» / «In VIP» sulla scheda nella chat del bot.
- Nella chat «ALE STARK Manager» c'è un loro vocale di 1:08 non ascoltato e la domanda «dimmi il tuo nome»: nessuna risposta inviata, decide l'operatore.
- Il bottone «Pannello» (mini app Telegram) non si apre con l'automazione; per i dati del pannello serve l'operatore o /mielead.
- Nella chat «LEO SUPPORTO» c'è una bozza non inviata nel campo messaggio (già presente); lasciata com'era.
