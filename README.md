# Gas
il mio assistente personale gas

## ⏪ Macchina del tempo — ripristino snapshot (SOLO umano)

Prima di ogni `write_file` e di ogni `run_command`, il kernel fotografa il repo
(file tracciati **e** non tracciati, inclusa `.gas_history.json`) in un commit
fuori-branch sotto `refs/gas/snapshots/`. Il ripristino **non è un tool di Gas**:
si fa a mano, con git. Indice leggibile in `reports/snapshots.log`.

```bash
# 1. Elenca gli snapshot (dal più vecchio al più recente)
git for-each-ref refs/gas/snapshots/

# 2. Ripristina UN file da uno snapshot
git restore --worktree --source refs/gas/snapshots/<nome-ref> -- percorso/del/file

# 3. Ripristina lo STATO INTERO del repo a quello snapshot
git restore --worktree --source refs/gas/snapshots/<nome-ref> -- .
```

Attenzione: il punto 3 riporta indietro i file presenti nello snapshot, ma **non
cancella** i file creati dopo (per quello: confrontare con
`git diff <ref> --stat` e rimuovere a mano). I file in `.gitignore` (venv, log)
non sono inclusi negli snapshot. Retention: il kernel conserva gli ultimi 100
snapshot e pota automaticamente i più vecchi.

## 🔒 Sandbox di `run_command` (no-shell + allowlist)

`run_command` **non** usa una shell. Ogni comando passa per un vetting
fail-closed e viene eseguito con `shell=False`, in tre barriere:

1. **Parsing senza shell** (`shlex.split`): pipe `|`, redirezioni `>`,
   concatenazioni `;`/`&&` e command substitution `$(...)` perdono potere —
   diventano testo o fanno fallire il parse. Virgolette sbilanciate → negato.
2. **Allowlist** sul binario: solo comandi di **sola lettura** (`ls`, `cat`,
   `head`, `tail`, `wc`, `grep`, `cut`, `diff`, `stat`…). Tutto il resto è
   negato. È una allowlist, non una denylist, perché i wrapper (`env curl`,
   `xargs`, `bash -c`) sfondano qualunque lista di proibiti. Gli interpreti
   (`python`, `bash`) sono esclusi di proposito.
3. **Ricontrollo dei path**: ogni argomento-percorso passa lo stesso guardrail
   anti-traversal di `read_file`/`write_file` e deve restare nella root.

L'ambiente del processo figlio è **ripulito dai segreti** (variabili con
`KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`, `AUTH` nel nome vengono
rimosse). Ordine: **vetting → snapshot → esecuzione**, così un comando negato
non spreca uno snapshot.

### Modalità — `GAS_SHELL_MODE`

| Valore              | Comportamento                                                        |
|---------------------|----------------------------------------------------------------------|
| `guarded` (default) | Vetting completo, poi esecuzione senza shell. Valore ignoto → qui (fail-safe). |
| `dry_run`           | Fa il vetting ma **non esegue** e **non fotografa**: `[DRY-RUN] ... NON eseguito`. Collaudo / kill-switch. |

```bash
GAS_SHELL_MODE=dry_run python3 gas.py    # congela i comandi senza eseguirli
```

### Niente pipeline — alternative native

| Prima (shell)            | Adesso (no-shell)                    |
|--------------------------|--------------------------------------|
| `grep X file \| wc -l`   | `grep -c X file`                     |
| `cat a b > c`            | `write_file` (mai redirezioni shell) |
| `wc -l < file`           | `wc -l file`                         |

### Limite residuo (onestà, come per gli snapshot)

Questa è una recinzione **applicativa** contro l'esfiltrazione naïve/diretta,
**non** un confinamento a livello OS. Gli interpreti restano fuori dall'allowlist
proprio perché ammetterli riaprirebbe l'esecuzione di codice arbitrario. Il muro
definitivo è a livello sistema (`bwrap`/`unshare` con rete chiusa e filesystem
read-only sul VPS): prossimo candidato roadmap, con check in `gas doctor`. La
falla nota si sposta da **aperta** a **ridotta**, non a **chiusa**.

Copertura: blocco **T12** in `tests/test_unit_kernel.py` (allowlist, no-shell,
traversal negli argomenti, env sanificata, dry-run, fallback); **T11c2**
rinforzato per esercitare davvero il fail-closed dello snapshot.
