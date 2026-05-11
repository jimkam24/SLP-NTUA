source ./path.sh

echo "Running decode for testing set - unigram model"
steps/decode.sh exp/mono0a/graph_nosp_tgpr_ug   data/test exp/mono0a/decode_test_ug

echo "Running decode for validation set - unigram model"
steps/decode.sh exp/mono0a/graph_nosp_tgpr_ug   data/dev exp/mono0a/decode_dev_ug

echo "Running decode for testing set - bigram model"
steps/decode.sh exp/mono0a/graph_nosp_tgpr_bg   data/test exp/mono0a/decode_test_bg

echo "Running decode for validation set - bigram model"
steps/decode.sh exp/mono0a/graph_nosp_tgpr_bg   data/dev exp/mono0a/decode_dev_bg


