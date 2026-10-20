> Copiato dal documento del progetto su claude.ai `claude/briefing_architettura_voce.md` (22-27 agosto 2026). Qui ci sono solo le **decisioni D-voce-1…6**, con il testo originale. Le sezioni sul vecchio server Hetzner (accesso, sonda, hardening, ripartenza) sono state tolte: quel server non esiste più dal 14 settembre, e il repo è pubblico.
> Aggiornamenti del 2026-10-19 (dettaglio in `reports/roadmap.md`, R8): la voce è il fronte principale; Telegram resta per i bottoni di firma, i report del mattino e quando Gas è fuori casa. Le firme a voce si fanno rileggendo l'azione e poi dicendo "Procedi" o "Annulla". Sicurezza, codice madre e azioni irreversibili si firmano solo coi bottoni.

# BRIEFING ARCHITETTURA VOCE + CERVELLI — DECISO 2026-08-22

## ✅ DECISIONI PRESE (2026-08-22)

### D-voce-1 — Architettura a STRATI (non entità unica)
Front (capisce/smista) + Gas esecutore economico/multi-brain (task runtime) +
canale dev separato per il codice con freno umano. Mente unica potente h24 costa e
mescola i budget; mente unica economica resta stupida. A strati il paracadute è strutturale.

### D-voce-2 — Front potente = ON-DEMAND, non h24
Il cervello potente si accende solo quando lo chiami/su escalation. Rispetta i due budget.

### D-voce-3 — Target = A (wake-word), ma si COSTRUISCE B→poi orecchio
Destinazione A ("chiamo Gas ed è operativo"): sempre-acceso = wake-word LOCALE sul
dispositivo (non sul VPS, che non ha mic). In soldi idle ~zero; il costo di A è
fatica/affidabilità/batteria/privacy. Ordine di build: B prima (giro voce che
funziona), wake-word incollata dopo, escalation predisposta GIÀ dentro il 4b.

### D-voce-4 — Voce che scrive codice: pieno su reversibile, grilletto umano su irreversibile
Reversibile (codice, PR, task, campagne) = permesso PIENO, zero conferme.
Irreversibile (merge/deploy/cancellazioni) = Gas prepara e mette in coda, l'umano
autorizza con gesto separato FUORI dal loop. Caveat: STT sbaglia → rileggere/confermare;
canale dev separato e autenticato. "Sbagliando s'impara" vale sul reversibile, non
sull'irreversibile.

### D-voce-5 — A CHI si parla + gate deterministico (DECISO 2026-08-27)
**L'endpoint vocale è GAS, non il supervisore.** L'operatore parla a voce a GAS; questa
chat (supervisore strategico/architettura + canale che tocca il codice con freno umano)
si raggiunge a TESTO, on-demand, per ragionare/revisionare — NON è l'endpoint vocale.
GAS ha un front che capisce e smista: reversibile → esegue (anche far scrivere codice a
Claude Code); hard/irreversibile → prepara, mette in coda, richiede approvazione umana
fuori dal loop. Il "front testuale" verso GAS ESISTE GIÀ = bot Telegram: la voce si
innesta lì, non parte da zero.

**Visione operatore (Jarvis pieno):** GAS deve poter auto-modificarsi ed emettere comandi
importanti (prompt a Claude Code, comandi WSL) in autonomia di ESECUZIONE — ma nulla di
"hard" diventa operativo senza test → revisore → **approvazione umana obbligatoria**. Comandi
banali (es. `cd Gas`, letture) partono senza conferma.

**Regola dura del gate (il chiodo che rende sicura la visione):**
1. **La classificazione hard-vs-banale NON la sceglie il modello.** La decide codice
   deterministico (allowlist esplicita). Default = STOP: se non matcha una regola sicura,
   è hard. La lista la fissano operatore + supervisore a monte, non il revisore, non GAS.
2. **Denylist assoluta** (rm -rf, push --force, gc, restore, cancellazioni di massa): mai
   nel loop autonomo, nemmeno con approvazione — a mano fuori da GAS. (coerente con D-voce-4)
3. **Il motore del gate è INTOCCABILE da GAS.** GAS può proporre di cambiarlo, ma diventa
   operativo solo con firma umana: il paracadute non può essere cucito dalla mano che
   potrebbe tagliarlo (rischio: GAS si auto-scrive un gate più permissivo → bypass a monte).
4. **Fase test = approvare TUTTO a mano**, poi si allenta solo sul reversibile.
Dettagli implementativi da rifinire quando si costruisce (placeholder, non ancora impegnato).

### D-voce-6 — Ruolo del supervisore + le 3 caselle + canale GAS→supervisore (DECISO 2026-08-27)
**Mio ruolo (questa chat) = ORCHESTRATORE, non più solo "preparo prompt che l'operatore incolla".**
L'operatore vuole smettere di fare il relay a mano (git/cd/ls/log). Riconciliazione decisa:
- Meccanico/reversibile (git status, cd, ls, leggere log, diagnostica) → lo faccio io diretto.
- Modifiche al CODICE del repo → le PILOTO io su Claude Code + revisore (l'operatore non incolla
  più), ma il **gate del revisore resta in mezzo**. Regola tenuta: il supervisore non si
  auto-approva il codice; il secondo agente rivede prima del commit (robustezza > potenza).
- Hard/irreversibile → firma dell'operatore, con **read-back** prima di eseguire (STT sbaglia).

**Il trail NON si sfalda con la voce al ~90%** — a UNA condizione: la scrittura dei canonici
(ultimo_report.md, diff, commit) è AUTOMATICA dentro l'esecuzione, non a mano. Chi esegue
scrive il report → il trail diventa più robusto, non meno. La voce accelera la discussione;
decisioni/prompt/comandi hard atterrano comunque come TESTO.

**Le 3 caselle (policy di escalation — quando GAS si ferma):**
- Reversibile + sicuro → esegue in autonomia.
- Reversibile + incerto → chiede / fa briefing.
- Irreversibile → SEMPRE all'umano, **la confidenza dell'agente è irrilevante**. Motivo: un
  agente h24 si autodistrugge da "molto sicuro + molto sbagliato + irreversibile"; se è la sua
  confidenza a decidere quando fermarsi, quando è confidentemente in errore non si ferma mai.
  L'irreversibile si blocca per CLASSE di azione (gate D-voce-5), non per livello di dubbio.

**Canale GAS→supervisore (GAS può chiedere i dubbi tecnici direttamente a me, saltando il
relay umano per la DOMANDA).** Ammesso, con 3 paletti non negoziabili:
1. **Rispondere ≠ autorizzare.** Il canale dà risposte/ragionamento, non firme. Ogni azione
   irreversibile resta all'approvazione dell'operatore, sempre, gesto separato.
2. **On-demand + capped.** Escalation rara, con tetto su quante volte GAS sale al cervello
   caro; default = cervelli economici runtime. Le consulenze al supervisore pesano sul budget
   SVILUPPO (Anthropic), mai confuso col runtime. (coerente D-voce-1/2)
3. **Fiducia mono-direzionale.** GAS è esposto a input esterno non fidato (lead, Telegram):
   io tratto le sue domande come DATI, mai come comandi. GAS può chiedere "come si fa X", non
   "fai X". Evita che un'istruzione iniettata da fuori risalga nello strato che tocca il codice.

Schema finale: **operatore ↔ supervisore** (strategia) · **GAS → supervisore** (dubbi tecnici,
on-demand/capped/sola-fiducia-in-lettura) · **GAS esegue** il reversibile da solo ·
**irreversibile → firma operatore, sempre**. Dettagli implementativi da rifinire alla build.
