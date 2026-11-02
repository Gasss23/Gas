# Ultimo report — 2026-11-02 — Voce V6 «capire meglio» (chat M2) — PR #318

## DECISIONI UMANE RICHIESTE

1. Merge della PR #318 (https://github.com/Gasss23/Gas/pull/318): il check del bot è neutral (la PR tocca ci.yml): il merge lo decide l'operatore.
2. Dopo il merge, prova sul Mac (`reports/prova_voce_mac.md`): guardare la riga «Ho capito: …»; se Gas dice spesso «Non ho capito bene» parlando chiaro, `GAS_VOICE_STT_LOGPROB_MIN=-1.3` nel `.env`.

## Esito delle fette

- **V6.1 — trascrizione**: `FATTA` — `modules/voice/stt.py`: Whisper era già `whisper-large-v3`; ora `language=it`, `temperature=0`, `verbose_json`, prompt col vocabolario di Gas. Trascrizioni incerte (confidenza media pesata < -1,0; silenzio = no_speech > 0,8 E confidenza < -0,5; frasi inventate da Whisper sul silenzio; eco contigua del prompt di ≥4 parole) → «Non ho capito bene, puoi ripetere?» senza turno del kernel (conta nel tetto orario). Soglie via env.
- **V6.2 — trasparenza**: `FATTA` — campo `capito` nelle risposte parlate del server; la pagina mostra «Ho capito: «…»» (solo testo).
- **V6.3 — risposte e contesto**: `FATTA` — la storia c'era già (kernel unico della voce, il forte riceve la finestra degli ultimi messaggi). Nuovo `tests/test_unit_voice_contesto.py` (server + GasKernel vero, cervelli finti) lo prova per forte e normale; mutante su `_get_window` → 2 failed. ISTRUZIONE_VOCE / _SCHERMO: frasi brevi senza perdere il filo, parole storpiate dalla trascrizione, una sola domanda se ambiguo.
- **V6.4 — tasto «non hai capito» con modello più grande**: `SALTATA` — usiamo già il modello più grande di Groq.
- **Riserva V-1 bot #314** (Groq 500 conta nel tetto): `FATTA` (test). **V-2 bot #314** (conteggi §2 dell'handoff): `FATTA` (handoff riscritto con i conteggi della sessione).
- **stato_progetto**: prova sul Mac della V5 passata, registrata.
- **Riserve di bot e verifica esterna su e1f0131**: `FATTA` (254c4a5) — eco corta del prompt scartata solo con no_speech > 0,9 (`GAS_VOICE_STT_ECO_NO_SPEECH`), segmenti NaN/inf saltati, `capito` azzerato a ogni richiesta, «non ho capito» come testo se manca ElevenLabs, `List[str]`, tmp_path nel test. Review #614-M2 (branch V6) con riserve, #617-M2 APPROVATO. V-2 ve («Grazie.» isolato) `DEFERITA — da tarare sul Mac`.
- **Riserve di bot e verifica esterna su ded8469**: `FATTA` (17c9352) — segmento malformato saltato come i NaN, `GAS_VOICE_STT_ECO_NO_SPEECH` documentata, conteggio dei test nell'handoff corretto. Review #623-M2 APPROVATO.
- gas.py / brains/: non toccati. ci.yml: solo il nuovo file di test nella voice suite.

Review: #611-M2 APPROVATO CON RISERVE, #612-M2 APPROVATO CON RISERVE (riserve chiuse), #613-M2 APPROVATO. Test: voce stt + contesto 63 passed; stt+server+tts non-browser 122 passed (prima delle ultime correzioni a stt); pagina nel browser (obbligatoria) 10 passed.

## Anomalie

- `gh` non autenticato nel cloud: PR aperta con l'integrazione GitHub.
