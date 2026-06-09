import os
import json
import requests

class FakeMsg:
    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls if tool_calls is not None else []

class FakeFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class FakeToolCall:
    def __init__(self, tc_id, function_obj):
        self.id = tc_id
        self.type = "function"
        self.function = function_obj

def chat(messages, tools_schema=None):
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return FakeMsg("Errore API: Chiave OPENROUTER_API_KEY o ANTHROPIC_API_KEY assente.")

    system_instruction = (
        "Sei Gas, un agente operativo autonomo ottimizzato per Marketing, Coding e Comandi Vocali. "
        "La tua risposta testuale deve essere BREVE, DISCORSIVA, PRIVA di blocchi di codice o markdown.\n"
        "Se l'utente richiede modifiche, creazioni di file, cartelle o analisi, devi GENERARE "
        "l'azione includendo nella risposta un oggetto JSON pulito nel testo strutturato in questo modo:\n"
        "{\"action\": \"nome_tool\", \"params\": {\"chiave\": \"valore\"}}\n"
        "Tool supportati: read_file(path), write_file(path, content), run_command(command), list_dir(path)."
    )

    formatted_messages = [{"role": "system", "content": system_instruction}]
    for m in messages[-8:]:
        role = m.get("role", "user")
        if role == "system": continue
        content_text = m.get("content") or ""
        if role == "tool":
            role = "user"
            content_text = f"[Risultato dello strumento eseguito]: {content_text}"
        if len(str(content_text)) > 2000:
            content_text = str(content_text)[:2000] + "... [Payload troncato]"
        formatted_messages.append({"role": role, "content": content_text})

    response = None

    # 1. TENTATIVO SILENZIOSO TRAMITE OPENROUTER
    if os.environ.get("OPENROUTER_API_KEY"):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        models_to_try = [
            "anthropic/claude-3.5-sonnet", "anthropic/claude-3.5-sonnet:beta",
            "google/gemini-2.5-pro", "meta-llama/llama-3.3-70b-instruct",
            "meta-llama/llama-3.3-70b-instruct:free", "deepseek/deepseek-r1:free"
        ]
        
        for model_name in models_to_try:
            try:
                res = requests.post(url, headers=headers, json={"model": model_name, "messages": formatted_messages, "temperature": 0.2}, timeout=15)
                if res.status_code == 200:
                    response = res
                    break
            except Exception:
                continue

    # 2. SE OPENROUTER FALLISCE, PASSA A GROQ SENZA SPAMMARE IL TERMINALE
    if not response and os.environ.get("GROQ_API_KEY"):
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        groq_headers = {"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}", "Content-Type": "application/json"}
        try:
            g_res = requests.post(groq_url, headers=groq_headers, json={"model": "llama-3.3-70b-versatile", "messages": formatted_messages, "temperature": 0.2}, timeout=15)
            if g_res.status_code == 200:
                response = g_res
                print("  \033[92m✔ Canale Cloud saturato o non disponibile. Esecuzione assistita da Groq (Llama 3.3)\033[0m")
        except Exception:
            pass

    if not response:
        return FakeMsg("Errore Canali API: Nessun provider ha risposto.")

    try:
        res_json = response.json()
        text_reply = res_json["choices"][0]["message"]["content"] or ""
        tool_calls = []
        text_to_scan = text_reply
        
        while True:
            start_idx = text_to_scan.find("{")
            if start_idx == -1: break
            brace_count = 0
            end_idx = -1
            for i in range(start_idx, len(text_to_scan)):
                if text_to_scan[i] == "{": brace_count += 1
                elif text_to_scan[i] == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i
                        break
            if end_idx != -1:
                p_json = text_to_scan[start_idx:end_idx+1]
                try:
                    parsed = json.loads(p_json.strip())
                    action = parsed.get("action")
                    params = parsed.get("params", {})
                    if action:
                        fn_obj = FakeFunction(action, json.dumps(params))
                        tool_calls.append(FakeToolCall(f"vcall_claude_{action}", fn_obj))
                        text_reply = text_reply.replace(p_json, "").strip()
                except Exception:
                    pass
                text_to_scan = text_to_scan[end_idx+1:]
            else:
                text_to_scan = text_to_scan[start_idx+1:]

        return FakeMsg(content=text_reply, tool_calls=tool_calls)
    except Exception as e:
        return FakeMsg(f"Errore nel parsing della risposta finale: {e}")