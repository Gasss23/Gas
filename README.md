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
