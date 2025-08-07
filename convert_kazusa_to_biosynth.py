#!/usr/bin/env python3

import argparse
import os


def extract_codons(input_path, output_path=None):
    codon_count = 0

    # If no output path given, use default in the same directory as input
    if output_path is None:
        input_dir = os.path.dirname(input_path)
        output_path = os.path.join(input_dir, "biosynth_codon_usage.txt")

    with open(input_path, "r") as infile:
        raw = infile.read()

    entries = raw.strip().split(")")

    with open(output_path, "w") as outfile:
        for entry in entries:
            if not entry.strip():
                continue  # skip empty chunks
            parts = entry.strip().split()

            # Ensure valid structure: CODON AA rel abs (count)
            if len(parts) >= 5:
                codon = parts[0]
                rel_freq = parts[2]
                outfile.write(f"{codon}\t{rel_freq}\n")
                codon_count += 1
            else:
                print(f"❗ Skipped malformed entry: {entry.strip()}")

    if codon_count == 64:
        print(f"✅ Success: 64 codons written to {output_path}")
    else:
        print(f"⚠️ Warning: Only {codon_count} codons written to {output_path} (expected 64)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Kazusa codon usage table to BioSynth format.")
    parser.add_argument("input_file", help="Path to the input codon usage file from Kazusa")
    parser.add_argument(
        "-o", "--output_file",
        help="Optional path/name for the output file (default: biosynth_codon_usage.txt in input directory)",
        default=None
    )

    args = parser.parse_args()
    extract_codons(args.input_file, args.output_file)
