from Bio.Seq import Seq
import random


class DNAHighlighter:
    def __init__(self, seq):
        """
        Initializes a DNAHighlighter object with a DNA sequence.

        Parameters:
            seq (str): DNA sequence as a string.
        """
        self.seq = seq

    def highlight_coding_regions(self, coding_regions):
        """
        Highlights coding regions within the DNA sequence using colored escape codes.

        Parameters:
            coding_regions (list of Seq): List of coding regions (Seq objects) to be highlighted.

        Returns:
            str: DNA sequence with highlighted coding regions using escape codes.
        """
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
        """
        Identifies and returns coding regions within the DNA sequence.

        Returns:
            list of Seq: List of coding regions (Seq objects) found in the DNA sequence.
        """
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
        """
        Initializes a CodonScorer object with a codon scoring scheme.

        Parameters:
            C (list of dict): List of dictionaries representing codon scoring information.
        """
        self.C = C

    def get_codon_scores(self, codon):
        """
        Retrieves the scoring information for a given codon.

        Parameters:
            codon (str): Codon sequence for which scoring information is needed.

        Returns:
            list or None: List of scoring information for the codon, or None if codon is not found.
        """
        for amino_acid_dict in self.C:
            for codon_key, scoring_dicts in amino_acid_dict.items():
                if codon_key == codon:
                    return scoring_dicts
        return None  # Codon not found

    def calculate_scores(self, sequence):
        """
        Calculates scores for each codon in a given sequence using the provided scoring scheme.

        Parameters:
            sequence (str): DNA sequence for which codon scores are to be calculated.

        Returns:
            list: List of scores for each codon in the sequence.
        """
        scores_array = []  # To store scores for each codon

        for i in range(0, len(sequence), 3):
            codon = sequence[i:i + 3]
            codon_scores = self.get_codon_scores(codon)
            if codon_scores:
                scores_array = scores_array + codon_scores
            else:
                print(f"Warning: Codon {codon} not found in the scoring scheme.")

        return scores_array
