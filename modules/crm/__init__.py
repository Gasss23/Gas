"""CRM clienti di Gas: chi è cliente, in quali servizi, quanto guadagna e cosa proporgli.

Pezzi:
- `store`     — tabelle `crm_*` in un file SOLO del CRM (`.gas_memory_crm.db`, separato
                dalla memoria di Gas dal 17-11) con le sue copie di sicurezza; registro
                dei movimenti IMMUTABILE, soldi in centesimi.
- `copia_cifrata` — copia giornaliera CIFRATA fuori dal Mac (iCloud Drive) e ripristino.
- `analisi`   — conti puri sui dati (capitale, profitto, commissioni, rendimento per
                servizio, affinità fra servizi): nessuna scrittura.
- `motore`    — il CRM che «legge se stesso»: trova le opportunità (nuovo servizio,
                aumento di capitale, presentazione di amici) e prepara il messaggio.
                Deterministico, zero modelli, zero token: i dati dei clienti non escono.
- `messaggi`  — testi WhatsApp per tipo e livello di insistenza, senza promesse di guadagno,
                e link wa.me col messaggio già scritto.
- `server`    — dashboard web in tempo reale (token, solo dal computer stesso).

Regola che non si tocca (principio del 19 ottobre): tutto ciò che esce verso il mondo
aspetta la firma. Il motore trova e scrive da solo; l'invio al cliente lo conferma
l'operatore con un click.
"""
