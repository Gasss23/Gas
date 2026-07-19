# Ultimo Report — R-crm-1b Fetta 2: idempotenza diario rileva_duplicati_email

**Data:** 2026-07-19
**Branch:** fix/crm-idemp-diario → PR su main (d9651af)
**Revisore:** #57 — APPROVATO CON RISERVE (riserva chiusa in-session)

---

## Scope

Fetta 2 di R-crm-1b: rendere idempotente la scrittura nel diario di
`rileva_duplicati_email()` (modules/memory/store.py ~790).

## Problema risolto

`rileva_duplicati_email()` chiamava `append_diario("sospetto_duplicato_email", ...)`
per OGNI coppia a OGNI invocazione. Il diario è append-only immutabile → ri-lanci
producevano righe identiche permanenti.

## Soluzione implementata

### modules/memory/store.py

Per ogni coppia `(a, b)`:

1. **Token stabile:** `[k=<email_norm>|<id_lo>-<id_hi>]`
   (`id_lo=min`, `id_hi=max` → deterministico indipendentemente dall'ordine di iterazione).
2. **Token embedded** nella descrizione:
   `"sospetto duplicato: <a> ~ <b> (email <email>) [k=<email>|<lo>-<hi>]"`
3. **Pre-check SELECT** prima di ogni append:
   `SELECT 1 FROM diario WHERE tipo=? AND descrizione LIKE ? ESCAPE '\' LIMIT 1`
   con pattern LIKE-escaped (gestisce `%` e `_` nelle email).
4. **FAIL-OPEN §9:** `except (sqlite3.Error, OSError)` → log warning → `_do_append=True` → append comunque.
5. **Return invariato:** la funzione ritorna sempre tutte le coppie correnti.
6. **Docstring aggiornata** (riserva revisore #57 chiusa in-session).

Nessuna modifica allo schema SQLite. Diario resta append-only (nessun UPDATE/DELETE).
Nessun nuovo metodo pubblico.

### tests/test_unit_kernel.py — T57h/i/j

- **T57h:** doppia invocazione su stessa coppia → esattamente 1 riga nel diario; 2ª call ritorna ancora la coppia.
- **T57i:** terza scheda con stessa email aggiunta dopo la 1ª detection → 2 nuove coppie loggiate 1 volta; coppia originale non ri-appesa; 3ª invocazione = 0 nuove righe.
- **T57j:** fail-open simulato droppando la tabella diario → pre-check fallisce (OperationalError), warning loggato, `append_diario` chiamato comunque, nessun crash, coppia ritornata.

## Evidenza di esecuzione

```
Suite completa: 247 PASS, 0 FAIL
(era 220 prima del task; +27 includono T57h/i/j nuovi e T57a-g/T58/T59 intatti)
```

## Verdetto revisore #57 (INTEGRALE)

> **Verdetto: APPROVATO CON RISERVE**
>
> **Correttezza tecnica — store.py**
> - Il token stabile `[k=<email_norm>|<id_lo>-<id_hi>]` è deterministico: `min/max`
>   sugli id garantisce lo stesso token indipendentemente dall'ordine di iterazione.
> - L'escaping LIKE è corretto. I caratteri `[`, `]` e `|` nel token non sono
>   metacaratteri LIKE in SQLite: sono letterali.
> - Il pre-check usa `with self._connect()` in modo coerente con il resto del codebase.
> - `append_diario` ha il proprio `try/except` con log e `return None`: il FAIL-OPEN
>   del pre-check non può produrre crash a valle.
> - L'immutabilità del diario (§6) è preservata: il pre-check è sola lettura;
>   `append_diario` resta l'unico ingresso di scrittura.
> - FAIL-SAFE §9: `except (sqlite3.Error, OSError)` logga su `gas_debug.log` con
>   path DB e messaggio, poi FAIL-OPEN. Corretto a due livelli.
> - Il return di `coppie` è invariato: la funzione segnala sempre tutte le coppie
>   trovate indipendentemente dallo stato del diario.
>
> **Correttezza tecnica — test**
> - T57h (caso base): morde il buco originale e verifica che il return non sia soppresso.
> - T57i (coppie progressive): testa il caso misto "alcune già loggiate, altre nuove".
> - T57j (fail-open): monkey-patch legittimo su metodo di istanza, nessuna violazione
>   §5. La connessione droppata copre il ramo `except` del pre-check e verifica che
>   `append_diario` venga comunque chiamato.
> - Nessun raw history slicing, nessuna tool simulation (Wall of Shame §5 pulito).
> - Guardrail critici: nessuno toccato (loop cap §8, `_get_window()` §5, immutabilità
>   diario §6 tutti invariati).
>
> **Riserva 1 — docstring di `rileva_duplicati_email` non aggiornata:**
> Diceva ancora "scrive una riga append-only nel diario" senza menzionare
> l'idempotenza. Da aggiornare nella prossima occasione utile.
>
> Il commit può procedere.

**Riserva chiusa in-session:** docstring aggiornata prima del commit.

## Stato finding R-crm-1b

- ✅ Fetta email (T57a-g, review #47+#48, 2026-07-14)
- ✅ Merge umano (T58, review #47+#48, 2026-07-14)
- ✅ **Fetta 2 — idempotenza diario (T57h/i/j, review #57, 2026-07-19)** ← questo task
- 🟡 Fetta 3 — telefono: FUORI SCOPE di questo task
