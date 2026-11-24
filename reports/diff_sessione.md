# DIFF SESSIONE — 23 novembre 2026 (ritocchi finali del funnel)

> Questo file si riscrive a ogni sessione; la storia completa sta in git.
> Branch claude/ritocchi-simulazione da main (post merge PR #396 funnel e #397 CRM).

File toccati (tutti doc, nessun file del motore):

- `reports/funnel/funnel_v2.md` — nuova prima regola comune: via la domanda «Da quale community arrivi?» dalla fase 1 (decisione dell'operatore 23/11); allineati i due punti che dicevano «la fase 1 resta com'è».
- `reports/funnel/tasto_collaboratori.md` — §3.1 riscritto: percorso diretto SOLO nome e cognome, con la riga «confermi 18 anni e ci autorizzi a risponderti»; §4.5 tutele aggiornate (consenso promo non chiesto nel diretto → niente promozione senza sì); §4.6 nuovo requisito: «I miei link» vive DENTRO il Pannello blu esistente.
- `reports/funnel/simulazione_funnel.html` — fase 1 senza la domanda della community; flusso diretto rifatto (messaggio unico → campo nome con riga 18 anni → CTA), funzione `ctaConConsenso` rimossa perché non più usata; nota del Pannello blu nella scheda agente. Ripubblicata sulla pagina pubblica e provata dal vivo.
- `reports/stato_progetto.md` — voce Funnel aggiornata (PR #396 mergiata, i tre ritocchi, cosa resta).
- Secondo giro (note del 1° verdetto bot su #401): lingua del diretto dichiarata in `tasto_collaboratori.md` (§3.1, §4.5) e nella simulazione; card «solo nome e cognome»; rimando all'eccezione del diretto nella regola del consenso di `funnel_v2.md`; handoff §3/§6 coi commit reali.
- Terzo giro (note del 2° verdetto bot su #401): riga sul rischio nell'ultimo passo del diretto (spec + simulazione); fase 1 di oggi descritta con la domanda della community; «Fetta 1» al posto di «Fetta unica». Merge di origin/main (PR #398, chat Voce) nel ramo: conflitto sui 3 report canonici risolto coi nostri, perimetro identico a main (review #851-MERGE APPROVATO); `.claude/agents/memoria_revisore.md` con la riga #851.
- Quarto giro (note del 3° verdetto bot su #401, ok dell'operatore 24/11): conferma 18 anni in testa al messaggio unico del diretto; «ai lead del diretto il bot non manda MAI promozione» in spec, funnel_v2 e simulazione; 2° merge di origin/main (PR #399 e #400).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — riscritti per questa sessione.
