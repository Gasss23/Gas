# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 — Server voce reso sicuro, fetta 1 (R8: tentativi falliti, tetto al testo, avvio fail-closed) — chat M2, coordinata da M1

---

## §0 DECISIONI UMANE RICHIESTE

1. **PR di sicurezza: il merge lo decide l'operatore** (CLAUDE.md §10; tocca accessi e rete esposta).
2. Proposta `reports/proposta_voce_sicura.md`: scelte per le fette 2 e 3 (tunnel privato, TLS opzionale, token di sessione e loro durata) e soglie della fetta 1 (10 tentativi falliti in 10 minuti per IP, 120 richieste a testo all'ora).
3. Limite noto da confermare (R-720-2-M2): sul Mac tutti i client arrivano da 127.0.0.1, quindi un client con un token vecchio blocca per 15 minuti anche la pagina e l'ascolto H24.

---

## §1 SCOPE & ESITO FETTE

- **PR #356**: `MERGIATA` (69d76b9) col sì dell'operatore riferito da M1.
- **R8 fetta 1, server voce più sicuro**: `FATTA` in `modules/voice/server.py`:
  - C1 — `_autorizza()`: tetto ai tentativi con token sbagliato per IP (`GAS_VOICE_MAX_FALLITI`, default 10 in 10 minuti → 429 per 15 minuti a quell'IP, anche col token giusto); nel log solo IP ed esito; memoria limitata a 1024 IP; usato in tutti e quattro i punti che controllavano il token.
  - C2 — tetto alle richieste a testo (`GAS_VOICE_MAX_TESTO_ORA`, default 120/ora): controllato prima del tetto voce (V12), contato solo se anche V12 lascia passare.
  - Avvio fail-closed: `GAS_VOICE_BIND` non locale (controllo con `ipaddress.is_loopback` o «localhost») → il server non parte senza `GAS_VOICE_RETE_PRIVATA=1`.
  - Proposta con opzioni e raccomandazione: `reports/proposta_voce_sicura.md`.
- Review #720-M2 e #722-M2 APPROVATO CON RISERVE (riserve di codice corrette: R-720-1, R-720-3, R-722-1), #723-M2 APPROVATO, #724-M2 APPROVATO (stesso contenuto riposizionato sopra la #356). Il commit 1c928ea ha lo stesso albero del commit revisionato 7e7f14b (`git diff 7e7f14b 1c928ea` vuoto).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++
 modules/voice/server.py            | 126 +++++++++++++++++++++++++++---
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/proposta_voce_sicura.md    |  50 ++++++++++++
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_voice_server.py    | 154 +++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main 69d76b9 (merge della #356).

## §3 GIT LOG --ONELINE (sessione)

```
1c928ea feat(voce): server voce più sicuro, fetta 1 — tetto ai tentativi con token sbagliato per IP, tetto alle richieste a testo, avvio rifiutato fuori da 127.0.0.1 senza rete privata; proposta R8 (decisione dell'operatore via M1)
9a1300d chore(revisore): memoria review #723 — APPROVATO
3a1596f chore(revisore): memoria review #722 — APPROVATO CON RISERVE
6a72415 chore(revisore): memoria review #720 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. La riga della memoria #724-M2 è dentro 1c928ea (scritta durante il cherry-pick, come da regola).

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #720-M2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #720-M2, fetta di sicurezza R8 fetta 1, diff staged nella worktree /home/user/Gas-sicura (branch feat/voce-sicura-locale, base b827447).

Letture obbligatorie fatte: CLAUDE.md §5, stato_progetto (righe R8), memoria della worktree.
- Wall of Shame: nessun taglio diretto della storia e nessuna simulazione degli strumenti.
- Test: `pytest tests/test_unit_voice_server.py` dà **150 passed**, `git diff --cached --check` è pulito, la worktree coincide con l'index.

**Elementi del diff esaminati**
- modules/voice/server.py:505 — `_autorizza`: legge l'IP solo da `client_address`. Nessun X-Forwarded-For né altri header, quindi niente bypass via header. L'IP bloccato riceve 429 prima del confronto del token. Stato tenuto come copie riassegnate sulla classe; nel log solo IP ed esito. — Rischi esaminati: bypass, stato condiviso, token nel log. — **ok**
- modules/voice/server.py:528 — tetto di 1024 IP su `bloccati` e su `falliti` (:534). La lista di un IP non supera la soglia, perché al blocco l'IP esce da `falliti`. Memoria quindi limitata. Però con le tabelle piene gli IP nuovi non vengono più contati né bloccati (fail-open). — **riserva R-720-4-M2**
- modules/voice/server.py:653 — tetto C2 sulle richieste a testo. Viene dopo i rifiuti locali (JSON non valido, «uso» → 400), che quindi non contano: corretto. Viene però DOPO il blocco V12 (:651), che ha già aggiunto un posto a `turni_parlati`. Sonda mia (GAS_VOICE_MAX_TESTO_ORA=1, testo con Accept audio/mpeg, chiave ElevenLabs finta): 3 richieste → 200/429/429, ma `turni_parlati` = 3. Il testo rifiutato da C2 consuma posti del tetto voce, cioè anche dell'ascolto H24. — **riserva R-720-1-M2**
- modules/voice/server.py:374 — `_bind_locale` accetta qualsiasi stringa che inizi con «127.», anche un nome host: `_bind_locale("127.evil.example")` dà True (provato), e quel nome può risolversi su un'interfaccia pubblica, aggirando il fail-closed di :1298. Serve un errore di configurazione dell'operatore. — **riserva R-720-3-M2**
- modules/voice/server.py:1298 — avvio rifiutato fuori da loopback senza GAS_VOICE_RETE_PRIVATA=1. Il messaggio a schermo non stampa il token (lo verifica il test). — **ok**
- modules/voice/server.py:1057 e modules/voice/server.py:554 — GET /voce/conferma, /voci/elenco, /voci/libreria e POST /voci/* passano tutti da `_autorizza`. I 404/405 restano senza autenticazione e non contano, come prima. — **ok**
- tests/test_unit_voice_server.py:2008, :2028, :2034 — coprono blocco e scadenza, assenza del token nel log, stato non condiviso con VoiceHandler, e nessun turno oltre il tetto del testo. Manca un test sull'ordine C2/V12. — **ok, con la lacuna della R-720-1-M2**

**Riserve**
- **R-720-1-M2 (BASSA)**: spostare il controllo C2 prima del blocco V12 (modules/voice/server.py:641-651). Basta riordinarli, più un test che controlli `turni_parlati` dopo un 429 di C2.
- **R-720-2-M2 (BASSA, decisione dell'operatore)**: tutti i client locali arrivano da 127.0.0.1, anche la pagina, perché clients/voice/browser_server.py fa da proxy. Un client con un token vecchio blocca per 15 minuti sia la pagina sia l'ascolto H24. Il blocco si rinnova a ogni scadenza finché quel client resta acceso: le richieste bloccate non contano, ma dopo la scadenza bastano altri 10 errori. L'ascolto manda richieste solo dopo la parola di attivazione, quindi è lento a raggiungere la soglia. Accettabile come scelta prudente, da dichiarare all'operatore. Sul tunnel invece gli IP sono per dispositivo.
- **R-720-3-M2 (BASSA)**: in `_bind_locale` usare `ipaddress.ip_address(bind).is_loopback` più il solo «localhost».
- **R-720-4-M2 (BASSA)**: fail-open con le tabelle piene. Irrilevante su loopback o tunnel; da dichiarare prima di un uso sul VPS.
- **R-720-5-M2 (COSMETICA)**: una riga di warning per ogni richiesta bloccata, senza limite: sotto attacco gas_debug.log cresce (il doctor ne controlla la dimensione). Un login riuscito non azzera il conto dei tentativi falliti: è una scelta esplicita, coperta dal test di :2028.

Nota, non introdotta da questo diff: `_bind_locale` accetta «::1», ma HTTPServer è solo IPv4, quindi con GAS_VOICE_BIND=::1 l'avvio fallisce con un'eccezione non gestita (comportamento che c'era già prima).

**Rischio esplicitamente escluso**: non ho provato il comportamento reale di Tailscale (IP di origine visto dal server, NAT) né il server avviato davvero fuori da loopback: non si riproduce in questo ambiente. Non ho rieseguito le altre suite della voce (prova_voci, tts, stt, voce_ascolto, telegram_voce): il diff tocca solo server.py, e il risultato di 664 passed è quello dichiarato dall'agente. Non ho rilanciato i suoi mutanti.

- Memoria aggiornata con la riga #720-M2 e una lezione: /home/user/Gas-sicura/.claude/agents/memoria_revisore.md. Committata solo lei nella worktree (commit 3bb6c6f); l'index del diff è intatto.
- Sonda: /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonda_r8.py

Review #722-M2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Ho controllato la review #722-M2, che è il seguito della #720-M2. Il lavoro è nella worktree /home/user/Gas-sicura (branch feat/voce-sicura-locale, base b827447) e ho esaminato lo staged.

**Elementi del diff esaminati**
- modules/voice/server.py:647 — il tetto al testo (C2) ora sta prima del blocco V12 (modules/voice/server.py:661-673). Rischio esaminato: un testo rifiutato da C2 non deve più consumare un posto del tetto voce. Esito: ok, R-720-1-M2 chiusa. Il nuovo test tests/test_unit_voice_server.py:2044 passa (200/429/429, turni_parlati = 1).
- modules/voice/server.py:375 — `_bind_locale` ora usa `ipaddress.ip_address(b).is_loopback` più il solo «localhost». Rischio esaminato: un nome host che comincia con «127.» non deve passare per locale, e i casi limite devono restare fail-closed. Esito: ok, R-720-3-M2 chiusa. I casi in tests/test_unit_voice_server.py:2075 coprono «127.evil.example» e la stringa vuota. «::ffff:127.0.0.1» (con Python 3.11) e «[::1]» con le parentesi danno False: il server rifiuta di partire, quindi chiude invece di aprire.
- modules/voice/server.py:76 — aggiunto l'import di `ipaddress`. Esito: ok.
- reports/proposta_voce_sicura.md — la sezione «Stato» dichiara i limiti R-720-2, R-720-4 e R-720-5. Esito: ok, la conferma spetta all'operatore.
- Esecuzione: tests/test_unit_voice_server.py dà 153 passed e `git diff --cached --check` è pulito.

**Riserva**
- R-722-1-M2 BASSA: è lo stesso problema di R-720-1-M2 nel verso opposto. In modules/voice/server.py:659 C2 conta la richiesta a testo prima che V12 decida. Così un testo che chiede la risposta in audio (Accept audio/mpeg), se V12 lo rifiuta, consuma comunque un posto del tetto testo. Sonda eseguita con GAS_VOICE_MAX_TURNI_ORA=1 e GAS_VOICE_MAX_TESTO_ORA=3: tre richieste a testo con audio e poi una solo a testo danno 200/429/429/429. Alla fine turni_testo = 3 ma è partito un solo turno, e la richiesta solo a testo viene rifiutata da C2 senza aver fatto lavoro. Correzione suggerita: tenere il controllo C2 dov'è, ma aggiungere l'istante a `turni_testo` solo dopo che anche V12 ha lasciato passare, e aggiungere un test con la sonda descritta. È da correggere o da dichiarare in stato_progetto.md.

**Cosa non ho verificato**
- Non ho rieseguito le altre suite della voce (prova_voci, tts, contesto, stt, telegram_voce): ho preso per buono il tuo 377 passed. Il diff tocca solo do_POST/do_GET e `_bind_locale` del server, quindi l'impatto su quelle suite è improbabile.
- Non ho provato il comportamento con un tunnel reale (Tailscale) né su VPS: non si può riprodurre in questo ambiente.

**Memoria**
Ho aggiunto in /home/user/Gas-sicura/.claude/agents/memoria_revisore.md la riga #722-M2 e una lezione: ogni tetto deve contare la richiesta solo dopo che tutti i controlli successivi sono passati. Le ho committate con lo script della memoria nella worktree (commit e4bc254). Lo staged del diff è intatto (3 file, 291+/9-).

Review #723-M2 (verdetto integrale):

## VERDETTO: APPROVATO

La riserva R-722-1-M2 è chiusa: un testo rifiutato dal tetto voce non consuma più un posto del tetto al testo. Non ho riserve nuove.

**Righe del diff che ho esaminato**
- `modules/voice/server.py:647` — il tetto al testo (C2) viene controllato prima di V12, ma qui si annota solo l'istante in `testo_ora` (`:663`), senza aggiungerlo a `turni_testo`. Il rifiuto (`:657`) ripulisce la lista senza aggiungere nulla. Rischio: che un rifiuto consumi un posto, o che resti dentro un istante vecchio. Esito: ok.
- `modules/voice/server.py:679` — l'istante entra in `turni_testo` solo dopo che anche V12 ha lasciato passare. Ho cercato altri `return` tra il controllo (`:656`) e il conteggio (`:680`): c'è solo il 429 di V12 (`:670-673`), ed è proprio il caso in cui non si deve contare. Il ramo `cervello == "uso"` (`:640`) esce prima del controllo e quindi non conta. Rischio: rifiuti che consumano il tetto, o turni partiti senza essere contati. Esito: ok.
- `tests/test_unit_voice_server.py:2065` — è la mia sonda di #722: tetto voce 1, tetto testo 3, tre testi con risposta a voce e uno solo a testo danno 200/429/429/200, con 2 posti usati nel tetto al testo. Rischio: un test che non distingua il vecchio ordine dal nuovo. Ti fidi del fatto che col codice di #722 fallisce (non l'ho rifatto io), ma i valori attesi corrispondono a quanto avevo misurato a mano in #722 (200/429/429/429, 3 posti usati). Esito: ok.
- Contesto: `modules/voice/server.py:1328` — il server è un `HTTPServer` senza thread, quindi lo spazio più largo tra controllo e conteggio non apre una corsa tra richieste concorrenti. Esito: ok.

**Prove**
- `pytest tests/test_unit_voice_server.py -k "tetto or testo"`: 14 passed.
- `git diff --cached --check`: pulito.
- La suite completa del file l'ho lanciata in background ed è andata oltre i 120 s del comando; non ne ho letto l'esito. Mi baso sui tuoi 378 passed.

**Cosa non ho verificato**
- Suite completa del file e suite voce intera: non le ho rifatte io.
- Comportamento con il server dietro un proxy o con più thread: oggi il server è a thread singolo, quindi non riproducibile.
- I turni partiti e finiti in errore 500 contano lo stesso nel tetto al testo. Lo ritengo corretto, perché il lavoro è partito.

**Memoria**: aggiunta la riga #723-M2 in `/home/user/Gas-sicura/.claude/agents/memoria_revisore.md` e committata con lo script nella worktree (commit 49bfebf). `/home/user/Gas` non l'ho toccato.

Review #724-M2 sul riposizionamento sopra la #356 (verdetto integrale):

## VERDETTO: APPROVATO

Il cherry-pick di 5c233ce sopra 0d34fe6 (#356) ha lo stesso contenuto del commit originale. L'unione automatica di server.py ha tenuto sia la cache della #356 sia le difese R8, e nessun test della #356 è andato perso.

Letture obbligatorie fatte: CLAUDE.md sezione 5, reports/stato_progetto.md (righe su R8 e #356, lette in modo mirato) e la coda di .claude/agents/memoria_revisore.md (lezioni #722 e #723 sull'ordine dei tetti, applicate qui sotto).

**Cosa ho controllato**
- **Stesso contenuto.** Ho messo a confronto le sole righe +/- di `git diff --cached` e di `git show 5c233ce`, tolte le intestazioni dei file: sono identiche. Cambia solo il contesto. Anche lo stat coincide: 3 file, 321 righe aggiunte e 9 tolte.
- **Test della #356 intatti.** `git diff 0d34fe6 -- tests/` dà solo 154 aggiunte e 0 righe tolte. Gli hunk sono due: l'import a riga 15 e l'accodamento dopo `test_sintesi_cache_ha_un_tetto`. L'ordine è prima la #356, poi R8, come hai detto.
- **Unione pulita.** Niente marcatori di conflitto in modules/voice/server.py né in tests/test_unit_voice_server.py, e nessuna modifica fuori dallo staging.
- **Test eseguiti da me.** `pytest tests/test_unit_voice_server.py` → 161 passed. Il tuo 276 (con sottofondo e telegram_voce) non l'ho rieseguito.

**Elementi del diff esaminati**
- `modules/voice/server.py:542` — `_autorizza`: tetto ai tentativi falliti per IP, 429 a un IP bloccato anche col token giusto, nel log solo IP ed esito. Rischio: che l'unione abbia lasciato una strada col controllo diretto del token. `_check_auth()` compare una sola volta, a :560 dentro `_autorizza`; le quattro chiamate (:592, :609, :1104, :1111) passano tutte da `_autorizza()`. Esito: ok.
- `modules/voice/server.py:685` — tetto alle richieste a testo (C2): controllato prima del tetto voce (V12, :694-702), contato solo dopo che anche V12 lascia passare (:709-710, `testo_ora`). Rischio: tornare indietro sulle riserve R-720-1 e R-722-1 (un rifiuto di un tetto che consuma l'altro). Ordine conservato: tra il controllo e il conteggio l'unico return è il 429 di V12, voluto. Esito: ok.
- `modules/voice/server.py:1345` — avvio rifiutato (fail-closed) se l'indirizzo d'ascolto non è locale e manca `GAS_VOICE_RETE_PRIVATA`; resta dopo il controllo del token (:1333) e prima dell'import di GasKernel. Rischio: blocco perso nell'unione. Presente e intatto. Esito: ok.
- `tests/test_unit_voice_server.py:2078` — inizio dei 153 test R8 accodati, subito dopo i test della cache della #356 (:2040-2076). Rischio: test persi o sovrascritti nella risoluzione del conflitto. Solo aggiunte. Esito: ok.

Contesto, file non toccati dal cherry-pick: la cache `sintesi()` della #356 è viva in `modules/voice/server.py:327` (tetto 32 voci, mai in cache un audio vuoto), insieme a `_finiti_jobs` (:589, :824-834).

**Cosa NON ho verificato**
- I test di sottofondo e telegram_voce e quelli col browser: non rieseguiti per tempo (la sola suite voice_server dura 4 minuti e mezzo).
- Il comportamento reale sul Mac con Tailscale: non riproducibile in questo ambiente.

**Memoria**
Riga `#724-M2 … APPROVATO …` accodata in /home/user/Gas-sicura/.claude/agents/memoria_revisore.md e messa in staging con `git add`, senza commit: entra col commit del cherry-pick, come chiesto. Nessuna lezione nuova.

Prossimo passo: `git cherry-pick --continue`. Per il gate serve prima `bash scripts/segna_review_ok.sh`, perché il diff in staging ora include anche la memoria.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: +1 classe `TestR8Limiti` (blocco e scadenza, token giusto bloccato, log senza token, stato non condiviso, tetto al testo, ordine dei due tetti nei due versi, soglie scritte male) e test `test_r8_*` (indirizzo locale, avvio rifiutato, avvio con rete privata dichiarata). R8: 24 passed. Comando: `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py tests/test_unit_telegram_voce.py -k "not conversazione_nel_browser"` → 276 passed, 15 deselected (sullo stesso albero, prima del riposizionamento). Mutanti uccisi: ramo del blocco, tetto al testo, fail-closed, stato condiviso, soglia mai raggiunta, ordine dei tetti. `gas.py` non toccato.

## §6 STATO CI

`gh` non autenticato nel cloud. I commit sono pushati insieme a questo report: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-720-2-M2 BASSA (decisione dell'operatore): un client locale con token vecchio blocca per 15 minuti tutti i client su 127.0.0.1.
- R-720-4-M2 BASSA: con 1024 IP già ricordati i nuovi non vengono più contati né bloccati (irrilevante su 127.0.0.1 o tunnel; da rivedere prima di un uso sul VPS).
- R-720-5-M2 COSMETICA: una riga di log per ogni richiesta bloccata.
- Ereditate dalla #356: bot V-1/V-2 su 84b88f8 (chiuse in locale, PR di velocità a seguire), ve #356 V-4, bot su 0d34fe6 V-1/V-2/V-3 (log dell'handoff, test del tetto della cache, numero dei test nel report).
- Non verificato: comportamento reale con un tunnel (Tailscale) e server avviato fuori da 127.0.0.1.
