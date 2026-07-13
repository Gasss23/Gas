import os

MODEL_GEMINI_LITE = os.environ.get("GAS_MODEL_GEMINI_LITE", "gemini-2.5-flash-lite")
MODEL_GEMINI_FLASH = os.environ.get("GAS_MODEL_GEMINI_FLASH", "gemini-2.5-flash")
MODEL_GROQ = os.environ.get("GAS_MODEL_GROQ", "openai/gpt-oss-120b")
MODEL_OPENROUTER = os.environ.get("GAS_MODEL_OPENROUTER", "meta-llama/llama-3.3-70b-instruct:free")
MODEL_OLLAMA = os.environ.get("GAS_MODEL_OLLAMA", "qwen2.5:7b-instruct")

# Prezzi Groq per milione di token (USD) — fonte groq.com/pricing, verificato 2026-07-13.
# Storico: output era $0.75 al lancio, sceso a $0.60. Overridabili via env GAS_GROQ_PRICE_IN/OUT.
try:
    GROQ_PRICE_IN_USD_PER_1M  = float(os.getenv("GAS_GROQ_PRICE_IN",  "0.15"))
    GROQ_PRICE_OUT_USD_PER_1M = float(os.getenv("GAS_GROQ_PRICE_OUT", "0.60"))
except (TypeError, ValueError):
    GROQ_PRICE_IN_USD_PER_1M  = 0.15
    GROQ_PRICE_OUT_USD_PER_1M = 0.60
