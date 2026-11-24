"""Testi e voci per «ehi jarvis» italiano: positivi (varianti di pronuncia in IPA per piper,
testo per espeak), negativi avversari, divisione voci addestramento / valutazione.

Le frasi della simulazione del 23/11 (lib_sim.FRASI_IT, FRASI_TV, QUASI_OMOFONI) NON sono
usate in addestramento: i flussi della simulazione restano una prova su testi mai visti."""
from __future__ import annotations

import itertools
import random

# ── positivi ──────────────────────────────────────────────────────────────
# pronuncia italiana: «ehi/hei» = ˈei / ˈɛi (anche con h o j), «jarvis/giàrvis» = dʒˈaɾvis
# con r battuta/vibrante, a lunga, s finale a volte sonora o «sc».
FONEMI_POS_IT = [
    "ˈɛi dʒˈaɾvis", "ˈei dʒˈaɾvis", "ˈɛi dʒˈarvis", "ˈei dʒˈarvis", "ˈɛj dʒˈaːrvis",
    "ˈei dʒˈaːɾvis", "hˈɛi dʒˈaɾvis", "hˈei dʒˈarvis", "ˈɛi dʒˈaɾviz", "ˈei dʒˈarviz",
    "ˈei, dʒˈaɾvis", "ˈɛi, dʒˈarvis", "ˈɛi dʒˈarviʃ", "eˈi dʒˈaɾvis", "ˈɛːi dʒˈaɾvis",
    "ˈei dʒˈaɾvis!", "ˈɛi dʒˈaɾvis?", "ˈej dʒˈaɾvis", "ˈɛi dʒˈaɾvɪs", "ˈɛi dʒˈarvɪs",
]
# pronuncia inglese (l'operatore a volte dice «hey jarvis» all'inglese): ~15%
FONEMI_POS_EN = ["hˈeɪ dʒˈɑːɹvɪs", "hˈeɪ dʒˈɑːɹvɪs!", "hˈeɪ, dʒˈɑːɹvɪs", "hˈeɪ dʒˈɑːvɪs"]
TESTI_POS_ESPEAK = ["ehi jarvis", "ehi giarvis", "hei giàrvis", "ehi, jarvis", "ei jarvis",
                    "ehi giàrvis", "hey jarvis", "ehi jàrvis", "hei jarvis"]

# ── negativi avversari (testo italiano, fonemizzato con espeak «it») ─────────
PARZIALI = ["ehi", "hei", "jarvis", "giarvis", "giàrvis", "ehi ja", "ehi giar", "jarvis?",
            "jarvis!", "eh jar", "ehi ehi", "jarvis jarvis", "ehi tu", "hey", "jar"]
QUASI = [
    "ehi chiara", "hai visto", "servizi", "ehi mario", "ehi marta", "ehi davide", "ehi carlo",
    "ehi sara", "ehi giorgio", "ehi gigi", "ehi giulia", "ehi giovanna", "ehi gianluca",
    "ehi jacopo", "ehi jessica", "ehi giada", "ehi gervaso", "hai vinto", "hai finito",
    "hai capito", "ai servizi", "il servizio", "giardino", "giravite", "gelatina",
    "il garage", "ehi ragazzi", "ehi arturo", "ehi alvise", "ehi elvis", "ehi marco",
    "ehi alvaro", "ehi gabriele", "ehi gerardo", "chiamami jarvis", "dov'è jarvis",
    "il signor jarvis", "jarvis dopo", "fai vedere", "ai tavoli", "ehi garbo", "ehi giulio",
    "e io vado", "e invece", "ehi giacinto", "ehi bambini", "ehi tesoro", "ehi amore",
    "dai vieni", "hai visto marco", "e già", "ehi già", "ehi giusto", "ma davvero",
    "ehi dario", "ehi silvia", "ehi gianfranco", "ehi gino", "ehi guarda", "ehi senti",
    "ehi scusa", "ehi aspetta", "ehi ciao", "ehi siri", "ehi google", "ok google",
    "alexa", "ehi alexa", "ehi travis", "ehi harvey", "ehi jarno", "ehi charlie", "ehi davis",
    "hey jervis", "hey jarvi", "hey garvey", "ehi jargon", "ehi sergio", "ehi ivo",
]
SOGGETTI = ["io", "tu", "mio fratello", "la mia collega", "il cliente", "il tecnico",
            "mia madre", "luca", "la dottoressa", "il vicino", "noi", "voi", "loro",
            "il commercialista", "la banca", "il fornitore", "elena", "paolo", "stefano"]
VERBI = ["ha mandato", "deve controllare", "ha dimenticato", "vuole spostare", "ha chiesto",
         "ha già pagato", "sta preparando", "aspetta", "ha trovato", "non ha ricevuto",
         "porta", "cerca", "ha rotto", "ha venduto", "deve firmare", "ha scritto"]
OGGETTI = ["la fattura di marzo", "il contratto nuovo", "le chiavi del magazzino",
           "il preventivo del cliente", "la lista della spesa", "un messaggio vocale",
           "il pacco per milano", "la password del wifi", "i documenti della macchina",
           "la presentazione di domani", "il biglietto del treno", "la torta per stasera",
           "il report settimanale", "le foto delle vacanze", "il conto del ristorante",
           "la mail di ieri", "il modulo per l'assicurazione", "il caricatore del telefono"]
CODE = ["", " ieri sera", " stamattina", " entro venerdì", " per la riunione", " di nuovo",
        " prima di pranzo", " senza dirmi niente", " alle cinque", " dopo cena"]
FRASI_LIBERE = [
    "che bella giornata oggi", "non so se riesco a venire", "chiudi la finestra che c'è corrente",
    "quanto costa un caffè al bar", "accendi la radio per favore", "abbiamo finito il latte",
    "il computer è lentissimo oggi", "domani parto presto per roma", "ci pensi tu al pranzo",
    "ho dimenticato l'ombrello in ufficio", "la lavatrice ha finito", "andiamo in pizzeria stasera",
    "mi richiami tra cinque minuti", "il wifi non funziona più", "che cosa danno in tv",
    "devo rinnovare il passaporto", "il bambino dorme finalmente", "spegni la luce in corridoio",
    "il volo è stato cancellato", "ho prenotato il dentista per martedì", "va bene, ci vediamo dopo",
    "allora io vado, ciao", "sì sì, ho capito", "no, non è vero", "ma dai, non ci credo",
    "aspetta un attimo", "guarda che ore sono", "scusa, mi ripeti", "certo, nessun problema",
    "ehi, come va", "ehi, ci sei", "ehi, mi senti", "ehi, guarda qui", "ehi, sei pronto",
    "jarvis è il maggiordomo di iron man", "il film con jarvis l'ho visto due volte",
    "la serie su marvel la guardiamo dopo", "harvard è un'università famosa",
    "il garzone ha portato il pane", "gervasio arriva domani", "giovanni e silvia si sposano",
    "servizio clienti, buongiorno", "il servizio è incluso nel prezzo", "i servizi segreti",
]


def frasi_generate(n: int, seme: int) -> list[str]:
    rng = random.Random(seme)
    out = []
    for _ in range(n):
        out.append(f"{rng.choice(SOGGETTI)} {rng.choice(VERBI)} {rng.choice(OGGETTI)}"
                   f"{rng.choice(CODE)}")
    return out


def testi_negativi(seme: int, n_generate: int = 400) -> list[str]:
    try:   # escludi i testi della simulazione del 23/11 (restano solo per la valutazione)
        import lib_sim as L
        vietati = set(L.FRASI_IT + L.FRASI_TV + L.QUASI_OMOFONI)
    except ImportError:
        vietati = set()
    tutti = PARZIALI * 3 + QUASI * 3 + FRASI_LIBERE + frasi_generate(n_generate, seme)
    return [t for t in tutti if t not in vietati]


# ── voci: addestramento / valutazione (parlanti mai visti in addestramento) ──
# (modello piper, parlanti addestramento, parlanti valutazione, peso)
PIPER = [
    ("it_IT-paola-medium", [None], [], 0.16),
    ("it_IT-serena-medium", [None], [], 0.16),
    ("it_IT-riccardo-x_low", [], [None], 0.30),        # voce italiana maschile tenuta da parte
    ("en_US-libritts_r-medium", list(range(0, 800)), list(range(800, 904)), 0.33),
    ("en_GB-vctk-medium", list(range(0, 90)), list(range(90, 109)), 0.12),
    ("en_US-l2arctic-medium", list(range(0, 20)), list(range(20, 24)), 0.10),
    ("es_ES-sharvard-medium", [0], [1], 0.05),
    ("pt_BR-faber-medium", [None], [], 0.08),
]
ESPEAK_IT_TRAIN = ["it", "it+m1", "it+m2", "it+m4", "it+m5", "it+m6", "it+m7", "it+f1",
                   "it+f2", "it+f3", "it+f4", "it+f5", "it+klatt", "it+klatt2", "it+klatt3",
                   "it+Andy", "it+Mario", "it+Diogo", "it+edward", "it+steph"]
ESPEAK_IT_TEST = ["it+m3"]   # l'«operatore» della simulazione del 23/11


# ── seconda tornata di negativi (24/11): «ehi/hey + nome» ────────────────────
# Il primo modello scattava su «ehi gianni», «ehi charlie», «hey jervis» (frasi della
# simulazione, mai viste): servono molti più «ehi + nome» e parole che iniziano come «jar».
# Tolti di proposito i nomi delle frasi della simulazione (jervis, travis, charlie, marvin…),
# perché restino una prova su frasi mai viste.
NOMI_IT = ["gianna", "giovanni", "giuseppe", "gianmarco", "gianpiero", "giacomino", "gilda",
           "gisella", "giorgia", "giordano", "germano", "gemma", "geppetto", "ciro", "cesare",
           "cecilia", "chiara", "carla", "carlo", "carmela", "carmen", "cristina", "jari",
           "jolanda", "giampaolo", "gianfranco", "ginevra", "giovanna", "giusy", "giuliano",
           "jacopo", "jessica", "gerry", "giancarlo", "giuliana", "gennaro", "gerardo", "gelsomina",
           "ciccio", "cinzia", "sandro", "sara", "sergio", "silvio", "marisa", "marina", "mariano",
           "martino", "marcello", "mirko", "dario", "davide", "dalila", "fabio", "flavio",
           "franco", "ivan", "irene", "luigi", "mauro", "nadia", "piero", "rosa", "tiziana",
           "vanessa", "walter", "arianna", "armando", "alvaro", "elvira", "ervin", "jarno"]
NOMI_EN = ["jason", "jessie", "jared", "charles", "janet", "jamie", "jack", "garvey",
           "jarrod", "javier", "jarvie", "mervyn", "jasper",
           "jaden", "chase", "jeremy", "jerry", "james", "gary", "jovial", "jarring", "carlos", "jarvik"]
PAROLE_JA = ["giardino", "giara", "giallo", "giacca", "giarrettiera", "ciarlatano", "sciarpa",
             "jazz", "giaguaro", "giavellotto", "giapponese", "chiaro", "ciao", "garbo", "carbone",
             "jar", "jargon", "servizio", "salvis", "parvis", "harvard", "marvel"]


def testi_negativi_nomi(seme: int) -> list[str]:
    try:
        import lib_sim as L
        vietati = set(L.FRASI_IT + L.FRASI_TV + L.QUASI_OMOFONI)
    except ImportError:
        vietati = set()
    rng = random.Random(seme)
    out = []
    for n in NOMI_IT + PAROLE_JA:
        out += [f"ehi {n}", f"hei {n}", f"ehi, {n}", f"ei {n}"]
    for n in NOMI_EN + PAROLE_JA:
        out += [f"hey {n}", f"ehi {n}"]
    for _ in range(150):
        n = rng.choice(NOMI_IT + NOMI_EN)
        out.append(rng.choice([f"ehi {n}, vieni qui", f"ehi {n} come stai", f"hai visto {n}",
                               f"ehi {n}, sai chi è", f"dov'è {n}", f"ciao {n}"]))
    return [t for t in out if t not in vietati]


# «ehi + nome» MAI usati in addestramento (né qui né in QUASI/NOMI): prova pulita dei quasi-omofoni
QUASI_VALUTAZIONE = ["ehi gioele", "ehi giacinta", "ehi ciriaco", "ehi jenny", "hey jonas",
                     "ehi chantal", "ehi gilberto", "ehi gianmaria", "ehi ciriana", "ehi jader",
                     "hey jarrett", "hey jarek", "ehi giasone", "ehi carlotta", "ehi sabrina",
                     "ehi marzia", "ehi dalia", "hey jeffrey", "hey jordan", "ehi gerlando",
                     "ehi giarre", "ehi ciarli", "ehi barbara", "ehi alvin", "ehi sergino",
                     "ehi, hai visto gianni", "ehi garvis", "hey carvis",
                     "jarvis non c'è", "ehi, chi è jarvis"]
