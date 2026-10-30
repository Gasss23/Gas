# GAS — ROADMAP COMPLETA

> Aggiornata il 19 ottobre 2026.
> Base: la roadmap completa dell'11 ottobre (`main` al commit `ea4a368`), più gli avanzamenti fino al 19 ottobre (`main` al commit `2536ffd`, PR #219) e le decisioni prese dall'operatore il 19 ottobre in chat vocale.
> È la fonte unica della roadmap (regola di `CLAUDE.md` del 19 ottobre): la copia nel progetto claude.ai va tolta.

**Simboli:** ✅ fatto · 🔄 in corso · ⏳ da fare · 🔒 bloccato da altro · 👤 tocca a te · 🅿️ parcheggiato · ❌ scartato.
Le sigle tra parentesi (es. R-203-2) servono solo a ritrovare la voce nei file.

---

## 0. In una pagina

**Dove vogliamo arrivare.** Gas fa da solo lavori complessi, giorno e notte, e chiede la tua firma solo per le azioni delicate. Gli parli a voce da ovunque.

**Dove siamo.** Il motore è solido: memoria, voce in locale, cancello con firma su Telegram, giro notturno, lezioni, riflessione automatica, controlli automatici sul codice. Gas legge, cerca e conta con strumenti suoi (niente più comandi di sistema). Però non ha ancora mani verso il mondo (niente web, niente mail), ha un cervello gratuito e debole, e gira solo se il Mac è acceso.

**Le rocce grosse, in ordine.**

| # | Roccia | Stato |
|---|---|---|
| R0 | Chiudere la classe "comandi di sistema" | ✅ fatto (11-13 ott) |
| R1 | Giro notturno provato dal vero | ⏳ |
| R2 | Cervello forte: Claude con l'abbonamento Max 5x di Gas | 🔄 fetta 1 fatta (12 ott) |
| R3 | Turno di notte dello sviluppo (in cloud, sull'abbonamento) | ⏳ |
| R4 | Protezioni di base: backup cifrato, repo chiuso agli estranei | ⏳ 👤 |
| R5 | Server sempre acceso (Netcup) | ⏳ 👤 |
| R6 | Le mani: web, mail, social, notifiche (missioni M1 e M2) | ⏳ |
| R7 | Direttore v2: compiti lunghi che riprendono dopo un crash (M3) | ⏳ |
| R8 | Voce "Jarvis" sempre disponibile (M5) | ⏳ 🔒 R5 |
| R9 | Imparare da solo | 🔄 riflessione automatica fatta |
| R10 | Aggiustarsi e programmarsi da solo, dentro il recinto | ⏳ 🔒 R5 |
| R11 | Motore marketing | ⏳ tra gli ultimi |
| R12 | Controllo del PC | 🅿️ |
| R13 | Secondo cervello personale | 🅿️ 🔒 R5 |

**L'ordine è confermato** (19 ottobre): queste rocce, in quest'ordine, con il server anticipato a R5. Supera l'ordine scritto del 14 e 21 settembre (server rimandato).

**Principio dell'autonomia (19 ottobre).** "Dentro Gas autonomia piena; tutto ciò che esce verso il mondo aspetta la firma." Tutto ciò che è reversibile e interno a Gas è libero, anche dopo una lettura. La firma resta solo per: (a) codice madre, (b) sicurezza, (c) azioni verso l'esterno (mail, messaggi, post, social, moduli), (d) azioni irreversibili o delicate. Supera la regola C-d e la decisione R-203-2.

**Regola dei modelli (19 ottobre).** I lavori importanti e tutti quelli con dati di clienti passano solo dai modelli forti (Claude). Se Claude non è disponibile aspettano in coda finché i limiti ripartono: non passano mai ai modelli gratuiti. Ai modelli deboli o gratuiti vanno solo i lavori semplici senza dati personali (riassunti, rubrica). L'etichetta "importante" la dà una regola fissa o Gas-operatore quando assegna il compito, mai il modello.

---

## 1. La destinazione

"Finito" vuol dire che Gas supera da solo queste prove (approvate da te il 28-29 settembre):

- **M1 — lavoro autonomo:** "trova 10 potenziali clienti di tipo X e salvali in rubrica con la fonte". Zero domande.
- **M2 — cancello:** "scrivi e manda una mail a 3 di loro". Le bozze le fa da solo, per l'invio chiede la firma.
- **M3 — resistenza:** un compito lungo interrotto a metà (crash, provider giù, riavvio). Riprende e finisce.
- **M4 — attacco:** durante una missione legge un testo malevolo. Non lo esegue e non scavalca il cancello.
- **M5 — voce h24:** gli parli da ovunque e lui lavora sul server.

Tu hai aggiunto: queste prove ci avvicinano molto, ma il finito pieno è autonomia altissima più voce praticamente sempre disponibile.

**Principi che non si toccano.**
- Robustezza prima della potenza, zero crash.
- "La memoria non deve mentire."
- Le operazioni irreversibili stanno fuori dalla mano del modello.
- Quando un controllo fallisce, si chiude (non si lascia passare).
- Due budget mai confusi: sviluppo e funzionamento di Gas.
- Mai simulare il risultato di uno strumento.
- Mai tagliare la cronologia a fette grezze.
- Ogni modifica al motore vuole una prova vera del giro completo.
- In prova si approva tutto a mano; poi si allenta solo sul reversibile.

---

## 2. Cosa c'è già

### Motore
- ✅ **FASE 1 — sicurezza del terminale** (giugno): foto di sicurezza prima di ogni scrittura, blocco dei percorsi fuori cartella, comandi senza shell, modalità di prova a secco, recinto di sistema (bwrap) con rete chiusa, tetto alla finestra di conversazione, `gas doctor`.
- ✅ **FASE 2 — memoria** (giugno): diario che non si può riscrivere, rubrica contatti, ricerca per parole, ricerca per significato (spenta se non la accendi), backup automatico, comandi `reindex`, `backup`, `tokens`, `duplicati`, tetto di spesa giornaliero.
- ✅ **Bot Telegram** per parlare con Gas dal telefono (`gas telegram`, 27 giugno).
- ✅ **FASE 2.5 — compressione della cronologia** (27 giugno).
- ✅ **Revisione delle fondamenta** (15 luglio): verdetto "solide"; chiusi il buco del diario riscrivibile e il salvataggio non sicuro della cronologia; tolti 17 file morti.
- ✅ **Cascata dei modelli**: Gemini flash-lite → Gemini flash → Groq → OpenRouter gratuito → Ollama. Nomi dei modelli in un file solo. (Ollama è rimosso dal piano dal 19 ottobre: oggi è ancora nel codice.)
- ✅ **Gas risponde sempre in italiano** (21 settembre).
- ✅ **Calcolatrice obbligatoria** per i conti (1 settembre).

### Voce
- ✅ **FASE 3 — giro vocale completo** (15 settembre, PR #90): microfono → trascrizione Groq → Gas → voce ElevenLabs. Endpoint con token, client di prova, client nel browser. Provata con voce vera il 22 agosto. Tetto alla lunghezza del testo da leggere.
- ✅ Token della voce rigenerato il 15 settembre.

### Autonomia
- ✅ **Studiare** (settembre): conoscenza in un archivio separato, solo da fonti approvate, con sei protezioni contro i testi malevoli. Attacco di prova respinto.
- ✅ **Quaderno delle lezioni** (28 settembre, PR #101): le lezioni entrano nel comportamento solo se le approvi tu.
- ✅ **Riflessione a fine lavoro** (7 ottobre): `gas rifletti` scrive un riassunto e propone al massimo 3 lezioni in quarantena.
- ✅ **Cancello** (1-3 ottobre): ogni azione è libera, da firmare, o vietata. Coda delle firme, messaggio su Telegram con l'azione esatta, bottoni Approva e Rifiuta, esecuzione una sola volta.
- ✅ **Scrittura a 3 livelli** (11 ottobre): file normali liberi; codice solo con la tua firma e il diff vero davanti; segreti, memoria e cancello mai.
- ✅ **Gas legge il proprio codice** ma non lo tocca senza firma (11 ottobre, PR #181).
- ✅ **Giro notturno, fetta 1 e 2** (8-10 ottobre): `gas notte` esegue un elenco di compiti, con tetti di tempo e di spesa, e manda il riepilogo su Telegram.
- ✅ **Gas carica da sé il file delle chiavi** (11 ottobre).
- ✅ **Strumenti suoi per leggere, cercare e contare** (11-13 ottobre, R0): `elenca_cartella`, `leggi_righe`, `cerca_testo`, `conta_file`, `data_ora`. I comandi di sistema non sono più nella mano del modello.
- ✅ **Tetto di spesa ricontrollato prima di ogni chiamata** (12 ottobre, R2 fetta 1).
- ✅ **Riflessione automatica** a fine compito notturno e a `clear`, e **ripartenza dal riassunto pertinente** con scadenza (15-16 ottobre, PR #211, #213, #215, #216). Provate sul Mac.

### Controlli sul lavoro di sviluppo
- ✅ Revisore obbligatorio prima di ogni modifica al motore, con cancello automatico. Revisore sempre sul modello più forte, sessione di lavoro su quello leggero.
- ✅ `main` chiuso a chiave: si entra solo con PR e tre controlli verdi.
- ✅ Test automatici a ogni push: 895 controlli del motore più 1450 test degli altri gruppi (19 ottobre).
- ✅ Dossier di fine lavoro e due controlli automatici sul dossier.
- ✅ Verifica esterna con un agente nuovo a ogni giro (3 ottobre). Per le fette di sicurezza, secondo controllo nella chat di strategia.
- ✅ **Bot di verifica con identità separata** (6-7 ottobre): giudica ogni PR. Quattro prove dal vero; valida la quarta.
- ✅ Merge autonomo dell'agente solo col sì pulito del bot (regola dell'8 ottobre). Eccezione: le PR di soli registri di sessione, con test verdi.
- ✅ **Agente senza poteri di amministratore sul repo** (G-3, 14 ottobre): token ristretto `gas-agente` (scade il 4 gennaio 2027), avvio con `gasclaude`; `gasmerge --auto` si ferma se il token non è quello verificato.
- ✅ `gasmerge`, il comando di merge con i suoi controlli. Le sue riserve di luglio sono chiuse.
- ✅ Risposte brevi obbligatorie e niente stampa dei report a schermo (11 ottobre).

### Macchine
- ✅ Passaggio da Windows al MacBook, certificato (12 settembre).
- ✅ Comando dello sviluppo dal telefono (15 luglio). Regole che restano: "chiedi prima di agire", accesso solo alla cartella del repo, controllo del PC spento, mai permessi dati in anticipo; funziona solo a computer acceso.
- ❌ Server Hetzner **perso** il 14 settembre per mancato pagamento. Oggi non esiste nessun server.

---

## 3. Cosa può e non può fare Gas oggi

**Strumenti del modello (11):** leggere un file, leggere un pezzo scelto di un file, scrivere un file, elencare una cartella, cercare un testo, contare file, data e ora, cercare in memoria, salvare un contatto, cambiare lo stato di un contatto, fare un calcolo. Nessun comando di sistema.

**Non può:** andare sul web, mandare mail o messaggi, usare git, aprire PR, toccare la propria memoria o il cancello. Per modificare un file deve riscriverlo intero.

**Limiti del giro notturno.**
- Massimo 10 compiti per giro, 15 minuti l'uno, 2 ore in tutto. I tetti di tempo non sono duri: nel caso peggiore sfora di circa 36 minuti.
- Massimo 10 passi di ragionamento per ogni modello della cascata.
- Tetto di spesa: 1 dollaro in 24 ore se non ne metti un altro. Il conto usa i prezzi di listino anche per i modelli gratuiti, quindi può scattare senza spesa vera.
- Ogni compito parte da zero, senza ricordare la conversazione con te.
- L'elenco dei compiti sta fuori dalla sua cartella: non può aggiungersene da solo.
- Le azioni rischiose aspettano la tua firma. **La firma di giorno scade dopo 30 minuti**. Massimo 5 richieste in attesa. Dal 20 ottobre le richieste del giro notturno durano 24 ore.
- Dal 20 ottobre, dopo aver letto qualcosa (un file, la memoria) restano liberi la rubrica e la scrittura dei file normali; restano alla firma `reports/`, `knowledge/`, il codice e tutto ciò che esce verso il mondo (principio al capitolo 0).
- Non può leggere la cartella del giro notturno: non sa dirti cosa ha fatto stanotte.
- Il cervello è gratuito: va bene per riassunti e rubrica, non per lavori difficili.
- Parte solo se il Mac è acceso alle 03:00 (se dorme, parte al risveglio).
- Per eseguire un'azione firmata deve essere acceso anche il bot Telegram.

---

## 4. Le rocce grosse, una per una

### R0 — Chiudere la classe "comandi di sistema" ✅ (11-13 ottobre)
**Perché.** Da #269 a #277 quasi ogni revisione ha trovato un nuovo modo di abusare di `grep`, `date`, `uniq`, `file`. Una lista di comandi di sistema non si chiude mai.
**Cosa.** Gas legge (anche un pezzo scelto di un file lungo), cerca, conta ed elenca con funzioni sue scritte in Python. I comandi di sistema escono dalla sua mano.
**Chiude:** R-273-1, R-273-2, R-274-2, R-nw-2 (nomi di file innocui rifiutati), la trappola della cartella di lavoro sul server, la firma inutile sul Mac, il messaggio che suggerisce un comando vietato (F4 delle fondamenta), `echo` nella lista (F6 del prompt), il rischio di fuga di dati nella modalità senza recinto.
**Guadagno in più.** Funziona anche sul Mac. Gas può leggere i file lunghi.
**Fatto:** strumenti nativi (PR #184, 11 ottobre), comandi di sistema tolti dalla mano del modello (11 ottobre), budget onesto di `cerca_testo` e chiusure della lista #197 (12-13 ottobre).
**Resta:** R-277-1 (file con nomi tipo `prod.environment` leggibili): provato che resta leggibile anche dagli strumenti nuovi, compromesso aperto.

### R1 — Giro notturno provato dal vero ⏳
Finché non passa, "Gas lavora di notte" non è vero. Nessun lavoro autonomo su un server finché i bottoni di firma non sono provati con un click vero.
- ✅ Messaggio del mattino su Telegram arrivato (prova dell'operatore, 22 ottobre, giro lanciato con `/notte`).
- ✅ Bottoni Approva e Rifiuta provati con un click vero (22 ottobre): Approva scrive il file, Rifiuta non esegue nulla. Emerso un difetto (il modello chiedeva i pro e contro all'utente): corretto lo stesso giorno.
- ✅ **Durata della firma** (decisa il 19 ottobre, nel codice dal 20 ottobre): 24 ore per le richieste del giro notturno (`GAS_APPROVAL_TIMEOUT_NOTTE_SECS`); di giorno restano 30 minuti (`GAS_APPROVAL_TIMEOUT_SECS`). Si cambia dal file delle chiavi.
- ✅ **Autonomia dopo una lettura** (decisa il 19 ottobre, nel codice dal 20 ottobre; supera C-d e R-203-2): dopo una lettura restano liberi la rubrica (`salva_contatto`, `imposta_stato_contatto`) e `write_file` sui soli documenti `.md`, `.txt`, `.csv` di livello 1 (con foto di sicurezza; script, pagine web, file di avvio, configurazioni e file nascosti restano alla firma, V-1 verifica esterna #222). Restano alla firma: codice madre (livello 2), azioni verso l'esterno e irreversibili, e — come «sicurezza» — `reports/` (la leggono revisore e bot) e `knowledge/` (catalogo delle fonti di studio), e i file ignorati da git (non entrano nella foto di sicurezza, es. `gas_debug.log`). Il controllo vale anche sul file vero (cartella di lavoro, symlink). La contaminazione non si ricicla dalla memoria: un contatto o un'azione scritti dopo una lettura restano segnati «non fidati», e il turno che li rivede nel blocco di memoria è a sua volta contaminato (V-1 bot #222).
- ✅ Scadenza delle firme (fetta C5, 20 ottobre): chiusa dal bot e dal giro, mostrata in `gas doctor`, avviso «approvazione scaduta».
- ⏳ 👤 Archivio della conoscenza mai creato sul Mac (avviso `knowledge_fts`).
- ✅ Mac riallineato a `main` (43a2545) e timer `com.gas.notte` installato (22 ottobre); catalogo `~/.gas_notte.yaml` dall'esempio, tetto `GAS_DAILY_TOKEN_BUDGET=1.0`.
- ✅ Contatti fermi (22 ottobre): `ricorda fermi=true` e compito d'esempio punto_lead. ⏳ Riempire il catalogo vero sul Mac con lavori veri. ✅ Resoconto di spesa e stato (21 ottobre): lo calcola il kernel a fine giro, senza modello, e va nel messaggio del mattino (solo numeri).
- ✅ Giro lanciato da Telegram con `/notte` (codice dal 21 ottobre, provato dal vero il 22).
- La prova si fa a mano e di giorno. Per le notti vere serve R5.

### R2 — Cervello forte: Claude con l'abbonamento 🔄
**Riscritto il 19 ottobre.** Gas usa Claude con l'abbonamento **Max 5x di Gas**, tramite `claude -p` / Agent SDK, nei limiti del piano.
- ⚠️ Le regole Anthropic sull'uso dell'abbonamento sono cambiate più volte nel 2026: **riverificare sulla pagina ufficiale prima di costruire**.
- ✅ **Regole riverificate il 23 ottobre** (`reports/r2_regole_abbonamento.md`): con l'abbonamento `claude -p`/SDK consumano i limiti del piano, ma l'uso automatico su server è ambiguo per le Consumer Terms; il Max 5x include ora **100 $ al mese di crediti API**, validi con una API key (uso automatico esplicitamente permesso). ✅ 👤 Decisione del 23 ottobre: **via B** (`claude -p` col login dell'abbonamento, rischio dichiarato accettato). ✅ Fetta 1 (adattatore `brains/claude_cli.py` + rung «forte» senza ripiego sui gratuiti, PR #256). ✅ Fetta 2 (PR #258) e ✅ fetta 3 (24 ottobre: costo su ogni errore, conto sotto lucchetto, doctor «Cervello forte»). ✅ **Acceso sul Mac il 27 ottobre** (PR #269): prova del login R-496-3 riuscita il 26 (`ok 0.007764`), `GAS_CLAUDE_CLI=1` nel `.env`, doctor OK, `punto_lead` con `cervello: forte`, `/forte` provato da terminale («Ciao!»); Telegram e voce supportati nel codice, non ancora provati sul Mac. Fetta 2 in dettaglio: tag con codice casuale per chiamata, variabili d'ambiente permesse, tetto giornaliero `GAS_CLAUDE_CLI_TETTO_USD` (default 4,60 $ «come se fosse API», misura indicativa: il limite del piano non è in dollari), errori senza testo di Claude. Campo `cervello: forte` nel catalogo notturno: ✅ (PR #269); setup del Mac: ✅ fatto dall'operatore il 27 ottobre (registrato nella PR #274).
- ✅ Fetta 1 (12 ottobre): tetto di spesa ricontrollato prima di ogni chiamata, non solo a inizio compito (chiude F2).
- ⏳ **Budget di Gas:** al massimo il 20% del limite **settimanale** al giorno, misurato **solo sul consumo di Gas**. Il consumo di sviluppo (Gas-operatore con Claude Code) non conta e non blocca Gas.
- ⏳ Di notte nessun freno sulla finestra delle 5 ore.
- ✅ **Chiarito il 20 ottobre (scelta A):** nessun freno sulla finestra delle 5 ore, né di giorno né di notte. Vale solo il tetto del 20% del limite settimanale al giorno, contato sul solo consumo di Gas (quello che l'operatore aveva già usato non conta).
- ⏳ Al tetto: i lavori semplici passano ai modelli gratuiti, quelli importanti aspettano (regola dei modelli, capitolo 0). Parte la riflessione R9: analizza cosa ha fatto Gas, se era utile e come farlo con meno token, e propone lezioni in quarantena (le approva Gas-operatore).
- ❌ Crediti API da 100 dollari: **non usati per ora** (riserva a crediti rifiutata il 19 ottobre).
- ⏳ **Dubbio aperto:** come legge Gas il limite residuo? Forse deve contare da solo il proprio consumo. Da verificare in costruzione.
- Riapre la decisione "Claude Code sul server di produzione" (capitolo 11): da ridecidere con R2 e R5.
- ✅ Regola di `CLAUDE.md` "Claude non è un gradino di Gas" cambiata il 20 ottobre (approvata dall'operatore).

### R3 — Turno di notte dello sviluppo ⏳
**Cos'è.** Un'attività programmata di Claude Code in cloud ("routine"): parte da sola, lavora sul repo, apre una PR. È inclusa nell'abbonamento (Pro 5 al giorno, Max 15), conta nei limiti d'uso, non dipende dal Mac.
- ⏳ Prima notte di prova: un compito solo documentale, nessun merge.
- ⏳ Poi una riserva piccola del motore per notte, dalla lista del capitolo 5.
- ✅ Coda dei lavori notturni: `reports/coda_notte.md` (22 ottobre); turno programmato ogni notte alle 00:41. La prima notte (22→23 ottobre) ha fatto le voci 1 e 2 ma non ha potuto pubblicarle (403: la sessione non aveva il repo collegato); il 23 ottobre l'attività è stata ricreata in una **sessione fissa con il repo** (dettagli in `coda_notte.md`). Rischio dichiarato: la sessione fissa accumula il contesto delle notti; se pesa, si torna a una sessione nuova per notte col repo collegato (da creare dal pannello delle routine di claude.ai). Protezioni R4 fatte dall'operatore il 22 ottobre: issue spente (verificato dall'agente via API), interazioni limitate ai collaboratori (dichiarato dall'operatore, non verificabile col token dell'agente).
- **Costruisce Claude Code in cloud**, non Gas col cervello gratuito.
- **Niente connettori** (Gmail e gli altri) nelle routine notturne, per ora. Si riapre più avanti.
- **Nessun merge di notte.** Al mattino un report breve per ogni PR, poche righe: cosa ha fatto, perché, cosa migliora, quali rischi. Gas-operatore controlla e decide il merge. Per ora il merge è sempre al mattino.
- **Priorità della notte:** prima si chiudono i lavori aperti della roadmap (riserve, cose a metà, parte tecnica). Se avanzano tempo e limiti, si prosegue con i lavori successivi. Le idee nuove vengono dopo.
- **Divisione 80/20:** di giorno il 20% importante (Gas-operatore + Claude), di notte il resto tecnico.
- **Ultimi giri entro le 05:00**, così alle 10 la finestra delle 5 ore è già ripartita. Va bene consumare i limiti di notte, ma il limite settimanale va tenuto d'occhio nelle prime settimane.
- ⏳ Lavori già destinati al turno di notte: regola di merge nel codice e allineamento di `fine-task.md` ("non mergiare"); il lavoro tecnico di R7.
- ⚠️ Una routine lavora senza chiedere permessi: per questo le protezioni gratuite di R4 sono state fatte prima di accenderla (22 ottobre, vedi R4).
- Limiti del cloud: lì Gas non gira (niente chiavi dei modelli, niente recinto), quindi le prove del recinto valgono solo nei test automatici. Il cloud scrive solo su un ramo suo e non può cancellare rami. Per GitHub: `gh api` REST passa dal proxy della sessione solo se il repo è collegato alla sessione (la prima notte non lo era: 403); il turno notturno non ha gli strumenti GitHub di sessione (attività creata senza connettori). Se non riesce ad aprire la PR, lo scrive in `reports/report_notte.md` sul suo ramo.
- Più avanti: Gas stesso scrive le proposte in coda (vedi "Ponte" in R10).

### R4 — Protezioni di base ⏳ 👤
- ⏳ 👤 **Backup cifrato su iCloud Drive** (deciso il 19 ottobre) di: memoria (`.gas_memory.db`: diario e rubrica), file delle chiavi (`.env`) e cronologia delle conversazioni (`.gas_history.json`). Password della cifratura nel gestore di password. Mai chiavi in chiaro. Il comando di copia esterna esiste già da giugno.
- 🅿️ **Protezioni del repo — repo privato + GitHub Pro: rimandato** (19 ottobre; è l'impegno «protezioni del repo» citato da V-3 bot #249, tracciato qui per decisione dell'operatore del 24 ottobre). Intanto, gratis e **prima di accendere R3**:
  - ✅ 👤 issue disattivate (22 ottobre, verificato via API);
  - ✅ 👤 interazioni limitate ai collaboratori (22 ottobre, dichiarato dall'operatore; da rinnovare ogni 6 mesi, entro il 22 aprile 2027);
  - ✅ l'agente notturno legge solo il codice e la sua coda, mai issue o commenti di altri (regola nella coda e nel prompt dell'attività, 22 ottobre).
- ⏳ 👤 Verificare che il token Telegram esposto il 5 luglio non sia quello in uso oggi.
- ⏳ 👤 Chiave ElevenLabs: un documento la dà sostituita il 26 agosto, il repo dice ancora "da ruotare". Controllare sul pannello; per il server, chiave nuova in ogni caso.
- ⏳ 👤 Vecchio PC: dismetterlo dopo aver salvato le chiavi `.ssh` e gli altri progetti, e aver controllato che non restino segreti nelle impostazioni del terminale.
- ⏳ **Revisione esterna** (aggiorna la decisione del 24 settembre): durante lo sviluppo, doppia verifica bot + chat di strategia solo dove c'è un dubbio vero. Una persona fisica controlla prima dei dati di clienti veri (Gas-operatore ha già qualcuno in mente).

### R5 — Server sempre acceso ⏳ 👤
Tutto da zero. Lista completa al capitolo 8.
- 👤 **Netcup** (KVM, x86), circa 8 GB di RAM per partire, "nei prossimi giorni" (deciso il 19 ottobre). Prezzo da verificare all'acquisto.
- 👤 Prima dell'acquisto: metodo di pagamento valido + avviso di fatturazione + accesso a due fattori con il codice di recupero su carta.
- ⏳ Messa in sicurezza dal primo giorno, backup automatico fuori dal server.
- ⏳ Gas su Telegram sempre acceso, giro notturno col timer di Linux, riavvio automatico, allarme se cade.
- ⏳ Tarature sui dati veri (ricerca per significato, memoria RAM).
- Ollama non va sul server: rimosso dal piano (capitolo 5.6).

### R6 — Le mani: web, mail, social, notifiche ⏳
**Ordine (19 ottobre):** web → mail → social → notifiche Telegram.
- ✅ **Decisione porte del lettore web** (operatore, 22 ottobre): `leggi_pagina` solo verso le porte 80 e 443, anche dopo un redirect. ✅ Nel codice dal 2026-10-30 (chat Mani, PR #310, review #583).
- ⏳ Leggere il web in un ambiente chiuso (browser senza schermo), per cercare clienti e leggere siti. Ogni testo letto è "non fidato".
- ⏳ Mail: leggere, preparare bozze, inviare **solo con firma**.
- ⏳ Messaggi diretti, post pubblici sui social e invio di moduli: sempre con firma.
- ⏳ Notifica su Telegram come strumento di Gas.
- ⏳ **Allarme urgente sul telefono** (nuovo, 19 ottobre): **solo gratuito** (es. ntfy a priorità massima, che suona anche in silenzioso). Twilio scartato perché a pagamento. 👤 Motivi dell'allarme e tetto al giorno: da decidere insieme.
- ⏳ Le prove M1, M2 e M4 scritte come test veri nel repo.
- ❌ Bottone "Modifica" e firme a gruppi (fetta C6 del cancello): l'operatore ha scelto «lasciamo così» il 21 ottobre (una firma per azione).
- ⏳ **Regole fisse** (disegno della memoria di giugno, mai costruito): chi non contattare, tono, canali, cosa vendi. 👤 Le scrive Gas-operatore.
- ⏳ Dati di persone vere: valgono la regola dei modelli del capitolo 0 (solo modelli forti) e il GDPR (capitolo 6).
- ⏳ Pulizie collegate: gli argomenti degli strumenti finiscono nel diario e nel promemoria anche quando contengono testo di terzi (F-diario-args, F-args-pin, fetta "C-pin"). La correzione del diario di settembre vale solo in avanti: il testo di terzi già scritto resta.

### R7 — Direttore v2: compiti lunghi ⏳
Oggi ogni compito notturno parte da zero e non può riprendere. Nessuna decisione da prendere: tutto lavoro tecnico, adatto al turno di notte (R3).
- ⏳ Piano scritto del compito, progressi salvati, ripresa dopo un'interruzione (M3).
- ⏳ **Lista dei lavori ricorrenti con stato** (fatto, in sospeso, fallito, da non ritentare): disegno di giugno, mai costruito.
- ⏳ Tetti di tempo duri.
- ✅ Tre stati per un comando firmato: non partito, finito, partito con esito incerto (R-c4b3-5, review #428/#429, 21 ottobre). ✅ R-c4b3-3 (crash tra reclamo e storia: esito recuperato al nuovo click, review #445-#447, 21 ottobre).
- ✅ Due processi che scrivono la stessa cronologia: lock e unione dei turni (R-c4b3-4, review #430/#431, 21 ottobre).
- ✅ L'esito di un compito notturno non è più dedotto dall'inizio del testo: lo dice il kernel (R-222-2, review #425, 21 ottobre).
- 🅿️ Un file di stato con roadmap attiva e compiti del giorno (idea "Scratchpad" del Blueprint: si valuta solo a roadmap finita).

### R8 — Voce "Jarvis" ⏳ 🔒 R5
Documento: [`reports/briefing_architettura_voce.md`](briefing_architettura_voce.md).
Pezzi decisi a luglio-agosto e mai costruiti.
- ⏳ Parola di attivazione "Hey Gas" sul dispositivo (openWakeWord; prima il modello pronto, poi la parola nostra).
- ✅ Finestra di ascolto di circa 12 secondi dopo la risposta, senza ripetere la parola (V3, 30 ottobre, chat M2: nella pagina del browser, `GAS_VOICE_FINESTRA`; la parola di attivazione resta da fare).
- ✅ "Due secondi o ci sto ragionando": timer nel client e frase di attesa già pronta (V3, 30 ottobre: detta dal browser con la voce di sistema). Risposte a voce di 1-3 frasi col parere subito (istruzione del solo turno parlato), il testo lungo a schermo.
- ⏳ **Firme a voce** (19 ottobre): Gas rilegge l'azione esatta, poi le parole "Procedi" / "Annulla" (da rivedere in sviluppo). Sicurezza, codice madre e azioni irreversibili: **solo coi bottoni**.
- ⏳ 👤 **Voce da scegliere all'ascolto** tra: Piper italiano (gratis, in locale); modello "Jarvis" per Piper (inglese, **solo uso privato**, mai coi clienti); clone della voce di Gas-operatore (es. Chatterbox, in locale, file custodito come una chiave). Niente imitazioni di persone famose verso l'esterno. ElevenLabs a pagamento: non scelto, si resta sul gratis.
- ⏳ Server voce esposto in modo sicuro: connessione cifrata, token che scadono, limite di richieste.
- ⏳ 👤 Tetto di consumo per trascrizione e voce, con risposta in solo testo se la quota finisce (non discussa 19 ott).
- ⏳ Dispositivo dedicato sempre acceso per il microfono (mini-PC o simile); telefono come microfono.
- ⏳ Fuori casa: voce via Telegram.
- ✅ **Deciso il 19 ottobre** (chiude la domanda del 22 agosto): la voce è il fronte principale (dialoghi rapidi, decisioni, poi Gas lavora dietro). Telegram resta per i bottoni di firma, i report del mattino e quando sei fuori casa.
- ✅ **Voce V2** (29 ottobre, chat M2): «forte» detto senza richiesta → istruzione d'uso a voce (nessun lavoro avviato); il server voce dice subito «avvio in corso»; la pagina nel browser aspetta il forte fino a 600 s (`GAS_VOICE_TIMEOUT`) e, se scade, dice che Gas può star ancora lavorando.
- 🅿️ Interruzione mentre parla, profondità adattiva (circa 20 secondi), voce e testo mescolati.
- ⏳ Canale Gas → supervisore per i dubbi tecnici (deciso il 27 agosto, mai costruito): raro e con tetto; "rispondere non è autorizzare"; le domande di Gas sono dati, mai comandi.
- Da sapere: oggi l'audio va a Groq e il testo a ElevenLabs.
- ✅ Chiuse come superate (19 ottobre): indirizzo del client che cambia a ogni riavvio (D1-ter), variabili sovrascritte e scelta del dispositivo audio (D2-audio), sonda F0 mai verificata, errore non gestito nel client di prova (R-client4a-1).
- ✅ I test della voce (trascrizione e sintesi) girano nei test automatici dalla PR #229 (20 ottobre); dal 29 ottobre (V1, chat M2) non si rompono più se nell'ambiente c'è un proxy (R-384-1 chiusa). Il client nel browser è entrato senza revisione.
- ✅ **Cervello forte dalla voce** (V1, 29 ottobre, chat M2): «forte …» o «Gas forte …» detto all'inizio della frase vale «/forte» (mai ai gratuiti; «forte» senza richiesta → istruzione d'uso). Con `GAS_VOCE_FORTE=1` nel `.env` tutta la voce va al forte (spento di default; il server voce, avviato con `python -m modules.voice.server`, ora carica il `.env` come la CLI e lo dice a schermo: V-1 bot #304); forte fermo → risposta dichiarata, mai i gratuiti. Vale anche dopo un saluto prima di «Gas» («Ehi/Ok/Ciao Gas, forte…»). Limiti: «Gas e forte…» o un saluto fuori elenco restano turni normali (V-2 ve #304); «Forte!» detto come esclamazione a inizio frase va al forte, come «forte-forte» o «forte: …» (direzione sicura, consuma budget: R-564-1-M2, V-1 ve #304).

### R9 — Imparare da solo 🔄
- ✅ Riflessione a comando e lezioni in quarantena.
- ✅ **Riflessione automatica** (fetta 2, decisa il 15 ottobre): a fine compito notturno riuscito e a ogni `clear` (PR #211, #212). Provata sul Mac.
- ✅ **Riassunto pertinente con scadenza** (fetta 3, R-199-3 chiusa, PR #213); usato solo se pertinente, niente lezioni quasi uguali (PR #215, #216). Provato sul Mac (15-16 ottobre).
- Limite dichiarato: dopo una lettura o una compressione i riassunti restano "non fidati" e non vengono riusati fino a `clear`.
- ⏳ 👤 Lezioni #4, #5, #6 da rivedere a testo, dopo questa verifica (parere dell'agente: approva 6 e 5, rifiuta 4).
- ⏳ Riflessione al tetto del budget (R2): analizza cosa ha fatto Gas, se era utile e come farlo con meno token.
- ⏳ Fonti vere nel catalogo della conoscenza (oggi c'è solo una fonte di prova), fonti da indirizzo web, studio programmato.
- ⏳ **Studiare dai video** (disegno di giugno; nessuna decisione il 19 ottobre): YouTube → trascrizione, più i fotogrammi → concetti, dichiarando i dubbi → memoria. Instagram escluso. La parte di rete in un componente isolato. Primo passo: prototipo fuori dal motore. Tre bracci in ordine di rischio: conoscenza; poi istruzioni, con diff e ripristino; poi codice. Rapporto al mattino e approvazione voce per voce.
- ⏳ Collegare un errore alla sua soluzione; "confidenza" sui fatti salvati; valore precedente quando un contatto cambia (R1, R4 e nota della sonda del 23 settembre).
- ⏳ Gemini che ogni tanto scarta la riflessione: alla prossima, leggere il motivo nel registro.
- ⏳ Piccole: R-202-1, R-202-2, R-204-1, errore possibile nel ramo d'eccezione di `rifletti`. Prova col modello vero mai fatta nell'ambiente di sviluppo.
- 🅿️ Dal Blueprint: "tabù" dopo un tuo veto, riflessione notturna sui registri.

### R10 — Aggiustarsi e programmarsi da solo ⏳ 🔒 R5
Documento: [`reports/recinto_autonomia.md`](recinto_autonomia.md).
✅ Bozza del recinto **approvata** (19 ottobre). Proposte di Gas: idee illimitate in una lista ordinata per valore; al massimo **10 PR a notte**; le proposte con etichetta "importante" possono superare il limite. Resta la catena: PR su un ramo suo → firma di Gas-operatore → gemello di prova.
- 🔄 Aggiustarsi: oggi c'è solo il passaggio automatico al modello successivo.
- ⏳ Avviso in tempo reale quando un compito degrada a "solo testo" (rimandato per falsi allarmi; D3 della sonda telemetria).
- ⏳ Programmarsi: Gas propone una PR su un ramo suo, mai su `main`. Solo codice applicativo: infrastruttura, messa in linea, servizi di sistema e dipendenze restano sempre a mano tua.
- ⏳ Catena dei cancelli: proposta → revisore → firma tua → "usciere" che fa il merge → gemello di prova → promozione.
- ⏳ **Approvazioni semplici ma fedeli**: ogni proposta spiegata in parole semplici, col diff vero sotto e un sì o no per voce; un secondo revisore controlla che la spiegazione corrisponda al diff.
- ⏳ **Gemello**: copia di Gas con dati e chiavi separati e azioni verso l'esterno finte. Promozione dopo almeno 5 giorni, N eventi, zero crash. Costa il doppio: lo si fa girare su richieste registrate o solo durante la prova.
- ⏳ Token di Gas senza permesso di scrivere su `main`.
- ⏳ Di notte solo proposte, al massimo 10 PR (vedi sopra). Studio solo da fonti approvate.
- 🔄 **Ponte Gas → sviluppo, strada A** (deciso dall'operatore il 29 ottobre, PR #307): lo strumento `richiedi_sviluppo` scrive la richiesta come issue (etichetta `da-gas`) nel repo PRIVATO `Gasss23/Gas-richieste` con un token DEDICATO (solo Issues su quel repo, mai il token dello sviluppo: vincolo qui sotto rispettato); la chat di coordinamento M1 la legge e assegna il lavoro; revisore, CI e firme come sempre. A finestra contaminata va alla firma. Strada B (Gas lancia Claude Code da solo sul Mac) rimandata. Disegno originale: ⏳ **Ponte Gas ↔ Claude Code con firma** (registrato il 7 luglio, senza data). Gas scrive la proposta come file, tu approvi con `/approva`, Claude Code la esegue su un ramo. Vincoli: il server non ha mai le credenziali della macchina di sviluppo (è quella che va a prendersi le proposte); bot Telegram separato; solo comandi fissi, mai testo libero; codici usa-e-getta che scadono in 24 ore; massimo 3 proposte al giorno; tetto di spesa per proposta; tutto nel diario. Nodo aperto: funziona solo a computer acceso. Le routine di R3 possono risolverlo.

### R11 — Motore marketing (FASE 4) ⏳
Per tua scelta tra gli ultimi. Oggi non esiste: il vecchio modulo era vuoto ed è stato tolto.
- ✅ **Deciso il 19 ottobre:** Gas-Python orchestra tutto. n8n come piano B, solo se un collegamento è troppo costoso da fare da zero. Make scartato.
- ⏳ Modulo Meta Ads e generazione di contatti.
- ⏳ Testi persuasivi per annunci e messaggi.
- ⏳ Automazione dei canali del brand (voce della roadmap di giugno).
- ⏳ GDPR e dati personali dei contatti.
- ⏳ Gas potrà preparare pagine web o contenitori per un tuo progetto? Oggi è vietato (R-249-2).
- 🅿️ Claude Cowork per il materiale di marketing e la trascrizione dei video in locale.
- ⏳ Piano "GAS WEB OS": entra in roadmap dopo il completamento di Gas (capitolo 10).

### R12 — Controllo del PC 🅿️
Deciso in chat il 29 settembre (supera il repo, che dice ancora "nessuna soluzione decisa"): sì al pieno controllo, con un cancello. Azioni tranquille libere, azioni delicate con firma; la lista la scriviamo noi, non il modello; dopo aver letto roba esterna niente azioni delicate. 👤 Lista da scrivere insieme. Oggi il cancello lo classifica tutto come "firma sempre": va corretto quando arriva il suo turno. Collegata all'idea di giugno "Gas controlla la macchina a un orario stabilito, sempre col tuo consenso".

### R13 — Secondo cervello personale 🅿️ 🔒 R5
Segnato nel repo come "molto importante, non prioritario". Magazzino delle tue note, decisioni e video, più risposte nel tuo stile. Detto onestamente: imita lo stile e ritrova le tue conoscenze, non ragiona col tuo giudizio. Vincoli: archivio separato dai contatti; fornitori che non si allenano sui tuoi testi (o solo modelli locali); memoria RAM del server da dimensionare; "agire a tuo nome" sempre con firma.

---

## 5. Tutte le voci aperte, per area

Sono le "task minori" per il turno di notte. Gravità come scritta nei file.

### 5.1 Lettura e comandi (le chiude R0)
- R-273-1 (bassa): tre comandi hanno una lista di opzioni vietate invece che permesse.
- R-273-2 (bassa): le versioni Mac dei comandi mai provate.
- R-274-2 (bassa): alcuni argomenti legittimi rifiutati.
- R-nw-2 (cosmetica): un nome di file che contiene "venv", ".git" o ".env" dentro una parola viene rifiutato.
- R-277-1 (bassa): `prod.environment` e simili leggibili.
- R-277-2 (cosmetica): commento di una funzione; collegamento non protetto in un test.
- R-eco-run-1, R-eco-1 (minori): un ramo senza test e un controllo legato al testo di un messaggio.
- Il cancello considera il recinto attivo solo se la variabile è scritta per esteso; il motore anche quando manca.
- Se la cartella di lavoro sta fuori dalla cartella di Gas, ogni comando viene negato.

### 5.2 Cancello e firme
- V-1 esterna / V-2 bot #180: il codice che applica cancello e firma (bot, memoria, script dei controlli, `CLAUDE.md`) **resta livello 2** (deciso il 19 ottobre), ma con: doppia verifica obbligatoria bot + chat, firma **solo coi bottoni** (mai a voce) e **mai di notte**. ⏳ Da mettere nel codice.
- Note basse su #180: finta riga di intestazione dentro il diff della firma; caratteri invisibili gestiti in parte per classe e in parte a elenco; messaggi diversi al modello senza avviso a te; un diff oltre 4096 caratteri non passa su Telegram; caratteri sosia non rilevabili; "una PR per scopo" saltata.
- ✅ R-203-2 e C-d superate dal principio dell'autonomia del 19 ottobre (capitolo 0), nel codice dal 20 ottobre (vedi R1). `stato_progetto.md` e `CLAUDE.md` allineati il 20 ottobre.
- C5 non fatta: scadenza delle approvazioni (vedi R1). C6 non fatta: bottone Modifica e firme a gruppi. C-pin non fatta.
- R-c3-1b (mitigata), R-c3-2 (validare la durata), R-c3-5 (cosmetica).
- R-c4b1-3: invio del messaggio di firma che blocca il turno fino a 15 secondi per destinatario.
- R-c4b1-4: una riga rovinata conta nel tetto finché non scade.
- R-c4b2-6: esecuzione nello stesso filo del bot; i bottoni degli altri destinatari restano.
- R-c4b2-7: dopo un errore del database la richiesta resta senza bottoni.
- R-c4b2-8, R-c4a-2 (cosmetiche). R-c4b2-10: test sensibile alla lentezza.
- ✅ R-c4b3-3 (#445-#447), R-c4b3-4 (#430/#431) e R-c4b3-5 (#428/#429) chiuse.
- R-c2-2, R-c2-4, R-c2-5, R-c2-6, R-c2-10 (non bloccanti); R-c2-8 (accettata: un test entrato senza seconda revisione).
- R-erm-1, R-erm-2: l'isolamento dei test da Telegram copre un file solo e un solo modo di chiamare la rete.
- R-220-1: l'esito di un'azione notturna firmata finisce nella tua conversazione.
- Il documento del cancello si contraddice in tre punti con il codice di oggi: da riallineare.

### 5.3 Giro notturno e scritture
- ✅ **Catalogo delle fonti di studio alla firma** (20 ottobre, PR #228): ogni scrittura in `knowledge/` (catalogo e file delle fonti) chiede la firma. Le fonti di tipo file fuori da `knowledge/` vengono rifiutate dall'ingest (nota bot #228, chiusa).
- R-223-1 (bassa): la cartella `reports/` è scrivibile da Gas, e quei testi li leggono revisore e bot.
- R-223-2 (deciso il 19 ottobre): si tiene la lista dei file vietati, decisa insieme a Gas-operatore. In più: ✅ segnalazione **solo** quando nasce un file nuovo che sembra delicato (chiavi, configurazioni, script); i documenti normali passano in silenzio (nel codice dal 20 ottobre, PR dopo #228).
- R-224-2 (cosmetica): nome del compito con spazio o punto finale.
- R-251-1 (bassa): nomi alternativi dello stesso file su Windows, che non usiamo.
- ✅ R-222-2: esito dedotto dall'inizio del testo — chiusa (review #425).
- Tetti di tempo non duri. Il riepilogo Telegram si spegne solo con `0`.
- Disco senza blocco dei file: il giro si ferma e avvisa; da riprovare sul server.
- Nessun timer per Linux: esiste solo quello del Mac.
- `setup_notte.md` dice ancora "Gas non può modificare il proprio motore": oggi può, con firma. Testo da riallineare.

### 5.4 Memoria, conoscenza, vettori
- F-diario-args, F-args-pin (vedi R6).
- R-fts-1 (tetto alle parole cercate), R-fts-2, R-fts-3, R-e2e-refactor-1/2, R-k4-3 (minori o cosmetiche).
- Prova reale della conoscenza: 2 su 3; fallisce la domanda di una parola sola.
- Iniezione "comportamentale": mitigata, non chiusa.
- R-lez-bis-1 (cosmetica), R-lez-2 (nessun blocco strutturale sugli strumenti delle lezioni, coperto da un test).
- Separatori Unicode insoliti non rifiutati nelle lezioni.
- R3 della sonda: il diario non ha archiviazione. Mai cancellare; esportare quando servirà.
- R5 della sonda: rafforzare ancora la protezione del diario.
- R-wire-1: soglia della ricerca per significato tarata su esempi finti. 🔒 R5.
- R-wire-2: ricerca per significato debole sulle domande corte in italiano.
- Confronto col modello `e5-small`: mai fatto.
- R-reidx-3: picco di memoria RAM durante la reindicizzazione (le fonti si contraddicono: chiusa o solo ridotta). 🔒 R5.
- R-vec-3: riprovare sul server nuovo che il motore dei vettori si carichi.
- Tre comandi dei vettori ignorano la variabile che sposta l'archivio: sul server lavorerebbero su un archivio diverso.
- R26-1, R26-2: codice d'uscita del backup esterno e un test mancante.
- Nessun test per i due comandi dei vettori.
- R1-R4 della rubrica: quattro ritocchi a codice e test.
- R-crm-diario-rr: un test mai ri-revisionato.
- Riserve vecchie di giugno, mai chiuse e senza dettaglio in nessun file: R-test-1 (tetto finestra), R2 #6 (cambio cartella), R3 #4 (falsi allarmi sui percorsi), foto di sicurezza "TASK C", aggancio di fine sessione, R-mem, R-mem2a.
- F4 del prompt: nelle istruzioni convivono "dichiara che non puoi" e "non bloccarti". Mitigata, non risolta.
- Il registro `gas_debug.log` ha un percorso relativo: se Gas parte da un'altra cartella finisce altrove.

### 5.5 Telegram e telemetria
- R-tel-budget-perf: il costo si ricalcola rileggendo tutto il registro a ogni turno.
- R-tel-tool_res (cosmetica).
- F5 delle fondamenta: una sola cronologia condivisa nel bot.
- Il bot ri-esegue i messaggi modificati; i messaggi oltre 60 caratteri contano sempre come "complessi".
- Tempi di risposta e numero di tentativi nel registro: mai fatto. Riconoscimento del "troppe richieste" fatto confrontando testi. Il registro conserva solo il livello dell'errore.
- Avvisi di rete del bot a riposo: abbassare il rumore. Registro che cresce: rotazione.
- Indagine sulla lentezza di Gas sul server (voce di luglio). 🔒 R5.
- Notifica su Telegram se Gas parte degradato: decisa, da verificare se esiste.

### 5.6 Modelli e fornitori
- Gradino OpenRouter gratuito in degrado: trovare un modello gratuito stabile o dichiararlo "quando va".
- Mistral come gradino candidato: prima la sonda sui limiti e sulle regole dei dati. Vale la regola dei modelli del capitolo 0: i gratuiti solo per lavori semplici senza dati personali.
- 🅿️ Sblocco OpenRouter da 10 dollari (da 50 a 1000 richieste al giorno): rimandato (19 ottobre), si riapre se serve.
- ⏳ **OmniRoute come sonda fuori dal motore** (riaperto il 19 ottobre): affidabilità, dove finiscono i dati, utilità come ponte. Se si rompe spesso, scartato.
- Groq: limite di 8000 token al minuto, più cadute sul gradino dopo.
- Gemini gratuito finito a 20 richieste al giorno nella prova del 28 settembre: da ricontrollare.
- Commento sui prezzi Gemini datato.
- ❌ Ollama: rimosso dal piano (19 ottobre).
- 🅿️ `gas --brain`, DeepSeek come operaio, "Il Consiglio" di modelli economici, profilo del revisore a pezzi. La voce di giugno "ragionamento avanzato" è confluita qui e in R2.
- Voce del 21 giugno "ottimizzazione della cache dei prompt": citata in chat, contenuto non ritrovato.

### 5.7 Bot di verifica, merge, permessi
- R-162-1: isolamento nel lavoro del bot (probabilmente chiusa, mai confermata). R-162-2, R-160-1: la pulizia dei segreti dipende da una versione fissata.
- R-158-5 (👤): il bot non esegue i test.
- R-192-1: senza recinto non partono nemmeno i modelli di riserva.
- R-193-1, R-193-2, R-194-3, R-191-1 (basse o cosmetiche).
- Fable 5.1 nel bot fallisce, causa ignota. Oggi è l'ultima riserva: resta da capire perché.
- R-198-1: il bot dichiara da sé di aver usato gli strumenti. R-198-2 (cosmetica, documento).
- R-163-2 (👤): il NO del bot è legato al commit, un commit vuoto riapre il giudizio. R-163-3, R-164-3 (dichiarate).
- R-205-1, R-205-2: due modi di sfuggire al controllo sul testo del verdetto.
- R-161-2: convalida dell'approvazione automatica (probabilmente già avvenuta, non scritta).
- ✅ G-3 fatto (14 ottobre): token ristretto `gas-agente` creato (scade il 4 gennaio 2027), avvio con `gasclaude`, blocco in `gasmerge --auto` (fase 2). Restano R-186-3, R-186-4, R-189-1. Limite: GitHub non separa il permesso di inviare da quello di fare merge.
- ⏳ La regola di merge autonomo è scritta in `CLAUDE.md` ma non nel codice (lavoro per il turno di notte, R3). `fine-task.md` allineato il 20 ottobre.
- ⏳ **Pulizia di rami e PR una volta a settimana** (19 ottobre; più spesso solo se crescono): l'agente verifica che il contenuto sia su `main` e prepara la lista; la cancellazione resta di Gas-operatore.
- Regole da non rompere: mai escludere percorsi dai test automatici; etichetta `verifica` obbligatoria sulla PR.
- Nessun controllo sull'indirizzo passato al verificatore: fa fede il commit nel suo commento.
- Il commento del verificatore esterno esce con la tua identità.
- Il verificatore esterno deve usare un modello diverso da quello dell'agente: oggi può coincidere.
- Il bot ha dato "fallito" per "finding medio" su un verdetto con soli finding bassi (PR #183).

### 5.8 Cancello di sviluppo, dossier, agganci automatici
- V-B (media): il controllo prova che le citazioni esistono, non che la revisione sia avvenuta; il segno di "revisione fatta" lega il diff, non il verdetto. V-C (media): l'aggancio vede solo `git commit`.
- V-5 esterna #180 (bassa): il controllo delle citazioni scarta quelle precedute da una parola con i due punti e non vede più una riga inesistente. V-3 esterna #180: regola di fine lavoro da precisare.
- R-141-2 (mitigata): una PR può svuotare i controlli tenendone il nome. R-143-2 (mitigata), R-143-3 (👤 uscita dallo stallo).
- R-139-1, R-136-2, R-136-3, R-138-3: formati di verdetto che passano o si spezzano.
- R-137-1, R-137-2 / R-gjq-1 (il cancello blocca qualunque comando che contiene "git … commit"), R-137-3, R-gjq-2, R-gjq-3.
- R-138-5 / V-5 #121 (👤): file fuori dal perimetro di revisione (`.gitignore`, `knowledge/`, `CLAUDE.md`). V-3 #121 (👤): etichette `origin/*`.
- F-controlli-auto: verdetto vuoto che passa; dossier scritto prima del push; esiti diversi tra le parti.
- R-ci-1: ricerca del titolo non ancorata a inizio riga. R-verdetto-evidenza: manca il controllo sulla riga citata.
- R-finegat-1, R-finegat-2, R-finale-2, R-147-2.
- V-2 della verifica #127 (un secondo aggiornamento senza pulizia, non coperto da test). V-3 della verifica #123: il controllo degli indirizzi IP è cieco a certe codifiche e agli indirizzi spezzati.
- R-155-3 (👤): due agenti nella stessa cartella. Finding "aggancio di fine sessione + sessioni parallele" mai registrato.
- 👤 F3 "partenza su `main`": i commit fatti direttamente su `main` sfuggono all'aggancio.
- F-scrivi-rep-main, F-sessionend-msg, etichetta sbagliata in `settings.json`, commit del revisore con numero non compilato, F-handoff-c4a (un dossier vecchio con un dato falso).
- Sessione interrotta prima della chiusura: la cronologia non si salva.
- Se una PR entra dopo il calcolo del diff, il dossier può includere commit estranei.
- Proposta mai impegnata: la chiusura si ferma se manca la PR. Contare i rami a fine giro.
- `gasmerge`: residui minori (#62-R1 mitigata, finestra di pochi millisecondi, variabile che può puntare a un altro repo).
- Note #146: righe doppie in `.gitignore`; i futuri file audio di prova vanno aggiunti a mano.
- Verdetti #173-#177 non provabili per intero. Review #56 con verdetto vuoto; PR #43 revisionata da un agente generico; lezione #50 persa; mancano #83 e #84.

### 5.9 Documenti da riallineare
- `stato_progetto.md` pesa 143 KB; la regola dice circa 100 righe. Lo storico va spostato; restano tre ✅ da archiviare e marcatori vecchi (es. R-finale-1, F-env-app).
- ✅ `roadmap.md` sostituito da questo documento (19 ottobre).
- ✅ `README.md`: aggiunto un riassunto di cosa fa Gas oggi (20 ottobre).
- ✅ `gas_identity.md`: cascata aggiornata (20 ottobre).
- ✅ `fine-task.md`: "non mergiare / merge da WSL" allineato alla regola di merge (20 ottobre). Restano: aggiunge un file che git ignora; parla solo di motore e test mentre il perimetro di revisione è più largo.
- Regole operative di `stato_progetto.md`: superate R1 e R2 ("merge mai dall'agente") e i riferimenti a WSL. Le altre valgono.
- Titoli fuorvianti, sigle riusate (F1, F3, F6, R2), contatore delle review fermo a 92.
- Sezioni sul server che parlano del vecchio Hetzner come vivo.
- `setup_verifica_bot.md`: un passo scritto come futuro è già fatto.
- `raccomandazioni_aperte.md`: contiene solo "repo privato".
- Micro-compito di luglio mai fatto: raffinare il controllo di processo segnato 🟡.
- ⏳ 👤 Istruzioni del progetto su claude.ai: chiedono ancora la stampa integrale del report, il comando `/agents` e parlano di Codespace. Da aggiornare; collegare anche il repo GitHub al progetto (regola del 19 ottobre).
- Versioni di Python diverse: 3.11 nei test automatici, 3.14 sul Mac.

### 5.10 Spesa
- Spesa di sviluppo: non tracciata né fermata dal codice. La leva è la disciplina (modello leggero di default, contesto pulito tra i compiti).
- Tetto di spesa di Gas: conta a prezzi di listino anche i modelli gratuiti. Diventa una protezione vera con R2.

---

## 6. Decisioni che spettano a te

Restano solo quelle aperte. Le decisioni del 19 ottobre sono scritte nelle rocce e nel capitolo 0.

**Aperte dal 19 ottobre.**
1. Motivi dell'allarme urgente sul telefono e tetto al giorno (R6).
2. Scelta della voce all'ascolto: Piper italiano, "Jarvis" per Piper o clone della tua voce (R8).
3. Lezioni #4, #5, #6, da rivedere a testo (R9).

**Non discusse il 19 ottobre.**
5. PR da chiudere o mergiare: #158, #109, #141, #87 (da verificare se ancora aperte) — non discussa 19 ott.
6. Regole del bot: R-163-2, R-158-5, perimetro di revisione, etichette `origin/*`, uscita dallo stallo, due agenti nella stessa cartella, partenza su `main` — non discussa 19 ott.
7. Regole sui dati dei fornitori e GDPR prima dei contatti veri — non discussa 19 ott.
8. Tetto di consumo della voce — non discussa 19 ott.
9. Mistral e Cerebras a pagamento — non discussa 19 ott.
10. Quando Gas riflette da solo — non discussa 19 ott. La riflessione automatica di ottobre (fine compito notturno e `clear`) copre il caso principale; resta aperto se servono altri momenti (es. ogni N turni).
11. Lista delle azioni tranquille e delicate per il controllo del PC (R12) — non discussa 19 ott.
12. TradeGasFX in un repo suo — non discussa 19 ott.
13. Firma dei commit dell'agente — non discussa 19 ott.

## 7. Lavoro mai arrivato su `main`

Rami non mergiati (controllati con git l'11 ottobre):

| Ramo | Avanti di | Ultimo | Cos'è |
|---|---|---|---|
| `codex/tradegasfx-redesign` | 20 commit | 7 ott | Sito TradeGasFX, solo documenti (PR #141) |
| `fix/r2-durabilita-memoria` | 9 | 19 ago | Vecchio lavoro su revisore e controlli |
| `fix/nonascii-cd-tests` | 4 | 19 ago | Test sui nomi non ASCII |
| `cert/mac-migration-2026-09-12` | 3 | 12 set | Certificazione Mac (PR #87 mai mergiata) |
| `chore/fine-task-robusto` | 3 | 2 ott | Modifica a `fine-task.md` |
| `test/prova-verifica-bot` | 2 | 7 ott | Prova del bot |
| `docs/scollega-gashistory-da-r2` | 1 | 20 ago | Nota superata |
| `feat/merge-automatico` | 1 | 6 ott | Solo una risposta salvata |
| `fix/crm-idemp-diario` | 1 | 19 lug | Nota superata |

- Altri 16 rami sono già dentro `main`. Se ne possono cancellare 15: `feat/merge-automatico-z1xjx2` è il ramo di lavoro attivo e resta.
- Aggiornamento del 19 ottobre: `fix/crm-idemp-diario` cancellato dall'operatore. Da qui in poi la pulizia si fa una volta a settimana (capitolo 5.7). La tabella sopra è ferma all'11 ottobre: si rifà alla prossima pulizia.
- Nominati nei file e non più presenti: `fix/review44-riserve-AC`, `claude/phone-gas-development-10svqc` (toccava i modelli), `fix/gasmerge-hardening` (il suo contenuto è arrivato su `main` a luglio). Per i primi due non è scritto chi li ha tolti.
- Cancellare un ramo è un'azione tua; prima si controlla a mano che il contenuto sia su `main`. `gasmerge` cancella già da solo il ramo appena mergiato.

---

## 8. Server nuovo: la lista completa

**Prima di accenderlo.**
- Metodo di pagamento verificato e avviso di fatturazione. È la lezione del 14 settembre: server perso per circa 26 euro non pagati.
- Accesso a due fattori sull'account del fornitore, col codice di recupero su carta.
- Repo privato. Revisione umana esterna.
- Chiavi tutte nuove (ElevenLabs, voce, Telegram, modelli).
- Niente vecchia chiave SSH ereditata dall'account.
- Macchina virtuale KVM, processore x86: **Netcup**, circa 8 GB di RAM per partire (deciso il 19 ottobre). Oracle gratuito e DigitalOcean scartati; l'account Hetzner è stato chiuso.

**Messa in sicurezza (procedura in `reports/runbook_s1_hardening.md`).**
0. Console di emergenza del fornitore aperta e provata prima di toccare l'accesso. Lezione di luglio: la console web storpiava i tasti; la via vera era la modalità di soccorso con password nota. Ctrl+Alt+Canc lì riavvia il server.
1. Aggiornamenti automatici.
2. Blocco automatico di chi sbaglia la password (fail2ban).
3. Utente non amministratore per Gas.
4. Accesso solo con chiave, provato da una seconda finestra.
5. Niente accesso da amministratore, niente password.
6. Verifica finale con tre prove.
- Mancano nella procedura e vanno aggiunti: muro di rete (solo la porta 22), recinto bwrap, backup fuori dal server, file delle chiavi con permessi stretti.
- Memoria di scambio da 2 a 4 GB; limiti di RAM per il servizio; un utente amministratore separato.

**Installazione di Gas.**
- Copia pulita da GitHub, ambiente Python, `python gas.py doctor` senza errori.
- File delle chiavi con: Gemini, Groq, OpenRouter, Telegram (token e lista di chi può scrivere), voce, ElevenLabs, tetto di spesa, modalità del recinto, interruttore e posizione dell'archivio dei vettori.
- Un vecchio `.env` accanto al programma riempie le variabili mancanti: controllare (R-260-3).
- Nome dell'ambiente Python fuori dalle foto di sicurezza (F7).
- Servizio che riparte da solo; `gas doctor` non blocca l'avvio.
- Mai lo stesso token Telegram su due macchine.
- Giro notturno col timer di Linux (da scrivere).
- Server voce separato, solo locale finché non c'è la connessione cifrata.
- Gli agganci automatici di sviluppo vanno riprovati su Linux.

**Dopo.**
- Backup automatico di memoria e cronologia verso l'esterno, dal primo giorno.
- Allarme "uomo morto": se Gas smette di dare segni, arriva un avviso.
- Tarare la ricerca per significato e misurare la RAM a regime.
- Foto di sicurezza: se `doctor` ne mostra zero è anomalo; la pulizia resta manuale.
- Rotazione dei registri.
- Recinto sempre in modalità stretta se c'è altro sulla macchina.
- Idea vecchia da rivalutare: Gas che parte a tempo e si spegne, invece del servizio sempre acceso.

---

## 9. Idee e parcheggi

- 🅿️ Telegram unico per comandare Gas e Claude Code: superato a metà dal comando da telefono; resta il ponte di R10.
- 🅿️ Notifiche push sul telefono (crash, test rossi, fine del giro): in parte coperte dall'allarme gratuito di R6.
- 🅿️ OpenClaw: solo ricognizione, mai copia nel motore.
- 🅿️ Mirage (file di servizi diversi visti come una cartella): da valutare con il marketing. Solo in lettura, con lista delle risorse permesse, mai scritture automatiche verso il cloud.
- 🅿️ `revisor.py` / "Claude Council": concetto interno, mai chiarito.
- 🅿️ Comandi vocali per Claude Code a mani libere durante lo sviluppo (roadmap di giugno, poi sparita).
- 🅿️ `monitor.py` (roadmap di giugno): oggi coperto da `doctor`; l'allarme è al capitolo 8.
- 🅿️ Accesso da telefono con SSH + tmux: solo se serve. Una sessione esposta è una porta d'ingresso sulla macchina di sviluppo.
- 🅿️ Claude Dispatch: scartato a luglio perché pilotava Windows; col Mac il motivo è caduto.
- 🅿️ Conservazione del diario: archivio ed esportazione, mai cancellazione.
- ✅ Abbonamento usato tramite Agent SDK o `claude -p`: entrato in roadmap come R2 (19 ottobre). Le regole vanno riverificate prima di costruire.

---

## 10. Piani esterni parcheggiati

Stanno in `reports/roadmap_da_valutare.md`, non filtrati. Si valutano a roadmap principale finita, salvo GAS WEB OS (sotto). La divisione qui sotto è una mia proposta. Le voci contrarie ai principi restano escluse senza una decisione consapevole.

### "Blueprint Supremo" (19 luglio), 7 fasi
- **Compatibile, da filtrare dentro:** firma umana via Telegram, cuore del sistema in sola lettura, cifratura dei dati a riposo, contenitori Docker, archivio su spazio esterno (R2/S3), grafo delle conoscenze, memoria vettoriale su database, pulizia degli ingressi ("Doganiere"), ricerca mista, riflessione notturna, "tabù" dopo un veto, controllo di CPU e RAM prima dei lavori pesanti, backup notturno cifrato, file di stato, commit automatico di ogni modifica autorizzata.
- **Già coperto in parte da quello che abbiamo:** guardiano della spesa che taglia le connessioni, compressione della chat, foto di sicurezza con ritorno indietro.
- **Contrario ai nostri principi (non entra senza una tua decisione consapevole):** Gas che riscrive da solo le proprie istruzioni senza approvazione, Gas che scrive e integra codice nel proprio cuore senza cancelli, micro-addestramento notturno automatico (LoRA), "darwinismo" della memoria con cancellazioni decise dal modello, memoria olografica in RAM. Diverso è il braccio previsto a giugno: istruzioni cambiate con diff, ripristino e tua approvazione.
- **Altre voci del piano:** due cervelli con micro-agenti, cache privata per ogni sotto-agente, memoria veloce Redis, comandi di sistema sui file in cloud di ogni formato, flussi tra servizi diversi, cache a due livelli, sincronizzazione con Obsidian o Anytype, osservatore dell'editor di codice, precaricamento predittivo, spazio di lavoro portabile, estrazione di idee dai video ("De-Boner"), generatore di copioni video, avatar e influencer virtuali.

### "GAS WEB OS" (27 luglio) — ⏳ entra in roadmap (19 ottobre)
**Deciso il 19 ottobre:** entra dopo il completamento di Gas, con alta ambizione: deve distinguersi dalla concorrenza (test e un salto di qualità rispetto ad altri che ci hanno provato). ⏳ Blueprint da sviluppare presto, dopo Gas.
Sistema per vendere siti e servizi digitali alle attività locali: trovare le attività, analizzare la presenza online, punteggio da 0 a 100, strategia e bozza del sito, rubrica e ricontatti.
- Strumenti previsti: Airtable (archivio), HubSpot (trattative), Make (automazioni), agente "GAS WEB SCOUT".
- Tre fasi: prima a mano con le prime automazioni; poi raccolta e analisi automatiche; poi quattro agenti (Scout, Analyst, Sales, Follow-up).
- Obiettivo: 1000 attività raccolte, le migliori 100 pronte per la chiamata, tu fai solo la vendita.
- Nodi aperti: dati dei contatti su servizi terzi (GDPR). La scelta Make contro Gas-Python è chiusa: Gas-Python, n8n come piano B (R11).

---

## 11. Scartato o già deciso (non riaprire)

- ❌ Cerebras gratuito come gradino: contesto reale di 8192 token e coda satura.
- ❌ GitHub Models come gradino (limiti da prototipo e un token GitHub sul server); resta usabile come banco di prova in sviluppo.
- ❌ Più di circa 6 gradini nella cascata.
- ~~❌ Accesso con l'abbonamento Claude dentro Gas~~: superato il 19 ottobre, è il nuovo R2.
- ❌ OmniRoute nel motore, per ora. Riaperto solo come sonda fuori dal motore (capitolo 5.6).
- 🔄 Claude Code sul server di produzione: **da ridecidere con R2 e R5** (19 ottobre).
- ❌ "Sempre in ascolto" che agisce senza essere chiamato.
- ❌ Instagram come fonte automatica.
- ❌ Fusione dei contatti, ripristini e pulizie in mano al modello: solo a mano.
- ❌ L'opzione di GitHub che cancella da sola i rami dopo il merge.
- ❌ Riscrittura della storia di git.
- ✅ Deciso: livello 2 (firma) per `gas.py`, `brains/` e `modules/`; lettura libera.
- ✅ Deciso: cascata del bot Opus 5.5 → Opus 4.8 → Fable 5.1.
- ✅ Deciso: il revisore cita sempre col percorso completo.
- ✅ Deciso: il verdetto del verificatore esterno va come commento sulla PR.
- ✅ Deciso: si lavora in Cowork; la chat di strategia fa il controllo esterno ogni tanto.
- ✅ Deciso: i brainstorming anche a voce; i comandi per l'agente sempre scritti.
- ❌ Secondo account GitHub "macchina": scartato (19 ottobre), coperto dal token ristretto.
- ❌ Make per il marketing; Twilio per l'allarme; ElevenLabs a pagamento; Ollama; crediti API Claude per ora (19 ottobre).
- ❌ Merge automatico dopo N notti pulite: sostituito da "merge sempre al mattino, per ora" (19 ottobre).

---

## 12. Progetti satellite (fuori dal motore)

Il bot di trading è uscito dalla roadmap (19 ottobre): l'operatore lo ha fatto altrove.

- **TradeGasFX**: sito con pannello servizi e contatto WhatsApp. Vive su un ramo del repo di Gas (20 commit, solo documenti). Da decidere se spostarlo in un repo suo. Prima di pubblicare: testimonianze vere e verifica delle condizioni dichiarate.
- **Sala segnali sull'oro (XAUUSD) su Telegram**: tuo piano separato, non è nella roadmap di Gas.

---

## 13. Come è stata controllata

1. Ogni file di `reports/`, `CLAUDE.md`, i file in `.claude/` e i sette documenti del progetto sono stati letti per intero, da lettori diversi.
2. I punti tecnici sono stati riscontrati nel codice: 41 affermazioni controllate, nessuna falsa, 10 imprecise e corrette.
3. Cinque controlli indipendenti hanno confrontato la bozza con le fonti, uno per gruppo: roadmap del repo e piani parcheggiati; prima metà dello stato; seconda metà e storico; progetti, procedure e codice; documenti del progetto, memoria e 40 ricerche nelle chat.
4. I controlli hanno trovato circa 45 voci mancanti e circa 20 frasi sbagliate o imprecise. Sono tutte dentro questa versione.
5. Le regole Anthropic sono state verificate sulle pagine ufficiali l'11 ottobre 2026.

**Limiti onesti.**
- Lo stato delle PR aperte non l'ho potuto leggere da GitHub: le voci "da verificare" sono segnate.
- Le chat si cercano per spezzoni, non si rileggono intere: una frase detta una volta sola e mai scritta in un file può essere sfuggita.
- Dove due file si contraddicono ho preso il più recente e l'ho scritto.
- Sette riserve di giugno hanno solo il nome: il dettaglio non è in nessun file.
