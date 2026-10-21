# ULTIMO REPORT — 2026-10-21 — Avviso file delicati, giro da Telegram (R1), firma in parallelo (5.2), R7, cancello

Ramo `feat/merge-automatico-z1xjx2`, PR #233 (la #232 era già mergiata: ramo riallineato a main). Richieste dell'operatore: lavorare di fila sulla roadmap senza chiedere; un compito e un prompt per una terza chat che non vada in conflitto.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #233: pro e contro in `reports/da_mergiare.md` (voci 1-10). Il check del bot è rosso solo per i caratteri invisibili che il bot stesso ricopia: il testo dei verdetti è APPROVATO CON RISERVE.
2. C6 (bottone «Modifica» e firme a gruppi): decidere (a) lasciare così, (b) disegnare il «Modifica», (c) anche le firme a gruppi.
3. Aprire la terza chat «Mani» col prompt dato in chat (anche in fondo a `reports/lavoro_parallelo.md`).
4. Provare dal vero sul Mac: `python3 gas.py telegram`, poi `/compito <nome>` dal telefono.
5. Fetta cancello (voce 8): secondo passaggio nella chat claude.ai col link della PR.

## Esito

- **R-390-1 + note verifica esterna #232** — FATTA. Review #391 (chat Motore).
- **Compito della chat Mani** — FATTA (solo documento).
- **R1: giro o compito lanciato da Telegram** — FATTA. Review #392, #393.
- **Avviso se il giro muore prima di partire** — FATTA. Review #394, #395.
- **5.2: richiesta di firma in parallelo (R-c4b1-3)** — FATTA. Review #396.
- **5.2: bottone Modifica e firme a gruppi (C6)** — SALTATA: serve una decisione dell'operatore (30 settembre: «niente gruppi»; «Modifica» senza disegno).
- **R7: registro accanto a gas.py, archivio dei vettori con GAS_VECTORS_DB** — FATTA. Review #397.
- **Cancello: caratteri invisibili e lettere travestite (V-1 verifica esterna #233 3° giro, R-398-1, R-399-1)** — FATTA. Review #398, #399, #400.
- **Registro non apribile → Gas parte lo stesso; doctor avvisa; «cmd» segnalato (V-2 bot #233, V-2 verifica esterna #233 4° giro, R-401-1/3)** — FATTA. Review #401, #402.
- **Cancello, 2ª parte: invisibili di ogni tipo senza fondere le parole; /notte@altro bot ignorato (V-1/V-2/V-3 bot #233 5° giro, R-403-1, R-404-1)** — FATTA. Review #403, #404 BOCCIATO (R-404-1 ALTA: regressione introdotta dalla mia fetta #398), #405 APPROVATO CON RISERVE.
- Tutte le altre review: APPROVATO CON RISERVE, nessuna ALTA/MEDIA aperta.
- **Test** — kernel 950 → 957 PASS, 0 FAIL; gate 745 → 811; notte 103; pytest intero 1627 passed (prima della fetta cancello).
- **Verifica esterna #233** — cinque giri, tutti APPROVATO CON RISERVE.
- **Anomalia** — il bot di verifica ha bocciato per «caratteri invisibili nel testo» verdetti che erano APPROVATO CON RISERVE: li avevo incollati nei report; ora sono scritti come `<U+200B>`.

## Prossimi passi

1. R7: compiti lunghi che riprendono dopo un crash (M3) — serve un disegno.
2. Riserve basse: R-397-1, R-395-1, R-396-1.
3. Agganciare lo strumento web della chat Mani quando arriva la sua richiesta.
