#!/usr/bin/env python3

import os

def extract_codons(input_path):
    codon_count = 0

    # Construct output path in the same directory as input file
    input_dir = os.path.dirname(input_path)
    output_path = os.path.join(input_dir, "biosynth_codon_usage.txt")

    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            tokens = line.strip().split()
            for i in range(0, len(tokens), 6):
                if i + 2 < len(tokens):
                    codon = tokens[i]
                    freq = tokens[i + 2]
                    outfile.write(f"{codon}\t{freq}\n")
                    codon_count += 1

    if codon_count == 64:
        print(f"✅ Success: 64 codons written to {output_path}")
    else:
        print(f"⚠️ Warning: Only {codon_count} codons written to {output_path} (expected 64)")

if __name__ == "__main__":
    input_path = input("Enter the path to your input file: ").strip()
    extract_codons(input_path)
