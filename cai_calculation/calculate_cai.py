import numpy as np
from Bio.Data import CodonTable

genetic_code = CodonTable.ambiguous_dna_by_id[1]

def translate_codon(codon):
    if codon in genetic_code.stop_codons:
        return "*"
    return genetic_code.forward_table.get(codon)

def load_and_normalize_weights(codon_usage_table):
    """Load codon frequencies from DNA Chisel and normalize them into
    relative adaptiveness weights (w = f / max(f_synonymous))."""

    try:
        raw_freqs = {}

        for codon, freq in codon_usage_table.items():
            raw_freqs[codon.upper().replace("U", "T")] = freq

        # Group frequencies by amino acid
        aa_groups: dict[str, list[float]] = {}
        for codon, freq in raw_freqs.items():
            aa = translate_codon(codon)
            if aa:
                aa_groups.setdefault(aa, []).append(freq)

        print(f"aa_groups = {aa_groups}")

        # Normalize
        normalized_weights: dict[str, float] = {}
        for codon, freq in raw_freqs.items():
            aa = translate_codon(codon)
            if aa:
                max_freq = max(aa_groups[aa])
                normalized_weights[codon] = (
                    freq / max_freq if max_freq > 0 else 0.0
                )
            else:
                normalized_weights[codon] = 0.0

        print(f"Normalized {len(normalized_weights)} codons..")
        print(f"normalized_weights = {normalized_weights}")
        return normalized_weights

    except Exception as e:
        print(f"Failed to load/normalize codon usage table: {e}")
        return None

def calculate_cai(sequence: str, weights: dict[str, float]):
    seq_str = sequence.upper().replace("U", "T")
    codons = [seq_str[i : i + 3] for i in range(0, len(seq_str) - 2, 3)]

    sum_log_w: float = 0.0
    count: int = 0

    for codon in codons:
        if (w := weights.get(codon)) is not None:
            # Use 0.01 as a floor for very rare codons to avoid log(0)
            sum_log_w += np.log(w)
            count += 1

    print(f"count = {count}, sum_log_w = {sum_log_w}")
    return np.exp(sum_log_w / count) if count > 0 else 0.0

def load_and_calculate_cai(sequence, codon_usage_table):
    weights = load_and_normalize_weights(codon_usage_table)
    if not weights:
        return

    cai_val: float = calculate_cai(sequence, weights)
    print(f"CAI =  {cai_val:.4f}")
