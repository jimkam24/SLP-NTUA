. ./path.sh # Needed for KALDI_ROOT
. ./cmd.sh
#===============================Make the mfcc===========================================================================
#Make MFCC features. mfcc_i where i = {train,test,dev} should be some place with a largish disk where you
#want to store MFCC features. nj number of parallel jobs - 1 is perfect for such a small data set
for x in train test dev; do
    steps/make_mfcc.sh  --mfcc-config conf/mfcc.conf --cmd "$train_cmd" --nj 4 \
    data/$x exp/make_mfcc/$x mfcc_${x} || exit 1;
    steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x mfcc || exit 1;
done
