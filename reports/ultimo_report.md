# Ultimo report — 2026-11-17 — CRM clienti, prima bozza (fetta 1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (dopo bot e verifica esterna).
2. I 4-5 servizi veri: nome, come guadagniamo (% sul profitto, % annua sul capitale, fisso mensile), capitale minimo. Oggi ci sono solo quelli della demo.
3. Invio WhatsApp senza firma: oggi l'operatore approva ogni messaggio (principio del 19 ottobre). L'invio automatico richiede di cambiare quella regola e l'API WhatsApp Business con modelli approvati da Meta.
4. Consenso dei clienti ai messaggi promozionali da raccogliere davvero; verifica con un consulente delle regole Consob sulla promozione di servizi di investimento prima dell'uso vero.

## Esito
- **CRM clienti, fetta 1**: FATTA — commit 99d82f3f, review #803 BOCCIATO (R-803-1 ALTA: con la memoria collegata la dashboard riscriveva il file della memoria a ciclo; R-803-2 MEDIA: corpo non letto eseguito come richiesta; R-803-3 MEDIA: import CSV non atomico) → corretti, ognuno con un test che fallisce sul codice precedente → #804 APPROVATO CON RISERVE (R-804-1..4 BASSE/COSMETICA; R-803-4 MEDIA e R-803-10 BASSA tracciate). Modulo `modules/crm/`: clienti, servizi, posizioni, registro movimenti immutabile in centesimi, proposte, diario del CRM; motore delle opportunità deterministico (nuovo servizio → dopo un no aumento di capitale → presentazione di un amico; consenso, STOP, pause, tetti, insistenza crescente); testi WhatsApp fissi e link wa.me; dashboard in tempo reale su 127.0.0.1 con token; riga di comando e dati demo. Guida: `reports/crm.md`.
- **Gate IP**: FATTA — indirizzi d'esempio di un test marcati `gasmerge-ip-ok` (commit f1c109a7, review #805 APPROVATO).
- **Invio automatico su WhatsApp**: SALTATA — oggi esce solo con un click dell'operatore (principio del 19 ottobre); per l'API servono numero business e modelli approvati.
- **Strumento CRM per il modello di Gas**: DEFERITA — sarà in sola lettura e solo col cervello forte (regola dei modelli); il kernel non è toccato in questa fetta.
- **Integrazioni (broker, risposte WhatsApp automatiche)**: DEFERITE — prossime fette (`reports/crm.md` §7).

## Test
- `tests/test_unit_crm.py`: 93 passed (3 giri stabili; i 13 test `test_r803_*` rigirati sul codice prima delle correzioni: 12 falliti, passa solo quello del keep-alive normale); mypy pulito su `modules/crm`.
- Prova con dati veri (memoria collegata, Playwright): 0 riletture di /api/stato in 10 s a pagina aperta, lead pronti mostrati.
- Suite pytest completa (senza e2e), girata sulla prima versione del CRM (80 test CRM): 4103 passed, 33 failed tutti in `tests/test_unit_web_browser.py`, identici sul commit di partenza: in questo container manca `bwrap` (la CI lo installa). Le correzioni dopo la #803 toccano solo `modules/crm` e la sua suite (rigirata: 93 passed).
- Suite del kernel (`python tests/test_unit_kernel.py`): `=== RIEPILOGO: 1167 PASS, 0 FAIL ===` (kernel non toccato).
- Prova dal vero nel browser (Chromium): quattro schede, approvazione con apertura di WhatsApp, esito «sì», aggiornamento in tempo reale da un altro processo, nessun errore in console.

## Riserve aperte
- R-803-4 (MEDIA): il controllo della regola dei modelli non conosce i clienti del CRM → non scrivere a Gas nomi e guadagni dei clienti finché la fetta «Gas legge il CRM» non lo chiude.
- R-803-9 (decide l'operatore: GDPR), R-803-10, R-804-1..4: vedi `reports/stato_progetto.md`.

## Anomalie
- Il primo giro del revisore ha trovato un difetto ALTO che la prova in demo non poteva vedere (la demo non collega la memoria): la prova con dati veri si fa sempre, anche in bozza.
- Ambiente cloud senza `bwrap`: vedi Test.
