# Setup G-3 — l'agente lavora con un token che NON amministra il repo

Oggi l'agente (Claude Code in locale) usa `gh` col TUO token: sei il proprietario del repo,
quindi può cambiare il ruleset `main-lock`, i workflow, l'environment `verifica-bot` e
mergiare. G-3 separa le due cose: il tuo token resta a te, l'agente ne usa uno senza
Administration. I token li crei TU: non incollarli mai in chat.

**Limite dichiarato:** GitHub non separa "pushare" da "mergiare": un token che può pushare
branch può anche mergiare una PR via API. Il freno al merge resta il ruleset (check richiesti,
più avanti `verifica-bot` dell'App); il token separato impedisce all'agente di **toccare il
ruleset e le impostazioni**, cioè di togliersi il freno da solo.

## A. Token fine-grained dell'agente

1. github.com → foto profilo → **Settings** → **Developer settings** → **Personal access tokens**
   → **Fine-grained tokens** → **Generate new token**.
2. **Token name**: `gas-agente`. **Expiration**: 90 giorni (lo rinnovi tu).
3. **Repository access** → **Only select repositories** → `Gasss23/Gas`.
4. **Repository permissions** — SOLO queste:
   - **Contents** → Read and write (push dei branch)
   - **Pull requests** → Read and write (aprire PR, etichetta `verifica`)
   - **Checks** → Read-only, **Actions** → Read-only, **Commit statuses** → Read-only (stato CI)
   - Metadata → Read-only (automatico)
   - **Administration: No access** · **Workflows: No access** · **Environments: No access** ·
     **Secrets: No access** · **Variables: No access**
5. **Generate token** → copialo.

## B. Usarlo per l'agente (sul Mac)

1. Salva il token fuori dal repo, es. nel Portachiavi o in `~/.config/gas/agente_token`
   con `chmod 600`.
2. Avvia Claude Code per Gas con quel token per `gh`, es.:
   `GH_TOKEN=$(cat ~/.config/gas/agente_token) claude`
   (`GH_TOKEN` ha la precedenza sul login di `gh`; il tuo login personale resta intatto
   per quando lavori tu.)
3. Controllo: nel repo, `bash scripts/avviso_token_admin.sh` deve stampare
   `G-3: il token gh in uso non amministra il repo — OK`.
   Con il tuo token stampa invece `AVVISO G-3: ... AMMINISTRA ...`.

## C. Cosa fa il codice (fase "solo avviso")

- `scripts/avviso_token_admin.sh` prova la capacità reale del token sull'endpoint delle deploy
  key (richiede Administration): 200 → avviso, 403/404 → OK, altro → "non verificabile".
  Non blocca mai.
- Lo chiamano `gasmerge` (all'avvio) e `fine_task_finale.sh` (prima del push).
- Fase successiva (decisione tua, quando il token A–B è in uso): trasformare l'avviso in un
  blocco per `gasmerge --auto`.

**Cosa NON copre il controllo:** prova solo il permesso Administration. Che Workflows,
Environments, Secrets e Variables siano davvero "No access" lo controlli tu alla creazione
del token (passo A.4). Un token con Administration in sola lettura dà comunque l'avviso
(errore dal lato prudente). L'"OK" vale solo per il TUO repo: il controllo esige anche che il
repo risolto da `gh` sia uno in cui il tuo utente ha ruolo admin (un token di un utente
diverso, o un repo sbagliato, dà "non verificabile").

## D. Da NON fare

- Non dare al token dell'agente Administration, Workflows o Environments "per comodità":
  è esattamente ciò che G-3 toglie.
- Non aggiungere il token dell'agente (né il suo utente) ai bypass del ruleset `main-lock`.
