# ULTIMO REPORT — 2026-10-21 — Ripresa dei compiti dopo un crash (R7/M3), spesa giornaliera incrementale (5.5)

Ramo `feat/merge-automatico-z1xjx2`, ripartito da main dopo il merge della PR #233 (operatore: «mergia 233… continua fino a che non finisci la roadmap»).

## DECISIONI UMANE RICHIESTE

1. Merge della nuova PR: pro e contro in `reports/da_mergiare.md` (voci 1-6).
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
- **Test che riempivano /tmp, cache del modello, avviso «ripreso» (R-415-1/2, R-416-1, V-2 bot #234)** — FATTA. Review #415, #416, #417 APPROVATO CON RISERVE.
- **Ordine delle riprese (V-1 bot #234)** — FATTA. Review #418 APPROVATO CON RISERVE; limite dichiarato R-418-3.
- **Compiti che crashano non affamano gli altri; registro dei costi a blocchi; date future (V-1/V-2 verifica #234 3° giro, V-1 bot #234, R-419-1, R-420-1 — tutte e tre MEDIE chiuse)** — FATTA. Review #419, #420, #421 APPROVATO CON RISERVE.
- **Righe valide lunghe contate; compito «sospetto» resta segnato e va in coda dopo un nuovo crash (V-1/V-2 verifica #234 4° giro, R-421-1/2/3)** — FATTA. Review #422 APPROVATO CON RISERVE (R-422-1/2 BASSE, R-422-3 COSMETICA).
- **Riserve R-422 (avviso per righe enormi, test a cavallo di blocchi)** — FATTA. Review #423 APPROVATO CON RISERVE.
- **Riga finale del registro dei token non riletta a file invariato; avviso «firme scadute» anche in gas_debug.log (V-1 bot e verifica esterna #234 5° giro, R-417-1)** — FATTA. Review #424 APPROVATO CON RISERVE. V-3 verifica esterna non regge (registro toccato solo sotto il lock del giro).
- **R7 / R-222-2: il riepilogo della notte non si fa più ingannare da un file che comincia con «Operazione negata» (l'esito lo dice il kernel); test T94j più stretto (R-424-2/3)** — FATTA. Review #425 APPROVATO CON RISERVE.
- **Anomalie** — disco temporaneo pieno due volte: cloni e ambienti Python degli agenti di verifica, poi ~129.000 cartelle `gas_*` lasciate dai test in /tmp (ripulite: da 4 MB a 29 GB liberi). Un agente di verifica ha staccato l'HEAD del repo vero: commit dei report rifatto sul ramo giusto.
- **Verifica esterna #234** — APPROVATO CON RISERVE, nessuna ALTA/MEDIA. Bot su #234: APPROVATO CON RISERVE (neutral, decide l'operatore).
- **Test** — kernel 957 → 969 PASS, 0 FAIL; gate 811 → 817; notte 106 → 130.

## Prossimi passi

1. R7: ripresa dal punto esatto (rileggere la storia parziale del compito) — valutare.
2. R-408-1: potare il registro solo se il file del catalogo è stato letto.
3. Agganciare lo strumento web della chat Mani quando arriva la sua richiesta.
