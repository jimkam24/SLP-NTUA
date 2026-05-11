. ./path.sh # Needed for KALDI_ROOT
. ./cmd.sh

#===================================4_4_1====================================

steps/train_mono.sh --nj 4 --cmd "$train_cmd" \
data/train data/lang_test exp/mono0a || exit 1;
