# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-25 — Voce: log più chiari e nome del modello sicuro (dopo la PR #405)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR del ramo `fix/voce-log-e-modello`. Con APPROVATO pulito del bot la mergia l'agente; altrimenti serve il «mergia» dell'operatore.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Log del primo turno scartato**: FATTA. Prova del 25/11 sul Mac: «fine» sul primo turno ora è loggato come richiesta scartata, non più come seguito.
- **Fetta 2 — Nome del modello**: FATTA. Un nome non semplice ripiega su hey_jarvis (V-1 bot #405); il nome è normalizzato in `main` (R-864-1).
- **Fetta 3 — Log di avvio col modello in uso**: FATTA (R-855-1).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  3 +++
 clients/voice/ascolto.py           | 36 +++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           | 21 ++++++++++-----------
 reports/handoff.md | n/d
 reports/stato_progetto.md          |  2 +-
 reports/ultimo_report.md           | 68 ++++++++++++++++----------------------------------------------------
 tests/test_unit_voce_ascolto.py    | 38 +++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d»: il conteggio di reports/handoff.md non è misurabile mentre lo si scrive; la riga di totale è tolta.

## §3 GIT LOG --ONELINE (sessione)

```
c46b0b86 fix(voce): log chiaro sul primo turno scartato, modello in uso nel log di avvio, nome del modello normalizzato e mai un percorso (V-1 bot #405, R-855-1, R-864-1)
98ec858e chore(revisore): memoria review #865 — APPROVATO CON RISERVE
5586236b chore(revisore): memoria review #864 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit c46b0b86 tocca `tests/test_unit_voce_ascolto.py`, che è nel perimetro. Sotto ci sono i verdetti INTEGRALI: #864 sul diff, #865 sulle correzioni R-864-1 e R-864-2.

```
## VERDETTO: APPROVATO CON RISERVE

Review #864 di fix/voce-log-e-modello, `git diff --cached` (2 file, +54/−5). Suite tests/test_unit_voce_ascolto.py rieseguita: 393 passati. Il motore (gas.py, brains/) non è toccato. Non ho usato git stash e l'indice è intatto.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1456` — un nome non semplice (percorso, maiuscole, vuoto) ora ripiega su `hey_jarvis` con un avviso nel log, invece di arrivare a openWakeWord.
   - Rischio: un percorso preso dall'ambiente che arriva a openWakeWord, il quale controlla `os.path.exists(nome)` rispetto alla cartella corrente.
   - Esito: ok, V-1 del bot #405 è chiusa. Il test `tests/test_unit_voce_ascolto.py:3407` lo prova con `../`, un percorso assoluto, maiuscole e la stringa vuota.
   - Effetto collaterale: vedi R-864-1.
2. `clients/voice/ascolto.py:773` — quando il server risponde «fine», il messaggio nel log dipende da `seguito`, il parametro di `turno` (`clients/voice/ascolto.py:749`). Sul primo turno dice «richiesta scartata dal server…». Il comportamento non cambia (`chiudi=True`, svuota, `return False`).
   - Esito: ok. Il test `tests/test_unit_voce_ascolto.py:547` controlla anche che non ci siano bip né audio riprodotto.
3. `clients/voice/ascolto.py:1485` — `descrivi_modello`, usata nel log «ascolto pronto» di `clients/voice/ascolto.py:1706`, distingue tre casi: nome invariato, ripiego, file nostro.
   - Esito: ok, R-855-1 è chiusa. Il test `tests/test_unit_voce_ascolto.py:3377` copre i tre casi. Vedi R-864-2.

**Riserve (da tracciare in stato_progetto.md)**

- **R-864-1 BASSA** (`clients/voice/ascolto.py:1456`):
  - Prima openWakeWord accettava anche nomi di modelli pronti scritti con spazi o con la versione (es. «hey mycroft», «alexa_v0.1»), perché li confrontava per pezzo di nome. Ora ripiegano su hey_jarvis, con l'avviso nel log. Per hey_jarvis il risultato è identico; per gli altri modelli pronti cambia parola in silenzio, salvo il log.
  - `verifica_della_voce` cerca il filtro col nome grezzo: con un nome ripiegato (es. «Hey_Jarvis») un filtro hey_jarvis già addestrato non si carica.
  - Proposta: normalizzare il nome (minuscole, spazio → `_`) prima della regex, oppure documentare che vale solo il nome esatto.
- **R-864-2 COSMETICA** (`clients/voice/ascolto.py:1488`): `descrivi_modello` richiama `modello_della_parola`, quindi all'avvio l'avviso di ripiego compare due volte nel log. Basterebbe passarle il risultato già calcolato.
- **Da prima, ancora aperta** (nota, non nuova): se il file di ehi_jarvis_it manca e si ripiega su hey_jarvis, resta la `GAS_ASCOLTO_SOGLIA=0.5` scritta da installa.sh per il modello italiano.
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello nuovo non è misurata.

**Rischi esclusi**

- Ho preso per buona la prova dal vero del 25/11 sul Mac (richiesta di 1,0 s, il server chiude con `X-Gas-Comando: fine`). Il log del server non è nel repo.
- Non ho verificato che il server mandi «fine» solo per trascrizioni vuote o non chiare: modules/voice/ non è nel diff. Il nuovo messaggio dice «di solito», quindi non lo afferma come certo.
- Comportamento con openWakeWord vero: non l'ho riprovato, qui il pacchetto non è installato nell'ambiente dei test.

**Memoria**: aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md la riga #864 e una lezione (una funzione che descrive per il log non deve richiamare la funzione che decide e logga, altrimenti gli avvisi si duplicano). Già committate da sole (5586236b).

Il commit è consentito.
```

```
## VERDETTO: APPROVATO CON RISERVE

Review #865, solo il delta rispetto alla #864 su fix/voce-log-e-modello. L'indice ora vale 2 file, +68/−6. Ho rieseguito la suite tests/test_unit_voce_ascolto.py: 394 passati. Non ho usato git stash e l'indice è intatto.

R-864-1 è chiusa. R-864-2 è chiusa solo in parte: l'avviso di ripiego esce ancora due volte (sotto). Non blocca il commit.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1690` — in `main` il nome preso da `GAS_ASCOLTO_MODELLO` ora si pulisce (spazi ai lati, minuscole, spazi interni → `_`) prima di `verifica_della_voce` e del rilevatore.
   - Rischio: aprire una strada a un percorso.
   - Esito: ok. «/TMP/X.ONNX» diventa «/tmp/x.onnx», che la regex continua a rifiutare, quindi si ripiega comunque. Un filtro hey_jarvis già addestrato ora si carica anche con «Hey Jarvis» nel .env.
   - R-864-1 è chiusa per spazi e maiuscole. I nomi con la versione («alexa_v0.1») restano un ripiego dichiarato nell'avviso: va bene così.
2. `tests/test_unit_voce_ascolto.py:192` — test nuovo: «  Hey  Jarvis » produce «parola «hey_jarvis»» nel log, senza avviso di nome non valido.
   - Esito: ok, il test copre il caso.
   - COSMETICO: la lista `visti`, che raccoglie i nomi passati al rilevatore, non viene mai controllata. Un `assert visti == ["hey_jarvis"]` proverebbe che anche il rilevatore riceve il nome pulito. Ci sono anche 3 righe vuote prima del `@pytest.mark.parametrize` successivo.
3. `clients/voice/ascolto.py:1485` — `descrivi_modello(modello, usato)` ora riceve il risultato già calcolato e non richiama più `modello_della_parola`.
   - Esito: ok nella funzione.
   - Però `main` a `clients/voice/ascolto.py:1709` chiama di nuovo `modello_della_parola(modello)`. La chiama già `rilevatore_openwakeword` a `clients/voice/ascolto.py:1538`. Quindi all'avvio, quando si ripiega, l'avviso esce ancora due volte (vedi R-864-2).

**Riserve (da tracciare in stato_progetto.md)**

- **R-864-2 COSMETICA, ancora aperta**: le chiamate a `modello_della_parola` all'avvio sono ancora due (`clients/voice/ascolto.py:1538` e `clients/voice/ascolto.py:1709`). Correzione semplice: calcolare `usato` una volta in `main` e passarlo al rilevatore, oppure far restituire `usato` a `rilevatore_openwakeword`.
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello italiano non è misurata.
- Ancora aperta, da prima: se il file manca, il ripiego su hey_jarvis resta con la `GAS_ASCOLTO_SOGLIA=0.5` scritta da installa.sh.

**Rischi esclusi**

- Il comportamento con openWakeWord vero e sul Mac: qui il pacchetto non c'è nell'ambiente dei test.
- La parte del diff già vista nella #864 (log del «fine» sul primo turno, ripiego per i nomi non semplici): non l'ho riesaminata.

**Memoria**: aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md la riga #865, con la lezione «una correzione di una chiamata doppia va verificata contando le chiamate col grep, non leggendo solo la funzione corretta». Già committata da sola (98ec858e).

Il commit è consentito.
```

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_voce_ascolto.py`: 391 → 394 passed (3 test nuovi, 1 aggiornato).
- Suite completa: non rilanciata in questo container. La CI la esegue sul push.

## §6 STATO CI

Nessuna run su c46b0b86, 98ec858e e 5586236b alla scrittura: vanno col push di questo commit di fine-task. La run del commit di fine-task non è ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-864-2 COSMETICA: all'avvio l'avviso di ripiego compare due volte (`modello_della_parola` chiamata dal rilevatore e da `main`).
- R-854-3 BASSA: interruzione col modello italiano non misurata.
- Ripiego su hey_jarvis con la soglia 0,5 (bot #405): BASSA, aperta.
- Chiuse: V-1 bot #405 (nome non semplice), R-855-1, R-864-1.
- Riserve delle altre chat: in `reports/stato_progetto.md`.
