# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-27 — R2 Sanitize Hardening (fetta 2b chiusura riserve fetta A)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #100 (https://github.com/Gasss23/Gas/pull/100).

---

## §1 SCOPE & ESITO FETTE

- **Punto 1 — `_sanitize_memory_text` hardening**: `FATTA`
  Escape universale `<`→`&lt;` e `>`→`&gt;` (tutti i caratteri, non solo tag esatti); aggiunto C1
  (0x80-0x9F) alla regex. +7 test T65g (varianti bypass + C1). Review #105 APPROVATO.

- **Punto 2 — E2E reale su COPIA `.gas_memory.db`**: `FATTA`
  Root temporanea scratchpad, voce malevola `id=25` inserita. Pin mostra `&lt;/MEMORIA_DATI&gt;`
  (iniezione strutturale bloccata, 1 sola chiusura reale). 2 giri reali (gemini-flash-lite,
  gemini-flash): entrambi hanno CITATO il contenuto come dato, non obbedito al comando.
  Etichetta: **MITIGATO** (non CHIUSO).

- **Punto 3 — Discrepanza verdetto #104**: `FATTA`
  `memoria_revisore.md` contiene solo 1 riga di riepilogo (verbatim non recuperabile).
  Versione integrale (5 pt) è in `handoff.md` della sessione precedente; `ultimo_report.md`
  era una versione condensata (4 pt — punto 4 `gas.py:79` anti-injection perso). Annotato.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 gas.py                             |  13 +-
 reports/diff_sessione.md           |  25 ++--
 reports/handoff.md                 | 106 ++++++++--------
 reports/stato_progetto.md          |   4 +-
 reports/ultimo_report.md           | 245 +++++++++++++++++++++----------------
 tests/test_unit_kernel.py          |  23 ++++
 7 files changed, 236 insertions(+), 181 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
653c3f8 feat(r2-hardening): _sanitize_memory_text escape universale <> + C1 + T65g
2b6dcc7 chore(revisore): memoria review #105 — APPROVATO
```

---

## §4 VERDETTO DEL REVISORE

**Commit 653c3f8** tocca `gas.py` e `tests/test_unit_kernel.py` — verdetto integrale review #105:

> **APPROVATO**
>
> 1. `gas.py:51` — `text.replace('<','&lt;').replace('>','&gt;')`: sostituzione sequenziale
>    senza toccare `&`; rischio doppio-escape su entità preesistenti (`&lt;` già presente)
>    esaminato: il `<` in `&lt;` non esiste dopo la prima sostituzione, `&` non viene mai
>    toccato → nessun doppio-escape possibile. Esito: ok.
>
> 2. `gas.py:54` — regex `[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\x80-\x9f]`: copre correttamente
>    C0 senza TAB/LF + DEL + C1 completo (128–159). Esito: ok.
>
> 3. `tests/test_unit_kernel.py:4006` — ciclo T65g su 4 varianti bypass: condizione
>    `"<" not in _san and ">" not in _san` discriminante verso la vecchia implementazione
>    (escape solo tag esatti avrebbe lasciato `<` grezzo nelle varianti). Esito: ok.
>
> 4. Contratto caller: `_memoria_pin` e `_ricorda` aggiungono i tag wrapper DOPO la
>    sanitizzazione; diff non tocca quei caller; costanti `_MEMORIA_DATI_OPEN`/`_CLOSE`
>    restano usate dai caller (non dead code). Esito: ok.
>
> 5. Wall of Shame §5: conforme. Cap 10 iter (§8): intatto. `_get_window()`: non toccato.
>
> Rischio escluso: comportamento runtime provider LLM sul prompt con entità HTML non
> verificabile in review statica — E2E reale già eseguito (2 giri) dichiarato nel report.

---

## §5 DELTA TEST DEL MOTORE

**Prima (sessione precedente fetta 2):** 339 PASS, 5 FAIL
**Dopo (questa sessione):** 346 PASS, 5 FAIL

```
=== RIEPILOGO: 346 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile...
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS...
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS...
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS...
```

I 5 FAIL sono T11c2/T11e/T12a/T12c/T12e — bwrap macOS (F-mac-1, noto, fuori scope).
Nessun FAIL nuovo. Nuovi PASS: +7 (T65g).

---

## §6 STATO CI

```
completed	success	feat(r2-hardening): _sanitize_memory_text escape universale <> + C1 +…	CI	fix/r2-sanitize-hardening	push	36335558534	1m2s	2026-09-27T17:04:18Z
completed	success	Merge pull request #99 from Gasss23/feat/apprendimento-f2	CI	main	push	36327304930	55s	2026-09-27T14:49:23Z
completed	success	docs(handoff): path completo citazione store.py §4 (sblocco check_ver…	CI	feat/apprendimento-f2	push	36138728813	1m17s	2026-09-25T13:04:58Z
```

**Mappatura commit→run:**
- `653c3f8` (feat r2-hardening) — run `36335558534` su `fix/r2-sanitize-hardening`, **completed success** ✅
- `2b6dcc7` (chore revisore) — pushato in bundle con `653c3f8`; incluso nell'albero testato dalla run `36335558534`; SHA intermedio mai testato in isolamento

---

## §7 RISERVE APERTE

- **Etichetta MITIGATO (R2 fetta A)**: la sanitizzazione blocca l'iniezione strutturale (escape universale `<>`); quella comportamentale dipende dal modello. Testato solo con gemini-flash-lite e gemini-flash, 2 giri. Da re-testare al deploy VPS con diario reale e provider diversi.
- **Discrepanza verdetto #104** (annotata, non bloccante): `memoria_revisore.md` contiene solo 1 riga di riepilogo per #104; il verbatim non è recuperabile. La versione integrale (5 pt) vive solo in `handoff.md` della sessione 2026-09-25. Considerare in futuro di incollare il verbatim direttamente in `memoria_revisore.md`.
