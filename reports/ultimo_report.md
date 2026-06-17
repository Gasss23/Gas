# CHIUSURA FASE 2 memoria — declassamento `unisci_contatti` a manutenzione umana + igiene

**Data:** 2026-06-17
**Commit motore:** `0240161` (revisore #21 — APPROVATO, 1 nota cosmetica chiusa in sessione)
**Commit doc:** vedi sotto (stampato a fine task)
**Suite:** **135/135, 0 FAIL** (era 132)
**Scope (gate STRETTO rispettato):** nessuna feature nuova, nessun un-merge, nessuno
Strato B, **NESSUNA modifica a store.py** (meccanismo di merge intatto).

---

## PUNTO 1 — MOTORE: `unisci_contatti` fuori dall'autopilot (modifica principale)

**Decisione architetturale:** il merge di lead è mutante e IRREVERSIBILE (lossy,
COALESCE senza inverso pulito). Un modello in autopilot h24 su VPS non deve poterlo
invocare da sé — stessa classe del restore di snapshot e del `git gc`, già "solo
umano". Il dedup mancato è recuperabile; un merge errato no.

In `gas.py`:
- **rimossa** l'entry `unisci_contatti` da `tools_schema` (il modello non lo vede più);
- **rimosso** il ramo `elif name == "unisci_contatti"` da `execute_tool_call`: ora cade
  nel `else` → `"Tool non trovato."`;
- l'handler **`_unisci_contatti` RESTA** come metodo richiamabile (uso manuale/futuro),
  con docstring aggiornata: è MANUTENZIONE UMANA, non tool autopilot, e perché
  (irreversibile/lossy, classe restore/gc);
- `_riassumi_args` **lasciato invariato** (il caso `unisci_contatti`): scelta esplicita,
  l'handler resta richiamabile (il mandato: "se l'handler resta richiamabile, lascialo").

Il **MECCANISMO** di merge in `MemoryStore` (`unisci_contatti`, `merged_into`,
`_ensure_columns`, risolutore canonico) **NON è toccato** (store.py non nel diff).

## PUNTO 2 — MOTORE: coerenza whitespace in `_trova_contatto`

Il confronto substring usava `termine.lower()` senza collassare il whitespace, mentre le
chiavi storate sono normalizzate. Ora il collasso si applica a **ENTRAMBI i lati**
riusando `normalizza_chiave` SOLO ai fini del confronto (needle e haystack chiave+nome):
un needle `"anna   rossi"` trova lo storato `"anna rossi"`. Il ramo **match-esatto**
(`get_contatto_per_chiave`) **NON toccato**.

## PUNTO 3 — MOTORE (cosmetico): chiude R-crm-norm-1

I messaggi di **successo** di `_salva_contatto`/`_imposta_stato_contatto` mostrano ora la
chiave nella forma CANONICA persistita (`normalizza_chiave(chiave)`): schermo e DB
coincidono. Solo il testo del messaggio.

## PUNTO 4 — DOC (no review)

In `reports/stato_progetto.md`: (a) **R-crm-1b** spostato da ✅CHIUSA a **🟡 MITIGATA**
(dedup cross-formato non prevenuto; meccanismo di merge come manutenzione umana; difesa
preventiva "chiave canonica" candidata, non presa); (b) voce motore "Fusione lead
cross-formato" riscritta (merge non più tool autopilot, e perché); (c) **R-crm-norm-1**
marcata CHIUSA; (d) paragrafo "Istituzioni di processo C" riscritto pulito (era #18
duplicato + narrazione doppia) — ultima review ora **#21** (lo stato reale è oltre il
"#19" indicato nel mandato, scritto prima delle review #20/#21). Registrato che lo
**Strato B del Vector DB è CONGELATO** (FTS5 basta; si rivaluta solo se il funnel reale
lo richiede) e che un **un-merge è NON necessario** col merge manuale.

---

## VERIFICHE (eseguite e dimostrate)

### A. Suite completa
`python tests/test_unit_kernel.py` → **`=== RIEPILOGO: 135 PASS, 0 FAIL ===`** (era 132).

### B. `git diff --cached --stat` (commit motore `0240161`)
```
 gas.py                    | 49 +++++++++++++++++++++-------------
 tests/test_unit_kernel.py | 65 +++++++++++++++++++++++++++++++++++++++++-----
 2 files changed, 89 insertions(+), 25 deletions(-)
```
SOLO `gas.py` + `tests/`. **`modules/memory/store.py` NON nel diff** (verificato:
`git diff --stat modules/memory/store.py` vuoto). Le invarianti motore
(`_get_window`/`_cap_window_chars`/`for _ in range(10)`/bwrap/`_snapshot`) e i simboli
del meccanismo (`merged_into`/`_ensure_columns`/`diario_fts`/`cerca_diario`) NON
compaiono nel diff di `gas.py`.

### C. `unisci_contatti` non più esposto, meccanismo intatto (grep)
- `grep -c '"name": "unisci_contatti"' gas.py` → **0** (fuori da `tools_schema`)
- `grep -c 'elif name == "unisci_contatti"' gas.py` → **0** (fuori dal dispatcher)
- `def unisci_contatti` / `merged_into` / `def _ensure_columns` → **presenti in
  `modules/memory/store.py`** (meccanismo INTATTO)
- handler `_unisci_contatti` ancora presente in `gas.py` (richiamabile a mano)

### D. Esito dei nuovi test
```
[PASS] T28a unisci_contatti fuori da schema+dispatcher, meccanismo manuale intatto
[PASS] T28b _trova_contatto: whitespace multiplo nel needle trova lo storato normalizzato
[PASS] T28c messaggi di successo mostrano la chiave normalizzata (R-crm-norm-1)
```
I T24a-f (merge nello store) restano **verdi**: T24a/c/d migrati da
`execute_tool_call("unisci_contatti", ...)` (path tool rimosso) all'handler
`_unisci_contatti(...)` — stesso output, asserzioni invariate; T24b/e/f usano già lo
store direttamente.

---

## PROCESSO
- **Gate di review §3**: PUNTI 1-3 toccano `gas.py`/`tests/` → subagent **revisore**
  invocato sul diff staged PRIMA del commit → **APPROVATO** (review #21). Unica nota
  cosmetica (commento su `_trova_contatto` impreciso sul `nome` non normalizzato in
  storage) **chiusa in sessione** affinando il commento. PUNTO 4 doc-only → no review.
- Hook deterministico onorato (`.claude/.review_ok` creato per il commit, rimosso subito dopo).
- `stato_progetto.md` e `diff_sessione.md` aggiornati.

---

## §FINALE — Fuori da questo mandato (NON eseguito, scope umano)
- **Difesa PREVENTIVA di R-crm-1b**: policy di chiave canonica (preferire SEMPRE l'email
  quando disponibile) per evitare a monte il dedup cross-formato. Scelta di semantica
  della rubrica, NON presa.
- **Un-merge / reverse-merge**: NON necessario finché il merge è manuale. Se un domani il
  merge tornasse automatico servirebbe; oggi no. Registrato, nessun impegno.
- **`GAS_MEMORY_PIN_SCAN`** env override e **R-crm-2** (`int(c["id"])`): già tracciati tra
  i finding 🟡, fuori scope qui.
