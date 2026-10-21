# ULTIMO REPORT — 2026-10-21 — Avviso file delicati, giro notturno da Telegram (R1), firma in parallelo (5.2)

Ramo `feat/merge-automatico-z1xjx2`, PR #233 (la #232 era già mergiata: ramo riallineato a main). Richieste dell'operatore: lavorare di fila sulla roadmap senza chiedere; un compito e un prompt per una terza chat che non vada in conflitto.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #233: pro e contro in `reports/da_mergiare.md` (voci 1-6).
2. Aprire la terza chat «Mani» col prompt dato in chat (anche in fondo a `reports/lavoro_parallelo.md`).
3. Provare dal vero sul Mac: `python3 gas.py telegram`, poi `/compito <nome>` dal telefono.

## Esito

- **R-390-1 + note verifica esterna #232** — FATTA. Review #391 (chat Motore) APPROVATO CON RISERVE.
- **Compito della chat Mani** (R6, leggere il web in `modules/web/`) — FATTA (solo documento).
- **R1: lanciare un giro o un compito da Telegram** — FATTA. Review #392 e #393 (chat Motore) APPROVATO CON RISERVE.
- **Avviso se il giro muore prima di partire (R-393-1, R-394-1, V-1/V-3 verifica esterna #233)** — FATTA. Review #394 e #395 (chat Motore) APPROVATO CON RISERVE.
- **5.2: richiesta di firma in parallelo (R-c4b1-3)** — FATTA. Review #396 (chat Motore) APPROVATO CON RISERVE.
- **5.2: bottone Modifica e firme a gruppi (C6)** — DEFERITA: prossima fetta.
- **Test** — kernel 950 → 952 PASS, 0 FAIL; notte 103 passed; gate 760.
- **Verifica esterna #233** — due giri, entrambi APPROVATO CON RISERVE; nessuna ALTA/MEDIA aperta.

## Prossimi passi

1. Roadmap 5.2: bottone Modifica e firme a gruppi (C6).
2. Roadmap R7: compiti lunghi che riprendono dopo un crash.
3. Riserve basse: R-395-1 (nomi del catalogo con «-»/«_» iniziale), R-396-1 (tetto di tempo assoluto per l'invio).
