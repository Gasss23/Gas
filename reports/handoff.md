# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-20 — CRM fetta 7: note basse del bot e della verifica esterna sull'ultimo commit della PR #386, più R-820-1

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta. L'operatore ha già dato il via in chat il 20-11 («ok mergia quando è tutto verde»): la mergia l'agente con CI e bot verdi. PR #387 (https://github.com/Gasss23/Gas/pull/387), aperta dopo il push di 5f9d3c8c con l'etichetta «verifica».
2. Password delle copie cifrate nel `.env` del Mac (`GAS_CRM_BACKUP_PASSWORD`), salvata anche nel gestore di password.
3. Verificare che la cartella di Gas sia `~/Gas`, fuori da Scrivania e Documenti sincronizzate con iCloud.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 7 — note basse sull'ultimo commit della PR #386 (8a107c47) e R-820-1**: FATTA, commit 99e0dcb8. Review #821-CRM APPROVATO CON RISERVE (R-821-1 BASSA).
  - Bot V-1 (guida) e V-2 (indicatore se fallisce la copia locale).
  - Bot V-3 e verifica V-3 (temporaneo del ripristino).
  - Verifica V-1 (disco non collegato), V-4 (file di lavoro come collegamento pendente) e V-5 (copia locale rovinata).
  - Residuo `.prova-*.tmp`.
  - R-820-1 (prova all'avvio con tempo massimo).
- **Regola in CLAUDE.md §10** (doc): non fermarsi ad aspettare il merge (operatore, 20-11).
- **Ancora aperte da prima** (vedi §7): falsi allarmi del filtro delle parole vietate (R-810-2) e il punto di mount rimasto in `/Volumes` (rischio non verificato del revisore).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 CLAUDE.md                          |   1 +
 modules/crm/__main__.py            |   9 ++------
 modules/crm/copia_cifrata.py       |  67 +++++++++++++++++++++++++++++++++++++++++++++++++++-------
 modules/crm/server.py              |  45 ++++++++++++++++++++++++---------------
 reports/crm/guida.md               |   4 ++--
 reports/diff_sessione.md           |  26 +++++++++++------------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  56 ++++++++++++++++---------------------------------
 tests/test_unit_crm.py             |  72 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base della sessione: 0aa26672 (origin/main, dopo il merge della PR #386).

## §3 GIT LOG --ONELINE (sessione)

```
5f9d3c8c docs(fine-task): CRM fetta 7 — note basse della PR #386 chiuse, review #821; regola «non fermarsi ad aspettare il merge»
99e0dcb8 fix(crm): copie fuori dal Mac più solide — disco non collegato, copia locale rovinata, temporaneo del ripristino esclusivo, avvio con tempo massimo, indicatore anche se fallisce la copia locale
1307a80f chore(revisore): memoria review #821 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #821-CRM (commit 99e0dcb8)

## VERDETTO: APPROVATO CON RISERVE

Review #821-CRM sul diff staged (4 file, +162/−31). Ramo ripartito da main 0aa26672 (PR #386 mergiata).

Chiude le note BASSE del bot e della verifica esterna su 8a107c47 e la mia R-820-1. Resta una sola riserva BASSA: con la copia esterna spenta, un fallimento della copia locale non si vede (R-821-1).

**Verifiche rifatte da me:**
- Suite CRM: 133 passed. mypy pulito su modules/crm.
- Fail-before su main 0aa26672 col file di test nuovo: falliscono i 2 test nuovi, 131 passano.
- Tre prove a mano (risultati sotto):
  1. disco non collegato;
  2. cartella che non risponde;
  3. copia locale fallita con la copia esterna spenta.
- Kernel non toccato. Nessuno slicing della history, nessuna simulazione di tool.

### Riserva

**1. R-821-1 — BASSA — con la copia esterna spenta, un fallimento della copia locale non si vede.**
- **Prova:** senza password, cioè con la copia esterna spenta, `_copia_giornaliera` (`modules/crm/server.py:297`) segna l'esito come `{'spenta': True, 'ok': None, 'motivo': 'la copia sul Mac non è riuscita…'}`.
- **Cosa vede l'operatore:** la dashboard mostra «☁ copia spenta», non il rosso. Il fallimento della copia locale compare solo nel title e nel log, e non parte nessun avviso.
- **Perché pesa poco:** con la copia esterna attiva, cioè il caso scelto dall'operatore, il fallimento invece si vede e parte l'avviso: il V-2 del bot è chiuso.
- **Rimedio:** un campo a parte per la copia locale, o il rosso anche quando la copia esterna è spenta.

### Elementi del diff esaminati

- **`modules/crm/copia_cifrata.py:107` — la cartella delle copie si crea solo se esiste quella che la contiene** (niente più `parents=True`), sia nella prova sia nella copia.
  - Prova a mano: con la cartella su un disco «non collegato», l'avvio dice «NON FUNZIONA (… non c'è (disco non collegato?) …)» e non viene creata nessuna cartella sul disco del Mac.
  - Rischio esaminato: una copia che «riesce» senza uscire dal Mac.
  - Esito: ok.
- **`modules/crm/copia_cifrata.py:198` — `_integro` sulla copia locale prima di cifrare.**
  - Rischio esaminato: una copia locale rovinata che sostituisce la copia buona del giorno, visto che il nome è per giorno. Ora la copia del giorno resta quella di prima, e il test lo controlla.
  - Esito: ok.
- **`modules/crm/copia_cifrata.py:288` — temporaneo del ripristino unico e creato in esclusiva.**
  - Con O_EXCL l'apertura fallisce anche su un collegamento simbolico, anche pendente, quindi non scrive mai dentro un altro file.
  - Su `FileExistsError` il file non è nostro e il `finally` non lo tocca.
  - Il controllo dei file di lavoro ora vede anche i collegamenti pendenti (`modules/crm/copia_cifrata.py:275`).
  - I `.prova-*.tmp` più vecchi di un'ora vengono tolti (`modules/crm/copia_cifrata.py:235`).
  - Esito: ok.
- **`modules/crm/copia_cifrata.py:146` — `esito_all_avvio`:** la prova gira in un thread daemon con tempo massimo, e `serve` stampa solo la riga che ne esce (`modules/crm/__main__.py:131`).
  - Prova a mano con una prova che dura 30 s: «NON VERIFICATA» dopo 1,0 s, e il server parte.
  - Chiude R-820-1. Il thread bloccato resta daemon e non trattiene l'uscita del processo.
  - Esito: ok.
- **`modules/crm/server.py:297` — `_copia_giornaliera` e `_segna_copia`:** copia locale nel guardiano, copia esterna in un thread a parte (resta valida R-815-4).
  - Se la copia locale fallisce, l'indicatore passa a «NON riuscita» e parte l'avviso, ma solo con la copia esterna attiva (vedi R-821-1).
  - L'avviso non contiene dati dei clienti.
  - Esito: ok, salvo R-821-1.
- **`tests/test_unit_crm.py:1648` e `tests/test_unit_crm.py:1708`:** coprono disco non collegato, copia locale rovinata, `.prova` vecchia, collegamento simbolico al posto del temporaneo, journal pendente, prova lenta, copia locale fallita.
  - Sul codice di main falliscono entrambi.
  - Esito: ok.

### Rischi esplicitamente NON verificati

- Su macOS, a volte un punto di mount resta in `/Volumes` come cartella vuota anche a disco staccato. In quel caso `_genitore_assente` vedrebbe la cartella «che la contiene» e la copia finirebbe sul disco del Mac. Qui non è riproducibile, e il default (iCloud Drive) non è toccato. Per un disco esterno si potrebbe controllare che il percorso sia davvero un mount (`os.path.ismount`).
- Comportamento vero di iCloud Drive e dei permessi di macOS: non c'è un Mac qui.
- Documenti fuori stage (guida, frase di CLAUDE.md §10): non letti.

### Note

- Restano aperte dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Riga contatore #821-CRM aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (commit 1307a80f). Il diff staged è intatto (4 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_crm.py`:** 131 su main 0aa26672 → 133 passed. I 2 test nuovi (`test_ve386c_note_del_terzo_giro`, `test_v2_bot386c_copia_locale_fallita_si_vede`) falliscono sul codice di main (2 failed, 131 passed).
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.
- **mypy:** 0 errori in `modules/crm`.

## §6 STATO CI

`gh run list` non usato: in questa sessione cloud GitHub si interroga con gli strumenti MCP.
- La PR #386 è mergiata, con CI verde su 8a107c47: unit-suite 44646271307 success, handoff-check success, verifica-bot success.
- Mappatura commit→run:
  - `1307a80f`, `99e0dcb8`: run non ancora disponibile alla scrittura dell'handoff. Saranno pushati insieme al commit di fine-task che contiene questo file.
  - `5f9d3c8c` (primo fine-task della fetta): run appena partita al push, esito non ancora disponibile alla scrittura dell'handoff.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-821-1 (BASSA):** con la copia esterna spenta, un fallimento della copia locale appare come «☁ copia spenta» e non come rosso, e non parte nessun avviso. Con la copia attiva (la scelta dell'operatore) si vede.
- **Rischio non verificato (revisore #821):** su macOS un punto di mount vuoto rimasto in `/Volumes` farebbe passare il controllo del disco non collegato. Si applica solo con `GAS_CRM_BACKUP_CIFRATO_DIR` su un disco esterno; il default iCloud non è toccato.
- **Chiuse in questa fetta:**
  - V-1/V-2/V-3 del bot su 8a107c47 (V-4 era documentale);
  - V-1/V-3/V-4/V-5 della verifica esterna #386 (3° giro, https://github.com/Gasss23/Gas/pull/386#issuecomment-7026471536);
  - R-820-1.
- **Ancora aperte da prima:** R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4 (vedi `reports/stato_progetto.md`).
