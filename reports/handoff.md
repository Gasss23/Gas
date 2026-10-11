# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — merge #175 + giro notturno senza la conversazione dell'operatore (PR #176)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #176 (https://github.com/Gasss23/Gas/pull/176). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"url":"https://github.com/Gasss23/Gas/pull/176"}`): `gh` nel container non è autenticato. Merge autonomo dell'agente solo con verdetto testuale del bot `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. Metodo di protezione del cancello: (A) scrittura solo in cartelle permesse, (B) lista di nomi vietati.
3. Aperte da prima: archivio verifiche esterne (a/b), roadmap, costo del bot di verifica, V-2 bot #163, V-2 verifica esterna #172, prova sul Mac.

---

## §1 SCOPE & ESITO FETTE

- **Merge di #175**: `FATTA` — su richiesta esplicita dell'operatore, merge commit `d92e874` (= BASE di questa sessione).
- **Fetta 1 — R-220-2**: `FATTA` — `GasKernel(carica_storia=False)` in `notte_cmd` e nella fabbrica di default.
- **Lista dei nomi vietati del cancello**: `SALTATA` — in attesa della scelta (A)/(B).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |   9 ++++++---
 modules/notte/notte.py             |   3 ++-
 reports/diff_sessione.md           |  11 ++++++-----
 reports/handoff.md                 | 227 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  28 ++++++++++------------------
 tests/test_unit_notte.py           |  44 ++++++++++++++++++++++++++++++++++++++++++++
 8 files changed, 146 insertions(+), 181 deletions(-)
```

Nota: i conteggi di righe dei report scritti dopo lo stat (`reports/handoff.md`) sono approssimati per costruzione. Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
63eb092 fix(notte): il giro notturno non legge né mette in quarantena la conversazione dell'operatore (R-220-2)
fc9b742 chore(revisore): memoria review #253 — APPROVATO
838f4e8 chore(revisore): memoria review #252 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE

### Review #252 (prima versione del diff di 63eb092)

## VERDETTO: BOCCIATO

La riserva R-220-2 non è chiusa. La modifica protegge solo il percorso di default di `esegui_notte`, ma in produzione quel percorso non viene mai usato.

**Elementi del diff esaminati**

1. `gas.py:661` — se `carica_storia` è False, `history=[]` e `_load_history` non viene chiamata (quindi niente quarantena). Rischio esaminato: qualcosa in `__init__` dopo la riga 661 che legge `self.history` o il file della storia. Ho controllato le righe 662-756: la storia non viene mai letta; `db_path` resta quello di default finché `_esegui_compito` (`modules/notte/notte.py:193-194`) non lo sposta in `notte_dir`. Il default `True` lascia invariati bot, voce, `rifletti_cmd` e REPL. Esito: **ok**.
2. `modules/notte/notte.py:396` — la fabbrica di default ora passa `carica_storia=False`. Rischio esaminato: che questa riga sia davvero il percorso usato in produzione. Esito: **blocco**, vedi il punto 3.
3. Contesto, `gas.py:3618` — `notte_cmd` chiama `esegui_notte(root_dir, kernel_factory=lambda r: GasKernel(root_dir=r))`. È l'unico percorso di produzione: il timer lancia `gas notte`, `main` (`gas.py:3664`) chiama `notte_cmd`. Questa fabbrica esplicita sostituisce quella di default e **non passa `carica_storia=False`**. Esito: **blocco**.
   - Riprodotto con il diff applicato: storia `{non json` in una root temporanea, poi la fabbrica presa da `gas.notte_cmd(root)`. Il file finisce rinominato in `.gas_history.json.corrupt.20261011-095756`, cioè esattamente il comportamento che R-220-2 voleva eliminare.
4. `tests/test_unit_notte.py:812-821` (`test_giro_crea_i_kernel_senza_storia`) sostituisce `gas.GasKernel` e chiama `esegui_notte` senza fabbrica. Così prova solo la fabbrica di default, che in produzione non gira. La mutation test riportata (1 failed) è vera ma copre il percorso sbagliato. Esito: **blocco**, perché il test dà una falsa garanzia.

**Correzione minima richiesta**
- `gas.py:3618`: aggiungere `carica_storia=False` alla lambda di `notte_cmd`. In alternativa, togliere del tutto la fabbrica esplicita e lasciare che si usi quella di default.
- Aggiungere un test sul percorso reale. Per esempio: sostituire `modules.notte.esegui_notte` (o `gas.GasKernel`) e verificare che `notte_cmd` produca un kernel con `carica_storia=False`. Oppure, con una storia corrotta, verificare che dopo la fabbrica di `notte_cmd` non esista nessun file `.corrupt.*`.

**Altri punti controllati (come richiesto)**
- `_save_history` (`gas.py:779`) scrive su `self.db_path`, cioè `notte_dir/storia_<nome>.json` dopo `_esegui_compito`. Il file temporaneo sta in `db_path.parent`. Non dipende dalla storia letta all'avvio: ok.
- `_diario_log` (`modules/notte/notte.py:230`) e `MemoryStore` non usano `history`: ok.
- `rifletti` / `rifletti_cmd` (`gas.py:3609`) non viene chiamato dal giro notturno e mantiene `carica_storia=True`, come deve.
- `_get_window` e i tetti non sono toccati. Nessuno slicing grezzo nel diff: ok.

**Rischio escluso**
- Non ho eseguito pytest né la suite del kernel: mi fido dei numeri riportati (861 passed, 715/0), perché il blocco è indipendente dalle suite e l'ho riprodotto a mano.
- Non ho verificato il comportamento sotto timer systemd su VPS: non è riproducibile in sviluppo. La catena timer → `main` → `notte_cmd` l'ho però verificata leggendo il codice.

**Memoria aggiornata**
Riga #252 e una lezione nuova (con una fabbrica iniettabile, cercare con grep i chiamanti che passano il parametro esplicitamente) aggiunte a `.claude/agents/memoria_revisore.md` e committate con `commit_memoria_revisore.sh` (838f4e8).

### Review #253 (diff finale di 63eb092)

## VERDETTO: APPROVATO

Il blocco della review #252 è risolto e la riserva R-220-2 è chiusa: anche nel percorso reale (`gas notte`) il giro notturno non legge più la conversazione dell'operatore né la mette in quarantena se è corrotta. Ho rieseguito i test, ripetuto la mutation test e riprodotto a mano il caso con storia corrotta.

**Elementi del diff esaminati**

1. `gas.py:3619` — `notte_cmd` ora passa `kernel_factory=lambda r: GasKernel(root_dir=r, carica_storia=False)`. È il percorso di produzione: il timer lancia `gas notte`, `main` (`gas.py:3664`) chiama `notte_cmd`.
   - Rischio esaminato: che la quarantena scatti ancora.
   - Ripetuto a mano lo stesso scenario della #252 (`.gas_history.json` = `{non json`, kernel costruito con la fabbrica presa da `notte_cmd`): `history == []`, file intatto, nessun `.corrupt.*`.
   - Tenere la fabbrica esplicita è ragionevole per il motivo dichiarato: quando `gas.py` gira come `__main__`, la fabbrica di default rifarebbe `from gas import GasKernel` caricando una seconda copia del modulo.
   - Esito: **ok**.
2. `gas.py:661` — se `carica_storia` è False, `history=[]` e `_load_history` non viene chiamata. Rischio esaminato: altri chiamanti che cambiano comportamento. Il default resta `True`; bot (`modules/telegram/bot.py:261`), voce (`modules/voice/server.py:269`), `rifletti_cmd` (`gas.py:3609`) e REPL sono invariati. Esito: **ok**.
3. `tests/test_unit_notte.py:824-840` (`test_gas_notte_reale_non_tocca_la_conversazione`) — sostituisce `modules.notte.esegui_notte` e chiama il vero `gas.notte_cmd`.
   - Rischio esaminato: che il test passi anche se la sostituzione non ha effetto. Non succede: `notte_cmd` fa `from modules.notte import esegui_notte` al momento della chiamata, quindi legge la versione sostituita.
   - Mutation test ripetuta (tolto `carica_storia=False` alla riga 3619): 1 failed, cioè proprio questo test. File ripristinato e confrontato con la versione staged: identico.
   - Esito: **ok**.
4. `modules/notte/notte.py:396` — la fabbrica di default è allineata (`carica_storia=False`) ed è coperta da `test_giro_crea_i_kernel_senza_storia`. Esito: **ok**.

**Dipendenze dalla storia letta all'avvio (controllo richiesto)**
Nessuna dipendenza: questa parte resta valida dalla #252.
- `_save_history` scrive su `db_path`, che `_esegui_compito` (`modules/notte/notte.py:193-194`) sposta in `notte_dir`.
- `_diario_log` e `MemoryStore` non usano `history`.
- `rifletti` non viene chiamato dal giro notturno.
- `_get_window` e i tetti non sono toccati; nessuno slicing grezzo della history.

**Test rieseguiti da me**
- `tests/test_unit_notte.py`: 52 passed.

**Rischio escluso**
- Non ho rieseguito la suite completa (862) né `tests/test_unit_kernel.py` (715/0): mi fido dei numeri riportati, perché il delta tocca solo la costruzione del kernel e la parte notte l'ho verificata direttamente.
- Non ho verificato il comportamento sotto timer systemd su VPS: non è riproducibile in sviluppo.

**Memoria aggiornata**
Riga #253 (nessuna lezione nuova) aggiunta a `.claude/agents/memoria_revisore.md` e committata (fc9b742). Il diff staged sotto review non è stato toccato.

(Modifiche dell'agente al testo dei verdetti: path assoluti scritti relativi; elenco «File rilevanti» finale omesso in entrambi.)

## §5 DELTA TEST DEL MOTORE

Notte 49 → 52 passed; `pytest tests/` 859 → 862 passed; kernel 715 PASS / 0 FAIL in locale (717 in CI).

```
52 passed in 4.52s
862 passed in 101.47s (0:01:41)
=== RIEPILOGO: 715 PASS, 0 FAIL ===
```

Mutation: fabbrica di default senza `carica_storia` → 1 failed; `notte_cmd` senza `carica_storia` → 1 failed (`test_gas_notte_reale_non_tocca_la_conversazione`).

## §6 STATO CI

`gh` non autenticato nel container; PR #176 appena aperta.

Per costruzione i commit intermedi sono ROSSI su `handoff-check`: fa fede la run sul commit di fine-task.

- `838f4e8`, `fc9b742`, `63eb092`: pushati insieme; run su `63eb092` attesa rossa su `handoff-check` per costruzione (gli altri non hanno una run propria).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna nuova da questa fetta.
- Cancello: residuo per nomi (V-1 verifiche esterne #175) in attesa della scelta (A)/(B).
- Decisioni dell'operatore aperte da prima (§0.3).
