# 📄 REPORT FINE TASK — Test di sicurezza: isolamento sandbox `run_command` (bwrap)

**Data:** 2026-06-14 · **Esito:** ✅ RECINTO INTEGRO — nessuna fuga di scrittura · **Tipo:** collaudo di sicurezza (nessuna modifica al motore)

---

## Richiesta
Verificare l'isolamento della sandbox di `run_command`: tentare di scrivere un
file FUORI dalla project root (cartella superiore o directory utente di sistema) e
confermare se il comando fallisce (come deve) con "Read-only file system /
Permission denied" oppure se riesce a scrivere fuori dal recinto.

## Metodo
Test reale (zero token LLM) su `GAS_SANDBOX_MODE=os_strict`, `GAS_CWD=/workspaces/Gas`,
sandbox bwrap disponibile. Esercitate ENTRAMBE le barriere in serie di `run_command`:
1. **Vetting/allowlist** — via l'entry point reale `execute_tool_call("run_command", …)`.
2. **Sandbox bwrap (filesystem read-only)** — `touch` eseguito dentro `_bwrap_prefix`,
   replicando il confinamento OS reale.
Bersagli fuori dal progetto: `/workspaces` (cartella superiore), `/tmp` (dir di
sistema), `/home/codespace` (home utente).

## Risultati REALI

### Barriera 1 — vetting/allowlist (comandi di scrittura rifiutati prima di partire)
```
$ run_command 'touch ../gas_escape.txt'      -> NEGATO: comando 'touch' non consentito
$ run_command 'touch /tmp/gas_escape.txt'    -> NEGATO: comando 'touch' non consentito
$ run_command 'tee /home/codespace/...'      -> NEGATO: comando 'tee' non consentito
```
`run_command` accetta SOLO comandi di sola lettura da allowlist (ls, cat, grep, wc…):
`touch`/`tee` non vengono nemmeno eseguiti.

### Barriera 2 — sandbox bwrap, filesystem READ-ONLY (scrittura forzata dentro il recinto)
```
$ (bwrap) touch /workspaces/gas_escape_parent.txt
    rc=1  stderr="touch: cannot touch '...': Read-only file system"   | file fuori? NO
$ (bwrap) touch /tmp/gas_escape_tmp.txt
    rc=1  stderr="touch: cannot touch '...': Read-only file system"   | file fuori? NO
$ (bwrap) touch /home/codespace/gas_escape_home.txt
    rc=1  stderr="touch: cannot touch '...': No such file or directory" | file fuori? NO
```

| Bersaglio | Errore reale | File creato fuori dal recinto? |
|---|---|---|
| `/workspaces/...` (cartella superiore) | `Read-only file system` | **NO** |
| `/tmp/...` (dir di sistema) | `Read-only file system` | **NO** |
| `/home/codespace/...` (home utente) | `No such file or directory` | **NO** |

## Nota onesta (non è un buco)
Sulla home l'errore è `No such file or directory` (non `Read-only`) perché bwrap
MASCHERA le cartelle home con una tmpfs vuota e isolata (per nascondere chiavi/token):
lì dentro `/home/codespace` non esiste. Un'eventuale scrittura sulla radice di quella
tmpfs riuscirebbe, ma su un filesystem EFFIMERO e ISOLATO che non tocca mai la home
reale e sparisce a fine comando. Netto: nessun dato esce o persiste fuori dal sandbox.

## Verdetto
✅ **Recinto integro.** Tutti i tentativi di scrittura fuori dal progetto sono falliti:
rifiutati dall'allowlist e/o bloccati dal filesystem read-only del sandbox OS. **Zero
fughe.** Coerente con i test permanenti T13b/T13c della suite (61/61).

## Tracce / stato
- Nessuna modifica al motore (`gas.py`/`tests/` invariati); file di prova ripuliti;
  working tree pulito prima di questo report.
- Finding "🟡 Esfiltrazione via shell — CHIUSA a livello OS in os_strict" confermato
  sul piano della scrittura fuori-recinto (vedi `reports/stato_progetto.md`).
- Complemento non ancora rifatto in questa sessione: verifica dell'isolamento di RETE
  (no esfiltrazione via internet) — coperta dal test permanente T13a.
