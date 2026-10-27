# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-27 — V-1 della verifica esterna #273 (chat Motore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione: numero e URL nel commit successivo (dalla risposta di `create_pull_request`; `gh` nel cloud non è autenticato).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Merge della PR #274**: `FATTA` — conflitto col main #275 risolto (review #525), merge su richiesta dell'operatore.
- **Fetta 2 — V-1 ve #273**: `FATTA` — comportamento invariato (il fix proposto rompeva T20d senza chiudere un percorso reale), commento corretto e test T21b2; review #526 APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 gas.py                             |  7 +++++--
 reports/diff_sessione.md           |  8 +++++---
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |  4 ++--
 reports/ultimo_report.md           | 14 ++++++--------
 tests/test_unit_kernel.py          | 12 ++++++++++++
```

NB: regola «n/d» — conteggio di `reports/handoff.md` non misurabile, riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
8b6a965 fix(memoria): V-1 ve #273 — pin con contatti illeggibili: comportamento chiarito e fissato da un test
661d2d0 chore(revisore): memoria review #526 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #526 (integrale, commit 8b6a965)

## VERDETTO: APPROVATO

L'analisi regge. Ho cercato un percorso in cui un contatto non fidato arrivi al modello quando la lettura dei contatti fallisce, e non ne ho trovati. Tenere il segno a False quando la lettura fallisce è corretto: metterlo a True farebbe passare alla firma ogni scrittura con la memoria guasta (rompe T20d) senza chiudere nessun percorso reale.

Elementi del diff esaminati:
1. `gas.py:3645` — nuovo commento: se la lettura fallisce, nel pin non entra nessun lead e il segno resta False di proposito. Rischio esaminato: che il commento copra un fail-open reale. `gas.py:3653` chiama `lista_contatti`, che con la lettura fallita restituisce `[]`. Quindi la lista dei lead attivi è vuota, nel pin non c'è la sezione dei lead e nessun campo di contatto raggiunge il prompt di sistema. Le eccezioni restano in fail-closed: il ramo except mette il segno a True (`gas.py:3707`). Esito: ok.
2. `tests/test_unit_kernel.py:1035` — T21b2: rimpiazza `lista_contatti` con una funzione che restituisce `[]`, poi controlla che il pin non abbia lead, abbia ancora il diario («DM inviato a Mario») e che il segno resti False. Rischio esaminato: che il test non morda. Se si applica il fix proposto (`leggi_contatti` con True su None), il rimpiazzo non agisce più, Mario torna nel pin e la condizione «## Lead attivi not in pin_ko» fallisce. Il test quindi rileva il cambio, anche se con un messaggio di errore poco esplicito. Esito: ok.

Contesto, file non toccati:
3. `modules/gate/gate.py:82` — `ricorda` è tra i tool di input non fidato (`UNTRUSTED_INPUT_TOOLS`): se il modello legge i contatti con `ricorda`, la finestra risulta contaminata a prescindere dal pin. Esito: ok.
4. `gas.py:4256` — `salva_contatto` e `imposta_stato_contatto` restituiscono solo la chiave e lo stato forniti dal modello, mai campi letti da un contatto salvato. Le righe del diario scritte in turni contaminati entrano nel pin mascherate (dettagli e tipo omessi). `_pin_non_fidato_visto` resta vero fino a `clear`. Esito: nessun percorso alternativo.

Finding:
1. COSMETICA: T21b2 rimpiazza `lista_contatti` e non `leggi_contatti`. Va bene oggi, ma se il codice passasse a `leggi_contatti` il test fallirebbe con un messaggio che non spiega il motivo. Non blocca.

Rischio escluso: non ho riprodotto un vero «database is locked» fra due processi né provato `gas notte` dal vero con il DB guasto. Il ramo d'errore è lo stesso (`leggi_contatti` → None → `[]`), già coperto da #520.

Verifica: kernel rifatto da me, 1044 PASS 0 FAIL.

Memoria: riga #526 più una lezione, committata da sola in 661d2d0 (/home/user/Gas/.claude/agents/memoria_revisore.md).

## §5 DELTA TEST DEL MOTORE

- Kernel: 1043 → 1044 PASS (T21b2 nuovo), 0 FAIL. Blocco reale: `=== RIEPILOGO: 1044 PASS, 0 FAIL ===`

## §6 STATO CI

`gh` nel cloud non è autenticato. 661d2d0, 8b6a965 e commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- COSMETICA #526: T21b2 sostituisce `lista_contatti`, non `leggi_contatti`.
- Preesistenti: V-1 bot #273 (BASSA), R-520-1 (BASSA), R-516-1 (COSMETICA), bot #269 «/forte@NomeBot» (BASSA), COSMETICHE ve #269.
