# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-06 — Bot di verifica: «ad alta voce» non è una gravità (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta del parser (numero e URL nella risposta dell'integrazione GitHub alla creazione; `gh` nel cloud non è autenticato). Tocca `scripts/bot_esito.py` (macchina del bot): il check `verifica-bot` dà neutral e il merge lo decide l'operatore (CLAUDE.md §10). La fetta è stata approvata dall'operatore via M1 («fallo in una PR separata subito dopo la #339, con test sul testo vero»).

---

## §1 SCOPE & ESITO FETTE

- **Falso failure del bot su «ad alta voce»** (verdetto vero #339 su 312cd86, solo BASSE/COSMETICHE, dato come MEDIA): `FATTA` — `_ALTA_VOCE` in `scripts/bot_esito.py`, review #687-M2 APPROVATO CON RISERVE, #688-M2 APPROVATO (R-687-1-M2 chiusa).
- **Altro falso failure su d9c09e9** (citazione «R-682-1-M2 MEDIA …» senza parentesi): `NON FATTA — fuori scope`: il difetto blocca invece di lasciar passare (direzione sicura); si evita scrivendo le riserve come «R-xxx (GRAVITÀ)».
- **Fetta 2 voce rapida** e **documento della fetta 3**: `DEFERITE — prossime fette` (ordine di M1).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md               |  2 ++
 reports/diff_sessione.md                         | n/d
 reports/handoff.md                               | n/d
 reports/ripartenza_m2.md                         | n/d
 reports/stato_progetto.md                        | n/d
 reports/ultimo_report.md                         | n/d
 scripts/bot_esito.py                             |  9 ++++++++-
 tests/dati_verifica_bot/verdetto_339_312cd86.txt | 22 ++++++++++++++++++++++
 tests/test_unit_verifica_bot.py                  | 37 +++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task, quindi i loro conteggi non sono misurabili mentre si scrivono; riga di totale tolta. Base: origin/main 3cde8a5 (merge della #339).

## §3 GIT LOG --ONELINE (sessione)

```
17f062d fix(bot): «ad alta voce» / «a voce alta» non è una gravità (falso failure del bot #339 su 312cd86) (chat M2)
4b525ce chore(revisore): memoria review #688 — APPROVATO
37f6eaa chore(revisore): memoria review #687 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #687-M2 sul primo stage di 17f062d (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #687-M2. Diff staged: `scripts/bot_esito.py`, `tests/test_unit_verifica_bot.py` e `tests/dati_verifica_bot/verdetto_339_312cd86.txt`. Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 9), le parti di `reports/stato_progetto.md` su `bot_esito` e la coda della memoria.

**Cosa ho controllato nel diff**

1. `scripts/bot_esito.py:132`: la nuova regola `_ALTA_VOCE` riconosce il modo di dire «ad alta voce» / «a voce alta». Rischio cercato: che nasconda una gravità vera (cioè che un «no» diventi un «sì»). Esito: ok.
   - «alta» viene tolta solo se è scritta in minuscolo.
   - Tra le parole accetta solo spazi o tab. Un NBSP (spazio non separabile) o un a capo non vengono riconosciuti, quindi la riga resta bloccante.
   - Ho provato con una sonda:
     - «ad alta voce» dà MEDIA;
     - «a voce alta\tma alta» dà MEDIA;
     - «a  voce alta media» dà MEDIA;
     - «gravità alta: letto ad alta voce» dà MEDIA, perché la regola cerca su tutta la riga e trova anche l'altra «alta».
   - Con caratteri invisibili attaccati («ad ​alta voce», «ad alta​ voce», «a voce ⁠alta») il risultato è COMMENT: li ferma `_invisibili_su_gravita`, che a `scripts/bot_esito.py:408` scatta prima della pulizia.
2. `scripts/bot_esito.py:227`: la regola si applica solo alla ricerca della gravità scritta a parole, dopo `_GRAVITA_NEGATA` e `_BLOCCANTE_TECNICO`. Rischio cercato: che indebolisca anche le parole maiuscole o le gravità tra parentesi. Esito: ok.
   - La ricerca delle parole maiuscole (`_PAROLA_BLOCCANTE`) lavora su `finding`, non su `pulita`, quindi non cambia.
   - La ricerca tra parentesi (`_FINDING_GRAVITA`) lavora su `sezione`, quindi non cambia.
   - «V-1 — ad alta voce (MEDIA)» dà ancora MEDIA.
   - Sostituire il modo di dire con «voce» non può creare una gravità nuova, né far sparire l'id di un finding o una negazione.
3. `tests/test_unit_verifica_bot.py:1321`: test sul verdetto vero 312cd86 (APPROVE), 5 casi che devono restare bloccati e 3 casi del modo di dire. Rischio cercato: test che passano anche col codice sbagliato. Esito: ok.
   - Sul file intero: 591 passed.
   - Ho provato il codice sbagliato apposta (sostituzione tolta, in una copia): falliscono 4 test, il 339 e i 3 casi del modo di dire. Il quinto rosso, `test_invisibili_come_nel_gate`, dipende solo dal fatto che la copia sta fuori dal repo.
4. `tests/dati_verifica_bot/verdetto_339_312cd86.txt:10`: testo vero del bot, con «il testo viene letto ad alta voce». Esito: ok, corrisponde al caso del bug.

**Riserva**

- R-687-1-M2 (BASSA): «a voce alta» seguito da un nome viene tolto anche quando «alta» si riferisce al nome dopo. Esempio: «V-1 (BASSA) — comando a voce alta priorità» dà APPROVE. È un caso costruito apposta e resta il campo strutturato della gravità. Si può chiudere con un controllo che escluda le parole che seguono, ad esempio `(?![ \t]+(?:priorit|gravit|severit|rischi))`, oppure accettarlo dichiarandolo. Da tracciare in stato_progetto.md.

**Cosa NON ho verificato**

- Il comportamento nel workflow vero `verifica-bot` su GitHub: non si può riprodurre qui. Per questo la PR resta neutral (tocca la macchina del bot) e il merge spetta all'operatore.
- La nota fuori scope «R-682-1-M2 MEDIA … da decidere» senza parentesi: non toccata. È un difetto già esistente che blocca invece di lasciar passare, quindi non è pericoloso.

Memoria: riga #687-M2 aggiunta e committata (37f6eaa) con `scripts/commit_memoria_revisore.sh`.

File rilevanti:
- /home/user/Gas/scripts/bot_esito.py
- /home/user/Gas/tests/test_unit_verifica_bot.py
- /home/user/Gas/tests/dati_verifica_bot/verdetto_339_312cd86.txt
- /home/user/Gas/.claude/agents/memoria_revisore.md

Review #688-M2 (seconda review di #687-M2) sul commit 17f062d (verdetto integrale):

## VERDETTO: APPROVATO

Review #688-M2: seconda review della modifica #687-M2 sul diff staged (branch feat/voce-v12-m2). La riserva R-687-1-M2 è chiusa. Letture obbligatorie fatte: CLAUDE.md §5, la voce R-687 in reports/stato_progetto.md e la coda della memoria del revisore.

**Elementi del diff esaminati**
- `scripts/bot_esito.py:133` — `_ALTA_VOCE`: la seconda alternativa («a voce alta») ora viene tolta solo se dopo c'è un segno di punteggiatura o la fine della riga (`(?=[ \t]*(?:[.,;:)!?»"']|$))`, con re.M). Rischio esaminato: che re.M allarghi la prima alternativa, o che il filtro tolga una gravità vera. Prove fatte direttamente sulla regex:
  - re.M agisce solo su `^`/`$`, e la prima alternativa non li contiene: per lei non cambia nulla.
  - Restano bloccanti: «a voce alta priorità», «a voce alta — MEDIA» (il trattino non è nella lista, quindi resta bloccante: scelta prudente), «ad ALTA voce», «a voce altamente».
  - «a voce alta,gravità alta» diventa «voce,gravità alta», ma il secondo «alta» viene ancora preso dalla regola a parole, quindi resta bloccante.
  - «a voce alta\nMEDIA» → «voce\nMEDIA»: qui `$` con re.M scatta a fine riga, ma MEDIA resta visibile.
  - Esito: ok.
- `scripts/bot_esito.py:229` — il filtro si applica solo prima di `_FINDING_GRAVE_A_PAROLE` (la regola che cerca la gravità scritta a parole); le altre regole non cambiano. Esito: ok.
- `tests/test_unit_verifica_bot.py:1338` — il nuovo caso «comando a voce alta priorità» deve dare COMMENT (cioè bloccare); «Gas lo dice a voce alta, poi tace» deve dare APPROVE. Rischio esaminato: test che non distingue il codice giusto da quello sbagliato. Ho provato una versione sbagliata (mutante): tolto il lookahead, il caso «priorità» fallisce (1 failed, 592 passed). Codice poi ripristinato: lo staged è identico a prima. Esito: ok.
- `tests/dati_verifica_bot/verdetto_339_312cd86.txt:13` — il caso reale «letto ad alta voce» in V-1 (BASSA) passa ancora dalla prima alternativa, che non è cambiata. Esito: ok.

**Test:** `tests/test_unit_verifica_bot.py` dà 593 passed, rilanciato col venv indicato.

**Residuo accettato (nessuna riserva aperta):** il filtro toglie ancora «ad alta voce <nome>» e «"a voce alta" <nome>» tra virgolette (« o "), anche se un nome segue. Sono forme rare e innaturali in italiano, e la gravità strutturata del finding continua a contare.

**Rischio escluso:** non ho verificato il comportamento sul bot reale. Servirebbe il workflow `verifica-bot` su una PR con l'etichetta `verifica`, che non si riproduce in locale. Non ho nemmeno rilanciato le suite kernel/voce, perché il diff non tocca il motore runtime.

**Memoria:** riga #688-M2 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata a parte (4b525ce, «chore(revisore): memoria review #688 — APPROVATO»). Lo staged del diff è intatto: 3 file, +67/-1. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

Motore (gas.py, brains/, modules/) non toccato. `tests/test_unit_verifica_bot.py`: +11 test (verdetto vero 312cd86 → APPROVE; 6 casi che restano bloccati; 4 casi del modo di dire) — `593 passed` (prima 582). Mutanti: «sostituzione tolta» → 4 failed; «lookahead tolto» → 1 failed.

## §6 STATO CI

`gh` non autenticato nel cloud: check lette con l'integrazione GitHub. 37f6eaa, 4b525ce, 17f062d e il commit di fine-task che contiene questo file sono pushati insieme: run non ancora disponibile alla scrittura dell'handoff (la run testerà solo la testa). Su questa PR `verifica-bot` dà neutral (tocca la macchina del bot).

## §7 RISERVE APERTE

- Nessuna riserva aperta di questa fetta (R-687-1-M2 chiusa in #688-M2). Residuo accettato dal revisore: «ad alta voce <nome>» e «"a voce alta" <nome>» tra virgolette vengono ancora tolti.
- Noto, fuori scope: una citazione di riserva senza parentesi («R-682-1-M2 MEDIA …») fa bloccare il bot (falso failure, direzione sicura).
