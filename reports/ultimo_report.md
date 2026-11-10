# Ultimo report — 2026-11-10 — richiesta d'un fiato non più persa sotto «Sì, signore?» (chat Mani)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #368 (https://github.com/Gasss23/Gas/pull/368): riserve solo BASSE; il merge lo fa M1 col sì dell'operatore.
2. Lanciare sul Mac i 3 comandi di lettura del log mandati a M1 (falsi «Hey Jarvis» o turni di seguito?) e incollarne l'output: servono per i default più severi.

## Esito

- **PR #361**: MERGIATA (da M1).
- **Richiesta d'un fiato (prova dal vivo del 10/11, 6 attivazioni su 8 senza richiesta)**: FATTA. In `clients/voice/ascolto.py` dopo la parola si ascolta 0,6 s; con 0,4 s di voce continua niente «Sì, signore?» e si registra da lì. Log della richiesta con secondi di voce e volume massimo in multipli della soglia. Test dell'ascolto: 310 passed (7 nuovi, mutanti presi). Review #753-M1 e #754-M1 APPROVATO CON RISERVE, riserve MEDIA/BASSA chiuse, restano BASSE.
- **Scarto delle trascrizioni allucinate («grazie» su audio quasi vuoto)**: SALTATA — sta in modules/voice/stt.py (chat M2) e scartare «grazie» toglierebbe anche quelli veri; proposto a M1.
- **Default più severi contro le risposte non richieste**: DEFERITA — prima i log del Mac.

## Anomalie

Nessuna.
