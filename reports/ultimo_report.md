# CI — run auto-verificabile (job summary + gate sandbox)

**Data:** 2026-06-23
**Task:** chiudere la lacuna di osservabilità emersa verificando la run precedente — il
segnale critico (esito bwrap, conteggio PASS/FAIL/SKIP) stava SOLO nel log dietro auth
(HTTP 403), quindi una "CI di osservabilità" non era di fatto osservabile senza scaricare
lo zip. Renderla leggibile a colpo d'occhio dalla pagina della run.
**Tipo:** infrastruttura CI (`.github/workflows/`) NON-motore. **Revisore:** non applicabile
(nessun diff su `gas.py`/`brains/`/`modules/`/`tests/`).

---

## §DECISIONI UMANE RICHIESTE

1. **Verificare la run post-push** (https://github.com/Gasss23/Gas/actions, commit più
   recente): ora il **Job Summary** della run mostra senza scaricare nulla —
   - esito smoke-test bwrap (post-install + post-sysctl): `BWRAP_OK` / `BWRAP_FAIL`;
   - la riga `RIEPILOGO: N PASS, M FAIL` della suite + conteggio `SKIP`;
   - la lista dei FAIL.
   E lo step **"Gate — sandbox OS attivo"** è rosso/verde a sé:
   - **verde** → sandbox attivo: i 5 bwrap + 4 T13 hanno esercitato il profilo reale; gli
     eventuali FAIL residui sono T9a/T9c (env, attesi);
   - **rosso** → `BWRAP_FAIL`: STOP GATE, il runner GitHub nega gli userns → micro-task
     skip-on-CI dei test bwrap (tocca `tests/`, **con revisore**).
2. La via verso una CI **verde** piena resta il micro-task su `tests/` (T9a/T9c + eventuale
   skip-on-CI bwrap): fuori dallo scope solo-workflow, da autorizzare.

---

## CONTESTO (perché questo intervento)

Verificando la run precedente (commit `4f8d014`) via API pubblica: job **failure**, step
sandbox **success**, step suite **failure**. Ma:
- "failure" del job è ATTESO anche nel caso buono (T9a/T9c restano rossi per disegno);
- lo step sandbox risultava "success" SEMPRE, perché lo smoke-test era `... || echo
  BWRAP_FAIL` → non falliva lo step nemmeno a sandbox assente;
- il log dettagliato (BWRAP_OK/FAIL, conteggio) è dietro auth (`/logs` → HTTP 403) e `gh`
  non è installato.

→ Impossibile distinguere "sandbox attivo, 2 FAIL attesi" da "BWRAP_FAIL, 7 FAIL" senza lo
zip. Lacuna reale per un'infrastruttura di osservabilità. Chiusa qui.

---

## COSA È STATO FATTO (Commit `5dab394`)

`.github/workflows/ci.yml`, sempre ZERO token LLM, nessun secrets/provider:

1. **Smoke-test esposto come output** dello step `Enable OS sandbox` (`id: sandbox`):
   `smoke1`/`smoke2` (= `BWRAP_OK`/`BWRAP_FAIL` pre/post sysctl) in `$GITHUB_OUTPUT`,
   riusati dagli step successivi. Lo step **non fallisce** su BWRAP_FAIL: lascia girare la
   suite per avere il quadro completo (la distinzione la fa il gate finale).
2. **Step `Run unit suite`**: ora `set -o pipefail` + `tee "$RUNNER_TEMP/suite_output.txt"`
   → l'output è catturato per il summary E l'**exit code NATIVO della suite resta il
   verdetto** (il verde/rosso non viene mai mascherato).
3. **Step `Job summary`** (`if: always()`, `set +e`): scrive nel `$GITHUB_STEP_SUMMARY`
   (pagina della run, niente zip/auth) una tabella con esito bwrap, riga RIEPILOGO, SKIP e
   lista FAIL. Puramente informativo, non cambia il verdetto.
4. **Step `Gate — sandbox OS attivo`** (`if: always()`, per ULTIMO così il summary è già
   scritto): `exit 1` con `::error::` chiaro SOLO se `smoke2 != BWRAP_OK` → "rosso da
   sandbox" diventa un segnale nominato e distinto dal "rosso da T9a/T9c".

**Decisioni di principio rispettate:** non maschero il verdetto della suite (nessun
allowlist di test "accettabili" nel workflow — sarebbe il parsing fragile vietato dalla
spec originale); informo, non override. La CI resta rossa finché esistono FAIL, ma ora il
*perché* è leggibile a colpo d'occhio.

YAML validato in locale con PyYAML (7 step, `on: push`).

---

## DELTA TEST DEL MOTORE

**0.** `tests/` e `gas.py` INVARIATI.

## VERDETTO DEL REVISORE

**Non applicabile — task non-motore.** Diff solo su `.github/workflows/ci.yml` (+ report).

## STATO CI

**Run post-push da verificare** — ma ora bastano la pagina della run (Job Summary) e lo
stato dello step "Gate — sandbox OS attivo", senza scaricare il log. NON scrivo "CI verde"
senza averla vista girare.

## RISERVE / NOTE
- **CI-4 (NUOVA):** finché T9a/T9c restano rossi (env, fuori scope) il job resta ROSSO anche
  con sandbox attivo. È onesto ma il segnale "verde" non è raggiungibile senza il micro-task
  su `tests/`. Mitigazione: il gate sandbox + summary rendono leggibile il "rosso buono".
- **CI-3** (sessione precedente) di fatto risolta: l'esito bwrap è ora visibile senza auth.
