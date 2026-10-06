# ULTIMO REPORT — 2026-10-06 — Gate IP: `read` in C (fail-open con byte non UTF-8) + discriminazione latin1 su glibc

## Decisioni umane richieste

1. Merge della PR #134 — **prioritario**: chiude due fail-open già presenti su main, il gate IP (privacy) e il gate di review (commit di un file del perimetro senza review), entrambi in locale UTF-8.
2. Fetta di sicurezza: secondo passaggio indipendente nella chat claude.ai con l'URL dell'handoff (protocollo §4quater).
3. Ordine di merge della notte: ogni PR riscrive i report canonici; dopo un merge le altre vanno riallineate a main (conflitto solo su `reports/` e `memoria_revisore.md`).

## Esito per fette

- **V-2 #124/#125 — discriminazione latin1 su glibc**: FATTA — provato su glibc 2.39 che il test esistente (`caf\xe9 <IP>`, separatore spazio) non uccideva la mutation su `LC_ALL=C git grep`; test nuovi col byte ATTACCATO all'IP e locale UTF-8 forzato la uccidono.
- **Bug trovato — fail-open del gate IP**: FATTA — `while IFS= read -r` di bash 5.2 in locale UTF-8 perde l'ultima riga se finisce con un byte non UTF-8 → IP "loopback". Fix `IFS= LC_ALL=C read` in gasmerge.sh e fine_task_finale.sh.
- **R-167-1** (stessa classe nel ciclo ENGINE_DIFF di gasmerge): FATTA. **R-167-2** (skip se manca `locale`): FATTA.
- **Mutation**: FATTA — read, git grep ×2, grep -qE, grep -Fx uccise sotto C.UTF-8; `sed` equivalente; `read -r v` del perimetro equivalente in pratica.
- **Review**: #167 APPROVATO CON RISERVE → #170 APPROVATO.
- **macOS**: NON VERIFICATO — bash 3.2 di sistema probabilmente non colpito; bash 5 di homebrew sì (ragionamento del revisore).

- **Verifica esterna #134**: FATTA — APPROVATO CON RISERVE; V-2 (`review_gate.sh:76`, stesso difetto: fail-open del gate di review, provato) e V-3 (locale esigito in CI) CHIUSE; R-177-1/R-177-2/R-178-1 chiuse. Review #177/#178 APPROVATO CON RISERVE → #179 APPROVATO. Suite 281 passed in C e C.UTF-8.

## Anomalie

- Nessuna. `gh` non autenticato: PR via connettore GitHub.
