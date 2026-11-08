# Ultimo report — 2026-11-08 — voce via Telegram, fetta 1 (chat Mani): vocale → testo

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 1 Telegram: review APPROVATO CON RISERVE (solo BASSE/COSMETICHE) e PR nel perimetro, quindi decide l'operatore via M1.
2. Per la fetta 2: la risposta vocale arriva solo quando l'operatore manda un vocale, oppure sempre?

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
