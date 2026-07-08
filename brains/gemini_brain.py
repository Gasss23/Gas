import os
import requests

from brains.model_ids import MODEL_GEMINI_FLASH, MODEL_GROQ

class FakeGeminiResponse:
    def __init__(self, text):
        # Modificato da self.text a self.content per allinearsi a gas.py
        self.content = text
        # Evita crash se gas.py controlla la presenza di tool_calls
        self.tool_calls = []

def chat(history, tools_schema=None, **kwargs):
    """
    Riceve la history dei messaggi da gas.py, la adatta ai formati 
    delle API e gestisce il failover automatico.
    """
    google_key = os.environ.get("GEMINI_API_KEY")
    if google_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_GEMINI_FLASH}:generateContent?key={google_key}"
        headers = {"Content-Type": "application/json"}
        
        # Converte la history di Gas nel formato 'contents' richiesto da Google
        contents = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content", "")
            
            # Salta i messaggi dei tool grezzi che l'API standard non digerisce direttamente
            if not content and "tool_calls" in msg:
                continue
                
            # Per Google, l'assistente si chiama 'model'
            g_role = "model" if role == "assistant" else "user"
            if content:
                contents.append({"role": g_role, "parts": [{"text": content}]})
        
        payload = {"contents": contents, "generationConfig": {"temperature": 0.3}}
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=15)
            if res.status_code == 200:
                data = res.json()
                text_out = data["candidates"][0]["content"]["parts"][0]["text"]
                return FakeGeminiResponse(text_out)
        except Exception:
            pass

    # SE GEMINI È BLOCCATO DALLA QUOTA (429), RECUPERA DA GROQ PER PORTARE A TERMINE LA RISPOSTA
    if os.environ.get("GROQ_API_KEY"):
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        groq_headers = {
            "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        # Pulisce la history per passarla a Groq in formato standard OpenAI
        messages = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content", "")
            if role in ["user", "assistant", "system"] and content:
                messages.append({"role": role, "content": content})
        
        try:
            g_res = requests.post(groq_url, headers=groq_headers, json={
                "model": MODEL_GROQ,
                "messages": messages,
                "temperature": 0.3,
                "reasoning_effort": "low"
            }, timeout=15)
            if g_res.status_code == 200:
                text_out = g_res.json()["choices"][0]["message"]["content"]
                return FakeGeminiResponse(text_out)
        except Exception:
            pass

    return FakeGeminiResponse("Sia le API di Gemini che i sistemi di recupero sono attualmente saturi. Riprova tra poco.")