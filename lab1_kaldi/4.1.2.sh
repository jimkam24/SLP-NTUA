#!/bin/bash
    
source path.sh

# Define the target directories
TARGET_STEPS_DIR=~/Desktop/kaldi/egs/wsj/s5/steps
TARGET_UTILS_DIR=~/Desktop/kaldi/egs/wsj/s5/utils

# Define the symlink names
STEPS_LINK_NAME=steps
UTILS_LINK_NAME=utils

# Check if the symlink already exists
if [ -L "$STEPS_LINK_NAME" ]; then
    echo "Symbolic link '$STEPS_LINK_NAME' already exists."
else
# Check for the target directory 
if [ ! -d "$TARGET_STEPS_DIR" ]; then
    echo "Error: Target directory '$TARGET_STEPS_DIR' does not exist."
    exit 1
fi
#Symbolic link for steps
    ln -s "$TARGET_STEPS_DIR" "$STEPS_LINK_NAME"
    echo "Symbolic link '$STEPS_LINK_NAME' created -> $TARGET_STEPS_DIR"
fi

# Check if the symlink already exists
if [ -L "$UTILS_LINK_NAME" ]; then
    echo "Symbolic link '$UTILS_LINK_NAME' already exists."
else
# Check for the target directory 
if [ ! -d "$TARGET_UTILS_DIR" ]; then
    echo "Error: Target directory '$TARGET_UTILS_DIR' does not exist."
    exit 1
fi
#Symbolic link for utils
    ln -s "$TARGET_UTILS_DIR" "$UTILS_LINK_NAME"
    echo "Symbolic link '$UTILS_LINK_NAME' created  -> $TARGET_UTILS_DIR"
fi
