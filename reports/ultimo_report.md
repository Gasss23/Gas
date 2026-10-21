# ULTIMO REPORT — 2026-10-21 — Ripresa dei compiti dopo un crash (R7/M3), spesa giornaliera incrementale (5.5)

Ramo `feat/merge-automatico-z1xjx2`, ripartito da main dopo il merge della PR #233 (operatore: «mergia 233… continua fino a che non finisci la roadmap»).

## DECISIONI UMANE RICHIESTE

1. Merge della nuova PR: pro e contro in `reports/da_mergiare.md` (voci 1-5).
2. C6 (bottone «Modifica» e firme a gruppi): (a) lasciare così, (b) disegnare il «Modifica», (c) anche le firme a gruppi.
3. Secondo passaggio claude.ai sulle fette del cancello della #233 (se non già fatto).

## Esito

- **Merge PR #233** — FATTO (`7bd0875`), su richiesta dell'operatore.
- **R7/M3 fetta 1: ripresa dei compiti dopo un crash** — FATTA. Review #406 (chat Motore) APPROVATO CON RISERVE (R-406-1 MEDIA), #407 APPROVATO CON RISERVE (chiude R-406-1/2/3).
- **Riserve piccole (R-407-1/2, R-405-1/2, R-404-2)** — FATTA. Review #408 APPROVATO CON RISERVE.
- **5.5 R-tel-budget-perf: spesa letta solo sulle righe nuove** — FATTA. Review #409, #411 (chat Motore) APPROVATO CON RISERVE.
- **V-1 bot #234, V-4 verifica #234, R-409-1/2/3** — FATTA. Review #410 APPROVATO CON RISERVE.
- **R7 R-fts-1: tetto alle parole delle ricerche** — FATTA. Review #412 APPROVATO CON RISERVE (solo statica: disco temporaneo pieno; suite rieseguita dopo).
- **Budget: date non valide o future ignorate, ultima riga senza a capo contata, gas tokens robusto (V-2 bot #234, V-1 verifica #234, R-411-1, R-413-1/2)** — FATTA. Review #413, #414 APPROVATO CON RISERVE.
- **Anomalie** — disco temporaneo pieno due volte: cloni e ambienti Python degli agenti di verifica, poi ~129.000 cartelle `gas_*` lasciate dai test in /tmp (ripulite: da 4 MB a 29 GB liberi). Un agente di verifica ha staccato l'HEAD del repo vero: commit dei report rifatto sul ramo giusto.
- **Verifica esterna #234** — APPROVATO CON RISERVE, nessuna ALTA/MEDIA. Bot su #234: APPROVATO CON RISERVE (neutral, decide l'operatore).
- **Test** — kernel 957 → 964 PASS, 0 FAIL; gate 811 → 817; notte 106 → 122.

## Prossimi passi

1. R7: ripresa dal punto esatto (rileggere la storia parziale del compito) — valutare.
2. Pulizia delle cartelle temporanee nei test (riempiono /tmp).
3. V-2 bot #234: avviso «ripreso» solo quando il compito parte davvero.
4. R-408-1: potare il registro solo se il file del catalogo è stato letto.
3. Agganciare lo strumento web della chat Mani quando arriva la sua richiesta.
