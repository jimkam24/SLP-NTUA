input_filename = "uttids"  
output_filename = "wav.scp"

# Read the input file
with open(input_filename, "r") as infile:
    lines = infile.readlines()

# Process each line
with open(output_filename, "w") as outfile:
    for line in lines:
        line = line.strip()  # Remove any surrounding whitespace
        if line:  # Ensure the line is not empty
            prefix = line[:2]  # Extract first two letters
            path = f"/home/angeliki/Desktop/kaldi/egs/usc/wav/{line}.wav"
            outfile.write(f"{line} {path}\n")

print(f"Processed data has been saved to {output_filename}")
