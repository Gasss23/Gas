# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-03 — Voce V10: «audio+pezzi», voce senza schermo (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. PR della V10: da aprire (numero dopo la creazione).
2. Client H24 (chat Mani): usare `X-Gas-Formato: audio+pezzi`, gestire anche il JSON 200 con `errore_voce` senza chiave ElevenLabs.

---

## §1 SCOPE & ESITO FETTE

- **V10 — formato «audio+pezzi» per il client senza schermo**: `FATTA` (review #660-M2).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 modules/voice/server.py            |  36 ++++++++++++++++++++++++++++++++++--
 reports/diff_sessione.md           |  16 ++++++----------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  26 +++++++++++++-------------
 tests/test_unit_voice_server.py    |  57 ++++++++++++++++++++++++++++++++++++++++++++++++++++++---
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
f7be4d0 feat(voce): V10 — formato «audio+pezzi» per il client senza schermo: tutta la risposta frase per frase, istruzione voce (chat M2; review #660-M2)
1d44d04 chore(revisore): memoria review #660 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit della V10 (f7be4d0). Review #660-M2:

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto CLAUDE.md (sez. 5), la parte di reports/stato_progetto.md sulla voce (V7b e V8) e la coda di .claude/agents/memoria_revisore.md. Il diff non tocca la storia dei messaggi né `_get_window`, non simula l'output dei tool e non indebolisce nessun guardrail.

**Cosa ho guardato nel diff**
- `modules/voice/server.py:423` — **ok.** Il turno a voce sceglie `ISTRUZIONE_VOCE_SCHERMO` solo se `_vuole_audio_testo()` è vero, e questa vale solo per «audio+testo» e «audio+testo+pezzi». Rischio controllato: che «audio+pezzi» prendesse l'istruzione pensata per lo schermo. Non succede, e il test lo verifica dall'istruzione che arriva al kernel.
- `modules/voice/server.py:176` — **ok, con una nota cosmetica.** `frasi_voce` tiene le frasi intere entro 1500 caratteri; se la prima frase è già più lunga la taglia all'ultimo spazio. Rischio controllato: una lista vuota con testo non vuoto, che manderebbe a `_do_pezzi_response` zero frasi. Non può succedere: il ramo di taglio copre il caso e il chiamante salta già il testo vuoto (`modules/voice/server.py:496`). Nota cosmetica: se `testo[:1500]` finisce proprio alla fine di una parola, `rsplit` la toglie lo stesso.
- `modules/voice/server.py:506` — **ok.** «audio+pezzi» passa per `_do_pezzi_response(frasi_voce)`, quindi stessi tempi della V7a/V7b (voce, voce_tutta, `_chiudi_tempi`), stesso stop se il client chiude e stessa gestione degli errori ElevenLabs. Ho provato un mutante (`frasi_parlate` al posto di `frasi_voce`): `test_v10_formato_audio_pezzi_senza_schermo` fallisce. Ho ripristinato il file dall'index.
- `modules/voice/server.py:464` — **ok.** «non ho capito» e «uso» arrivano a righe anche con il nuovo formato. Mutante che toglie il ramo: `test_v10_non_ho_capito_a_righe` fallisce. Ripristinato dall'index; il working tree è pulito.
- `tests/test_unit_voice_server.py:1196` — **ok.** L'helper passa da `return_value` a `side_effect=[trascrizione]`: la trascrizione viene chiamata una volta sola per richiesta, quindi i test V7b esistenti restano verdi.

**Contesto (file non toccati)**
- `clients/voice/ascolto.py:413` — oggi il client manda `Accept: audio/mpeg` senza `X-Gas-Formato`, quindi il suo comportamento attuale non cambia. Lo sceglierà M1.
- Restano invariati il percorso MP3 grezzo (`modules/voice/server.py:453`) e la pagina col formato «audio+testo+pezzi» (`modules/voice/server.py:503`). Il nuovo controllo viene dopo, nell'ordine dei rami.

**Costo ElevenLabs**
- Il tetto di 1500 caratteri spende meno del percorso MP3 attuale, che sintetizza tutta la risposta senza tetto (`modules/voice/server.py:586`).
- Il caso peggiore teorico è 60 turni/ora (`GAS_VOICE_MAX_TURNI_ORA`, controllato prima di Groq) × 1500 = 90.000 caratteri/ora.
- Nella pratica `ISTRUZIONE_VOCE` chiede 1-3 frasi brevi, quindi il tetto scatta di rado.
- Dividere in frasi non aggiunge caratteri, solo più richieste.

**Riserve**
- **R-660-1-M2 (BASSA):** nessun test per il caso senza chiave ElevenLabs con «audio+pezzi». In quel caso la risposta è un JSON 200 con `errore_voce`, non NDJSON, mentre oggi col MP3 era un 503. Il client H24 di M1 deve gestire anche questo caso: va detto a M1.
- **R-660-2-M2 (COSMETICA):** il taglio della prima frase lunga perde l'ultima parola quando il testo finisce esattamente al confine dei 1500 caratteri.

**Prove:** ho rieseguito `tests/test_unit_voice_server.py`: 95 passed. Con i due mutanti, 1 test V10 fallito ciascuno.

**Cosa non ho verificato:**
- Il comportamento reale col client H24 sul Mac e con ElevenLabs vero: non si riproduce qui e `ascolto.py` non è nel diff.
- Le altre suite voce (stt, contesto, voce_ascolto, prova_voci), che dichiari 334 passed: non le ho rieseguite, il diff non le tocca.
- Le tariffe ElevenLabs effettive.

**Memoria:** ho aggiunto la riga #660-M2 a `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata con lo script (1d44d04). Il diff staged è rimasto intatto (2 file, +88/−5).

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: 3 test nuovi V10 (`test_v10_frasi_voce_tutto_il_parlato_senza_schermo`, `test_v10_formato_audio_pezzi_senza_schermo`, `test_v10_non_ho_capito_a_righe`); mutante (server di main) → 3 failed. voice_server + voice_stt + voice_contesto + voce_ascolto + voice_prova_voci: 334 passed (`GAS_TEST_BROWSER_OBBLIGATORIO=1`). Kernel non toccato (`gas.py` identico a main).

## §6 STATO CI

`gh` non autenticato nel cloud. Commit della sessione e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo la testa).

## §7 RISERVE APERTE

- R-660-1-M2 BASSA: nessun test per «audio+pezzi» senza chiave ElevenLabs (JSON 200 con `errore_voce`, non NDJSON): il client H24 deve gestirlo.
- R-660-2-M2 COSMETICA: il taglio di una prima frase più lunga di 1500 caratteri perde l'ultima parola se il testo finisce esattamente al confine.
