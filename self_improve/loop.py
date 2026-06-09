import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

LOGS_DIR = ROOT / "logs"
CHANGELOG = LOGS_DIR / "CHANGELOG_AUTO.md"
GAS_FILE = ROOT / "gas.py"
IMPROVE_INTERVAL = 3600
RESEARCH_INTERVAL = 7200

def log(msg):
    print(f"\033[90m[AutoImprove {datetime.now().strftime('%H:%M:%S')}] {msg}\033[0m")

def analyze_gas_code():
    try:
        code = GAS_FILE.read_text()
        try:
            from brains import gemini_brain as brain
            brain_name = "Gemini"
        except Exception:
            from brains import groq_brain as brain
            brain_name = "Groq"
        log(f"Analisi con {brain_name}...")
        messages = [
            {"role": "system", "content": 'Sei un senior engineer. Analizza questo codice e suggerisci miglioramenti. Rispondi SOLO in JSON: {"improvements": [{"title": "...", "description": "...", "priority": "high/medium/low"}], "summary": "..."}'},
            {"role": "user", "content": f"```python\n{code}\n```"}
        ]
        msg = brain.chat(messages, max_tokens=2000)
        text = msg.content.strip()
        if "```" in text:
            text = text.split("```")[1].replace("json","").strip()
        return json.loads(text)
    except Exception as e:
        log(f"Errore analisi: {e}")
        return {"improvements": [], "summary": f"Errore: {e}"}

def update_changelog(analysis, discoveries=None):
    LOGS_DIR.mkdir(exist_ok=True)
    existing = CHANGELOG.read_text() if CHANGELOG.exists() else "# Gas Auto-Changelog\n\n"
    entry = f"\n## {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    entry += f"**Analisi:** {analysis.get('summary','N/A')}\n\n"
    improvements = analysis.get('improvements', [])
    if improvements:
        entry += f"**Miglioramenti suggeriti ({len(improvements)}):**\n"
        for i in improvements:
            entry += f"- [{i.get('priority','?')}] {i.get('title','')}: {i.get('description','')}\n"
        entry += "\n"
    if discoveries:
        entry += f"**Tool AI scoperti ({len(discoveries)}):**\n"
        for d in discoveries:
            entry += f"- {d['name']}: {d['reason']}\n"
        entry += "\n"
    CHANGELOG.write_text(existing + entry)

def save_pending(improvements):
    pending_file = LOGS_DIR / "PENDING_APPROVALS.md"
    existing = pending_file.read_text() if pending_file.exists() else "# Approvazioni Pendenti\n\n"
    new = f"\n## Miglioramenti Codice — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    for imp in improvements:
        new += f"### [{imp.get('priority','?')}] {imp.get('title','')}\n{imp.get('description','')}\n\n"
    pending_file.write_text(existing + new)

def run_loop():
    log("🚀 Loop avviato")
    LOGS_DIR.mkdir(exist_ok=True)
    last_research = 0
    cycle = 0
    while True:
        cycle += 1
        log(f"Ciclo #{cycle}")
        analysis = analyze_gas_code()
        if analysis.get("improvements"):
            save_pending(analysis["improvements"])
        discoveries = []
        if time.time() - last_research > RESEARCH_INTERVAL:
            try:
                from self_improve.researcher import run_research_cycle
                discoveries = run_research_cycle()
                last_research = time.time()
            except Exception as e:
                log(f"Errore research: {e}")
        update_changelog(analysis, discoveries)
        log(f"Ciclo completato. Prossimo tra {IMPROVE_INTERVAL//60} min.")
        time.sleep(IMPROVE_INTERVAL)

if __name__ == "__main__":
    run_loop()
