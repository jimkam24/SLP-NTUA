# Source Kaldi environment and command configuration
source ./path.sh      # Initializes KALDI_ROOT and related paths
source ./cmd.sh       # Loads command setup (e.g., for queueing)

# Set up IRSTLM tool path and update system PATH
export IRSTLM="$KALDI_ROOT/tools/irstlm"
export PATH="$PATH:$IRSTLM/bin"

# Prepare language data using dictionary and placeholder for OOV
./utils/prepare_lang.sh data/local/dict "<oov>" data/local/lm_tmp data/lang
