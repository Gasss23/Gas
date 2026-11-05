# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — Voce V15: pausa a voce, turni di seguito col cervello forte, conferma che non blocca (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #339 (https://github.com/Gasss23/Gas/pull/339). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5180114384","url":"https://github.com/Gasss23/Gas/pull/339"}`); `gh` nel cloud non è autenticato. Merge secondo la regola di CLAUDE.md §10.
2. R-675-1-M2 parte storia (MEDIA, privacy): i turni di seguito giudicati «non per me» restano nella storia condivisa (li scrive gas.py): toglierli nella fetta «profilo voce» o subito.

---

## §1 SCOPE & ESITO FETTE

- **Pausa a voce** (contratto rivisto dall'operatore via M1): `FATTA`.
- **Turni di seguito** (`X-Gas-Seguito: 1`, solo cervello forte, «[NON_PER_ME]» → `X-Gas-Comando: fine`): `FATTA`.
- **V-2 bot #335** (conferma: timeout 5 s, errore in cache 60 s) e R-669-1-M2 per la conferma: `FATTA`.
- **V-1 bot #335** («Jarvis Gas» dichiarato con un test): `FATTA`.
- **Storia senza turni «non per me»**: `DEFERITA — richiede gas.py` (fetta profilo voce).
- **C1**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |   5 +++++
 modules/voice/server.py             |  86 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 modules/voice/tts.py                |   4 +++-
 reports/diff_sessione.md            |  13 ++++++-------
 reports/handoff.md                  | n/d
 reports/ripartenza_m2.md            |   8 ++++----
 reports/stato_progetto.md           |   3 ++-
 reports/ultimo_report.md            |  23 +++++++++++------------
 tests/test_unit_voice_prova_voci.py |  34 ++++++++++++++++++++++++++++++++--
 tests/test_unit_voice_stt.py        | 111 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
5cf7267 feat(voce): V15 — pausa a voce, turni di seguito decisi dal cervello forte, conferma che non blocca (chat M2)
2d2d432 chore(revisore): memoria review #675 — APPROVATO CON RISERVE
8c9bc1b chore(revisore): memoria review #675 — APPROVATO CON RISERVE
04532a3 chore(revisore): memoria review #675 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

La prima emissione #675-M2 riguardava una versione dello stage poi sostituita (contratto della pausa cambiato): non è stata riportata dall'agente revisore se non come premessa della bis, che la dichiara superata.

Review #675-M2 bis sul diff staged (contratto rivisto; sostituisce la prima emissione #675-M2 sulla versione precedente dello stage), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #675-M2 (bis). Ho guardato il `git diff --cached` attuale, quello con il contratto rivisto: pausa con «basta (così)» e risposta «Va bene.», poi X-Gas-Seguito con [NON_PER_ME], poi la conferma con la cache degli errori. Lo stage è cambiato mentre la review era in corso. La prima versione (pausa/standby con «Va bene, mi metto in pausa.») l'avevo già esaminata e giudicata APPROVATO CON RISERVE, ma non vale più: la sostituisce questo verdetto. I test li ho lanciati sull'albero staged esportato (`git checkout-index` in /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/staged675b), non sulla cartella di lavoro: `tests/test_unit_voice_stt.py` + `tests/test_unit_voice_prova_voci.py` danno 155 passed. Sulla versione precedente dello stage la suite voce (`-k voice`) dava 304 passed.

Elementi esaminati (righe dello stage attuale):
- modules/voice/server.py:130 — regex `_SOLO_PAUSA` ancorata con ^…$ — falsi positivi e backtracking — ok. Vanno al cervello, cioè nella direzione sicura: «pausa caffè», «in pausa», «metti in pausa la musica», «basta il sale», «basta, grazie», «pausa per favore», «forte pausa». Una stringa da 350k caratteri si chiude in 0,02 s. Unico caso dubbio: «basta così?» detto come domanda chiude la conversazione (R-675-4-M2).
- modules/voice/server.py:509 — controllo della pausa solo nel ramo audio, prima di «Dimmi.» e prima di `cervello_voce` — forte e formati — ok. Passa da `_rispondi_senza_turno`, quindi funziona in ogni formato. A testo «pausa» resta una richiesta normale (test a tests/test_unit_voice_stt.py:768). «forte, pausa» va al cervello forte (R-675-4-M2).
- modules/voice/server.py:446 — override di `end_headers` che aggiunge X-Gas-Comando — comando rimasto da una richiesta precedente — ok. `_comando` si azzera in do_POST e do_GET. Il server è HTTP/1.0 senza keep-alive, quindi ogni connessione ha un'istanza nuova. Vale per JSON, MP3 e NDJSON.
- modules/voice/server.py:559 — `ISTRUZIONE_SEGUITO` aggiunta all'istruzione del turno se `_seguito()` (modules/voice/server.py:623) — privacy — **riserva MEDIA**, vedi R-675-1-M2.
- modules/voice/server.py:587 — `SEGNO_NON_PER_ME in result_content` → JSON {"content":"","fine":true} con X-Gas-Comando: fine — esce prima di ogni sintesi o streaming? — ok, ElevenLabs non viene chiamato. Il segno però è cercato come sottostringa (R-675-3-M2). Nel formato audio+pezzi il client riceve JSON e non NDJSON: va confermato lato Mani.
- modules/voice/server.py:870 e modules/voice/server.py:881 — cache negativa di 60 s per (voce, frase), timeout di 5 s, `http.client.HTTPException` intercettata — il server a un thread si blocca? — ok. Un successo azzera l'errore; con un'altra voce non resta bloccato (test a tests/test_unit_voice_prova_voci.py:737). modules/voice/tts.py:84 — nuovo parametro `timeout` con default invariato di 30 s — ok.

Riserve:
- **R-675-1-M2 MEDIA (privacy, decide l'operatore)**: il seguito manda al cervello il parlato di terzi (stanza, TV, telefonate). Con `GAS_VOCE_FORTE` spento lo manda ai modelli gratuiti, contro la regola dei modelli di CLAUDE.md §2 (ai gratuiti niente dati personali). Gli strumenti restano attivi: se il cervello sbaglia a giudicare, agisce su parlato ambientale. Inoltre run_turn salva il parlato nella storia condivisa. Proposta: turni di seguito solo col cervello forte, fail-closed se non è disponibile, e turni [NON_PER_ME] non salvati (fetta «profilo voce» in gas.py).
- **R-675-2-M2 BASSA**: oltre il tetto orario il 429 arriva prima della trascrizione, quindi «pausa» non si può dire proprio quando il client continua a mandare richieste. Anche i turni di seguito ambientali consumano il tetto.
- **R-675-3-M2 BASSA**: il segno è cercato come sottostringa. Le varianti senza parentesi («NON_PER_ME», «Non per me») non vengono riconosciute e quindi vengono lette ad alta voce.
- **R-675-4-M2 COSMETICA**: «basta così?» e «Pausa?» detti come domanda chiudono la conversazione; «forte, pausa» va al cervello forte.
- Nota: il controllo `self._parlato` in `_seguito()` è ridondante con `is_audio`, quindi il mutante sopravvive. È una difesa voluta: accettabile.

Cosa NON ho verificato: il comportamento reale del client H24 (riprendi.sh, gestione di «fine» e del JSON in formato pezzi), perché è lato Mani e non è nel repo di questa fetta. Non ho verificato nemmeno quanto bene un LLM reale distingue il parlato rivolto a Gas: non si riproduce senza cervello reale, i test usano un kernel finto.

Attenzione per il gate: le righe citate valgono per lo stage attuale (211 righe aggiunte). Se lo stage cambia ancora prima del commit, serve una nuova review.

Memoria: righe #675-M2 e #675-M2 bis, più due lezioni, in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con scripts/commit_memoria_revisore.sh (commit 04532a3 e 8c9bc1b).

Review #675-M2 ter sullo stage finale del commit 5cf7267 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #675-M2 ter: solo l'aggiunta che chiude R-675-1-M2 (parte server) e R-675-3-M2, sul `git diff --cached` attuale. I test li ho lanciati sull'albero staged esportato (/tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/staged675c): `tests/test_unit_voice_stt.py` + `tests/test_unit_voice_prova_voci.py` danno 155 passed.

Cosa ho controllato:
- modules/voice/server.py:567 — nel ramo `_seguito()` il turno va solo al cervello forte (`kw["cervello"] = "forte"`). Rischio controllato: che passi lo stesso ai gratuiti. Esito: ok. In gas.py:923 (contesto, file non toccato) la catena «forte» contiene solo claude-cli: se il forte non c'è, il turno non scende ai gratuiti. I test verificano il forte col seguito (tests/test_unit_voice_stt.py:747) e nessun campo `cervello` senza seguito (tests/test_unit_voice_stt.py:763). **R-675-1-M2 parte server: chiusa.**
- modules/voice/server.py:143 — nuova regex `_NON_PER_ME` (`^\W*non[_\s]+per[_\s]+me\W*$`, maiuscole e minuscole uguali), usata in modules/voice/server.py:594. Rischio controllato: risposte vere scambiate per il segno, e lentezza su testi lunghi. Esito: ok.
  - Riconosciute: «[NON_PER_ME]», «NON_PER_ME», «Non per me.», ««[NON_PER_ME]»».
  - Restano risposte normali: «Non per me è un problema, lo faccio subito.», «[NON_PER_ME] Ciao», «Non è per me.».
  - Nessun rallentamento: 200k caratteri in meno di 1 ms. **R-675-3-M2: chiusa.**

Riserve:
- **R-675-1-M2, parte storia: resta APERTA (MEDIA)**. I turni [NON_PER_ME] finiscono comunque nella storia condivisa scritta da gas.py. Va fatta nella fetta «profilo voce», che spetta all'operatore.
- **R-675-5-M2 BASSA (nuova)**. Due effetti da dire all'operatore:
  1. Con il forte dormiente (`GAS_CLAUDE_CLI` spento) ogni turno di seguito risponde 500 senza X-Gas-Comando. La finestra di conversazione non funziona finché il forte non è acceso, e il client (lato Mani) deve chiudere la conversazione anche su un errore.
  2. Con il forte acceso, ogni frase captata nella finestra (anche TV o persone che parlano fra loro) spende il budget giornaliero del forte.
- Restano come prima R-675-2-M2 (tetto orario) e R-675-4-M2 (frasi in forma di domanda).

Cosa NON ho verificato: un turno reale col forte (claude-cli) acceso. Non si riproduce in questo ambiente: i test usano un kernel finto, quindi ho verificato solo che il server chiede il forte, non come risponde davvero.

Memoria: riga #675-M2 ter in /home/user/Gas/.claude/agents/memoria_revisore.md, committata con scripts/commit_memoria_revisore.sh (commit 2d2d432).

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_stt.py`: +6 test V15 (`test_v15_pausa_nessun_turno_e_comando`, `test_v15_pausa_solo_dal_parlato`, `test_v15_seguito_non_per_me_chiude_senza_voce`, `test_v15_seguito_rivolto_a_gas_risponde_normalmente`, `test_v15_senza_seguito_nessuna_decisione`, `test_v15_seguito_a_testo_ignorato`), «Jarvis Gas» fra i positivi. `tests/test_unit_voice_prova_voci.py`: +1 (`test_v15_conferma_errore_recente_non_richiama_elevenlabs`), IncompleteRead nel test degli errori. Suite voce della CI in un venv con requirements + requirements-dev: `291 passed in 314.82s` prima delle correzioni R-675-1/3; dopo, voice_stt + voice_prova_voci `155 passed in 46.28s` e `-k v15` 6 passed. Mutanti: senza intestazione, senza comando, senza registrazione dell'errore, senza ramo «fine»: uccisi; `self._parlato` in `_seguito()` ridondante con `is_audio` (sopravvive, difesa voluta). Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud: check lette con l'integrazione GitHub.
- 04532a3, 8c9bc1b, 2d2d432: nessuna run su questi SHA da soli (pushati insieme a 5cf7267).
- 5cf7267 e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (la run sul push finale testerà solo la testa).

## §7 RISERVE APERTE

- R-675-1-M2 parte storia MEDIA: i turni «non per me» restano nella storia condivisa (gas.py).
- R-675-2-M2 BASSA: oltre il tetto orario «pausa» riceve 429; i turni ambientali consumano il tetto.
- R-675-4-M2 COSMETICA: «basta così?» come domanda chiude la conversazione; «forte, pausa» va al forte.
- R-675-5-M2 BASSA: forte spento → turni di seguito 500 (il client deve chiudere); forte acceso → ogni frase captata spende il budget del forte.
- Da verificare lato client (Mani): JSON (non NDJSON) nella risposta «fine» col formato audio+pezzi.
