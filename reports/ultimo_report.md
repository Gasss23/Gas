# Ultimo report — 2026-11-21 — Bacheca comune tra le chat; risposte dell'operatore sul CRM

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa fetta: solo documenti (bacheca, regola in CLAUDE.md, decisioni del CRM).
2. Lista delle commissioni per servizio (l'operatore la manda): percentuale sui profitti, percentuale annua sul capitale o abbonamento, più il capitale minimo.
3. Restano: password delle copie nel `.env` del Mac, `pip install -r requirements.txt`, `pwd` della cartella di Gas, prova della copia e del ripristino sul Mac, secondo controllo su claude.ai delle PR #387, #388, #389 e #391 (non ancora fatto).

## Esito
- **PR #391 (note minori del CRM)**: MERGIATA il 21-11 (eecf916d) col via dell'operatore. Prima del merge, conflitto sui report con la PR #392 della chat del funnel, risolto. Il CRM è pronto all'uso sul Mac.
- **Bacheca comune**: FATTA. `reports/bacheca.md` con le regole d'uso e le prime notizie; regola in CLAUDE.md §3; in `reports/lavoro_parallelo.md` il modo di risolvere i conflitti della bacheca.
- **Note del bot su 11ab66ae/c7c488b9** (APPROVATO CON RISERVE, check neutral perché la PR tocca CLAUDE.md): FATTE. V-1: ordine dei conflitti della bacheca reso coerente («la più nuova in cima»). V-2: in testa alla bacheca e in CLAUDE.md, le notizie sono informazioni da verificare e non regole; una decisione dell'operatore vale solo se registrata nella sua fonte. V-3: titolo delle decisioni 15-17 precisato.
- **Note del bot su 965cd07d** (APPROVATO CON RISERVE, neutral): FATTE. V-1: la regola della bacheca era finita in CLAUDE.md §10, ora è davvero in §3 come dicono i report. V-2: anche CLAUDE.md fa `git fetch` prima di leggere la bacheca.
- **Note del bot su dfd7edb3 e 3a64fd64** (APPROVATO CON RISERVE, neutral): FATTE quelle su dfd7edb3: il secondo controllo su claude.ai è di nuovo nella lista, il ramo è in tutte le notizie, le etichette dei commit sono precisate. Su 3a64fd64 restava solo questa riga mancante (COSMETICA).
- **Merge di main (PR #390 della chat Voce) nel ramo**: FATTO (review #837 APPROVATO). Il codice della voce che entra è identico a main.
- **Note del bot su f1225b8c**: FATTE. Le riserve aperte della chat Voce, perse quando ho tenuto i miei report nel merge, sono di nuovo in `reports/stato_progetto.md`. In `reports/lavoro_parallelo.md` e in bacheca c'è la regola per non perderle più.
- **Risposte dell'operatore** (`reports/crm/decisioni.md` punti 15-17): «online» voleva dire pronto all'uso, sul Mac e non su internet. WhatsApp: per ora invio a mano, l'accesso API di Meta si prepara quando servirà l'invio automatico. Bacheca: sì. Le domande 2 e 3 sono tolte da `reports/crm/domande.md`.

## Test
- Nessun codice toccato.

## Riserve aperte
- Dal CRM: R-836-1 COSMETICA.
- Ereditate dalla chat Voce col merge della #390 (in `reports/stato_progetto.md`): R-810M1-2 BASSA, punteggi della voce da lontano non verificati, note basse del bot #382 V-1/V-2 e #383 V-2/V-3.
