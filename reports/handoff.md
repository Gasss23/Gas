# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-20 — CRM fetta 7: note basse della PR #386, R-821-1 e finding del bot sulla PR #387 (b098adf1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #387 (https://github.com/Gasss23/Gas/pull/387). L'operatore ha già dato il via in chat il 20-11 («ok mergia quando è tutto verde»): la mergia l'agente con CI verde e bot senza finding ALTA/MEDIA sul nuovo head.
2. Password delle copie cifrate nel `.env` del Mac (`GAS_CRM_BACKUP_PASSWORD`), salvata anche nel gestore di password; poi `pip install -r requirements.txt`.
3. Verificare che la cartella di Gas sia `~/Gas`, fuori da Scrivania e Documenti sincronizzate con iCloud.
4. Secondo passaggio nella chat claude.ai col link della PR #387 (riservatezza delle copie dei clienti).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 7 — note basse sull'ultimo commit della PR #386 (8a107c47) e R-820-1**: FATTA, commit 99e0dcb8. Review #821-CRM APPROVATO CON RISERVE (R-821-1 BASSA).
  - Bot V-1 (guida), V-2 (indicatore se fallisce la copia locale), V-3 (temporaneo del ripristino).
  - Verifica esterna #386 V-1 (disco non collegato), V-3, V-4 (file di lavoro come collegamento pendente), V-5 (copia locale rovinata); residuo `.prova-*.tmp`; R-820-1 (prova all'avvio con tempo massimo).
- **Correzione #822 — R-821-1 e punto di mount vuoto in `/Volumes`**: FATTA, commit 4a442c4f. Review #822-CRM APPROVATO.
- **Correzione #823 — V-1 MEDIA e V-2 del bot sulla PR #387 (b098adf1)**: FATTA, commit 2b4d32f2. Review #823-CRM APPROVATO.
  - V-1: un permesso negato sulla cartella delle copie (PermissionError da `is_dir` fuori dal try) rompeva la copia e faceva dire «ATTIVA» all'avvio.
  - V-2: `_integro` creava un file vuoto su un percorso inesistente; ora apre in sola lettura.
  - Chiusa anche la nota minore del revisore #822 (collegamento simbolico verso `/Volumes`, «/volumes» minuscolo).
- **Regola in CLAUDE.md §10** (doc): non fermarsi ad aspettare il merge (operatore, 20-11).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 CLAUDE.md                          |   1 +
 modules/crm/__main__.py            |   9 ++------
 modules/crm/copia_cifrata.py       |  98 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 modules/crm/server.py              |  47 ++++++++++++++++++++++++--------------
 reports/crm/guida.md               |   4 ++--
 reports/diff_sessione.md           |  25 ++++++++++----------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  62 ++++++++++++++++++++------------------------------
 tests/test_unit_crm.py             | 151 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base della sessione: 0aa26672 (origin/main, dopo il merge della PR #386).

## §3 GIT LOG --ONELINE (sessione)

```
2b4d32f2 fix(crm): permesso negato sulla cartella delle copie non rompe più la copia né dà ATTIVA all'avvio; controllo di integrità in sola lettura (V-1 MEDIA e V-2 del bot su #387) — review #823 APPROVATO
5b815013 chore(revisore): memoria review #823 — APPROVATO
4a442c4f fix(crm): indicatore rosso se fallisce la copia sul Mac anche a copia esterna spenta; disco esterno con punto di mount vuoto riconosciuto (R-821-1) — review #822 APPROVATO
47188b59 chore(revisore): memoria review #822 — APPROVATO
b098adf1 docs(fine-task): handoff — PR #387 aperta con l'etichetta verifica
5f9d3c8c docs(fine-task): CRM fetta 7 — note basse della PR #386 chiuse, review #821; regola «non fermarsi ad aspettare il merge»
99e0dcb8 fix(crm): copie fuori dal Mac più solide — disco non collegato, copia locale rovinata, temporaneo del ripristino esclusivo, avvio con tempo massimo, indicatore anche se fallisce la copia locale
1307a80f chore(revisore): memoria review #821 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #821-CRM (commit 99e0dcb8)

## VERDETTO: APPROVATO CON RISERVE

Review #821-CRM sul diff staged (4 file, +162/−31). Ramo ripartito da main 0aa26672 (PR #386 mergiata).

Chiude le note BASSE del bot e della verifica esterna su 8a107c47 e la mia R-820-1. Resta una sola riserva BASSA: con la copia esterna spenta, un fallimento della copia locale non si vede (R-821-1).

**Verifiche rifatte da me:**
- Suite CRM: 133 passed. mypy pulito su modules/crm.
- Fail-before su main 0aa26672 col file di test nuovo: falliscono i 2 test nuovi, 131 passano.
- Tre prove a mano (risultati sotto):
  1. disco non collegato;
  2. cartella che non risponde;
  3. copia locale fallita con la copia esterna spenta.
- Kernel non toccato. Nessuno slicing della history, nessuna simulazione di tool.

### Riserva

**1. R-821-1 — BASSA — con la copia esterna spenta, un fallimento della copia locale non si vede.**
- **Prova:** senza password, cioè con la copia esterna spenta, `_copia_giornaliera` (`modules/crm/server.py:297`) segna l'esito come `{'spenta': True, 'ok': None, 'motivo': 'la copia sul Mac non è riuscita…'}`.
- **Cosa vede l'operatore:** la dashboard mostra «☁ copia spenta», non il rosso. Il fallimento della copia locale compare solo nel title e nel log, e non parte nessun avviso.
- **Perché pesa poco:** con la copia esterna attiva, cioè il caso scelto dall'operatore, il fallimento invece si vede e parte l'avviso: il V-2 del bot è chiuso.
- **Rimedio:** un campo a parte per la copia locale, o il rosso anche quando la copia esterna è spenta.

### Elementi del diff esaminati

- **`modules/crm/copia_cifrata.py:107` — la cartella delle copie si crea solo se esiste quella che la contiene** (niente più `parents=True`), sia nella prova sia nella copia.
  - Prova a mano: con la cartella su un disco «non collegato», l'avvio dice «NON FUNZIONA (… non c'è (disco non collegato?) …)» e non viene creata nessuna cartella sul disco del Mac.
  - Rischio esaminato: una copia che «riesce» senza uscire dal Mac.
  - Esito: ok.
- **`modules/crm/copia_cifrata.py:198` — `_integro` sulla copia locale prima di cifrare.**
  - Rischio esaminato: una copia locale rovinata che sostituisce la copia buona del giorno, visto che il nome è per giorno. Ora la copia del giorno resta quella di prima, e il test lo controlla.
  - Esito: ok.
- **`modules/crm/copia_cifrata.py:288` — temporaneo del ripristino unico e creato in esclusiva.**
  - Con O_EXCL l'apertura fallisce anche su un collegamento simbolico, anche pendente, quindi non scrive mai dentro un altro file.
  - Su `FileExistsError` il file non è nostro e il `finally` non lo tocca.
  - Il controllo dei file di lavoro ora vede anche i collegamenti pendenti (`modules/crm/copia_cifrata.py:275`).
  - I `.prova-*.tmp` più vecchi di un'ora vengono tolti (`modules/crm/copia_cifrata.py:235`).
  - Esito: ok.
- **`modules/crm/copia_cifrata.py:146` — `esito_all_avvio`:** la prova gira in un thread daemon con tempo massimo, e `serve` stampa solo la riga che ne esce (`modules/crm/__main__.py:131`).
  - Prova a mano con una prova che dura 30 s: «NON VERIFICATA» dopo 1,0 s, e il server parte.
  - Chiude R-820-1. Il thread bloccato resta daemon e non trattiene l'uscita del processo.
  - Esito: ok.
- **`modules/crm/server.py:297` — `_copia_giornaliera` e `_segna_copia`:** copia locale nel guardiano, copia esterna in un thread a parte (resta valida R-815-4).
  - Se la copia locale fallisce, l'indicatore passa a «NON riuscita» e parte l'avviso, ma solo con la copia esterna attiva (vedi R-821-1).
  - L'avviso non contiene dati dei clienti.
  - Esito: ok, salvo R-821-1.
- **`tests/test_unit_crm.py:1648` e `tests/test_unit_crm.py:1708`:** coprono disco non collegato, copia locale rovinata, `.prova` vecchia, collegamento simbolico al posto del temporaneo, journal pendente, prova lenta, copia locale fallita.
  - Sul codice di main falliscono entrambi.
  - Esito: ok.

### Rischi esplicitamente NON verificati

- Su macOS, a volte un punto di mount resta in `/Volumes` come cartella vuota anche a disco staccato. In quel caso `_genitore_assente` vedrebbe la cartella «che la contiene» e la copia finirebbe sul disco del Mac. Qui non è riproducibile, e il default (iCloud Drive) non è toccato. Per un disco esterno si potrebbe controllare che il percorso sia davvero un mount (`os.path.ismount`).
- Comportamento vero di iCloud Drive e dei permessi di macOS: non c'è un Mac qui.
- Documenti fuori stage (guida, frase di CLAUDE.md §10): non letti.

### Note

- Restano aperte dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Riga contatore #821-CRM aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (commit 1307a80f). Il diff staged è intatto (4 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #822-CRM (commit 4a442c4f)

## VERDETTO: APPROVATO

Review #822-CRM sul diff staged (3 file, +45/−4), sopra b098adf1 (head della PR #387). Chiude la mia R-821-1 e il rischio che nel #821 avevo lasciato non verificato: il punto di mount vuoto in /Volumes.

**Verifiche rifatte da me:**
- Suite CRM: 135 passed. mypy pulito su modules/crm.
- Fail-before: con il codice di b098adf1 e il file di test nuovo falliscono i 2 test nuovi (133 passati).
- Kernel non toccato. Nessuno slicing della history, nessuna simulazione di tool.

**Elementi del diff esaminati:**
- `modules/crm/server.py:306` — se la copia LOCALE fallisce, `_segna_copia(stato, None, False, …)`: l'indicatore diventa rosso e parte l'avviso anche con la copia esterna spenta.
  - Rischio esaminato: lo stato «falso rosso» che resta dopo. Alla copia locale successiva riuscita, `_copia_esterna` ricalcola `motivo_spenta()` e rimette lo stato reale (spenta oppure ok).
  - Test: `tests/test_unit_crm.py:1720`, senza password: ok False, spenta False, motivo presente, 1 avviso.
  - Esito: ok.
- `modules/crm/copia_cifrata.py:108` — `_genitore_assente`: dopo il controllo della cartella che la contiene, per un percorso sotto `/Volumes` richiede che il primo livello sia un mount vero (`os.path.ismount`, `modules/crm/copia_cifrata.py:121`).
  - Rischio esaminato: un disco staccato il cui punto di mount resta come cartella vuota sul disco del Mac. Ora la prova dice «non è collegato» e non crea nessuna cartella.
  - Fuori da /Volumes (iCloud Drive) non cambia nulla: `relative_to` fallisce e la funzione ritorna None.
  - Un `/Volumes/Macintosh HD`, che è un collegamento al disco del Mac, viene rifiutato: è il verso giusto, quella non è una copia fuori dal Mac.
  - Test: `tests/test_unit_crm.py:1734`, con `VOLUMI` sostituita da una cartella temporanea; con `ismount` vero la prova riesce.
  - Esito: ok.

**Nota minore, non classificata come riserva:** il controllo del mount guarda il percorso così com'è, senza risolverlo (`modules/crm/copia_cifrata.py:118`). Un collegamento simbolico che porta dentro /Volumes (per esempio `~/Backup` → `/Volumes/Disco/…`), oppure «/volumes» scritto in minuscolo su un disco che non distingue maiuscole e minuscole, salta il controllo. Basterebbe risolvere il percorso prima di `relative_to`.

**Rischio esplicitamente NON verificato:** il comportamento vero di `os.path.ismount` sui dischi esterni di macOS (APFS, exFAT, dischi di rete montati in /Volumes). Qui non c'è un Mac; il test sostituisce `ismount`.

**Note:**
- Questo commit resta locale fino al merge della #387, poi va in una PR nuova, come previsto.
- Restano aperte dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Ho aggiunto la riga contatore #822-CRM in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit 47188b59). Il diff staged è intatto (3 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #823-CRM (commit 2b4d32f2)

## VERDETTO: APPROVATO

Review #823-CRM sul diff staged (2 file, +90/−21), sopra 4a442c4f. Chiude la V-1 MEDIA del bot su b098adf1 (PR #387), la sua V-2 e la mia nota minore del #822; non ho trovato riserve nuove.

**Verifiche rifatte da me:**
- Suite CRM: 136 passed. mypy pulito su modules/crm.
- Fail-before: col codice di 4a442c4f e il file di test nuovo, `test_v1_bot387_permesso_negato_non_rompe_la_copia` fallisce (1 failed, 135 passed).
- Prove a mano su `_integro`, la funzione che controlla se il database è integro:
  - percorso con spazi, `#` e `?` nel nome → True, quindi l'URI viene codificato correttamente;
  - percorso inesistente → False, e nessun file viene creato;
  - collegamento simbolico che punta a se stesso → False, nessuna eccezione.
- Kernel non toccato. Nessuno slicing della history, nessuna simulazione di tool.

**Elementi del diff esaminati:**
- `modules/crm/copia_cifrata.py:108` — `_genitore_assente` ha tutto il corpo in try/except OSError (`modules/crm/copia_cifrata.py:129`), quindi un permesso negato su `is_dir` diventa un motivo leggibile e non un'eccezione. Il controllo del mount usa il percorso risolto (`modules/crm/copia_cifrata.py:121`) e confronta i primi livelli senza badare a maiuscole e minuscole, sia per la destinazione sia per `VOLUMI`.
  - Rischi esaminati: una PermissionError che fa fallire `copia_fuori`, che deve invece non sollevare mai; un collegamento simbolico verso /Volumes, o «/volumes» minuscolo, che saltava il controllo (la mia nota #822).
  - `os.path.ismount` gestisce già da sé i propri errori.
  - Con il percorso risolto, `/Volumes/Macintosh HD/…` porta al disco del Mac e viene accettato come una qualunque cartella del Mac. È coerente: il controllo serve a scoprire i dischi staccati, non a vietare le cartelle locali.
  - Esito: ok.
- `modules/crm/copia_cifrata.py:221` — in `copia_fuori` il controllo della cartella e quello di integrità della copia locale ora stanno DENTRO il try. A quel punto `tmp` vale ancora None, quindi il `finally` non tocca niente. Così una copia fallita aggiorna di nuovo l'indicatore in dashboard e manda l'avviso.
  - Esito: ok.
- `modules/crm/copia_cifrata.py:172` — `esito_all_avvio` parte da «prova non conclusa per un errore inatteso», e il thread intercetta ogni eccezione. Solo una prova che finisce senza errori dà ATTIVA.
  - Rischio esaminato: un «ATTIVA» stampato dopo un'eccezione nel thread.
  - Esito: ok.
- `modules/crm/copia_cifrata.py:278` — `_integro` apre il database in sola lettura (URI `mode=ro`), quindi un percorso inesistente non diventa un file vuoto. I tre chiamanti (copia locale appena fatta, `.ripristino.tmp` appena scritto, `dest` dopo il posizionamento) non hanno journal rimasti: il caso del journal è già rifiutato prima.
  - Esito: ok.
- `tests/test_unit_crm.py:1750` — copre permesso negato, prova che solleva un'eccezione, `_integro` su un percorso inesistente e collegamento simbolico verso un disco non montato.
  - Esito: ok.

**Rischio esplicitamente NON verificato:** il comportamento vero di macOS con TCC che nega `~/Library/Mobile Documents`. Qui il caso è simulato sostituendo `Path.is_dir`. Su Python 3.11 della CI `Path.resolve` passa da `os.path.realpath` e non solleva sui collegamenti ad anello; l'ho provato solo con Python 3.13 del container.

**Note:**
- Questi commit vanno sulla PR #387 insieme al #822, come previsto.
- Restano aperte dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Ho aggiunto la riga contatore #823-CRM in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit 5b815013). Il diff staged è intatto (2 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_crm.py`:** 131 su main 0aa26672 → 133 (#821) → 135 (#822) → 136 passed (#823).
  - #821: `test_ve386c_note_del_terzo_giro`, `test_v2_bot386c_copia_locale_fallita_si_vede` falliscono sul codice di main (2 failed, 131 passed).
  - #822: i 2 test `test_r821_*` falliscono sul codice di b098adf1 (133 passati).
  - #823: `test_v1_bot387_permesso_negato_non_rompe_la_copia` fallisce sul codice di 4a442c4f (1 failed, 135 passed).
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.
- **mypy:** 0 errori in `modules/crm`.

## §6 STATO CI

`gh run list` non usato: in questa sessione cloud GitHub si interroga con gli strumenti MCP.
- Head precedente della PR #387, b098adf1: handoff-check success (run 44745012051); unit-suite in corso alla scrittura dell'handoff; verifica-bot failure (run 44745017566: verdetto del bot BOCCIATO per V-1 MEDIA, chiusa da 2b4d32f2).
- Mappatura commit→run:
  - `1307a80f`, `99e0dcb8`: nessuna run su questi SHA (pushati insieme a 5f9d3c8c; l'albero testato è quello di 5f9d3c8c).
  - `5f9d3c8c`: run CI 44744925231 (superata dal push di b098adf1); verifica-bot 44744965200 annullata.
  - `b098adf1`: run CI 44745012051, verifica-bot 44745017566 (vedi sopra).
  - `47188b59`, `4a442c4f`, `5b815013`, `2b4d32f2`: run non ancora disponibile alla scrittura dell'handoff. Saranno pushati insieme al commit di fine-task che contiene questo file: una sola run testerà l'albero di testa.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **Rischi non verificabili qui (revisori #822 e #823, non c'è un Mac):** comportamento vero di `os.path.ismount` sui dischi esterni di macOS; blocco dei permessi di macOS (TCC) su `~/Library/Mobile Documents`, simulato nei test.
- **Chiuse in questa sessione:**
  - V-1/V-2/V-3 del bot su 8a107c47 (V-4 era documentale); V-1/V-3/V-4/V-5 della verifica esterna #386 (3° giro, https://github.com/Gasss23/Gas/pull/386#issuecomment-7026471536); R-820-1 (#821);
  - R-821-1 e il rischio del punto di mount vuoto (#822);
  - V-1 MEDIA e V-2 del bot su b098adf1, nota minore del revisore #822 (#823);
  - V-1/V-2/V-3 della verifica esterna su #387 (https://github.com/Gasss23/Gas/pull/387#issuecomment-7040844433): chiuse da #822 e #823.
- **Ancora aperte da prima:** R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4 (vedi `reports/stato_progetto.md`).
