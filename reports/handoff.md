# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-21 — Bacheca comune tra le chat; risposte dell'operatore sul CRM

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #394 (https://github.com/Gasss23/Gas/pull/394), aperta dopo il push di 11ab66ae (commit della fetta, scritto col primo giro del fine-task) e poi etichettata «verifica» col commit c7c488b9: solo documenti. Il bot dà neutral (la PR tocca CLAUDE.md): il merge lo decide l'operatore.
2. Lista delle commissioni per servizio (l'operatore ha detto che la manda).

---

## §1 SCOPE & ESITO FETTE

- **Bacheca comune tra le chat**: FATTA. `reports/bacheca.md` nuovo; regola in CLAUDE.md §3; conflitti della bacheca in `reports/lavoro_parallelo.md`.
- **Risposte dell'operatore sul CRM**: FATTA, in `reports/crm/decisioni.md` punti 15-17. Domande 2 e 3 tolte da `reports/crm/domande.md`.
- **Note del bot sulla PR #394** (verdetto APPROVATO CON RISERVE su c7c488b9: V-1 BASSA ordine dei conflitti, V-2 BASSA bacheca come canale di istruzioni, V-3 COSMETICA titolo delle decisioni): FATTE, tutte nei documenti.
- **Note del bot su 965cd07d** (APPROVATO CON RISERVE: V-1 BASSA regola in §10 e non in §3, V-2 COSMETICA fetch mancante in CLAUDE.md): FATTE, regola spostata in §3 col fetch.
- **Note del bot su dfd7edb3** (APPROVATO CON RISERVE: V-1 BASSA «secondo controllo su claude.ai» sparito dall'ultimo_report, V-2/V-3 COSMETICHE etichetta di 11ab66ae e ramo mancante in una notizia): FATTE.
- **Merge di main (PR #390, chat Voce) nel ramo**: FATTO, review #837 APPROVATO. Conflitti solo nei report (tenuti quelli del ramo). Il codice della voce che entra è identico a main.
- **Note del bot su 3a64fd64** (COSMETICA: riga mancante nell'ultimo_report) e **su f1225b8c** (APPROVATO CON RISERVE: V-1 BASSA riserve aperte della chat Voce perse nel merge dei report; V-2 COSMETICA questa riga mancante qui): FATTE. Le riserve della chat Voce sono in `reports/stato_progetto.md`; la regola 3 di `reports/lavoro_parallelo.md` dice di riportarle prima di scartare i report dell'altro lato; notizia in bacheca.
- **PR #391**: MERGIATA prima di questa fetta (eecf916d).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 CLAUDE.md                          |   1 +
 reports/bacheca.md                 |  30 ++++++++++++++++++++++++++++++
 reports/crm/decisioni.md           |   6 ++++++
 reports/crm/domande.md             |   4 +---
 reports/diff_sessione.md           |  17 +++++++----------
 reports/handoff.md                 | n/d
 reports/lavoro_parallelo.md        |   3 ++-
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  29 +++++++++++++++--------------
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base: dcedea6a (origin/main dopo il merge della PR #390, entrato nel ramo col merge di main); i file della #390 escono quindi dal diff.

## §3 GIT LOG --ONELINE (sessione)

```
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
  - `aaf754cf`: handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE: V-1 BASSA riserve Voce mancanti in §7 e nell'ultimo_report, V-2 COSMETICA «prime tre notizie»: chiuse in questo commit).
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna nuova di questa fetta. Dal CRM resta R-836-1 COSMETICA.
- **Riserve della chat Voce ereditate dal merge della #390** (riportate in `reports/stato_progetto.md`): R-810M1-2 BASSA (messaggio «ogni N secondi» senza bip e analisi, da verificare sul Mac); punteggi reali della voce da lontano non verificati; note basse del bot #382 V-1/V-2 e #383 V-2/V-3.
