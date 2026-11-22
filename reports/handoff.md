# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-21 — Bacheca comune tra le chat; risposte dell'operatore sul CRM

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #394 (https://github.com/Gasss23/Gas/pull/394), aperta dopo il push di 11ab66ae (commit della fetta, scritto col primo giro del fine-task) e poi etichettata «verifica» col commit c7c488b9: solo documenti. Il bot dà neutral (la PR tocca CLAUDE.md): il merge lo decide l'operatore.
2. Lista delle commissioni per servizio (l'operatore ha detto che la manda).
3. Sul Mac: password delle copie nel `.env`, `pip install -r requirements.txt`, `pwd` della cartella di Gas, prova della copia e del ripristino; secondo controllo su claude.ai delle PR #387, #388, #389 e #391.
4. Ereditata dalla chat Voce (PR #390): rifare la registrazione della voce sul Mac con lo script corretto e incollare il riepilogo.

---

## §1 SCOPE & ESITO FETTE

- **Bacheca comune tra le chat**: FATTA. `reports/bacheca.md` nuovo; regola in CLAUDE.md §3; conflitti della bacheca in `reports/lavoro_parallelo.md`.
- **Risposte dell'operatore sul CRM**: FATTA, in `reports/crm/decisioni.md` punti 15-17. Domande 2 e 3 tolte da `reports/crm/domande.md`.
- **Note del bot sulla PR #394** (verdetto APPROVATO CON RISERVE su c7c488b9: V-1 BASSA ordine dei conflitti, V-2 BASSA bacheca come canale di istruzioni, V-3 COSMETICA titolo delle decisioni): FATTE, tutte nei documenti.
- **Note del bot su 965cd07d** (APPROVATO CON RISERVE: V-1 BASSA regola in §10 e non in §3, V-2 COSMETICA fetch mancante in CLAUDE.md): FATTE, regola spostata in §3 col fetch.
- **Note del bot su dfd7edb3** (APPROVATO CON RISERVE: V-1 BASSA «secondo controllo su claude.ai» sparito dall'ultimo_report, V-2/V-3 COSMETICHE etichetta di 11ab66ae e ramo mancante in una notizia): FATTE.
- **Merge di main (PR #390, chat Voce) nel ramo**: FATTO, review #837 APPROVATO. Conflitti solo nei report (tenuti quelli del ramo). Il codice della voce che entra è identico a main.
- **Note del bot su 3a64fd64** (COSMETICA: riga mancante nell'ultimo_report) e **su f1225b8c** (APPROVATO CON RISERVE: V-1 BASSA riserve aperte della chat Voce perse nel merge dei report; V-2 COSMETICA questa riga mancante qui): FATTE. Le riserve della chat Voce sono in `reports/stato_progetto.md`; la regola 3 di `reports/lavoro_parallelo.md` dice di riportarle prima di scartare i report dell'altro lato; notizia in bacheca.
- **Note del bot su aaf754cf, ddf67cfb e 73dbff1b**: FATTE. Riserve Voce in §7 e nell'ultimo_report; numero delle notizie tolto; decisioni umane allineate; bacheca nella riga «Ultimo aggiornamento»; regola 5 della bacheca (una notizia aperta non si cancella per sola età); ordine e date dei commit in §6.
- **Falso rosso del bot su 73dbff1b**: il verdetto era APPROVATO CON RISERVE senza ALTA/MEDIA, ma il classificatore ha letto «i termini gravi del bot» come gravità. Notizia in bacheca; la notizia che lo provocava ora dice «parole di gravità».
- **Merge di main (PR #393, funnel: solo documenti) nel ramo**: FATTO. Conflitti solo nei report e nella memoria del revisore (unione); prima di scartare i report del funnel, le sue decisioni in sospeso sono state portate in `reports/stato_progetto.md` (regola 3 di `reports/lavoro_parallelo.md`). L'operatore ha detto in chat «sì, mergia la #394».
- **Merge di main (PR #395, chat Voce) nel ramo**: FATTO, review #838-MERGE (chat CRM) APPROVATO CON RISERVE (R-838M-1 COSMETICA, chiusa). Codice della voce identico a main; riserve della voce aggiornate in `reports/stato_progetto.md`.
- **PR #391**: MERGIATA prima di questa fetta (eecf916d).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 CLAUDE.md                          |   1 +
 reports/bacheca.md                 |  31 +++++++++++++++++++++++++++++++
 reports/crm/decisioni.md           |   6 ++++++
 reports/crm/domande.md             |   4 +---
 reports/diff_sessione.md           |  13 +++++++------
 reports/handoff.md                 | n/d
 reports/lavoro_parallelo.md        |   3 ++-
 reports/stato_progetto.md          |   5 ++++-
 reports/ultimo_report.md           |  33 +++++++++++++++++++--------------
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base: 9a9d0036 (origin/main dopo il merge della PR #395, entrato nel ramo col merge di main); i file delle PR #390, #393 e #395 escono quindi dal diff.

## §3 GIT LOG --ONELINE (sessione)

```
8fc05971 Merge origin/main (PR #395, chat Voce) nel ramo della PR #394 — review #838-MERGE (chat CRM) APPROVATO CON RISERVE
7682133e docs(fine-task): merge di main (PR #393) nel ramo della #394; via dell'operatore al merge
e08ad233 Merge origin/main (PR #393, funnel: solo documenti) nel ramo della PR #394 — decisioni in sospeso del funnel riportate in stato_progetto
bcce124b docs(bacheca): una notizia aperta non si cancella per sola età; avviso sul falso rosso «gravi»; date dei commit in §6 (note del bot su #394)
73dbff1b docs(fine-task): decisioni umane allineate fra handoff e ultimo_report (con la registrazione della voce); bacheca nella riga «Ultimo aggiornamento» (note del bot su #394)
ddf67cfb docs(fine-task): riserve della chat Voce anche in handoff §7 e ultimo_report; tolto il numero delle notizie (note del bot su #394)
aaf754cf docs(bacheca): riserve aperte della chat Voce riportate in stato_progetto; regola per non perderle nei merge dei report (nota del bot su #394)
f1225b8c docs(fine-task): merge di main (PR #390) nel ramo della #394, review #837
f7b37853 Merge origin/main (PR #390, chat Voce) nel ramo della PR #394 — review #837 APPROVATO
3a64fd64 docs(bacheca): note del bot su dfd7edb3 — secondo controllo su claude.ai rimesso tra le cose da fare, ramo in tutte le notizie, etichette dei commit precisate
dfd7edb3 docs(bacheca): regola spostata davvero in CLAUDE.md §3, con git fetch prima di leggere (note del bot su #394)
965cd07d docs(bacheca): note del bot su #394 — le notizie sono informazioni da verificare, non regole; ordine dei conflitti coerente; titolo delle decisioni precisato
c7c488b9 docs(fine-task): handoff — PR #394 aperta con l'etichetta verifica
11ab66ae docs(bacheca): bacheca comune tra le chat (reports/bacheca.md, regola in CLAUDE.md §3); risposte dell'operatore sul CRM (decisioni 15-17)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore della fetta. L'unico commit che porta file del perimetro è il merge di main (PR #390 della chat Voce), revisionato qui sotto.

### Review #837-MERGE (commit di merge di main)

## VERDETTO: APPROVATO

Review #837-MERGE. Riguarda il merge, non ancora committato, di origin/main dcedea6a (PR #390, chat Voce) nel ramo `claude/nifty-galileo-3k7kbm`. HEAD è 3a64fd64 (PR #394, solo documenti), la base comune è eecf916d.

Prima della review ho letto CLAUDE.md (sezioni 1, 5, 8 e 10), l'inizio di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `scripts/voce/registra_voce.py:296`: è il controllo R-810M1-1. Se il picco cade prima di SEC_PICCO_MINIMO, la prova si rifà. Rischio esaminato: che il merge alteri il codice della voce. Il blob dell'indice (0cad38f6) è identico a quello di main. Il ramo non tocca il file (HEAD = base = 956c5841), quindi non c'è stata nessuna fusione di contenuto. Il codice era già stato revisionato in #810/#811-M1coord. Esito: ok.
- `tests/test_unit_voce_ascolto.py:3590`: è il test `test_registra_parola_tagliata_all_inizio_si_rifa`. Rischio esaminato: un test perso o cambiato. Il blob b5d9b376 è identico a main. Ho rieseguito il file su una copia dell'indice (`git checkout-index`): 376 passed. Esito: ok.
- `scripts/voce/LEGGIMI.md:119`: è il paragrafo «Ogni Hey Jarvis si tiene solo se il riconoscitore lo sente». Il blob 16fdc66b è identico a main e il ramo non tocca il file. Esito: ok.
- `reports/stato_progetto.md:4` e `reports/stato_progetto.md:9`: sono l'unico file cambiato da tutti e due i lati. Main cambia la riga 4 («Ultimo aggiornamento», con l'aggiunta della voce 20/11). Il ramo aggiunge la riga 9 (la notizia «Bacheca comune»). Rischio esaminato: righe perse o duplicate dall'unione automatica. L'indice è byte-identico all'output di `git merge-file` a tre vie (HEAD, base, main). Il confronto riga per riga dà 0 righe perse e 0 in più. È anche l'unico file diverso sia da HEAD sia da main. Esito: ok.
- `.claude/agents/memoria_revisore.md`: il ramo non la tocca (HEAD = base = 5137c29c). L'indice è uguale a main (ff788f56) e contiene le 6 righe di main (#810/#811 e lezioni, #812 e #814). Anche qui `git merge-file` dà un risultato identico e il confronto riga per riga dà 0 perse e 0 in più. Esito: ok.

**Controlli strutturali**
- Nessun file in conflitto rimasto (`git ls-files -u` vuoto).
- Nessun marcatore di conflitto negli 8 file interessati.
- `git diff --cached --check` pulito.
- Albero di lavoro uguale all'indice (prima della mia riga in memoria).
- Il delta `git diff --cached origin/main` sul perimetro di review (gas.py, brains, modules, tests, scripts, .claude, .github, clients) è VUOTO. Il codice che entra è byte-identico a main.
- Questi file hanno lo stesso blob di HEAD, cioè la versione del ramo:
  - reports/handoff.md, reports/ultimo_report.md, reports/diff_sessione.md (conflitti risolti col ramo, come dichiarato);
  - CLAUDE.md, reports/bacheca.md, reports/crm/decisioni.md, reports/crm/domande.md, reports/lavoro_parallelo.md.
- Il delta verso main riguarda solo i 9 file .md della PR #394, come dichiarato.

**Antipattern (sezione 5)**: il merge non introduce codice nuovo, quindi non c'è slicing della history né simulazione dei tool. Guardrail invariati.

**Cosa NON ho verificato**
- Non ho rifatto la review semantica dei 3 file della voce: sono byte-identici a main e già revisionati in #810/#811-M1coord. R-810M1-2 BASSA (tempi del messaggio «ogni N secondi») resta aperta e va verificata sul Mac.
- Non ho rieseguito la suite completa: solo il test della voce. Il resto del codice è identico a HEAD o a main, e la CI di main è già verde.
- Non ho controllato se i contenuti dei report del ramo sono corretti: verranno riscritti dal fine-task.

**Note per il chiamante**
1. Ho aggiunto la riga contatore `#837-MERGE` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. NON è in staging e NON l'ho committata: durante un merge `git commit -o` viene rifiutato e tu avevi chiesto di non committare. Va messa in staging da te (`git add .claude/agents/memoria_revisore.md`) prima di chiudere il merge. Non ho creato `.claude/.review_ok`.
2. Nel fine-task, la riga «Ultimo aggiornamento» di reports/stato_progetto.md cita funnel 21/11 e voce 20/11, ma non ancora la bacheca. La bacheca sta solo nella riga 🆕 di «Stato motore». Puoi aggiungerla, se lo ritieni utile.

Nessuna lezione nuova.

### Review #838-MERGE (chat CRM, commit di merge della PR #395)

## VERDETTO: APPROVATO CON RISERVE

Review #838-MERGE (chat CRM). Ho controllato il merge in corso di origin/main 9a9d0036 (PR #395, voce) nel ramo `claude/nifty-galileo-3k7kbm` (HEAD 7682133e, PR #394, solo documenti). La base è a98a11cf. Il merge non perde codice e non lo altera. Nello stato non manca nessuna riga, ma la riga «Voce, riserve aperte», riscritta, ha perso una voce (riserva sotto).

**Controlli meccanici (rieseguiti da me)**
- Nessun file in conflitto (`git ls-files -u` vuoto), nessun marcatore di conflitto, `git diff --cached --check` pulito, albero di lavoro uguale all'indice.
- Nel perimetro di review, l'indice differisce da main solo nella memoria del revisore.
- Sono rimasti identici a HEAD: handoff, ultimo_report, diff_sessione, CLAUDE.md, bacheca, crm/decisioni, crm/domande, lavoro_parallelo. È corretto per la regola 3 di `reports/lavoro_parallelo.md`.

**Elementi del diff esaminati**
1. `scripts/voce/registra_voce.py:277`: se il microfono non ha mai dato suono, dopo le 3 prove (`TENTATIVI_PAROLA`) della prima clip lo script si ferma con un errore. Rischio esaminato: che il codice entrato col merge sia diverso da quello revisionato in #813-M1coord. I tre file della voce sono identici a main. Il loro diff staged ha sha256 31c92e5c, lo stesso di b46fde99 e di base..MERGE_HEAD. L'errore lo cattura `scripts/voce/registra_voce.py:625` e viene stampato senza traceback. Esito: ok.
2. `scripts/voce/registra_voce.py:302`: `sentito_suono` diventa vero solo dopo il controllo del volume. Rischio esaminato: un mutante che sposta il flag. È R-813M1-1, già aperta e riportata nello stato, quindi niente di nuovo. Esito: ok.
3. `tests/test_unit_voce_ascolto.py:3607`: test nuovi sul microfono muto, sul silenzio dopo un suono (`tests/test_unit_voce_ascolto.py:3625`) e sui secondi interi del messaggio. Rischio esaminato: che i test non girino sull'albero unito. Ho rieseguito la suite su una copia dell'indice: **379 passed**. Esito: ok.
4. `scripts/voce/LEGGIMI.md:122`: la guida dice «ogni 9 secondi circa» e spiega cosa succede col permesso negato. È coerente con `scripts/voce/registra_voce.py:268` (arrotondamento per eccesso di 6 + 1,5 + 1 = 9). Esito: ok.
5. `.claude/agents/memoria_revisore.md`: rischio esaminato, righe perse nell'unione. Ho confrontato le quattro versioni (base, HEAD, main, indice) riga per riga, dividendo solo su `\n`. `splitlines()` dava numeri falsi per via di caratteri speciali. L'unione è esatta: 0 righe perse, 0 in più. Si aggiungono #837-MERGE del ramo, #813-M1coord di main e la sua lezione, che resta subito dopo la sua riga. L'ordine relativo di ciascun lato è rispettato. Esito: ok.
6. `reports/stato_progetto.md:4`: rischio esaminato, che il ramo o main perdano qualcosa nella riga «Ultimo aggiornamento». Ho provato che la riga dell'indice è esattamente quella di main con in testa il frammento del ramo sulla bacheca («bacheca comune tra le chat in `reports/bacheca.md`, regola in CLAUDE.md §3; »). Gli altri 4 segmenti sono identici. Le righe 9 e 11 sono uguali a HEAD, le 978 righe totali sono come in HEAD, e cambiano solo la 4 e la 10. Esito: ok.
7. `reports/stato_progetto.md:10`: la riga «Voce, riserve aperte» è riscritta dalla sezione «Riserve aperte» dell'ultimo_report di main. Ci sono R-813M1-1, le V-1/V-2/V-3 del bot su #390, R-810M1-2 attenuata, le note di #382/#383, il limite «non verificabile qui» sul permesso negato e la cosa da fare (rifare la registrazione sul Mac). Rischio esaminato: voci della riga precedente cadute. Esito: **riserva** (sotto).

**Riserve**
- **R-838M-1 (COSMETICA)**: la nuova `reports/stato_progetto.md:10` perde la voce della riga vecchia «punteggi reali della voce dell'operatore da lontano (3 m, altra stanza) col microfono del Mac non verificati». Veniva dal «Non verificato qui» del report della #390 (dcedea6a). Nel report della #395 manca perché ultimo_report riguarda un solo task, non perché la cosa sia stata verificata. Il danno è basso, perché resta «rifare la registrazione della voce sul Mac e incollare il riepilogo», che produrrà quei punteggi. Rimedio: rimettere una frase, per esempio «punteggi reali da lontano non verificati: li darà il riepilogo della nuova registrazione».

**Note per il fine-task (non bloccanti)**
- `reports/handoff.md:136` e `reports/ultimo_report.md:26` sono le versioni del ramo, tenute per regola. Elencano ancora le riserve voce vecchie: R-810M1-2 «senza bip e analisi», niente R-813M1-1, niente V-1/V-2/V-3 del bot su #390. Vanno allineate alla riga 10 dello stato.
- In `reports/stato_progetto.md:4` la data dice ancora 2026-11-21, mentre le righe 9 e 10 dicono 22-11.

**Cosa non ho verificato e perché**
- La suite completa: ho rieseguito solo `tests/test_unit_voce_ascolto.py`. Nel perimetro l'albero unito è identico a main, salvo la memoria, quindi il resto del codice non cambia rispetto a main. Lo stato della CI su main 9a9d0036 non l'ho controllato.
- Il comportamento reale su macOS col permesso del microfono negato (silenzio puro o rumore minimo): non si riproduce qui. È già dichiarato nell'ultimo_report di main.

**Citazioni per il controllo del verdetto (`check_verdetto.py`)**: dopo il merge il diff di sessione del ramo contiene solo .md fuori dal perimetro, quindi il minimo di 2 citazioni non si applica. Tutte le citazioni sopra esistono a HEAD dopo il merge, compresi i file della voce che arrivano da main.

**Memoria**: ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga contatore #838-MERGE e una lezione nuova: quando un merge riscrive la riga «riserve aperte» di un'altra chat, confrontarla voce per voce con quella che sostituisce. Le due righe sono solo nell'albero di lavoro, non in staging: le aggiungi tu all'indice prima del commit di merge. Non ho lanciato `scripts/commit_memoria_revisore.sh`, perché il suo commit del solo file a merge in corso concluderebbe il merge (lezione del 2026-11-02) e perché me l'hai chiesto. Non ho creato `.claude/.review_ok` e non ho committato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - `11ab66ae` (commit della fetta, col primo giro del fine-task): run appena partita al push, esito non ancora disponibile alla scrittura dell'handoff.
  - `c7c488b9`: handoff-check success; unit-suite in corso; verifica-bot neutral (APPROVATO CON RISERVE, note chiuse in questo commit).
  - `965cd07d`: handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, note chiuse in questo commit).
  - `dfd7edb3`: handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, note chiuse in questo commit).
  - `3a64fd64`: unit-suite success, handoff-check success, verifica-bot neutral (APPROVATO CON RISERVE, una nota COSMETICA chiusa qui); PR in conflitto dopo il merge della #390.
  - `f7b37853` (merge di main): nessuna run propria (pushato con f1225b8c).
  - `f1225b8c`: handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, note chiuse in aaf754cf).
  - `aaf754cf`: handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE: V-1 BASSA riserve Voce mancanti in §7 e nell'ultimo_report, V-2 COSMETICA «prime tre notizie»: chiuse in ddf67cfb).
  - `ddf67cfb`: handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE: V-1 BASSA decisioni umane non allineate fra handoff e ultimo_report, V-2 COSMETICA bacheca assente dalla riga «Ultimo aggiornamento»: chiuse in 73dbff1b).
  - `73dbff1b`: handoff-check success; verifica-bot failure per un falso positivo del classificatore (verdetto APPROVATO CON RISERVE con V-1 BASSA e V-2 COSMETICA; la parola «gravi», citata come argomento, letta come gravità): note chiuse in questo commit.
  - `bcce124b`: unit-suite success, handoff-check success, verifica-bot neutral (APPROVATO CON RISERVE, una nota COSMETICA sulla regola 5); poi conflitto dopo il merge della #393 su main.
  - Merge di main (PR #393): run non ancora disponibile alla scrittura dell'handoff.
  - `7682133e`: unit-suite success, handoff-check success, verifica-bot neutral (APPROVATO CON RISERVE); poi conflitto dopo il merge della #395.
  - Merge di main (PR #395): run non ancora disponibile alla scrittura dell'handoff.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna nuova di questa fetta. Dal CRM resta R-836-1 COSMETICA.
- **Riserve della chat Voce ereditate dai merge della #390 e della #395** (in `reports/stato_progetto.md`): R-813M1-1 BASSA (manca un test «suono forte non riconosciuto 3 volte»), note basse del bot #390 (V-1/V-2/V-3), R-810M1-2 BASSA attenuata (margine di 1 s da misurare sul Mac), note basse #382 V-1/V-2 e #383 V-2/V-3, punteggi della voce da lontano non verificati.
- **R-838M-1 (COSMETICA, review #838-MERGE chat CRM):** nella riga «Voce, riserve aperte» mancavano i punteggi da lontano: rimessi.
