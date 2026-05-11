input_filename = "uttids"
output_filename = "utt2spk"

with open(input_filename, "r") as infile:
    lines = infile.readlines()

with open(output_filename, "w") as outfile:
    for line in lines:
        line = line.strip()
        if line:
            prefix = line[:2]
            outfile.write(f"{line} {prefix}\n")

print(f"Processed data has been saved to {output_filename}")