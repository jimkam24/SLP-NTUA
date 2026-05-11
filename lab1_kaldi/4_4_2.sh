#!/bin/bash
source ./path.sh

# Rename G_train_unigram.fst to G.fst in order to
# run the mkgraph.sh which searches for an G.fst.

# unigram
cp data/lang_test/G_train_ug.fst data/lang_test/G.fst
# Make HCLG graph.
utils/mkgraph.sh --mono data/lang_test exp/mono0a exp/mono0a/graph_nosp_tgpr_ug



# bigram

cp data/lang_test/G_train_bg.fst data/lang_test/G.fst
# Make HCLG graph.
utils/mkgraph.sh --mono data/lang_test exp/mono0a exp/mono0a/graph_nosp_tgpr_bg
