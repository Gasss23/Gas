# Doctor — 402 "crediti esauriti" su rung free opzionale → WARN (non KO)

**Data:** 2026-06-17
**Commit motore:** `7220c28` (revisore #20 — APPROVATO senza riserve)
**Commit doc:** vedi sotto (stampato a fine task)
**Suite:** **132/132, 0 FAIL** (era 128)
**Scope:** onestà della diagnosi `gas doctor` quando un paracadute gratuito è esaurito.
NESSUNA modifica al comportamento a runtime (già corretto).

---

## CONTESTO — perché

Il `doctor` mostrava `[KO]` allarmante per OpenRouter quando l'account aveva i crediti
esauriti (HTTP `402`). Ma OpenRouter è un rung **OPZIONALE** della cascata (paracadute
free, 4° rung): un suo 402 è uno stato **benigno e atteso**, non un guasto.

**Punto chiave verificato dal vivo:** a runtime `run_turn` GIÀ gestiva il 402
correttamente — l'eccezione del provider viene catturata, loggata nella scatola nera
(§9) e la cascata **scala da sé al rung successivo** (Ollama o termina). Nessun crash,
nessuna modifica necessaria lì. Il difetto era **solo** nell'etichetta del `doctor`.

---

## COSA È STATO FATTO

### `gas.py`
- **Nuovo helper PURO `_classify_provider_error(status_code, err_text, obbligatoria)
  -> (esito, dettaglio)`**, accanto a `_classify_free_model`. Regole:
  - `429` → `QUOTA` (per qualsiasi rung; comportamento storico)
  - `402` su rung **OPZIONALE** → `WARN` ("402: crediti esauriti (rung free opzionale)")
  - `402` su rung **OBBLIGATORIO** → `KO` (un provider a pagamento senza credito è un
    problema reale)
  - tutto il resto → `KO` con dettaglio troncato a 60 char (comportamento storico)
- **`doctor`**: il blocco `except` del ping provider ora **delega all'helper** (prima:
  `429→QUOTA` inline, `else→KO`).

### `tests/test_unit_kernel.py` — T27a-d (zero token)
- **T27a** `429` → `QUOTA` (sia via `status_code` sia via testo).
- **T27b** `402` su rung opzionale → `WARN` (non KO), dettaglio corretto.
- **T27c** `402` su rung obbligatorio → `KO` (il ramo WARN NON intercetta).
- **T27d** errore generico → `KO` con dettaglio troncato a 60 char.

---

## VERIFICHE (eseguite e dimostrate)

### A. Suite completa
`python tests/test_unit_kernel.py` → **`=== RIEPILOGO: 132 PASS, 0 FAIL ===`** (era 128).

### B. Dal vivo
`python gas.py doctor` → riga OpenRouter ora `[QUOTA] 429: quota esaurita`
(in questo run il live era 429/rate-limit; il ramo 402 è coperto da T27b). VERDETTO
`OPERATIVO CON AVVISI`, **exit 0**. Niente più `[KO]` allarmante per il paracadute free.

### C. Exit code e invarianti
- **Exit code INVARIATO**: `WARN`/`QUOTA`/`KO` contano tutti come "avvisi"; solo `FAIL`
  alza l'exit a 1. Spostare il 402 opzionale da KO a WARN NON cambia l'exit (entrambi
  erano già nel secchio "avvisi") → nessun rischio di mascherare un FAIL.
- **Invarianti motore INVARIATE**: `_get_window` / `_cap_window_chars` /
  `for _ in range(10)` / sandbox bwrap / snapshot / cascata `run_turn` non toccati.
- **`doctor` resta a ZERO token** (helper puro; ping invariato a `max_tokens=1`).

---

## PROCESSO
- **Gate di review §3**: diff su `gas.py`/`tests/` → subagent **revisore** invocato sul
  diff staged PRIMA del commit → **APPROVATO** (review #20, nessuna riserva), validato
  dal vivo, mutation testing dei 4 rami.
- Hook deterministico onorato (`.claude/.review_ok` creato per il commit, rimosso subito dopo).
- `stato_progetto.md` e `diff_sessione.md` aggiornati.

---

## §FINALE — Fuori da questo task (azione UMANA)
- **Ricarica crediti OpenRouter**: per riattivare il 4° rung gratuito serve un saldo
  minimo su `openrouter.ai/credits` (i modelli `:free` su molti account richiedono un
  credito una-tantum per sbloccare i limiti). NON è codice: è una scelta operativa.
  Gas funziona comunque senza (la cascata scala a Gemini/Groq, e a Ollama sul VPS).
