# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 — chat Mani: ascolto più severo di default (zero risposte non richieste)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #371 (https://github.com/Gasss23/Gas/pull/371): review APPROVATO; merge secondo CLAUDE.md §10 (verdetto testuale del bot sull'head, CI verde).
2. Al mattino: prova dal vivo di «Hey Jarvis» con 0,7 e 3 blocchi; se non scatta, `GAS_ASCOLTO_SOGLIA=0.6` o `GAS_ASCOLTO_BLOCCHI_PAROLA=2` nel .env.

---

## §1 SCOPE & ESITO FETTE

- **Default più severi dell'ascolto (priorità ALTA dell'operatore via M1)**: `FATTA` — 84481ea, review #757-M1 APPROVATO CON RISERVE (R-757-1-M1 MEDIA chiusa) e #758-M1 APPROVATO.
- **Lettura dei log del Mac**: `DEFERITA — l'operatore dorme, ascolto in pausa`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 clients/voice/ascolto.py           |  55 ++++++++++++++++++++++++++++++++++++-------------------
 reports/diff_sessione.md           |  12 ++++++------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  15 ++++++---------
 scripts/voce/LEGGIMI.md            |  35 ++++++++++++++++++++++-------------
 tests/test_unit_voce_ascolto.py    |  68 +++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------
```

NB: per la regola «n/d» dell'operatore (2026-10-24) la riga di `reports/handoff.md` dice `n/d` e manca la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
84481ea fix(voce): ascolto più severo di default — zero risposte non richieste — review #757-M1/#758-M1
1aa50f0 chore(revisore): memoria review #758 — APPROVATO
e1d46fa chore(revisore): memoria review #757 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 84481ea: verdetto integrale della review #757-M1 (primo giro) e della re-review #758-M1 (sul diff committato).

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md, la voce di stato_progetto.md sull'ascolto H24 (riga 694) e la coda di memoria_revisore.md. Il diff non tocca kernel, provider, `_get_window` o il cap di 10 iterazioni. Non c'è slicing della history e non c'è simulazione di tool.

**Elementi esaminati**
- clients/voice/ascolto.py:118 — `MAX_TURNI_PREDEFINITO = 1`. Rischio controllato: che la finestra si apra comunque. **Esito: ok.** In `conversazione` il controllo `turni >= self.max_turni` (clients/voice/ascolto.py:844) fa `break` prima di `aspetta_voce` (clients/voice/ascolto.py:850). Lo conferma anche il nuovo test `test_col_predefinito_di_main_niente_turni_di_seguito`.
- clients/voice/ascolto.py:836 — il ramo dell'interruzione con la parola, con max_turni=1. Rischio controllato: l'interruzione resta utilizzabile? **Esito: riserva MEDIA (R-757-1-M1).** L'ho provato con lo stesso scenario di `test_la_parola_interrompe_gas_e_apre_una_nuova_richiesta`:
  - con max_turni=3: suona A poi C, 2 invii, due bip;
  - con max_turni=1: suona solo A, 1 invio, un bip.
  Quindi «Hey Jarvis» detto mentre Gas parla lo ferma, ma la nuova domanda non viene registrata e non c'è il bip: va ripetuta la parola una seconda volta. scripts/voce/LEGGIMI.md:47 promette invece «fa il bip e ascolta la nuova domanda». Va contro l'obiettivo «zero risposte non richieste»? No, è più prudente. Però una funzione documentata (fetta 41) si spegne in silenzio. Due rimedi possibili, a scelta vostra o dell'operatore:
  1. dare all'interruzione un tetto suo, per esempio permettere almeno 1 interruzione anche con max_turni=1, tenendo il tetto di R-668-1 contro l'eco;
  2. documentare nel LEGGIMI che, con il default, interrompere = solo «fermati».
  Nessun test copre interruzione + max_turni=1: aggiungerne uno.
- clients/voice/ascolto.py:125-126 — soglia 0,7 e 3 blocchi di fila. Rischio: la parola vera non scatta più (R-736-1). **Esito: ok.** Il rimedio è scritto sia nel commento (clients/voice/ascolto.py:123-124) sia nel LEGGIMI (scripts/voce/LEGGIMI.md:129-131: `GAS_ASCOLTO_SOGLIA=0.6` / `GAS_ASCOLTO_BLOCCHI_PAROLA=2`). La tabella è verificata dai nuovi test.
- clients/voice/ascolto.py:346-349 — il costruttore ora ha default letterali (15 / 3 / 0,7). Rischio: qualcuno usa ancora i default del costruttore. **Esito: ok.** L'unico `Ascolto(` fuori dai test è in main (clients/voice/ascolto.py:1235), che passa sempre soglia, blocchi_parola, finestra_s, max_turni e soglia_interruzione. `MAX_TURNI_PREDEFINITO`, `FINESTRA_PREDEFINITA_S` e `SOGLIA_INTERRUZIONE_PREDEFINITA` non compaiono in nessun altro file .py.
- clients/voice/ascolto.py:154 — interruzione a 0,8, sopra la soglia normale di 0,7. **Esito: ok**, c'è anche un assert nel test di main.

**Riserve BASSE**
- scripts/voce/LEGGIMI.md:50 dice ancora «soglia 0.7 invece di 0.5»: ora è 0.8 contro 0.7.
- I commenti a clients/voice/ascolto.py:153 («quella normale (0.5)») e clients/voice/ascolto.py:846 («soglia 0,7 … 0,6») sono rimasti con i valori vecchi.
- Il test si chiama `test_finestra_di_15_secondi` ma verifica `FINESTRA_PREDEFINITA_S == 10.0`. Il nome è difendibile, perché la prova usa i 15 s del costruttore, ma confonde.

**Cosa NON ho verificato**
- Il comportamento dal vivo sul Mac (falsi positivi e mancate attivazioni con 0,7 e 3 blocchi): non si può riprodurre senza microfono e openWakeWord. Va provato dall'operatore col nuovo log.
- browser_server.py: non è toccato, quindi non l'ho esaminato.
- La suite completa del motore: ho rilanciato solo tests/test_unit_voce_ascolto.py (315 passed).

Memoria: riga #757-M1 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con lo script (e1d46fa). La lezione: quando si abbassa a 1 un tetto condiviso come max_turni, va provato ogni ramo che lo usa.

## VERDETTO: APPROVATO

Re-review #758-M1: approvato. La riserva MEDIA della #757 è risolta e le riserve BASSE pure. 317 test passano.

**Elementi esaminati**
- clients/voice/ascolto.py:157 — la nuova costante `TURNI_CON_INTERRUZIONE = 2`, col commento che la lega a R-757-1-M1. Rischio controllato: che allarghi i turni di seguito senza parola. **Esito: ok.** Si usa solo nel ramo dell'interruzione.
- clients/voice/ascolto.py:842 — il tetto `max(self.max_turni, TURNI_CON_INTERRUZIONE)` nel ramo `if self.interrotto`. **Esito: ok.**
  - Rischio 1, che dopo la domanda nata da un'interruzione si apra la finestra con i seguiti spenti. Il controllo di clients/voice/ascolto.py:850 usa ancora `self.max_turni` puro. Al secondo turno turni=2 ≥ 1, quindi `break` prima di `aspetta_voce`.
  - Prova fatta: parola, interruzione con nuova domanda, poi voce senza parola, con finestra 10 e max_turni=1. Risultato: si sentono A e B, 2 invii, la voce che segue NON viene inviata.
  - Rischio 2, cioè R-668-1 (la voce di Gas che si interrompe da sola all'infinito). Resta limitato: la seconda interruzione chiude la conversazione. Lo verifica `test_coi_seguiti_spenti_la_seconda_interruzione_chiude` (tests/test_unit_voce_ascolto.py:2763).
  - Con max_turni ≥ 2 il comportamento non cambia, perché il max vale quanto max_turni.
- tests/test_unit_voce_ascolto.py:2752 — `test_coi_seguiti_spenti_l_interruzione_apre_ancora_la_nuova_domanda`. Copre esattamente il caso che la sonda della #757 aveva trovato rotto. **Esito: ok.** I mutanti dichiarati («tetto = max_turni» e «tetto 9») fanno fallire un test ciascuno, coerente con i due test nuovi.
- scripts/voce/LEGGIMI.md:51 — ora dice «0.8 invece di 0.7» e spiega l'interruzione coi seguiti spenti: la prima apre la nuova domanda, la seconda ferma Gas. **Esito: ok**, coerente col codice. Anche le altre BASSE della #757 sono chiuse (commenti con i numeri vecchi, nome del test sulla finestra).

**Cosa NON ho verificato**
- Il comportamento dal vivo sul Mac: se 0,8 durante la risposta di Gas sente ancora la parola vera e se 0,7 con 3 blocchi riduce davvero le attivazioni per sbaglio. Senza microfono e openWakeWord non si può riprodurre: va provato dall'operatore col log.
- La suite completa del motore: ho rilanciato solo tests/test_unit_voce_ascolto.py (317 passed).

Memoria: riga #758-M1 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (1aa50f0).

## §5 DELTA TEST DEL MOTORE

Kernel non toccato. `tests/test_unit_voce_ascolto.py`: da 314 (base 904d9d6) a 317 casi. `test_unit_voice_server.py` + `test_unit_manutenzione.py` (-k "not browser"): 233 passed.

```
317 passed in 28.62s
```

Mutanti presi: tetto dell'interruzione = max_turni (1 failed), tetto 9 (1 failed).

## §6 STATO CI

`gh` non autenticato nel container (GitHub passa dallo strumento MCP). Mappatura commit→run:
- e1d46fa, 1aa50f0 (memoria del revisore): nessuna run su questo SHA (pushati insieme a 84481ea).
- 84481ea: run del push del branch non letta alla scrittura; la PR #371 è stata aperta dopo.
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Da provare dal vivo: con soglia 0,7 e 3 blocchi la parola vera scatta ancora? (stesso tema di R-736-1). Rimedio documentato nel LEGGIMI.
- La pagina web della voce (`clients/voice/browser_server.py`) resta a 12 s e 5 turni (V-4 verifica esterna #361): prossima fetta voce.
- Le riserve della PR #368 restano in `reports/stato_progetto.md`.
