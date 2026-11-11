# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 — voce: filtro 2, più allucinazioni di Whisper scartate (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #373 (https://github.com/Gasss23/Gas/pull/373): con verdetto del bot APPROVATO pulito e CI verde la mergia la chat (regola notturna di M1); con riserve resta pronta per il «mergia» del mattino.
2. R-764-2-M2: su Telegram un vocale «Grazie di cuore» ora riceve «Non ho capito bene il vocale». Va bene? (file della chat Mani)

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Varianti dei saluti, frasi intere senza punteggiatura interna, allucinazioni composte frase per frase**: `FATTA` (438704b).
- **Parti note solo su frasi corte (V-1 bot #369)**: `FATTA` (438704b).
- **Intercalari nel seguito**: `FATTA` (438704b).
- **R-764-1, R-766-1, R-767-1**: `FATTA` — chiuse prima del commit (review #766, #767, #769-M2).
- **Prova sul Mac dal vero**: `DEFERITA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 modules/voice/server.py            |  13 ++++++++++++-
 modules/voice/stt.py               |  58 +++++++++++++++++++++++++++++++++++++++++++++++++++-------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  18 ++++++++++--------
 tests/test_unit_voice_server.py    |  12 ++++++++++++
 tests/test_unit_voice_stt.py       |  32 ++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
438704b fix(voce): filtro 2 — varianti dei saluti di Whisper e allucinazioni composte scartate frase per frase, intercalari nel seguito, parti note solo su frasi corte — review #764/#766/#767/#769-M2 (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #769-M2 (seguito di #767-M2, R-767-1) — verdetto integrale

VERDETTO: APPROVATO

Review #769-M2 (segue la #767-M2) sul diff staged di /home/user/Gas-filtro2. R-767-1-M2 è chiusa: le allucinazioni composte (crediti + saluto) tornano a essere scartate e le richieste vere passano.

Le review #764, #766 e #767 le avevo già consegnate prima dei tuoi messaggi. In breve, tutte APPROVATO CON RISERVE:
- #764-M2: R-764-1 e R-764-2, entrambe BASSE.
- #766-M2: chiude R-764-1 e apre R-766-1 (BASSA).
- #767-M2: chiude R-766-1 e apre R-767-1 (MEDIA), ora chiusa da questo diff.

**Elementi del diff esaminati**
- `modules/voice/stt.py:124` — `_frase_allucinata` raccoglie le regole che prima valevano per tutta la trascrizione: nessuna parola, parti note col tetto di 8 parole, frasi intere con e senza punteggiatura interna, saluti con almeno un «grazie». Rischio: perdere una regola nello spostamento. Esito: ok, i casi di #764, #766 e #767 danno lo stesso risultato.
- `modules/voice/stt.py:121` — `_FINE_FRASE_STT` divide le frasi solo dove la punteggiatura di fine frase è seguita da uno spazio. Rischio: spezzare «amara.org». Esito: ok.
  - «amara.org» resta intera e la frase dei crediti viene scartata.
  - «Grazie.Grazie mille.» (senza spazio) viene scartata già dal controllo sulla frase intera.
- `modules/voice/stt.py:151` — divisa in frasi, la trascrizione è scartata solo se OGNI frase è un'allucinazione (`all`). Esito: ok.
  - Scartate, anche passando da `_motivo_incerta`: «Sottotitoli creati dalla comunità Amara.org. Grazie per la visione.», «Sottotitoli a cura di QTSS. Grazie a tutti per la visione.», «Grazie. Grazie mille. Alla prossima!», «Grazie! Ciao a tutti!».
  - Passano: «Grazie. Ora segna il lead Rossi.», «Grazie mille. Che ore sono?», «Grazie. Il prossimo.», «Segna il lead Rossi. …» (la frase fatta di soli puntini non trascina con sé quella vera), la richiesta lunga coi «sottotitoli a cura di Rai», «Chi ha fatto i sottotitoli a cura di Rai? Sottotitoli a cura di chi?».

**Test e mutanti**
- Suite voice_stt + voice_server + telegram_voce + voce_ascolto (`-k "audit or not browser"`): **751 passed**.
- Mutanti provati, entrambi fanno fallire i test (quindi i test li rilevano):
  - `all` → `any` nella riga `modules/voice/stt.py:151`: 2 test falliti;
  - «niente divisione in frasi» (`return False`): 3 test falliti.
- Ho ripristinato il file dopo ogni mutante: nessuna modifica rimasta fuori dallo staging.

Il diff non tocca la storia dei messaggi né `_get_window`, non simula l'output dei tool e non cambia i provider.

**Riserve ancora aperte da prima**: R-764-2-M2 BASSA (su Telegram un vocale «Grazie di cuore» ora riceve «non ho capito»), R-761-4 COSMETICA. Questo diff non ne aggiunge.

**Cosa non ho verificato**: come Whisper mette davvero punteggiatura e spazi tra le frasi su audio reale (per esempio crediti e saluto senza punto in mezzo). Serve la prova sul Mac.

**Memoria**: ho aggiunto la riga #769-M2 in /home/user/Gas-filtro2/.claude/agents/memoria_revisore.md, senza lezioni nuove, e l'ho messa in staging con `git -C /home/user/Gas-filtro2 add`. Non ho fatto commit.

### Review #767-M2 (seguito di #766-M2) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #767-M2 (segue la #766-M2) sul diff staged di /home/user/Gas-filtro2. Il problema dei saluti con la virgola (R-766-1) è chiuso, ma il nuovo limite di 8 parole lascia passare di nuovo alcune allucinazioni: è la riserva MEDIA R-767-1-M2 qui sotto.

**Elementi del diff esaminati**
- `modules/voice/stt.py:133` — le frasi intere ora si confrontano anche senza la punteggiatura interna, e l'elenco ha in più «grazie mille e alla prossima» e «grazie mille a tutti e alla prossima». Rischio esaminato: che il confronto senza punteggiatura scarti anche richieste vere. Prove: «Grazie, e alla prossima!», «Grazie mille, e alla prossima», «Grazie, per l'ascolto», «Iscriviti, al canale» vengono tutte scartate. Esito: ok, R-766-1-M2 chiusa.
- `modules/voice/stt.py:128` — le parti note (`_ALLUCINAZIONI_PARTI`) fanno scartare la frase solo se ha al massimo `_PARTI_MAX_PAROLE` = 8 parole. Il limite vale anche in `_motivo_incerta` (`modules/voice/stt.py:152`). «Gas, cerca chi ha fatto i sottotitoli a cura di Rai per il film» passa. Il problema: le allucinazioni COMPOSTE, cioè una riga di crediti più un saluto, superano le 8 parole e ora arrivano al cervello («Sottotitoli creati dalla comunità Amara.org. Grazie per la visione.», «Sottotitoli a cura di QTSS. Grazie a tutti per la visione.»). Esito: **riserva MEDIA R-767-1-M2**, non bloccante. Proposta: togliere la parte nota dal testo e scartare se quello che resta è vuoto o è a sua volta un'allucinazione.
- `tests/test_unit_voice_stt.py:1399` — il test con la richiesta lunga dei «sottotitoli a cura di Rai». Esito: ok, ma manca un test per la frase composta crediti + saluto.

**Test e mutante**: suite voice_stt + voice_server + telegram_voce + voce_ascolto: 746 passed. Mutante «tolto il limite di parole»: 1 test fallisce.

**Riserve aperte**: R-767-1-M2 (MEDIA); R-764-2-M2 (BASSA); R-761-4 (COSMETICA).

**Cosa non ho verificato**: quanto spesso Whisper produce davvero le frasi composte crediti + saluto. Serve audio reale sul Mac.

**Memoria**: riga #767-M2 e una lezione nuova (con un tetto di lunghezza a un filtro per sottostringa, provare l'unione di due frasi già nell'elenco), in staging.

### Review #766-M2 (seguito di #764-M2) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #766-M2 (segue la #764-M2) sul diff staged di /home/user/Gas-filtro2 (branch fix/voce-filtro2-m2). R-764-1-M2 è chiusa. Ho controllato solo la parte nuova del diff.

**Elementi del diff esaminati**
- `modules/voice/stt.py:52`: l'elenco `_PAROLE_DEI_SALUTI` di oggi non contiene più «prossimo», «prossima», «ancora», «il», «video», «alla», «al». Restano «la», «per», «di», «l», «a», «e». «Grazie, la prossima.» passa lo stesso, perché «prossima» non è più nell'elenco. Esito: ok.
- `modules/voice/stt.py:61`: le chiusure tipiche ora sono frasi intere in `_ALLUCINAZIONI_INTERE`. Il confronto toglie la punteggiatura solo ai bordi. Restano scartate «Grazie a tutti e alla prossima.», «Alla prossima.», «Grazie per aver guardato il video.», «Grazie di cuore.», «Grazie, grazie.», «Grazie mille a tutti.»; passano «Grazie, il prossimo.», «Grazie, la prossima.», «Grazie, ancora.», «Grazie, il video.»; passano anche «Grazie, e alla prossima!» e «Grazie mille e alla prossima». Esito: **riserva BASSA R-766-1-M2**.
- `tests/test_unit_voice_stt.py:1395`: i 4 casi di R-764-1 stanno nel test delle richieste che devono passare. Esito: ok.

**Test e mutante**: `-k "filtro2 or allucin"`: 59 passed. Mutante «ancora rimesso in `_PAROLE_DEI_SALUTI`»: 1 test fallito.

**Riserve aperte**: R-766-1-M2 (BASSA); R-764-2-M2 (BASSA); R-761-4 (COSMETICA).

**Memoria**: riga #766-M2 in staging.

### Review #764-M2 — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Ho fatto la review #764-M2 sul diff staged di /home/user/Gas-filtro2 (branch fix/voce-filtro2-m2, head 8b11ba8). Prima ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (in modo mirato) e la memoria del revisore.

**Elementi del diff esaminati**
- `modules/voice/stt.py:121` — nuovo ramo di `allucinazione()`: la frase è scartata se contiene almeno un «grazie» e tutte le parole sono nell'elenco `_PAROLE_DEI_SALUTI`. Sonde: «Grazie Gas», «Grazie a te.», «Grazie, a domani», «Grazie, per oggi è tutto», «grazie e basta» passano; «Ciao» e «Buonanotte.» passano. Esito: **riserva** (R-764-1).
- `modules/voice/stt.py:67` — l'elenco `_PAROLE_DEI_SALUTI` contiene anche «il», «la», «per», «di», «prossimo/prossima», «ancora», «video». «Grazie, il prossimo.», «Grazie, la prossima.», «Grazie, ancora.» e «Grazie, il video.» risultano allucinazioni. Esito: **riserva BASSA R-764-1-M2**.
- `modules/voice/stt.py:59` — «ciao a tutti» e «ciao ciao a tutti» aggiunti; tolta «sottotitoli a cura di», che resta coperta dall'elenco delle frasi parziali. Esito: ok.
- `modules/voice/server.py:233` — `seguito_da_scartare` scarta le frasi fatte solo di intercalari (elenco `_INTERCALARI` a `modules/voice/server.py:220`). «Niente.» da solo era già scartato prima; cambiano solo le frasi di più intercalari. Scartare vuol dire chiudere il seguito senza turno (`modules/voice/server.py:802`). «Niente, annulla», «Allora sì» e «Boh, dimmi tu» passano. Esito: ok.
- Contesto: `modules/voice/stt.py:138` — `_motivo_incerta` chiama `allucinazione()`, quindi il filtro vale anche per il bot Telegram. Esito: **riserva BASSA R-764-2-M2**.

**Test e mutanti**: suite voice_stt + voice_server + telegram_voce: 429 passed. Mutanti: requisito «almeno un grazie» tolto (2 falliti), `all` → `any` (2 falliti), ramo degli intercalari tolto (5 falliti).

**Riserve**: R-764-1-M2 (BASSA), R-764-2-M2 (BASSA), R-761-4 COSMETICA.

Wall of Shame: il diff non tocca la history né `_get_window`, non simula output di tool e non cambia guardrail o provider.

**Cosa non ho verificato**: il comportamento dal vivo sul Mac con il microfono. Non ho provato nemmeno parole con accenti fuori dalla regex `_PAROLA`.

**Memoria**: riga #764-M2 in staging.

## §5 DELTA TEST DEL MOTORE

- gas.py non toccato. Test nuovi: `test_filtro2_varianti_dei_saluti` (15 casi), `test_filtro2_le_richieste_passano` (15), `test_filtro2_seguito_solo_intercalari` (9).
- `python -m pytest -q tests/test_unit_voice_stt.py tests/test_unit_voice_server.py tests/test_unit_telegram_voce.py tests/test_unit_voce_ascolto.py -k "audit or not browser"`:

```
751 passed, 25 deselected in 78.91s (0:01:18)
```

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud).
- 438704b: run non ancora disponibile alla scrittura dell'handoff (pushato prima di aprire la PR #373).
- Commit di fine task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-764-1-M2 BASSA, R-766-1-M2 BASSA, R-767-1-M2 MEDIA: CHIUSE (438704b, review #766/#767/#769-M2).
- V-1 BASSA del bot su #369 (parti note in una richiesta lunga): CHIUSA.
- R-764-2-M2 BASSA: su Telegram un vocale «Grazie di cuore» ora riceve «Non ho capito bene il vocale» (allarga R-761-1).
- R-761-4-M2 COSMETICA: «grazie» nell'elenco delle risposte brevi del seguito non viene più raggiunto.
- Non verificato: come Whisper punteggia davvero le frasi su audio reale (prova sul Mac).
