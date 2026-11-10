# Proposta R7 — Direttore v2: compiti lunghi che riprendono dopo un crash (M3, 2026-11-10)

**Oggi.** Un compito in sottofondo (`modules/sottofondo/`, M2) gira in un processo separato. Se il
processo muore (kill, riavvio, crash), alla prima interazione diventa «ko» e l'operatore riceve
«non è finito». Il giro di notte (`modules/notte/`) parte sempre da zero. Nessuna ripresa (prova M3).

## Opzioni

1. **Ripresa automatica del compito in sottofondo (consigliata come fetta 1).** Quando il controllo
   trova il processo morto (non oltre la durata massima), il compito torna «in_coda» e riparte da
   solo, al massimo `GAS_SOTTOFONDO_RIPRESE` volte (default 2). Un file a parte (`<id>.passi`) tiene i
   **progressi** scritti dal kernel (solo NOMI degli strumenti registrati, eseguiti o in attesa di firma;
   mai argomenti o testo letto) e il compito ripreso li riceve nel prompt («hai già usato: …, controlla
   prima di rifare»). Riuso totale di coda, posto unico e avviso di M2; presa del posto sotto lock
   (`fcntl`) così due processi non lo riavviano due volte. A ogni ripresa l'operatore riceve un avviso; per fermare davvero un compito: `python gas.py sottofondo-ferma` (niente ripresa). Esito finale: «ripreso N volte».
2. **Piano scritto dal modello** (strumento `segna_passo(nota)`, piano + passi fatti nel file del
   compito). Ripresa più precisa, ma le note sono testo del modello (possibile eco di testo
   letto): da fare dopo la 1, con lo stesso marchio «non fidato» del diario.
3. **Lista dei lavori ricorrenti con stato** (fatto / in sospeso / fallito / da non ritentare) per il
   giro di notte: il disegno di giugno. Indipendente, utile quando R3/R5 girano davvero.
4. **Avvio della ripresa al boot** (`gas.py sottofondo-riprendi` da launchd/systemd): oggi la ripresa
   scatta alla prima interazione dopo il riavvio. Piccola, va con R5 (server).

## Raccomandazione
Ordine 1 → 4 → 2 → 3. La fetta 1 non tocca la sicurezza: il cancello resta quello di sempre (un'azione
firmata ripetuta dopo la ripresa torna in firma, non parte da sola), nel prompt solo nomi di strumenti registrati (niente testo letto
o inventato), nessun permesso nuovo; il tempo totale resta dentro la durata massima del compito, contata dalla prima creazione (tetto duro).
**Nessuna decisione richiesta all'operatore** per la fetta 1.
