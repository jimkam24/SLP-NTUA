  #!/bin/bash
    source path.sh
    
#Define path to the original file and the destination folder
SOURCE_SCORE_SCRIPT=~/Desktop/kaldi/egs/wsj/s5/steps/score_kaldi.sh
DEST_DIR=local
LINKED_SCORE_SCRIPT=score_kaldi.sh

# Create the destination folder if it doesn't exist
if [ ! -d "$DEST_DIR" ]; then
    mkdir -p "$DEST_DIR"
    echo "Destination folder '$DEST_DIR' created."
fi

# Check if the source file exists
if [ ! -f "$SOURCE_SCORE_SCRIPT" ]; then
    echo "Error: Source file '$SOURCE_SCORE_SCRIPT' does not exist."
    exit 1
fi

# Create the symbolic link
ln -s "$SOURCE_SCORE_SCRIPT" "$DEST_DIR/$LINKED_SCORE_SCRIPT"

# Verify and print success message
if [ -L "$DEST_DIR/$LINKED_SCORE_SCRIPT" ]; then
    echo "Symbolic link '$LINKED_SCORE_SCRIPT' created in 
    '$DEST_DIR' -> $SOURCE_SCORE_SCRIPT"
else
    echo "Error: Failed to create symbolic link."
    exit 1
fi
