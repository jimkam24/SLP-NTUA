#!/bin/bash
source ./path.sh

# Print PER - dev unigram
echo "Best WER for dev unigram"
[ -d exp/mono0a/decode_dev_ug ] && grep WER exp/mono0a/decode_dev_ug/wer_* | utils/best_wer.sh

echo "Best WER for test unigram"
# Print PER - test unigram
[ -d exp/mono0a/decode_test_ug ] && grep WER exp/mono0a/decode_test_ug/wer_* | utils/best_wer.sh

echo "Best WER for dev bigram"
# Print PER - dev bigram
[ -d exp/mono0a/decode_dev_bg ] && grep WER exp/mono0a/decode_dev_bg/wer_* | utils/best_wer.sh

echo "Best WER for dev bigram"
# Print PER.
[ -d exp/mono0a/decode_test_bg ] && grep WER exp/mono0a/decode_test_bg/wer_* | utils/best_wer.sh


