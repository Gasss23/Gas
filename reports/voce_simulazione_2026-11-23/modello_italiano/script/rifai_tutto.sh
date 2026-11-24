#!/bin/bash
# Rifà da zero il modello «ehi jarvis» con accento italiano (openWakeWord, solo CPU).
# Uso:  bash rifai_tutto.sh <cartella_di_lavoro>
# Serve: python 3.11+ (provato con 3.13), espeak-ng, ffmpeg, ~25 GB di disco, ~12 GB di RAM,
# rete verso huggingface.co (e i suoi CDN, oggi us.aws.cdn.hf.co) e PyPI.
# Tempi su 4 CPU: scarico ~5 min, clip ~50 min, caratteristiche ~25 min, addestramento ~15 min,
# valutazione 1-2 ore (le tracce a 4 fasi sono lente). Semi fissi, ma JAX su CPU può dare
# numeri leggermente diversi da una macchina all'altra.
set -euo pipefail
W=$(realpath "${1:?cartella di lavoro}")
QUI=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W"
cd "$W"
if [ ! -x tenv/bin/python ]; then
  python3 -m venv tenv
  tenv/bin/pip install -q "jax[cpu]" optax onnx piper-tts onnxruntime scipy numpy scikit-learn \
    tqdm requests soundfile pyarrow
  # openwakeword 0.6.0 senza dipendenze (tflite-runtime non esiste per Python recenti: si usa onnx)
  tenv/bin/pip install -q --no-deps openwakeword==0.6.0
  tenv/bin/python -c "import openwakeword.utils as u; u.download_models(['hey_jarvis'])"
fi
PY=tenv/bin/python
bash "$QUI/scarica.sh" "$W/dati"
[ -s dati/mls_test.npy ] || $PY "$QUI/mls.py" dati/mls_test.npy 100000 dati/mls/test-00000-of-00001.parquet
[ -s dati/mls_train.npy ] || $PY "$QUI/mls.py" dati/mls_train.npy 3700 dati/mls/train-00000-of-00008.parquet
[ -s dati/ami_train.npy ] || $PY "$QUI/mls.py" dati/ami_train.npy 1000000 dati/ami/*.parquet
$PY "$QUI/genera.py" dati clip                       # clip sintetiche (piper + espeak-ng)
$PY "$QUI/feature.py" dati clip feat                 # augmentation + caratteristiche
mkdir -p modelli
# configurazione scelta il 24/11 (v7): rete 128, 1 blocco, negativi avversari (anche «ehi + nome»)
# 384 per passo, parlato vero MLS+AMI 256, ACAV 1024
$PY "$QUI/addestra.py" dati feat modelli/ehi_jarvis_it.onnx --dim 128 --blocchi 1 \
  --passi 50000 --wmax 1500 --batch 64,384,256,1024 --seme 2
# valutazione (facoltativa): flussi nuovi + tracce col rilevatore vero di una copia del repo
if [ -n "${GAS_REPO:-}" ]; then
  mkdir -p repo flussi tracce ris
  git -C "$GAS_REPO" archive HEAD clients scripts/voce | tar -x -C repo
  $PY "$QUI/flussi_nuovi.py" dati flussi
  for M in hey_jarvis modelli/ehi_jarvis_it.onnx; do
    for F in 1 4; do
      $PY "$QUI/valuta.py" tracce repo flussi tracce $M $F G_chiamate_nuove H_parlato_vero
      T=$(basename $M .onnx)
      $PY "$QUI/valuta.py" griglia repo flussi tracce $T $F 0.3,0.4,0.5,0.6,0.7,0.8,0.9 \
        G_chiamate_nuove H_parlato_vero > ris/griglia_${T}_f$F.json
    done
  done
  $PY "$QUI/valuta.py" validazione dati hey_jarvis modelli/ehi_jarvis_it.onnx
  $PY "$QUI/quasi_prova.py" dati hey_jarvis modelli/ehi_jarvis_it.onnx
  $PY "$QUI/tabella.py" ris/griglia_*.json
fi
echo "fatto: $W/modelli/ehi_jarvis_it.onnx"
