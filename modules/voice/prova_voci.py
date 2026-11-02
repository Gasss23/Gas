"""
V8 (chat M2) — «prova voci»: aiuta l'operatore a scegliere la voce di Gas all'ascolto.

- `ordina_voci`: le voci dell'account ElevenLabs, con in cima le candidate (maschili, calme,
  accento britannico: lo «stile maggiordomo»). Solo le categorie AMMESSE (R-624-1-M2:
  elenco di ammesse, non di vietate): voci di serie, voci create da descrizione e voci
  professionali con licenza. Fuori le clonate, le «famous» e qualunque categoria nuova:
  lo stile sì, l'imitazione di una persona vera no. Il server accetta in prova solo le voci
  dell'ultimo elenco mostrato.
- `FRASI_PROVA`: frasi italiane FISSE (mai testo libero dalla pagina: ogni prova spende
  caratteri ElevenLabs, quindi si sceglie solo fra queste).
- `piper_disponibile` / `sintetizza_piper`: voce locale gratis, solo se sul computer ci sono
  il comando `piper` e un modello italiano (GAS_PIPER_MODEL = percorso del file .onnx).

Zero dipendenze esterne. Nessuna scrittura del `.env`: la pagina dice quale riga metterci.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List, Optional

FRASI_PROVA = (
    "Buongiorno. Ho controllato i lead di stanotte: tre sono interessanti, uno è urgente. "
    "Vuole che prepari le bozze?",
    "Fatto. Il report è pronto e l'ho salvato nella cartella del progetto. Il resto è a schermo.",
    "Mi scusi, non ho capito bene. Può ripetere?",
)

_ID_VOCE = re.compile(r"^[A-Za-z0-9]{8,40}$")
CATEGORIE_AMMESSE = frozenset({"premade", "generated", "professional"})
PIPER = "piper"   # id riservato alla voce locale

_PAROLE_CALME = ("calm", "warm", "deep", "mature", "soft", "narrat", "authoritative",
                 "classy", "gentle", "smooth", "butler", "confident", "trustworthy")


def voce_valida(voice_id: Any) -> bool:
    """Id di voce accettabile nel percorso dell'API ElevenLabs (niente `/`, `?`, ecc.)."""
    return isinstance(voice_id, str) and bool(_ID_VOCE.match(voice_id))


def _punteggio(v: Dict[str, str]) -> int:
    genere = v.get("genere", "").lower()
    accento = v.get("accento", "").lower()
    testo = f"{v.get('descrizione', '')} {v.get('nome', '')}".lower()
    punti = 0
    if genere == "male":
        punti += 3
    if "british" in accento or "english" in accento:
        punti += 2
    if any(p in testo for p in _PAROLE_CALME):
        punti += 1
    if v.get("eta", "").lower() in ("middle aged", "middle_aged", "old"):
        punti += 1
    return punti


def ordina_voci(voci: List[Dict[str, str]], attuale: str = "") -> List[Dict[str, Any]]:
    """Voci da far provare: solo categorie ammesse e id puliti, le candidate prima.
    Ogni voce riceve `candidata` (True per le prime per punteggio) e `attuale`."""
    buone = [v for v in voci
             if voce_valida(v.get("id")) and v.get("categoria", "").lower() in CATEGORIE_AMMESSE]
    buone.sort(key=lambda v: (-_punteggio(v), v.get("nome", "")))
    out: List[Dict[str, Any]] = []
    for v in buone:
        # candidata = maschile + accento britannico + almeno un tratto calmo o maturo
        out.append(dict(v, candidata=_punteggio(v) >= 6, attuale=v.get("id") == attuale))
    return out


def piper_disponibile() -> Optional[str]:
    """Percorso del modello Piper se la voce locale si può usare, altrimenti None."""
    modello = os.environ.get("GAS_PIPER_MODEL", "").strip()
    if not modello or not os.path.isfile(modello) or not shutil.which("piper"):
        return None
    return modello


def sintetizza_piper(testo: str, modello: str, timeout: float = 60) -> bytes:
    """WAV della frase con Piper (programma locale, gratis). Il testo va su stdin, mai
    nella riga di comando. Solleva OSError / subprocess.SubprocessError se fallisce."""
    with tempfile.TemporaryDirectory(prefix="gas_piper_") as cartella:
        uscita = os.path.join(cartella, "voce.wav")
        subprocess.run(["piper", "--model", modello, "--output_file", uscita],
                       input=testo.encode("utf-8"), capture_output=True, timeout=timeout,
                       check=True)
        with open(uscita, "rb") as f:
            return f.read()
