import shutil
import time
from pathlib import Path

from dnachisel import (
    AvoidPattern,
    DnaOptimizationProblem,
    EnforceTranslation,
    MaximizeCAI,
    AvoidChanges
)

from toolscomparison.helper import find_coding_location
from toolscomparison.calculate_cai import load_and_calculate_cai

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "files"


def run_dnachisel(gene_dir, gene_name, pattern_file_name, codon_usage_file_name, species):
    output_dir = Path(f"./results/{gene_name}")
    sequence_file = DATA_DIR / gene_dir / f"{gene_name}.txt"
    pattern_file = DATA_DIR / gene_dir / f"{pattern_file_name}.txt"
    codon_file = DATA_DIR / gene_dir / f"{codon_usage_file_name}.txt"

    if output_dir.exists():
        shutil.rmtree(output_dir)
        print(f"Deleted {output_dir} before running DNAChisel.")

    if not sequence_file.exists():
        raise FileNotFoundError(f"Sequence file not found: {sequence_file}")
    sequence = sequence_file.read_text().strip()

    if not pattern_file.exists():
        raise FileNotFoundError(f"Patterns file not found: {pattern_file}")
    unwanted_patterns = pattern_file.read_text().split("\n")

    result = find_coding_location(sequence)
    if result is None:
        raise RuntimeError(f"{gene_name} coding region was not found")
    coding_start, coding_end = result
    print(
        f"{gene_name} coding region found at positions "
        f"{coding_start}-{coding_end}"
    )

    original_sequence = sequence.replace("*", "")

    problem = DnaOptimizationProblem(
        sequence=original_sequence,
        constraints=[
            *[AvoidPattern(pattern) for pattern in unwanted_patterns],
            EnforceTranslation(location=(coding_start, coding_end)),
        ],
        objectives=[
            MaximizeCAI(
                species=species,
                location=(coding_start, coding_end),
            ),
            AvoidChanges(
                location=(0, coding_start),
            ),
            AvoidChanges(
                location=(coding_end, len(original_sequence)),
            ),
        ],
    )

    print("Running DNAChisel...")
    time_start = time.time()
    try:
        problem.resolve_constraints()
        problem.optimize()
    except SystemExit as e:
        if e.code not in (0, None):
            raise RuntimeError(f"DNAChisel failed with exit code {e.code}")
    time_end = time.time()

    print(problem.constraints_text_summary())
    print(problem.objectives_text_summary())
    print(f"DNAChisel finished successfully in {time_end - time_start:.4f} seconds.")

    optimized_seq = problem.sequence
    if not optimized_seq:
        return

    print("Optimized sequence length:", len(optimized_seq))
    print("Optimized sequence:")
    print(optimized_seq)
    print("Optimized sequence in coding region:")
    print(optimized_seq[coding_start:coding_end])

    if not codon_file.exists():
        raise FileNotFoundError(f"Codon usage file not found: {codon_file}")
    codon_usage_table = {}
    with codon_file.open() as f:
        for line in f:
            if line.strip():
                codon, freq = line.strip().split("\t")
                codon_usage_table[codon.replace("U", "T")] = float(freq)
    print(f"Loaded {len(codon_usage_table)} codons.")

    load_and_calculate_cai(
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