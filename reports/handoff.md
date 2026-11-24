# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-24 — Dashboard del CRM sempre accesa sul Mac

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #403 (https://github.com/Gasss23/Gas/pull/403). Script per il Mac e guida; il merge di main porta solo codice già su main.
2. Sul Mac, una volta sola dopo il merge: `cd ~/Gas && git pull && bash scripts/crm/installa.sh`; controllare che l'ultima riga dica «Copia cifrata giornaliera fuori dal Mac: ATTIVA».
3. Da decidere (R-852M-2): mettere `scripts/crm/` nel perimetro di review come `scripts/voce/`.
4. Dalla chat Voce (#400): controllare nel `.env` del Mac che non ci sia una vecchia `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8`.

---

## §1 SCOPE & ESITO FETTE

- **Dashboard del CRM sempre accesa** (richiesta dell'operatore: «vorrei mettere da qualche parte questa dashboard… che non dipenda da Claude o dall'IA… accessibile anche offline e in modo facile»): FATTA (5d5911b4). LaunchAgent `com.gas.crm`, `scripts/crm/installa.sh` e `spegni.sh`, icona «CRM Gas» sulla Scrivania (il token non finisce in nessun file), guida aggiornata.
- **Note del bot su 51d446c4** (APPROVATO CON RISERVE, V-1 MEDIA): FATTE (20791587). V-1 attesa dopo il bootout e 3 tentativi di bootstrap; V-2 cartella con soli caratteri sicuri; V-3 servizio tolto se la dashboard non parte e stop se `GAS_CRM_BIND` non è 127.0.0.1; V-4 `spegni.sh` toglie l'icona; guida (login da rifare dopo un riavvio, controllo della copia cifrata).
- **Note del bot su 67f4dc34** (APPROVATO CON RISERVE, V-1 MEDIA): FATTE. V-1 registro non bufferizzato (`PYTHONUNBUFFERED=1`) e attesa della riga della copia cifrata di questo avvio; V-2 uscita con 0; V-3 controllo del `.env` con `env -i` (come lo vedrà launchd) ed errori distinti.
- **Merge di main (PR #398, #399, #400)** (f4381a2e): FATTO, review #852-MERGE APPROVATO CON RISERVE. Codice identico a main; report del ramo tenuti; decisioni e riserve della #400 (anche quelle dell'ultimo verdetto del bot, R-852M-1) in `reports/stato_progetto.md`.
- **Prova su un Mac vero** (launchctl, Scrivania, iCloud sotto launchd): SALTATA — il Mac non è raggiungibile da qui.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 reports/crm/guida.md               |   2 ++
 reports/diff_sessione.md           |  18 +++++++++---------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  40 ++++++++++++++--------------------------
 scripts/crm/com.gas.crm.plist      |  36 ++++++++++++++++++++++++++++++++++++
 scripts/crm/installa.sh            | 134 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 scripts/crm/spegni.sh              |  10 ++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
71a7f12c fix(crm): note del bot su 67f4dc34 — registro non bufferizzato (esito della copia cifrata visibile), installer esce con 0, controllo del .env con l'ambiente pulito di launchd
67f4dc34 docs(fine-task): note del bot sulla #403 corrette, merge di main (#398-#400), review #852-MERGE
20791587 fix(crm): note del bot sulla #403 — attesa dopo il bootout e 3 tentativi di bootstrap, cartella con soli caratteri sicuri, servizio tolto se la dashboard non parte, stop se GAS_CRM_BIND non è 127.0.0.1, spegni toglie l'icona
f4381a2e Merge origin/main (PR #398, #399, #400) nel ramo della PR #403 — review #852-MERGE APPROVATO CON RISERVE
51d446c4 docs(fine-task): CRM sempre acceso sul Mac — report, handoff e stato (PR #403)
5d5911b4 feat(crm): dashboard sempre accesa sul Mac — LaunchAgent com.gas.crm, installa/spegni e icona sulla Scrivania
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore nel diff di sessione (solo `scripts/crm/`, report e memoria del revisore). Il merge di main (f4381a2e) portava codice già su main ed è stato revisionato; verdetto integrale incollato:

## VERDETTO: APPROVATO CON RISERVE

Review #852-MERGE. Oggetto: merge in corso (non committato) di origin/main af0215de, che porta le PR #398, #399 e #400, nel ramo claude/nifty-galileo-3k7kbm (PR #403, HEAD 51d446c4). Prima della review ho letto CLAUDE.md (§5, §8, §10), `reports/stato_progetto.md` (ricerca mirata) e la memoria. Ho controllato anche che origin/main non si sia mosso dopo il fetch: è ancora af0215de.

**Elementi del diff esaminati**
- `gas.py:7347`: comando `sottofondo-riprendi` portato dalla #398. Rischio: che il merge l'abbia alterato. Ho confrontato col diff indice contro origin/main tutto il perimetro (ogni riga di `.claude/perimetro_review.txt`): risultato vuoto. Esito: ok.
- `modules/notte/notte.py:927`: `_ERRORI_ESTERNI` e `_ko_esterno` (`modules/notte/notte.py:945`) della #399, file identico a main. Esito: ok.
- `clients/voice/ascolto.py:165`: `SOGLIA_VERIFICA_PREDEFINITA = 0.6` della #400, file identico a main. Esito: ok. Collegata a R-852M-1 qui sotto.
- `modules/sottofondo/__init__.py:366`: `riprendi_al_boot` della #398, identico, come `scripts/sottofondo/com.gas.sottofondo.plist` e i test. Esito: ok.
- `.claude/perimetro_review.txt:33`: `scripts/sottofondo/` portato da main, identico. Il perimetro non contiene `scripts/crm/`: vedi R-852M-2.
- `.claude/agents/memoria_revisore.md:1720`: il blob nell'indice è quello di main (b844fa75). Righe di HEAD mancanti: 0. Il ramo non ha toccato la memoria dopo la #397. Esito: ok.
- `reports/stato_progetto.md:4`: la riga «Ultimo aggiornamento» nell'indice è byte per byte la riga di main con il frammento del 24-11 in testa. La riga di HEAD è quella della base più lo stesso frammento, quindi niente si perde. Esito: ok.
- `reports/stato_progetto.md:9-10`: rispetto a main ci sono solo 2 righe in più (CRM sempre acceso e #400). Le righe di main mancanti sono 0: l'unica riga che cambia è la 4, fusa come sopra. Le righe R7 fetta 2 e fetta 3 restano. La riga della #400 è fedele all'ultimo_report di main: prova di taratura, decisione sul modello «ehi Jarvis», cose da provare sul Mac, 0/180, voci sintetiche. Le «aperte da prima» sono già nella riga «Voce, riserve aperte». Esito: ok, salvo R-852M-1.
- `reports/voce_simulazione_2026-11-23/LEGGIMI.md:52`: i 49 file della simulazione sono identici a main, `traccia_fasi.py` e `train_varianti.py` compresi, e R-818-1 è chiusa. Gli spazi a fine riga trovati da `--check` stanno solo nei `.patch` di main. Esito: ok.

**Controlli meccanici**
- `git ls-files -u` vuoto, nessun marcatore di conflitto.
- Il diff dell'indice contro origin/main contiene solo gli 8 file della #403: `scripts/crm/` (3 file), `reports/crm/guida.md` e 4 report.
- handoff, ultimo_report e diff_sessione sono uguali a HEAD (regola 3).
- `bacheca.md` è uguale a main.
- `bash -n` dei due script del CRM ok, plist valido (plistlib). `.gas_memory_crm_server.log` è coperto dal `.gitignore`.
- Test: 893 passed (crm, notte, sottofondo, voce_ascolto) su una copia dell'indice.

**Riserve**
- **R-852M-1 BASSA**: le riserve finali della #400 non sono scritte in nessun file del repo. L'ultimo verdetto del bot sull'head mergiata (f1b29b68) è APPROVATO CON RISERVE, letto con `gh api pulls/400/reviews` ed emesso dopo l'handoff. Contiene:
  - V-1 BASSA: una vecchia `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8` rimasta nel `.env` tiene l'interruzione quasi spenta (8/180) senza nessun avviso nel log. Il bot raccomanda di controllare il `.env` sul Mac dopo il merge.
  - V-2 COSMETICA: «prima 8/180» invece di 4/180; il LEGGIMI della simulazione alla riga 30 mette in grassetto 170/180 (soglia 0,5) invece di 158/180 (soglia 0,6).
  - V-3 COSMETICA: l'handoff si contraddice su R-816-1.
  - Correzione: aggiungere V-1 e il controllo del `.env` alla riga della #400 in `reports/stato_progetto.md:10`.
- **R-852M-2 BASSA (fuori dal merge, riguarda la PR #403)**: `scripts/crm/com.gas.crm.plist:20` installa un LaunchAgent con KeepAlive, ma `scripts/crm/` non è nel perimetro di review. È la stessa categoria per cui ci sono già `scripts/voce/` (V-4 della verifica esterna #323) e `scripts/sottofondo/`. Decide l'operatore. Allargare il perimetro passa comunque dal revisore.
- **COSMETICA**: la riga «Ultimo aggiornamento» (testo di main) dice «aperte BASSE R-816-1», ma R-816-1 è chiusa in #817 (§7 dell'handoff della #400 e claim 7 del bot).

**Avviso importante**: durante la review sono comparse nel working tree modifiche NON in staging a `scripts/crm/installa.sh`, `scripts/crm/com.gas.crm.plist`, `scripts/crm/spegni.sh` e `reports/crm/guida.md` (correzioni V-2/V-3 del bot #403, +54/−8). Non le ho revisionate. Il verdetto vale solo per l'indice. Un `git commit` senza `-a` non le include.

**Rischi esclusi**
- Suite del kernel e pytest completa non rieseguite: il perimetro è identico byte per byte a main, e su f1b29b68 `unit-suite` risulta success.
- Comportamento sul Mac (launchd, microfono, iCloud) non verificabile qui.
- Le modifiche al working tree comparse durante la review: vedi l'avviso sopra.

**Memoria**: in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` ho aggiunto la riga #852-MERGE (senza IP letterali) e 2 lezioni (regola 3: leggere l'ultimo verdetto del bot sull'head mergiata; servizi launchd fuori dal perimetro). Non sono in staging e non le ho committate, come richiesto: `commit_memoria_revisore.sh` non l'ho lanciato perché il merge è in corso. `.claude/.review_ok` non l'ho creato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/ da questo ramo (il codice del merge è identico a main).

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - `5d5911b4`: nessuna run propria (pushato insieme a 51d446c4).
  - `51d446c4`: handoff-check success, verifica-bot failure (APPROVATO CON RISERVE con V-1 MEDIA, chiusa in 20791587), unit-suite in corso alla lettura; poi PR in conflitto dopo i merge delle #398-#400.
  - `f4381a2e`, `20791587`: nessuna run propria (pushati insieme al commit di fine-task).
  - `67f4dc34` (fine-task precedente): handoff-check success, verifica-bot failure (APPROVATO CON RISERVE con V-1 MEDIA, chiusa nel commit dopo).
  - Commit della correzione e di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-852M-2 BASSA (decide l'operatore): `scripts/crm/` fuori dal perimetro di review.
- R-852M-1 BASSA: riportata in `reports/stato_progetto.md` (riga della #400). COSMETICA #852: la riga «Ultimo aggiornamento» di main cita R-816-1 come aperta, ma è chiusa.
- Script non provati su un Mac vero.
- Dalla PR #397: R-848-2 BASSA, R-848-3 BASSA, V-3 BASSA della verifica esterna, cosmetiche #848; R-836-1 COSMETICA.
