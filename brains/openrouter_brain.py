import os
import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

MODELS = [
    "qwen/qwen-2.5-72b-instruct:free",
    "cohere/command-r-plus:free",
    "meta-llama/llama-3-8b-instruct:free"
]

def chiedi_openrouter(cronologia_completa):
    if not OPENROUTER_API_KEY:
        return "Errore: OPENROUTER_API_KEY manca nei segreti dell'ambiente."
    
    # Estraiamo l'ultimo messaggio dell'utente per OpenRouter
    ultimo_messaggio = next((m["content"] for m in reversed(cronologia_completa) if m["role"] == "user"), "")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [{"role": "user", "content": ultimo_messaggio}]
    }
    
    for current_model in MODELS:
        try:
            data["model"] = current_model
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=10 # Alzato a 10 secondi per evitare falsi timeout sui modelli free
            )
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and "choices" in result and len(result["choices"]) > 0:
                    return str(result["choices"][0]["message"]["content"])
        except:
            continue

    # FALLBACK: Se OpenRouter fallisce, proviamo Groq ma in modo sicuro
    print(f"  \033[93m⚠ OpenRouter KO o lento. Fallback d'emergenza su Groq con memoria ottimizzata...\033[0m")
    try:
        from brains.groq_brain import chat as groq_chat
        
        cronologia_ottimizzata = []
        for m in cronologia_completa:
            contenuto = m["content"]
            if "Rate limit reached for model" in contenuto or "Request too large" in contenuto:
                linee = contenuto.split("\n")
                contenuto = "\n".join(linee[:3]) + "\n[...Errore di sistema troncato per risparmiare spazio...]"
            
            cronologia_ottimizzata.append({"role": m["role"], "content": contenuto})
        
        res = groq_chat(cronologia_ottimizzata)
        # Controlliamo se res è un oggetto con attributo content o una stringa
        if hasattr(res, "content"):
            return res.content
        return str(res)
    except Exception as groq_err:
        return "Servizio momentaneamente sovraccarico. Riprova tra pochissimi secondi!"

class FakeMsg:
    def __init__(self, content):
        self.content = content

def chat(messages):
    risposta = chiedi_openrouter(messages)
    # Forza risposta a essere una stringa pulita prima di impacchettarla
    return FakeMsg(str(risposta))