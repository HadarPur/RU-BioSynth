import math
from biosynth.utils.logger import Logger


def calculate_cai(sequence: str, coding_indexes: tuple[int, int], weights: dict[str, float]) -> float:
    seq_str = sequence[coding_indexes[0]:coding_indexes[1]].upper().replace("U", "T")
    codons = [seq_str[i : i + 3] for i in range(0, len(seq_str) - 2, 3)]

    sum_log_w: float = 0.0
    count: int = 0

    for codon in codons:
        if (w := weights.get(codon)) is not None:
            # Use 0.01 as a floor for very rare codons to avoid log(0)
            val = max(w, 0.01)
            sum_log_w += math.log(val)
            count += 1

    return math.exp(sum_log_w / count) if count > 0 else 0.0
