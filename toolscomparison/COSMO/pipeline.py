import shutil
import stat
import subprocess
import time
import zipfile
from pathlib import Path

from Bio.Data import CodonTable

from toolscomparison.helper import find_coding_location
from toolscomparison.calculate_cai import load_and_calculate_cai

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "files"
COSMO_DIR = Path(__file__).resolve().parent
COSMO_BINARY = COSMO_DIR / "cosmo0.9" / "cosmo"
COSMO_ZIP = COSMO_DIR / "cosmo0.9.zip"


def ensure_cosmo_binary():
    if COSMO_BINARY.exists():
        return
    if not COSMO_ZIP.exists():
        raise FileNotFoundError(
            f"COSMO binary not found at {COSMO_BINARY} and archive not found at {COSMO_ZIP}"
        )
    print(f"COSMO binary not found. Extracting {COSMO_ZIP}...")
    with zipfile.ZipFile(COSMO_ZIP) as zf:
        zf.extractall(COSMO_DIR)
    if not COSMO_BINARY.exists():
        raise FileNotFoundError(
            f"COSMO binary still missing after extracting {COSMO_ZIP}"
        )
    COSMO_BINARY.chmod(COSMO_BINARY.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Extracted COSMO binary to {COSMO_BINARY}.")


def run_cosmo(gene_dir, gene_name, pattern_file_name, codon_usage_file_name):
    ensure_cosmo_binary()

    output_dir = Path(f"./results/{gene_name}")
    sequence_file = DATA_DIR / gene_dir / f"{gene_name}.txt"
    pattern_file = DATA_DIR / gene_dir / f"{pattern_file_name}.txt"
    codon_file = DATA_DIR / gene_dir / f"{codon_usage_file_name}.txt"

    if output_dir.exists():
        shutil.rmtree(output_dir)
        print(f"Deleted {output_dir} before running COSMO.")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not sequence_file.exists():
        raise FileNotFoundError(f"Sequence file not found: {sequence_file}")
    if not pattern_file.exists():
        raise FileNotFoundError(f"Patterns file not found: {pattern_file}")
    if not codon_file.exists():
        raise FileNotFoundError(f"Codon usage file not found: {codon_file}")

    cosmo_codon_file = output_dir / f"{codon_usage_file_name}.cu"
    table = CodonTable.unambiguous_rna_by_name["Standard"]
    codon_to_aa = {codon: aa for codon, aa in table.forward_table.items()}
    for codon in table.stop_codons:
        codon_to_aa[codon] = "*"

    with codon_file.open() as f, cosmo_codon_file.open("w") as out:
        for line in f:
            if line.strip():
                codon, freq = line.strip().split("\t")
                aa = codon_to_aa[codon]
                dna_codon = codon.replace("U", "T")
                count = int(float(freq) * 100000)
                out.write(f"{aa} {dna_codon} {freq} {count}\n")

    codon_usage_table = {}
    with codon_file.open() as f:
        for line in f:
            if line.strip():
                codon, freq = line.strip().split("\t")
                codon_usage_table[codon.replace("U", "T")] = float(freq)
    print(f"Loaded {len(codon_usage_table)} codons.")

    patterns = "|".join(
        line.strip() for line in pattern_file.read_text().splitlines() if line.strip()
    )

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
    cds_sequence = original_sequence[coding_start:coding_end]

    cds_file = output_dir / f"{gene_name}_coding_regions.txt"
    cds_file.write_text(cds_sequence)

    command = [
        str(COSMO_BINARY),
        "-f", str(cds_file),
        "-t", str(cosmo_codon_file),
        "-of", "CAI",
        "-p", patterns,
        "-d",
    ]

    print("Running COSMO...")
    time_start = time.time()
    completed = subprocess.run(command, capture_output=True, text=True)
    time_end = time.time()

    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        raise RuntimeError(f"COSMO failed with exit code {completed.returncode}")

    print(completed.stdout)
    print(f"COSMO finished successfully in {time_end - time_start:.4f} seconds.")

    optimized_cds = None
    lines = completed.stdout.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("Solution="):
            optimized_cds = lines[i + 1].strip()
            break

    if optimized_cds is None:
        raise RuntimeError("Could not find optimized sequence in COSMO output")

    if len(optimized_cds) != len(cds_sequence):
        raise RuntimeError(
            f"Optimized CDS length {len(optimized_cds)} does not match "
            f"original CDS length {len(cds_sequence)}"
        )

    optimized_seq = (
        original_sequence[:coding_start]
        + optimized_cds
        + original_sequence[coding_end:]
    )

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

    pattern_hits = {p: optimized_cds.count(p) for p in patterns.split("|") if p}
    for pattern, count in pattern_hits.items():
        if count > 0:
            print(f"Pattern '{pattern}' occurs {count} time(s) in optimized coding region.")
    all_patterns_removed = all(count == 0 for count in pattern_hits.values())

    return {
        "cai": cai,
        "non_coding_substitutions": non_coding_changes,
        "all_patterns_removed": all_patterns_removed,
        "pattern_hits": pattern_hits,
    }
