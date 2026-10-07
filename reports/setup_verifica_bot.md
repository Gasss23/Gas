# Setup del bot di verifica (V-B) — passi dell'operatore

Il bot è il workflow `.github/workflows/verifica-bot.yml`. Parte solo dopo il merge su main,
e solo sulle PR con l'etichetta `verifica`. I segreti li inserisci TU: l'agente non li vede mai.
Non incollare token o chiavi in chat.

**Ordine importante (V-6 verifica esterna #130):** nessuna PR va etichettata `verifica` prima
della fine del setup. Se il bot partisse prima, GitHub creerebbe l'environment `verifica-bot`
SENZA la regola "solo main". Fai la sezione C1–C2 e controlla che la regola `main` sia attiva
PRIMA di inserire i segreti (C3–C5).

## A. Token dell'abbonamento Claude (gratis, usa la tua quota)

1. Apri Terminal.app ed esegui `claude setup-token`.
2. Accedi nel browser che si apre. Il terminale stampa un token che inizia con `sk-ant-oat`.
   Copialo e tienilo da parte per il passo C3.

## B. GitHub App dedicata (l'identità che pubblica il check `verifica-bot`)

1. Su github.com: foto profilo → **Settings** → **Developer settings** → **GitHub Apps** → **New GitHub App**.
2. **GitHub App name**: `gas-verificatore`. Se è già preso, scegli un altro nome e dimmelo.
   **Homepage URL**: `https://github.com/Gasss23/Gas`.
3. **Webhook**: togli la spunta da **Active**.
4. **Repository permissions** (B2, G-1 verifica chat #130): **Pull requests → Read and write**
   (review COMMENT col verdetto), **Checks → Read and write** (il check run `verifica-bot`, che è
   il sì/no del bot), **Contents → Read-only**. Non toccare nient'altro (Metadata in sola
   lettura è automatico). Se l'App esiste già con i permessi vecchi: aggiungi **Checks → Read
   and write** e poi accetta i nuovi permessi nella pagina dell'installazione.
5. **Where can this GitHub App be installed?** → **Only on this account** → **Create GitHub App**.
6. Nella pagina dell'App copia il **Client ID** (serve al passo C4).
7. Scendi a **Private keys** → **Generate a private key**: si scarica un file `.pem`.
8. Menu a sinistra **Install App** → **Install** su Gasss23 → **Only select repositories** → `Gas` → **Install**.

## C. Environment `verifica-bot` (segreti leggibili solo da main)

1. Repo Gas → **Settings** → **Environments** → **New environment** → nome `verifica-bot` → **Configure environment**.
   Se esiste già (creato da una run), aprilo e controlla comunque il passo 2.
2. **Deployment branches and tags** → **Selected branches and tags** → **Add deployment branch or tag rule** → `main`.
3. **Environment secrets** → **Add environment secret**: nome `CLAUDE_CODE_OAUTH_TOKEN`, valore = token del passo A2.
4. **Environment variables** → **Add environment variable**: nome `GASBOT_CLIENT_ID`, valore = Client ID del passo B6.
5. **Environment secrets** → **Add environment secret**: nome `GASBOT_APP_KEY`, valore = tutto il contenuto del
   file `.pem` (aprilo con TextEdit, copia tutto comprese le righe `-----BEGIN` / `-----END`).
6. Cancella il `.pem` da Download (o spostalo nel tuo gestore di password).

## D. Etichetta `verifica` (la crei TU, a setup finito)

L'etichetta la crei tu, SOLO dopo aver finito A–C (repo → Issues → Labels → New label →
`verifica`, oppure `gh label create verifica`). L'agente non la crea: a fine fetta la mette
sulla PR (`gh pr edit N --add-label verifica`, fine-task §4quater) ed è il dosaggio della
quota. Finché l'etichetta non esiste quel comando fallisce e il bot non parte mai.

## E. Da NON cambiare

- Settings → Actions → General → **Allow GitHub Actions to create and approve pull requests** resta
  **SPENTO** (verificato 2026-10-05: `can_approve_pull_request_reviews=false`). Se fosse acceso, un
  workflow aggiunto da una PR potrebbe approvarsi da solo.

## F. Dopo il test di convalida (te lo dico io quando)

Ruleset `main-lock` → **Require status checks to pass** → aggiungi il check **`verifica-bot`**
scegliendo come sorgente l'App `gas-verificatore` (così il ruleset salva l'`integration_id`
dell'App: un check omonimo pubblicato da Actions o da un'altra App non conta). NON serve
"1 approvazione": il sì del bot è il check, non una review (G-1 #130; `gasmerge --auto`
controlla proprio questo e si blocca se il ruleset non lo richiede).

Cosa vuol dire ogni conclusione del check:
- **success** — il bot ha detto sì: mergeabile, anche con `gasmerge --auto`;
- **failure** — il bot ha detto NO: definitivo su quello SHA (G-2), serve un commit nuovo;
- **cancelled** — verifica non conclusa (head cambiata, verdetto o elenco file illeggibile,
  bot che non è riuscito a leggere diff e CI — R-196-1):
  si rilancia;
- **neutral** — la PR tocca la macchina del bot e il bot avrebbe detto sì: **decide
  l'operatore** (neutral non blocca il ruleset, `gasmerge --auto` invece vuole success e si
  ferma). Un NO sulla macchina del bot resta failure (R-163-1).

`gasmerge` manuale ora aspetta i check della PR (`gh pr checks --watch`), quindi eredita
anche `verifica-bot`: con il check richiesto, un failure del bot blocca anche il merge
manuale (R-163-3, voluto). Finché il bot non è provato non aggiungerlo al ruleset:
bloccherebbe ogni merge.
