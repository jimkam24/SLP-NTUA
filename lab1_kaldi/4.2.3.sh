# Load Kaldi environment
source ./path.sh  # Sets up KALDI_ROOT

# Set and export IRSTLM path
export IRSTLM=$KALDI_ROOT/tools/irstlm
export PATH=$PATH:$IRSTLM/bin

# Compile UNIGRAM models (train1, test1, dev1)
compile-lm lm_train1.ilm.gz --text=yes lm_train1.lm
compile-lm lm_train1.ilm.gz --text=yes /dev/stdout | grep -v unk |
gzip > lm_phone_ug_train.arpa.gz

compile-lm lm_test1.ilm.gz --text=yes lm_test1.lm
compile-lm lm_test1.ilm.gz --text=yes /dev/stdout | grep -v unk | 
gzip > lm_phone_ug_test.arpa.gz

compile-lm lm_dev1.ilm.gz --text=yes lm_dev1.lm
compile-lm lm_dev1.ilm.gz --text=yes /dev/stdout | grep -v unk |
gzip > lm_phone_ug_dev.arpa.gz

# Compile BIGRAM models (train2, test2, dev2)
compile-lm lm_train2.ilm.gz --text=yes lm_train2.lm
compile-lm lm_train2.ilm.gz --text=yes /dev/stdout | grep -v unk |
gzip > lm_phone_bg_train.arpa.gz

compile-lm lm_test2.ilm.gz --text=yes lm_test2.lm
compile-lm lm_test2.ilm.gz --text=yes /dev/stdout | grep -v unk |
gzip > lm_phone_bg_test.arpa.gz

compile-lm lm_dev2.ilm.gz --text=yes lm_dev2.lm
compile-lm lm_dev2.ilm.gz --text=yes /dev/stdout | grep -v unk |
gzip > lm_phone_bg_dev.arpa.gz