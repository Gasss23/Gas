# Ultimo report — 2026-11-02 — Mani: piano della mail di Gas (R6), PR doc-only

## DECISIONI UMANE RICHIESTE
0. Merge della PR #324: il sì era sull'head 7346994; dopo, due giri del bot (BOCCIATO, finding MEDIA) hanno cambiato il piano (più protezioni). Serve di nuovo il sì sull'head attuale.
1. Rispondere alle 7 domande in fondo a `reports/piano_mail.md` (casella e provider, accesso OAuth o IMAP, dove sta la credenziale, cosa senza firma, tetti, testo non fidato, GDPR). Niente codice della mail prima delle risposte.

## Esito
- **PR #323 (fetta 37, voce H24)**: `FATTA` — mergiata (9718e0c) col sì dell'operatore; la parola resta «hey_jarvis» per ora.
- **Piano mail**: `FATTA` — `reports/piano_mail.md`, una pagina, senza codice, chiesto da M1.
- **Riserve di #323 in stato_progetto**: `FATTA` — V-1 del bot e V-1…V-6 della seconda verifica esterna su 3672964, registrate senza altri giri (decisione di M1).
- **Bot su 0c0081f (PR #324)**: APPROVATO CON RISERVE (check success). V-1 BASSA (requisito del kernel: output delle mail fuori dalla storia o mai ai gratuiti), V-2 BASSA (V-4 bot #323 registrata), V-3 COSMETICA (numero della PR): `FATTA`.
- **Bot su 9718c6a (PR #324)**: APPROVATO CON RISERVE (check success). V-1 BASSA (nomi degli strumenti come nel cancello: `fetch_email`/`send_email`), V-2 BASSA (handoff riallineato): `FATTA`.
- **Bot su cb84cc0 (PR #324)**: APPROVATO CON RISERVE (check success). V-1 BASSA (`fetch_email` da aggiungere a GATE_ALLOWLIST nella fetta 1), V-2 COSMETICA (V-3 bot #323 registrata): `FATTA`.
- **Bot su 18f2621 (PR #324)**: APPROVATO CON RISERVE. V-1 BASSA (requisito del kernel esteso a tutto il turno mail), V-2 BASSA (main unita dopo la #322, con merge), V-3 COSMETICA (`_LIBERI_DOPO_LETTURA`): `FATTA`.
- **Merge di main (PR #322) nella #324**: `FATTA` in b66ac40, review #626 APPROVATO CON RISERVE; R-626-1 BASSA (tre percorsi verso i gratuiti nel piano) e R-626-2 BASSA (handoff) `FATTA`.
- **Bot su 970beca (PR #324)**: NON approvato (check failure). V-1 MEDIA (quarto percorso verso i gratuiti: pin della memoria e `ricorda`) e V-2 BASSA (`notify_telegram` SAFE): `FATTA` nel piano.
- **Bot su 7346994 (PR #324)**: APPROVATO CON RISERVE (check success), sì dell'operatore. V-1 BASSA (snapshot di `.gas_history.json` per 7 giorni) e V-2 COSMETICA (`test_notify_telegram_safe` da aggiornare nella fetta 1): `REGISTRATE` in stato_progetto, senza altri giri (decisione di M1).
- **Merge di main (PR #325, voce V7b) nella #324**: `FATTA` in 9174640, review #627 APPROVATO; file del perimetro identici a main.
- **Bot su d783938 (PR #324)**: BOCCIATO (check failure). V-1 MEDIA (quinto percorso: file scritti con `write_file` in un turno mail e riletti sui gratuiti) e V-2 BASSA (conservazione del testo contraddittoria; proposta: turno mail tolto o mascherato dalla storia, anche dagli snapshot): `FATTA` nel piano.
- **Bot su a48caa0 (PR #324)**: BOCCIATO. V-1 MEDIA (storia salvata anche a metà turno e copiata negli snapshot: mascheramento a ogni salvataggio, snapshot senza storia mail), V-2 BASSA (sì dell'operatore da richiedere sull'head nuovo), V-3 COSMETICA (nota del §3): `FATTA`.
- **Bot su bd38966 (PR #324)**: BOCCIATO. V-1 MEDIA (rubrica libera dopo una mail: ora con una mail nella finestra resta libero solo `prepara_bozza`), V-2 BASSA (maschera anche sulla storia in memoria), V-3 COSMETICA: `FATTA`.
- **Fetta piccola sulla voce (V-1 ve, V-1/V-4 bot, V-4 ve di #323)**: commit locale bc369ed sul branch voce-fix (review #624 BOCCIATO, #625 APPROVATO CON RISERVE); `DEFERITA — PR subito dopo questa (un solo branch remoto)`.
