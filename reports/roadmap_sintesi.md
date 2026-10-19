# Gas — roadmap in una pagina (2026-10-19, per la discussione a voce)

Fonte completa: `reports/roadmap.md` + `reports/stato_progetto.md`. Questa pagina è solo un riassunto.

## Dove siamo

| Fase | Cosa | Stato |
|---|---|---|
| 1 | Sicurezza del terminale (snapshot, sandbox) | ✅ chiusa |
| 2 / 2.5 | Memoria (diario, contatti, ricerca) e compressione della storia | ✅ chiuse |
| 2.6 | Gas impara da solo: riflessione a fine compito e a `clear`, lezioni con il tuo sì, recap pertinente | ✅ fette 1–3 fatte e provate sul Mac (3 prove) |
| 3 | Voce (microfono → Gas → audio) | ✅ completata |
| 4.5 | Giro notturno sul Mac + riepilogo su Telegram | ✅ fette 1–2 fatte; manca la prova di una notte vera con la riflessione |
| Cervello forte | Claude via API come gradino «forte» (a pagamento, spento di default) | fetta 1 (tetto di spesa) fatta; fette 2–4 ferme sul tuo setup della Console |
| 4 | Marketing (lead, Meta Ads, funnel) | ⬜ non iniziata, «tra gli ultimi» |
| 5 | VPS h24 | 🔴 da rifare da zero, rimandato |

Ordine che avevi dato: italiano ✅ → auto-apprendimento (quasi fatto) → marketing → VPS.

## Decisioni da prendere a voce

1. **Cervello forte (Fetta C)**: lo facciamo adesso? Serve che tu prepari la Console Anthropic (workspace «gas» con limite di spesa mensile, chiave nel `.env`, niente ricarica automatica). Da scegliere: il modello di default (proposta: Sonnet 5.5) e il tetto giornaliero (proposta: 2 $).
2. **Dopo la 2.6, cosa?** (a) un giro notturno più utile, con compiti veri sui lead; (b) l'inizio del marketing (FASE 4); (c) il VPS. Prima va presa una decisione di architettura aperta da luglio: Gas fa tutto in Python, oppure Make (strumento senza codice) orchestra e Gas fa la parte intelligente.
3. **Divieti di scrittura per nome (R-223-2)**: oggi Gas non può scrivere una lista di file pericolosi. L'alternativa più solida è che scriva solo in cartelle permesse. Da decidere prima di dargli più autonomia.
4. **Pulizia dei branch vecchi**: vedi `reports/ultimo_report.md`. C'è un solo branch obsoleto da cancellare (lo cancelli tu oppure dai l'ok).
