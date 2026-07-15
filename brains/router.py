# brains/router.py — classificatore del compito per la cascata (run_turn).
# UNICO simbolo vivo del modulo. Storia: le funzioni legacy get_brain/rispondi/
# _chiama (pipeline pre-kernel, slicing grezzo della history — violazione sez.5
# CLAUDE.md) e i brain legacy non wired sono stati rimossi il 2026-07-15
# (revisione fondamenta Fable-5, vedi reports/roadmap.md).

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
