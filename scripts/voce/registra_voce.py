#!/usr/bin/env python3
"""
scripts/voce/registra_voce.py — registra la tua voce e addestra la verifica di «Hey Jarvis».

Passo 1 di reports/proposta_verifica_parlante.md. Il modello pronto «hey_jarvis» dà alla
voce dell'operatore solo 0,37-0,43 (misura del 17/11 sul Mac): con la soglia 0,7 quasi
tutte le chiamate si perdono, e abbassarla da sola fa rispondere a TV e persone. Questo
script registra:
  a) 15 «Hey Jarvis» da posti diversi (vicino al Mac, a 3 metri, dall'altra stanza,
     camminando, voce bassa e normale), uno per bip;
  b) 60 s di parlato normale SENZA la parola (e, se vuoi, 60 s di TV accesa);
  c) da solo, senza microfono: «Hey Jarvis» e parole simili dette dalle voci di sistema
     del Mac (comando `say`, in locale): sono gli esempi di «altre persone» che insegnano
     al filtro a scartare chi non è registrato (prova del 17/11: senza di loro il filtro
     accettava qualunque voce);
poi addestra il «custom verifier» di openWakeWord: un piccolo filtro che, quando il modello
della parola sente qualcosa (da 0,25 in su), decide se è una persona registrata che dice
«Hey Jarvis». L'ascolto lo usa da solo al prossimo avvio (clients/voice/ascolto.py).

Uso (sul Mac, dalla cartella di Gas, con l'ascolto IN PAUSA: altrimenti Jarvis risponde a
ogni prova):
    bash scripts/voce/pausa.sh
    .venv/bin/python scripts/voce/registra_voce.py                  # registra e addestra
    .venv/bin/python scripts/voce/registra_voce.py --persona giulia  # un'altra persona
    .venv/bin/python scripts/voce/registra_voce.py --solo-addestra   # riaddestra e basta
    bash scripts/voce/riprendi.sh                                    # l'ascolto la carica

File (tutti in .gas_voce/, fuori da git, cartelle leggibili solo da te: la voce è un dato
biometrico):
    .gas_voce/verifica/<persona>/positivi/*.wav     i «Hey Jarvis»
    .gas_voce/verifica/<persona>/negativi/*.wav     parlato e TV senza la parola
    .gas_voce/verifica/_altre_voci/negativi/*.wav   le voci del Mac (rigenerate se mancano)
    .gas_voce/verifica/hey_jarvis_verifier.pkl      il filtro addestrato (+ .json di riepilogo)
Più persone: il filtro le impara TUTTE insieme («una delle persone registrate dice la
parola»), non distingue chi delle due. Ogni nuova registrazione si aggiunge alle precedenti
(riaddestra tutto); per togliere una persona cancella la sua cartella e usa --solo-addestra.

Exit 0 = filtro addestrato e salvato; 1 = errore (messaggio in italiano, niente traceback).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import pickle
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, List, Optional, Sequence, Tuple

RADICE = Path(__file__).resolve().parents[2]
if str(RADICE) not in sys.path:
    sys.path.insert(0, str(RADICE))
from clients.voice import ascolto as a  # noqa: E402 — solo libreria standard all'import

PERSONA_PREDEFINITA = "operatore"
MODELLO_PREDEFINITO = "hey_jarvis"
_PERSONA = re.compile(r"[a-z0-9][a-z0-9_-]{0,31}")
ALTRE_VOCI = "_altre_voci"    # cartella degli esempi «altre persone» (non è una persona)
SEC_CLIP = 3.0                # durata di un «Hey Jarvis» registrato (la parola è ~1 s)
SEC_FRA_CLIP = 1.5            # pausa dopo ogni clip, prima del bip successivo
# 20/11: dall'altra stanza il bip non si sente e 3 s non bastavano: le clip «lontane»
# erano solo rumori (lavastoviglie, pentole) salvate come «Hey Jarvis». Da lontano si
# ascolta più a lungo, e ogni clip si tiene solo se il modello della parola la riconosce.
SEC_CLIP_LONTANO = 6.0        # finestra per i gruppi con attesa lunga (lontano dal Mac)
ATTESA_LONTANO_S = 6.0        # da quest'attesa in su il gruppo è «lontano»
SEC_DOPO_PICCO = 0.5          # la clip tenuta finisce poco dopo il picco del punteggio
TENTATIVI_PAROLA = 3          # prove per clip prima di saltarla
SEC_PICCO_MINIMO = 0.5        # picco prima di così: la parola è iniziata prima della finestra
# un ciclo vero dura più di finestra + pausa (bip, analisi, svuotamento): margine per
# il messaggio «dillo ogni N secondi» quando il bip non si sente (R-810M1-2)
MARGINE_CICLO_S = 1.0
SEC_NEGATIVI = 60.0
# (dove e come, quante volte, secondi per mettersi in posizione dopo Invio): 15 in tutto
GRUPPI: Tuple[Tuple[str, int, float], ...] = (
    ("vicino al Mac (mezzo metro), voce normale", 3, 2.0),
    ("vicino al Mac, voce bassa", 2, 2.0),
    ("a circa 3 metri dal Mac, voce normale", 3, 6.0),
    ("dall'altra stanza (porta aperta), voce normale o un po' più forte", 3, 12.0),
    ("camminando per la stanza, voce normale", 2, 5.0),
    ("di spalle al Mac o come ti viene di solito (anche veloce o stanco)", 2, 5.0),
)
MIN_POSITIVI = 3              # «Hey Jarvis» utili sotto cui il filtro non si addestra
RIPETIZIONI_POSITIVI = 5      # come openWakeWord: ogni clip 5 volte, spostata di poco
IMBOTTITURA_PRIMA_S = 1.0     # silenzio prima della clip: il modello è muto nei primi 5 blocchi
IMBOTTITURA_DOPO_S = 0.5      # e dopo: il punteggio sale a fine parola
# Voci di sistema del Mac per gli esempi «altre persone»: frasi che fanno salire il modello
# della parola (la parola stessa e i quasi-omofoni della misura del 12/11), due velocità.
TESTI_ALTRE_VOCI = ("Hey Jarvis", "Ehi Jarvis", "Hey Chavez", "Hey Jasmine")
VELOCITA_ALTRE_VOCI = (160, 210)
MAX_ALTRE_VOCI = 12
_LINGUE_ALTRE_VOCI = ("it_", "en_", "es_", "fr_", "de_")
# voci «effetto» di macOS: non sono voci di persone
_VOCI_EFFETTO = {"albert", "bad news", "bahh", "bells", "boing", "bubbles", "cellos",
                 "deranged", "good news", "hysterical", "jester", "organ", "pipe organ",
                 "superstar", "trinoids", "whisper", "wobble", "zarvox"}


class Errore(Exception):
    """Errore da dire all'operatore in italiano, senza traceback."""


# ─────────────────────────────────────────── file ──

def cartella(radice: Path = RADICE) -> Path:
    return radice / a.CARTELLA_VERIFICA


def _privata(p: Path, radice: Path) -> Path:
    """Crea la cartella; lei e le sue madri fino a .gas_voce/verifica compresa diventano
    leggibili solo da te (la voce è un dato biometrico)."""
    p.mkdir(parents=True, exist_ok=True)
    base = cartella(radice)
    q = p
    while True:
        os.chmod(q, 0o700)
        if q == base or base not in q.parents:
            break
        q = q.parent
    return p


def _scrivi_privato(p: Path, dati: bytes) -> None:
    """Scrittura atomica, file 0600 (file temporaneo nella stessa cartella e rename)."""
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix=".tmp_", suffix=p.suffix)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(dati)
        os.chmod(tmp, 0o600)
        os.replace(tmp, p)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def persone(radice: Path = RADICE) -> List[str]:
    """Le persone con almeno un «Hey Jarvis» registrato."""
    c = cartella(radice)
    if not c.is_dir():
        return []
    return sorted(d.name for d in c.iterdir() if d.is_dir() and _PERSONA.fullmatch(d.name)
                  and any((d / "positivi").glob("*.wav")))


def clip(radice: Path, tipo: str) -> List[Path]:
    """Le clip `tipo` («positivi» o «negativi») di tutte le persone (e, per i negativi,
    delle altre voci)."""
    c = cartella(radice)
    if not c.is_dir():
        return []
    cartelle = [d for d in c.iterdir() if d.is_dir()
                and (_PERSONA.fullmatch(d.name) or (d.name == ALTRE_VOCI and tipo == "negativi"))]
    return sorted(p for d in cartelle for p in (d / tipo).glob("*.wav"))


def _di_altre_voci(p: Path) -> bool:
    return p.parent.parent.name == ALTRE_VOCI


# ─────────────────────────────────────────── altre voci (say del Mac) ──

def voci_del_mac(elenco: str) -> List[str]:
    """Dalle righe di `say -v ?` («Alice   it_IT   # Ciao…», anche con nomi tra parentesi)
    le voci di persone delle lingue utili, prima le italiane, al massimo MAX_ALTRE_VOCI."""
    voci: List[Tuple[int, str]] = []
    for riga in elenco.splitlines():
        m = re.match(r"^(.+?)\s+([a-z]{2,3}_[A-Z0-9]{2,3})\s+#", riga)
        if not m:
            continue
        nome, lingua = m.group(1).strip(), m.group(2)
        if nome.lower() in _VOCI_EFFETTO or not lingua.startswith(_LINGUE_ALTRE_VOCI):
            continue
        voci.append((0 if lingua.startswith("it_") else 1, nome))
    visti: List[str] = []
    for _, nome in sorted(voci, key=lambda x: x[0]):
        if nome not in visti:
            visti.append(nome)
    return visti[:MAX_ALTRE_VOCI]


def genera_altre_voci(radice: Path, esegui: Callable[..., Any] = subprocess.run,
                      say: Optional[str] = None) -> int:
    """Genera con `say` (in locale, niente rete) le clip delle altre voci, 16 kHz mono 16
    bit. Fail-safe: senza `say` (non è un Mac) o con una voce che non va, salta e basta.
    Restituisce quante clip ha salvato."""
    say = say or shutil.which("say")
    if not say:
        return 0
    try:
        elenco = esegui([say, "-v", "?"], capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return 0
    d = _privata(cartella(radice) / ALTRE_VOCI / "negativi", radice)
    n = 0
    for i, voce in enumerate(voci_del_mac(elenco or "")):
        for j, testo in enumerate(TESTI_ALTRE_VOCI):
            for vel in VELOCITA_ALTRE_VOCI:
                p = d / ("voce%02d_%d_%d.wav" % (i, j, vel))
                try:
                    r = esegui([say, "-v", voce, "-r", str(vel), "-o", str(p),
                                "--file-format=WAVE", "--data-format=LEI16@16000", testo],
                               capture_output=True, text=True, timeout=30)
                    if getattr(r, "returncode", 1) == 0 and p.exists():
                        os.chmod(p, 0o600)
                        n += 1
                except Exception:
                    continue
    return n


# ─────────────────────────────────────────── registrazione ──

@dataclass
class Registratore:
    """Registrazione guidata, con microfono, bip, input e attese iniettati (test)."""
    mic: Any
    radice: Path
    persona: str
    chiedi: Callable[[str], str] = input
    dorme: Callable[[float], None] = time.sleep
    bip: Callable[[str], None] = a.bip_di_sistema
    stampa: Callable[[str], None] = print
    # (punteggio massimo del modello della parola, indice del blocco) per una clip appena
    # registrata; None = nessun controllo (solo il volume, come prima)
    misura: Optional[Callable[[List[Any]], Tuple[float, int]]] = None
    soglia_parola: float = a.SOGLIA_BASE_PREDEFINITA
    salvati: List[Path] = field(default_factory=list)
    sentito_suono: bool = False   # almeno una finestra con un suono (microfono vivo)

    def _blocchi(self, secondi: float) -> List[Any]:
        self.mic.svuota()   # niente audio vecchio (né il bip appena suonato)
        n = a.blocchi_per(secondi)
        out: List[Any] = []
        for b in self.mic.blocchi():
            out.append([int(c) for c in b])
            if len(out) >= n:
                break
        return out

    def _salva(self, tipo: str, nome: str, blocchi: List[Any]) -> Path:
        d = _privata(cartella(self.radice) / self.persona / tipo, self.radice)
        p = d / nome
        _scrivi_privato(p, a.in_wav(blocchi))
        self.salvati.append(p)
        return p

    def positivi(self, gruppi: Sequence[Tuple[str, int, float]] = GRUPPI) -> int:
        quando = time.strftime("%Y%m%d-%H%M%S")
        n = 0
        totale = sum(g[1] for g in gruppi)
        for dove, quante, attesa in gruppi:
            lontano = attesa >= ATTESA_LONTANO_S
            finestra = SEC_CLIP_LONTANO if lontano else SEC_CLIP
            self.chiedi("\n→ %s: %d volt%s. Premi Invio, poi hai %g s per metterti lì; a "
                        "ogni bip di' «Hey Jarvis» una volta, come lo diresti di solito.%s "
                        % (dove, quante, "a" if quante == 1 else "e", attesa,
                           " Se da lì non senti il bip, dillo ogni %d secondi circa."
                           % math.ceil(finestra + SEC_FRA_CLIP + MARGINE_CICLO_S)
                           if lontano else ""))
            self.dorme(attesa)
            for _ in range(quante):
                for _prova in range(TENTATIVI_PAROLA):
                    self.bip("ok")
                    clip_ok = self._una_clip(finestra)
                    self.dorme(SEC_FRA_CLIP)
                    if clip_ok is None:
                        if not self.sentito_suono and _prova == TENTATIVI_PAROLA - 1:
                            # V-1 bot #390: microfono muto senza errore (permesso negato):
                            # fermarsi subito invece di 15 × 3 bip a vuoto
                            raise Errore(
                                "il microfono non dà nessun suono: controlla il permesso "
                                "del microfono per il Terminale (Impostazioni di Sistema → "
                                "Privacy e sicurezza → Microfono) e il microfono scelto")
                        continue
                    n += 1
                    self._salva("positivi", "hey_jarvis_%s_%02d.wav" % (quando, n), clip_ok)
                    self.stampa("   ✓ %d di %d" % (n, totale))
                    break
                else:
                    self.stampa("   (dopo %d prove la salto)" % TENTATIVI_PAROLA)
        return n

    def _una_clip(self, finestra: float) -> Optional[List[Any]]:
        """Registra una finestra e tiene SOLO un «Hey Jarvis» vero: senza voce, o se il
        modello della parola non lo riconosce (rumori, parole diverse), None e lo dice. Da
        una finestra lunga tiene i SEC_CLIP secondi che finiscono poco dopo il picco."""
        blocchi = self._blocchi(finestra)
        picco = max((a.rms(b) for b in blocchi), default=0.0)
        if picco < a.VOCE_RMS_PREDEFINITO / 2:
            self.stampa("   (non ti ho sentito: rifallo)")
            return None
        self.sentito_suono = True
        if self.misura is None:
            return blocchi
        punteggio, i = self.misura(blocchi)
        if punteggio < self.soglia_parola:
            self.stampa("   (non ho riconosciuto «Hey Jarvis», punteggio %.2f: rifallo)"
                        % punteggio)
            return None
        if i < a.blocchi_per(SEC_PICCO_MINIMO):   # R-810M1-1: parola tagliata all'inizio
            self.stampa("   («Hey Jarvis» tagliato all'inizio: rifallo dopo il bip)")
            return None
        fine = min(len(blocchi), i + 1 + a.blocchi_per(SEC_DOPO_PICCO))
        inizio = max(0, fine - a.blocchi_per(SEC_CLIP))
        return blocchi[inizio:fine]

    def negativi(self, secondi: float, tv: bool) -> int:
        quando = time.strftime("%Y%m%d-%H%M%S")
        prese = [("parlato", "Ora parla normalmente per %g s SENZA dire «Hey Jarvis»: leggi "
                  "un articolo ad alta voce o racconta la giornata, anche muovendoti. Invio "
                  "per iniziare (bip all'inizio e alla fine). " % secondi)]
        if tv:
            risposta = self.chiedi("\nVuoi registrare anche %g s di TV (o un video con gente "
                                   "che parla) a volume normale, senza parlare tu? [s/N] "
                                   % secondi)
            if risposta.strip().lower() in ("s", "si", "sì", "y", "yes"):
                prese.append(("tv", "Accendi la TV o il video. Invio per iniziare. "))
        n = 0
        for nome, invito in prese:
            self.chiedi("\n→ " + invito)
            self.bip("ok")
            blocchi = self._blocchi(secondi)
            self.bip("ok")
            self._salva("negativi", "%s_%s.wav" % (nome, quando), blocchi)
            self.stampa("   ✓ %s: %g s salvati" % (nome, secondi))
            n += 1
        return n


# ─────────────────────────────────────────── addestramento ──

class MotoreOWW:
    """Il modello vero di openWakeWord (onnx, come l'ascolto) e il verificatore di
    openwakeword.custom_verifier_model. Le caratteristiche si estraggono come
    `get_reference_clip_features` della libreria, ma con la soglia base dell'ascolto (la
    libreria, in `train_custom_verifier`, usa 0,5 fisso: con la voce dell'operatore, che
    sta a 0,37-0,43, non resterebbe nessun esempio) e tenendo anche il punteggio del
    modello, per il riepilogo. Il classificatore è quello della libreria
    (`train_verifier_model`), così il file si carica con `Model(custom_verifier_models=…)`."""

    def __init__(self, modello: str) -> None:
        import numpy as np
        from scipy.io import wavfile
        from openwakeword.model import Model
        from openwakeword import custom_verifier_model as cvm
        self.np, self._wavfile, self._cvm = np, wavfile, cvm
        self.nome = modello
        self.oww = Model(wakeword_models=[modello], inference_framework="onnx")
        self._caso = np.random.default_rng(0)

    def blocchi(self, wav: Path, ripetizioni: int, imbottitura: bool
                ) -> List[Tuple[float, Any]]:
        """(punteggio del modello, caratteristiche) per ogni blocco da 80 ms della clip."""
        np = self.np
        try:
            freq, dati = self._wavfile.read(str(wav))
        except Exception as e:
            raise Errore("%s illeggibile (%s)" % (wav.name, type(e).__name__))
        if freq != a.FREQ or dati.dtype != np.int16 or dati.ndim != 1:
            raise Errore("%s non è un WAV 16 kHz mono 16 bit" % wav.name)
        if imbottitura:
            dati = np.concatenate([np.zeros(int(IMBOTTITURA_PRIMA_S * a.FREQ), np.int16), dati,
                                   np.zeros(int(IMBOTTITURA_DOPO_S * a.FREQ), np.int16)])
        out: List[Tuple[float, Any]] = []
        for _ in range(ripetizioni):
            self.oww.reset()
            d = dati[int(self._caso.integers(0, a.BLOCCO)):] if ripetizioni > 1 else dati
            for i in range(0, d.shape[0] - a.BLOCCO, a.BLOCCO):
                p = float(self.oww.predict(d[i:i + a.BLOCCO])[self.nome])
                f = self.oww.preprocessor.get_features(self.oww.model_inputs[self.nome])
                out.append((p, f))
        return out

    def misura(self, blocchi: List[Any]) -> Tuple[float, int]:
        """(punteggio massimo del modello della parola, indice del blocco) su una clip
        appena registrata, con il silenzio davanti come in `blocchi` (il modello è muto nei
        primi blocchi)."""
        np = self.np
        self.oww.reset()
        for _ in range(a.blocchi_per(IMBOTTITURA_PRIMA_S)):
            self.oww.predict(np.zeros(a.BLOCCO, np.int16))
        migliore, indice = 0.0, 0
        for i, b in enumerate(blocchi):
            p = float(self.oww.predict(np.asarray(b, dtype=np.int16))[self.nome])
            if p > migliore:
                migliore, indice = p, i
        return migliore, indice

    def addestra(self, positivi: List[Any], negativi: List[Any]) -> Any:
        np = self.np
        x = np.vstack(positivi + negativi)
        y = np.array([1] * len(positivi) + [0] * len(negativi))
        return self._cvm.train_verifier_model(x, y)

    def probabilita(self, verificatore: Any, caratteristiche: List[Any]) -> List[float]:
        if not caratteristiche:
            return []
        return [float(p) for p in
                verificatore.predict_proba(self.np.vstack(caratteristiche))[:, -1]]


@dataclass
class Riepilogo:
    persone: List[str]
    usati: List[Tuple[str, float]]          # (clip, punteggio max del modello)
    scartati: List[Tuple[str, float]]       # sotto la soglia base: fuori dall'addestramento
    illeggibili: List[str]
    negativi: int                            # file di parlato/TV
    blocchi_negativi: int
    riconosciuti: int                        # «Hey Jarvis» usati che il filtro accetta
    falsi: int                               # blocchi di parlato/TV che passerebbero
    blocchi_al_filtro: int                   # blocchi di parlato/TV che arrivano al filtro
    altre_voci: int                          # clip delle altre voci che arrivano al filtro
    altre_accettate: int                     # … e che il filtro accetta (deve stare a ~0)
    percorso: Path


def addestra(radice: Path, modello: str, soglia_base: float, soglia_verifica: float,
             motore: Any) -> Riepilogo:
    """Addestra il filtro su TUTTE le persone registrate (più le altre voci come esempi da
    scartare) e lo salva (0600, scrittura atomica) in .gas_voce/verifica/
    <modello>_verifier.pkl, con un .json di riepilogo."""
    uscita = a.percorso_verificatore(modello, radice)
    if uscita is None:
        raise Errore("nome del modello non ammesso per la verifica: %r" % modello)
    pos_file, neg_file = clip(radice, "positivi"), clip(radice, "negativi")
    if not pos_file:
        raise Errore("nessun «Hey Jarvis» registrato in %s: lancia lo script senza "
                     "--solo-addestra" % cartella(radice).relative_to(radice))
    if not [p for p in neg_file if not _di_altre_voci(p)]:
        raise Errore("manca il parlato senza la parola (cartelle negativi/): serve per "
                     "addestrare. Lancia lo script senza --solo-addestra")
    illeggibili: List[str] = []

    def leggi(p: Path, ripetizioni: int, imbottitura: bool) -> Optional[List[Tuple[float, Any]]]:
        try:
            return motore.blocchi(p, ripetizioni, imbottitura)
        except Errore as e:  # una clip rovinata non ferma l'addestramento
            illeggibili.append(str(e))
            return None

    pos_caratt: List[Any] = []
    pos_per_clip: List[List[Any]] = []
    usati: List[Tuple[str, float]] = []
    scartati: List[Tuple[str, float]] = []
    for p in pos_file:
        blocchi = leggi(p, RIPETIZIONI_POSITIVI, True)
        if blocchi is None:
            continue
        picco = max((s for s, _ in blocchi), default=0.0)
        buoni = [f for s, f in blocchi if s >= soglia_base]
        nome = "%s/%s" % (p.parent.parent.name, p.name)
        if buoni:
            usati.append((nome, picco))
            pos_caratt.extend(buoni)
            pos_per_clip.append(buoni)
        else:
            scartati.append((nome, picco))
    if len(usati) < MIN_POSITIVI:
        raise Errore("solo %d «Hey Jarvis» arrivano a %.2f (ne servono almeno %d): "
                     "registra di nuovo, un po' più vicino al Mac"
                     % (len(usati), soglia_base, MIN_POSITIVI))
    neg_caratt: List[Any] = []
    al_filtro: List[Any] = []                 # parlato/TV che arriva al filtro
    altre_per_clip: List[List[Any]] = []      # altre voci che arrivano al filtro
    n_neg = 0
    for p in neg_file:
        blocchi = leggi(p, 1, _di_altre_voci(p))
        if blocchi is None:
            continue
        neg_caratt.extend(f for _, f in blocchi)
        sopra = [f for s, f in blocchi if s >= soglia_base]
        if _di_altre_voci(p):
            if sopra:
                altre_per_clip.append(sopra)
        else:
            n_neg += 1
            al_filtro.extend(sopra)
    if not n_neg:
        raise Errore("il parlato registrato non si legge: registralo di nuovo")
    verificatore = motore.addestra(pos_caratt, neg_caratt)
    # Prova sui dati stessi (ottimista: sono gli esempi dell'addestramento)
    riconosciuti = sum(1 for c in pos_per_clip
                       if max(motore.probabilita(verificatore, c)) >= soglia_verifica)
    falsi = sum(1 for q in motore.probabilita(verificatore, al_filtro) if q >= soglia_verifica)
    altre_accettate = sum(1 for c in altre_per_clip
                          if max(motore.probabilita(verificatore, c)) >= soglia_verifica)
    _privata(uscita.parent, radice)
    _scrivi_privato(uscita, pickle.dumps(verificatore))
    chi = persone(radice)
    _scrivi_privato(uscita.with_suffix(".json"), json.dumps({
        "modello": modello, "persone": chi, "positivi_usati": len(usati),
        "positivi_scartati": len(scartati), "negativi": n_neg,
        "altre_voci": len(altre_per_clip), "soglia_base": soglia_base,
        "addestrato": time.strftime("%Y-%m-%d %H:%M:%S"),
    }, ensure_ascii=False, indent=1).encode("utf-8"))
    return Riepilogo(chi, usati, scartati, illeggibili, n_neg, len(neg_caratt), riconosciuti,
                     falsi, len(al_filtro), len(altre_per_clip), altre_accettate, uscita)


def descrivi(r: Riepilogo, radice: Path, soglia_base: float, soglia_verifica: float
             ) -> List[str]:
    punteggi = [s for _, s in r.usati]
    righe = ["",
             "Verifica della voce addestrata: %d person%s (%s)."
             % (len(r.persone), "a" if len(r.persone) == 1 else "e", ", ".join(r.persone)),
             "  «Hey Jarvis» usati: %d su %d (punteggio del modello della parola: min %.2f, "
             "mediana %.2f, max %.2f)" % (len(r.usati), len(r.usati) + len(r.scartati),
                                          min(punteggi), statistics.median(punteggi),
                                          max(punteggi))]
    for nome, s in r.scartati:
        righe.append("  scartato (sotto %.2f, max %.2f): %s" % (soglia_base, s, nome))
    for motivo in r.illeggibili:
        righe.append("  saltato: %s" % motivo)
    righe += ["  parlato e TV senza la parola: %d file" % r.negativi,
              "  prova sulle registrazioni stesse (ottimista), soglia %.2f:" % soglia_verifica,
              "    tuoi «Hey Jarvis» accettati: %d su %d" % (r.riconosciuti, len(r.usati)),
              "    blocchi di parlato/TV scambiati per la parola: %d su %d arrivati al filtro"
              % (r.falsi, r.blocchi_al_filtro)]
    if r.altre_voci:
        righe.append("    altre voci (Mac) accettate: %d su %d (meglio se 0)"
                     % (r.altre_accettate, r.altre_voci))
    else:
        righe.append("    altre voci: nessuna (comando `say` del Mac non disponibile): il "
                     "filtro distingue poco le altre persone")
    righe += ["File: %s" % r.percorso.relative_to(radice),
              "Per usarla: bash scripts/voce/riprendi.sh (o installa.sh); nel log "
              "dell'ascolto deve comparire «verifica della voce: attiva»."]
    if r.riconosciuti < len(r.usati):
        righe.append("Attenzione: non tutte le tue chiamate passano il filtro: registra "
                     "altri «Hey Jarvis» (si aggiungono) o abbassa "
                     "GAS_ASCOLTO_SOGLIA_VERIFICA nel .env.")
    return righe


# ─────────────────────────────────────────── main ──

def messaggio_modulo(e: ModuleNotFoundError, script: str) -> str:
    """Il messaggio per un modulo mancante: quasi sempre lo script è stato lanciato col
    python3 di sistema invece che con quello di Gas (taratura del 17/11)."""
    return ("✗ manca il modulo «%s»: lancia lo script col Python di Gas, dalla cartella di "
            "Gas: .venv/bin/python scripts/voce/%s (se .venv non c'è: bash "
            "scripts/voce/installa.sh)" % (e.name or "?", script))


def main(argv: Optional[List[str]] = None, *,
         microfono: Optional[Callable[[], Any]] = None,
         motore: Optional[Callable[[str], Any]] = None,
         altre_voci: Callable[[Path], int] = genera_altre_voci,
         radice: Path = RADICE,
         chiedi: Callable[[str], str] = input,
         dorme: Callable[[float], None] = time.sleep,
         bip: Optional[Callable[[str], None]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Registra la tua voce e addestra la verifica di «Hey Jarvis».")
    ap.add_argument("--persona", default=PERSONA_PREDEFINITA,
                    help="chi registra (default operatore); un nome nuovo aggiunge una persona")
    ap.add_argument("--solo-addestra", action="store_true",
                    help="niente registrazione: riaddestra dalle clip già salvate")
    ap.add_argument("--senza-tv", action="store_true",
                    help="non chiedere la registrazione della TV")
    ap.add_argument("--secondi-negativi", type=float, default=SEC_NEGATIVI)
    ap.add_argument("--modello", default=MODELLO_PREDEFINITO)
    args = ap.parse_args(argv)
    persona = args.persona.strip().lower()
    if not _PERSONA.fullmatch(persona):
        print("✗ --persona: solo lettere minuscole, cifre, «-» e «_» (al massimo 32, "
              "senza «_» all'inizio)", file=sys.stderr)
        return 1
    if a.percorso_verificatore(args.modello, radice) is None:
        print("✗ --modello: solo il nome di un modello pronto (es. hey_jarvis)", file=sys.stderr)
        return 1
    a._carica_dotenv(radice)   # le stesse soglie dell'ascolto (GAS_ASCOLTO_SOGLIA_BASE…)
    soglia_base = a._numero("GAS_ASCOLTO_SOGLIA_BASE", a.SOGLIA_BASE_PREDEFINITA, 0.05, 0.9)
    soglia_verifica = max(a._numero("GAS_ASCOLTO_SOGLIA_VERIFICA",
                                    a.SOGLIA_VERIFICA_PREDEFINITA, 0.05, 0.99), soglia_base)
    mic = None
    try:
        # prima il modello: se manca, l'operatore lo sa PRIMA di registrare per 5 minuti
        try:
            m = (motore or MotoreOWW)(args.modello)
        except (ModuleNotFoundError, Errore):
            raise
        except Exception as e:
            raise Errore("modello «%s» di openWakeWord non pronto (%s): esegui "
                         "bash scripts/voce/installa.sh" % (args.modello, type(e).__name__))
        if not args.solo_addestra:
            try:
                mic = (microfono or a.Microfono)()
            except ModuleNotFoundError:
                raise
            except Exception as e:
                raise Errore("microfono non disponibile (%s): controlla il permesso del "
                             "microfono per il Terminale (Impostazioni di Sistema → Privacy e "
                             "sicurezza → Microfono)" % type(e).__name__)
            print("Registrazione della voce di «%s». Prima metti in pausa l'ascolto "
                  "(bash scripts/voce/pausa.sh), altrimenti Jarvis risponde a ogni prova. "
                  "L'audio resta solo sul Mac, in %s." % (persona, a.CARTELLA_VERIFICA))
            reg = Registratore(mic, radice, persona, chiedi=chiedi, dorme=dorme,
                               bip=bip or a.bip_di_sistema,
                               misura=getattr(m, "misura", None), soglia_parola=soglia_base)
            if reg.positivi() < 1:
                raise Errore("nessun «Hey Jarvis» sentito: controlla il microfono e riprova")
            reg.negativi(max(args.secondi_negativi, 5.0), tv=not args.senza_tv)
            mic.chiudi()
            mic = None
        if not any((cartella(radice) / ALTRE_VOCI / "negativi").glob("*.wav")):
            print("\nPreparo gli esempi di altre voci con le voci del Mac…", flush=True)
            print("  %d clip" % altre_voci(radice))
        print("\nAddestro il filtro (qualche decina di secondi)…", flush=True)
        r = addestra(radice, args.modello, soglia_base, soglia_verifica, m)
    except ModuleNotFoundError as e:
        print(messaggio_modulo(e, "registra_voce.py"), file=sys.stderr)
        return 1
    except Errore as e:
        print("✗ %s" % e, file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrotto: le clip già salvate restano. Per addestrare con quelle: "
              "--solo-addestra", file=sys.stderr)
        return 1
    except Exception as e:  # §9: niente traceback per l'operatore
        print("✗ errore inatteso (%s): %s" % (type(e).__name__, e), file=sys.stderr)
        return 1
    finally:
        if mic is not None:
            mic.chiudi()
    for riga in descrivi(r, radice, soglia_base, soglia_verifica):
        print(riga)
    return 0


if __name__ == "__main__":
    sys.exit(main())
