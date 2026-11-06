# Ultimo report — 2026-11-06 — Voce rapida, fetta 2 (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 2 (con riserve: sì dell'operatore via M1).
2. Sul Mac: misurare i tempi del cervello a voce (log `gas.voce.tempi`, prima 3,9–16,9 s) e controllare `claude --help | grep effort`.

## Esito delle fette

- **PR #342** (parser del bot): `MERGIATA` (c131452) con CI verde, bot neutral e verifica esterna senza ALTA/MEDIA.
- **Fetta 2 voce rapida**: `FATTA` — a voce finestra di 6 messaggi, niente recap vecchio, `--effort low` del forte con ripiego, C1 «rispondi solo all'ultima»; review #689-M2 APPROVATO CON RISERVE (R-689-1-M2 BASSA, R-689-2-M2 COSMETICA).
- **Tempi prima/dopo**: `NON FATTA — serve il Mac`.
- **Fetta 3 (documento)**: `DEFERITA`.
- Test: kernel 1089 PASS 0 FAIL; claude_cli 49 passed; voce 518 passed.

## Anomalie

- La fetta 2 è stata committata su un branch locale mentre la #342 era aperta e poi portata sul branch col cherry-pick (stesso diff revisionato).
