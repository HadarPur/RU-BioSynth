from Bio.Seq import Seq
import random


class DNAHighlighter:
    def __init__(self, seq):
        self.seq = seq

    def highlight_coding_regions(self, coding_regions):
        available_color_codes = [code for code in range(91, 98) if code not in [93, 97]]
        region_color_mapping = {}

        for region_seq in coding_regions:
            if not available_color_codes:
                break
            color_code = random.choice(available_color_codes)
            available_color_codes.remove(color_code)
            region_color_mapping[str(region_seq)] = f'\033[{color_code}m'

        highlighted_seq = str(self.seq)

        for region_seq in coding_regions:
            region_str = str(region_seq)
            region_start = highlighted_seq.find(region_str)

            while region_start >= 0:
                region_end = region_start + len(region_str)
                color_code = region_color_mapping[region_str]

                highlighted_seq = (
                    highlighted_seq[:region_start] +
                    color_code + highlighted_seq[region_start:region_end] + '\033[0m' +
                    highlighted_seq[region_end:]
                )

                region_start = highlighted_seq.find(region_str, region_end)

        return highlighted_seq

    def get_coding_regions(self):
        dna_seq = Seq(self.seq)
        start_codon = Seq("ATG")
        stop_codons = [Seq("TAA"), Seq("TAG"), Seq("TGA")]
        coding_regions = []
        i = 0

        while i < len(dna_seq):
            if dna_seq[i:i + 3] == start_codon:
                start_idx = i
                in_coding_region = True
                for j in range(i + 3, len(dna_seq), 3):
                    if dna_seq[j:j + 3] in stop_codons:
                        coding_regions.append(dna_seq[start_idx:j + 3])
                        i = j + 3
                        in_coding_region = False
                        break
                if in_coding_region:
                    i += 3
            else:
                i += 1

        return coding_regions


class CodonScorer:
    def __init__(self, C):
        self.C = C

    def get_codon_scores(self, codon):
        for amino_acid_dict in self.C:
            for codon_key, scoring_dicts in amino_acid_dict.items():
                if codon_key == codon:
                    return scoring_dicts
        return None  # Codon not found

    def calculate_scores(self, sequence):
        scores_array = []  # To store scores for each codon

        for i in range(0, len(sequence), 3):
            codon = sequence[i:i + 3]
            codon_scores = self.get_codon_scores(codon)
            if codon_scores is not None:
                scores_array = scores_array + codon_scores
            else:
                print(f"Warning: Codon {codon} not found in the scoring scheme.")

        return scores_array
