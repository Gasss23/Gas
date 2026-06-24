# Report task CI-4 — 2026-06-24

## Scope
Fix condizionale skip T9a/T9c in CI. Solo `tests/test_unit_kernel.py`. Nessuna modifica al motore.

## Problema
T9a e T9c falliscono in CI perché GEMINI_API_KEY e GROQ_API_KEY sono assenti sul runner.
- T9a controlla `len(chiamate) == 3` (3 provider obbligatori): in CI tutti skippati da `gas.py:1282` (`if not os.environ.get(env): continue`) → chiamate vuoto → FAIL.
- T9c controlla `k.db_path.exists() and size > 0`: senza provider che rispondono, `_save_history()` non viene mai chiamata → FAIL.
- T9b (`"Pipeline esausta."`) già passava correttamente in CI (l'errore viene emesso anche con 0 provider).

## Fix applicata
`tests/test_unit_kernel.py`:
1. `skip()` spostata da riga ~395 a riga 24 (subito dopo `check()`), rendendola disponibile prima del blocco T9.
2. `_has_live_keys = bool(os.environ.get("GEMINI_API_KEY") and os.environ.get("GROQ_API_KEY"))` introdotta prima di T9a.
3. T9a e T9c condizionati: con chiavi → `check()` come prima; senza chiavi → `skip()` con reason `"richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI"`.
4. T9b rimane incondizionato (corretto in entrambi gli ambienti).

## Onestà della fix
Nessun mock, nessuna falsificazione. I provider non vengono né simulati né bypassati. Il check viene semplicemente skippato quando le precondizioni ambientali non sono soddisfatte, con reason esplicita.

## Verdetto revisore (INTEGRALE)
**APPROVATO**

1. La fix è onesta: controlla solo `os.environ.get(...)`, non altera il comportamento del motore né menta sul risultato.
2. `skip()` è ora disponibile a riga 24, prima di ogni suo uso (riga ~151 T9a, riga ~160 T9c). Zero rischio NameError.
3. T9b è fuori dal blocco condizionale, eseguito sempre. Corretto.
4. Comportamento locale invariato: con chiavi → `_has_live_keys=True` → check come prima.
5. Nessuna regressione su altri test. La variabile `_has_live_keys` è locale al blocco T9.

Riserve: nessuna tecnica. Nota pre-esistente: T9a è fragile se OPENROUTER_API_KEY è presente (ma il test già la poppava prima del turno T9).

## DECISIONI UMANE RICHIESTE
- **Nota minore**: il job summary del CI (`ci.yml` righe 117-118) contiene un commento che cita T9a/T9c come "FAIL attesi". Dopo questa fix quei commenti sono stale (T9a/T9c saranno SKIP non FAIL). Pulirlo è un one-liner nel YAML ma richiederebbe un commit separato fuori scope — decidi tu se/quando aggiornarlo.

## File toccati
- `tests/test_unit_kernel.py` (17 ins, 7 del)
- `reports/ultimo_report.md` (questo file)

## Commit
Hash: `089b0618694b20a41d4e676f0f4af6d4bb8dcfb6`
