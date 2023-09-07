from utils.amono_acid_utils import AminoAcidScheme
from settings.costs_settings import s_coding_region, o_coding_region, w_coding_region, x_coding_region
from settings.costs_settings import s_non_coding_region, o_non_coding_region, w_non_coding_region, x_non_coding_region

class CodonScorer:
    def __init__(self):
        """
        Initializes a CodonScorer object with a codon scoring scheme.

        Parameters:
            coding_region_scheme (list of dict): List of dictionaries representing codon scoring information for coding regions
            non_coding_region_scheme (list of dict): List of dictionaries representing codon scoring information for non coding regions
        """
        self.coding_region_scheme = AminoAcidScheme(w_coding_region, o_coding_region, s_coding_region, x_coding_region).get_cost_table()
        self.non_coding_region_scheme = AminoAcidScheme(w_non_coding_region, o_non_coding_region, s_non_coding_region, x_non_coding_region).get_cost_table()

    def get_codon_scores(self, codon, codon_scores):
        """
        Retrieves the scoring information for a given codon.

        Parameters:
            codon (str): Codon sequence for which scoring information is needed.

        Returns:
            list or None: List of scoring information for the codon, or None if codon is not found.
        """
        for amino_acid_dict in codon_scores:
            for codon_key, scoring_dicts in amino_acid_dict.items():
                # print(f"codon_key = {codon_key}")
                # print(f"scoring_dicts = {scoring_dicts}")
                if codon_key == codon:
                    return scoring_dicts
        return None  # Codon not found

    def calculate_scores(self, sequences):
        """
        Calculates scores for each codon in a list of sequences using the provided scoring schemes based on 'is_coding_region'.

        Parameters:
            sequences (list of dict): List of dictionaries, each containing a 'seq' key and an 'is_coding_region' key.

        Returns:
            list: List of scores for each codon in the sequences.
        """
        scores_array = []  # To store scores for each codon

        for seq_info in sequences:
            sequence = seq_info['seq']
            is_coding_region = seq_info['is_coding_region']

            if is_coding_region:
                codon_scores = self.coding_region_scheme
            else:
                codon_scores = self.non_coding_region_scheme

            for i in range(0, len(sequence), 3):
                codon = sequence[i:i + 3]
                score = self.get_codon_scores(codon, codon_scores)
                if score:
                    scores_array = scores_array + score
                else:
                    print(f"Warning: Codon {codon} not found in the scoring scheme.")

        return scores_array


