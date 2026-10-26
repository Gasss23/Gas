# brains/router.py — classificatore del compito per la cascata (run_turn).
# Simboli vivi: classifica_compito e prefisso_forte (R2). Storia: le funzioni legacy get_brain/rispondi/
# _chiama (pipeline pre-kernel, slicing grezzo della history — violazione sez.5
# CLAUDE.md) e i brain legacy non wired sono stati rimossi il 2026-07-15
# (revisione fondamenta Fable-5, vedi reports/roadmap.md).

from typing import Optional, Tuple

KEYWORDS_COMPLESSO = [
    "analizza", "debug", "refactor", "ottimizza", "complesso",
    "scrivi", "copy", "ads", "marketing", "campagna",
    "implementa", "architettura", "spiega", "confronta",
]

def classifica_compito(messaggio: str) -> str:
    """Restituisce 'semplice' o 'complesso' in base a lunghezza e keyword."""
    msg = messaggio.lower().strip()
    if len(msg) < 60 and not any(w in msg for w in KEYWORDS_COMPLESSO):
        return "semplice"
    return "complesso"


def prefisso_forte(prompt: str) -> Tuple[Optional[str], str]:
    """R2: «/forte <richiesta>» manda il turno al solo cervello forte (mai ai gratuiti);
    con la barra una frase normale non ci finisce per sbaglio (R-511-2). Fail-closed
    (V-1 bot #269): qualunque testo che inizia con «/forte» ma non è «/forte», un
    separatore (spazio, tab, NBSP…) e una richiesta → ("uso", ""), mai ai gratuiti.
    Ritorna (cervello, richiesta): (None, prompt) se il prefisso non c'è. Un prefisso
    scritto male («/frote») non è riconoscibile: va come testo normale (limite
    dichiarato in reports/r2_regole_abbonamento.md). Usata da terminale, Telegram e
    voce (R-ve269-2)."""
    if not prompt.lower().startswith("/forte"):
        return None, prompt
    parti = prompt.split(None, 1)  # None: separa su ogni spazio Unicode (NBSP, tab)
    if parti[0].lower() != "/forte" or len(parti) < 2 or not parti[1].strip():
        return "uso", ""
    return "forte", parti[1].strip()
