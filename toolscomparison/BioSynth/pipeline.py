import shutil
import sys
import time
from pathlib import Path

from biosynth.BioSynth import BioSynthApp

from toolscomparison.helper import find_coding_location
from toolscomparison.calculate_cai import load_and_calculate_cai

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "files"


def run_biosynth(gene_dir, gene_name, pattern_file_name, codon_usage_file_name):
    output_dir = Path(f"./results/{gene_name}")
    sequence_file = DATA_DIR / gene_dir / f"{gene_name}.txt"
    pattern_file = DATA_DIR / gene_dir / f"{pattern_file_name}.txt"
    codon_file = DATA_DIR / gene_dir / f"{codon_usage_file_name}.txt"

    if output_dir.exists():
        shutil.rmtree(output_dir)
        print(f"Deleted {output_dir} before running BioSynth.")

    if not sequence_file.exists():
        raise FileNotFoundError(f"Sequence file not found: {sequence_file}")
    if not pattern_file.exists():
        raise FileNotFoundError(f"Patterns file not found: {pattern_file}")
    if not codon_file.exists():
        raise FileNotFoundError(f"Codon usage file not found: {codon_file}")

    sys.argv = [
        "biosynth",
        "-s", str(sequence_file),
        "-p", str(pattern_file),
        "-c", str(codon_file),
        "-o", str(output_dir),
    ]

    print("Running BioSynth...")
    time_start = time.time()
    try:
        BioSynthApp.execute(sys.argv[1:])
    except SystemExit as e:
        if e.code not in (0, None):
            raise RuntimeError(f"BioSynth failed with exit code {e.code}")
    time_end = time.time()
    print(f"BioSynth finished successfully in {time_end - time_start:.4f} seconds.")

    codon_usage_table = {}
    with codon_file.open() as f:
        for line in f:
            if line.strip():
                codon, freq = line.strip().split("\t")
                codon_usage_table[codon.replace("U", "T")] = float(freq)
    print(f"Loaded {len(codon_usage_table)} codons.")

    sequence = sequence_file.read_text().strip()
    result = find_coding_location(sequence)
    if result is None:
        raise RuntimeError(f"{gene_name} coding region was not found")
    coding_start, coding_end = result
    print(
        f"{gene_name} coding region found at positions "
        f"{coding_start}-{coding_end}"
    )

    original_sequence = sequence.replace("*", "")

    optimized_dir = output_dir / "BioSynth-Outputs"
    optimized_files = list(optimized_dir.glob("Optimized-Sequence*.txt"))
    if not optimized_files:
        raise FileNotFoundError(
            f"No optimized sequence file found in {optimized_dir}"
        )
    optimized_file = optimized_files[0]
    with optimized_file.open() as f:
        optimized_seq = f.readline().strip()

    print("Optimized sequence file:", optimized_file)
    print("Optimized sequence length:", len(optimized_seq))
    print("Optimized sequence:")
    print(optimized_seq)
    print("Optimized sequence in coding region:")
    print(optimized_seq[coding_start:coding_end])

    cai = load_and_calculate_cai(
        optimized_seq[coding_start:coding_end],
        codon_usage_table,
    )

    assert len(original_sequence) == len(optimized_seq)
    five_utr_changes = sum(
        a != b
        for a, b in zip(
            original_sequence[:coding_start], optimized_seq[:coding_start]
        )
    )
    three_utr_changes = sum(
        a != b
        for a, b in zip(
            original_sequence[coding_end:], optimized_seq[coding_end:]
        )
    )
    non_coding_changes = five_utr_changes + three_utr_changes
    print(f"5' UTR substitutions: {five_utr_changes}")
    print(f"3' UTR substitutions: {three_utr_changes}")
    print(f"Non-coding substitutions: {non_coding_changes}")

    unwanted_patterns = [
        p.strip() for p in pattern_file.read_text().splitlines() if p.strip()
    ]
    pattern_hits = {p: optimized_seq.count(p) for p in unwanted_patterns}
    all_patterns_removed = all(count == 0 for count in pattern_hits.values())

    return {
        "cai": cai,
        "non_coding_substitutions": non_coding_changes,
        "all_patterns_removed": all_patterns_removed,
        "pattern_hits": pattern_hits,
    }