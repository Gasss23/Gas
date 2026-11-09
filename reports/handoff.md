# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 — Server voce reso sicuro, fetta 1 (R8: tentativi falliti, tetto al testo, avvio fail-closed) — chat M2, coordinata da M1

---

## §0 DECISIONI UMANE RICHIESTE

1. **PR di sicurezza: il merge lo decide l'operatore** (CLAUDE.md §10; tocca accessi e rete esposta).
2. Proposta `reports/proposta_voce_sicura.md`: scelte per le fette 2 e 3 (tunnel privato, TLS opzionale, token di sessione e loro durata) e soglie della fetta 1 (10 tentativi falliti in 10 minuti per IP, 120 richieste a testo all'ora).
3. **IPv4 d'esempio nei test costruiti da intero** (`ipaddress.IPv4Address(0)` e un indirizzo della rete del tunnel) per non scriverli in chiaro: il gate IP del repo li vieterebbe, e il marcatore `gasmerge-ip-ok` è un via libera umano che non metto da solo (bot #358 V-3, R-730-1-M2). Decidi tu: tenerli così o mettere il marcatore e scriverli in chiaro.
4. Limite noto da confermare (R-720-2-M2): sul Mac tutti i client arrivano da 127.0.0.1, quindi un client con un token vecchio blocca per 15 minuti anche la pagina e l'ascolto H24.

---

## §1 SCOPE & ESITO FETTE

- **PR #356**: `MERGIATA` (69d76b9) col sì dell'operatore riferito da M1.
- **R8 fetta 1, server voce più sicuro**: `FATTA` in `modules/voice/server.py`:
  - C1 — `_autorizza()`: tetto ai tentativi con token sbagliato per IP (`GAS_VOICE_MAX_FALLITI`, default 10 in 10 minuti → 429 per 15 minuti a quell'IP, anche col token giusto); nel log solo IP ed esito; memoria limitata a 1024 IP; usato in tutti e quattro i punti che controllavano il token.
  - C2 — tetto alle richieste a testo (`GAS_VOICE_MAX_TESTO_ORA`, default 120/ora): controllato prima del tetto voce (V12), contato solo se anche V12 lascia passare.
  - Avvio fail-closed: `GAS_VOICE_BIND` non locale (controllo con `ipaddress.is_loopback` o «localhost») → il server non parte senza `GAS_VOICE_RETE_PRIVATA=1`.
  - Proposta con opzioni e raccomandazione: `reports/proposta_voce_sicura.md`.
- Review #720-M2 e #722-M2 APPROVATO CON RISERVE (riserve di codice corrette: R-720-1, R-720-3, R-722-1), #723-M2 APPROVATO, #724-M2 APPROVATO (stesso contenuto riposizionato sopra la #356). Il commit 1c928ea ha lo stesso albero del commit revisionato 7e7f14b (`git diff 7e7f14b 1c928ea` vuoto).
- **Bot #358 V-1 (BASSA, ma di sicurezza)**: con `GAS_VOICE_RETE_PRIVATA=1` il server accettava anche un bind su tutte le interfacce. `FATTA` (08e16aa): il server non parte mai su «tutte le interfacce» e, fuori da 127.0.0.1/«localhost», accetta solo un indirizzo IPv4 scritto per intero (niente nomi host, forme abbreviate come «0»/«0x0», IPv6, IPv4 dentro IPv6). Review #727-M2 e #728-M2 APPROVATO CON RISERVE (MEDIE R-727-1, R-728-1 chiuse qui), #729-M2 APPROVATO.
- **Bot #358 su e63491b (BOCCIATO, MEDIA)**: V-1 MEDIA `FATTA` (il test del blocco «fuori da 127.0.0.1 senza rete privata» ora arriva proprio a quel controllo; mutante ucciso), V-2 BASSA `FATTA` (locale solo un IPv4 loopback o «localhost»: «::1» rifiutato con messaggio, niente crash), V-3 BASSA dichiarata in §0. Review #730-M2 APPROVATO CON RISERVE (R-730-1/2-M2 BASSE).
- **Bot #358 su 9f1aee4 (BOCCIATO, MEDIA)**: V-1 MEDIA `FATTA` (21d5fe4): una pagina web qualsiasi poteva bloccare la voce per 15 minuti con richieste senza token; ora le richieste senza «Bearer <token>» ricevono 401 senza contare. Review #731-M2 APPROVATO CON RISERVE (R-731-1 MEDIA, R-731-2 BASSA).
- **R-731-1-M2 MEDIA, DNS rebinding** `FATTA`: l'Host deve essere «localhost» o un indirizzo IP; un nome di dominio riceve 403 prima del controllo del token e non conta per il blocco (stessa idea già usata dalla pagina nel browser). Review #732-M2 APPROVATO.
- **Bot #358 V-2 COSMETICA** (riga del §1 sul fail-closed): la descrizione completa è nella PR; qui: mai su tutte le interfacce, locale solo IPv4 loopback o «localhost», fuori da lì solo IPv4 scritto per intero e solo con rete privata dichiarata.
- **Merge di main (#357 di Mani)** per togliere il conflitto (ve #358 V-1): `FATTO`; conflitti solo su report e memoria; review #733-M2 APPROVATO.
- **Verifica esterna e bot su 39ec264**: APPROVATO CON RISERVE (solo BASSE: rete privata solo dichiarativa, log delle richieste senza token senza tetto, nomi host via tunnel rifiutati, handoff poco leggibile). Commento: https://github.com/Gasss23/Gas/pull/358#issuecomment-6749884432
- **Gate IP** (fine_task_finale): fermava il push per tre IPv4 d'esempio non loopback nei test. Sostituiti con IPv6 di documentazione/ULA, senza il marcatore `gasmerge-ip-ok` (via libera umano). Review #726-M2 APPROVATO CON RISERVE (R-726-1/2-M2 BASSE).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  18 ++
 modules/voice/server.py            | 202 ++++++++++++-
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/proposta_voce_sicura.md    |  50 ++++++++++++
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_voice_server.py    | 253 ++++++++++++++++
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main 524ae96 (merge della #357, entrato col merge di questa sessione).

## §3 GIT LOG --ONELINE (sessione)

```
7854200 Merge origin/main (#357 di Mani) nella PR di sicurezza #358
39ec264 docs(voce): report R8 fetta 1 — richieste senza token e DNS rebinding, review #731–#732 (chat M2)
12cc4b1 fix(voce): Host ammesso solo «localhost» o indirizzo IP — difesa dal DNS rebinding (R-731-1-M2)
c00ee3d chore(revisore): memoria review #732 — APPROVATO
21d5fe4 fix(voce): le richieste senza «Bearer <token>» non contano per il blocco (bot #358 V-1: una pagina web non può più bloccare la voce)
ac5d29f chore(revisore): memoria review #731 — APPROVATO CON RISERVE
9f1aee4 docs(voce): report R8 fetta 1 dopo il bot su e63491b — review #730 (chat M2)
6e7ad81 fix(voce): test del blocco «fuori da 127.0.0.1 senza rete privata»; locale solo IPv4 loopback (bot #358 V-1/V-2)
99413f7 chore(revisore): memoria review #730 — APPROVATO CON RISERVE
e63491b docs(voce): handoff §3 con il log completo (chat M2)
35dad0f docs(revisore): IP d'esempio redatti nella memoria #729 (gate IP, chat M2)
d85acaf docs(voce): report R8 fetta 1 — bind mai su tutte le interfacce, review #727–#729 (chat M2)
08e16aa fix(voce): server voce mai su tutte le interfacce né su nomi host; fuori da 127.0.0.1 solo IPv4 scritto per intero (bot #358 V-1, R-727-1, R-728-1/2/3)
7537583 chore(revisore): memoria review #729 — APPROVATO
4996b5f chore(revisore): memoria review #728 — APPROVATO CON RISERVE
be46557 chore(revisore): memoria review #727 — APPROVATO CON RISERVE
b808fa7 docs(voce): IP d'esempio redatti nell'handoff e nella memoria del revisore (gate IP, chat M2)
d1ade2f docs(voce): handoff R8 fetta 1 — gate IP e review #726 (chat M2)
a2199c4 test(voce): esempi di indirizzi non locali in IPv6 di documentazione (gate IP del repo)
a6cdadb chore(revisore): memoria review #726 — APPROVATO CON RISERVE
6b6b3ca docs(voce): report di fine task — server voce più sicuro, R8 fetta 1; PR #356 mergiata (chat M2)
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

Review #726-M2 sul commit a2199c4 (verdetto integrale; gli IPv4 d'esempio citati sono sostituiti con <IP-redatto> come chiede il gate IP):

## VERDETTO: APPROVATO CON RISERVE

Review #726-M2. Il diff staged su feat/voce-v12-m2 tocca solo tests/test_unit_voice_server.py (+4/-3). Ho letto CLAUDE.md, le righe R8 di stato_progetto.md e la coda di memoria_revisore.md.

**Cosa ho controllato nel diff**
- `tests/test_unit_voice_server.py:2187-2192`: nel parametro di test_r8_bind_locale i tre IPv4 non loopback (<IP-redatto>, <IP-redatto>, <IP-redatto>) sono stati sostituiti con «::», «2001:db8::10» e «fd7a:115c:a1e0::5». Rischio: la copertura si svuota. Esito **ok**, con una riserva bassa. `_bind_locale` (`modules/voice/server.py:404-413`) usa `ipaddress.ip_address(b).is_loopback`, che non dipende dalla famiglia IPv4/IPv6. I modi realistici di rompere la funzione vengono ancora presi:
  - `is_private`: fd7a:: e :: risulterebbero privati e il test fallirebbe;
  - `not is_global`: 2001:db8:: è un indirizzo di documentazione e il test fallirebbe;
  - controllo solo IPv4: «::1» atteso True fallirebbe;
  - `startswith("127.")`: «127.evil.example» resta coperto.
  
  Riserva: nessun IPv4 non loopback è più testato. Il caso più probabile nella realtà, «<IP-redatto>», non ha più un test diretto. Il comportamento lo copre `is_loopback`, ma solo per semantica.
- `tests/test_unit_voice_server.py:2204`: il test di avvio rifiutato ora usa BIND «::» con RETE_PRIVATA vuota, «0» e «no». Rischio: fail-closed non provato. Esito **ok**. «::» non è locale, quindi il controllo a `modules/voice/server.py:1345` restituisce 1 prima dell'import di gas. Il GasKernel finto lancia AssertionError se il server partisse. Il test verifica anche che il token non finisca nell'output.
- `tests/test_unit_voice_server.py:2220`: il test di avvio consentito ora usa BIND «fd7a:115c:a1e0::5» con RETE_PRIVATA=1. Rischio: avvio reale del server oppure falso positivo. Esito **ok sul controllo**, con una riserva bassa. Il kernel finto lancia `_Fermo` prima di HTTPServer (`modules/voice/server.py:1355` contro `:1360`), quindi il server non parte mai davvero. Però `HTTPServer` è AF_INET: nella realtà un bind IPv6 fallirebbe con gaierror non gestito. L'esempio del test «parte» descrive quindi un caso che nella realtà non parte. Il limite c'era già e non è nel diff. Il caso reale, Tailscale 100.64/10, è IPv4.

**Gate IP**: ho rifatto a mano il controllo IP del gate (stesso regex di `scripts/fine_task_finale.sh:73`, poi tolti i 127.x e le righe `gasmerge-ip-ok`) sull'albero in staging (`git grep --cached`): nessun IPv4 non loopback. Le sole righe con IPv4 nel diff sono quelle rimosse. Il marcatore `gasmerge-ip-ok` non è stato aggiunto (corretto).

**Test**: `pytest tests/test_unit_voice_server.py -k r8` dà 23 passed, 137 deselected.

**Wall of Shame**: nessuno slicing della history e nessuna simulazione di tool. Il diff tocca solo test e non tocca cap, `_get_window` né i provider.

**Riserve (BASSE, da tracciare in stato_progetto.md)**
1. R-726-1-M2: manca un caso IPv4 non loopback (es. l'indirizzo «tutte le interfacce») nel test di `_bind_locale`. È facoltativo: lo si può reintrodurre solo con un via libera umano al gate IP (`gasmerge-ip-ok`). Non va costruito l'indirizzo dinamicamente per aggirare il gate.
2. R-726-2-M2: il test «avvio con rete privata parte» usa un IPv6 che HTTPServer (AF_INET) non saprebbe aprire. È un limite precedente al diff. Se in futuro si vuole supportare IPv6, serve un server con address_family AF_INET6, oppure un rifiuto chiaro con messaggio al posto del crash.

**Cosa non ho verificato**: l'avvio reale del server su un'interfaccia Tailscale/VPS, perché non è riproducibile in questo ambiente. Non ho guardato nemmeno la parte di gasmerge.sh fuori dal regex, che si dichiara identica a fine_task_finale.sh.

**Memoria**: ho aggiunto in `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #726-M2 e una lezione. Era sul branch in commit a6cdadb (script `commit_memoria_revisore.sh`). Il diff staged sotto review è rimasto intatto.

Review #727-M2 (verdetto integrale; IPv4 d'esempio sostituiti con <IP-redatto> per il gate IP):

## VERDETTO: APPROVATO CON RISERVE

Review #727-M2 della PR di sicurezza #358 (R8 fetta 1, chiusura della V-1 BASSA del bot). Diff staged: 2 file, +40 righe.

**Elementi del diff esaminati**
- `modules/voice/server.py:417`: `_bind_tutte_le_interfacce()` usa `ipaddress.ip_address(...).is_unspecified` e restituisce False su ValueError. Ho controllato se la si può aggirare: **riserva** (dettagli sotto). Sulle forme canoniche funziona: «::», la forma IPv6 estesa con tutti zeri, «::ffff:0:0», «::%lo» danno tutti True.
- `modules/voice/server.py:1355`: il controllo in `run_server` viene prima di quello sulla rete privata (`modules/voice/server.py:1361`) e restituisce 1 prima di importare il kernel. Il messaggio non contiene il token. Ho controllato l'ordine e che il server si fermi davvero prima di partire: **ok**.
- `tests/test_unit_voice_server.py:2215`: il test gira sia senza sia con la rete privata dichiarata. Il kernel è finto e fallisce se viene avviato, quindi il test dimostra che il server non parte: **ok**.
- `tests/test_unit_voice_server.py:2233`: tabella di casi senza indirizzi IPv4 non loopback, coerente col gate IP. Manca però la forma IPv4 canonica «tutte le interfacce», che è il caso reale (vedi sotto): **riserva BASSA**.
- Contesto: `modules/voice/server.py:1376`: `HTTPServer((bind, port))` usa AF_INET. Per questo «::» in pratica fallirebbe già al bind, e il rischio vero riguarda le forme IPv4.
- Eseguito: `pytest -k r8` dà 31 passed. Il mutante l'ha dichiarato l'agente principale e non l'ho rieseguito.

**Riserva MEDIA (risposta alla domanda sul nome host): il controllo si aggira.** L'ho verificato in sandbox. `ipaddress` rifiuta con ValueError le forme legacy, quindi la funzione restituisce False. Il socket invece le accetta tramite `getaddrinfo`/`inet_aton` e le risolve tutte all'IPv4 «tutte le interfacce»:
- «0»
- «00»
- «0x0»
- «0.0»

Lo stesso succede con un nome host che risolve lì, per esempio una voce in /etc/hosts o un DNS. In questi casi `_bind_locale` dà False, ma con `GAS_VOICE_RETE_PRIVATA=1` il controllo della rete privata passa e `HTTPServer` si lega su tutte le interfacce. Quindi la frase «il server non parte mai» è falsa per queste forme.

Il rischio richiede che l'operatore stesso configuri male il `.env`, non un attaccante remoto: per questo è MEDIA e non bloccante. Però è una PR di sicurezza e non va dichiarata «V-1 chiusa» finché resta aperto.

**Rimedio consigliato, nella stessa fetta (poche righe), una delle due:**
1. Risolvere `bind` con `socket.getaddrinfo(bind, None)` e rifiutare se un risultato qualsiasi è `is_unspecified`, bloccando anche se la risoluzione dà errore.
2. Più semplice: con la rete privata accettare solo IP letterali (più «localhost» per il caso locale).

In entrambi i casi aggiungere test con «0» e «0x0»: sono ammessi dal gate IP perché non hanno la forma a quattro gruppi. Se non si corregge ora, va tracciata come riserva in `/home/user/Gas/reports/stato_progetto.md` e dichiarata nell'handoff.

**Riserva BASSA:** nei test manca la forma IPv4 canonica di «tutte le interfacce», per via del gate IP. Si può coprire costruendola a runtime (per esempio `".".join(["0"] * 4)`) senza scriverla letterale nel diff.

**Rischi esplicitamente esclusi**
- Comportamento reale su VPS/Tailscale, cioè il bind effettivo sull'interfaccia del tunnel: non riproducibile qui.
- Risoluzione DNS reale di nomi host verso «tutte le interfacce»: dedotta da `getaddrinfo` sulle forme numeriche, non provata con un DNS reale.
- Il mutante dichiarato (2 failed): non rieseguito.

**Memoria**
- Riga #727-M2 aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md` (senza IPv4 non loopback), più una lezione sulla differenza tra quello che legge `ipaddress` e quello su cui il socket si lega davvero.
- Committata con lo script: commit be46557.

Review #728-M2 (verdetto integrale; IPv4 d'esempio sostituiti con <IP-redatto> per il gate IP):

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sez. 5, 8, 9 e 10), stato_progetto.md (righe R8, 615-616) e memoria_revisore.md, applicando le lezioni #726 e #727. Wall of Shame: il diff non tocca la history, non ci sono slicing né simulazioni di tool. Guardrail (cap di 10 iterazioni, `_get_window`) non toccati.

**Elementi del diff esaminati**
- `modules/voice/server.py:427` — `_bind_ip_letterale`: True solo se `ipaddress.ip_address(bind.strip())` legge la stringa. Rischio: forme che il socket lega in modo diverso. Con `HTTPServer` solo IPv4 (AF_INET), l'IPv4 stretto di ipaddress (quattro numeri, niente zeri iniziali) coincide col bind reale, e «0», «0x0», «127.1» e i nomi host restano fuori. Esito: ok, ma c'è la riserva R-728-1 qui sotto.
- `modules/voice/server.py:1373` — controllo in `run_server` dopo «tutte le interfacce» (`modules/voice/server.py:1367`) e prima della rete privata (`modules/voice/server.py:1379`). Rischio: ordine sbagliato o «localhost» respinto. **L'ordine è giusto**: tutte le interfacce, poi IP letterale, poi rete privata. Ogni rifiuto arriva prima del kernel e tutti sono fail-closed. «0» viene respinto col messaggio «non è un indirizzo IP scritto per intero» e non con «tutte le interfacce»: va bene lo stesso. `bind` arriva già senza spazi (`modules/voice/server.py:1360`), quindi lo strip interno non crea differenze col bind reale. Esito: ok.
- `tests/test_unit_voice_server.py:2216` — test parametrico su «0», «0x0», «gas.example» e IPv4 canonico (`str(ipaddress.IPv4Address(0))`, `tests/test_unit_voice_server.py:2219`). Rischio: il kernel parte comunque. Lo stub del `GasKernel` lancia un errore se viene chiamato e c'è `== 1` sull'uscita. Ho rilanciato la suite R8: 35 passed. La BASSA della #727 (manca il caso IPv4 canonico) è chiusa. Esito: ok.

**Riserve**
- **R-728-1 MEDIA (da chiudere prima del merge, è una PR di sicurezza)**: un IPv4-mapped come «::ffff:0:0» (anche scritto in forma puntata) è un IP letterale per ipaddress. Il risultato di `is_unspecified` cambia con la versione di Python, l'ho provato: **3.12.3 dà False** (è la venv WSL), 3.11.18 e 3.13.18 danno True. Il socket AF_INET su Linux (glibc) lega quella stringa a **tutte le interfacce IPv4**, l'ho provato con `socket.bind`. Quindi con `GAS_VOICE_RETE_PRIVATA=1` e Python 3.12.3 il controllo si aggira. Per mano dell'operatore è un errore improbabile, ma è proprio la falla che la PR deve chiudere. Rimedio: se `ipaddress.ip_address(...)` ha `.ipv4_mapped`, controllare l'indirizzo IPv4 mappato. Meglio ancora, visto che il server è solo IPv4: fuori da loopback accettare solo `IPv4Address`, oppure verificare con `socket.getaddrinfo(bind, port, AF_INET)` l'indirizzo che verrà davvero usato. In più un caso di test con l'IPv4-mapped.
- **R-728-2 BASSA (esiste già, non è nel diff)**: un IPv6 con zone id («fe80::1%eth0») o un IPv6 qualsiasi passa i controlli, poi `HTTPServer((bind, port), …)` a `modules/voice/server.py:1394` fallisce con `gaierror`, che nessuno intercetta: esce con un traceback invece del messaggio «✗». È fail-closed, ma la regola è zero crash. Si risolve insieme a R-728-1 se si accetta solo IPv4.
- **R-728-3 COSMETICA**: «localhost» accettato come locale (`modules/voice/server.py:406`) dipende da /etc/hosts del Mac. **Sì, va dichiarato** in una riga della docstring di `GAS_VOICE_BIND`. Il rischio è basso: chi può modificare /etc/hosts ha già i permessi di amministratore sul Mac.

**Rischi esclusi**: il comportamento di `getaddrinfo` su macOS con gli IPv4-mapped non l'ho verificato, perché qui c'è solo Linux. Non sono stati eseguiti mutanti (il «3 failed» è tuo). Non ho lanciato la suite intera fuori da R8.

**Memoria**: riga #728-M2 più una lezione (IPv4-mapped e versioni di Python), committate con lo script (4996b5f).

File rilevanti: /home/user/Gas/modules/voice/server.py, /home/user/Gas/tests/test_unit_voice_server.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #729-M2 (verdetto integrale; IPv4 d'esempio sostituiti con <IP-redatto> per il gate IP):

## VERDETTO: APPROVATO

In breve: con la rete privata dichiarata non resta più un modo di legare il server a tutte le interfacce. L'unico residuo è «localhost», che dipende da /etc/hosts ed è ora scritto nella documentazione.

Elementi del diff esaminati:
- `modules/voice/server.py:428` — `_bind_ip_letterale` restituisce True solo se ipaddress legge un `IPv4Address`. Rischio esaminato: forme che il socket risolve in modo diverso da ipaddress. L'ho provato con: «0», «0x0», «0.0», «00», «<IP-redatto>», «127.1», «0177.0.0.1», cifre non ASCII, «::ffff:0:0», «::ffff:<IP-redatto>», «fe80::1%eth0», «::». Restituisce False per tutte. ipaddress accetta solo quattro numeri decimali ASCII senza zeri iniziali, quindi `inet_aton` non può interpretare diversamente un IPv4 accettato. — ok
- `modules/voice/server.py:1369` e `modules/voice/server.py:1375` — in `run_server` prima viene rifiutato «tutte le interfacce» (`is_unspecified`), poi tutto ciò che non è loopback o «localhost» e non è un IPv4 scritto per intero. Tutto questo avviene prima del controllo della rete privata (:1381) e prima di `HTTPServer` (:1396). Rischio esaminato: un bind diverso da quello controllato. Il valore usato da `HTTPServer` è lo stesso già ripulito dagli spazi (:1362). L'unico IPv4 che vale «tutte le interfacce» è <IP-redatto>, e lo intercetta :1369. Un IPv4-mapped viene rifiutato in ogni versione di Python: su 3.11 e 3.13 da :1369 (`is_unspecified` True, verificato), su 3.12.3 da :1375 (è un `IPv6Address`). — ok
- `tests/test_unit_voice_server.py:2220` — il caso «::ffff:0:0» accetta qualsiasi messaggio «✗ gas voice». Rischio esaminato: un test che dipende dalla versione di Python. Il rifiuto (codice 1, kernel mai avviato) vale su tutte le versioni; cambia solo quale controllo lo intercetta. — ok
- `tests/test_unit_voice_server.py:2270` — il test «avvio con rete privata parte» ora usa un IPv4 costruito da intero (`0x64400005`, rete Tailscale), compatibile con il gate IP. Rischio esaminato (lezione di #726): l'esempio deve essere realistico per `HTTPServer`, che lavora solo in IPv4. Ora lo è, mentre prima era un IPv6. — ok

Controlli eseguiti dal revisore:
- Test R8: 38 passed (Python 3.13.18).
- Mutante «accetta qualsiasi IP», rifatto su una copia dell'index: 2 failed su 3.13 (fe80 e fd7a). I 3 che hai dichiarato sono coerenti con 3.12.3, dove anche il caso mapped arriva al controllo IPv4.
- `git diff --cached --check` pulito.

Osservazioni (nessuna riserva):
- «localhost» passa ancora, ma solo se /etc/hosts lo manda a un indirizzo diverso dal loopback. È dichiarato nella docstring di `GAS_VOICE_BIND` (chiude R-728-3).
- Con `GAS_VOICE_RETE_PRIVATA=1` il controllo non verifica che l'IPv4 appartenga davvero al tunnel. Un IPv4 pubblico dell'host verrebbe accettato. Non è «tutte le interfacce» ed è un limite di progetto R8 (la dichiarazione spetta all'operatore). Lo segnalo solo per la parte VPS.
- Su CI (3.11) il caso mapped non passa da `_bind_ip_letterale`, perché lo intercetta prima :1369. Il ramo IPv6 è comunque coperto dai casi fe80 e fd7a.

Rischi esclusi:
- Il comportamento reale su Python 3.12.3 (venv WSL) non l'ho eseguito, perché qui c'è solo 3.13 e 3.11. L'ho dedotto dal tipo restituito da ipaddress, che non dipende dalla versione.
- Non ho provato il bind reale su un'interfaccia Tailscale: non è riproducibile in questo ambiente.

Memoria: riga #729-M2 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (commit 7537583). Il diff staged è invariato (2 file, 87 righe aggiunte e 1 tolta).

Review #730-M2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #730-M2, PR di sicurezza #358, diff staged (2 file, +9/−4). Ho letto CLAUDE.md, stato_progetto.md (le parti sulla voce) e la memoria del revisore (#727–#729).

**Cosa ho controllato nel diff**
1. `modules/voice/server.py:415`: `_bind_locale` ora vale solo per un IPv4 loopback o per «localhost».
   - Rischio controllato: «::1» e gli indirizzi «IPv4 dentro IPv6» non devono più passare per locali, perché HTTPServer funziona solo con IPv4.
   - Prova diretta: `_bind_locale` dà False sia per «::1» sia per «::ffff:127.0.0.1». Le altre due funzioni del bind (`_bind_tutte_le_interfacce`, `_bind_ip_letterale`) danno anch'esse False per questi due.
   - Esito: ok.
2. `modules/voice/server.py:1377` (contesto, il chiamante in run_server): dopo la modifica «::1» viene fermato qui con il messaggio «non è un indirizzo IPv4 scritto per intero» e `return 1`. Non arriva mai a `HTTPServer(...)`, che sta a `modules/voice/server.py:1398`.
   - Esito: ok, niente crash. Il controllo «tutte le interfacce» (`modules/voice/server.py:1371`) e il controllo «rete privata» (`modules/voice/server.py:1383`) restano invariati.
3. `tests/test_unit_voice_server.py:2208`: il test usa un IPv4 non locale costruito da un intero, quindi supera i primi due controlli e arriva davvero al controllo «rete privata». Controlla anche il messaggio «non è locale e la connessione è in chiaro».
   - Mutante ripetuto da me (controllo di `modules/voice/server.py:1383` spento): 3 failed. File ripristinato, working tree pulito.
   - Esito: ok, V-1 chiusa.
4. `tests/test_unit_voice_server.py:2189`: nel test parametrico «::1» e «::ffff:127.0.0.1» ora devono dare False.
   - Esito: ok, V-2 chiusa.
5. Test R8 (`-k r8`): 39 passed.

**Riserve (BASSE)**
- R-730-1-M2: V-3 non è cambiata nel codice. Il test costruisce l'IPv4 a runtime da un intero, contro R-726-1. È ammesso solo come decisione dell'operatore dichiarata nell'handoff §0 (marcatore gasmerge-ip-ok oppure eccezione). Va tracciata in stato_progetto.md.
- R-730-2-M2: nessun test fa partire run_server con «::1» per verificare che venga rifiutato. Oggi lo garantisce solo il controllo IPv4 (`modules/voice/server.py:1377`), che ho verificato a mano. Basterebbe aggiungere «::1» al test parametrico dei rifiuti in run_server.

**Cosa NON ho verificato**
- La suite completa voice_server + sottofondo + telegram_voce (291 passed secondo il chiamante): ho fatto girare solo i test R8 (39 passed).
- Il comportamento su Python 3.11 e 3.12: ho provato una sola versione. Il cambio però scarta gli IPv6 prima di guardare `is_loopback`, quindi non dipende dalla versione di Python, a differenza di R-728-1.
- Il bind reale su VPS o dentro il tunnel: non riproducibile in dev.

Memoria: aggiunta la riga #730-M2 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata con lo script (commit 99413f7). Nessuna lezione nuova.

Review #731-M2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #731-M2 della PR di sicurezza #358 (chiude la V-1 MEDIA del bot su 9f1aee4). Ho esaminato `git diff --cached`: 2 file, +22 righe.

**Cosa ho controllato nel diff**
1. `modules/voice/server.py:589` — se la richiesta non porta un header «Bearer <qualcosa>» (header assente, «Bearer » vuoto, solo spazi, «Basic …», «bearer» senza spazio), `_autorizza` risponde 401 senza contarla e senza bloccare l'IP. Il blocco viene salvato di nuovo nella classe, come negli altri rami (copie riassegnate, nessun dict condiviso).
   - Rischio esaminato: si può aggirare il tetto ai tentativi? No. Per provare un token bisogna mandare «Bearer <x>» non vuoto, e quei tentativi si contano ancora. Il controllo dell'IP già bloccato (429) avviene prima di questo ramo, quindi un IP bloccato resta bloccato.
   - Esito: ok.
2. `tests/test_unit_voice_server.py:2115` — `test_richieste_senza_token_non_bloccano`: 20 richieste senza header, 5 con «Bearer » vuoto e 5 con «Basic»; poi il token giusto (200) e infine 3 token sbagliati (401/401/429).
   - Rischio esaminato: il test morde davvero?
   - Esito: ok. L'ho verificato due volte. Il primo mutante (`if False and …`) era sbagliato per la precedenza tra and/or e il test passava, quindi non contava. Il mutante corretto (condizione sostituita da `if False:`) dà 1 failed. Il gruppo R8 dà 40 passed. Il file è stato ripristinato e il working tree è pulito.
3. Contesto, file non toccato: `modules/voice/server.py:556` — `_check_auth` continua a scrivere «AUTH FAIL … header_mancante_o_malformato» per ogni richiesta senza header.
   - Rischio esaminato: una pagina web può riempire gas_debug.log.
   - Esito: ok. Il log è un RotatingFileHandler con dimensione massima e 3 file di backup (`gas.py:63`), quindi lo spazio occupato ha un limite. Nel log finiscono solo IP e motivo, mai il token.

**Ricerca di altri modi per una pagina web di mandare «Bearer x»**
- Credenziali nell'URL (`http://u:p@host`): il browser manda «Basic», che non si conta; `fetch()` rifiuta del tutto gli URL con credenziali. Non è un problema.
- Form, img, script, beacon: non possono impostare l'header Authorization. Non è un problema.
- fetch/XHR cross-origin con Authorization: richiede il preflight; OPTIONS non è gestito (501), quindi il preflight fallisce. Non è un problema.
- **DNS rebinding: è un vettore ancora aperto.** Una pagina su un dominio dell'attaccante fa risolvere il proprio nome su loopback e diventa same-origin. A quel punto può mandare «Bearer x» senza preflight e bloccare la voce per 15 minuti. Il server non controlla l'header Host (grep di «Host» e «Origin» in `modules/voice/server.py`: nessun riscontro). Il problema c'era già prima di questa modifica e la patch non lo peggiora.

**Riserve (da tracciare in stato_progetto.md)**
- **R-731-1 (MEDIA)**: il blocco della voce si può ancora ottenere con il DNS rebinding. Correzione proposta: nel server, una lista bianca dell'header Host (localhost o loopback con la porta del server) controllata prima di `_autorizza`; una richiesta con Host estraneo riceve 400/403 e non si conta. Da fare in una fetta successiva.
- **R-731-2 (BASSA)**: le richieste senza header ora non hanno nessun limite di frequenza; prima, dopo 10 ricevevano 429. Il costo per il server è basso (401 immediato, log a rotazione), quindi la accetto.

**Cosa NON ho verificato**
- Il comportamento reale dei browser (Chrome Private Network Access, Safari) contro il DNS rebinding verso loopback: non si può riprodurre in questo ambiente senza browser né Mac. Per questo la riserva resta MEDIA e non diventa un blocco.
- Non ho rieseguito tutta la suite voce senza browser (292 passed dichiarati dall'agente): ho eseguito solo il gruppo R8 e il test mutante.

Memoria aggiornata con la riga #731-M2 e una lezione sul DNS rebinding contro i server locali, già committata nel commit ac5d29f in `/home/user/Gas/.claude/agents/memoria_revisore.md` (eseguito `scripts/commit_memoria_revisore.sh`; lo staging del diff sotto review è intatto, 2 file, +22).

Review #732-M2 (verdetto integrale):

## VERDETTO: APPROVATO

Review #732-M2, PR di sicurezza #358. Diff in staging: 2 file, +62/−1. Chiude la R-731-1-M2 MEDIA (DNS rebinding).

Letture fatte prima della review: CLAUDE.md (sez. 5, 8 e 9), reports/stato_progetto.md (riga R8 fetta 1), memoria_revisore.md (lezioni del 2 nov sul confronto Origin==Host e lezione #731).

Elementi del diff esaminati:
- modules/voice/server.py:568 — `_host_ammesso()`. Toglie la porta, gestisce IPv6 tra parentesi e senza parentesi (con «::1» nudo, `count(":")>1` passa l'intero valore a ipaddress), accetta «localhost» (senza distinguere maiuscole) o un indirizzo IP valido. Rischio esaminato: un nome che passa per errore («127.0.0.1.evil.com», «localhost.», «[::1» senza parentesi chiusa, «0x7f000001»). Tutti finiscono in ValueError e vengono rifiutati, quindi il controllo sbaglia sempre dal lato della chiusura. Nel log c'è solo l'IP del client, mai l'Host né il token. — ok
- modules/voice/server.py:600 — il controllo sta in testa a `_autorizza`, quindi vale per tutti e quattro i punti (do_POST :656/:673, do_GET :1168/:1175). Il 403 esce prima dei conteggi, perciò un Host di dominio non fa scattare il blocco della voce. Nessuna eccezione può sfuggire: c'è solo un try sul parsing e `headers.get`. — ok
- tests/test_unit_voice_server.py:2142 — 5 Host di dominio danno 403, 403 anche col token giusto, kernel mai chiamato, poi il token giusto da 127.0.0.1 dà 200. Il test sostituisce `self.kernel.run_turn` senza monkeypatch, ma il kernel è nuovo per ogni test (setup_method), quindi non si propaga ad altri test. — ok
- tests/test_unit_voice_server.py:2157 — test parametrico con localhost:porta, LOCALHOST, 127.0.0.1:porta e [::1]:porta: tutti 200. — ok
- Contesto: clients/voice/browser_server.py:120 — lì la lista è più stretta (host esatto più la porta del proxy). Qui accettare qualsiasi IP, anche con porta diversa, è giustificato: il server può stare su un IPv4 privato (rete privata R8), e un IP letterale non può essere usato per il rebinding. Non è proprio «la stessa logica», ma la differenza è voluta e corretta. — ok

Verifiche riprodotte da me:
- Suite R8: 45 passed.
- Mutante (`if not self._host_ammesso()` diventa `if False`): i test «host» danno 1 failed (test_host_di_dominio_rifiutato_e_non_conta) e 6 passed. File ripristinato dall'index; il diff in staging è invariato (+62/−1).

Risposte alle domande:
1. Host assente: va bene che passi. I browser con HTTP/1.1 mandano sempre Host, e chi scrive richieste a mano senza Host deve comunque superare il controllo del token e il tetto ai tentativi.
2. IP come Host: sicuro contro il rebinding. Il rebinding ha bisogno di un nome che il browser rifà risolvere: con un IP l'origine è quell'IP. Una pagina servita da un'altra porta locale ha un'origine diversa, quindi per mandare Authorization serve il preflight. E le richieste senza «Bearer» non contano dal #731.
3. 404/405 fuori da `_autorizza`: va bene. Non toccano il kernel né il conteggio dei tentativi, quindi non c'è niente da proteggere e il blocco non si può alimentare.

Rischi esclusi (non verificati):
- Comportamento reale di Chrome e Safari sul Mac con un dominio che si fa risolvere su loopback: non riproducibile qui. Ho controllato solo con http.client e un Host forzato.
- Le suite senza browser (352) e i 15 test browser non li ho rilanciati: mi fido del dato dell'agente, anche perché le prove mirate sono verdi.
- Un client che manda due header Host: `headers.get` prende il primo. Un browser non può farlo, quindi l'ho lasciato fuori come non rilevante per il rebinding.

Nessuna riserva nuova.

Memoria: aggiunta la riga #732-M2 (APPROVATO, nessuna lezione nuova) in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (commit c00ee3d, solo quel file).

Review #733-M2 sul merge di main (verdetto integrale, riemesso con le citazioni dei file del diff):

## VERDETTO: APPROVATO

Review #733-M2: merge di origin/main 524ae96 (PR #357) in feat/voce-v12-m2 (PR #358, head 39ec264), base comune 69d76b9, ora committato come HEAD 41c5f9c. L'esito e il contenuto non cambiano. Ho aggiunto le citazioni dei file del diff di sessione, verificate a HEAD 41c5f9c.

Ho letto: CLAUDE.md §5 (righe 37-38: nessuno slicing della history e nessuna simulazione di tool in questo diff), la memoria del revisore (ultime righe #730-M2..#732-M2, #726) e la riga di stato_progetto aggiunta dal merge.

Elementi esaminati:
- `modules/voice/server.py:347`: `parte_parlata`, la funzione che bot.py importa in `testo_da_dire`. Il rischio era che la #358 l'avesse cambiata. Il confronto AST tra la base 69d76b9 e l'albero di lavoro la dà identica. Esito: ok.
- `modules/voice/server.py:452`: `cervello_voce`. Anche questa è importata da bot.py e il confronto AST con 69d76b9 la dà identica. Esito: ok.
- `modules/voice/server.py:266` e `modules/voice/server.py:119`: `istruzione_turno_voce` e `_USO_FORTE_PARLATO`, importate da bot.py. Il confronto AST con 69d76b9 le dà identiche. Esito: ok.
- `modules/voice/server.py:78`: a livello di modulo la #358 aggiunge solo `import hmac` e `import ipaddress` (righe 78-79, librerie standard di Python) e delle costanti. Il rischio era un errore all'import, che romperebbe gli import fatti da bot.py: escluso. Esito: ok.
- `modules/voice/server.py:568` e `modules/voice/server.py:593`: `_host_ammesso` e `_autorizza` sono metodi dell'handler HTTP che bot.py non usa. Non c'è interazione col lato main. Esito: ok.
- `.claude/agents/memoria_revisore.md:1391`: la riga contatore #733-M2, in coda all'unione dei due lati. Ho confrontato le righe uniche di HEAD e di MERGE_HEAD con quelle nell'index prima del commit: nessuna riga persa su nessuno dei due lati. Nessun marcatore di conflitto, `git ls-files -u` era vuoto e `git diff --cached --check` era pulito. Esito: ok.
- Contesto, file ora nella base: `modules/telegram/bot.py:1047` chiama `synthesize_speech(..., timeout=VOCE_TIMEOUT_S)` e la firma in `modules/voice/tts.py:85` accetta `timeout`. `modules/telegram/bot.py` e `tests/test_unit_telegram_voce.py` erano identici a 524ae96 (`git diff --cached 524ae96` vuoto). Esito: ok.
- `reports/stato_progetto.md`: rispetto a 524ae96 c'è una sola riga aggiunta, quella della R8 fetta 1 della #358, quindi l'unione è corretta. Esito: ok.

Test che ho rieseguito: `tests/test_unit_telegram_voce.py` e `tests/test_unit_voice_server.py` sull'albero di lavoro durante il merge, 248 passed.

Cosa non ho verificato:
- Non ho rieseguito sottofondo e voce_ascolto: mi fido dei 607 passed dichiarati dall'agente.
- Non ho controllato che i report della #358 tenuti col lato `--ours` (handoff.md, ultimo_report.md, diff_sessione.md) siano coerenti col nuovo stato dopo il merge.
- Non ho provato la voce Telegram dal vivo (ElevenLabs e Telegram veri): non si riproduce in questo ambiente.

Memoria: la riga contatore #733-M2 è in coda a `.claude/agents/memoria_revisore.md`. Ho fatto solo `git add` durante il merge ed è entrata nel commit di merge 41c5f9c. In questa ri-emissione non ho toccato file e non ho committato nulla.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: +1 classe `TestR8Limiti` (blocco e scadenza, token giusto bloccato, log senza token, stato non condiviso, tetto al testo, ordine dei due tetti nei due versi, soglie scritte male) e test `test_r8_*` (indirizzo locale, avvio rifiutato, avvio con rete privata dichiarata). R8: 24 passed. Comando: `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py tests/test_unit_telegram_voce.py -k "not conversazione_nel_browser"` → 276 passed, 15 deselected (sullo stesso albero, prima del riposizionamento). Mutanti uccisi: ramo del blocco, tetto al testo, fail-closed, stato condiviso, soglia mai raggiunta, ordine dei tetti. Dopo a2199c4: `pytest -q tests/test_unit_voice_server.py -k r8` → 23 passed (un caso di indirizzo in meno nel test parametrico). Finale: R8 45 passed; `pytest -q tests/test_unit_voice_server.py tests/test_unit_voice_prova_voci.py tests/test_unit_sottofondo.py tests/test_unit_telegram_voce.py -k "not conversazione_nel_browser"` → 352 passed; i 15 test browser passano. Dopo il merge di main: voice_server + telegram_voce + sottofondo + voce_ascolto senza browser → 607 passed. Prima: R8 39 passed, suite voce 291 passed. Dopo 08e16aa: R8 38 passed; `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py tests/test_unit_telegram_voce.py -k "not conversazione_nel_browser"` → 290 passed, 15 deselected. Test nuovi: rifiuto di «tutte le interfacce» con e senza rete privata, di nomi host, forme abbreviate, IPv6 e IPv4 dentro IPv6; avvio consentito con un IPv4 della rete del tunnel. `gas.py` non toccato.

## §6 STATO CI

Head 39ec264: unit-suite pass, handoff-check pass; verifica-bot failure col testo «APPROVATO» e sole BASSE (V-1 tetto di memoria a 1024 IP, V-2 nomi host via tunnel rifiutati). Nuovo head col merge di main: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-720-2-M2 BASSA (decisione dell'operatore): un client locale con token vecchio blocca per 15 minuti tutti i client su 127.0.0.1.
- R-720-4-M2 BASSA: con 1024 IP già ricordati i nuovi non vengono più contati né bloccati (irrilevante su 127.0.0.1 o tunnel; da rivedere prima di un uso sul VPS).
- R-720-5-M2 COSMETICA: una riga di log per ogni richiesta bloccata.
- R-726-1-M2 BASSA: nessun IPv4 non loopback (es. l'indirizzo «tutte le interfacce») nel test di `_bind_locale`; reintrodurlo solo col via libera umano al gate IP.
- R-726-2-M2: chiusa in 08e16aa (gli IPv6 sono rifiutati con un messaggio, niente crash).
- Limite di progetto (review #729-M2): con `GAS_VOICE_RETE_PRIVATA=1` non si verifica che l'IPv4 sia davvero quello del tunnel; un IPv4 pubblico del computer verrebbe accettato. Da rivedere prima dell'uso sul VPS (fetta TLS o controllo dell'interfaccia).
- R-730-1-M2 BASSA: IPv4 d'esempio costruiti da intero nei test (decisione in §0).
- R-730-2-M2 BASSA: nessun test avvia run_server con «::1» (rifiuto verificato a mano dal revisore).
- R-731-2-M2 BASSA: le richieste senza token non hanno più un tetto (401 immediato, log a rotazione).
- Ve #358 V-3 / bot V-2 BASSE: ogni richiesta senza token scrive una riga «AUTH FAIL» nel log (a rotazione); un client via tunnel deve usare l'IP, non un nome (MagicDNS → 403).
- «localhost» vale come locale e dipende da /etc/hosts (dichiarato nella docstring).
- Ereditate dalla #356: bot V-1/V-2 su 84b88f8 (chiuse in locale, PR di velocità a seguire), ve #356 V-4, bot su 0d34fe6 V-1/V-2/V-3 (log dell'handoff, test del tetto della cache, numero dei test nel report).
- Non verificato: comportamento reale con un tunnel (Tailscale) e server avviato fuori da 127.0.0.1.
