# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 — Audit dell'11 novembre: gasmerge senza timeout sul Mac, maiuscole nei gate, sottofondo-ferma fuori cartella, CI in sola lettura (chat M3, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #376 (https://github.com/Gasss23/Gas/pull/376). Tocca la macchina di controllo (gate, hook, CI): con il bot «neutral» o con riserve decide l'operatore, via M1. Revisore APPROVATO (#767-M1, #768-M1). Bot su 078ad0a: APPROVATO CON RISERVE, check neutral, nessuna ALTA/MEDIA; la sua V-1 BASSA è corretta in 6272544.

---

## §1 SCOPE & ESITO FETTE

- **B1 MEDIA — `scripts/gasmerge.sh` senza `timeout` sul Mac**: `FATTA` — timeout → gtimeout → perl padre che uccide il figlio ed esce 124. Primo tentativo BOCCIATO (#766-M1: gh è Go e ignora SIGALRM), corretto e APPROVATO (#767-M1).
- **B2 MEDIA — maiuscole in `tocca_macchina_bot` e `_nel_perimetro`**: `FATTA` — casefold; stesso bug trovato e corretto in `.claude/hooks/review_gate.sh` (grep -i, `GIT_ICASE_PATHSPECS=1`).
- **B4 BASSA — `sottofondo-ferma` fuori dalla cartella di Gas**: `FATTA` — errore con la cartella da usare, exit 1.
- **S1 — `ci.yml` senza `permissions`**: `FATTA` — `permissions: contents: read`.
- **Bot #376 (078ad0a) e verifica esterna #376**: APPROVATO CON RISERVE, nessuna ALTA/MEDIA (https://github.com/Gasss23/Gas/pull/376#issuecomment-6784648609). V-1 BASSA comune (B2 incompleto: il promemoria «FILE DI MOTORE» di gasmerge distingueva le maiuscole): `FATTA` in 6272544 (`shopt -s nocasematch` attorno al ciclo, test), review #768-M1 APPROVATO. V-3 cosmetica (docstring di un test hooks) corretta; V-2 cosmetica (§2 «17 +-») corretta qui sotto.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  4 +
 .claude/hooks/review_gate.sh       |  6 +-
 .github/workflows/ci.yml           |  5 +
 modules/sottofondo/__init__.py     |  7 +
 reports/diff_sessione.md           | 19 +-
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |  4 +-
 reports/ultimo_report.md           | 20 +-
 scripts/bot_esito.py               | 10 +-
 scripts/check_verdetto.py          |  5 +-
 scripts/gasmerge.sh                | 17 +-
 tests/test_unit_gasmerge.py        | 63 +
 tests/test_unit_handoff_check.py   |  3 +
 tests/test_unit_hooks.py           | 19 +
 tests/test_unit_sottofondo.py      | 17 +
 tests/test_unit_verifica_bot.py    |  2 +
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile al momento della scrittura; riga di totale tolta. BASE = e3eb542.

## §3 GIT LOG --ONELINE (sessione)

```
62725449 fix(audit 11 nov): bot #376 V-1 — promemoria «FILE DI MOTORE» di gasmerge senza maiuscole (M3)
0d5ab5b7 chore(revisore): memoria review #768 — APPROVATO
078ad0a7 docs(fine-task): audit 11 nov B1/B2/B4/S1, PR #376 (M3)
8eb21c02 fix(audit 11 nov): gasmerge senza timeout sul Mac, maiuscole nei gate, sottofondo-ferma fuori cartella, CI in sola lettura (M3)
a3e00420 chore(revisore): memoria review #767 — APPROVATO
c2f8b03f chore(revisore): memoria review #766 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 8eb21c0: due giri, #766-M1 (BOCCIATO) → #767-M1 (APPROVATO). Commit 6272544 (bot #376 V-1): #768-M1 (APPROVATO). Verdetti integrali.

### Review #766-M1

## VERDETTO: BOCCIATO

Review #766-M1. Diff nel working tree di feat/r7-direttore-m3, 11 file. Ho letto CLAUDE.md (sez. 5), stato_progetto.md e la mia memoria. La riga di memoria è committata (c2f8b03f).

**Motivo del blocco (B1, MEDIA → blocco: il fix promette un timeout che sul Mac non c'è)**
- scripts/gasmerge.sh:82 — ripiego `perl -e 'alarm shift; exec @ARGV or exit 127' 900`. Rischio esaminato: SIGALRM sopravvive a exec, ma lo deve far morire il programma lanciato. Esito: **blocco**. gh è un binario Go (verificato con `file /usr/local/bin/gh`: «Go BuildID»). Il runtime Go cattura SIGALRM e, senza `signal.Notify`, lo ignora: «Other signals will be caught but no action will be taken». Prova fatta: un binario Go che dorme 6 s, lanciato sotto il perl con 1 s, finisce dopo 6 s con rc=0. Lo stesso binario sotto `timeout 1` esce con rc=124 dopo 1 s. Quindi sul Mac senza gtimeout `gh pr checks --watch` torna a poter restare appeso all'infinito, e la riga 85 (142→124) non scatta mai con gh.
- tests/test_unit_gasmerge.py:1664 — `test_perl_alarm_scaduto_vale_timeout` prova il perl con `sleep`, che è un programma C e muore con SIGALRM: con gh la prova non vale. Il secondo pezzo usa uno stub che esce 142 da solo, quindi prova solo la mappa dei codici. Esito: **blocco** (la prova non dimostra quello che dichiara).
- **Correzione proposta, già provata qui**: il perl fa da padre, con fork e kill esplicito:
  `perl -e 'my $t=shift; my $p=fork; exit 127 unless defined $p; if(!$p){exec @ARGV or exit 127} $SIG{ALRM}=sub{kill "TERM",$p; sleep 2; kill "KILL",$p; waitpid $p,0; exit 124}; alarm $t; waitpid $p,0; exit($? & 127 ? 128+($? & 127) : $? >> 8)' 900`
  Esiti misurati: binario Go ucciso dopo circa 3 s con rc 124; un figlio che esce 8 restituisce 8; un comando inesistente restituisce 127. Con questa versione la riga 85 (142→124) non serve più. Il test va rifatto con un figlio che ignora SIGALRM, per esempio `perl -e '$SIG{ALRM}="IGNORE"; sleep 5'`, verificando rc=124 e un tempo trascorso molto sotto i 5 s.
- Sulla mappa dei codici d'uscita, come richiesto: se gh esce da solo, il suo codice passa intatto (exec sostituisce il processo), e un exec fallito dà 127. Su questo la mappa è corretta.

**Resto del diff (ok)**
- scripts/bot_esito.py:210 — casefold su NOMI_MACCHINA_BOT e MACCHINA_BOT. Rischio esaminato: che allarghi o restringa male. Esito: ok. Il confronto può solo allargarsi, quindi più PR finiscono in «neutral» (decide l'operatore): è la direzione prudente. I test_no esistenti restano verdi e `[".Claude/hooks/x.sh"]`/`[".GITHUB/..."]` sono coperti.
- scripts/check_verdetto.py:155 — `_nel_perimetro` senza maiuscole. Lo usano anche scripts/check_handoff.py:144 e scripts/check_verdetto.py:249, entrambi come «tocca il perimetro → servono più controlli». Allargare quindi rende i gate più severi, mai più deboli. Esito: ok.
- .claude/hooks/review_gate.sh:371 — `grep -qiE "$PERIM_RE"`. Il regex è ancorato con `^(...)` (.claude/hooks/review_gate.sh:341); -i allarga solo, nella direzione del blocco. Esito: ok. Test: tests/test_unit_hooks.py `test_gate_maiuscole_bloccano`, 3 passed rieseguiti.
- .github/workflows/ci.yml:25 — `permissions: contents: read`. Rischio esaminato: step che scrivono su GitHub. Gli step usano solo actions/checkout@v4, setup-python@v5, `git fetch origin main` (.github/workflows/ci.yml:372) e script con gh finto. Nessun job ridefinisce i permessi. Esito: ok.
- modules/sottofondo/__init__.py:276 — `ferma()` senza cartella della coda restituisce (False, frase) ed exit 1 (unico chiamante: gas.py:6707). Tutto resta dentro il try e non introduce eccezioni nuove. Esito: ok, con una nota COSMETICA sotto.

**Riserve (da tracciare anche dopo il nuovo giro)**
- BASSA, risponde alla tua domanda sulla riga ~360 — sì, il pathspec ha lo stesso problema. .claude/hooks/review_gate.sh:360: il filtro di `git status ... -- "${PERIM_PATHS[@]}"` distingue le maiuscole. Prova in un repo di prova: `GAS.py` e `Brains/x.py` non tracciati restano invisibili col pathspec `gas.py brains/`, e compaiono con `GIT_ICASE_PATHSPECS=1`. Sul Mac il danno è limitato: il disco non distingue le maiuscole e git di norma vede il nome reale sul disco. Su Linux un file come `GAS.py` non tracciato sfugge al blocco «modifiche non in stage». Correzione: anteporre `GIT_ICASE_PATHSPECS=1` a quel `git status`, più un test.
- COSMETICA: in una cartella di Gas dove non è mai partito nessun compito, `sottofondo-ferma` dice «lancia il comando dalla cartella di Gas», che lì è fuorviante. Si potrebbe distinguere controllando se esiste gas.py in root.

**Rischi esclusi (non verificati)**
- Non ho provato su macOS reale: le differenze tra perl e il runtime Go per Darwin le ho dedotte. Il comportamento Go su SIGALRM è documentato uguale su tutti i sistemi ed è provato qui su Linux.
- Non ho rieseguito le suite complete (891 test di gasmerge/verifica_bot/handoff_check/sottofondo, 214 hooks, 1135 kernel): mi fido dei numeri dichiarati. Ho rieseguito solo i test nuovi: 2 passed con `-k Timeout` e 3 passed per le maiuscole negli hooks.
- Non ho verificato la run CI reale con i nuovi permessi.

Nessuno slicing della history e nessuna simulazione dei tool nel diff.

File rilevanti:
- scripts/gasmerge.sh
- tests/test_unit_gasmerge.py
- .claude/hooks/review_gate.sh
- .claude/agents/memoria_revisore.md

### Review #767-M1

## VERDETTO: APPROVATO

Secondo giro della review #766-M1 (che era BOCCIATO), branch feat/r7-direttore-m3, modifiche ancora non committate (working tree). Ho letto prima CLAUDE.md §5, la memoria del revisore e l'intestazione di stato_progetto.

Cosa ho esaminato nel diff:

- `scripts/gasmerge.sh:84` — Cosa fa: se mancano `timeout` e `gtimeout`, usa perl come processo padre (fork ed exec del comando, poi alarm; allo scadere manda TERM, aspetta 2 s, manda KILL ed esce 124). Rischio esaminato: gh è un binario Go e ignora SIGALRM, che era il motivo del BOCCIATO. Prova fatta con un binario Go vero, compilato apposta, col programma perl estratto da gasmerge.sh:
  - binario da 8 s con limite 1 s → rc 124 in 3 s;
  - figlio che esce con codice 3 → rc 3 (codice passato);
  - `kill -9` su se stesso → rc 137;
  - figlio che ignora sia TERM sia ALRM → ucciso con KILL, rc 124.

  La mappa 142→124 è tolta e il `case` a `scripts/gasmerge.sh:91` è coerente. Esito: ok.
- `tests/test_unit_gasmerge.py:1665` — Cosa fa: estrae il programma perl dal sorgente di gasmerge.sh con una regex, quindi il test si rompe se lo script cambia. Prova un figlio che ignora SIGALRM (rc 124 in meno di 6 s), il codice 8 passato e il 127 su un comando inesistente. Rischio esaminato: che sia di nuovo una prova falsa come col vecchio `sleep`. Il figlio perl con `$SIG{ALRM}="IGNORE"` riproduce il comportamento di Go. Esito: ok.
- `.claude/hooks/review_gate.sh:361` — Cosa fa: aggiunge `GIT_ICASE_PATHSPECS=1` a `git status` sul pathspec del perimetro, così le maiuscole non contano anche per i file non tracciati. Rischio esaminato: un file non tracciato come Brains/x.py non verrebbe visto. Esito: ok, coperto da `tests/test_unit_hooks.py:572`.
- `modules/sottofondo/__init__.py:277` — Cosa fa: `ferma()` senza coda ma con gas.py nella root risponde (True, «Nessun compito in sottofondo in corso.»). Da un'altra cartella resta l'errore che dice di lanciarlo dalla cartella di Gas. Tutto sta dentro il try esistente, quindi nessuna eccezione nuova. Esito: ok.

Suite rieseguita: gasmerge + hooks + sottofondo + verifica_bot + handoff_check, 1106 passed (cioè 891 + 215, come dichiarato).

Wall of Shame: nessuno slicing della storia e nessuna simulazione di tool. Il motore (gas.py, brains) non è toccato.

Cosa NON ho verificato:

- Non ho fatto la prova a mano di `GIT_ICASE_PATHSPECS` in un repo temporaneo: il comando conteneva la parola "commit" e il gate e il classificatore dei permessi l'hanno negato. Non ho aggirato il blocco. Mi affido al test `tests/test_unit_hooks.py:572`, che è passato. Non ho rifatto nemmeno la prova inversa (il test fallisce senza la correzione): resta un'affermazione dell'autore.
- Comportamento reale su macOS non verificato: qui gira Linux. Il perl di sistema del Mac e un gh vero in modalità `--watch` non sono riproducibili in questo ambiente.
- Limite noto (BASSA, non è una riserva): con il ripiego perl l'uccisione arriva solo al figlio diretto, non ai suoi eventuali sotto-processi. Per `gh pr checks` non conta, perché non ne lancia.

Memoria del revisore: aggiunta la riga #767-M1 e committata da sola con lo script dedicato (commit a3e00420), in .claude/agents/memoria_revisore.md. Nessuna lezione nuova.

### Review #768-M1 (bot #376 V-1)

## VERDETTO: APPROVATO

Il fix è corretto e ha un ambito stretto. Il test morde, la suite passa.

**Elementi del diff esaminati**

- `scripts/gasmerge.sh:237`: `shopt -s nocasematch` viene acceso subito prima del ciclo del promemoria «FILE DI MOTORE». Ho cercato un'uscita anticipata che lasci l'opzione accesa. Nel ciclo, che va da `scripts/gasmerge.sh:240` a `scripts/gasmerge.sh:249`, ci sono solo `continue` e `break`: niente `exit` né `return`, e niente comandi che possano far scattare `set -e`, perché i `[[ ]]` stanno dentro liste `&&` e `read` chiude il ciclo senza errore. Gli input arrivano con `<<<`, quindi non c'è una subshell. Dentro il ciclo nocasematch tocca anche il `case "$v" in */)`, ma quel modello non contiene lettere, quindi non cambia nulla. Esito: ok.
- `scripts/gasmerge.sh:250`: `shopt -u nocasematch` viene spento subito dopo il `done`. In tutto il file ci sono solo questi due `shopt`, entrambi in questo diff, quindi nessun altro confronto `[[ ]]` o `case` del file è influenzato. Il rischio che resta è opposto, cioè più file segnalati come motore, e per un promemoria che non è un gate va nel verso sicuro. Esito: ok.
- `tests/test_unit_gasmerge.py:537`: il test nuovo `test_maiuscole_nel_perimetro` copre `GAS.py` e `Modules/x.py`. Ho fatto una mutazione su una copia del repo nello scratchpad, togliendo `shopt -s`: 2 test falliti e 10 passati nella classe. Il test morde. Esito: ok.
- `tests/test_unit_hooks.py:573`: cambia solo la docstring, che ora parla di `Brains/x.py` e quindi corrisponde al corpo del test. Nota cosmetica: la riga è molto lunga, ma non blocca. Esito: ok.
- Suite `tests/test_unit_gasmerge.py` + `tests/test_unit_hooks.py`: 330 passati, rifatto da me.

**Cosa NON ho verificato**

Non ho eseguito il codice col bash 3.2 di macOS: qui non c'è. Che `nocasematch` esista in quella versione lo ricavo dalla documentazione di bash (l'opzione c'è dalla 3.1), non da una prova.

**Memoria del revisore**

Ho aggiunto in coda a `.claude/agents/memoria_revisore.md` la riga `#768-M1 — 2026-11-11 — APPROVATO — … — nessuna lezione nuova`. Ho poi lanciato `scripts/commit_memoria_revisore.sh`, che non ha stampato nulla; `git status` non mostra più quel file come modificato. Il diff sotto review è intatto nel working tree: `scripts/gasmerge.sh`, `tests/test_unit_gasmerge.py` e `tests/test_unit_hooks.py` risultano ancora modificati.

## §5 DELTA TEST DEL MOTORE

- Senza le correzioni (stash): 8 test falliscono in gasmerge/verifica_bot/handoff_check/sottofondo (`8 failed, 883 passed`); il test hook delle maiuscole (3 casi) e quello del file non tracciato falliscono senza il fix dell'hook; il vecchio ripiego `alarm; exec` dava rc 0 dopo 4 s su un figlio che ignora SIGALRM.
- Con le correzioni: gasmerge + verifica_bot + handoff_check + sottofondo `891 passed`; hooks `215 passed`. Dopo 6272544: gasmerge + hooks `330 passed` (test nuovo `test_maiuscole_nel_perimetro`: 2 failed senza il fix).
- Suite kernel (dopo il primo giro di correzioni; il secondo giro non tocca il codice letto dal kernel):

```
=== RIEPILOGO: 1135 PASS, 0 FAIL ===
```

## §6 STATO CI

Check della PR #376 letti alla scrittura dell'handoff, head 078ad0a (prima del push di questo giro): `handoff-check` success; `verifica-bot` neutral (PR sulla macchina del bot, verdetto APPROVATO CON RISERVE senza ALTA/MEDIA); `unit-suite` (run 42941195559) in corso secondo la verifica esterna, esito finale non letto.

Mappatura commit→run:
- 078ad0a: run 42941195559 (CI) e run del bot su quello SHA.
- 8eb21c0, a3e0042, c2f8b03: nessuna run su questi SHA (pushati insieme a 078ad0a).
- 0d5ab5b, 6272544: nessuna run su questi SHA (escono col push di questo giro).
- Commit di fine-task di questo giro: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Limite noto (BASSA, #767-M1): il ripiego perl uccide solo il figlio diretto (gh pr checks non lancia sotto-processi).
- Non verificato: macOS reale (perl di sistema, bash 3.2 con nocasematch, gh vero in `--watch`), esito finale di unit-suite coi nuovi permessi.
