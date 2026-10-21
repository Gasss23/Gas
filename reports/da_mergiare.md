# DA MERGIARE — coda della chat Motore

> Decisione dell'operatore (2026-10-21): la chat Motore lavora di fila sulla roadmap; qui si accumula ciò che è pronto, una voce per fetta, con i pro e i contro del merge. L'operatore passa 1-2 volte al giorno, legge questa pagina e scrive «mergia #N» oppure «no». Le voci mergiate si tolgono.

> **Decisione per te (C6, bottone «Modifica» e firme a gruppi):** il 30 settembre avevi deciso «una firma per ogni azione, niente gruppi»; il «Modifica» non ha ancora un disegno. Non lo costruisco finché non dici: (a) lasciamo così, (b) disegnamo il «Modifica» (cosa si può cambiare e come si rifirma), (c) anche le firme a gruppi.

## PR aperta del ramo `feat/merge-automatico-z1xjx2` (nuova, dopo il merge di #232)

> **Bot di verifica su #233:** il testo del verdetto è sempre APPROVATO CON RISERVE (nessuna ALTA/MEDIA), ma il check resta rosso per «caratteri invisibili nel testo»: questa PR parla proprio di caratteri invisibili e il bot li ricopia quando li cita. Ho tolto quelli nei miei file; se il check resta rosso, il merge lo decidi tu (regola: niente merge autonomo).

### 1. Avviso sui file delicati: chiavi e database tornano, via le parole ambigue
- **Cosa:** l'avviso «file nuovo che sembra delicato» torna a scattare su `server.pem.txt`, `dump.sql.txt`, `prod.env.txt`, `vault.kdbx.txt`; non scatta più su `customer.service.md`, `manuale.html.pdf`, `node.js.md`; i caratteri invisibili nel nome non lo aggirano più.
- **Pro:** chiude R-390-1 e le note della verifica esterna #232; meno falsi allarmi, nessun trucco con caratteri invisibili.
- **Contro:** `a.html.txt`, `x.js.md`, `a.ts.txt` non vengono più segnalati (R-391-1, bassa, scelta voluta); `dev.env.md` dà un avviso in più (R-391-2, cosmetica). È solo un avviso: non blocca nulla.
- **Controlli:** revisore #391 (chat Motore) APPROVATO CON RISERVE; gate 759, kernel 950 PASS. Verifica esterna #233 APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/233#issuecomment-6314303625)): V-1 MEDIA handoff mancante → rigenerato a fine giro; V-3 chiusa nella voce 4; V-2 non serve (i `.sh`/`.py` finali vanno già alla firma, review #393). Bot: vedi la PR.

### 2. Terza chat «Mani» (solo documento)
- **Cosa:** in `reports/lavoro_parallelo.md` l'area e il compito della chat Mani (R6, leggere il web, modulo `modules/web/` a sé) con il prompt da incollare.
- **Pro:** si lavora in tre senza conflitti (cartelle separate).
- **Contro:** la chat Mani tocca anche un passo di `ci.yml` (solo il suo); l'aggancio a Gas resta alla chat Motore.

### 3. Lanciare il giro notturno da Telegram (roadmap R1)
- **Cosa:** col bot acceso, `/notte` lancia un giro completo e `/compito <nome>` un solo compito del catalogo; anche `python3 gas.py notte <nome>` da terminale. Il bot risponde «avviato», il riepilogo arriva a fine giro come dal timer.
- **Pro:** chiude la voce R1 «lanciare un compito o un giro da Telegram»; utile per la prova dal vero di giorno; solo le chat autorizzate, mai passa dal modello, niente shell, un giro alla volta.
- **Contro:** il giro gira coi permessi del bot (stesse chiavi); un compito oltre il numero massimo del catalogo risulta «non trovato» (R-392-3, cosmetica); se Python muore prima di partire resta solo una riga in `.gas_notte/telegram_giro.log`, nessun avviso su Telegram (R-393-1, bassa).
- **Controlli:** revisore #392 (chat Motore) APPROVATO CON RISERVE; notte 96 passed, kernel 950 PASS; sonda reale (processo vero avviato, riepilogo scritto). Verifica esterna #233 (2° giro) APPROVATO CON RISERVE, nessuna ALTA/MEDIA ([commento](https://github.com/Gasss23/Gas/pull/233#issuecomment-6314455074)).

### 4. Rifiniture della voce 3 e dell'avviso
- **Cosa:** il bot avvia sempre il `gas.py` vero (anche se parte da un'altra cartella), l'uscita del giro va in `.gas_notte/telegram_giro.log`; `a.plist.txt` e `a.desktop.txt` di nuovo segnalati.
- **Pro:** chiude R-392-1, metà di R-392-2 e V-3 della verifica esterna #233.
- **Contro:** il log non ha rotazione (R-393-2, cosmetica).
- **Controlli:** revisore #393 (chat Motore) APPROVATO CON RISERVE; notte+gate 858 passed, kernel 950 PASS.

### 5. Avviso se il giro lanciato da Telegram muore prima di partire
- **Cosa:** se il giro lanciato dal bot si ferma prima di cominciare (errore di Python, import), arriva su Telegram «si è fermato prima di partire»; il giro scrive un marcatore di avvio, così non ci sono doppi messaggi; `/compito` non accetta nomi che iniziano con «-».
- **Pro:** chiude R-393-1, R-394-1 e le V-1/V-3 della verifica esterna #233 (2° giro); niente silenzi dopo «avviato».
- **Contro:** compiti del catalogo che iniziano con «-» o «_» non si lanciano da Telegram (R-395-1, bassa); due casi rari di avviso doppio o perso (R-395-2, cosmetica).
- **Controlli:** revisori #394 e #395 (chat Motore) APPROVATO CON RISERVE; notte 103 passed, kernel 950 PASS; sonda reale con un crash vero all'avvio.

### 6. Richiesta di firma inviata in parallelo (roadmap 5.2, R-c4b1-3)
- **Cosa:** il messaggio con i bottoni Approva/Rifiuta (e le notifiche) parte verso tutti i destinatari insieme, non uno dopo l'altro.
- **Pro:** con più telefoni autorizzati il turno di Gas non resta fermo 15 secondi per ciascuno; regola di sicurezza invariata (se non arriva a nessuno la firma è revocata).
- **Contro:** il tetto di ~15 s non è assoluto (rete lenta, oltre 8 destinatari: R-396-1, bassa).
- **Controlli:** revisore #396 (chat Motore) APPROVATO CON RISERVE; kernel 952 PASS. Verifica esterna #233 (3° giro) APPROVATO CON RISERVE, nessuna ALTA/MEDIA, «mergiabile» ([commento](https://github.com/Gasss23/Gas/pull/233#issuecomment-6314696663)).

### 7. Registro e archivio dei vettori sempre al posto giusto (roadmap R7)
- **Cosa:** `gas_debug.log` sta sempre accanto a `gas.py`, anche se Gas parte da un'altra cartella; `reindex`, `calibrate-vectors`, `eval-vectors` e `doctor` usano l'archivio dei vettori indicato da `GAS_VECTORS_DB`, come il resto di Gas.
- **Pro:** chiude due voci di R7; il bot Telegram avviato da un'altra cartella non sparpaglia più il registro.
- **Contro:** se la cartella di Gas non è scrivibile (es. VPS in sola lettura) Gas non parte (rischio già presente, ora senza scappatoia); con una cartella di lavoro diversa, un file utente `gas_debug.log` lì viene trattato come registro (R-397-1, bassa).
- **Controlli:** revisori #397 e #398 (chat Motore) APPROVATO CON RISERVE; kernel 955 PASS; pytest intero 1627 passed.

### 8. Cancello: caratteri invisibili e lettere «travestite» nei nomi dei file (sicurezza)
- **Cosa:** un nome come `run.sh` o `.env` con dentro un carattere invisibile non scivola più al livello libero (prima `.env` con un invisibile era libero); dopo una lettura, un nome che sembra `.md` ma non lo è davvero (invisibili, lettere a larghezza piena) va alla firma.
- **Pro:** chiude V-1 della verifica esterna #233 (3° giro), R-398-1 e R-399-1; il cancello diventa solo più stretto.
- **Contro:** nomi con accenti scritti «scomposti» (file nati su vecchi Mac) dopo una lettura chiedono la firma (R-400-1, bassa). Fetta di sicurezza: secondo passaggio nella chat claude.ai consigliato.
- **Controlli:** revisori #398, #399, #400 (chat Motore) APPROVATO CON RISERVE; gate 776 passed, kernel 955 PASS.

### 9. Gas parte anche se il registro non si può scrivere
- **Cosa:** se `gas_debug.log` non si può aprire (cartella in sola lettura), Gas parte lo stesso, scrive solo a schermo e `gas doctor` lo segnala; `avvio.cmd.txt` di nuovo segnalato come delicato.
- **Pro:** chiude V-2 del bot e V-2 della verifica esterna #233 (4° giro); rispetta «zero crash».
- **Contro:** in quel caso la scatola nera è spenta finché non si sistemano i permessi (lo dice doctor).
- **Controlli:** revisori #401 e #402 (chat Motore) APPROVATO CON RISERVE; kernel 957 PASS, gate 777.

### 10. Cancello: invisibili di ogni tipo, senza fondere le parole (sicurezza)
- **Cosa:** anche i caratteri invisibili «non standard» (selettori di variante, caratteri non assegnati, controlli) non aggirano più la firma; e un invisibile messo fra due parole («x<invisibile>secret.md») non nasconde più un nome da segreto. Bot Telegram: «/notte@AltroBot» ignorato; con il riepilogo spento la risposta non lo promette.
- **Pro:** chiude V-1/V-2/V-3 del bot (5° giro), R-403-1 (media) e R-404-1 (alta). R-404-1 era una regressione introdotta dalla voce 8 di questa stessa PR: senza questa voce la voce 8 NON va mergiata. Sonda del revisore su 46.707 nomi: nessun caso meno severo di prima della sessione.
- **Contro:** nomi di file con caratteri insoliti chiedono più spesso la firma. Restano R-405-1 (bassa, già esistente: read_file su un nome fatto solo di invisibili) e R-404-2 (un test vecchio del lock a volte fallisce, 1 su 20).
- **Controlli:** revisore #403 APPROVATO CON RISERVE, #404 BOCCIATO, #405 APPROVATO CON RISERVE (chat Motore); gate+notte 917 passed, kernel 957 PASS.
