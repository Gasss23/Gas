# DIFF SESSIONE — 21 novembre 2026 (simulazione funnel + conteggi vecchi)

> Questo file si riscrive a ogni sessione; la storia completa sta in git.
> Sessione-bis dopo il merge della PR #392 (funnel community); branch ripartito da main eecf916 (dopo il merge della PR #391, CRM).

File toccati (tutti doc, nessun file del motore):

- `reports/funnel/simulazione_funnel.html` — NUOVO: simulazione cliccabile stile Telegram del funnel Bozza B (3 passaggi), del link diretto `-vip` e del Pannello «I miei link»; testi presi da `funnel_v2.md` e `tasto_collaboratori.md`; provata dal vivo in tutti e tre i percorsi.
- Secondo giro (stessa sessione): corretti i finding del 1° verdetto del bot sulla PR #393 — V-1 (contatore di generazione: niente percorsi mescolati cambiando scheda), V-2 (righe proposte dall'agente marcate con * e dichiarate nei report; percorso diretto riallineato alla spec §3.1; claim «alla lettera» corretto), V-3 (textContent al posto di innerHTML). Pagina ripubblicata e riverificata.
- Terzo giro (stessa sessione): corretti i finding del 2° verdetto del bot — V-1 (claim «alla lettera» allineato anche nell'handoff), V-2 («ultimo passo» col testo della Bozza A di funnel_v2 + riga sul rischio), V-3 (bolla del consenso sopra la tastiera; nome azzerato a ogni start) — e merge di origin/main nel branch (019c6c8, conflitto creato dalla PR #390 sui report canonici; review #837-MERGE APPROVATO, perimetro byte-identico a main).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — riscritti per questa sessione (fotografia dell'ultima sessione). La nota bassa del bot sulla #392 (conteggi «7 domande»/«4 domande») è superata: la riscrittura dei report fatta dalla PR #391 li aveva già tolti da main, e questi non li ripropongono.
