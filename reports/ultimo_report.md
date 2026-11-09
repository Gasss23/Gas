# Ultimo report — 2026-11-08 — voce via Telegram, fetta 1 (chat Mani): vocale → testo

## DECISIONI UMANE RICHIESTE

1. V-2 della verifica esterna #353: l'operatore conferma con un suo commento sulla #353 la regola dei modelli per i vocali senza «forte» (opzione A data a M1 il 7/11).
Prese il 2026-11-09 via M1: sì al merge della #353; fetta 2 con risposta vocale solo dopo un vocale.

## Esito

- **PR #351 (fetta 45)**: MERGIATA (9bfafdb) col sì dell'operatore.
- **Voce via Telegram, fetta 1**: FATTA.
  - Un vocale della chat autorizzata viene scaricato (getFile) e trascritto con Groq; va a Gas come testo.
  - La risposta è in testo, con «Ho capito: «…»» in cima.
  - Tetti PRIMA del download: 60 s, 2 MB, 30 vocali all'ora (GAS_TELEGRAM_VOCALI_ORA). Le chat non autorizzate vengono scartate prima di tutto.
  - «Forte …» detto all'inizio va al cervello forte (stessa regola della voce di casa). /clear e /notte non valgono a voce. Le firme restano sui bottoni.
  - Test: 31 nuovi, aggiunti alla voice suite della CI. Mutanti presi.
  - Review #711/#712 APPROVATO CON RISERVE, #715 (unione) APPROVATO.
- **Proposta Telegram**: FATTA. Sono scritte in cima le decisioni del 7 e dell'8 novembre e corrette le V-1/V-2/V-3 del bot sulla #348.
- **Riserve accettate dall'operatore l'8 novembre**: i vocali senza «forte» seguono le regole dei testi (anche ai gratuiti); GAS_VOCE_FORTE vale anche per i vocali; tetto di 30 all'ora.
- **Merge della PR #352 di M2 nella #353**: FATTO, review #716 APPROVATO.
- **Verifica esterna #353**: APPROVATO CON RISERVE. V-1 BASSA (limite di read() senza test, va nella fetta 2), V-2 BASSA (conferma dell'operatore), V-3 COSMETICA.
