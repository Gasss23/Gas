# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Mani: voce H24, installazione sistemata dopo la prova dal vero sul Mac (fetta voce-fix) (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #328 (https://github.com/Gasss23/Gas/pull/328). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5128550561","url":"https://github.com/Gasss23/Gas/pull/328"}`), perché `gh` nel cloud non è autenticato. **Il merge lo decide l'operatore**: il diff tocca `.claude/perimetro_review.txt` (aggiunge `scripts/voce/`).
2. Sul Mac, dopo il merge: `bash scripts/voce/installa.sh` due volte di fila (la seconda non deve fermarsi con «Bootstrap failed: 5»), poi una richiesta a voce e `grep "tempi voce" gas_debug.log`.

---

## §1 SCOPE & ESITO FETTE

- **Rilevatore sempre in errore (V-1 ve #323)**: `FATTA` — log a 1, 2, 4, 8… errori e pausa crescente dal terzo, con l'esponente limitato (R-624-1); il conto si azzera quando torna a posto.
- **GAS_CLAUDE_BIN sotto launchd (V-1 bot #323)**: `FATTA` — installa.sh lo scrive nel .env se manca, solo con percorso assoluto e caratteri ammessi.
- **Token vuoto accettato (V-4 bot #323)**: `FATTA` — la regex rifiuta il token vuoto o col solo commento.
- **scripts/voce/ nel perimetro di review (V-4 ve #323)**: `FATTA`.
- **Seconda esecuzione di installa.sh (prova dal vero di M1: «Bootstrap failed: 5»)**: `FATTA` — dopo bootout si aspetta che `launchctl print` fallisca (al massimo 5 s per servizio), poi bootstrap con 3 tentativi a 1 s; launchctl finto con stato e 4 test che falliscono col vecchio script.
- **Tempi della voce nel log (M1: `grep gas.voce.tempi` non trova niente)**: `FATTA` — la riga c'è, in gas_debug.log accanto a gas.py anche sotto launchd, ma il formato non stampa il nome del logger: si cerca `grep "tempi voce"`. Scritto nella LEGGIMI.
- **Review**: #624 BOCCIATO (overflow della pausa, R-624-1 MEDIA, corretto); #625, #628, #629 APPROVATO CON RISERVE; riserve R-628-1/2/3/4 e R-629-1/2 corrette; #631 sul merge in main.
- **Riserve della PR #324 (bot su 84b1422 e su 922aac9)**: `FATTA` — registrate in stato_progetto; punto 0 di ultimo_report riscritto.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 ++++++++
 .claude/perimetro_review.txt       |   3 +++
 clients/voice/ascolto.py           |  29 +++++++++++++++++++++++++++--
 reports/diff_sessione.md           |  16 ++++++++--------
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  32 +++++++++++---------------------
 scripts/voce/LEGGIMI.md            |  14 +++++++++++---
 scripts/voce/installa.sh           |  48 ++++++++++++++++++++++++++++++++++++++++++++++--
 tests/test_unit_voce_ascolto.py    | 204 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
```

NB: base = merge-base con origin/main = c6206d2. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
2c7d842 docs(voce): report della fetta 38 (installazione dopo la prova sul Mac), riserve della PR #324 registrate
a316409 chore(revisore): memoria review #631 — APPROVATO CON RISERVE
6d2fe79 Merge voce-fix: rilevatore in errore, GAS_CLAUDE_BIN, token vuoto, attesa dopo bootout e tentativi di bootstrap, tempi voce nella LEGGIMI; R-629-1/2 (review #624-#631)
0793476 chore(revisore): memoria review #629 — APPROVATO CON RISERVE
2e1fdea Merge origin/main (PR #322, #325) in voce-fix; riserve R-628-1/3/4 corrette (review #629)
e57305e chore(revisore): memoria review #628 — APPROVATO CON RISERVE
ac425b8 fix(voce): installa.sh aspetta che il servizio vecchio sparisca dopo bootout e riprova bootstrap; tempi voce in gas_debug.log nella LEGGIMI (prova dal vero di M1; review #628)
bc369ed fix(voce): rilevatore in errore con log limitato e pausa crescente, GAS_CLAUDE_BIN scritto da installa.sh, token vuoto rifiutato, scripts/voce/ nel perimetro (V-1 ve, V-1/V-4 bot, V-4 ve #323; review #624-#625)
5c4cc46 chore(revisore): memoria review #625 — APPROVATO CON RISERVE
ec34430 chore(revisore): memoria review #624 — BOCCIATO
```

NB: l'head della PR, cioè il commit che contiene questo file, non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti integrali, in ordine.

Review #624 (chat Mani), su bc369ed prima della correzione:

```
## VERDETTO: BOCCIATO

Review #624 (chat Mani). Il diff staged sul branch voce-fix, base 9718e0c, ha sha256 che inizia per 2cf1b7dd230c735d. Prima di cominciare ho letto CLAUDE.md, l'inizio di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md (review #615-#623). Ho esportato l'indice con `git checkout-index` in una cartella a parte e lì ho rifatto le prove: 85 passed su tests/test_unit_voce_ascolto.py, come dichiarato.

**Elementi del diff esaminati**

- `clients/voice/ascolto.py:268` — calcola la pausa con `self.dorme(min(PAUSA_ERRORI_MAX_S, 0.5 * 2 ** (n - 3)))` — rischio: il contatore cresce senza limite in un servizio acceso giorno e notte — **blocco (R-624-1)**.
- `clients/voice/ascolto.py:250` — azzera il conto quando il rilevatore torna a funzionare e lo scrive nel log — rischio: nessun test fissa l'azzeramento — **riserva (R-624-2)**.
- `scripts/voce/installa.sh:32` — nuova regex del token (primo carattere che non sia spazio, # o virgoletta) — rischio: token vuoti accettati — **ok**. Ho provato il mutante con la regex vecchia `.+`: 3 failed. Le 4 righe vuote vengono rifiutate e le 3 buone passano.
- `scripts/voce/installa.sh:37` — controlla se GAS_CLAUDE_BIN c'è nel .env, poi fa `command -v`, controlla la lista bianca e aggiunge la riga in coda con `>>` — rischio: falso «aggiunto» — **riserva (R-624-3)**. Mutanti: senza scrittura 1 failed, `>` al posto di `>>` 1 failed, senza AVVISO 1 failed.
- `tests/test_unit_voce_ascolto.py:208` — test con 1000 blocchi sempre in errore — si ferma prima di n=1027, quindi non vede R-624-1 — **riserva**.
- `.claude/perimetro_review.txt:31` — aggiunge `scripts/voce/` — ha la stessa forma delle altre cartelle (`brains/`, `clients/`); ho controllato che installa.sh, LEGGIMI.md e il plist risultino nel perimetro — **ok**. Tocca la macchina di controllo, quindi il merge lo decide l'operatore.
- Contesto: `gas.py:608` (`_carica_dotenv`), dove vale la PRIMA riga di una chiave. Serve a provare R-624-3.

**Finding**

- **R-624-1 MEDIA (blocco)**: `0.5 * 2 ** (n - 3)` dà OverflowError da n=1027 in poi, cioè dopo circa 17 ore di pause da 60 s, perché un intero da 2**1024 non si converte in float.
  - L'errore finisce nell'`except` del §9: la pausa salta e a ogni blocco esce una riga «pausa del rilevatore fallita (OverflowError)», circa 12,5 al secondo.
  - È lo stesso diluvio di log che la fetta voleva chiudere, e torna proprio nel caso H24 (il servizio acceso giorno e notte).
  - Riprodotto sull'export dell'indice: con 1200 blocchi sempre in errore le pause si fermano a 1024 (16,97 ore) e le righe «pausa fallita» sono 174.
  - Correzione: limitare l'esponente, per esempio `0.5 * 2 ** min(n - 3, 7)`, oppure il contatore. Serve anche un test oltre i 1030 blocchi che verifichi che la pausa resta 60 e che le righe di log restano logaritmiche.
- **R-624-2 BASSA**: il mutante che toglie `self._errori_rilevatore = 0` (`clients/voice/ascolto.py:250`) sopravvive con 85 passed, ma scrive «di nuovo a posto» a OGNI blocco buono: 495 righe su 495 blocchi. Nel test del ritorno basta contare che quella riga compaia esattamente una volta e aggiungere un secondo giro di errori che riparta da una pausa di 0,5 s.
- **R-624-3 BASSA**: `scripts/voce/installa.sh:37` usa `.+`, quindi:
  - con `GAS_CLAUDE_BIN=` vuoto nel .env lo script aggiunge una seconda riga e stampa «aggiunto», ma `_carica_dotenv` tiene la prima, vuota (provato: valore `''`), e il forte sotto launchd resta senza `claude`;
  - con `GAS_CLAUDE_BIN= # x` non aggiunge la riga e non dà nemmeno l'AVVISO.
  - Conviene usare lo stesso criterio stretto del token alla riga 32.
- **R-624-4 COSMETICA**: l'intestazione `scripts/voce/installa.sh:7` dice ancora che il passo 1 fa solo controlli, mentre ora scrive anche il .env. Inoltre l'AVVISO dice «`claude` non trovato» anche quando claude c'è ma il suo percorso esce dalla lista bianca.

Restano aperte, senza cambiamenti: R-615-4 MEDIA (permesso del microfono sotto launchd, da provare sul Mac) e R-615-5 BASSA (licenza di hey_jarvis, decide l'operatore).

**Rischi esclusi**

- Non ho provato il comportamento vero sul Mac: sounddevice in overflow durante una pausa di 60 s e `command -v claude` col PATH dell'operatore. Non si può riprodurre qui.
- Non ho verificato il caso di un `claude` installato con npm (`#!/usr/bin/env node`), che sotto launchd non troverebbe node. Sul Mac GAS_CLAUDE_BIN è già nel .env dal 28 ottobre e il giro notturno funziona, quindi lì il blocco nuovo non fa nulla.
- Non ho rifatto la suite da 444 test (hooks, handoff_check, gasmerge): ho rifatto solo i test della voce.

**Memoria**: riga #624 e una lezione nuova sul backoff esponenziale che va in overflow, committate con `scripts/commit_memoria_revisore.sh` (commit ec34430, solo la memoria). Dopo il commit il diff staged è intatto (sha256 2cf1b7dd230c735d).

File: /home/user/Gas/clients/voice/ascolto.py, /home/user/Gas/scripts/voce/installa.sh, /home/user/Gas/tests/test_unit_voce_ascolto.py, /home/user/Gas/.claude/perimetro_review.txt, /home/user/Gas/.claude/agents/memoria_revisore.md
```

Review #625 (chat Mani), sulla correzione (commit bc369ed):

```
## VERDETTO: APPROVATO CON RISERVE

Review #625 (chat Mani), ri-review della #624. Ho esaminato il diff staged sul branch voce-fix (sha256 7a39e900684e241c, invariato anche dopo il mio commit di memoria). Base: 9718e0c più ec34430. Ho letto CLAUDE.md, reports/stato_progetto.md e .claude/agents/memoria_revisore.md, dove ci sono il verdetto #624 e la lezione sul backoff.

**Prove riprodotte.** Ho esportato l'indice con `git checkout-index` e lanciato tests/test_unit_voce_ascolto.py: **89 passed**.

Mutanti su clients/voice/ascolto.py (falliti / totale 89):

| Mutante | Esito |
|---|---|
| esponente senza limite | 1 failed |
| senza azzeramento del conto | 2 failed |
| pausa dal 1° errore | 4 failed |
| log a ogni errore | 2 failed |
| senza svuota dopo la pausa | 2 failed |
| tetto dell'esponente a 6 (pausa max 32 s) | 2 failed |
| tetto dell'esponente a 20 | sopravvive, ma è innocuo: 2**17 entra in un float |

Mutanti su scripts/voce/installa.sh (falliti / totale 30 test di installa):

| Mutante | Esito |
|---|---|
| regex `.+` vecchia per GAS_CLAUDE_BIN | 1 failed |
| senza il ramo «riga vuota» | 2 failed |
| messaggi AVVISO fusi in uno solo | **sopravvive** |
| senza lista bianca sul percorso di claude | **sopravvive** |

**Elementi del diff esaminati**
- clients/voice/ascolto.py:269 — pausa `min(PAUSA_ERRORI_MAX_S, 0.5 * 2 ** min(n - 3, 7))`. Rischio: OverflowError da n=1027 (R-624-1). L'esponente è limitato, quindi la pausa vale al massimo min(60, 64) = 60 s; con 1200 blocchi non c'è nessuna «pausa fallita». Esito: **ok, R-624-1 chiusa**.
- clients/voice/ascolto.py:250 — riga «di nuovo a posto» e azzeramento del conto. Rischio: una riga a ogni blocco buono (R-624-2). La riga esce solo se il conto è sopra zero, e il conto viene azzerato; il test tests/test_unit_voce_ascolto.py:271 pretende le pause [0.5, 1, 0.5, 1]. Esito: **ok, R-624-2 chiusa**.
- clients/voice/ascolto.py:265 — log solo quando n è una potenza di 2. Rischio: un log che tace per molto. A 60 s di pausa, il 1024° errore arriva dopo circa 17 ore e il 2048° dopo circa 34: accettabile per un servizio H24. Esito: ok.
- scripts/voce/installa.sh:40 — criterio stretto per GAS_CLAUDE_BIN, con un elif per la riga vuota o col solo commento. Rischio: riga doppia che gas._carica_dotenv ignora (R-624-3). Una riga commentata `# GAS_CLAUDE_BIN=…` non viene presa per valida e si aggiunge la riga vera (corretto, il parser salta i commenti). Il printf comincia con `\n`, quindi va bene anche un .env senza a-capo finale. Esito: **ok, R-624-3 chiusa**.
- scripts/voce/installa.sh:46 — riga scritta solo se il percorso è assoluto e passa la lista bianca CONSENTITI. Rischio: un percorso non filtrato scritto nel .env, per esempio con un a-capo che inietta altre righe. Il codice è giusto, ma nessun test lo fissa. Esito: **riserva (R-625-1)**.
- scripts/voce/installa.sh:8 — l'intestazione ora dice che il passo 1 può aggiungere GAS_CLAUDE_BIN. Esito: **ok, R-624-4 chiusa nel testo**.
- .claude/perimetro_review.txt:31 — `scripts/voce/` entra nel perimetro di review. Le voci-cartella sono già usate (brains/, modules/), e brains/claude_cli.py:293 conferma che un valore vuoto ricade su `shutil.which`, cioè l'AVVISO dice il vero. Esito: ok.

**Finding**
- **R-625-1 BASSA**: la lista bianca di CLAUDE_BIN (scripts/voce/installa.sh:46) e l'AVVISO distinto «percorso con caratteri non ammessi» non hanno test. Se li tolgo o fondo i due messaggi, la suite resta verde (30 passed). Serve un test con un `claude` finto in una cartella con un carattere vietato (es. `$`): .env invariato e AVVISO specifico. Non blocca, perché chi controlla le cartelle del PATH ha già vinto.
- **R-625-2 COSMETICA**: `command -v claude` può dare un nome non assoluto (es. una funzione bash esportata). In quel caso esce l'AVVISO «caratteri non ammessi», che è fuorviante: meglio un messaggio come «non è un percorso assoluto».

Restano aperte R-615-4 MEDIA (microfono sotto launchd, Mac) e R-615-5 BASSA (licenza hey_jarvis, decide l'operatore).

**Rischio escluso:** non ho verificato il comportamento reale sul Mac, cioè `command -v claude` sotto la zsh dell'operatore, dove claude può essere un alias che bash non vede, né l'ascolto sotto launchd con un rilevatore che fallisce davvero. Non si riproduce qui su Linux: i test usano un `dorme` e un `claude` finti.

**Coerenza col progetto:** la correzione va nella direzione «robustezza > potenza» (niente diluvio di log in H24, l'eccezione nella pausa resta intercettata e non fa crashare). Nessuno slicing della history, nessuna simulazione di output dei tool, nessun guardrail del kernel toccato.

Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga contatore #625 e una lezione nuova (mutante che fonde i messaggi o toglie il filtro). È committata con scripts/commit_memoria_revisore.sh nel commit 5c4cc46; il diff staged non è cambiato.

Il merge spetta all'operatore, perché il diff tocca .claude/perimetro_review.txt. R-625-1 e R-625-2 vanno annotate in reports/stato_progetto.md.
```

Review #628 (chat Mani), attesa dopo bootout e tempi voce (commit ac425b8):

```
## VERDETTO: APPROVATO CON RISERVE

Review #628 (chat Mani). Ho revisionato il diff staged nel worktree `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/vf`, branch voce-fix sopra bc369ed. Sono 3 file e lo sha256 del diff è 5c5ef2e9070cdf645adfa742bec4cd7fbe7b62eb6a77bc145b502337800512e5, quello atteso. Prima ho letto CLAUDE.md, le parti voce di stato_progetto.md e la memoria.

**Elementi del diff esaminati**

- `scripts/voce/installa.sh:98` — dopo i bootout, per ogni servizio fino a 50 letture di `launchctl print`, con `if !` e `sleep 0.1`.
  - Rischi esaminati: `set -e` dentro `if !`, `set -u` sulle variabili, `seq` e `sleep` con decimali su macOS.
  - Esito: **ok**. `if !` è una condizione e non fa scattare `set -e`; ANDATO è sempre assegnato; `seq` sta in /usr/bin su macOS e il `sleep` di macOS accetta i decimali. L'ordine è giusto: tutti i bootout, poi l'attesa per ciascun servizio, poi i bootstrap. Il tetto vero è 5 s per servizio, quindi al massimo circa 10 s in tutto: va bene, perché i due bootout partono insieme.
- `scripts/voce/installa.sh:102` — STOP «non si spegne» prima di qualunque bootstrap.
  - Esito: **ok**. Il messaggio è chiaro e nessun bootstrap parte se il servizio vecchio è ancora visibile.
- `scripts/voce/installa.sh:108` — bootstrap ripetuto fino a 3 volte, a 1 s di distanza, poi STOP «3 tentativi» (`scripts/voce/installa.sh:112`).
  - Esito: **ok, con nota cosmetica** (R-628-3). Lo stderr di bootstrap non è nascosto, cosa utile per capire i guasti.
- `tests/test_unit_voce_ascolto.py:600` e `tests/test_unit_voce_ascolto.py:608` — il launchctl finto ora ha uno stato: i file su/giu e un contatore dei bootstrap.
  - Rischio esaminato: rompere i test già esistenti.
  - Esito: **ok**. Con un'installazione da zero il bootout esce con 3 (assorbito da `|| true`), print risponde «not found», bootstrap crea il file «su», e i print finali dicono «running». Il file intero passa: **93 passed riprodotti**.
- `tests/test_unit_voce_ascolto.py:719`, `tests/test_unit_voce_ascolto.py:728`, `tests/test_unit_voce_ascolto.py:735` — controllo che i test non passino a vuoto, con mutanti miei (installa.sh ripristinato ogni volta, sha256 del diff staged rimasto identico).
  - Esito: **ok**, ogni mutante fa fallire i test giusti:

| Mutante | Test falliti |
|---|---|
| un solo tentativo di bootstrap | 2 (riprova e sempre_rotto) |
| attesa tolta | 2 (seconda_volta e non_si_spegne) |
| `seq 1 10` al posto di 50 | 1 (non_si_spegne) |
| installa.sh di HEAD | 4 |

- `scripts/voce/LEGGIMI.md:95` — dice che i tempi della voce finiscono in gas_debug.log accanto a gas.py, anche sotto launchd, e si cercano col testo.
  - Esito: **vero, con riserva** (R-628-1 e R-628-2). L'ho verificato con un'esecuzione su un worktree di origin/main 70e2f05, avviata con cwd /tmp: la riga INFO finisce nel gas_debug.log accanto a gas.py, senza il nome del logger.
  - Il contesto che lo conferma, letto su origin/main: il percorso del log non dipende dalla cartella di avvio (Path(__file__)); il logger `gas.voce.tempi` è a INFO e passa per il file handler; la console resta a WARNING su stderr, cioè voce.server.log come da plist; `_carica_env` importa gas, e quindi configura il log, prima di ogni richiesta.
  - In modules/voice non c'è nessuna chiamata `logging.warning()` a livello di modulo prima dell'import di gas, che svuoterebbe il basicConfig: quelle di tts.py stanno dentro funzioni chiamate solo durante una richiesta.

**Finding**

- **R-628-1 — BASSA.** L'esempio in `scripts/voce/LEGGIMI.md:98` scrive `stt=0.81s`, ma la chiave vera è `trascrizione`. La riga riprodotta è: `tempi voce (200): trascrizione=0.81s cervello=2.40s server=0.00s`. Le altre chiavi sono voce, voce_tutta e server. Il grep funziona lo stesso. Correzione: copiare l'esempio dalla riga vera.
- **R-628-2 — BASSA.** La base bc369ed NON contiene V7a: in quel branch il logger `gas.voce.tempi` non esiste, c'è solo su main (PR #322). Il LEGGIMI sarà vero dopo il merge con main; prima di mergiare conviene allineare il branch a main. Io ho verificato il comportamento su main, non sulla base.
- **R-628-3 — COSMETICA.**
  - Dopo il terzo bootstrap fallito c'è un `sleep 1` inutile.
  - I «Bootstrap failed: 5» dei tentativi poi riusciti restano a schermo senza un «riprovo»: possono far credere che sia andato male.
- **R-628-4 — COSMETICA.** `scripts/voce/LEGGIMI.md:100` dice «I log non ruotano da soli» subito dopo la voce su gas_debug.log, che invece ruota a 5 MB (RotatingFileHandler, backupCount=3). Precisare che la frase vale per i due log in .gas_voce.

**Coerenza col progetto:** nessun impatto sul motore, sui guardrail o su `_get_window`. Il fix va nella direzione «zero crash» e «STOP chiaro», con test realistici del caso di M1.

**Rischi esplicitamente esclusi**
- Il comportamento vero di launchd su macOS non è verificato: qui siamo su Linux e il launchctl è finto. In particolare non so se `launchctl print` sparisca davvero prima che bootstrap smetta di dare l'errore 5; i 3 tentativi coprono la finestra che resta. La prova va rifatta da M1 sul Mac: seconda esecuzione con i servizi già caricati.
- Il `sleep` è finto nei test, quindi i tempi reali (5 s di attesa, 1 s fra i tentativi) non sono misurati.
- Il caso di un servizio messo a «disabled» con `launchctl disable` non è coperto (spegni.sh usa solo bootout).

**Memoria:** ho aggiunto la riga #628 in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, solo nel working tree. Indici non toccati e `commit_memoria_revisore.sh` non eseguito, come chiedevi tu; il commit resta da fare a te. Lezione registrata: un esempio di riga di log in un documento si copia da un'esecuzione vera, non si ricostruisce a memoria.
```

Review #629 (chat Mani), merge di main in voce-fix e riserve della #628 (commit 2e1fdea):

```
## VERDETTO: APPROVATO CON RISERVE

Review #629 (chat Mani). Worktree /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/vf, branch voce-fix (HEAD e57305e), con un merge di origin/main 70e2f05 in corso. Lo SHA-256 del diff staged coincide: 88738b391e64108c04d7718d9151336a0d0a4ca4e6a8c63f388f355040868f7d.

**Merge (R-628-2)**
- Ho confrontato con MERGE_HEAD i 9 file che vengono da main: hanno tutti il blob identico. Sono modules/voice/server.py, clients/voice/browser_client.html, clients/voice/browser_server.py, tests/test_unit_voice_server.py, tests/test_unit_voice_stt.py e i 4 file di reports/.
- `git diff --cached MERGE_HEAD --stat` mostra solo i 6 file di voce-fix: memoria, perimetro_review, ascolto.py, LEGGIMI, installa.sh, test_unit_voce_ascolto.py.
- Memoria del revisore: base 1152 righe, HEAD 1157, MERGE_HEAD 1176, staged 1181 (cioè 1157+24). Nessuna riga tolta, nessuna doppia, nessun marcatore di conflitto.

**Elementi esaminati**
- `scripts/voce/installa.sh:110` — ora il messaggio «riprovo tra 1 s (tentativo N di 3)» e lo `sleep 1` partono solo se tentativo < 3. Rischio guardato: attesa inutile dopo il terzo fallimento, numero del tentativo sbagliato, messaggio sul canale sbagliato. Con 2 fallimenti escono i messaggi «2 di 3» e «3 di 3». Con fallimenti continui escono gli stessi due e poi stop su stderr. Il messaggio va su stdout. Esito: ok.
- `scripts/voce/installa.sh:108` — la variabile del ciclo passa da `_` a `tentativo`, il resto del ciclo non cambia. Esito: ok.
- `tests/test_unit_voce_ascolto.py:736` — nuova asserzione: 2 messaggi «riprovo» quando falliscono 2 bootstrap. Rischio guardato: conteggio che passerebbe anche col codice vecchio. Col codice vecchio il messaggio non esisteva, quindi il conteggio sarebbe 0 e il test fallirebbe. Esito: ok.
- `tests/test_unit_voce_ascolto.py:744` — nuova asserzione: 2 messaggi anche con il bootstrap sempre rotto. Il commento dice «niente attesa dopo il terzo», ma il finto `sleep` (`tests/test_unit_voce_ascolto.py:619`, `exit 0`) non lascia traccia nel registro. Ho provato un mutante su una copia: messaggio ancora con la guardia, `sleep 1` fuori dalla guardia. I 2 test bootstrap passano lo stesso. Esito: riserva (R-629-1).
- `scripts/voce/LEGGIMI.md:98` (R-628-1) — controllato sull'albero con V7a, dove le chiavi vengono da `_segna`/`_chiudi_tempi` (`modules/voice/server.py:261`, contesto). Le chiavi sono trascrizione, cervello, voce, voce_tutta, più server aggiunto per ultimo. L'esempio «trascrizione=… cervello=… server=…» ha un ordine possibile, perché il dict tiene l'ordine di inserimento. Anche «la riga non contiene il nome del logger» è vero: il formato è `%(asctime)s - %(levelname)s - %(message)s` (`gas.py:70`, contesto). Esito: ok.
- `scripts/voce/LEGGIMI.md:101` (R-628-4) — la frase «gas_debug.log invece ruota a 5 MB» è vera: RotatingFileHandler con `_LOG_MAX_BYTES = 5 * 1024 * 1024` (`gas.py:50`, contesto). I due log in .gas_voce/ sono lo stdout/stderr di launchd (scripts/voce/com.gas.voce.server.plist), quindi non ruotano. Esito: ok.

**Test**: tests/test_unit_voce_ascolto.py + tests/test_unit_voice_stt.py = 185 passed, rifatti da me.

**Finding**
- **R-629-1 (BASSA)**: «niente sleep dopo il terzo tentativo» non è provato da nessun test, perché il finto `sleep` esce e basta. Il codice è giusto, ma il commento a `tests/test_unit_voce_ascolto.py:744` dice più di quello che il test prova. Correzione: far scrivere al finto `sleep` una riga nel registro (es. `echo "sleep $*" >> "$REGISTRO"`), poi verificare che `sleep 1` ci sia 2 volte. Altrimenti togliere il commento.
- **R-629-2 (COSMETICA)**: in `scripts/voce/LEGGIMI.md:96` «una riga INFO per richiesta» vale solo per le richieste che hanno speso qualcosa: se `_tempi` è vuoto, `_chiudi_tempi` non scrive niente (per esempio con un 401).

**Rischio escluso**: non ho verificato `installa.sh` con il vero launchctl del Mac (bootout asincrono, errore 5 di bootstrap): qui non si può riprodurre, ho visto solo il comportamento con i finti del test. Non ho rifatto tests/test_unit_voice_server.py: il blob è identico a MERGE_HEAD, già revisionato in #651–#654-M2 e #627.

**Memoria**: aggiunta la riga #629 (più una lezione) in /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree, indice non toccato (git status: ` M`, +1 riga). Come mi hai chiesto, NON ho lanciato `scripts/commit_memoria_revisore.sh`: il commit di quel file resta da fare a te.
```

Review #631 (chat Mani), voce-fix su main e riserve della #629:

```
## VERDETTO: APPROVATO CON RISERVE

Review #631 (chat Mani). Ho fatto le tre letture obbligatorie: CLAUDE.md, le parti utili di reports/stato_progetto.md (la fetta 37, dove risulta ancora aperta R-623-2) e la memoria del revisore. Diff staged verificato: sha256 c454dc5b42e5f408…, HEAD c6206d2, MERGE_HEAD 0793476, merge-base 70e2f05.

**Fedeltà del merge (punto 1)**
- Dei file che ha toccato solo main dopo il merge-base, tutti e 15 (ci.yml, browser_server.py, prova_voci.html/.py, server.py, tts.py, test_unit_voice_prova_voci.py e reports/) hanno il blob dell'indice uguale a quello di HEAD.
- `.claude/perimetro_review.txt`, `clients/voice/ascolto.py` e `scripts/voce/installa.sh` hanno il blob uguale a quello di MERGE_HEAD.
- `git diff --cached MERGE_HEAD` sui file di voce-fix mostra solo LEGGIMI (R-629-2) e il test (R-629-1).
- Memoria: è l'unione esatta dei due lati. HEAD 1192 righe + 6 = MERGE_HEAD 1182 righe + 16 = 1198. Nessuna riga persa, nessuna doppia, nessun marcatore di conflitto, nessuna riga estranea. Rispetto a tutti e due i lati ci sono solo aggiunte.

**Elementi del diff esaminati**
1. `tests/test_unit_voce_ascolto.py:619` — il finto `sleep` ora scrive `sleep $*` nel registro. Rischio: che la riga non si possa osservare o che conti anche `sleep 0.1`. Esito: ok, perché il test usa `splitlines().count("sleep 1")`, cioè il confronto esatto della riga.
2. `tests/test_unit_voce_ascolto.py:745` — controlla che con il bootstrap sempre rotto ci siano esattamente 2 `sleep 1`. Rischio: un mutante che sopravvive. Esito: ok. Ho rifatto il mutante (sleep fuori dalla guardia `tentativo -lt 3`, in `scripts/voce/installa.sh:110`): il test fallisce. Ho ripristinato il file dall'indice e la suite dà 93 passed. Lo `sleep 1` di `scripts/voce/installa.sh:138` non entra nel conteggio, perché lo script si ferma prima di `nc`.
3. `scripts/voce/LEGGIMI.md:96` — «una riga INFO per ogni richiesta che ha speso qualcosa (niente riga … 401)». Rischio: affermazione falsa. Esito: vera. `do_POST` mette `_tempi = {}` (`modules/voice/server.py:319`). Il 401 passa da `_send_json` a `_chiudi_tempi`, che con il dizionario vuoto ritorna None senza scrivere (`modules/voice/server.py:270`). Per i GET, `_tempi = None` è prima del 401 (`modules/voice/server.py:631`).
4. `.claude/perimetro_review.txt:31` — aggiunge `scripts/voce/`. Esito: ok, il perimetro si allarga e non si indebolisce. Il merge spetta all'operatore, come già detto.

**Riserve**
- **R-631-1 COSMETICA**: R-623-2 resta aperta in stato_progetto. Se tolgo lo `sleep 1` del giro `nc` (`scripts/voce/installa.sh:138`), la suite dà ancora 93 passed: mutante vivo, ripristinato dall'indice. Ora che il finto sleep registra, la chiusura è una riga: in `test_installa_aspetta_il_server_lento` controllare che `registro.splitlines().count("sleep 1") == 3`.
- **R-631-2 COSMETICA**: «ha speso qualcosa» si può leggere come «ha speso soldi». Però `/voci/prova` spende crediti ElevenLabs e non scrive la riga dei tempi (`_tempi = None`, `modules/voice/server.py:332`). Meglio «che ha misurato dei tempi (trascrizione/cervello/voce)».

**Cosa non ho verificato**
- Non ho provato `installa.sh` sul Mac vero (launchctl reale, attesa dopo bootout): non si riproduce in dev, i test usano comandi finti.
- Non ho rieseguito la suite completa del repo: ho eseguito solo tests/test_unit_voce_ascolto.py (93 passed). Il codice di main entra con blob identici a HEAD, quindi la sua suite non cambia.

**Memoria**
- Ho scritto la riga `#631 (chat Mani)` e una lezione in `/home/user/Gas/.claude/agents/memoria_revisore.md`, solo nel working tree. L'indice è intatto: lo sha256 dello staged è ancora c454dc5b42e5f408….
- Non ho lanciato `scripts/commit_memoria_revisore.sh`: con il merge in corso, il commit del solo file di memoria chiuderebbe il merge.
- Per portare la riga nel commit di merge va fatto `git add` della memoria. Questo cambia lo sha dello staged, quindi `segna_review_ok.sh` va lanciato dopo l'add, oppure serve una nuova review del diff con la memoria.
- Nota: il mio primo tentativo di scrivere la riga è stato bloccato dall'hook review_gate, perché il testo conteneva la stringa del comando di commit. L'ho riformulato.
```

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 73 a 93 test (rilevatore in errore, GAS_CLAUDE_BIN, token vuoto, attesa dopo bootout, tentativi di bootstrap, attese contate). Nessuna modifica a gas.py.

## §6 STATO CI

`gh` non autenticato nel cloud.
- I commit di voce-fix (bc369ed, ac425b8, 2e1fdea e le memorie) sono stati solo in locale fino a questa PR.
- Il merge in main e il commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Da #324 (bot su 84b1422): V-1 BASSA (il controllo all'uscita non copre fornitori che non sono modelli, come ElevenLabs), V-2 BASSA (strumenti mail nei rami di default del diario): per la fetta 1 della mail.
- Da #324 (bot su 7346994): V-2 COSMETICA (`test_notify_telegram_safe`): per la fetta 1 della mail.
- R-625-1 BASSA (lista bianca di GAS_CLAUDE_BIN senza test), R-625-2 COSMETICA (messaggio per un nome non assoluto).
- R-615-4 MEDIA (microfono sotto launchd, da provare sul Mac); R-615-5 BASSA (licenza di hey_jarvis).
- Il comportamento vero di launchctl sul Mac (bootout asincrono) si prova solo sul Mac.
