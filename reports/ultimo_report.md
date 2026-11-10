# Ultimo report — 2026-11-10 — richiesta d'un fiato non più persa sotto «Sì, signore?» (chat Mani)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #368 (https://github.com/Gasss23/Gas/pull/368): riserve solo BASSE; il merge lo fa M1 col sì dell'operatore.
2. Lanciare sul Mac i 3 comandi di lettura del log mandati a M1 (falsi «Hey Jarvis» o turni di seguito?) e incollarne l'output: servono per i default più severi.

## Esito

- **PR #361**: MERGIATA (da M1).
- **Richiesta d'un fiato (prova dal vivo del 10/11, 6 attivazioni su 8 senza richiesta)**: FATTA. In `clients/voice/ascolto.py` dopo la parola si ascolta 0,6 s; con 0,4 s di voce continua niente «Sì, signore?» e si registra da lì. Log della richiesta con secondi di voce e volume massimo in multipli della soglia. Test dell'ascolto: 310 passed (7 nuovi, mutanti presi). Review #753-M1 e #754-M1 APPROVATO CON RISERVE, riserve MEDIA/BASSA chiuse, restano BASSE.
- **V-1 MEDIA della verifica esterna #368**: FATTA (af8ad62). Una coda di «…vis» lunga seguita da una pausa faceva inviare solo la coda; ora si aspetta altra voce continua fino a 5 s, altrimenti non si invia niente. Test 312 passed. Review #755-M1 APPROVATO CON RISERVE (R-755-1-M1 BASSA).
- **V-1 MEDIA / V-2 BASSA della verifica esterna #368, 2° giro**: FATTA (2213519). Una richiesta brevissima d'un fiato («Hey Jarvis, pausa») spariva in silenzio: ora suona «Sì, signore?» e si può ripetere; la voce che parte verso la fine dei 5 s non viene più scartata. Test 314 passed. Review #756-M1 APPROVATO CON RISERVE (R-756-1-M1 BASSA: la conferma di ripiego arriva dopo ~5 s).
- **Scarto delle trascrizioni allucinate («grazie» su audio quasi vuoto)**: SALTATA — sta in modules/voice/stt.py (chat M2) e scartare «grazie» toglierebbe anche quelli veri; proposto a M1.
- **Default più severi contro le risposte non richieste**: DEFERITA — prima i log del Mac.

## Anomalie

Nessuna.
