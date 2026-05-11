#!/bin/bash
# Load Kaldi environment variables
source path.sh
# List of dataset splits
SETS=("train" "test" "dev")

# Generate spk2utt from utt2spk for each dataset
for split in "${SETS[@]}"; do
    INPUT_FILE="data/$split/utt2spk"
    OUTPUT_FILE="data/$split/spk2utt"

    if [ -f "$INPUT_FILE" ]; then
        utils/utt2spk_to_spk2utt.pl < "$INPUT_FILE" > "$OUTPUT_FILE"
        echo "Created spk2utt for: $split"
    else
        echo "Missing utt2spk in $split — skipping"
    fi
done