# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Mani: piano della mail di Gas (R6), PR doc-only; riserve di #323 registrate (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #324 (https://github.com/Gasss23/Gas/pull/324). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5125431345","url":"https://github.com/Gasss23/Gas/pull/324"}`), perché `gh` nel cloud non è autenticato. Solo documenti: il merge segue la regola di CLAUDE.md §10 (verdetto del bot).
2. Rispondere alle 7 domande in fondo a `reports/piano_mail.md`: niente codice della mail prima delle risposte.

---

## §1 SCOPE & ESITO FETTE

- **PR #323 (fetta 37, voce H24)**: `FATTA` — mergiata (9718e0c) col sì dell'operatore; la parola resta «hey_jarvis» per ora («Hey Gas» in una fetta a parte, decisione di M1).
- **Piano mail (chiesto da M1)**: `FATTA` — `reports/piano_mail.md`: lettura non fidata, bozze in Gas, invio solo con firma, credenziali separate, tetti, solo cervello forte, 7 domande per l'operatore.
- **Riserve di #323 in stato_progetto (richiesta di M1)**: `FATTA` — V-1 del bot su 3672964 e V-1…V-6 della seconda verifica esterna (https://github.com/Gasss23/Gas/pull/323#issuecomment-6583621078), registrate senza altri giri.
- **Bot su 0c0081f (https://github.com/Gasss23/Gas/pull/324#pullrequestreview-5741499541)**: APPROVATO CON RISERVE, check success. V-1 BASSA (il piano prometteva «mail solo al forte» senza dire che l'output degli strumenti resta nella storia e va ai gratuiti al turno dopo): `FATTA` in 9718c6a — requisito del kernel nel punto 6 e nella fetta 1. V-2 BASSA (V-4 COSMETICA del bot su #323 non registrata): `FATTA`. V-3 COSMETICA (numero della PR): `FATTA`.
- **Bot su 9718c6a (https://github.com/Gasss23/Gas/pull/324#pullrequestreview-5741654147)**: APPROVATO CON RISERVE, check success. V-1 BASSA (il piano usava i nomi `leggi_mail`/`invia_mail`, ma il cancello contamina e mette alla firma per NOME): `FATTA` — ora `fetch_email`/`send_email`, con `fetch_email` già tra gli strumenti che contaminano e `send_email` già IRREVERSIBLE; `prepara_bozza` da aggiungere con un test. V-2 BASSA (handoff non riallineato all'head): `FATTA` in questo commit.
- **Bot su cb84cc0 (https://github.com/Gasss23/Gas/pull/324#pullrequestreview-5741711721)**: APPROVATO CON RISERVE, check success. V-1 BASSA (`fetch_email` è tra gli strumenti che contaminano ma non in GATE_ALLOWLIST, quindi oggi negato: «già nel cancello» era impreciso): `FATTA` — requisito della fetta 1 con un test. V-2 COSMETICA (V-3 bot #323 non registrata): `FATTA`.
- **Bot su 18f2621 (https://github.com/Gasss23/Gas/pull/324#pullrequestreview-5741750870)**: APPROVATO CON RISERVE, check success. V-1 BASSA (il requisito del kernel copriva solo l'output di fetch_email, non le risposte e gli argomenti dello stesso turno): `FATTA` — «una finestra con un turno mail non va mai ai gratuiti». V-2 BASSA (conflitto con main dopo la #322): `FATTA` — main unita con un merge, blocchi M2 tenuti (review del merge #626). V-3 COSMETICA (`_LIBERI_DOPO_LETTURA` per prepara_bozza): `FATTA`.
- **Merge di main (PR #322 di M2, voce V7a)**: `FATTA` in b66ac40 — conflitti solo nei report (tenuti i miei) e nella riga «Ultimo aggiornamento» (unite); file del perimetro entrati da main identici a MERGE_HEAD. **Review #626 (chat Mani)**: APPROVATO CON RISERVE. R-626-1 BASSA (il requisito del kernel nominava solo i turni dopo: ora anche riflessione di fine task e compressione) e R-626-2 BASSA (handoff non riallineato al merge): `FATTA` in questo commit.
- **Bot su 970beca (https://github.com/Gasss23/Gas/pull/324)**: NON approvato, check verifica-bot failure. V-1 MEDIA (il requisito del kernel non copriva la memoria: `_memoria_pin` mette i contatti attivi nel system di ogni turno, anche sui gratuiti, e `ricorda` li rende leggibili): `FATTA` — quarto percorso nel punto 6, contatti dalle mail con origine «mail» esclusi fuori dal forte, e finché non c'è nessun contatto salvato dalle mail. V-2 BASSA (`notify_telegram` è SAFE, quindi dopo una lettura partirebbe senza firma): `FATTA` — nel piano e nella fetta 1.
- **Fetta piccola sulla voce (V-1 ve, V-1/V-4 bot, V-4 ve di #323)**: `DEFERITA — commit locale bc369ed sul branch voce-fix (review #624 BOCCIATO, #625 APPROVATO CON RISERVE); PR subito dopo questa (un solo branch remoto)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 reports/diff_sessione.md           |  16 ++++++++--------
 reports/handoff.md                 | n/d
 reports/piano_mail.md              | 104 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ripartenza_mani.md         |   2 +-
 reports/roadmap.md                 |   4 ++--
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  32 +++++++++++++------------------
```

NB: base = merge-base con origin/main = c2f2a68. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
970beca docs(mail): tre percorsi verso i gratuiti nel requisito del kernel, handoff col merge di main (R-626-1/2)
ffff127 chore(revisore): memoria review #626 — APPROVATO CON RISERVE
b66ac40 Merge origin/main (PR #322, voce V7a) nella PR #324; piano mail: requisito del kernel su tutto il turno mail (review #626)
18f2621 docs(mail): fetch_email da aggiungere a GATE_ALLOWLIST nella fetta 1, V-3 bot #323 registrata (V-1/V-2 bot #324 su cb84cc0)
cb84cc0 docs(mail): nomi degli strumenti come nel cancello (fetch_email/send_email), handoff riallineato (V-1/V-2 bot #324 su 9718c6a)
9718c6a docs(mail): requisito del kernel per le mail (output mai ai gratuiti), V-4 bot #323 registrata, numero della PR (V-1/V-2/V-3 bot #324)
0c0081f docs(fine-task): piano mail, PR #324
ec1fdbb docs(mail): stato, roadmap e ripartenza col piano mail; riserve di #323 registrate
6af999b docs(mail): piano della mail di Gas (R6) con le domande per l'operatore, senza codice
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

I commit di documenti della PR non toccano il motore. Il merge di origin/main (PR #322 di M2) porta file del perimetro di main, invariati: verdetto integrale della review #626 (chat Mani) sul merge:

```
## VERDETTO: APPROVATO CON RISERVE

Review #626 (chat Mani). È il merge di origin/main c2f2a68 (PR #322 di M2, voce V7a) dentro claude/peaceful-lovelace-0w2b7q (PR #324). Il diff staged ha sha256 f005872104445eb3…, la base del merge è 9718e0c. Prima della review ho letto CLAUDE.md (sez. 1, 5, 8, 10), le parti di reports/stato_progetto.md che servivano e la memoria del revisore (lezioni #619 e #620 sui merge).

**Elementi del diff esaminati**
- `modules/voice/server.py:381`: entra da main con la misura dei tempi della V7a. Rischio: che il merge l'abbia modificato. Ho confrontato i blob dell'indice con MERGE_HEAD e sono identici, come per `clients/voice/browser_client.html`, `tests/test_unit_voice_server.py`, `tests/test_unit_voice_stt.py` e `.claude/agents/memoria_revisore.md`. `git diff --cached MERGE_HEAD` tocca solo reports/. Ho rilanciato i test della voce (server e trascrizione): 170 passed. Esito: ok.
- `.claude/agents/memoria_revisore.md:1164`: memoria entrata da main (12 righe, dalla #614-M2 alla #650-M2). Rischio: righe perse o un'unione sbagliata. Rispetto a HEAD non ci sono righe rimosse e il blob è identico a MERGE_HEAD. Esito: ok.
- `reports/stato_progetto.md:4`: la riga «Ultimo aggiornamento» è il tuo pezzo «piano mail» seguito dalla riga intera di main. Il blocco V7a, il blocco «piano mail» e la fetta 37 compaiono una volta sola ciascuno: niente doppioni, niente mancanti, nessun marcatore di conflitto. Il file passa da 899 a 900 righe, cioè solo il blocco V7a in più. Esito: ok.
- `reports/piano_mail.md:18`, punto 2: dice che `prepara_bozza` va messo in `_LIBERI_DOPO_LETTURA`, altrimenti a finestra contaminata andrebbe alla firma. Coerente col codice: `modules/gate/gate.py:544` (insieme oggi = rubrica + write_file) e `modules/gate/gate.py:650` (un nome diverso da write_file che sta nell'insieme è libero senza altri controlli). Il kernel ripete il controllo in `gas.py:3119`, senza casi speciali oltre a write_file. Esito: ok.
- `reports/piano_mail.md:47`, punto 6: la frase «`_get_window` rimanda tutto ai turni dopo, che di default vanno alla cascata gratuita» è vera. `gas.py:1805` tiene anche i messaggi tool e le risposte dell'assistente. `gas.py:911` manda al forte solo se compito == "forte", gli altri compiti finiscono nella cascata gratuita. Esito: ok, con la riserva R-626-1.

**Riserve**
- **R-626-1 BASSA**: il requisito del kernel («una finestra con un turno mail non va mai ai gratuiti») nomina solo `_get_window` e i turni successivi. Ci sono altri due percorsi che portano la storia ai gratuiti:
  - la riflessione di fine task: `gas.py:4004` usa `_cascata_provider("complesso")` su una finestra presa da `_get_window`;
  - il riepilogo di compressione: in `gas.py:1543` il testo degli strumenti diventa un messaggio user e il messaggio tool sparisce. Se la fetta 1 riconosce il «turno mail» dal nome dello strumento, dopo una compressione non lo trova più.

  Correzione: aggiungere al punto 6 una riga che nomini run_turn, riflessione e compressione.
- **R-626-2 BASSA**: `reports/handoff.md` è ancora identico a HEAD, quindi non è stato aggiornato col merge, anche se tu dici «tenuti i miei, poi aggiornati». Va riallineato prima del commit finale, con questo verdetto integrale nel §4.
- Nota cosmetica, senza numero: al punto 6, «Il testo letto non si conserva oltre il turno» sembra un fatto di oggi, mentre più sotto il requisito spiega che oggi la storia tiene tutto. Meglio scrivere «dovrà non conservarsi».

**Cosa NON ho verificato**: la suite del kernel e i test del cancello (gate). Il motivo è che gas.py, modules/gate/ e brains/ non stanno nel diff di questo merge (i due lati toccano file diversi, a parte i report). Non ho verificato nemmeno la CI di main su c2f2a68, perché non è riproducibile da qui.

**Memoria**: ho aggiunto la riga #626 in fondo a `/home/user/Gas/.claude/agents/memoria_revisore.md`, solo nel working tree. L'indice non è toccato: lo sha256 dello staged resta f005872104445eb3. Come chiede la lezione #619, non ho lanciato `scripts/commit_memoria_revisore.sh`: lancialo tu dopo aver committato il merge.
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh` non autenticato nel cloud.
- 6af999b (piano mail), ec1fdbb (report): pushati insieme prima dell'apertura della PR #324.
- 0c0081f (fine-task): CI success (handoff-check, unit-suite); verifica-bot success (bot APPROVATO CON RISERVE).
- 9718c6a (correzioni dopo il bot): CI success; verifica-bot success (bot APPROVATO CON RISERVE).
- cb84cc0 (correzioni dopo il bot): CI success; verifica-bot success (bot APPROVATO CON RISERVE).
- 18f2621 (correzioni dopo il bot): verifica-bot success (bot APPROVATO CON RISERVE); poi conflitto con main (PR #322).
- I commit di main entrati col merge (fino a c2f2a68, PR #322) hanno le run della PR #322.
- b66ac40 (merge), ffff127 (memoria #626), 970beca (fine-task): verifica-bot failure su 970beca (V-1 MEDIA, chiusa in questo commit); unit-suite non ancora conclusa alla scrittura dell'handoff.
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Da #323 (mergiata): V-1 bot su 3672964 BASSA (GAS_CLAUDE_BIN sotto launchd); V-4 bot COSMETICA (token vuoto accettato da installa.sh); V-3 bot COSMETICA superata dal merge; V-1 ve BASSA (rilevatore sempre in errore); V-2/V-3 ve BASSE (igiene dei test); V-4 ve BASSA (scripts/voce/ fuori dal perimetro); V-5 ve BASSA (spegni.sh e due garanzie senza test); V-6 ve COSMETICA; R-623-1/2/3; R-615-4 MEDIA (microfono sotto launchd, da provare sul Mac); R-615-5 BASSA (licenza).
- Da #319: V-1 bot su 9c44686 BASSA (limite dichiarato) e le altre registrate in stato_progetto.
