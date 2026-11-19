# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-19 — Presentazione clienti tolta dal repo (PR #385)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #385 (https://github.com/Gasss23/Gas/pull/385) — numero e URL dalla risposta reale dello strumento GitHub (create_pull_request), non da `gh` (in questo ambiente cloud `gh` è riservato alla ricerca). Richiesta dell'operatore: «toglielo da github direttamente».

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — togliere la presentazione clienti dal repo**: FATTA — 5e006dd2. PDF e sorgenti consegnati all'operatore in chat (zip) prima della rimozione; file locali con i contatti cancellati dal container.
- **Fetta 2 — repo privato**: SALTATA — l'operatore ha scelto di togliere il PDF invece di rendere privato il repo.
- **Fetta 3 — riserve del bot #385 su 2add2b71 (V-1 BASSA, V-2 COSMETICA)**: FATTA — a362b16f, voce «repo pubblico» di stato_progetto riscritta.
- **Fetta 4 — merge di main (#381 CRM) nel branch (conflitti nei report)**: FATTA — d088d4a5, review #816 APPROVATO.
- **Fetta 5 — riserve del bot #385 su 351bd668**: FATTA nel commit di fine-task — V-1 `presentazione_clienti/` nel .gitignore principale; V-2 conflitto con main risolto (fetta 4); V-3 vedi §7; V-4 voci chiuse spostate in stato_storico.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md               |    2 +
 .gitignore                                       |    4 ++
 presentazione_clienti/.gitignore                 |    4 --
 presentazione_clienti/PDF servizi ecosistema.pdf |  Bin 1440250 -> 0 bytes
 presentazione_clienti/build.py                   |  819 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 presentazione_clienti/render.js                  |   26 ---------
 presentazione_clienti/titoli_svg.json            |   10 ----
 reports/diff_sessione.md                         |   50 ++++-------------
 reports/handoff.md                               | n/d
 reports/stato_progetto.md                        |    6 +--
 reports/stato_storico.md                         |    4 ++
 reports/ultimo_report.md                         |   59 ++++----------------
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
d088d4a5 merge: porta main (#381 CRM) nel branch per la PR #385; conflitti solo nei report di sessione (i nostri) — review #816 (chat practical-tesla) APPROVATO
351bd668 docs(fine-task): handoff aggiornato con le riserve del bot #385 (PR #385)
a362b16f docs(stato): voce «repo pubblico» aggiornata dopo la rimozione della presentazione (bot #385 V-1/V-2)
2add2b71 docs(fine-task): report — presentazione clienti tolta dal repo (PR #385)
5e006dd2 presentazione clienti: tolta dal repo (decisione dell'operatore)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun commit di questa sessione modifica il motore. Il merge d088d4a5 ha portato nel branch codice del motore già revisionato su main (#381); il gate ha chiesto la review del merge. Verdetto integrale:

## VERDETTO: APPROVATO

Review #816: merge in corso di origin/main 12633cb0 (PR #381, CRM) nel ramo claude/practical-tesla-ea9a9g (PR #385). HEAD 351bd668, base del merge 491c7ff3.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 10), reports/stato_progetto.md (letto a pezzi), .claude/agents/memoria_revisore.md. Ho applicato le lezioni sui merge dell'ottobre-novembre (righe 484, 502, 514, 531, 715, 792, 1129, 1200 e 1611 della memoria).

**Integrità del merge (verificata a macchina)**
- Base→HEAD: il ramo tocca solo i 5 file di presentazione_clienti/ (tutti cancellati) e 4 report. Nessun file del perimetro di review.
- `git diff --cached MERGE_HEAD --name-status`: restano solo il delta del ramo, cioè 5 cancellazioni D di presentazione_clienti/ e la modifica M di reports/{diff_sessione,handoff,stato_progetto,ultimo_report}.md. Non ci sono altre differenze da main.
- Blob per blob, sui 28 file in staging: 27 coincidono con `MERGE_HEAD:<path>`. Tra questi ci sono gas.py, brains/model_ids.py, tutti i modules/crm/*, .github/workflows/ci.yml, tests/conftest.py, tests/test_unit_crm.py, tests/test_unit_kernel.py, tests/test_unit_notte.py, .gitignore, CLAUDE.md, reports/roadmap.md, reports/crm/* e la memoria del revisore. L'unico diverso è reports/stato_progetto.md, ed è atteso.
- reports/stato_progetto.md: ho rifatto il merge a tre vie con `git merge-file` (base/HEAD/MERGE_HEAD), 0 conflitti, e il risultato è identico byte per byte all'indice. Le voci della #381 ci sono tutte: l'intestazione al 17/11 (riga 4), «CI rossa» (riga 9), «CRM fetta 2» (riga 10), «CRM fetta 1» (riga 11). Ci sono anche le due voci del ramo (righe 387-388). Nessuna voce importata da main dice ancora aperta la presentazione clienti.
- I 3 report di sessione nell'indice sono il blob di HEAD, come dichiarato. Non ci sono marcatori di conflitto e `git diff --cached --check` è pulito.
- Memoria del revisore nell'indice = main. Contiene anche #815 del ramo, perché il ramo non l'aveva modificata dalla base.

**Elementi del diff esaminati**
- `gas.py:4609` — la riflessione con dati di clienti usa `MODEL_CLAUDE_CLIENTI`; se il modello non è Opus viene rimandata e registrata nel log, invece di passare a un modello minore. Rischio esaminato: fallback silenzioso a un modello debole o gratuito → ok, blob uguale a main e T117e PASS.
- `gas.py:5643` — durante il turno, con dati di clienti nella finestra, il forte chiama solo Opus. Se il modello configurato non è Opus il turno si ferma con un messaggio esplicito, e il pin pieno va solo al rung Opus (`gas.py:5663`). Rischio esaminato: crash o fuga di dati verso modelli minori → ok, T117d PASS. Il ciclo resta limitato a 10 iterazioni (`gas.py:5624`) e la finestra passa da `_get_window` (`gas.py:2181`). Nelle righe aggiunte non c'è slicing `[-N:]` della storia (grep vuoto).
- `brains/model_ids.py:13` / `brains/model_ids.py:17` — Opus fisso e `e_modello_opus` che controlla se «opus» compare nel nome del modello (senza distinguere maiuscole). Rischio esaminato: id vuoto o None → ok, `(model or "")` lo copre.
- `.github/workflows/ci.yml:235` — nuovo step della suite CRM con `if: always()` e `pipefail`. Rischio esaminato: indebolimento della CI → ok, è solo un'aggiunta e non ci sono `paths-ignore`.
- `tests/conftest.py:30` — fixture autouse che nasconde ai test pytest il DB vero dei clienti (`delenv GAS_CRM_DB` + `_RADICE_REPO` finto). Rischio esaminato: test che leggono dati reali → ok.

**Esecuzione** (copia di lavoro = indice; ho installato requirements.txt nell'ambiente): `python3 tests/test_unit_kernel.py` → 1191 PASS, 0 FAIL. `pytest tests/test_unit_crm.py tests/test_unit_notte.py` → 320 passed. Nessun file è stato sporcato.

**Rischi esplicitamente esclusi**
- Non ho rifatto la review del contenuto della #381 (CRM, server, dashboard), perché è già stata revisionata (#803–#814-CRM) e mergiata: ho verificato solo che i blob siano identici a main.
- Non ho eseguito tests/test_unit_web_browser.py né le altre suite pytest, e non ho verificato lo stato della CI su GitHub.
- Non ho verificato il comportamento sul Mac o sul VPS: non è riproducibile qui.

**Note operative per il commit successivo (non sono riserve sul merge)**
1. Gate B: dopo il merge la base della sessione diventa 12633cb0 e il diff di sessione resta fuori perimetro. Il gate quindi non chiede il minimo di 2 citazioni, ma verifica ogni path:riga a HEAD. Le citazioni qui sopra (gas.py, brains/model_ids.py, ci.yml, conftest.py) esistono a HEAD e passano. Non citare mai con :riga i file cancellati di presentazione_clienti/: il gate fallirebbe con «file non trovato a HEAD».
2. Il §2 dell'handoff (diff --stat) va rigenerato dopo il merge: la base si è spostata. L'insieme dei path non cambia, quindi il gate A regge, ma i conteggi vanno rimisurati.
3. In stato_progetto.md l'intestazione «Ultimo aggiornamento» è ferma al 17/11 (CRM) e non cita il 19/11. La voce «🔴 CI rossa per tutti i rami dal 17 nov», arrivata da main, va riverificata con la CI della PR #385: se è verde, aggiornarla. Erano già così prima del merge, non li ha introdotti il merge.

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nella copia di lavoro, la riga contatore «#816 (chat practical-tesla) — 2026-11-19 — APPROVATO — …» e una lezione nuova sui merge con delta del ramo fatto solo di cancellazioni. L'indice non l'ho toccato: il blob staged della memoria è ancora e547c7d6, uguale a main. commit_memoria_revisore.sh non l'ho lanciato. La modifica resta fuori dallo staging e va portata nel commit successivo.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/ da parte di questa sessione (i file del motore arrivati col merge sono identici a main; il revisore ha eseguito test_unit_kernel.py 1191 PASS e test_unit_crm/notte 320 passed).

## §6 STATO CI

`gh run list` non usato (in questo ambiente cloud `gh` è riservato alla ricerca). Stato dei check della PR #385 letto con lo strumento GitHub (pull_request_read get_check_runs) sull'head 351bd668 alla scrittura: handoff-check success, verifica-bot success (APPROVATO CON RISERVE, solo BASSE/COSMETICHE), unit-suite in corso (run 44608049759).

Mappatura commit→run:
- 5e006dd2 → nessuna run su questo SHA (pushato insieme a 2add2b71).
- 2add2b71 → run 44606183913: success.
- a362b16f → nessuna run su questo SHA (pushato insieme a 351bd668).
- 351bd668 → run 44608049759: in corso alla scrittura.
- d088d4a5 → nessuna run su questo SHA (sarà pushato insieme al commit di fine-task).
- commit di fine-task (questo file) → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Bot #385 su 2add2b71: V-1 BASSA e V-2 COSMETICA chiuse in a362b16f.
- Bot #385 su 351bd668: V-1 (.gitignore), V-2 (conflitto con main), V-4 (storico) chiuse in questa sessione; V-3: la riserva «numeri del PDF clienti non verificati da nessun gate» (agente-#380 V-3, ripresa come bot-#384 V-2 sul commit 45f92c51) DECADE per il repo, perché il PDF non c'è più; fuori dal repo la revisione legale l'ha fatta l'operatore (affermazione dell'operatore). La riserva sulla durata del ciclo era bot-#384 V-2 sul commit d83a764f (stesso numero, verdetto diverso): decade con build.py.
- In stato_progetto.md: repo pubblico (i due commit con i contatti raggiungibili per SHA fino alla richiesta al supporto GitHub); riserve del fix sandbox (agente-#380 V-2 e V-4, bot-#380 V-1 e V-2); R-806-2 e R-807-1 BASSE.
