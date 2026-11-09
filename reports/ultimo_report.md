# Ultimo report — 2026-11-09 — voce via Telegram, fetta 4: voce in un thread (chat Mani)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #359: è un CAMBIO DI SICUREZZA (guardia T78p delle firme allargata, opzione b scelta dall'operatore). Resta aperta fino al sì esplicito dell'operatore, anche se il bot dà un verdetto pulito. Consigliato il secondo passaggio nella chat claude.ai col link della PR.
2. Guardia T78p: il revisore (#733) consiglia di fermarsi qui. Le elusioni rimaste (R-733-1/2, BASSE) richiedono codice scritto apposta e visibile in review. L'operatore decide se accettare questo limite della guardia statica.

## Esito

- **PR #357 (fetta 3)**: MERGIATA (524ae96).
- **Voce in un thread (opzione b)**: FATTA (aca5b88; review #725 e #727).
- **Tempi della voce di casa**: FATTA (3404378; review #722).
- **Bot e verifica esterna #359** (V-1 MEDIA: la guardia non vincolava .map; V-2 MEDIA/BASSA: i nomi vietati erano una deny-list incompleta): CORRETTE. La guardia T78p ora è una allow-list. La consegna alla coda può essere solo `submit(_invia_risposta_vocale, base_url, chat_id, finale)`. Le funzioni raggiunte dal thread possono usare solo i nomi, gli attributi e gli import ammessi. Nessun legame può coprire un builtin o un nome del modulo. I legami di modulo si contano in modo esatto. Fuori dalle funzioni sono vietate le scritture su attributi e subscript, e in tutto il modulo l'accesso agli interni (__code__, sys.modules, exec…). Review #729–#733: a ogni giro una nuova classe di elusioni è stata chiusa con mutanti di prova; in tutto 27 mutanti presi su 28 (1 inconclusivo). V-3 (test del Ctrl-C nella pausa), V-4 (docstring) e V-5 (report): FATTE.
- **Merge di main con la PR #358 di M2**: FATTO, review #735.
- Test: telegram_voce, ascolto e voice_server danno 550 passed. Kernel: 1099 PASS, 1 FAIL (T31g, ambiente); T78p PASS.

## Anomalie

Nessuna nel codice della voce. La guardia statica ha richiesto 5 giri di review: è un limite noto dell'analisi per nomi.
