# Task — R-tts-1: cap deterministico testo TTS

**Data:** 2026-09-02
**Branch:** fix/tts-cap-testo
**PR:** #82 — https://github.com/Gasss23/Gas/pull/82
**Revisore:** review #96 — APPROVATO CON RISERVE (riserve chiuse nella stessa sessione)

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #82 (https://github.com/Gasss23/Gas/pull/82).

---

## Scope & Esito Fette

### Fetta UNICA — Cap deterministico GAS_TTS_MAX_CHARS in modules/voice/tts.py: FATTA

- Aggiunta funzione `_cap_text(text: str) -> str` in `tts.py`
- Limite configurabile via env `GAS_TTS_MAX_CHARS` (default 2000)
- Troncamento in ordine di priorità: ultimo confine frase (., !, ?) ≤ limite → ultimo spazio → hard-cut
- WARNING loggato con lunghezza originale, troncata e limite
- `text = _cap_text(text)` applicato come prima istruzione di `synthesize_speech()`
- Riserve revisore chiuse nella stessa sessione:
  - R-tts-cap-1: `try/except ValueError` su `int(os.environ.get(...))` per env var non numerica
  - R-tts-cap-2: `assert` sostituito con `if truncated > max_chars: hard-cut`

### Test REALI (7 nuovi TVT-cap-*): FATTI — 24/24 PASS

| Test | Esito |
|------|-------|
| test_below_limit_passes_intact | PASS |
| test_above_limit_truncates_at_sentence_boundary | PASS |
| test_above_limit_no_punctuation_truncates_at_space | PASS |
| test_above_limit_no_boundary_hard_cuts | PASS |
| test_env_override_respected | PASS |
| test_no_warning_when_below_limit | PASS |
| test_synthesize_never_sends_over_limit | PASS |

Intera voice suite: 24/24 PASS (erano 17 test pre-cap + i nuovi, più i 7 TVT-cap).

### Stop gate: RISPETTATO

Solo `modules/voice/tts.py` e `tests/test_unit_voice_tts.py` toccati. Nessun split multi-chunk, nessuno streaming, nessun refactor fuori scope — tutto differito al supervisore per valutazione.

---

## Anomalie

Nessuna.

---

## Idee fuori scope (da valutare)

- Split multi-chunk per testi > limite: inviare più chunk a ElevenLabs in sequenza e concatenare i byte MP3. Aumenta latenza e complessità; da valutare se l'agente VPS produce risposte sistematicamente > 2000 char.
- Streaming ElevenLabs: ElevenLabs supporta streaming chunked; riduce latenza first-byte. Out of scope per questa fetta.
