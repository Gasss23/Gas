# Proposta tecnica — Fetta 3: compiti lunghi in sottofondo (chat M2, 6 novembre 2026)

Solo documento (ordine dell'operatore via M1). Nessun codice in questa fetta.

## Problema
A voce un turno con molti giri di strumenti (pagine web, file grandi, più ricerche) tiene l'operatore in attesa 15–20 s e oltre. Il server voce ha un solo thread e un solo kernel: mentre lavora non ascolta altro. Con la fetta 2 (finestra corta, effort basso) i turni semplici si accorciano; quelli lunghi restano lunghi.

## Idea
A voce Gas risponde subito «Ci lavoro, ti avviso quando ho fatto» e il lavoro continua in un **processo separato**. Alla fine avvisa:
- su Telegram con `avvisa_operatore` (esiste dalla #319, un tetto al giorno);
- oppure a voce alla prossima attivazione («Ho finito quello che mi avevi chiesto: …»), letto da una coda su file.

## Quando parte il sottofondo
Due strade, da scegliere:
1. **Lo decide il modello**: uno strumento `in_sottofondo(compito)` offerto solo nei turni parlati (non nel seguito effimero, che non ha strumenti). Il modello lo usa quando il compito è lungo.
2. **Automatico**: se il turno parlato supera N giri di strumenti (es. 3) o T secondi, il kernel interrompe il turno, risponde «Ci lavoro…» e passa il compito al sottofondo.
Consiglio la 1 per partire (prevedibile e testabile), con la 2 come rete più avanti.

## Come gira (concorrenza)
- **Processo separato** con il suo `GasKernel` (stessa cartella, stessa `.gas_history.json`). Niente thread nel server voce: il kernel ha stato condiviso (storia, budget, tetti) senza lock in memoria.
- La storia resta **una sola**: l'unione fra processi esiste già (`_save_history` → `_unisci_storia_altrui`, lock su file `_blocca_storia`). Il compito parte da una copia della finestra al momento della richiesta e alla fine scrive nella storia la coppia «compito → risultato».
- Avvio: `subprocess.Popen([python, "-m", "gas", "sottofondo", <id>])` con il compito in un file di coda (`.gas_sottofondo/<id>.json`, permessi 0600), non negli argomenti (visibili con `ps`).
- Un compito alla volta (lock su file): un secondo «in sottofondo» mentre uno gira risponde «Ne sto già facendo uno».

## Regole che valgono
- **Cervello**: solo il forte (lavori importanti), con il tetto giornaliero `GAS_CLAUDE_CLI_TETTO_USD` e il budget. Forte spento o al tetto → il compito non parte e Gas lo dice subito.
- **Cancello di firma**: invariato. Le scritture irreversibili o dopo una lettura esterna vanno alla firma via Telegram come oggi.
- **Seguiti a voce** (V15): se la finestra contiene un seguito, il compito eredita il «solo forte» e la finestra non fidata.
- **Tetto di 10 iterazioni** per chiamata a `run_turn`: invariato.
- **Fail-safe §9**: un crash del processo scrive l'esito «ko» nella coda e l'avviso dice che il compito è fallito.

## Cosa tocca
- `gas.py`: strumento `in_sottofondo`, comando `gas.py sottofondo <id>`, coda su file, avviso finale. Serve il via su gas.py.
- `modules/voice/server.py`: risposta immediata quando il modello chiama `in_sottofondo`, lettura della coda dei finiti alla prossima attivazione.
- Test: round-trip §7 del processo (con kernel e cervello finti), concorrenza della storia fra due processi, compito fallito, forte spento, tetto.

## Rischi
- Due processi che scrivono la storia insieme: già coperto dal lock su file, ma va provato con processi veri.
- Costo: un compito lungo consuma il tetto del forte; resta visibile nel diario (`turno_fine`).
- Avvisi Telegram: un tetto al giorno già esistente; per il sottofondo potrebbe servire una quota dedicata.
- Il client H24 (chat Mani) non cambia, salvo l'eventuale lettura a voce dei compiti finiti.

## Fette proposte
1. Strumento + processo + avviso Telegram, solo a voce (modello decide).
2. Lettura a voce dei finiti alla prossima attivazione.
3. Passaggio automatico al sottofondo oltre N giri (opzionale).
