# Proposta: terminale e autonomia (Gas e agenti) — bozza M1, 9 novembre 2026

Decisione dell'operatore richiesta (tocca la sicurezza). Niente codice finché non decide.

## Dove siamo
- **M1 sul Mac (Remote Control):** bloccato lato prodotto. Il 9/11 la cartella «Gas» del MacBook è nella lista di Remote Control ma non è offerta alle sessioni cloud, anche dopo l'aggiornamento e il riavvio dell'app. Da qui non si sblocca: si riprova ogni tanto.
- **Gas:** dal 13 ottobre (R0) non ha più comandi di sistema liberi, solo strumenti suoi in Python (leggere, cercare, contare). Motivo: una lista di comandi permessi non si chiude mai (#269–#277).
- **Ponte Gas → sviluppo, strada A** (attivo): Gas scrive una richiesta come issue in `Gas-richieste`, M1 la legge e assegna. Strada B (Gas lancia Claude Code da solo sul Mac) rimandata.

## Opzioni
**A. Azioni fisse di manutenzione per Gas (consigliata come primo passo).**
Gas non riceve una shell: riceve 4-6 azioni con nome, scritte da noi, senza argomenti liberi. Per esempio `aggiorna_gas` (git pull da main + installa.sh), `stato_gas` (doctor), `riavvia_voce`, `log_voce` (ultime righe dei tempi voce). Quelle che cambiano qualcosa passano dalla firma su Telegram (bottoni), mai a voce e mai di notte.
Rischio basso: nessun testo del modello diventa un comando. Ti toglie il copia-incolla di ogni giorno.

**B. Strada B del ponte: Gas lancia Claude Code sul Mac per lavori di sviluppo.**
Gas, con la tua firma, avvia `claude -p` (abbonamento, già usato dal «forte») in una cartella copia del repo, su un branch nuovo, con regole fisse: niente push su main, solo PR, revisore e CI come sempre, tetto di tempo e di spesa, tutto nel diario.
Rischio medio: Claude Code ha una shell vera. Il recinto è il branch più la PR più la tua firma. Serve prima A, e serve decidere chi può avviarlo (solo tu da Telegram con bottoni).

**C. Shell libera per Gas.** Sconsigliata: riapre la classe di problemi chiusa con R0.

## Raccomandazione
1. A subito, in una fetta (M2 o Mani), PR di sicurezza: decide l'operatore.
2. B dopo una settimana di A senza problemi, con una proposta dedicata.
3. Remote Control per M1: si riprova, nessun lavoro da fare.

## Domande per l'operatore
1. A: sì/no? Va bene l'elenco delle azioni (aggiorna, stato, riavvia voce, log voce)?
2. B: rimandata dopo A (consigliato) oppure da preparare subito?
