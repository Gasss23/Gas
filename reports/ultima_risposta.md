Fatto.

Path: `reports/ultimo_report.md`
Branch: `refactor/model-ids-fonte-unica` (pushato, **non mergiato su main** come richiesto)
Hash commit: `160543aa6c2f769a61bdd1812149547bf70de2b3`

Contenuto integrale del report riportato sopra (identico a quello committato).

**Recap semplice:** ho cercato in tutto il progetto dove erano scritti "a mano" i nomi dei modelli AI (5 punti principali + alcuni extra in codice vecchio non collegato al motore attivo). Ho creato un unico file (`brains/model_ids.py`) che li contiene tutti, e fatto in modo che sia `gas.py` sia i vecchi file "brain" li leggano da lì invece di ripeterli — così in futuro basterà cambiare un valore in un solo posto. Nessun modello è stato cambiato, solo la fonte. Il revisore ha approvato con due riserve non bloccanti (proposte nel report, non eseguite perché fuori dallo scope di oggi). Tutto pushato sul branch dedicato, pronto per un merge umano quando vorrai.
