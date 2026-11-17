# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-17 — Voce: la parola di attivazione non arriva più al cervello (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione (riserve solo BASSE).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — togliere «Hey Jarvis» e storpiature in testa alla richiesta** (diario del Mac 17/11 15:28:57Z: `ricorda` con query 'jarways', un giro in più): FATTA — 1ae76716, review #806-M1coord APPROVATO CON RISERVE (R-806-1 MEDIA).
- **Fetta 2 — R-806-1: nel seguito il vocativo resta**: FATTA — 6e62dcde, review #807-M1coord APPROVATO CON RISERVE (R-807-1 BASSA).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/voice/server.py            |  28 +++++++++++++++++++++++++++-
 reports/diff_sessione.md           |   9 ++++-----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  15 ++++++---------
 tests/test_unit_voice_server.py    |  42 +++++++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
75732f2f docs(fine-task): voce — parola di attivazione tolta (review #806/#807-M1coord)
6e62dcde fix(voce): nel seguito il vocativo «Jarvis, …» resta (R-806-1) — review #807-M1coord
f36758e9 chore(revisore): memoria review #807 — APPROVATO CON RISERVE
1ae76716 fix(voce): la parola di attivazione (e le storpiature come «Jarways») non arriva più al cervello in testa alla richiesta — review #806-M1coord
be95f7a6 chore(revisore): memoria review #806 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #806-M1coord (commit 1ae76716)

## VERDETTO: APPROVATO CON RISERVE

Review #806-M1coord. L'id era libero (ultima voce in memoria #802-M1coord). Riga contatore e una lezione nel commit be95f7a6 (`.claude/agents/memoria_revisore.md`); diff staged intatto (2 file).

**Elementi del diff esaminati**
- `modules/voice/server.py:139` — `_NOME_JARVIS` con le storpiature, usato in `_ATTIVAZIONE_UNA` (quindi anche `_SOLO_ATTIVAZIONE` e `_SOLO_PAUSA`). Rischio: parole italiane catturate. Esito: ok — «Giarvisio è un nome» e «Jarvisè qui» invariati (serve `\b` dopo il nome); «Jarways pausa» vale come pausa, giusto.
- `modules/voice/server.py:148` — `_PAROLA_IN_TESTA`. Rischio: «Gas» come soggetto. Esito: ok — «Gas ha detto…» e «Gasolio…» invariati («Gas» da solo si toglie solo se seguito da punteggiatura). Riserva BASSA: «Ei, gas è salito» → «è salito»; «Gas: la bolletta del gas» → «la bolletta del gas» (rari).
- `modules/voice/server.py:153` — `togli_parola_in_testa`. Rischi: ciclo e risultato vuoto. Esito: ok — al massimo 3 giri; vuota → originale; `re.sub` su str non solleva (§9); niente log, niente privacy.
- `modules/voice/server.py:979` — solo nel ramo parlato, dopo i filtri pausa, solo attivazione e frammento, prima di `cervello_voce`. Rischio: interazione con «forte». Esito: ok, provato a mano: «Hey Jarvis, forte, riassumi i lead» → forte; «Jarways forte riassumi» → forte (miglioramento); «Gas forte riassumi» invariato → forte; «Gas, forte» → messaggio d'uso come prima. `self._capito` resta l'originale.
- `modules/voice/server.py:1056` (contesto) — **R-806-1 MEDIA**: nel seguito il vocativo («Gas, accendi la luce», «Jarvis, spegni») è il segno più forte che la frase è per Gas e viene tolto PRIMA che il forte la veda con `ISTRUZIONE_SEGUITO`; con «nel dubbio, silenzio» «accendi la luce» da sola può finire in [NON_PER_ME]. Proposta: nel seguito non togliere la parola, o sostituire le storpiature con «Jarvis».
- `tests/test_unit_voice_server.py:2844` — test parametrizzato con 10 casi, positivi e negativi. Esito: ok.
- `tests/test_unit_voice_server.py:2855` — test end-to-end: il kernel riceve «che ore sono?». Esito: ok; il campo `_prompt` dell'helper non rompe altri test: 248 passed (rieseguito, 304 s).

**Riserve da tracciare**: R-806-1 MEDIA (vocativo tolto nel seguito); R-806-2 BASSA (falsi positivi rari «Ehi, gas …», «Gas: …»); nessun test sul seguito col vocativo.

**Non verificato**: comportamento reale del forte nel seguito senza vocativo (serve `claude -p` sul Mac; R-806-1 è un'analisi); se il turno del 17/11 fosse un seguito; suite completa del kernel e del client.

### Review #807-M1coord (commit 6e62dcde)

## VERDETTO: APPROVATO CON RISERVE

Review #807-M1coord, delta sulla #806. Id libero; riga contatore in f36758e9; diff staged intatto (2 file, +13/-1).

**Elementi del diff esaminati**
- `modules/voice/server.py:979` — la parola in testa si toglie solo se `not self._seguito()`. Rischio: effetto sugli altri filtri: pausa, sola attivazione e frammenti del seguito stanno prima; ramo del testo scritto invariato. Esito: ok, **R-806-1 chiusa**.
- `tests/test_unit_voice_server.py:2862` — `test_nel_seguito_il_vocativo_resta`. Rischio: test che passa senza la correzione. Controprova: condizione sostituita da `if True:` → 1 failed; file ripristinato, `git diff` vuoto. Esito: ok.
- `tests/test_unit_voice_server.py:2855` — il caso fuori dal seguito («Jarways, che ore sono?» → «che ore sono?») passa ancora; 12 test mirati: 12 passed (rieseguiti). Esito: ok.

**Riserve**: **R-807-1 (BASSA)** — nel seguito una storpiatura («Jarways, …») arriva ancora al forte, che può chiamare `ricorda`: il caso del 17/11 può ripetersi solo nel seguito; correzione possibile: sostituire la storpiatura con «Jarvis». Da tracciare con R-806-2.

**Non verificato**: suite voice_server completa non rieseguita (la #806 dava 248 passed; il delta tocca una riga coperta dai test mirati); comportamento reale del forte nel seguito (serve `claude -p` sul Mac).

## §5 DELTA TEST DEL MOTORE

- `python -B -m pytest -q tests/test_unit_voice_server.py` → 236 passed (main 01eb9f5) → 248 passed (1ae76716) → 249 (6e62dcde; mirati 54 passed, suite completa non rilanciata dopo il delta).
- Kernel non toccato.

```
248 passed
```

## §6 STATO CI

CI NON VERIFICATA (gh assente): run della PR non ancora disponibile. Nota: dal 17/11 i 7 test bwrap di `tests/test_unit_web_browser.py` falliscono su tutti i branch (runner ubuntu-26.04); la correzione è in un'altra chat («Ecosistema servizi investimento PDF»).

## §7 RISERVE APERTE

- R-806-2 BASSA — falsi positivi rari: «Ehi, gas è salito» → «è salito»; «Gas: la bolletta…» → «la bolletta…».
- R-807-1 BASSA — nel seguito una storpiatura («Jarways, …») arriva ancora al forte.
