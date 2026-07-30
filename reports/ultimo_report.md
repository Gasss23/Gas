# Ultimo Report — Chiusura gate R4 su Riserva 1 di review #69 (2026-07-30)

**Task**: FASE UNICA — ri-review #70, chiusura formale Riserva 1 di #69 (`-> None`)
**Branch**: test/gasmerge-match-head
**Esito**: ✅ COMPLETATO — gate R4 chiuso, verdetto #70 APPROVATO

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #57 (`test(gasmerge): copertura POSITIVA end-to-end --match-head-commit`).

---

## ESITO FETTE

**Fetta 1 — Verifica stato (riga 410)**: `FATTA`
`git diff --stat origin/main HEAD -- tests/test_unit_gasmerge.py` → 1 file, 77 righe aggiunte.
Riga 410 confermata su disco: `def _make_stub_gh_recording_merge(fake_bin: Path, merge_log: Path, sha: str) -> None:`

**Fetta 2 — Ri-invoca subagent revisore (#70)**: `FATTA`
Revisore invocato sul diff `origin/main..HEAD` limitato a `tests/test_unit_gasmerge.py`.
Verdetto ricevuto: **APPROVATO**. Cita 3 elementi concreti (`:410`, `:528-533`, `:419-438`).
Riserva 1 dichiarata **CHIUSA** con riferimento file:riga esplicito.

**Fetta 3 — Aggiungi riga #70 in memoria_revisore.md**: `FATTA`
Riga aggiunta dal revisore stesso:
`#70 — 2026-07-30 — APPROVATO — Ri-review formale dopo chiusura R1 di #69 (-> None). Confermato su disco riga 410: firma completa con type hint -> None. Test TOCTOU positivo corretto: tre asserzioni discriminanti (exit 0 + merge_log.exists() + coppia --match-head-commit <SHA> nel log). Nessuna lezione nuova.`

**Fetta 4 — Aggiorna ultimo_report.md**: `FATTA`
Verdetto #69 titolato esplicitamente; verdetto #70 incollato verbatim; nota chiusura R4 in fondo.

**Fetta 5 — Aggiorna stato_progetto.md (#65-R2)**: `FATTA`
Riga `#65-R2` aggiornata: aggiunta clausola «Riserva 1 di forma chiusa a norma R4: ri-review #70 APPROVATO (2026-07-30), confermato `-> None` su disco a riga 410».

---

## VERDETTO REVISORE #69 (integrale — da sessione precedente)

**APPROVATO CON RISERVE**

> `tests/test_unit_gasmerge.py:429-431` — arm `*"headRefOid"*` restituisce SHA identico
> a entrambe le chiamate (pre-prompt e post-prompt) → TOCTOU check passa, nessun BLOCCO
> spurio. Rischio ordine arm: nessun conflitto con `*"pr merge"*` perché le rispettive
> `$*` non si sovrappongono. **Esito: ok**.
>
> `tests/test_unit_gasmerge.py:432-434` + `533` — `echo "$@"` registra gli argomenti
> reali di `gh pr merge`; l'asserzione `f"--match-head-commit {self._SHA}" in recorded`
> è mordace (fallirebbe su flag assente o SHA errato). Doppia guardia con
> `assert merge_log.exists()` che certifica che il ramo `pr merge` sia stato raggiunto.
> **Esito: ok**.
>
> **Riserva 1 (minore):** firma di `_make_stub_gh_recording_merge` senza `-> None`
> (CLAUDE.md §4). Coerente col pattern dell'intero file; correggibile al prossimo refactor.
>
> **Riserva 2 (pre-esistente):** `/tmp/gaspr.json` hardcoded, già tracciato come #65-R3.
> Non aggravata da questo diff.
>
> **Finding #65-R2 / #63-R2: CHIUSO.**

---

## VERDETTO REVISORE #70 — RI-REVIEW R4 (integrale)

**APPROVATO**

> `tests/test_unit_gasmerge.py:410` — `def _make_stub_gh_recording_merge(fake_bin: Path, merge_log: Path, sha: str) -> None:` — type hint `-> None` presente e confermato da Read del file su disco (offset 400, limit 140). Tutti e tre i parametri hanno type hint espliciti (Path, Path, str). Riserva 1 di #69 esaminata: CHIUSA. Rischio "violazione CLAUDE.md §4 rigoroso uso type hints": esito ok.
>
> `tests/test_unit_gasmerge.py:528-533` — blocco delle tre asserzioni in `test_head_unchanged_merge_uses_match_head_commit`: (1) `assert result.returncode == 0`; (2) `assert merge_log.exists()` — se `gh pr merge` non venisse invocato, il file non esiste e il test cade; (3) `assert f"--match-head-commit {self._SHA}" in recorded` — controlla la coppia flag+valore come sottostringa del log prodotto da `echo "$@"`. Mordacità verificata: se `gasmerge.sh` omettesse `--match-head-commit` o passasse uno SHA diverso, l'asserzione (3) fallirebbe correttamente. Il `merge_log` vive in `tmp_path / "merge_args.log"` (path univoco per invocazione pytest), isolato dal `/tmp/gaspr.json` già noto. Rischio "test che asserisce solo exit 0 non discrimina": esito ok — la catena di tre asserzioni è discriminante.
>
> `tests/test_unit_gasmerge.py:419-438` — corpo bash dello stub: pattern `case "$*" in` con ordine `*"headRefOid"*` PRIMA di `*"pr merge"*` e `*"--watch"*` PRIMA di `*"pr merge"*`. Rischio "collisione pattern se gasmerge.sh chiamasse `gh pr merge --watch`": la chiamata reale di `gh pr checks --watch` non contiene `pr merge`, quindi l'intercettazione errata non si produce. Ordine dei rami sicuro nel contesto reale. Rischio "interpolazione `{sha}` senza escape in testo bash": SHA git sono esadecimali puri, nessun carattere speciale bash possibile. Esito ok.
>
> Rischio esplicitamente escluso: il comportamento end-to-end su VPS con più worker paralleli (pytest-xdist) non è verificabile nell'ambiente di review — il rischio `/tmp/gaspr.json` condiviso tra test concorrenti (riserva #65-R3, già tracciata) rimane aperto ma non aggravato da questo diff.
>
> **Riserva 1 di #69 (-> None): CHIUSA** — riga 410 su disco: `def _make_stub_gh_recording_merge(fake_bin: Path, merge_log: Path, sha: str) -> None:`.
>
> Riserve residue: nessuna nuova. Resta aperta la pre-esistente #65-R3 (`/tmp/gaspr.json` hardcoded, non thread-safe con pytest-xdist), non aggravata da questo diff.

**→ Riserva 1 di #69 CHIUSA a norma R4 (ri-review #70 APPROVATO). Gate chiuso.**

---

## STOP GATE BLOCCANTE — verifica

- `git diff scripts/gasmerge.sh` → vuoto ✅ (nessuna modifica al di fuori di tests/)
- Diff staged: solo report/doc ✅
- PR #57 aperta, NON mergiata ✅ (istruzione rispettata)
- Gate R4 chiuso: ri-review #70 APPROVATO, Riserva 1 di #69 chiusa formalmente ✅
