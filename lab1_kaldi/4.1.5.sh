#!/bin/bash
source path.sh

# List of folders to create
FOLDERS_TO_CREATE=("data/lang" "data/local/dict" "data/local/lm_tmp" 
"data/local/nist_lm")

# Loop through each folder and create if it doesn't exist
for folder in "${FOLDERS_TO_CREATE[@]}"; do
    if [ ! -d "$folder" ]; then
    mkdir -p "$folder"
    echo "Created directory: $folder"
    else
    echo "Directory already exists: $folder"
    fi
done