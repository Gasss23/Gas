# Prova R1 — giro notturno provato dal vero (procedura per il Mac)

> Scritta il 10 novembre 2026 dalla chat M4. Roadmap: R1 in `reports/roadmap.md`.
> Si fa **una notte sola**: la sera prepari (10 minuti), la mattina controlli (5 minuti).
> Copia i comandi dei riquadri nel Terminale del Mac, uno alla volta.

## Cosa è già provato e cosa manca

Già provato (ottobre): messaggio del mattino, bottoni Approva/Rifiuta **di giorno** (giro lanciato a mano con `/notte`), timer `com.gas.notte` installato, giro delle 03:13 del 29 ottobre col cervello forte.

Manca, ed è quello che prova questa notte:

1. Il timer parte **alle 03:00 da solo** (non al risveglio del Mac, non a mano).
2. Una richiesta di firma **nata di notte** arriva su Telegram, **resta valida fino al mattino** (24 ore) e il click su Approva **del mattino** la esegue. Prima nessuna azione rischiosa parte da sola.
3. Riga «Riflessione:» nel resoconto del giro e lezioni in `gas lezioni lista`.
4. Avviso `knowledge_fts` tolto (archivio della conoscenza creato).

Nessuna modifica al codice serve per questa prova: il codice c'è già tutto.

---

## SERA (prima di andare a dormire)

**1. Codice aggiornato e ambiente attivo**

```
cd ~/Gas && git checkout main && git pull && source .venv/bin/activate
```

**2. Controllo generale** — non deve esserci nessuna riga FAIL; «Cervello forte» deve dire OK.

```
python3 gas.py doctor
```

**3. Archivio della conoscenza** (toglie l'avviso `knowledge_fts`, una volta sola)

```
python3 tools/ingest_knowledge.py
```

**4. Timer notturno installato e alle 03:00** — la prima riga deve mostrare `com.gas.notte`, poi `Hour => 3` e `Minute => 0`.

```
launchctl list | grep com.gas.notte; plutil -p ~/Library/LaunchAgents/com.gas.notte.plist | grep -A3 StartCalendarInterval
```

Se `com.gas.notte` non compare, reinstallalo:

```
mkdir -p ~/Gas/.gas_notte ~/Library/LaunchAgents && sed "s/TUO_UTENTE/$(whoami)/g" ~/Gas/scripts/notte/com.gas.notte.plist > ~/Library/LaunchAgents/com.gas.notte.plist && launchctl load ~/Library/LaunchAgents/com.gas.notte.plist
```

**5. Compito di prova nel catalogo** — prima una copia di sicurezza, poi aggiungi il compito `prova_firma_r1`: chiede a Gas di creare un piccolo script, cosa che **richiede sempre la tua firma**.

```
cp ~/.gas_notte.yaml ~/.gas_notte.yaml.prima_di_r1
```

```
printf '\n' >> ~/.gas_notte.yaml && cat >> ~/.gas_notte.yaml <<'EOF'
  - nome: prova_firma_r1
    cervello: forte
    prompt: >-
      Prova del giro notturno (R1). Usa write_file per creare il file
      prove_r1/buongiorno.sh con dentro una sola riga: echo buongiorno.
      Non fare altro: se serve la firma, aspettala.
EOF
```

Controllo del catalogo — deve stampare `prova_firma_r1` tra i compiti e `avvisi: []`:

```
python3 -c "from pathlib import Path; from modules.notte.notte import carica_catalogo; c,a=carica_catalogo(Path.home()/'.gas_notte.yaml', Path.cwd()); print('compiti:', [x['nome'] for x in c]); print('avvisi:', a)"
```

**6. Nessuna cartella di prova rimasta** — deve dire «No such file or directory»:

```
ls ~/Gas/prove_r1
```

**7. Bot Telegram acceso tutta la notte, e Mac sveglio.** Prima guarda se il bot gira già (se stampa una riga con `gas.py telegram`, NON avviarne un secondo e salta al comando `caffeinate -s` qui sotto, da solo):

```
pgrep -fl "gas.py telegram"
```

Se non gira, in una **finestra nuova** del Terminale (lasciala aperta):

```
cd ~/Gas && source .venv/bin/activate && caffeinate -s python3 gas.py telegram
```

Se il bot girava già, in una finestra nuova (lasciala aperta):

```
caffeinate -s
```

`caffeinate -s` tiene il Mac sveglio finché la finestra è aperta, **solo se è attaccato alla corrente**. Lo schermo può spegnersi. Se è un portatile: **alimentatore attaccato e coperchio aperto** (a coperchio chiuso dorme comunque).

Fine della sera. Non lanciare il giro a mano: deve partire da solo alle 03:00.

---

## MATTINA (prima di toccare Telegram)

**A. Messaggio del mattino su Telegram.** Deve esserci un messaggio «Gas — giro notturno del …» con **ora tra le 03:00 e le 03:10**, e due righe del tipo:
- `OK punto_lead (…)`
- `OK prova_firma_r1 (…) — in attesa della tua firma: 1`

Deve esserci anche, verso le 03, **la richiesta di firma con i bottoni** Approva/Rifiuta per `prove_r1/buongiorno.sh`. **Non cliccare ancora.**

**B. Il giro è partito dal timer e ha mandato il messaggio** — guarda l'ora nella prima riga e «Riepilogo Telegram inviato.»:

```
cd ~/Gas && source .venv/bin/activate && head -5 .gas_notte/ultimo_giro.md && grep -n "Riepilogo Telegram\|NON avviato\|INTERROTTO" .gas_notte/launchd.log | tail -3
```

**C. Resoconto completo** — cerca: `punto_lead — OK` con la riga «Riflessione: …», e `prova_firma_r1 — OK` con «in attesa della tua firma su Telegram: 1»:

```
grep -n "^## \|Riflessione\|in attesa\|Errore" .gas_notte/ultimo_giro.md
```

**D. Niente è partito da solo** — deve dire ancora «No such file or directory»:

```
ls ~/Gas/prove_r1
```

**E. Ora clicca «Approva»** sulla richiesta di firma di stanotte su Telegram (il bot deve essere acceso). Poi controlla che il file sia stato scritto — deve stampare `echo buongiorno`:

```
cat ~/Gas/prove_r1/buongiorno.sh
```

**F. Controllo finale** — nessun FAIL; la riga «Firme» deve finire con «nessuna scaduta»; poi le lezioni proposte stanotte:

```
python3 gas.py doctor; python3 gas.py lezioni lista
```

**G. Pulizia** — togli il file di prova, rimetti il catalogo di prima, chiudi la finestra con `caffeinate` (Ctrl-C; se lì girava anche il bot, riavvialo normalmente):

```
rm -r ~/Gas/prove_r1 && mv ~/.gas_notte.yaml.prima_di_r1 ~/.gas_notte.yaml
```

---

## Esito

**R1 passa** se A, B, C, D, E e F sono come descritto. Manda a M1 l'output di B, C, E, F e una foto del messaggio del mattino (A).

Se qualcosa non va, cosa guardare:

| Sintomo | Probabile causa | Comando |
|---|---|---|
| Nessun messaggio, `ultimo_giro.md` vecchio | Timer non partito o Mac addormentato | `cat ~/Gas/.gas_notte/launchd.log \| tail -20` |
| Messaggio arrivato ma ora diversa dalle 03 | Mac addormentato: è partito al risveglio | controlla corrente e coperchio, ripeti la notte |
| `prova_firma_r1` KO | cervello forte fermo o errore del modello | `grep -n "prova_firma_r1\|Errore" ~/Gas/.gas_notte/ultimo_giro.md` |
| Firma non arrivata | chiavi Telegram o testo troppo lungo | `tail -50 ~/Gas/gas_debug.log` |
| Click su Approva senza effetto | bot spento al momento del click | avvia il bot: il click viene letto all'avvio (Telegram lo tiene 24 ore) |
| `prove_r1` già presente al mattino prima del click | **grave**: azione eseguita senza firma | fermati e manda subito l'output a M1 |

Dopo la prova: le notti vere senza il Mac acceso restano a R5 (server sempre acceso).
