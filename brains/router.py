import os

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

def get_brain(messaggio):
    msg = messaggio.lower()

    if msg.startswith("@groq"):
        return "groq", messaggio[5:].strip()
    elif msg.startswith("@gemini") or msg.startswith("@openrouter"):
        return "openrouter", messaggio[7:].strip()
    elif msg.startswith("@claude"):
        return "claude", messaggio[7:].strip()

    if any(w in msg for w in ["analizza", "debug", "refactor", "ottimizza", "complesso"]):
        return "openrouter", messaggio
    elif any(w in msg for w in ["scrivi", "copy", "ads", "marketing", "campagna"]):
        return "openrouter", messaggio

    return "groq", messaggio

def _chiama(brain_name: str, testo: str):
    """Invoca chat() del brain richiesto e restituisce l'oggetto risposta."""
    if brain_name == "groq":
        from brains.groq_brain import chat
        return chat([{"role": "user", "content": testo}])
    elif brain_name in ("claude", "openrouter"):
        from brains.claude_brain import chat
        return chat([{"role": "user", "content": testo}])
    elif brain_name == "gemini":
        from brains.gemini_brain import chat
        return chat([{"role": "user", "content": testo}])

def rispondi(messaggio, memoria=[]):
    brain, testo = get_brain(messaggio)

    # Catena di fallback: qualsiasi eccezione (timeout, 429, rete) passa al successivo
    if brain in ("openrouter", "claude"):
        catena = [("claude", "Claude/OpenRouter"), ("groq", "Groq(fallback)")]
    else:
        catena = [("groq", "Groq"), ("claude", "OpenRouter(fallback)")]

    for brain_name, etichetta in catena:
        try:
            msg = _chiama(brain_name, testo)
            return msg.content, etichetta
        except Exception:
            continue

    return "Tutti i provider hanno fallito.", "nessuno"
