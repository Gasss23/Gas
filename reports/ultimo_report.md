# Memoria FASE 2 — Onestà tracking R-crm-1 (doc) + blindatura substring↔normalizzazione (test)

**Data:** 2026-06-17
**Commit test:** `f4b2321` (review revisore APPROVATO)
**Commit doc:** vedi sotto (stampato a fine task)
**Suite:** **112/112, 0 FAIL** (era 110)
**Scope:** UN punto doc (PUNTO 1) + UN punto test (PUNTO 2). NESSUNA modifica a `gas.py`.
Gate di scope rispettato: read-path (`_trova_contatto`) NON toccato; env override / fix
echo / Vector DB / merge tool solo proposti nel §FINALE.

---

## PUNTO 1 — DOC: split di R-crm-1 (chiusa solo a metà)

In `reports/stato_progetto.md` la voce dichiarava "R-crm-1 CHIUSA via normalizzazione".
Vero **solo per metà**: `normalizza_chiave` (lower + collapse-whitespace) unisce chiavi
che differiscono solo per case/spazi della STESSA stringa (`"Anna"` / `" ANNA "` → un
record), MA NON unisce identità cross-formato:
`normalizza_chiave("anna@ex.com")="anna@ex.com"` e `normalizza_chiave("Anna")="anna"` →
restano DUE record. Ed è proprio l'esempio testuale di R-crm-1.

Corretto il file vivo (NON `ultimo_report.md`/`diff_sessione.md`, che sono snapshot
storici) con uno split esplicito:

- ✅ **R-crm-1 (parte case/whitespace) — CHIUSA** (2026-06-17, `cdf764a`): chiavi che
  differiscono solo per maiuscole/whitespace della stessa stringa risolvono allo stesso
  record via `normalizza_chiave` (T23a/b; coerenza in lettura T23e).
- 🟡 **R-crm-1b (identità cross-formato) — APERTA**: stesso lead con chiavi
  semanticamente diverse (email a un turno, nome a un altro: `anna@ex.com` vs `Anna`).
  `normalizza_chiave` NON le unisce e non deve. Rischio di **QUALITÀ** del dato, non di
  sicurezza. **NON è un problema di migrazione** — esiste a runtime indipendentemente
  dallo stato del DB (il modello avrà a volte solo nome, a volte solo email per la stessa
  persona). Difesa candidata da PROGETTARE (fuori da questa fetta): policy di chiave
  canonica (es. preferire SEMPRE l'email come chiave quando disponibile) oppure un tool
  `unisci_contatti`/merge-lead. Nessun impegno preso.

---

## PUNTO 2 — TEST: blindatura interazione substring↔normalizzazione

### B. `_trova_contatto` — codice integrale (gas.py, INVARIATO) + risposte esplicite

```python
def _trova_contatto(self, termine: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if self.memory is None:
        return None, None
    esatto = self.memory.get_contatto_per_chiave(termine)
    if esatto:
        return esatto, None
    ago = termine.lower()
    cand = [c for c in self.memory.lista_contatti()
            if ago in (str(c.get("chiave", "")).lower() + " "
                       + str(c.get("nome", "")).lower())]
    if not cand:
        return None, None
    if len(cand) == 1:
        return cand[0], None
    # lista_contatti è ordinata per aggiornato_il DESC → cand[0] è il più recente
    nomi = ", ".join((c.get("nome") or c.get("chiave") or "?") for c in cand[:5])
    nota = (f"⚠ {len(cand)} lead corrispondono a '{termine}' ({nomi}…); mostro il "
            f"più recente. Usa la chiave esatta per disambiguare.")
    return cand[0], nota
```

- **(a) Il match-esatto passa per `get_contatto_per_chiave` o fa un confronto raw?**
  Passa per `get_contatto_per_chiave(termine)` → che **normalizza il termine** (stesso
  `normalizza_chiave` della scrittura). Quindi il match esatto è NORMALIZZATO su
  entrambi i lati (chiave storata normalizzata + termine normalizzato in lookup).
- **(b) Il confronto substring è case-insensitive su entrambi i lati?** **Sì**:
  `ago = termine.lower()` confrontato con `chiave.lower() + " " + nome.lower()`.
- **(c) Il termine subisce collapse del whitespace?** **No**: `ago = termine.lower()`
  applica solo `.lower()`, NON il `" ".join(split())`. (Limite noto: un needle con
  spazi multipli interni non combacerebbe con la chiave a spazio singolo; fuori dal
  caso dei test del mandato, NON corretto — vedi §FINALE.)

### Test aggiunti (zero token, locali, via tool reali) — T23e e T23f

- **T23e** — coerenza scrittura-normalizzata ↔ lettura-substring: salvo un lead con
  chiave `"  Anna   Rossi "` (storata `"anna rossi"`), poi `ricorda` con
  `contatto="anna rossi"` (risolve via match esatto normalizzato) e `contatto="ANNA"`
  (risolve via substring case-insensitive) → **TROVA** il lead in entrambi i casi.
  **PASS** — `T23e NON è fallito`: la lettura resta coerente con la scrittura
  normalizzata, **nessun gap di read-path da documentare**.
- **T23f** — onestà sul limite APERTO R-crm-1b: salvo `"anna@ex.com"` e `"Anna"` come
  due `salva_contatto` distinti → asserisco che restano **DUE record** (la
  normalizzazione NON fonde identità cross-formato), e che `get_contatto_per_chiave("Anna")`
  ha chiave storata `"anna"`. **PASS**. Test che incarna il limite, così nessun futuro
  intervento lo "aggiusta" per sbaglio.

---

## VERIFICHE (eseguite e dimostrate)

### A. Suite completa
`python tests/test_unit_kernel.py` → **`=== RIEPILOGO: 112 PASS, 0 FAIL ===`** (era 110).

### C. Esito singolo dei due test (dall'esecuzione reale)
```
[PASS] T23e lettura substring trova il lead salvato con chiave normalizzata — e1='CONTATTO Anna Rossi [nuovo] — prossima: — — note: —\nStoria:\n' e2='CONTATTO Anna Rossi [nuovo] — prossima: — — note: —\nStoria:\n'
[PASS] T23f (R-crm-1b APERTA) normalizzazione NON fonde identità cross-formato — n_record=2
```
T23e **PASS** (la lettura trova il lead) → non è scattata la clausola di STOP del
mandato; `_trova_contatto` NON è stato toccato.

### D. Diff del commit + invarianti
`git diff --cached --stat` del commit test `f4b2321`:
```
 tests/test_unit_kernel.py | 28 ++++++++++++++++++++++++++++
 1 file changed, 28 insertions(+)
```
**SOLO `tests/test_unit_kernel.py` toccato. `gas.py` INVARIATO** (confermato: il diff
staged su `gas.py`/`modules/` è vuoto, verificato anche dal revisore via mutation
testing con ripristino bit-identico).

---

## PROCESSO

- **Gate di review §3**: il commit dei test tocca `tests/` → subagent **revisore**
  invocato sul diff staged PRIMA del commit → **APPROVATO** (nessuna riserva). Mutation
  testing del revisore: mutando il `.lower()` del needle in `_trova_contatto`, T23e cade
  → il test morde davvero. Il PUNTO 1 è doc-only → nessuna review.
- Hook deterministico onorato (`.claude/.review_ok` creato per il commit test, rimosso
  subito dopo).
- `stato_progetto.md` (split R-crm-1/R-crm-1b + nuovi test) e `diff_sessione.md`
  aggiornati.

---

## §FINALE — Proposte FUORI da questo mandato (NON committate, scope deciso dall'umano)

Il GATE imponeva SOLO i due punti. Emerse durante il lavoro, NON eseguite:

1. **R-crm-1b (identità cross-formato)**: difesa da progettare — policy di chiave
   canonica (preferire l'email quando disponibile) oppure tool `unisci_contatti`/
   merge-lead. È una scelta di semantica della rubrica, non una svista da chiudere al
   volo.
2. **Collapse del whitespace sul needle di `_trova_contatto`** (limite (c) sopra): oggi
   il termine di ricerca subisce solo `.lower()`, non il `" ".join(split())`; un needle
   con spazi multipli interni non combacerebbe con la chiave a spazio singolo. Fix
   proposto (NON eseguito, tocca `gas.py` = modifica di semantica della lettura, fuori
   scope): normalizzare il needle SOLO ai fini del confronto substring, senza cambiare
   la semantica substring. Lasciato alla decisione umana. (NB: i test del mandato NON
   esercitano questo caso → nessun verde fittizio.)
3. **R-crm-norm-1** (eco RAW della chiave nei messaggi di successo dei tool) e
   **`GAS_MEMORY_PIN_SCAN`** env override: già tracciati tra i finding, fuori scope qui.
4. **Vector DB**: prossimo passo grosso di FASE 2, da progettare prima di implementare.

Nessuna di queste è stata toccata: lo scope lo decide l'umano, non il revisore.
