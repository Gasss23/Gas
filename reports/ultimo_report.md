# deps: pin core riproducibile + requests, escludi voce/Windows
**Data:** 2026-06-29 | **Scope:** solo requirements.txt — nessun tocco al motore

---

## A — DIRETTI MANCANTI VERIFICATI

Grep fresco su gas.py, brains/, modules/ → filtrando stdlib + locali → 5 terzi:

| PyPI | import | dove | top-level? | in old req.txt |
|------|--------|------|-----------|----------------|
| `openai` | `from openai import OpenAI` | gas.py:11 | ✅ sì | ✅ sì |
| `requests` | `import requests` | brains/*.py (tutti e 4) | ✅ sì | ❌ **MANCANTE** |
| `numpy` | `import numpy as _np` | modules/memory/vectors.py:57 | lazy try/except | ✅ sì |
| `fastembed` | `from fastembed import TextEmbedding` | modules/memory/vectors.py:63 | lazy try/except | ✅ sì |
| `onnxruntime` | _(transitivo di fastembed)_ | — | — | ✅ sì (esplicito) |

**Confermato: SOLO `requests` era il diretto mancante.** Nessun altro buco emerso.
torch/whisper/elevenlabs/pywin32/comtypes → ZERO occorrenze. Confermato.

---

## B — VERSIONI REALI INSTALLATE (output grezzo)

```
pip show openai numpy onnxruntime fastembed requests | grep -E "^(Name|Version):"

Name: openai
Version: 2.43.0
Name: numpy
Version: 2.4.6
Name: onnxruntime
Version: 1.27.0
Name: fastembed
Version: 0.8.0
Name: requests
Version: 2.34.2
```

---

## C — CHECK STATICO OPENAI 2.x

### Usi SDK trovati in gas.py (righe grezze)

```
gas.py:11  from openai import OpenAI

# istanziazione (run_turn, main loop):
gas.py:1465  client = OpenAI(base_url=url, api_key=os.environ.get(env))

# chiamata (normale + retry Gemini 400):
gas.py:1469  response = client.chat.completions.create(
gas.py:1471      model=model, messages=payload, tools=self.tools_schema, tool_choice="auto"
gas.py:1480  response = client.chat.completions.create(  # retry
gas.py:1481      model=model, messages=payload, tools=self.tools_schema, tool_choice="auto"

# lettura response:
gas.py:1488  usage = getattr(response, "usage", None)
gas.py:1491  getattr(usage, "prompt_tokens", 0)
gas.py:1492  getattr(usage, "completion_tokens", 0)
gas.py:1493  msg = response.choices[0].message
gas.py:1495  if msg.tool_calls:
gas.py:1496      ... msg.content ... msg.tool_calls ...
gas.py:1498      tc.function.name, tc.function.arguments
gas.py:1508      tc.id
gas.py:1512  elif msg.content:

# gestione eccezioni (status_code):
gas.py:1532  getattr(e, "status_code", None)

# istanziazione (doctor):
gas.py:1575  client = OpenAI(base_url=url, api_key=os.environ[env], timeout=15)
gas.py:1577  client.chat.completions.create(model=model, messages=[...], max_tokens=1)
gas.py:1581  getattr(e, "status_code", None)
```

### Esito check 2.x (fonte: METADATA del pacchetto installato)

Il README dentro `openai-2.43.0.dist-info/METADATA` dice testualmente:
> *"The previous standard (**supported indefinitely**) for generating text is the
> [Chat Completions API](https://platform.openai.com/docs/api-reference/chat)."*

Verifica punto per punto:

| uso | stato in 2.x | note |
|-----|-------------|------|
| `OpenAI(base_url=..., api_key=..., timeout=...)` | ✅ invariato | costruttore identico |
| `client.chat.completions.create(...)` | ✅ **supported indefinitely** | dichiarato esplicitamente nel README 2.x |
| `response.choices[0].message` | ✅ invariato | struttura ChatCompletion non cambiata |
| `msg.tool_calls`, `tc.function.name`, `tc.function.arguments`, `tc.id` | ✅ invariati | |
| `getattr(response, "usage", None)` + `getattr(usage, "prompt_tokens/completion_tokens", 0)` | ✅ safe | getattr con default — robusto a qualunque variazione |
| `getattr(e, "status_code", None)` | ✅ presente | `APIStatusError.status_code` confermato in `_exceptions.py` 2.43.0 |

**Esito: tutti gli usi sono compatibili 2.x → pin `openai==2.43.0` approvato.**

Nota: la macchina sta già girando openai 2.43.0 con test verdi — il check statico
lo conferma formalmente ma non aggiunge nuova evidenza a ciò che già funziona.

---

## D — requirements.txt FINALE (cat)

```
# voce (torch/whisper/elevenlabs) e Windows-only: esclusi dal deploy core
openai==2.43.0
requests==2.34.2
numpy==2.4.6
onnxruntime==1.27.0
fastembed==0.8.0
```

**Logica del pin:**
- `openai==2.43.0` — versione operativa con test verdi, check 2.x clean
- `requests==2.34.2` — aggiunto: era il diretto mancante (crash deploy fresh)
- `numpy==2.4.6` + `onnxruntime==1.27.0` — coppia ABI pinnata insieme (numpy 2.x rompe ABI)
- `fastembed==0.8.0` — layer vettoriale fail-safe
- onnxruntime resta esplicito (non solo transitivo): necessario per non saltare T30/T31/T32 in CI

**Limite noto:** wheel testate su Windows AMD64. Verifica manylinux_x86_64 al deploy CX22:
`pip download -r requirements.txt --platform manylinux_x86_64 --python-version 311 --only-binary=:all:`
