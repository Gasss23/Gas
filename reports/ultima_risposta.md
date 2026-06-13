Risultato empirico chiave (aggiorna la sonda FASE 0 della roadmap, che dava "binario assente"):

- ✅ `bubblewrap 0.9.0` **si installa** nel Codespace senza problemi.
- ✅ Il profilo restrittivo **funziona davvero**: `--unshare-net --ro-bind / / --tmpfs /tmp --die-with-parent` gira, e dentro il namespace di rete resta **solo loopback** (`eth0` sparito) → **isolamento di rete reale, qui, oggi**. Possiamo testare in dev.

Procedo con la proposta. **Solo design, nessun codice** — poi mi fermo per il tuo OK.

---

# BWRAP — FASE 1 (proposta di design)

## 1. Principio: bwrap è il guscio ESTERNO, la difesa applicativa resta SOTTO
La sandbox OS non sostituisce nulla dell'esistente: lo **avvolge**. L'ordine in `run_command` diventa:

```
vetting fail-closed (allowlist) → dry-run? → snapshot → [ bwrap … -- comando ] con shell=False + env sanificata
                                                          ^^^^^^^^^^ nuovo strato OS
```

Vetting, allowlist, snapshot ed env sanificata **restano identici** (difesa in profondità). bwrap aggiunge il confinamento del kernel che la recinzione applicativa non può dare: anche se un binario in allowlist venisse compromesso o avesse una falla, **non vede la rete e non scrive sul filesystem**.

## 2. Profilo bwrap proposto
`run_command` è **di sola lettura** (allowlist: `wc/grep/ls/cat/...`), quindi un root read-only è pienamente compatibile:

| Flag | Scopo |
|---|---|
| `--unshare-net` | **Rete chiusa** → chiude DEL TUTTO il finding esfiltrazione (oggi solo 🟡) |
| `--unshare-pid --proc /proc` | Isolamento processi (non vede/uccide i PID dell'host) |
| `--ro-bind / /` | Root **read-only**: nessuna scrittura fuori da /tmp |
| `--tmpfs /tmp` | Scratch effimero, isolato, sparisce a fine comando |
| `--dev /dev` | `/dev` minimale (no device dell'host) |
| `--die-with-parent` | Se GAS muore, il figlio muore (no processi orfani) |
| `--new-session` | Stacca dal TTY (blocca injection via `TIOCSTI`) |
| `--clearenv --setenv PATH …` | Env azzerata + ricostruita (si appoggia all'esistente `_sanitized_subprocess_env()`) |

La `cwd` (sotto la root read-only) resta leggibile: i comandi di lettura funzionano; le scritture sono comunque già intercettate da `write_file` + snapshot.

## 3. `GAS_SANDBOX_MODE` (asse nuovo, default sicuro)
- **`os_strict`** (DEFAULT): richiede bwrap + namespace funzionanti. Se mancano → **fail-closed duro**: `run_command` rifiuta di eseguire ("OS sandbox non disponibile"). È il comportamento da produzione/VPS.
- **`os_with_fallback`** (opt-in **esplicito**, solo dev): se bwrap/namespace non disponibili → degrada alla sandbox **applicativa** odierna (shell=False + vetting), con `logging.warning`. Più debole, quindi mai di default.
- Normalizzazione + fallback fail-safe su `os_strict` per valori ignoti (stesso pattern già usato per `GAS_SHELL_MODE`).

> Punto da decidere insieme (FASE 2): rapporto tra `GAS_SANDBOX_MODE` (confinamento OS) e l'esistente `GAS_SHELL_MODE` (`guarded`/`dry_run`). Sono ortogonali; propongo che `GAS_SANDBOX_MODE` governi *dove* gira il comando e `GAS_SHELL_MODE` *se* gira (dry-run). Da confermare.

## 4. `gas doctor` — check "OS sandbox"
Nuovo check che: (a) verifica presenza di `bwrap`; (b) esegue una **sonda namespace reale** (come quella di sopra, comando innocuo) per distinguere "binario presente" da "namespace concessi".
- In `os_strict` + sandbox non disponibile → **FAIL** (exit 1), come da tua richiesta.
- In `os_with_fallback` → **WARN**.
- Come distinguere "produzione": propongo una var esplicita `GAS_ENV=production|dev` (in prod, sandbox assente = FAIL secco). Da confermare.

## 5. Cosa NON tocco in FASE 1
Nessun codice, nessun test, nessuna modifica a `gas.py`. Difesa applicativa esistente intatta.

## 6. Domande aperte per il tuo OK (FASE 2 = implementazione)
1. Confermi il profilo bwrap di §2 (in particolare `--unshare-pid` e `--new-session`, che irrobustiscono ma aumentano i casi di test)?
2. `GAS_ENV` esplicita per distinguere prod/dev nel doctor, o preferisci inferirlo (es. presenza TTY)?
3. Relazione `GAS_SANDBOX_MODE` ↔ `GAS_SHELL_MODE` come in §3 (ortogonali) o li fondo in un unico asse?

---

**STOP come da tuo ordine.** In attesa del tuo OK (e delle risposte a §6) prima di implementare la FASE 2. Riepilogo di quanto fatto fino a qui in questa ripresa:

- **P0 + 1A** già in `5cc609b` (verificati, non rifatti).
- **1B** committato e pushato ora: **`458a2b5`**, working tree pulito, **46 PASS / 0 FAIL**, revisore #5 APPROVATO CON RISERVE.
- **Reporting**: path + hash + cat integrale stampati sopra. `diff_sessione.md` rigenerato.
- **BWRAP FASE 1**: proposta qui sopra, bubblewrap verificato installabile e funzionante nel Codespace.
