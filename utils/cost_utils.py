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

    # def get_amino_acid_scoring_scheme(self, regions_to_exclude=None):
    #     if regions_to_exclude:
    #
    #     else:
    #     return

