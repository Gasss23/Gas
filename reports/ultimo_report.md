# CERTIFICAZIONE MIGRAZIONE Win/WSL → Mac — 2026-09-12

**Branch:** cert/mac-migration-2026-09-12  
**Data:** 2026-09-12  
**Operatore:** Claude Sonnet 4.6 (cert automatica)  
**Repo:** HEAD=794a9a7 (main, aggiornato a origin)

---

## VERDETTO FINALE

**✅ MIGRAZIONE CERTIFICATA — L1+L2+L3 PASS**  
ZERO crash. ZERO danni ai dati. Unici rossi: ambiente Mac attesi + 1 finding nuovo F-mac-4.

---

## SONDA 0

| Check | Risultato |
|-------|-----------|
| Python | **3.14.7** (≥ 3.11 ✅) |
| Hash `.gas_memory.db` a inizio | `6202bb69f79503310136dd047097889db61f94ff30f589fc510593a2ae69bbc3` |
| Hash `.gas_memory.db` a fine | `5645da76e8fb50ed5500b35d3363fc83c696c755bfeecfe205185d872e3d0d8b` |
| `count(*)` diario a inizio | **14** ✅ |
| `count(*)` diario a fine | **16** (14 originali + 2 append L1 su kernel reale — ATTESO) |
| `.bak` files | assenti (doctor segnala ultimo backup 246h fa — già presente) |

**Nota sull'hash**: i 2 nuovi entry del diario (ID 15 = `ricorda`, ID 16 = `calcola 7*8`) sono stati aggiunti dai test L1 sul kernel reale — comportamento corretto e atteso. Il diario è append-only; le 14 voci originali (ID 1-14, tutte `calcola`, timestamp 2026-08-29 e 2026-09-01) sono intatte e non modificate. L2 e L3 hanno usato root temporanee: **ZERO scritture L2/L3 sul DB reale**.

---

## LIVELLO 1 — È VIVO E INTEGRO ✅

### gas doctor
```
[OK ] API keys   GEMINI_API_KEY       presente
[OK ] Provider   gemini-flash-lite    1279 ms
[OK ] Provider   gemini-flash         640 ms
[OK ] Provider   groq                 251 ms
[OK ] Memoria    integrità            quick_check ok
[OK ] Memoria    ricerca FTS5         attiva
[FAIL] Sandbox OS bwrap+namespace     bwrap non installato — mode=os_strict
VERDETTO: PROBLEMI RILEVATI (1 FAIL, 3 avvisi)
```
**Classificazione**: UNICO FAIL = bwrap — **COLPA MAC ATTESA**, comportamento corretto.

### Lettura memoria migrata (ricorda)
Gas ha letto il diario reale e restituito:
> "Dal diario so che hai eseguito diverse volte il calcolo di '7*8' e 'math.sqrt(144)'."

✅ Legge le 14 voci migrate.

### Round-trip agentico (calcola 7*8)
```
EVENT: {'type': 'tool_res', 'output': '56'}
EVENT: {'type': 'final', 'content': '7 per 8 fa 56.'}
Sequenza: [tool_res, final] — nessuna coppia orfana
```
✅ Ciclo chiuso, tool corretto.

---

## LIVELLO 2 — LAVORA DAVVERO (su COPIA) ✅

Root temporaneo: `/private/tmp/gas_cert_root_10168/`

### Task multi-tool
| Step | Risultato |
|------|-----------|
| `salva_contatto` mario_rossi_test | `id=1` ✅ |
| `imposta_stato_contatto` → `interessato` | ✅ |
| `calcola` sqrt(196) = 14.0 (scrive diario) | ✅ |
| DB finale: 3+ righe diario, 1 contatto, stato=interessato | ✅ |

### Persistenza dopo riavvio (nuovo processo)
Nuovo `GasKernel(root_dir=TMPROOT)` → 3 righe diario lette: **PASS** ✅  
Calcolo aggiuntivo (100/4=25.0) → 4 righe: **PASS** ✅

### Cascata provider live
Gemini con chiave invalida → WARNING → Groq risponde `2+2=4`:
```
WARNING - Provider gemini-flash-lite (gemini-2.5-flash-lite) fallito: 400 INVALID_ARGUMENT
WARNING - Provider gemini-flash (gemini-2.5-flash) fallito: 400 INVALID_ARGUMENT
EVENT: {'type': 'tool_res', 'output': '4'}
EVENT: {'type': 'final', 'content': '2 + 2 = 4.'}
```
✅ Fallthrough Gemini→Groq funzionante.

---

## LIVELLO 3 — ROBUSTEZZA SOTTO ATTACCO

### Suite kernel (python tests/test_unit_kernel.py)
```
=== RIEPILOGO: 290 PASS, 5 FAIL ===
FAIL: T11c2 — bwrap (colpa Mac ATTESA)
FAIL: T11e  — bwrap (colpa Mac ATTESA)
FAIL: T12a  — bwrap (colpa Mac ATTESA)
FAIL: T12c  — bwrap (colpa Mac ATTESA)
FAIL: T12e  — bwrap (colpa Mac ATTESA)
```
✅ **290 PASS, 5 FAIL** — IDENTICO al baseline atteso. Tutti i 5 FAIL = bwrap, colpa Mac ATTESA.

### Suite pytest (tutti i file eccetto test_unit_kernel.py)
```
111 PASS, 10 FAIL
FAIL: test_unit_gasmerge.py — TestIPGuard/TestIPAllowlist/TestLoopbackExemption (10 test)
```

**Classificazione 10 FAIL gasmerge**: macOS `git grep -E '\b...\b'` usa POSIX ERE, che NON supporta `\b` (word boundary). La regex IP esce con exit code 1 (nessun match) anche quando gli IP sono presenti. Su Linux/WSL la stessa regex funziona (git uses PCRE or different backend). → **Nuovo finding F-mac-4** (dettaglio sotto). Il VPS target è Linux: **nessun impatto sul deploy**.

Tutti gli altri file: **PASS completo**:
- test_unit_handoff_check.py: 11/11
- test_unit_hooks.py: 19/19
- test_unit_voice_server.py: 19/19
- test_unit_voice_stt.py: 28/28
- test_unit_voice_tts.py: 24/24

### Test di sicurezza espliciti
| Test | Risultato |
|------|-----------|
| T10a/b/c — path traversal bloccato | ✅ PASS |
| T13d — run_command fail-closed senza bwrap | ✅ PASS |
| T44 — budget giornaliero ferma la spesa | ✅ PASS |
| T19j — DB corrotto → degrada senza crash | ✅ PASS |
| T26a-e — backup funziona | ✅ PASS |
| T9a/b — loop cappato a 10 | ✅ PASS |
| T19f — diario immutabile (UPDATE/DELETE bloccati) | ✅ PASS |

### Task-trappola (su COPIA)
| Trappola | Risultato |
|----------|-----------|
| Aritmetica 127×89 → usa `calcola` (non allucinazione) → 11303 | ✅ PASS |
| Shell `ls -la /tmp` → bloccato (path traversal + fail-closed) | ✅ PASS |
| DB corrotto → warning + degrado + calcola 3×4=12 funziona | ✅ PASS |

---

## FINDING APERTI POST-CERTIFICAZIONE

### F-mac-4 (NUOVO, 2026-09-12) — gasmerge.sh: IP guard silenzioso su macOS
**Impatto**: `scripts/gasmerge.sh` usa `git grep -nE '\b[0-9]{1,3}...\b' "origin/$BRANCH"`. Su macOS, POSIX ERE non supporta `\b` → git grep esce con rc=1 (zero match) anche in presenza di IP. 10 test `test_unit_gasmerge.py` FAIL di conseguenza.  
**Classificazione**: Colpa Mac — comportamento diverso da Linux. NON è danno di migrazione dai dati WSL.  
**Impatto VPS**: ZERO. Il VPS target è Linux; git grep funzionerà correttamente.  
**Impatto locale Mac**: lo script di merge locale non rileva IP — le PR con IP passano il gate locale senza blocco. La CI su GitHub (Ubuntu) continua a funzionare.  
**Fix proposto**: aggiungere flag `-P` (PCRE) a `git grep` per portabilità: `git grep -nP '\b[0-9]{1,3}...\b'`. Alternativa: `grep -E` esterno su stdout di `git show`. Test-only fix: aggiungere `pytest.mark.skipif(platform.system() == 'Darwin', ...)` ai 10 test.

### F-mac-1, F-mac-2, F-mac-3 (dal 2026-09-09, nessun cambiamento)
Confermati invariati: bwrap, SyntaxWarning regex, collection-safety probe/win_mic_test.py.

---

## CERTIFICAZIONE

- **L1**: PASS ✅
- **L2**: PASS ✅ (su COPIA, DB reale intatto)
- **L3**: PASS ✅ (solo rossi = ambiente Mac noti + nuovo F-mac-4)
- **Zero crash**: ✅
- **Dati originali (14 voci diario) intatti**: ✅ (verificato ID 1-14 immutabili)
- **Memoria reale mai scritta da L2/L3**: ✅

**La migrazione Windows/WSL → Mac NON ha causato danni. Il sistema è operativo.**
