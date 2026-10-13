# REPORT — Raccolta dei problemi aperti dalla fetta `cerca_testo`

**Data:** 2026-10-13
**Ramo:** `docs/problemi-aperti-post-193` (da `origin/main` `a9fd74d`)
**Task:** su richiesta dell'operatore, raccogliere in un posto solo tutti i problemi trovati nella fetta
`cerca_testo` (PR #193), per chiuderli in un'unica sessione.

---

## DECISIONI UMANE RICHIESTE

1. **Merge di questa PR** (numero e URL in `reports/handoff.md` §0). Non la mergio io: `reports/stato_progetto.md`
   non è nella lista bianca `LOG_DI_SESSIONE` di `scripts/bot_esito.py`, quindi non ricade nell'eccezione di
   merge autonomo per i soli log di sessione.
2. **Due voci della lista sono decisioni tue, non lavoro da fare**: `C1`/`R-297-3` (il salto dei log non
   dipende dalla dimensione — l'alternativa condizionata è provata e perde la protezione sul tetto dei
   risultati) e `E2` (la numerazione univoca delle review: otto duplicati, da decidere sul ramo di
   integrazione).
3. **`E4`: resta da chiarire se hai una sessione viva altrove.** Quattro commit di autore ignoto sono entrati
   nella PR #193 da fuori questa macchina. Non è un problema di codice: è sapere chi scrive sul repo.

---

## ESITO

**FATTA.** Scritta in `reports/stato_progetto.md` la sezione «Problemi aperti dalla fetta `cerca_testo`
(PR #193) — da chiudere in UNA sessione»: **13 voci in 5 gruppi** (A hook, B bot, C `cerca_testo`,
D sicurezza, E igiene/processo).

**Ogni voce è stata RIVERIFICATA su `origin/main` `a9fd74d`, non ricopiata dalla lista precedente.** È la
parte che vale: due voci risultavano già chiuse dal merge e le ho marcate come «non rifarle», una era chiusa
solo a metà, e nove erano ancora aperte.

Esiti della riverifica:
- **`R-gate-worktree-1` CHIUSA** per `review_gate.sh` dalla PR #196 (il file su main lo dichiara).
- **Ma `promemoria_end.sh` è ancora cieco al worktree** (riga 11: `PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"`):
  è la metà non corretta, ed è `A1`, la voce più grave della lista.
- **`R-gate-matcher-1` ancora aperta**: su main la riga 131 è ancora `grep -Eq 'git[[:space:]].*commit'`.
- **`R-300-2` e `R-301-4` già chiuse** dall'altro autore e presenti su main: marcate «non rifarle».
- **Nove buchi della denylist credenziali ancora tutti LEGGIBILI** su `a9fd74d`, verificati uno per uno con
  `lettura_consentita()` in un worktree temporaneo: `token_cache.json`, `kubeconfig`, `mywallet.dat`,
  `.vault-token`, `.dockercfg`, `_netrc`, `clientsecret.json`, `*.gpg`, `*.asc`.
- **`AGENTS.md`**: 12.284 byte in root, non tracciata su main, `check-ignore` → non ignorata.
- **Base sana**: su un worktree di `origin/main`, kernel **840 PASS / 0 FAIL** e pytest **1067 passed,
  1 skipped**.

Ogni voce porta: cosa succede, come si riproduce (con i numeri misurati), dove sta nel codice, cosa vuol dire
«fatto», e il vincolo di processo che comporta (perimetro di review, fetta di sicurezza, decisione
dell'operatore). Dove il revisore o la verifica esterna avevano corretto una mia conclusione, è scritto il
loro argomento e non il mio — per esempio su `C2` (`letti` conta anche il file «non letto»), che credevo
«una riga» e non lo è.

## ANOMALIE

Nessuna. Modifica di soli `reports/`, fuori dal perimetro di review: nessun revisore richiesto
(CLAUDE.md sez. 3).
