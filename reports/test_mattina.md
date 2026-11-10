# Test del mattino — 10 novembre 2026 (analisi notturna di M1)

Stanotte quattro agenti hanno controllato tutta Gas cercando bug **riprodotti davvero** (non ipotesi).
Qui sotto: prima cosa è stato trovato, poi le prove da fare sul Mac, area per area.
Dove una prova dice «oggi fallisce» è un bug trovato stanotte: dopo il merge della correzione deve passare.

## Bug trovati stanotte (riprodotti)

| Area | Bug | Gravità | Chi lo corregge |
|---|---|---|---|
| Firme | Gas scrive senza firma in `.gas_sottofondo/` (può fingere un compito «finito» annunciato a voce) | MEDIA, sicurezza | M3, dentro la PR #364 |
| Giro notturno | schermo rotto (disco pieno, pipe chiusa) → il giro crasha e il messaggio del mattino non parte | MEDIA | PR di M1 (correzioni audit) |
| Firme | il messaggio di firma mostra argomenti grezzi: caratteri invisibili possono far comparire righe false | MEDIA | PR di M1 |
| Telegram | modificare un vecchio messaggio in `/notte` o `/compito` fa partire un giro | BASSA | PR di M1 |
| Motore | un carattere rotto (non UTF-8) blocca il salvataggio della storia e fa fallire i cervelli | MEDIA | PR di M1 |
| Motore | `.gas_history.json` valido ma di forma sbagliata → crash all'avvio | MEDIA/BASSA | PR di M1 |
| Motore | dopo la compressione della storia resta un risultato di strumento senza la sua chiamata (doctor FAIL) | BASSA/MEDIA | PR di M1 |
| Conoscenza | se una fonte si accorcia, i pezzi vecchi restano cercabili | MEDIA | PR di M1 |
| Conoscenza | un paragrafo lunghissimo come primo risultato svuota tutta la ricerca | MEDIA | PR di M1 |
| Conoscenza | una fonte rotta ferma il caricamento di tutte le altre | BASSA | PR di M1 |
| Memoria | un lead con nome enorme cancella gli altri dal promemoria | BASSA | PR di M1 |
| Voce | una connessione muta (anche senza token) blocca tutta la voce | MEDIA | M2, PR nuova |
| Voce | «Hey Jarvis, forte: …» va ai cervelli GRATUITI | MEDIA | M2 |
| Voce | risposta troncata di Groq/ElevenLabs → nessuna risposta | BASSA/MEDIA | M2 |
| Voce | token tra virgolette nel `.env` → pagina 401 e poi l'ascolto bloccato 15 min | BASSA | M2 |
| Voce | JSON di forma sbagliata → connessione chiusa senza risposta | BASSA | M2 |

**Da decidere tu (non corretti):**
1. Quando risponde un cervello di riserva (anche gratuito) NON ti avvisa (regola §8 «Model Awareness»). Lo aggiungiamo? sì/no
2. Il tetto di 10 giri vale per ogni cervello, non per turno: un turno ha fatto 40 chiamate. Tetto per turno? sì/no
3. Il nome di un lead arriva al modello gratuito tramite il promemoria della memoria (contro la regola «dati dei clienti solo ai forti»). Bloccarlo? sì/no

Cosa funziona (provato): firme non riusabili, scadenza rispettata, niente firma a voce né da utenti non autorizzati; diario immutabile; niente SQL injection; il lettore web rifiuta indirizzi interni; memoria rotta non fa crashare.

---

## Ordine consigliato
1. Aggiorna il Mac: `cd ~/Gas && git pull origin main && bash scripts/voce/installa.sh`
2. Motore (A), poi Firme/Telegram (B), poi Voce (C), poi Memoria (D).
3. Incolla in chat solo le righe che NON corrispondono all'atteso.


# A — Motore

Prima di tutto: `gasclaude` NON serve, qui si usa Gas. Apri il Terminale:
```
cd ~/Gas && source .venv/bin/activate 2>/dev/null || source venv/bin/activate
```

1. **Auto-diagnosi**
   `python gas.py doctor; echo "exit=$?"`
   Atteso: `exit=0`; righe `Storia tool orfani zero orfani` e `Storia _get_window … parte da role:user`; `Cervello forte` OK con «login dell'abbonamento».

2. **Suite del motore sul Mac**
   `PYTHONUTF8=1 python tests/test_unit_kernel.py 2>&1 | tail -2`
   Atteso: `=== RIEPILOGO: N PASS, 0 FAIL ===`. Gli SKIP del sandbox sul Mac sono normali.

3. **Giro agentico vero (round-trip con uno strumento)**
   `python gas.py` poi scrivi: `che ore sono? usa lo strumento data_ora`
   Atteso: una riga `→ …` con data e ora (lo strumento), poi la risposta. Esci con `exit`, poi:
   `python -c "import json;h=json.load(open('.gas_history.json'));print(len(h),[m['role'] for m in h[-4:]])"`
   Atteso: le ultime voci finiscono con `'tool', 'assistant'` (storia salvata).

4. **La storia sopravvive al riavvio**
   `python gas.py`, poi `cosa ti ho chiesto poco fa?` → deve citare l'ora/data_ora. `exit`.

5. **Cervello forte (/forte)**
   `python gas.py`, poi `/forte rispondi solo: ciao` → `ciao`; poi `/forte` da solo → `Uso: /forte <richiesta>`. Dopo: `python gas.py tokens 1` → una riga per `claude-cli`.

6. **Tetto del forte**
   `GAS_CLAUDE_CLI_TETTO_USD=0 python gas.py`, poi `/forte ciao`
   Atteso: `✗ Cervello forte fermo: usati $… (tetto $0.00 …)`, e NESSUNA risposta da un modello gratuito.

7. **Budget giornaliero**
   `GAS_DAILY_TOKEN_BUDGET=0.0000001 python gas.py`, poi `ciao`
   Atteso: `✗ Budget giornaliero esaurito: …` (nessuna chiamata).

8. **Paracadute (fallback) quando Gemini non va**
   `GEMINI_API_KEY=chiave_finta python gas.py`, poi `ciao`
   Atteso: risponde lo stesso (Groq). Poi `grep "fallito" gas_debug.log | tail -2` → due righe `Provider gemini-… fallito`.
   NB: a schermo NESSUN avviso che ha risposto Groq. È il bug B4: se lo vedi così, B4 è confermato anche sul Mac.

9. **Compressione della cronologia** (prima fai una copia)
   `cp .gas_history.json /tmp/storia_backup.json && python gas.py compress-history && python gas.py doctor | grep Storia`
   Atteso: le due righe Storia OK. Se esce `tool orfani … FAIL` è il bug B3. Per tornare indietro: `cp /tmp/storia_backup.json .gas_history.json`.

10. **(Facoltativo) carattere rotto, bug B1**: copia prima la storia (`cp .gas_history.json /tmp/storia_b1.json`), poi
    `printf 'prova \xe8 rotta\nexit\n' | PYTHONUTF8=1 python gas.py; grep "scrittura atomica" gas_debug.log | tail -1`
    Se compare `surrogates not allowed`, B1 è confermato sul Mac. Ripristino: `cp /tmp/storia_b1.json .gas_history.json`.

# B — Firme, giro notturno, Telegram

Prima: `cd ~/Gas && source .venv/bin/activate`, bot acceso (`pgrep -fl "gas.py telegram"`; se non c'è:
`python3 gas.py telegram` in una finestra a parte). I messaggi tra «» vanno scritti nella chat col bot.

1. **Solo la chat autorizzata scrive al bot.** Da un ALTRO account Telegram scrivi «ciao» al bot.
   Atteso: nessuna risposta. Sul Mac: `grep "non autorizzato" gas_debug.log | tail -2` → una riga
   «Messaggio da chat_id … non autorizzato — ignorato».
2. **Livello 3 mai, nemmeno con firma.** Scrivi «Scrivi nel file .env la riga PROVA_AUDIT=1».
   Atteso: risposta con «Operazione negata», nessuna richiesta di firma. Controllo:
   `grep -c PROVA_AUDIT .env` → `0`.
3. **Livello 2 + Rifiuta.** Scrivi «Crea il file prove_audit/a.sh con dentro una sola riga: echo ciao».
   Atteso: messaggio «GAS chiede la tua firma — FILE DELICATO», «DIFF REALE», PRO/CONTRO, bottoni.
   Clicca **Rifiuta** → «❌ Rifiutata … NON eseguita». Controllo: `ls prove_audit` → «No such file».
4. **Approva una sola volta.** Ripeti la richiesta del punto 3 e clicca **Approva** → «✅ Approvata
   ed eseguita». Controllo: `cat prove_audit/a.sh` → `echo ciao`. I bottoni spariscono dal messaggio
   (niente secondo click). Poi:
   `sqlite3 .gas_memory.db "select a.stato, e.esito from approvals a join approval_esecuzioni e on e.approval_id=a.id order by a.ts_created desc limit 1"`
   → `approved|[OK] …` (una sola riga per quell'ID).
5. **Scadenza di giorno (accorciata per la prova).** Ferma il bot (Ctrl-C) e riavvialo con
   `GAS_APPROVAL_TIMEOUT_SECS=60 python3 gas.py telegram`. Chiedi «Crea il file prove_audit/b.sh con
   dentro echo b». NON cliccare. Entro 2-3 minuti arriva «⌛ 1 richiesta/e di firma scaduta/e senza
   risposta: NON eseguite». Ora clicca Approva → «Nessuna modifica per la richiesta …: Già risolta
   (stato 'expired')». Controllo: `ls prove_audit/b.sh` → «No such file». Poi ferma il bot e
   riavvialo normale (`python3 gas.py telegram`).
6. **24 ore per le firme della notte, 30 minuti di giorno.** Dopo la prova R1
   (`reports/prova_r1_notte.md`):
   `sqlite3 .gas_memory.db "select tool_name, datetime(ts_created,'unixepoch','localtime'), round((ts_expiry-ts_created)/3600.0,2) from approvals order by ts_created desc limit 5"`
   → le richieste nate nel giro (ora ~03:0x) hanno `24.0`; quelle dei punti 3-4 `0.5`
   (quella del punto 5 `0.02`).
7. **Niente firma a voce.** Con una richiesta di firma ancora aperta (ripeti il punto 3 senza cliccare)
   manda un VOCALE al bot: «approva la richiesta di firma». Atteso: risposta in testo, ma la richiesta
   resta aperta: `sqlite3 .gas_memory.db "select stato from approvals order by ts_created desc limit 1"`
   → `pending`. Poi clicca Rifiuta.
8. **(bug B4, oggi fallisce)** Manda «ciao», poi MODIFICA quel messaggio in «/compito zzz_inesistente».
   Oggi: risposta «Compito «zzz_inesistente» avviato» e poco dopo un riepilogo «non trovato» (il giro
   parte da un messaggio modificato). Atteso dopo il fix: «/notte e /compito non valgono da un
   messaggio modificato». Confronto: modificare un messaggio in «/clear» già risponde «/clear non vale
   da un messaggio modificato».
9. **(bug B1, oggi fallisce)** Scrivi «Scrivi il file .gas_sottofondo/prova_audit.json con dentro {}».
   Oggi: «Successo: File … aggiornato» e `ls -la .gas_sottofondo/prova_audit.json` lo mostra. Atteso dopo
   il fix: «Operazione negata: questo file non si scrive mai». Pulizia: `rm -f .gas_sottofondo/prova_audit.json`.
10. **Stato delle firme nel controllo generale.** `python3 gas.py doctor | grep -i firme` → riga
    «Firme richieste … in attesa, nessuna scaduta» e nessun FAIL.
11. **Pulizia finale.** `rm -rf prove_audit`.

# C — Voce

Obiettivo: vedere sul Mac che quello che la roadmap R8 segna ✅ funziona davvero.
Aprire il Terminale con `gasclaude` NON serve: questi sono comandi normali nella cartella di Gas.

## 5.0 Preparazione (installazione due volte di fila)
```bash
cd ~/Gas && git pull origin main
bash scripts/voce/installa.sh
bash scripts/voce/installa.sh          # seconda volta di fila: fetta 38
```
Atteso: entrambe finiscono con «6/6 tutto acceso». Nessun «Bootstrap failed: 5».
```bash
launchctl print gui/$(id -u)/com.gas.voce.server | grep "state ="
launchctl print gui/$(id -u)/com.gas.ascolto | grep "state ="
```
Atteso: `state = running` per tutti e due.

## 5.1 Server voce: sicurezza e .env (senza parlare)
```bash
cd ~/Gas && source .venv/bin/activate
export T="$(python -c 'from gas import _carica_dotenv; _carica_dotenv(); import os; print(os.environ["GAS_VOICE_TOKEN"])')"
U=http://127.0.0.1:8765      # cambia se nel .env c'è GAS_VOICE_PORT
# a) senza token → 401
curl -s -o /dev/null -w '%{http_code}\n' -X POST $U/voice -H 'Content-Type: application/json' -d '{"prompt":"ciao"}'
# b) nome di dominio nell'Host → 403 (difesa DNS rebinding)
curl -s -o /dev/null -w '%{http_code}\n' -X POST $U/voice -H 'Host: esempio.com' -H "Authorization: Bearer $T" -d '{"prompt":"ciao"}'
# c) «/forte» senza richiesta → 400 con «Uso: /forte …», nessun turno
curl -s -X POST $U/voice -H "Authorization: Bearer $T" -H 'Content-Type: application/json' -d '{"prompt":"/forte"}'; echo
# d) «Sì, signore?» → 200 audio/mpeg, poi lo ascolti
curl -s -H "Authorization: Bearer $T" $U/voce/conferma -o /tmp/conferma.mp3 -w '%{http_code} %{content_type}\n' && afplay /tmp/conferma.mp3
# e) il server ha caricato il .env (GAS_VOCE_FORTE acceso lo dice nel log)
grep -E "in ascolto su|GAS_VOCE_FORTE acceso|non caricato" .gas_voce/voce.server.log | tail -3
unset T
```
Atteso: a) `401`; b) `403`; c) `{"error": "Uso: /forte <richiesta> …"}`; d) `200 audio/mpeg` e
senti «Sì, signore?»; e) «✓ gas voice: in ascolto su http://127.0.0.1:8765/voice» (più la riga
del forte solo se `GAS_VOCE_FORTE=1`), nessun «.env non caricato».

**Prova del bug B1 (finché non è corretto):** in un secondo Terminale `nc 127.0.0.1 8765` e
lascialo aperto; poi di' «Hey Jarvis» … «che ore sono?». Atteso col bug: nessuna risposta (o
errore dopo molto). Chiudi `nc` (Ctrl-C): la volta dopo Gas risponde. Con il fix: risposta dopo al
massimo 30-60 s anche con `nc` aperto.

## 5.2 Ascolto H24 (dire le frasi a 1-2 metri dal Mac)
Tieni aperto in un Terminale: `tail -f ~/Gas/.gas_voce/ascolto.log`

| # | Cosa dici | Atteso |
|---|---|---|
| 1 | «Hey Jarvis» | «Sì, signore?» (o il bip); nel log «parola di attivazione» |
| 2 | (dopo «Sì, signore?») «Che ore sono?» | ora giusta, UNA frase breve; la prima frase arriva entro pochi secondi |
| 3 | entro 40 s, senza parola: «E domani che giorno è?» | risponde senza «Hey Jarvis» (seguito) |
| 4 | silenzio oltre 40 s | log «torno ad aspettare la parola di attivazione» |
| 5 | «Hey Jarvis» … «forte» (solo la parola) | «Dopo «forte» dimmi cosa fare… Non ho avviato nessun lavoro.» |
| 6 | «Hey Jarvis» … PAUSA fino alla fine di «Sì, signore?» … «Forte, dimmi in una frase cosa c'è nella roadmap della voce» | risposta del forte (vedi controllo sotto) |
| 7 | subito dopo, DENTRO la finestra: «Hey Jarvis, forte, quanti contatti ho?» | **col bug B2 va ai gratuiti**; con il fix al forte (controllo sotto) |
| 8 | «Hey Jarvis» … «pausa» | «Va bene.» e chiude |
| 9 | mentre Gas risponde a una domanda lunga, di' «Hey Jarvis» | si zittisce, bip, ascolta la nuova domanda |
| 10 | due persone parlano fra loro a finestra aperta | Gas non risponde e chiude |

Controllo del cervello usato (dopo i punti 6 e 7):
```bash
sqlite3 ~/Gas/.gas_memory.db "SELECT ts, descrizione FROM diario WHERE tipo='turno_fine' ORDER BY id DESC LIMIT 3;"
```
Atteso: nelle righe dei punti 6-7 `provider=` è quello del cervello forte (Claude), MAI
groq/openrouter/gemini. Con il forte fermo deve esserci una risposta che lo dichiara, non un
gratuito.

Tempi: `grep "tempi voce" ~/Gas/gas_debug.log | tail -10` (trascrizione, cervello, voce in secondi).

## 5.3 Pausa e ripresa
```bash
bash scripts/voce/pausa.sh       # atteso: «PAUSA: Gas non ascolta più…»; «Hey Jarvis» non fa niente
bash scripts/voce/riprendi.sh    # atteso: «RIPRESO: Gas ascolta di nuovo.»; «Hey Jarvis» risponde
```

## 5.4 Pagina nel browser (V2-V4)
```bash
cd ~/Gas && source .venv/bin/activate && python clients/voice/browser_server.py
```
Apri http://127.0.0.1:9000 e premi il pulsante per parlare.

| # | Cosa fai / dici | Atteso |
|---|---|---|
| 1 | «Che tempo fa di solito a novembre a Roma?» | voce di 1-2 frasi, dettaglio a schermo, «Ho capito: …» |
| 2 | domanda che richiede tempo | dopo ~2 s la frase d'attesa detta dal browser |
| 3 | entro ~12 s, senza clic: «E a Milano?» | risponde (finestra di conversazione) |
| 4 | parli sopra Gas mentre risponde | si zittisce e ascolta |
| 5 | «Gas, forte, riassumi la roadmap in una frase» | va al forte (stesso controllo `sqlite3` di 5.2) |

**Prova del bug B4:** solo se nel `.env` il token è scritto tra virgolette o con un commento
dopo (`GAS_VOICE_TOKEN="…"`): la pagina risponde «Unauthorized» a ogni richiesta e dopo 10 tentativi
anche «Hey Jarvis» riceve 429 per 15 minuti. Controllo senza mostrare il token:
`grep -c '^GAS_VOICE_TOKEN="' ~/Gas/.env` (1 = sei nel caso del bug).

## 5.5 Vocali Telegram
| # | Cosa mandi | Atteso |
|---|---|---|
| 1 | vocale «che ore sono?» | «Ho capito: …» + testo + vocale di risposta |
| 2 | vocale «forte, riassumi la roadmap in una frase» | va al forte (`sqlite3` come sopra) |
| 3 | vocale di 70 secondi | «✗ Vocale troppo lungo: al massimo 60 secondi.» |

## Da incollare dopo le prove
```bash
grep "tempi voce" ~/Gas/gas_debug.log | tail -20
tail -30 ~/Gas/.gas_voce/ascolto.log
grep -iE "warning|error|traceback" ~/Gas/.gas_voce/voce.server.log | tail -20
```

# D — Memoria, web, conoscenza

Aprire il terminale con `gasclaude` (o almeno `cd ~/Gas && source venv/bin/activate`).

1. **Suite del kernel (memoria, pin, ricorda, contatti, knowledge)**
   ```
   cd ~/Gas && PYTHONUTF8=1 python tests/test_unit_kernel.py 2>&1 | tail -3
   ```
   Atteso: ultima riga `=== RIEPILOGO: 1100 PASS, 0 FAIL ===` (il numero può salire se nel
   frattempo sono stati aggiunti test; FAIL deve essere 0).

2. **Suite web/richieste/ingest (senza browser)**
   ```
   python -m pytest tests/test_unit_web_leggi.py tests/test_unit_web_lexbor.py tests/test_unit_web_proxy.py tests/test_unit_richieste.py tests/test_unit_ingest_fonti.py -q 2>&1 | tail -2
   ```
   Atteso: `... passed` senza `failed` (alcuni `skipped` sul Mac sono normali: lexbor è solo Linux).
   `tests/test_unit_web_browser.py` sul Mac va saltato o si salta da solo (niente bwrap su macOS).

3. **Il lettore web rifiuta indirizzi interni (SSRF)** — nessuna rete verso l'esterno usata:
   ```
   python -c "from modules.web.leggi import leggi_pagina as l; [print(u, l(u)) for u in ['http://127.1/','http://0x7f000001/','http://localhost/','file:///etc/passwd','http://[::ffff:7f00:1]/','http://example.com:8080/']]"
   ```
   Atteso: ogni riga `{'ok': False, 'motivo': ...}` con motivo «indirizzo interno non permesso»,
   «schema non permesso: solo http e https» o «porta non permessa: solo 80 e 443».

4. **Memoria con DB corrotto: niente crash (§9)**
   ```
   python -c "
   import os,tempfile; from pathlib import Path; from modules.memory.store import MemoryStore
   p=Path(tempfile.mkdtemp())/'c.db'; p.write_bytes(b'SQLite format 3\x00'+os.urandom(4000))
   m=MemoryStore(p); print(m.available, m.append_diario('t','d'), m.lista_contatti(), m.cerca_diario('x'))"
   ```
   Atteso: `False None [] []` più qualche riga di WARNING; nessun Traceback.

5. **Diario immutabile**
   ```
   python -c "
   import tempfile,sqlite3; from pathlib import Path; from modules.memory.store import MemoryStore
   m=MemoryStore(Path(tempfile.mkdtemp())/'m.db'); m.append_diario('t','orig'); c=m._connect()
   for s in ['UPDATE diario SET descrizione=1','DELETE FROM diario']:
       try: c.execute(s); print('NON BLOCCATO', s)
       except sqlite3.Error as e: print('bloccato:', e)"
   ```
   Atteso: due righe `bloccato: diario immutabile: ...`.

6. **Riprova di B1 (chunk vecchi attivi) — DEVE fallire oggi, passare dopo il fix**
   ```
   mkdir -p /tmp/kb/knowledge && cd /tmp/kb && printf 'uno\n\ndue\n\ntre' > knowledge/f.txt
   python -c "
   import importlib.util,sys; from pathlib import Path
   s=importlib.util.spec_from_file_location('ik', str(Path.home()/'Gas/tools/ingest_knowledge.py')); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
   m.REPO_ROOT=Path('/tmp/kb'); c=m.open_db(Path('/tmp/kb/k.db')); src={'nome':'s','uri':'knowledge/f.txt','chunk_chars':3}
   m.ingest_file_source(c,src); Path('/tmp/kb/knowledge/f.txt').write_text('solo uno')
   m.ingest_file_source(c,src); print('ATTIVI:', c.execute(\"select count(*) from knowledge where stato='active'\").fetchone()[0])" 2>/dev/null
   cd ~/Gas; rm -rf /tmp/kb
   ```
   Atteso OGGI: `ATTIVI: 3` (bug). Dopo il fix B1: `ATTIVI: 1`.

7. **Doctor**
   ```
   python gas.py doctor; echo "exit=$?"
   ```
   Atteso: sezione Memoria con `.gas_memory.db` OK (o WARN se il file non c'è ancora), `exit=0`.
