import re

input_filename = "text"  # dsFile with sentences
lexicon_filename = "lexicon.txt"  # Lexicon mapping words to phonemes
output_filename = "text"

# Load lexicon into a dictionary
lexicon = {}
with open(lexicon_filename, "r") as lex_file:
    for line in lex_file:
        parts = line.strip().split()
        if len(parts) > 1:
            word = parts[0].lower()
            phonemes = " ".join(parts[1:])
            lexicon[word] = phonemes

# Function to convert text to phonemes
def text_to_phonemes(sentence):
    sentence = sentence.lower()  # Convert to lowercase
    # Remove punctuation except single quotes
    sentence = re.sub(r"[^a-z0-9' ]", "", sentence)  
    words = sentence.split()
    # Replace words with phonemes
    phoneme_sentence = [lexicon.get(word, word) for word in words]  
    # Add silence phoneme at start & end
    return "sil " + " ".join(phoneme_sentence) + " sil"  

# Process input file
with open(input_filename,"r") as infile, open(output_filename, "w") as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        
        parts = line.split(" ", 1)  # Split speaker ID and sentence
        if len(parts) == 2:
            speaker_id, sentence = parts
            phoneme_sentence = text_to_phonemes(sentence)
            outfile.write(f"{speaker_id} {phoneme_sentence}\n")
        else:
            outfile.write(f"{line}\n")  # If no sentence, keep the line as is

print(f"Processed data has been saved to {output_filename}")