import os

MODEL_GEMINI_LITE = os.environ.get("GAS_MODEL_GEMINI_LITE", "gemini-2.5-flash-lite")
MODEL_GEMINI_FLASH = os.environ.get("GAS_MODEL_GEMINI_FLASH", "gemini-2.5-flash")
MODEL_GROQ = os.environ.get("GAS_MODEL_GROQ", "openai/gpt-oss-120b")
MODEL_OPENROUTER = os.environ.get("GAS_MODEL_OPENROUTER", "meta-llama/llama-3.3-70b-instruct:free")
MODEL_OLLAMA = os.environ.get("GAS_MODEL_OLLAMA", "qwen2.5:7b-instruct")
