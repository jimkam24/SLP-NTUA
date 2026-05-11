input_filename = "uttids"  # First input file with IDs
# Second input file with IDs and sentences
sentence_filename = "transcriptions.txt"  
output_filename = "text"

# Read the sentence mapping from the second file
from collections import defaultdict

sentence_dict = defaultdict(list)
with open(sentence_filename, "r") as sentence_file:
    for line in sentence_file:
        parts = line.strip().split("\t", 1)  # Split at tab character
        if len(parts) == 2:
            # Store sentences for all IDs
            sentence_dict[parts[0].strip()].append(parts[1].strip())  

# Read the first input file
with open(input_filename, "r") as infile:
    lines = infile.readlines()

# Process each line
with open(output_filename, "w") as outfile:
    for line in lines:
        line = line.strip()  # Remove any surrounding whitespace
        if line:  # Ensure the line is not empty
            prefix = line.split("_")[0]  # Extract prefix before underscore
            path = f"/home/angeliki/Desktop/kaldi/egs/usc/wav/{line}.wav"
            
            # Find sentences for the exact ID, or 
            #if unavailable, try a more general match (e.g., f1_003 -> 003)
            sentences = sentence_dict.get(line,
            sentence_dict.get(line.split("_")[1], ["No sentence found"]))
            
            outfile.write(f"{line}  {' | '.join(sentences)}\n")

print(f"Processed data has been saved to {output_filename}")