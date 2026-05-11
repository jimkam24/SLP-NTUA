# Needed for KALDI_ROOT
source path.sh

export IRSTLM=$KALDI_ROOT/tools/irstlm/
export PATH=${PATH}:$IRSTLM/bin

DATA_PATH=~/Desktop/kaldi/egs/usc/data/local/dict
OUTPUT_PATH=../lm_tmp

build-lm.sh -i "$DATA_PATH/lm_train.text" -n 1 -o lm_train1.ilm.gz
build-lm.sh -i "$DATA_PATH/lm_train.text" -n 2 -o lm_train2.ilm.gz
build-lm.sh -i "$DATA_PATH/lm_test.text" -n 1 -o lm_test1.ilm.gz
build-lm.sh -i "$DATA_PATH/lm_test.text" -n 2 -o lm_test2.ilm.gz
build-lm.sh -i "$DATA_PATH/lm_dev.text" -n 1 -o lm_dev1.ilm.gz
build-lm.sh -i "$DATA_PATH/lm_dev.text" -n 2 -o lm_dev2.ilm.gz