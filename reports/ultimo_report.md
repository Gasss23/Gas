# ULTIMO REPORT — 2026-10-21 — Tre stati per un comando firmato (R7, R-c4b3-5)

Ramo `feat/merge-automatico-z1xjx2`, ripartito da main dopo il merge della PR #234 (operatore: «mergia 234 e continua con la roadmap»; C6 decisa «lasciamo così»).

## DECISIONI UMANE RICHIESTE

1. Merge della nuova PR: pro e contro in `reports/da_mergiare.md`.

## Esito

- **Merge PR #234** — FATTO (`35b55be`) su richiesta dell'operatore, dopo aver unito main (#235 della chat Mani, review #427 APPROVATO) per togliere il conflitto.
- **C6** — DECISA dall'operatore: (a) «lasciamo così» (una firma per azione, niente «Modifica» né firme a gruppi). Registrata in roadmap e da_mergiare.
- **R7 / R-c4b3-5 — tre stati per un comando firmato** — FATTA. Un run_command firmato che parte e si interrompe (tempo scaduto) ora risulta «PARTITO, esito INCERTO» nella storia, nel diario e su Telegram, non più «NON eseguito (diniego interno)». Review #428 APPROVATO CON RISERVE (R-428-1 MEDIA).
- **R-428-1/2/3/4** — FATTA. Il segno «partito» si azzera a ogni tool call (non sporca più il diario di azioni negate o parcheggiate dopo); un errore di avvio (binario assente) non è «incerto»; anche il modello legge «PARTITO… esito INCERTO» senza l'argv di bwrap. Review #429 APPROVATO CON RISERVE (R-429-1 BASSA, R-429-2 COSMETICA).
- **Test** — kernel 971 → 975 PASS, 0 FAIL (T77u, T77v, T77w).

## Prossimi passi

1. R-429-1: due test mancanti (errore di avvio, meta residuo su azione parcheggiata).
2. R7 / R-c4b3-4: due processi che scrivono la stessa cronologia (lock + accodamento dei messaggi nuovi).
3. R7 / R-c4b3-3: crash tra reclamo e scrittura in storia.
4. R-408-1: potare il registro della notte solo se il file del catalogo è stato letto.
