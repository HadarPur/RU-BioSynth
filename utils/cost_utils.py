from settings.costs_settings import o_non_coding_region, w_non_coding_region, x_non_coding_region
from settings.costs_settings import s_coding_region, o_coding_region, w_coding_region, x_coding_region
from utils.amino_acid_utils import AminoAcidConfigScheme
from utils.output_utils import Logger


# Define a class called CodonScorer
def get_codon_scores(codon, codon_scores):
    """
    Retrieves the scoring information for a given codon.

    Parameters:
        codon (str): Codon sequence for which scoring information is needed.

    Returns:
        list or None: List of scoring information for the codon, or None if codon is not found.
        :param codon:
        :param codon_scores:
    """
    # Iterate through codon scores
    for amino_acid_dict in codon_scores:
        for codon_key, scoring_dicts in amino_acid_dict.items():
            if codon_key == codon:
                return scoring_dicts
    return None  # Codon not found


class CodonScorerFactory:
    def __init__(self):
        """
        Initializes a CodonScorer object with a codon scoring scheme.
        """

        # Initialize the object with codon scoring schemes for coding and non-coding regions
        self.coding_region_scheme = AminoAcidConfigScheme(w_coding_region, o_coding_region, x_coding_region,
                                                          s_coding_region).get_cost_table_coding_region()
        self.non_coding_region_scheme = AminoAcidConfigScheme(w_non_coding_region, o_non_coding_region,
                                                              x_non_coding_region).get_cost_table_non_coding_region()

    def calculate_scores(self, seq, codon_positions):
        """
        Calculates scores for each codon in coding regions and each base in non-coding regions.

        Parameters:
            seq (str): The DNA sequence to analyze.
            codon_positions (list): Precomputed array where each index contains 0 for non-coding or 1, 2, 3 for coding positions.

        Returns:
            list: List of scores for each codon or base in the sequence.
        """

        scores_array = []
        i = 0

        while i < len(seq):
            if codon_positions[i] != 0:
                # Start of a coding region (process codons)
                start = i
                while i < len(seq) and codon_positions[i] != 0:
                    i += 1
                end = i

                # Process codons within this coding region
                for j in range(start, end, 3):
                    codon = seq[j:j + 3]
                    if len(codon) == 3:  # Ensure codon is complete
                        score = get_codon_scores(codon, self.coding_region_scheme)
                        if score:
                            scores_array += score
                        else:
                            Logger.warning(
                                f"Codon {codon} at positions {j}-{j + 2} not found in the coding scoring scheme.")
            else:
                # Non-coding region (process bases)
                base = seq[i]
                score = get_codon_scores(base, self.non_coding_region_scheme)
                if score:
                    scores_array += score
                else:
                    Logger.warning(f"Base {base} at position {i} not found in the non-coding scoring scheme.")
                i += 1

        return scores_array


class EliminationScorerConfig:
    def __init__(self):
        """
        Initializes a DNASequenceAnalyzer object.
        Sets up the DNA alphabet containing the characters 'A', 'G', 'T', and 'C'.
        """
        self.alphabet = {'A', 'G', 'T', 'C'}

    @staticmethod
    def cost_function(C):
        """
        Creates a cost function based on the given cost matrix C.

        Args:
            C (list of dict): Cost matrix where each entry corresponds to costs for specific characters.

        Returns:
            function: A cost function that takes an index i and a character from the alphabet as arguments,
                      and returns the cost associated with that character at position i in the cost matrix.
        """

        def cost(i, alphabet):
            return C[i - 1][alphabet]

        return cost

