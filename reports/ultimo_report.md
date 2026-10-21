# ULTIMO REPORT — 2026-10-21 — Avviso file delicati (R-390-1) e giro notturno da Telegram (R1)

Ramo `feat/merge-automatico-z1xjx2`, PR #233 (la #232 era già mergiata: ramo riallineato a main). Richieste dell'operatore: lavorare di fila sulla roadmap senza chiedere; un compito per una terza chat che non vada in conflitto.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #233: pro e contro in `reports/da_mergiare.md` (voci 1-4).
2. Aprire la terza chat «Mani» col prompt in fondo a `reports/lavoro_parallelo.md`.
3. Provare dal vero sul Mac: `python3 gas.py telegram`, poi `/compito <nome>` dal telefono.

## Esito

- **R-390-1 + note verifica esterna #232** — FATTA. Review #391 (chat Motore) APPROVATO CON RISERVE.
- **Compito della chat Mani** (R6, leggere il web in `modules/web/`) — FATTA (solo documento).
- **R1: lanciare un giro o un compito da Telegram** — FATTA. Review #392 (chat Motore) APPROVATO CON RISERVE.
- **Rifiniture R-392-1/2 e V-3 verifica esterna #233** — FATTA. Review #393 (chat Motore) APPROVATO CON RISERVE. V-2 #233 non serve: i `.sh`/`.py` finali vanno già alla firma (livello 2), l'avviso guarda solo i file liberi.
- **Test** — kernel 950 PASS, 0 FAIL; notte+gate 858 passed.
- **Verifica esterna #233** — APPROVATO CON RISERVE (V-1 MEDIA handoff mancante, rigenerato ora).

## Prossimi passi

1. R-393-1: avvisare quando il giro lanciato dal bot muore prima di partire.
2. Roadmap 5.2: invio della firma che blocca il turno (R-c4b1-3), bottone Modifica (C6).
3. Roadmap R7: compiti lunghi che riprendono dopo un crash.
