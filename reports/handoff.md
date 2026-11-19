# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-19 — Presentazione clienti: tutte le avvertenze del catalogo d'esempio (PR #384)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #384 (https://github.com/Gasss23/Gas/pull/384) — numero e URL dalla risposta reale dello strumento GitHub (create_pull_request / pull_request_read), non da `gh` (in questo ambiente cloud `gh` è riservato alla ricerca). Presentazione e report; main (#383) portato nel branch con review #815 APPROVATO.
2. Prima di usare il PDF con i clienti, farlo vedere a un legale: proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia).
3. Inserire nel PDF nome dell'azienda, logo e contatti; confermare 23 mesi di storico e stop al 10%; decidere se citare «The Source Finance».

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — PDF definitivo (18/11)**: FATTA — f6630a72.
- **Fetta 2 — tutte le avvertenze del catalogo d'esempio (19/11)**: FATTA — d588f0bb. Piè di pagina con la frase del catalogo, pagina «Il rischio, per intero.» con 9 riquadri, nota sul confronto dei numeri in panoramica, drawdown «primo numero da leggere», «documento riservato».
- **Fetta 3 — merge di main (#383) nel branch per togliere i conflitti della PR #384**: FATTA — 27300187, conflitti solo nei report di sessione (presa la versione del branch), review #815 APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md                 |   1 +
 presentazione_clienti/Presentazione_Ecosistema.pdf | Bin 1408521 -> 1581422 bytes
 presentazione_clienti/build.py                     | 164 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------
 reports/diff_sessione.md                           |  14 +++++++++-----
 reports/handoff.md                                 | n/d
 reports/stato_progetto.md                          |   2 +-
 reports/ultimo_report.md                           |  20 ++++++++++++++------
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
27300187 merge: porta main (#383) nel branch per la PR #384; conflitti solo nei report di sessione (i nostri) — review #815 (chat practical-tesla) APPROVATO
d588f0bb presentazione clienti: tutte le avvertenze del catalogo d'esempio
2142a3db docs(fine-task): report della presentazione clienti definitiva (PR #384)
f6630a72 presentazione clienti: versione definitiva — schema semplice del matched trading, servizio 04 «Gruppo Privato», niente evidenziazioni
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun commit di questa sessione modifica il motore. Il merge 27300187 ha portato nel branch codice del motore già revisionato su main (#383: modules/voice/server.py, tests/test_unit_voice_server.py); il gate ha chiesto la review del merge. Verdetto integrale:

## VERDETTO: APPROVATO

Review #815 (chat practical-tesla). Oggetto: il merge in corso di origin/main 5cb2d2f8 (PR #383) nel branch claude/practical-tesla-ea9a9g (PR #384), sul diff staged.

**Prima della review ho letto**: CLAUDE.md (sez. 1, 5, 8, 10), reports/stato_progetto.md (in parte, per le sezioni dei finding) e la mia memoria. Ho applicato le lezioni sui merge: #497, #514, #531 e #1129 (diff in entrambe le direzioni), #502 (la base del merge si sposta), #484, #493 (numero della review), #1200 (niente script di commit della memoria mentre il merge è in corso).

**Prove raccolte**
- **Insiemi di file.** Base del merge 381f5d3d.
  - Il branch tocca solo presentazione_clienti/ (2 file) e reports/ (4 file).
  - Main tocca memoria, modules/voice/server.py, tests/test_unit_voice_server.py e gli stessi 4 report.
  - Nell'indice, rispetto a main, cambiano solo presentazione_clienti/ e reports/. Rispetto a HEAD cambiano solo memoria, server.py, il test e stato_progetto.
- **File del motore identici a main.** I blob nell'indice coincidono con quelli di main, quindi non hai modificato nessun file del motore:
  - modules/voice/server.py: 8c9ac070
  - tests/test_unit_voice_server.py: f50ee4aa
  - .claude/agents/memoria_revisore.md: 6b00e01f
- **I tre report presi dal branch sono identici a HEAD.** Sono reports/diff_sessione.md, reports/handoff.md e reports/ultimo_report.md. Le righe scartate di main sono il report di sessione della #383. Restano nella storia di git, e le sue riserve aperte (R-806-2 e R-807-1, entrambe BASSE) sopravvivono nella voce di stato_progetto.
- **stato_progetto.md è un'unione pura.** L'indice rispetto a HEAD aggiunge solo la riga portata da main. L'indice rispetto a main differisce solo per la voce del branch (CI 26.04 chiusa). Nessuna voce importata da main descrive come ancora aperta la CI che il branch chiude.
- **Nessun marcatore di conflitto** nell'indice.
- **Test.** tests/test_unit_voice_server.py: 246 passed, 3 failed. I 3 falliti dipendono dal container: manca il modulo `openai` (ModuleNotFoundError in gas.py:27), e la raccolta dell'intero repo dà 4 errori per la stessa causa. I file sono identici a main, e la CI di 5cb2d2f8 è verde (run 44357444098).

**Elementi del diff esaminati**
- `modules/voice/server.py:153` — `togli_parola_in_testa` toglie la parola di attivazione all'inizio della richiesta. Rischio esaminato: ciclo senza limite, richiesta svuotata, tool simulati, slicing della history. Il ciclo è fermo a 3 giri (`modules/voice/server.py:157`); se la richiesta resta vuota torna quella originale; la history non viene toccata. Esito: ok.
- `modules/voice/server.py:982` — la funzione si applica solo fuori dal seguito (`if not self._seguito()`), dopo i rami pausa, sola attivazione e frammento. Rischio esaminato: R-806-1, cioè il vocativo tolto nel seguito. È chiusa come nella #807. Esito: ok.
- `tests/test_unit_voice_server.py:1242` — il finto kernel ora registra anche il prompt (`dict(kw, _prompt=prompt)`). Rischio esaminato: rompere i test che leggono `turni`. Nell'esecuzione i test di `_voce_a_pezzi` passano. Esito: ok.
- `tests/test_unit_voice_server.py:2862` — test del vocativo che resta nel seguito, cioè il caso di R-806-1. Il mutante era già stato provato nella #807. Esito: ok.

**Rischi esclusi**
- Non ho rifatto i mutanti di `togli_parola_in_testa`: il codice è identico a main ed era già stato revisionato nella #806 e nella #807.
- I 3 test che dipendono da `openai` non li ho potuti eseguire qui: fa fede la CI.
- Non ho controllato il comportamento sul Mac.

**Note operative (non sono riserve)**
1. Per gate A e gate B, la tua prossima mossa: dopo il merge la base diventa 5cb2d2f8. Se metti nel commit di merge la mia riga di memoria, `.claude/agents/memoria_revisore.md` entra nel diff di sessione (origin/main...HEAD). Va quindi aggiunta al §2 di reports/handoff.md, altrimenti check_handoff (handoff-check) la segnala come omessa. Il §2 attuale è già vecchio nei numeri: dice build.py 132, oggi è 164 dopo d588f0bb. Rigeneralo dopo il merge.
2. Dopo il merge server.py e il test escono dal diff di sessione, che resta fuori dal perimetro di review. Il gate B controlla solo che le citazioni esistano a HEAD, e le righe citate sopra esistono.
3. Ho trovato reports/diff_sessione.md e reports/ultimo_report.md modificati solo nel working tree. Non sono modifiche mie, presumo siano tue in corso. Non fanno parte dell'indice revisionato.

**Memoria del revisore**: ho aggiunto la riga `#815 (chat practical-tesla) — 2026-11-19 — APPROVATO — …` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree. L'indice del merge è intatto: i blob staged sono ancora 6b00e01f, 8c9ac070 e f50ee4aa. Ho usato #815 perché su origin/claude/nifty-galileo-3k7kbm la chat CRM è già arrivata a #814. Non ho lanciato commit_memoria_revisore.sh (lezione #1200): la riga va messa in staging da te e la porta il commit di merge.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/ da parte di questa sessione (i file del motore arrivati col merge sono identici a main, CI di main verde: run 44357444098 secondo il revisore).

## §6 STATO CI

`gh run list` non usato (in questo ambiente cloud `gh` è riservato alla ricerca). Output reale dello strumento GitHub `actions_list` (list_workflow_runs, workflow ci.yml, branch claude/practical-tesla-ea9a9g) alla scrittura:

```
CI  run 44346944386  #1959  push  completed/success  sha 2142a3db  https://github.com/Gasss23/Gas/actions/runs/44346944386
CI  run 44346826214  #1958  push  completed/success  sha f6630a72  https://github.com/Gasss23/Gas/actions/runs/44346826214
```

Mappatura commit→run:
- f6630a72 → run 44346826214: success.
- 2142a3db → run 44346944386: success.
- d588f0bb, 27300187 → nessuna run su questi SHA (non ancora pushati: partono col push del commit di fine-task, che testa solo l'albero di testa).
- commit di fine-task (questo file) → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna nuova. Restano in reports/stato_progetto.md: verifica esterna #380 V-2 BASSA e V-4 COSMETICA; dalla #383 (main) R-806-2 e R-807-1 BASSE.
