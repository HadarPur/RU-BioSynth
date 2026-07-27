import numpy as np
from Bio.Data import CodonTable

def load_and_normalize_weights(codon_usage_table):
    """Load codon frequencies from DNA Chisel and normalize them into
    relative adaptiveness weights (w = f / max(f_synonymous))."""

    genetic_code = CodonTable.ambiguous_dna_by_id[1].forward_table

    try:
        raw_freqs = {}

        for codon, freq in codon_usage_table.items():
            raw_freqs[codon.upper().replace("U", "T")] = freq

        # Group frequencies by amino acid
        aa_groups: dict[str, list[float]] = {}
        for codon, freq in raw_freqs.items():
            aa = genetic_code.get(codon)
            if aa:
                aa_groups.setdefault(aa, []).append(freq)

        # Normalize
        normalized_weights: dict[str, float] = {}
        for codon, freq in raw_freqs.items():
            aa = genetic_code.get(codon)
            if aa:
                max_freq = max(aa_groups[aa])
                normalized_weights[codon] = (
                    freq / max_freq if max_freq > 0 else 0.0
                )
            else:
                normalized_weights[codon] = 0.0

        print(
            f"Normalized {len(normalized_weights)} codons.."
        )
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
            val = max(w, 0.01)
            sum_log_w += np.log(val)
            count += 1

    return np.exp(sum_log_w / count) if count > 0 else 0.0


def load_and_calculate_cai(sequence, codon_usage_table):
    weights = load_and_normalize_weights(codon_usage_table)
    if not weights:
        return

    cai_val: float = calculate_cai(sequence, weights)
    print(f"CAI =  {cai_val:.4f}")
