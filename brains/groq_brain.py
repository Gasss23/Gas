import os
import json
import requests

class FakeMsg:
    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls if tool_calls is not None else []

def chat(messages, tools_schema=None):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return FakeMsg("Errore API: GROQ_API_KEY assente.")
        
    # Taglio aggressivo del contesto per eliminare i blocchi da Rate Limit di Groq nelle automazioni
    if len(messages) > 8:
        messages = messages[:2] + messages[-6:]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.1
    }
    
    if tools_schema:
        payload["tools"] = tools_schema
        payload["tool_choice"] = "auto"
        
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=12)
        if response.status_code != 200:
            return FakeMsg(f"Errore Groq API: {response.text}")
            
        res_json = response.json()
        message_obj = res_json["choices"][0]["message"]
        tool_calls = message_obj.get("tool_calls", [])
        
        return FakeMsg(content=message_obj.get("content") or "", tool_calls=tool_calls)
        
    except Exception as e:
        return FakeMsg(f"Errore critico Groq Brain: {e}")