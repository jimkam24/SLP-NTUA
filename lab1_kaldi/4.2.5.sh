#!/bin/bash

# Load Kaldi path variables
source path.sh

# Set base data directory
DATA_DIR="~/Desktop/kaldi/egs/slp_lab/data"

# Process folders: train, dev, test
for split in train dev test; do
    SPLIT_DIR="$DATA_DIR/$split"

    if [ -d "$SPLIT_DIR" ]; then
        echo "Processing: $SPLIT_DIR"

        for file in wav.scp text utt2spk; do
            FILE_PATH="$SPLIT_DIR/$file"
            if [ -f "$FILE_PATH" ]; then
                sort "$FILE_PATH" -o "$FILE_PATH"
            else
                echo "  Warning: $file not found in $split"
            fi
        done

    else
        echo "Skipping missing directory: $SPLIT_DIR"
    fi
done

echo "File sorting finished."