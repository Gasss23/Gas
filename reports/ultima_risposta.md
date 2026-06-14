Ora ho la spiegazione completa, e non è un mio errore di scrittura: è **come funziona l'hook**. Leggendo `scrivi_rep.sh`:

- È uno **Stop hook**: gira alla fine di *ogni* turno finché in cronologia esiste un "scrivi rep".
- Salva **solo il blocco di testo** del mio messaggio che precede il trigger — **non** gli output dei comandi a terminale.

Le due conseguenze che stai vedendo:
1. **Si riscrive da solo a ogni turno** → la mia modifica manuale viene sovrascritta ogni volta (per questo "la vedi uguale a prima").
2. Il report integrale era un **output di comando** (`cat`), non testo del mio messaggio → l'hook non poteva catturarlo. Catturava solo il recap.

**La soluzione pulita, dentro il design dell'hook:** metto qui sotto il report **come testo del messaggio**; poi tu riscrivi `scrivi rep` e l'hook salverà *questa* risposta completa. Non serve toccare nulla a mano.

---

# 📄 REPORT FINE TASK — Consolidamento motore: TASK B (paracadute free) + TASK C (snapshot)

**Data:** 2026-06-14 · **Esito:** ✅ COMPLETATO · **Review:** #9 (TASK B) e #10 (TASK C), entrambe APPROVATO CON RISERVE · **Suite:** **75 PASS, 0 FAIL** (zero token LLM)

## DECISIONI UMANE RICHIESTE
Nessuna in questa sessione. Nessuno STOP è scattato: tutte le azioni sono verificabili dai test o report-only. In particolare il `git gc` (azione irreversibile) NON è stato eseguito né automatizzato — resta OPT-IN umano, oggi solo REPORTATO da `gas doctor` (vedi TASK C).

## (1) ESITO AUDIT STEP 0 — riconciliazione pre-blocco
- `git status` **pulito**, `git log origin/main..HEAD` **vuoto**: nessuna modifica non committata, nessun commit locale non pushato. **Niente lavoro perso.**
- La sessione precedente aveva **già completato e pushato TASK A** (commit `1cae65a`): costanti provider de-duplicate (`GEMINI_URL`, `GROQ_URL`, `OPENROUTER_URL`, slug dei modelli inclusi i due rung free) e helper `_parse_mode` condiviso da `__init__` e `doctor`. Presenti i test T16a/b/c.
- Confermato in codice ciò che `stato_progetto.md` dichiarava FATTO: `_cap_window_chars` + `_msg_chars` (WINDOW_CHAR_CAP, review #7) e blocco T14 nei test (review #8).
- **Baseline reale: 64/64** (non 61). Il delta +3 sono i T16 di TASK A: la sessione precedente è andata OLTRE la previsione della consegna. NON è codice mancante: lavoro genuino, già revisionato e pushato. Decisione: proseguire con TASK B e TASK C.
- Discrepanza nota e risolta: `ultimo_report.md` era fermo a review #6 / 52 test, non rigenerato dalla sessione interrotta. È stato RIGENERATO con lo stato reale.

## (2) LE TRE TASK

**TASK A — già chiuso dalla sessione precedente (verificato, non rifatto).** De-dup costanti provider (R3 #5) + parse `GAS_SANDBOX_MODE` unico init/doctor (R3 #6). Refactor puro. Commit `1cae65a` già pushato. T16c certifica che `__init__` e `doctor` risolvono lo STESSO mode (incl. ignoto → `os_strict`).

**TASK B — Integrità del paracadute free (chiude R1 #5, metà determ. R2 #5).**
- Sonda PRIMA di progettare: il singolo modello NON vive su `/models/<slug>` (404); vive su `<base>/models/<slug>/endpoints` → `{data:{...,endpoints:[{...,supported_parameters:[...]}]}}`. `supported_parameters` è **PER-ENDPOINT** (a livello `data` è `None`); `tools` nella lista = function calling. 404 confermato anche su slug fasullo.
- `doctor`: nuova voce "Paracadute / modello free", SOLO se `OPENROUTER_API_KEY` presente. 404 → **WARN** ("assente/rinominato"); `tools` assente → **WARN** ("degraderebbe a solo-testo"); presente+tool-capable → **OK**. GET di METADATI, nessuna generazione → "doctor non consuma token" intatto.
- `run_turn`: SOLO osservabilità (sez.9). Brain con modello fuori da `TOOL_CAPABLE_MODELS` → `logging.warning`. NESSUN skip, ordine del fallback INVARIATO. Rilevamento del degrado PER-TURNO RIMANDATO (falsi positivi).
- Helper: `_classify_free_model` (3 rami), `_probe_free_model` (`_fetch` mockabile), `_http_get_json` (404 senza raise), `_model_tool_capable`.

**TASK C — Manutenzione snapshot (chiude Prossimo passo #1, R2/R3 snapshot).**
- Retention IBRIDA dei ref `refs/gas/snapshots/*`: UNIONE di (ultimi `SNAPSHOT_KEEP=100`) e (più giovani di `SNAPSHOT_KEEP_DAYS=7`). I recenti sopravvivono anche a una sessione che ruota >100 ref. Helper PURI `_ref_age_epoch` (None → si TIENE, conservativo) e `_snapshot_retention` → `(keep, drop)`.
- PRUDENZA (§10, macchina del tempo): nessun prune distruttivo né `git gc` automatico. I ref oltre policy si rimuovono con `update-ref -d` (oggetto RECUPERABILE fino a `git gc`) e la rimozione è LOGGATA riga per riga.
- `snapshots.log`: gitignorato (`reports/snapshots.log[.1]`) + rotazione `.1` al cap `SNAPSHOT_LOG_MAX_BYTES`.
- `doctor` sezione 7 "Snapshot": SOLO REPORT (conteggio ref + hint oggetti loose via `count-objects -v` + dimensione log). `git gc` OPT-IN manuale.

## (3) TEST CHE MORDONO (zero token LLM) — output REALE
```
[PASS] T11f retention (ramo count, età disattivata) tiene solo gli ultimi N — refs=3 (limite 3)
[PASS] T16a _parse_mode normalizza i valori di mode — sb=os_with_fallback sh=dry_run
[PASS] T16b mode ignoto -> default (os_strict / guarded) — sb=os_strict sh=guarded
[PASS] T16c __init__ e doctor risolvono lo STESSO mode (incl. ignoto -> os_strict)
[PASS] T17a 404 -> WARN (modello free assente/rinominato)
[PASS] T17b modello senza 'tools' -> WARN (degrado a solo-testo)
[PASS] T17c modello presente + 'tools' dichiarato -> OK
[PASS] T17d classify: i tre rami sono distinti e corretti
[PASS] T17e _model_tool_capable: cascata tool-capable, ignoto -> False
[PASS] T18a recenti (<7gg) sopravvivono — keep=3 drop=4
[PASS] T18b vecchi oltre N E oltre T -> drop
[PASS] T18c keep_n protegge il vecchio dentro gli ultimi N
[PASS] T18d soglia più stretta -> set protetto diverso (mordace)
[PASS] T18e ref non parsabile -> tenuto (conservativo)
[PASS] T18f _ref_age_epoch parsa il ts dal nome ref

=== RIEPILOGO: 75 PASS, 0 FAIL ===
```
`gas doctor` provato dal vivo: `[OK] Paracadute modello free`, `[OK] Snapshot ref totali / oggetti loose / snapshots.log`. Nessun crash.

## Riserve tracciate (nessuna bloccante)
- **Review #9 (TASK B):** (1) due rami di sicurezza degli helper free senza test dedicato (solo copertura); (2) il warning `run_turn` si ripeterebbe fino a 10×/turno se un modello senza tool entrasse in cascata.
- **Review #10 (TASK C):** (1) `SNAPSHOT_KEEP_DAYS`/`SNAPSHOT_LOG_MAX_BYTES` non configurabili via env; (2) soglie magiche inline in doctor (cosmetico); (3) rotazione log a 1 generazione; (4) manca test dedicato per rotazione `.1` e per i 3 check di doctor sez.7 (provati dal vivo).

## File toccati
- `gas.py` (motore, 2 commit revisionati: TASK B + TASK C)
- `tests/test_unit_kernel.py` (T17, T18, T11f riadattato; 64 → 75)
- `.gitignore` (`reports/snapshots.log[.1]`)
- `reports/stato_progetto.md`, `reports/diff_sessione.md`, `reports/ultimo_report.md`
- `.claude/agents/memoria_revisore.md` (lezioni dei review #9 e #10)

## Conteggio finale suite
**75 PASS, 0 FAIL** (61 baseline review #8 + 3 T16 TASK A + 5 T17 TASK B + 6 T18 TASK C, con T11f riadattato).

## Commit della sessione
- `a9f1053` TASK B — integrità paracadute free (chiude R1 #5, metà determ. R2 #5)
- `35a9b7e` TASK C — manutenzione snapshot (retention ibrida + rotazione + report)
- (TASK A `1cae65a` già pushato dalla sessione precedente.)

## Prossimi passi
1. Rilevamento PER-TURNO del degrado a solo-testo (metà aperta di R2 #5; rimandato per falsi positivi).
2. Cap output dedicato per pipeline Whisper + `GAS_WINDOW_CHAR_CAP` e `GAS_SNAPSHOT_KEEP_DAYS` configurabili via env.
3. `git gc` OPT-IN dietro flag esplicito in `gas doctor` (azione irreversibile).

---

👉 **Adesso scrivi di nuovo `scrivi rep`**: l'hook prenderà *questo* messaggio (che è tutto testo) e salverà il report completo in `ultima_risposta.md`.

**Recap semplice:** non era un mio errore di scrittura — l'hook `scrivi_rep.sh` (1) si riscrive da solo a ogni turno, cancellando le modifiche manuali, e (2) salva solo il testo del messaggio, non l'output dei comandi (dov'era finito il report). Ho rimesso il report **dentro il testo** qui sopra: ora basta che riscrivi `scrivi rep` e il file verrà salvato completo.
