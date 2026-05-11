#!/bin/bash

# Exit on error
set -e

# Number of parallel jobs
nj=4
cmd=run.pl

# Directories
data_train=data/train
data_dev=data/dev
lang_dir=data/lang_test
mono_dir=exp/mono0a
tri_dir=exp/tri1
graph_dir=$tri_dir/graph
decode_dir=$tri_dir/decode_dev

# Step 1: Align phonemes using monophone model
echo "Aligning phonemes with monophone model..."
steps/align_si.sh --nj $nj --cmd "$cmd" $data_train $lang_dir $mono_dir ${mono_dir}_ali

# Step 2: Train a triphone model using the alignments
echo "Training triphone model..."
steps/train_deltas.sh --cmd "$cmd" 2000 10000 $data_train $lang_dir ${mono_dir}_ali $tri_dir

# Step 3: Create HCLG graph for decoding
echo "Building decoding graph..."
utils/mkgraph.sh $lang_dir $tri_dir $graph_dir

# Step 4: Decode test data using the triphone model
echo "Decoding with triphone model..."
steps/decode.sh --nj $nj --cmd "$cmd" $graph_dir $data_dev $decode_dir

# Step 5: Evaluate results
echo "Scoring the results..."
local/score.sh --cmd "$cmd" $data_dev $graph_dir $decode_dir

echo "Find best score"

[ -d exp/mono0a_ali/decode_dev ] && grep WER exp/mono0a_ali/decode_dev/wer_* | utils/best_wer.sh

echo "All steps completed successfully!"

