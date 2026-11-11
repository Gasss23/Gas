# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 notte — Blocco esteso dei nomi: dati dei clienti mai ai cervelli gratuiti (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #375 (https://github.com/Gasss23/Gas/pull/375).
2. Effetto della regola: anche un `ricorda` usato solo per la conoscenza caricata manda il turno al forte. Va bene così? sì/no

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — finestra con dati di lead → solo il forte**: FATTA.
- **Fetta 2 — recap e lezioni filtrati per i non forti**: FATTA.
- **Fetta 3 — riflessione con dati di lead solo al forte**: FATTA.
- **Fetta 4 — confronto dei nomi più robusto (NFKD, lapidi, telefoni, parole corte, tipo)**: FATTA.
- **Fetta 5 — bot/ve #375 V-1 MEDIA (contatti illeggibili), traslitterazione, avviso del forte**: FATTA — 96092c7e, review #767-M1coord BOCCIATO → #768-M1coord APPROVATO CON RISERVE.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 gas.py                             | 324 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------
 modules/memory/store.py            |  17 +++++++++++------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  22 +++++++++++-----------
 tests/test_unit_kernel.py          | 372 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 tests/test_unit_notte.py           |  10 +++++++---
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
96092c7e fix(kernel): blocco dei nomi fail-closed con contatti illeggibili, traslitterazione, avviso del forte (bot/ve #375)
5e5a3bb7 docs(fine-task): blocco esteso dei nomi (R-753-M1-A)
863ca51c feat(kernel): blocco esteso dei nomi — dati dei clienti mai ai cervelli gratuiti (chiude R-753-M1-A)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

# Verdetti integrali del revisore — blocco esteso dei nomi

## Giro 1 — #766-M1coord

## VERDETTO: APPROVATO CON RISERVE

Review #766-M1coord del diff staged sul branch feat/merge-automatico-z1xjx2 (PR #370). Chiude R-753-M1-A: i dati dei clienti non vanno più ai cervelli gratuiti. Ho letto CLAUDE.md (§2, §5, §8, §9), la riga 378 di reports/stato_progetto.md e la mia memoria.

**Cosa ho esaminato**
1. `gas.py:215`: `_finestra_ha_dati_lead` riconosce nella finestra le chiamate e i risultati degli strumenti dei contatti, e i nomi noti anche dentro le chiamate a strumento. Rischio esaminato: chiamate a strumento in forma non-dict, contenuto None o a lista. `_add_to_history` le salva sempre come dict, le sonde danno l'esito giusto. **ok**
2. `gas.py:5313`: controllo a inizio turno sulla stessa finestra `self._get_window(_n_finestra)`. Rischio esaminato: slicing della storia (§5). Nessuno: l'unico `[:_i_coda]` (`gas.py:5700`) taglia la coda dei cervelli, non la storia. **ok**
3. `gas.py:5422`: controllo a metà turno prima di ogni chiamata a un cervello non forte. Poi il salto al forte (`gas.py:5695-5700`) e il messaggio dichiarato (`gas.py:5706`). Rischi esaminati:
   - il `break` non aggiunge «10 iterazioni»;
   - `_turno_tentati.pop()` scatta solo se quel cervello non era stato chiamato;
   - il forte non entra due volte in coda (la cascata «forte» contiene solo claude-cli);
   - tetto di 10 chiamate e budget invariati (§8).
   
   Il mio mutante che toglie il controllo viene ucciso (T115c3/c4). **ok**
4. `gas.py:5327-5334` e `gas.py:5430-5433`: memoria, lezioni e riassunto della sessione (recap) in versione piena solo al forte, anonima agli altri. Se la lettura dei contatti fallisce, lezioni e recap vengono tolti (fail-closed). Il mutante «recap anonimo = pieno» viene ucciso (T115d1/d3). **ok**
5. `gas.py:4358-4366` e `gas.py:4406-4432`: la riflessione con dati di clienti la fa solo il forte (ClaudeCliClient, tetto controllato, uso registrato anche se la chiamata fallisce). Forte spento o al tetto → riflessione rimandata, senza crash. Prima la cascata «complesso» non conteneva claude-cli, quindi `_rung_disponibile` non cambia il resto del comportamento. **ok**
6. `gas.py:4008`: `_contatti_per_filtro` legge i lead fusi (lapidi), con ripiego `getattr` e §9 (avviso nel log e `None`). Il mutante sul tipo della riga di diario viene ucciso (T115b2). **ok, con R-766-3**
7. `modules/memory/store.py:1262`: `leggi_contatti(includi_lapidi)` usa solo pezzi SQL fissi; il valore dello stato resta parametrizzato, quindi niente SQL iniettabile. Il comportamento di default non cambia. **ok**
8. `tests/test_unit_kernel.py:977`: `run_turn_scriptato` ora gira sempre con un forte finto. **riserva R-766-2**

Test del kernel rilanciati da me: 1157 PASS, 0 FAIL. `--check` pulito; ho ripristinato gas.py dopo i mutanti (`git diff` del working tree vuoto).

**Finding**
- **R-766-1-M1coord (BASSA)**: falsi positivi. Le parole comuni nei nomi d'azienda contano come nomi: con «Studio Verde Srl», la frase «il prato è verde» manda il turno al forte. In più il regex dei telefoni (`gas.py:202`) unisce cifre separate da spazi: «file da 1 2 3 4 5 6 7 byte» viene preso per un telefono. Effetto: turni in più sul tetto giornaliero del forte, e con il forte spento un rifiuto. Il limite dichiarato (b) copre la lista delle parole generiche, non questo.
- **R-766-2-M1coord (BASSA)**: `run_turn_scriptato` (`tests/test_unit_kernel.py:977`) accende il forte finto per tutti i test che lo usano. I test vecchi con `ricorda`/`salva_contatto` ora passano dal forte senza che nessuno controlli quale cervello ha risposto: un test pensato per il percorso dei gratuiti può non provarlo più.
- **R-766-3-M1coord (COSMETICA)**: due difetti in `_contatti_per_filtro`. Il ripiego su `lista_contatti` (`gas.py:4019`) trasforma un errore di lettura in «nessun contatto», quindi non è fail-closed (riguarda solo memorie vecchie o finte, non quella usata in produzione). E `except TypeError` (`gas.py:4022`) riprova senza lapidi anche quando il TypeError nasce dentro la funzione.
- **R-766-4-M1coord (COSMETICA)**: il messaggio «Questa richiesta contiene dati di clienti…» (`gas.py:5706`) non dice che il blocco dura finché i dati restano nella finestra, né che `clear` lo toglie.

**Cosa NON ho verificato**
- Il comportamento con il vero `claude -p` sul Mac quando il passaggio avviene a metà turno, con la storia che contiene chiamate a strumento fatte da Gemini: i test usano un forte finto e qui non posso riprodurlo.
- Le altre suite pytest (telegram, notte, sottofondo, gate, manutenzione, voce): 1758 passed secondo il chiamante, non rilanciate da me.
- Altri percorsi verso modelli esterni fuori da gas.py (la trascrizione Groq della voce è un'eccezione già accettata dall'operatore).

Ho aggiunto la riga #766-M1coord e una lezione in coda a `.claude/agents/memoria_revisore.md` e ho messo in stage solo quel file. Nessun commit, `commit_memoria_revisore.sh` non lanciato, come richiesto.

### Review #767-M1coord (1° giro sul fix di bot/ve #375)

## VERDETTO: BOCCIATO

Review #767-M1coord, sul diff staged del branch feat/merge-automatico-z1xjx2 (PR #375): gas.py, tests/test_unit_kernel.py, tests/test_unit_notte.py.

**Motivo bloccante (privacy, CLAUDE.md §2)**
- gas.py:4032: la scorciatoia `if getattr(self.memory, "available", True) is False: return []` introduce una regressione. `available=False` non vuol dire che il DB sia illeggibile. Succede anche con `ChiaveNormCollisione` (modules/memory/store.py:586) e con un `sqlite3.Error` all'avvio, per esempio un lock oltre i 10 s. In questi casi il DB resta leggibile, perché `leggi_contatti`, `lista_contatti` e `diario_recente` (modules/memory/store.py:1250, modules/memory/store.py:1240, modules/memory/store.py:1010) non controllano `available`.
- L'ho provato a mano: MemoryStore reale con il contatto «Mario Rossi», `available=False` impostato a mano.
  - `leggi_contatti` restituisce `['Mario Rossi']`, mentre `_contatti_per_filtro` restituisce `[]`.
  - `_finestra_ha_dati_lead("scrivi a Mario Rossi")` dà False, quindi il turno va ai gratuiti.
  - La variante anonima del pin, quella che va ai gratuiti, contiene «- [email_inviata] mandata offerta a Mario Rossi». Con `available=True` la stessa riga esce come «(dettagli di un lead omessi…)».
- Prima di questo diff, nello stesso scenario, la lettura riusciva e i nomi venivano riconosciuti. Il fix peggiora quindi il caso che voleva rendere più prudente, e il commento «nessun contatto leggibile da nessuna parte (né pin né strumenti)» è falso.
- Correzione proposta:
  - provare comunque la lettura;
  - restituire `[]` solo se `available is False` e anche la lettura fallisce (allora il DB è davvero illeggibile, diario compreso);
  - in alternativa, fare rispettare `available` a tutti i lettori (pin/diario/strumenti).
- Serve un test con `available=False` e DB leggibile: nome nel testo, poi solo il forte, e il pin anonimo senza nome.

**Elementi del diff esaminati**
1. gas.py:234: con `identificativi is None` la funzione restituisce True (fail-closed), prima del controllo sugli strumenti. Rischio esaminato: un nome che passa ai gratuiti quando la lettura fallisce. Esito: ok. T115c8 (forte risponde, gratuito non visto) e T115c9 (forte spento: errore dichiarato, nessun gratuito) passano, rieseguiti.
2. gas.py:4032: scorciatoia `available is False → []`. Rischio esaminato: falso negativo sui dati dei clienti. Esito: blocco (dettaglio sopra).
3. gas.py:5673: `avviso_ripiego` per il forte quando ci sono dati di clienti. Rischio esaminato: sovrascrivere un avviso §8 già presente. Esito: ok, perché `_info_ripiego` (gas.py:573) per claude-cli restituisce sempre "" (non è mai ripiego né versione leggera). Solo testo, la voce non è toccata. T115c10 passa.
4. gas.py:152: tabella `_TRASLITTERA` (ł ø đ æ ß þ ı ħ ŧ…) applicata prima di NFKD in `_normalizza_confronto`. Rischio esaminato: rottura del confronto o eccezioni. Esito: ok. `str.translate` non solleva e la funzione resta pura. T115a1b passa, e passa anche il riconoscimento «Soren Odegard» contro «Søren Ødegård».
5. tests/test_unit_kernel.py:13015 (T115a6, None ora True) e T115d3 (gratuiti mai chiamati, errore dichiarato): cambio di comportamento voluto. L'asserzione nuova è più forte della vecchia («niente lezioni/recap» diventa «nessuna chiamata»). Esito: legittimi, nessun indebolimento.
6. tests/test_unit_notte.py:2421: è stata tolta l'asserzione `== 0` sul ritorno di `_giro` invece di aggiornarla. L'ho verificato a mano: ora il ritorno è 1. Esito: riserva BASSA, va asserito `== 1`, altrimenti il test non distingue un giro che crasha a metà dopo aver scritto il riepilogo. Il resto (`script.visti == []`, riepilogo «non letti», Telegram) va bene.

Suite: kernel 1161 PASS 0 FAIL (rieseguita); il test notte `-k contatti_illeggibili` passa (2 passed). Nessuno slicing della storia (la finestra passa sempre da `_get_window`, gas.py:5332). Nessuna eccezione nuova che si propaga.

**Riserve minori (da sistemare insieme al fix)**
- BASSA: il punto 6 sopra.
- COSMETICA: il commento a gas.py:5326 («resta il controllo sugli strumenti») è stantio dopo V-1.
- COSMETICA: con la lettura fallita il messaggio di stop di T115c9 dice «Questa richiesta contiene dati di clienti», ma non lo si sa. Meglio «potrebbe contenere» o «contatti illeggibili».

**Rischi esplicitamente esclusi**
- Suite pytest completa (1758) non rieseguita: ho eseguito solo il test notte toccato e la suite kernel.
- Comportamento su VPS con lock reale all'avvio non riprodotto: ho simulato `available=False` impostandolo a mano.
- Il caso `ChiaveNormCollisione` non l'ho costruito end-to-end: ho dedotto dal codice (modules/memory/store.py:586) che il DB resta leggibile in quello stato.

Memoria: in /home/user/Gas/.claude/agents/memoria_revisore.md ho aggiunto la riga contatore `#767-M1coord — 2026-11-11 — BOCCIATO — …` e una lezione: un flag diagnostico come `available` non equivale a «dati illeggibili» se altri lettori lo ignorano. Il file è in stage (git add). commit_memoria_revisore.sh non è stato lanciato, come richiesto.

### Review #768-M1coord (2° giro, commit 96092c7e)

## VERDETTO: APPROVATO CON RISERVE

Secondo giro della review #767-M1coord (numero di contatore #768-M1coord) sul diff staged del branch feat/merge-automatico-z1xjx2 (PR #375). Il blocco del primo giro è chiuso: si può committare, con le riserve sotto.

**Elementi del diff esaminati**
1. **gas.py:4045** — `_contatti_per_filtro` ora legge sempre i contatti (gas.py:4028-4039) e restituisce `[]` solo se `letti is None` e `available is False`.
   - Rischio esaminato: la regressione del primo giro, cioè `available=False` con DB leggibile che faceva arrivare i nomi ai gratuiti.
   - Esito: **ok**. Ho rifatto a mano l'esperimento del blocco: MemoryStore reale con «Mario Rossi» e `available=False`. Il filtro restituisce la riga, `_finestra_ha_dati_lead("scrivi a Mario Rossi")` dà True e il pin anonimo mostra «(dettagli di un lead omessi…)» senza il nome.
2. **tests/test_unit_kernel.py:13179-13190** — T115c11: `available=False` con DB leggibile; deve rispondere solo il forte e il pin anonimo non deve contenere «Mario Rossi».
   - Rischio esaminato: un test che non uccide la vecchia scorciatoia.
   - Esito: **ok**. Ho rimesso a mano nel working tree la scorciatoia del primo giro: T115c11 FAIL (risponde gemini-flash «gratis»), 1161 PASS e 1 FAIL. Working tree poi ripristinato dall'index.
3. **tests/test_unit_notte.py:2422** — ora `assert _giro(...) == 1`, più `script.visti == []`.
   - Rischio esaminato: test indebolito.
   - Esito: **ok**. Il codice di ritorno 1 coincide con quello che avevo misurato al primo giro (compito fermo dichiarato). I test riallineati (T115a6, T115d3) sono legittimi.
4. **gas.py:5326** — commento corretto: identificativi None, quindi la finestra conta come «con dati di clienti». Esito: ok.
5. **gas.py:234, gas.py:5673, gas.py:152** — già esaminati al primo giro (fail-closed con None, avviso del forte, traslitterazione) e invariati. Esito: ok.

Esecuzioni: suite kernel **1162 PASS, 0 FAIL** (rieseguita); `test_unit_notte -k contatti_illeggibili` 2 passed. Nessuno slicing della storia (la finestra passa da `_get_window`). L'eccezione resta intercettata e loggata (gas.py:4037-4039), nessun crash.

**Riserve**
- **R-768-1 COSMETICA**: quando la lettura dei contatti fallisce, il messaggio di stop dice comunque «Questa richiesta contiene dati di clienti», ma non lo si sa. Meglio «potrebbe contenere». T115c2 fissa il testo esatto: va cambiato insieme.
- **R-768-2 BASSA**: con `available is False` e lettura fallita, `[]` dà per scontato che sia illeggibile anche il diario. Se si guastasse solo la tabella contatti e il diario restasse leggibile, le righe del diario con nomi arriverebbero ai gratuiti senza filtro. Caso raro; ha senso tracciarlo in stato_progetto.md.

**Rischi esplicitamente esclusi**
- Suite pytest completa (1758) non rieseguita: ho rieseguito solo la suite kernel e il test notte toccato.
- `ChiaveNormCollisione` e lock all'avvio non riprodotti end-to-end: ho simulato `available=False` impostandolo a mano, come in T115c11.
- Comportamento su VPS non verificato.

**Memoria**: ho aggiunto la riga `#768-M1coord — 2026-11-11 — APPROVATO CON RISERVE — …` in /home/user/Gas/.claude/agents/memoria_revisore.md, dopo la #767 del primo giro, e l'ho messa in stage (git add). Nessuna lezione nuova. Non ho lanciato commit_memoria_revisore.sh.

## §5 DELTA TEST DEL MOTORE

- Kernel (`PYTHONUTF8=1 python tests/test_unit_kernel.py`): 1135 PASS / 0 FAIL (main e3eb542) → 1157 PASS / 0 FAIL (863ca51c) → 1162 PASS / 0 FAIL (96092c7e, rilanciato da M1; T115c8 e T115c11 falliscono senza il fix).
- `python -m pytest -q tests/test_unit_telegram_voce.py tests/test_unit_notte.py tests/test_unit_sottofondo.py tests/test_unit_gate.py tests/test_unit_manutenzione.py tests/test_unit_voice_server.py tests/test_unit_voce_ascolto.py -k "not browser"` → 1758 passed, 34 deselected (rilanciato da M1 anche dopo 96092c7e).

```
=== RIEPILOGO: 1162 PASS, 0 FAIL ===
```

Fuori scope: SKIP del kernel e test con «browser» (mancano bwrap, browser ed embedding nel container).

## §6 STATO CI

CI NON VERIFICATA (gh assente) con `gh run list`; check run letti con lo strumento GitHub sulla PR #375:
- 5e5a3bb7: handoff-check success; verifica-bot failure (V-1 MEDIA, chiusa in 96092c7e).
- 863ca51c: nessuna run propria (pushato insieme a 5e5a3bb7).
- 96092c7e e commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-768-1 COSMETICA — messaggio di stop «contiene dati di clienti» anche con la lettura fallita.
- R-768-2 BASSA — available=False e lettura fallita → [] presume illeggibile anche il diario.
- Ve #375 V-3/V-4 BASSE — parole di 1-2 lettere mai cercate da sole; nomi spaziati o con caratteri a larghezza zero.
- R-766-1 BASSA — falsi positivi del confronto (es. «verde» da «Studio Verde Srl», cifre separate da spazi): turni mandati al forte senza bisogno (direzione sicura).
- R-766-2 BASSA — i round-trip vecchi passano dal forte finto senza controllare chi ha risposto.
- R-766-3 COSMETICA — due imprecisioni nella lettura dei contatti per memorie vecchie/finte.
- R-766-4 COSMETICA — il messaggio «solo col cervello forte» non dice che `clear` toglie il blocco.
- Effetto della regola (decisione in §0): anche un `ricorda` sulla sola conoscenza manda il turno al forte.
- Non provato: passaggio al `claude -p` vero sul Mac a metà turno.
- Restano aperte le riserve precedenti in reports/stato_progetto.md (R-744-M1-*, R-750-M1-2/3, ve #366 V-2/V-3).
