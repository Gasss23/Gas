# DA MERGIARE — coda della chat Motore

> Decisione dell'operatore (2026-10-21): la chat Motore lavora di fila sulla roadmap; qui si accumula ciò che è pronto, una voce per fetta, con i pro e i contro del merge. L'operatore passa 1-2 volte al giorno, legge questa pagina e scrive «mergia #N» oppure «no». Le voci mergiate si tolgono.

> **C6 deciso (2026-10-21):** l'operatore ha scelto (a) «lasciamo così»: una firma per ogni azione, niente «Modifica» né firme a gruppi.


## Da fare domattina (operatore) — messe da parte il 2026-10-21 sera

1. **Ramo della PR #141**: apri https://github.com/Gasss23/Gas/pull/141 e in fondo premi «Delete branch» (la PR è già chiusa; l'agente non ha il permesso di cancellare rami).
2. **Secondo passaggio claude.ai sulla PR #239** (fetta di sicurezza della chat Mani, già mergiata): incolla il link https://github.com/Gasss23/Gas/pull/239 nella chat del progetto Gas su claude.ai e chiedi la verifica; se trova qualcosa, riportalo qui.
3. **Decisione R6 porte** (chat Mani, review #391): `leggi_pagina` oggi accetta qualunque porta (1-65535) verso host pubblici. Rispondi «solo 80/443» oppure «lascia così».

## Coda

### 1. Esito di un'azione firmata non perso dopo un'interruzione (roadmap R7, R-c4b3-3)
- **Cosa:** se Gas si ferma dopo aver preso in carico un'azione che hai firmato ma prima di scriverne l'esito, al nuovo click (o quando Telegram ripete il click) Gas non la riesegue: scrive nella storia l'esito che ha nel database (se manca, «esito INCERTO») e ti manda il messaggio giusto invece di «Nessuna modifica».
- **Pro:** il modello non resta all'oscuro di un'azione firmata; mai una seconda esecuzione.
- **Contro:** l'output dell'azione non c'è più (resta solo l'esito); R-445-3 (cosmetica, già c'era) aperta.
- **Controlli:** revisore #445 e #446 APPROVATO CON RISERVE (riserve chiuse), #447 APPROVATO; kernel 1008 PASS, pytest 1862 passed.
- **Aggiunte dopo (stessa PR #241):** chiuse le riserve del bot e della verifica esterna (testo del recupero, log, test «un click alla volta»; review #450-#452). Nuovo: **resoconto del mattino** (roadmap R1): nel messaggio Telegram del giro notturno spesa delle ultime 24 ore e tetto, lead attivi e fermi da 7+ giorni, firme in attesa — solo numeri, calcolati senza modello (review #453/#454).
- **Pro (aggiunte):** al mattino vedi subito quanto ha speso Gas e quali lead sono fermi, senza aprire file.
- **Contro (aggiunte):** il messaggio del mattino ha 3 righe in più; se la memoria è rotta le righe dicono «non letti»; R-453-2/R-454-1 basse.
- **Ancora:** `ricorda` con `fermi=true` elenca i lead attivi dal più fermo (il blocco di memoria mostrava solo i più recenti); il compito d'esempio punto_lead lo usa. La spesa del mattino avvisa se il log dei token è rovinato (review #455/#456).
- **Controlli (totale):** kernel 1020 PASS, pytest 1897 passed; main (PR #243) già unito, nessun conflitto.
