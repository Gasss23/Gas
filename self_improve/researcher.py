import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "logs"
RESEARCH_LOG = LOGS_DIR / "ai_research.json"
PENDING_FILE = LOGS_DIR / "PENDING_APPROVALS.md"

AI_TOPICS = [
    "new AI API 2025",
    "best AI tools for marketing automation",
    "AI video generation API",
    "AI voice API free tier",
    "Meta ads automation AI",
    "new LLM models released",
]

def search_web(query: str) -> str:
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Gas-Agent/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        results = []
        if data.get("AbstractText"):
            results.append(data["AbstractText"])
        for topic in data.get("RelatedTopics", [])[:3]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(topic["Text"])
        return "\n".join(results) if results else "Nessun risultato"
    except Exception as e:
        return f"Errore: {e}"

def analyze_with_groq(content: str, query: str) -> dict:
    try:
        from brains import groq_brain
        messages = [
            {"role": "system", "content": 'Analizza se questa scoperta è utile per Gas, un agente AI per coding e marketing. Rispondi SOLO in JSON: {"useful": true/false, "name": "nome", "reason": "perché", "integration": "come integrarlo", "cost": "gratuito/pagamento"}'},
            {"role": "user", "content": f"Query: {query}\n\nContenuto:\n{content}"}
        ]
        msg = groq_brain.chat(messages, max_tokens=500)
        text = msg.content.strip()
        if "```" in text:
            text = text.split("```")[1].replace("json","").strip()
        return json.loads(text)
    except Exception:
        return {"useful": False}

def run_research_cycle():
    LOGS_DIR.mkdir(exist_ok=True)
    print(f"\033[90m[Research] Avvio - {datetime.now().strftime('%H:%M')}\033[0m")
    discoveries = []
    for topic in AI_TOPICS:
        content = search_web(topic)
        if content and "Errore" not in content:
            analysis = analyze_with_groq(content, topic)
            if analysis.get("useful"):
                discoveries.append({
                    "timestamp": datetime.now().isoformat(),
                    "query": topic,
                    "name": analysis.get("name","Unknown"),
                    "reason": analysis.get("reason",""),
                    "integration": analysis.get("integration",""),
                    "cost": analysis.get("cost","sconosciuto"),
                })
    existing = []
    if RESEARCH_LOG.exists():
        try:
            existing = json.loads(RESEARCH_LOG.read_text())
        except Exception:
            pass
    existing.extend(discoveries)
    RESEARCH_LOG.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    if discoveries:
        existing_md = PENDING_FILE.read_text() if PENDING_FILE.exists() else "# Approvazioni Pendenti\n\n"
        new = f"\n## Tool AI Scoperti — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        for d in discoveries:
            new += f"### {d['name']}\n- **Perché:** {d['reason']}\n- **Come:** {d['integration']}\n- **Costo:** {d['cost']}\n- **Stato:** ⏳ attesa approvazione\n\n"
        PENDING_FILE.write_text(existing_md + new)
    print(f"\033[90m[Research] {len(discoveries)} scoperte.\033[0m")
    return discoveries
