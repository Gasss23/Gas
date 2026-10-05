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

## B. GitHub App dedicata (l'identità che approva)

1. Su github.com: foto profilo → **Settings** → **Developer settings** → **GitHub Apps** → **New GitHub App**.
2. **GitHub App name**: `gas-verificatore`. Se è già preso, scegli un altro nome e dimmelo.
   **Homepage URL**: `https://github.com/Gasss23/Gas`.
3. **Webhook**: togli la spunta da **Active**.
4. **Repository permissions**: **Pull requests → Read and write**, **Contents → Read-only**.
   Non toccare nient'altro (Metadata in sola lettura è automatico).
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

## D. Da NON cambiare

- Settings → Actions → General → **Allow GitHub Actions to create and approve pull requests** resta
  **SPENTO** (verificato 2026-10-05: `can_approve_pull_request_reviews=false`). Se fosse acceso, un
  workflow aggiunto da una PR potrebbe approvarsi da solo.

## E. Dopo il test di convalida (te lo dico io quando)

Ruleset `main-lock`: approvazioni richieste 1, "Dismiss stale approvals" acceso,
"Require approval of the most recent push" acceso. Ti darò i passi esatti in quel momento:
finché il bot non è provato, accenderli bloccherebbe ogni merge.
