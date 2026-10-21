# ULTIMO REPORT — 2026-10-21 — Avviso sui file delicati: note di #231; nuovo modo di lavorare

Ramo `feat/merge-automatico-z1xjx2`, dopo il merge di #231 (operatore: «mergia 231 e continua con la roadmap… tieni da parte tutto quello che c'è da mergiare con pro e contro»; poi «salva tutto, ripartiamo dando un clear»).

## DECISIONI UMANE RICHIESTE

1. Merge della PR aperta: pro e contro in `reports/da_mergiare.md`.
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non vi ha accesso).

## Esito

- **Note di verifica esterna e bot su #231, R-388-1/2** — FATTA. Estensioni interne solo eseguibili, parole delicate su tutto il nome, spazi nei pezzi, `tronca_visibile_coda(t, 0)`. Review #390 (chat Motore) APPROVATO CON RISERVE (R-390-1 BASSA, R-390-2 COSMETICA).
- **Nuovo modo di lavorare** — registrato in `reports/stato_progetto.md` e nella nuova coda `reports/da_mergiare.md`.
- **Test** — kernel 949 → 950 PASS, 0 FAIL; pytest tests/ 1582 passed.

## Prossimi passi (per la sessione dopo il clear)

1. R-390-1: rimettere pem, p12, pfx, kdbx, ovpn, gpg, jks, sql, sqlite tra le estensioni interne.
2. Roadmap R1: lanciare un compito o un giro notturno da Telegram.
3. Roadmap 5.2: invio della firma che blocca il turno (R-c4b1-3), bottone Modifica (C6).
4. Roadmap R7: compiti lunghi che riprendono dopo un crash.
