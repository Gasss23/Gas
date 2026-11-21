# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-21 — M1 — Voce: `registra_voce.py` si ferma subito col microfono muto; «ogni 9 secondi»

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge di questa PR: con riserve del bot serve il «mergia» dell'operatore; lo esegue l'agente.

---

## §1 SCOPE & ESITO FETTE

- **PR #390:** MERGIATA il 21-11 (dcedea6a) col via dell'operatore («ok mergia quando è tutto verde»).
- **Fetta #813 — note del bot su #390 (V-1 microfono muto, V-2 «7.5») e R-810M1-2:** FATTA, commit b46fde99 (cherry-pick di 5eb5780f su main dcedea6a, stesso diff: SHA-256 31c92e5c). Review #813-M1coord APPROVATO CON RISERVE (R-813M1-1 BASSA).

---

## §2 GIT DIFF --STAT (sessione)

```
(da rigenerare)
```

## §3 GIT LOG --ONELINE (sessione)

```
(da rigenerare)
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #813-M1coord (commit 5eb5780f, riportato come b46fde99)

## VERDETTO: APPROVATO CON RISERVE

Review #813-M1coord del diff staged del branch fix/voce-registra-microfono-muto (3 file, +69/−3, sha256 31c92e5c).

Elementi del diff esaminati:
- `scripts/voce/registra_voce.py:277` — `Errore` se dopo l'ultima prova (`_prova == TENTATIVI_PAROLA - 1`) il microfono non ha mai dato suono (microfono muto senza errore, cioè permesso negato). Rischi esaminati:
  - falso stop dopo un primo suono: non succede, il flag resta True;
  - stop già alla prima prova muta: no, il mutante `if not self.sentito_suono:` viene ucciso dal test sul microfono muto;
  - controllo che non scatta mai: il mutante `if False:` viene ucciso.
  - Esito: ok.
- `scripts/voce/registra_voce.py:302` — `sentito_suono = True` appena il volume supera la soglia, prima del controllo del riconoscitore. Corretto: anche un rumore o una parola non riconosciuta provano che il microfono funziona. Rischio esaminato: un test che non protegge questo punto. Il mutante che segna il flag solo sulle clip tenute sopravvive (379 passed). Esito: **riserva R-813M1-1 BASSA**: manca un test «suono forte non riconosciuto per 3 volte → la registrazione non si ferma»; senza, un refactoring può far fermare per «permesso» un microfono che funziona.
- `scripts/voce/registra_voce.py:267` — il messaggio dice «ogni %d secondi» con `math.ceil(6.0 + 1.5 + 1.0)` = 9. Rischi esaminati: numero non intero o senza margine. Esito: ok; il test controlla 9 e l'assenza di «7.5». Chiude V-2 e R-810M1-2; resta da vedere sul Mac se 9 secondi bastano.
- `scripts/voce/registra_voce.py:625` (contesto, nel main) — `except Errore` stampa «✗ …» ed esce con 1, senza traceback; nessuna clip salvata perché non c'è mai stato un suono. Esito: ok (§9).
- `tests/test_unit_voce_ascolto.py:3607` — test sul microfono che dà solo silenzio: controlla l'`Errore` con «permesso» e che i bip siano esattamente TENTATIVI_PAROLA (3, non 45). Esito: ok.

Nota COSMETICA: se il microfono funziona ma l'operatore resta zitto ai primi 3 bip, il messaggio sul permesso è fuorviante; danno nullo, basta rilanciare lo script.

Wall of Shame: non riguarda questo diff (niente history, tool o provider).

Test: 379 passed, rieseguiti su una copia dell'indice con `checkout-index`, senza stash; provati anche 3 mutanti.

Rischio escluso: il comportamento vero su macOS col permesso negato non si riproduce qui. Non so se CoreAudio dà silenzio puro o un rumore minimo sopra `VOCE_RMS_PREDEFINITO/2`; nel secondo caso il controllo non scatterebbe.

Memoria aggiornata con la riga #813-M1coord e una lezione sui flag di stato impostati prima delle uscite anticipate (commit 85d51212, riportato come ca88c976).

---

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_voce_ascolto.py`:** 376 su main dcedea6a → 379 passed (3 test nuovi). Mutanti del revisore: 2 uccisi, 1 sopravvissuto (R-813M1-1).
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.

## §6 STATO CI

Run della PR non ancora disponibile alla scrittura dell'handoff: il ramo si pusha col commit di fine-task che contiene questo file.

## §7 RISERVE APERTE

- **R-813M1-1 BASSA:** test mancante sul flag `sentito_suono` (vedi §4).
- **Bot #390, ultimo giro (BASSE):** V-1 nessun test di main() con un motore che ha `misura`; V-2 soglia 0,5 s della parola tagliata forse larga; V-3 clip da vicino accorciate dal taglio sul picco.
- **Chiuse:** V-1/V-2 del bot su #390 (giro su c95ea806), R-810M1-2.
