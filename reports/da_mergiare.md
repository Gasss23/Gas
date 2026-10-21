# DA MERGIARE — coda della chat Motore

> Decisione dell'operatore (2026-10-21): la chat Motore lavora di fila sulla roadmap; qui si accumula ciò che è pronto, una voce per fetta, con i pro e i contro del merge. L'operatore passa 1-2 volte al giorno, legge questa pagina e scrive «mergia #N» oppure «no». Le voci mergiate si tolgono.

## PR aperta del ramo `feat/merge-automatico-z1xjx2` (nuova, dopo il merge di #232)

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
- **Controlli:** revisore #396 (chat Motore) APPROVATO CON RISERVE; kernel 952 PASS.
