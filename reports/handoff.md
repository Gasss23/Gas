# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-02 — R-tts-1: cap deterministico testo TTS (fix/tts-cap-testo)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #82 (https://github.com/Gasss23/Gas/pull/82).

---

## §1 SCOPE & ESITO FETTE

- **Fetta UNICA — Cap deterministico GAS_TTS_MAX_CHARS in tts.py**: `FATTA`
  `_cap_text()` aggiunta e cablata in `synthesize_speech()`. Riserve revisore R-tts-cap-1 e R-tts-cap-2 chiuse nella stessa sessione. 24/24 PASS voice suite.

- **Stop gate**: `RISPETTATO` — solo `tts.py` + test toccati. Nessun split multi-chunk, streaming o refactor out-of-scope.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 modules/voice/tts.py               |  51 +++++++++++++++
 reports/diff_sessione.md           |  26 ++++----
 reports/handoff.md                 | 130 ++++++++++++++++++-------------------
 reports/stato_progetto.md          |   6 +-
 reports/ultimo_report.md           |  72 ++++++++++----------
 tests/test_unit_voice_tts.py       |  99 +++++++++++++++++++++++++++-
 7 files changed, 263 insertions(+), 123 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
a7f23e2 fix(tts): cap deterministico GAS_TTS_MAX_CHARS su synthesize_speech — review #96 APPROVATO CON RISERVE
eca1dd5 chore(revisore): memoria review #46 — ?
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

**Commit `a7f23e2`** — fix(tts): cap deterministico GAS_TTS_MAX_CHARS su synthesize_speech

**Verdetto revisore #96: APPROVATO CON RISERVE**

Elementi del diff verificati sul file reale `/home/gqual/Gas/modules/voice/tts.py`:

- `tts.py:32` — `int(os.environ.get("GAS_TTS_MAX_CHARS", _DEFAULT_TTS_MAX_CHARS))` senza `try/except ValueError` — rischio ValueError non catturata da server.py se env var non numerica — **RISERVA (R-tts-cap-1)** → **CHIUSA nella stessa sessione** (try/except aggiunto prima del commit).
- `tts.py:56` — `assert len(truncated) <= max_chars` — assert matematicamente sempre vera per costruzione, non è un vero safety-check, disabilitabile con `-O` — **RISERVA MINORE (R-tts-cap-2)** → **CHIUSA nella stessa sessione** (sostituita con if-hard-cut).
- `tts.py:89` — `text = _cap_text(text)` come prima riga di `synthesize_speech()`, prima di qualsiasi apertura di connessione — posizione corretta — **ok**.
- `tts.py:57-62` — `logging.warning(...)` con stringa di formato, stile corretto, usa root logger — **ok**.

Rischio esplicitamente escluso: comportamento su testi multi-byte (CJK/emoji) non verificato senza chiamata API reale a ElevenLabs — non bloccante, fail-safe 4xx → 502 regge.

Scope rispettato. Nessun antipattern Wall of Shame. Nessun guardrail indebolito. Commit consentito.

---

## §5 DELTA TEST DEL MOTORE

Voice suite prima: **17 PASS** (test_unit_voice_tts.py, ante-sessione)
Voice suite dopo: **24 PASS** (+7 TVT-cap-*)

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
collected 24 items

tests/test_unit_voice_tts.py::TestTVTRoute::test_no_accept_returns_json PASSED
tests/test_unit_voice_tts.py::TestTVTRoute::test_accept_audio_mpeg_routes_to_tts PASSED
tests/test_unit_voice_tts.py::TestTVTRoute::test_accept_audio_wildcard_routes_to_tts PASSED
tests/test_unit_voice_tts.py::TestTVTRoute::test_accept_json_returns_json PASSED
tests/test_unit_voice_tts.py::TestTVTErrors::test_no_key_returns_503 PASSED
tests/test_unit_voice_tts.py::TestTVTErrors::test_empty_text_returns_json_200 PASSED
tests/test_unit_voice_tts.py::TestTVTErrors::test_elevenlabs_error_returns_502 PASSED
tests/test_unit_voice_tts.py::TestTVTErrors::test_network_error_returns_502 PASSED
tests/test_unit_voice_tts.py::test_synth_ok_returns_bytes PASSED
tests/test_unit_voice_tts.py::test_synth_sends_correct_headers PASSED
tests/test_unit_voice_tts.py::test_synth_sends_correct_path PASSED
tests/test_unit_voice_tts.py::test_synth_non200_raises_error PASSED
tests/test_unit_voice_tts.py::test_synth_401_raises_error PASSED
tests/test_unit_voice_tts.py::test_synth_oserror_propagates PASSED
tests/test_unit_voice_tts.py::test_synth_key_not_logged PASSED
tests/test_unit_voice_tts.py::test_default_voice_id_defined PASSED
tests/test_unit_voice_tts.py::TestCapText::test_below_limit_passes_intact PASSED
tests/test_unit_voice_tts.py::TestCapText::test_above_limit_truncates_at_sentence_boundary PASSED
tests/test_unit_voice_tts.py::TestCapText::test_above_limit_no_punctuation_truncates_at_space PASSED
tests/test_unit_voice_tts.py::TestCapText::test_above_limit_no_boundary_hard_cuts PASSED
tests/test_unit_voice_tts.py::TestCapText::test_env_override_respected PASSED
tests/test_unit_voice_tts.py::TestCapText::test_no_warning_when_below_limit PASSED
tests/test_unit_voice_tts.py::TestCapText::test_synthesize_never_sends_over_limit PASSED
tests/test_unit_voice_tts.py::test_server_uses_default_voice_when_env_absent PASSED

============================== 24 passed in 4.65s ==============================
```

Nessun FAIL. Nessun test preesistente rotto.

---

## §6 STATO CI

```
completed	success	fix(tts): cap deterministico GAS_TTS_MAX_CHARS su synthesize_speech —…	CI	fix/tts-cap-testo	push	33684018406	55s	2026-09-02T21:14:30Z
completed	success	Merge pull request #81 from Gasss23/fix/chiusura-f1-calcola-2026-09-01	CI	main	push	33672706420	47s	2026-09-02T19:20:25Z
completed	success	docs(fine-task): fix CI handoff-check — §4 "nessun diff motore" PR #8…	CI	fix/chiusura-f1-calcola-2026-09-01	push	33659578443	1m40s	2026-09-02T17:11:56Z
```

**Mappatura commit→run:**
- `a7f23e2` (motore) → run 33684018406 — **SUCCESS ✅** (push `fix/tts-cap-testo`, 2026-09-02T21:14:30Z)
- `eca1dd5` (memoria revisore, doc-only) → nessuna run dedicata; incluso nell'albero testato da run 33684018406 (commit `a7f23e2` è HEAD al momento del push, `eca1dd5` è in tree ma non testato standalone)
- Commit fine-task (questo file) → run non ancora disponibile alla scrittura dell'handoff

---

## §7 RISERVE APERTE

- **R-tts-cap-1** — CHIUSA (try/except ValueError aggiunto nella stessa sessione prima del commit definitivo)
- **R-tts-cap-2** — CHIUSA (assert sostituito con if-hard-cut nella stessa sessione)
- **R-tts-multibyte** — APERTA (comportamento su testi CJK/emoji non testato; fail-safe 4xx→502 regge; non bloccante)
- Riserve preesistenti da sessioni precedenti: R-finegat-1, R-finegat-2, R-client4a-1, R1/R2/R3/R4 CRM, R-verdetto-evidenza — invariate (non toccate da questa sessione).
