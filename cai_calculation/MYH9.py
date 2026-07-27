import sys
import shutil
from pathlib import Path

from biosynth.BioSynth import BioSynthApp
from helper import find_coding_location
from calculate_cai import load_and_calculate_cai

# -------------------------------
# Define paths
# -------------------------------

output_dir = Path("./results/MYH9")

sequence_file = Path("../files/cloning_example/OQ689691.1.txt")
pattern_file = Path("../files/cloning_example/mcs_unwanted_patterns.txt")
codon_file = Path("../files/cloning_example/codon_usage_ecoli.txt")


# -------------------------------
# Remove previous results
# -------------------------------

if output_dir.exists():
    shutil.rmtree(output_dir)
    print(f"Deleted {output_dir} before running BioSynth.")


# -------------------------------
# Run BioSynth
# -------------------------------

sys.argv = [
    "biosynth",
    "-s", str(sequence_file),
    "-p", str(pattern_file),
    "-c", str(codon_file),
    "-o", str(output_dir)
]

print("Running BioSynth...")

try:
    BioSynthApp.execute(sys.argv[1:])
except SystemExit as e:
    # Allows the script to continue if BioSynth calls sys.exit()
    if e.code not in (0, None):
        raise RuntimeError(f"BioSynth failed with exit code {e.code}")

print("BioSynth finished successfully.")


# -------------------------------
# Load codon usage table
# -------------------------------

codon_usage_table = {}

if not codon_file.exists():
    raise FileNotFoundError(f"Codon usage file not found: {codon_file}")

with codon_file.open() as f:
    for line in f:
        if line.strip():
            codon, freq = line.strip().split("\t")
            codon_usage_table[codon.replace("U", "T")] = float(freq)

print(f"Loaded {len(codon_usage_table)} codons.")


# -------------------------------
# Find coding location
# -------------------------------

if not sequence_file.exists():
    raise FileNotFoundError(f"Sequence file not found: {sequence_file}")

with sequence_file.open("r") as file:
    cloning_sequence = file.read().strip()

location = find_coding_location(cloning_sequence)

if location:
    print(
        f"OQ689691.1 coding region found at positions "
        f"{location[0]}-{location[1]}"
    )
else:
    print("OQ689691.1 coding region was not found")


# -------------------------------
# Extract optimized sequence
# -------------------------------

optimized_dir = output_dir / "BioSynth-Outputs"

optimized_files = list(
    optimized_dir.glob("Optimized-Sequence*.txt")
)

if not optimized_files:
    raise FileNotFoundError(
        f"No optimized sequence file found in {optimized_dir}"
    )

optimized_file = optimized_files[0]

with optimized_file.open() as f:
    optimized_seq = f.readline().strip()


# -------------------------------
# Print results
# -------------------------------

print("Optimized sequence file:", optimized_file)
print("Optimized sequence length:", len(optimized_seq))
print("Optimized sequence:")
print(optimized_seq)

# -------------------------------
# Calculate CAI
# -------------------------------

load_and_calculate_cai(
    optimized_seq[location[0]:location[1]],
    codon_usage_table
)

