#!/bin/bash
# Scarica i dati per l'addestramento di «ehi jarvis» italiano. Uso: bash scarica.sh <cartella_dati>
set -e
D=${1:?cartella dati}; mkdir -p $D/feat $D/piper $D/rir
H=https://huggingface.co/datasets/davidscripka/openwakeword_features/resolve/main
F=$H/openwakeword_features_ACAV100M_2000_hrs_16bit.npy   # (5625000,16,96) float16, header 128 byte
R=3072  # byte per riga
[ -s $D/feat/validation_set_features.npy ] || curl -sSL -o $D/feat/validation_set_features.npy $H/validation_set_features.npy
# solo cinque fette da 500k righe (~1,5 GB l una, 7,7 GB in tutto) con richieste Range, non i 17 GB interi
[ -s $D/feat/acav_a.bin ] || curl -sSL -r 128-$((128+500000*R-1)) -o $D/feat/acav_a.bin $F
[ -s $D/feat/acav_b.bin ] || curl -sSL -r $((128+3000000*R))-$((128+3500000*R-1)) -o $D/feat/acav_b.bin $F
# altre tre fette (più varietà di negativi: con due sole i falsi su validation_set restavano alti)
for k in c:1000000 d:2000000 e:4500000; do
  n=${k%%:*}; r0=${k##*:}
  [ -s $D/feat/acav_$n.bin ] || curl -sSL -r $((128+r0*R))-$((128+(r0+500000)*R-1)) -o $D/feat/acav_$n.bin $F
done
PV=https://huggingface.co/rhasspy/piper-voices/resolve/main
for f in it/it_IT/paola/medium/it_IT-paola-medium it/it_IT/riccardo/x_low/it_IT-riccardo-x_low \
         it/it_IT/serena/medium/it_IT-serena-medium en/en_US/libritts_r/medium/en_US-libritts_r-medium \
         en/en_GB/vctk/medium/en_GB-vctk-medium en/en_US/l2arctic/medium/en_US-l2arctic-medium \
         es/es_ES/sharvard/medium/es_ES-sharvard-medium pt/pt_BR/faber/medium/pt_BR-faber-medium; do
  b=$(basename $f)
  [ -s $D/piper/$b.onnx ] || curl -sSL -o $D/piper/$b.onnx $PV/$f.onnx
  curl -sSL -o $D/piper/$b.onnx.json $PV/$f.onnx.json
  curl -sSL -o $D/piper/$b.MODEL_CARD $PV/$(dirname $f)/MODEL_CARD
done
RH=https://huggingface.co/datasets/davidscripka/MIT_environmental_impulse_responses
for p in $(curl -s "https://huggingface.co/api/datasets/davidscripka/MIT_environmental_impulse_responses/tree/main/16khz" | python3 -c "import json,sys;[print(x['path']) for x in json.load(sys.stdin) if x['path'].endswith('.wav')]"); do
  [ -s $D/rir/$(basename $p) ] || curl -sSL -o $D/rir/$(basename $p) $RH/resolve/main/$p
done
echo FATTO
# parlato italiano vero (MLS, audiolibri LibriVox, CC BY 4.0): una parte del train per i negativi, il test per la valutazione
mkdir -p $D/mls
M=https://huggingface.co/datasets/facebook/multilingual_librispeech/resolve/main/italian
for f in train-00000-of-00008.parquet test-00000-of-00001.parquet; do
  [ -s $D/mls/$f ] || curl -sSL -o $D/mls/$f $M/$f
done
echo FATTO MLS
# parlato inglese di conversazione da lontano (AMI, microfono singolo distante, CC BY 4.0):
# negativi «riunione/cena», il tipo di audio dove il primo modello sbagliava di più
mkdir -p $D/ami
A=https://huggingface.co/datasets/edinburghcstr/ami/resolve/main/sdm
for f in train-00000-of-00027.parquet train-00005-of-00027.parquet train-00013-of-00027.parquet; do
  [ -s $D/ami/$f ] || curl -sSL -o $D/ami/$f $A/$f
done
echo FATTO AMI
