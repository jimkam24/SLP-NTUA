input_file = "text"
output_file = "output.txt"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # Skip any empty lines

        tokens = line.split()
        sentence_id = tokens[0]         # e.g., f1_003
        sentence_tokens = tokens[1:]    # e.g., ['sil', 'sh', 'iy', ...]

        # Construct the new sentence with <s> and </s>
        new_sentence = f"{sentence_id} <s> {' '.join(sentence_tokens)} </s>"

        outfile.write(new_sentence + "\n")

print(f"Created '{output_file}' with <s> and </s> around each sentence.")