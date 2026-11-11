# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 notte — Blocco esteso dei nomi: dati dei clienti mai ai cervelli gratuiti (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione (branch feat/merge-automatico-z1xjx2 → main): numero e URL dall'output di `create_pull_request` dello strumento GitHub (gh assente), riportati nel riepilogo all'operatore.
2. Effetto della regola: anche un `ricorda` usato solo per la conoscenza caricata manda il turno al forte. Va bene così? sì/no

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — finestra con dati di lead → solo il forte**: FATTA.
- **Fetta 2 — recap e lezioni filtrati per i non forti**: FATTA.
- **Fetta 3 — riflessione con dati di lead solo al forte**: FATTA.
- **Fetta 4 — confronto dei nomi più robusto (NFKD, lapidi, telefoni, parole corte, tipo)**: FATTA.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 gas.py                             | 292 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------
 modules/memory/store.py            |  17 +++++++++++------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  21 ++++++++++-----------
 tests/test_unit_kernel.py          | 330 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

- Kernel (`PYTHONUTF8=1 python tests/test_unit_kernel.py`): 1135 PASS / 0 FAIL (main e3eb542) → 1157 PASS / 0 FAIL (rilanciato da M1 sul commit 863ca51c).
- `python -m pytest -q tests/test_unit_telegram_voce.py tests/test_unit_notte.py tests/test_unit_sottofondo.py tests/test_unit_gate.py tests/test_unit_manutenzione.py tests/test_unit_voice_server.py tests/test_unit_voce_ascolto.py -k "not browser"` → 1758 passed, 34 deselected (rilanciato da M1).

```
=== RIEPILOGO: 1157 PASS, 0 FAIL ===
```

Fuori scope: SKIP del kernel e test con «browser» (mancano bwrap, browser ed embedding nel container).

## §6 STATO CI

CI NON VERIFICATA (gh assente).
- 863ca51c: nessuna run su questo SHA (pushato insieme al commit di fine-task).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-766-1 BASSA — falsi positivi del confronto (es. «verde» da «Studio Verde Srl», cifre separate da spazi): turni mandati al forte senza bisogno (direzione sicura).
- R-766-2 BASSA — i round-trip vecchi passano dal forte finto senza controllare chi ha risposto.
- R-766-3 COSMETICA — due imprecisioni nella lettura dei contatti per memorie vecchie/finte.
- R-766-4 COSMETICA — il messaggio «solo col cervello forte» non dice che `clear` toglie il blocco.
- Effetto della regola (decisione in §0): anche un `ricorda` sulla sola conoscenza manda il turno al forte.
- Non provato: passaggio al `claude -p` vero sul Mac a metà turno.
- Restano aperte le riserve precedenti in reports/stato_progetto.md (R-744-M1-*, R-750-M1-2/3, ve #366 V-2/V-3).
