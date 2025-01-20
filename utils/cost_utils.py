from settings.costs_settings import o_non_coding_region, w_non_coding_region, x_non_coding_region
from settings.costs_settings import s_coding_region, o_coding_region, w_coding_region, x_coding_region
from utils.amino_acid_utils import AminoAcidConfigScheme
from utils.output_utils import Logger
import numpy as np
from utils.amino_acid_utils import AminoAcidConfig

# Define a class called CodonScorer
# def get_codon_scores(codon, codon_scores):
#     """
#     Retrieves the scoring information for a given codon.
#
#     Parameters:
#         codon (str): Codon sequence for which scoring information is needed.
#
#     Returns:
#         list or None: List of scoring information for the codon, or None if codon is not found.
#         :param codon:
#         :param codon_scores:
#     """
#     # Iterate through codon scores
#     for amino_acid_dict in codon_scores:
#         for codon_key, scoring_dicts in amino_acid_dict.items():
#             if codon_key == codon:
#                 return scoring_dicts
#     return None  # Codon not found
#
#
# class CodonScorerFactory:
#     def __init__(self):
#         """
#         Initializes a CodonScorer object with a codon scoring scheme.
#         """
#
#         # Initialize the object with codon scoring schemes for coding and non-coding regions
#         self.coding_region_scheme = AminoAcidConfigScheme(w_coding_region, o_coding_region, x_coding_region,
#                                                           s_coding_region).get_cost_table_coding_region()
#         self.non_coding_region_scheme = AminoAcidConfigScheme(w_non_coding_region, o_non_coding_region,
#                                                               x_non_coding_region).get_cost_table_non_coding_region()
#
#     def calculate_scores(self, seq, codon_positions):
#         """
#         Calculates scores for each codon in coding regions and each base in non-coding regions.
#
#         Parameters:
#             seq (str): The DNA sequence to analyze.
#             codon_positions (list): Precomputed array where each index contains 0 for non-coding or 1, 2, 3 for coding positions.
#
#         Returns:
#             list: List of scores for each codon or base in the sequence.
#         """
#
#         scores_array = []
#         i = 0
#
#         while i < len(seq):
#             if codon_positions[i] != 0:
#                 # Start of a coding region (process codons)
#                 start = i
#                 while i < len(seq) and codon_positions[i] != 0:
#                     i += 1
#                 end = i
#
#                 # Process codons within this coding region
#                 for j in range(start, end, 3):
#                     codon = seq[j:j + 3]
#                     if len(codon) == 3:  # Ensure codon is complete
#                         score = get_codon_scores(codon, self.coding_region_scheme)
#                         if score:
#                             scores_array += score
#                         else:
#                             Logger.warning(
#                                 f"Codon {codon} at positions {j}-{j + 2} not found in the coding scoring scheme.")
#             else:
#                 # Non-coding region (process bases)
#                 base = seq[i]
#                 score = get_codon_scores(base, self.non_coding_region_scheme)
#                 if score:
#                     scores_array += score
#                 else:
#                     Logger.warning(f"Base {base} at position {i} not found in the non-coding scoring scheme.")
#                 i += 1
#
#         return scores_array


def calculate_cost(target_sequence, coding_positions, codon_usage, i, v, sigma, alpha, beta, w):
    codon_pos = coding_positions[i]  # Non-coding: 0; Coding: ((i - \text{coding\_start}) \mod 3) + 1.

    if codon_pos == 0:  # Non-coding region
        if AminoAcidConfig.is_transition(target_sequence[i], sigma):
            return alpha  # Transition substitution
        else:
            return beta  # Transversion substitution

    elif codon_pos in {1, 2}:  # Cost is always 0 for positions 1 and 2
        return 0

    elif codon_pos == 3:  # At 3rd position of codon
        current_codon = AminoAcidConfig.get_last3(target_sequence, i)
        last2_bases = AminoAcidConfig.get_last2(v)
        proposed_codon = f'{last2_bases}{sigma}'

        if proposed_codon == current_codon:
            return 0  # No substitution
        elif AminoAcidConfig.encodes_same_amino_acid(proposed_codon, current_codon):
            return -np.log(codon_usage[proposed_codon], 1e-10)  # Synonymous substitution
        elif AminoAcidConfig.is_stop_codon(proposed_codon):
            return float('inf')  # Stop codon formation
        else:
            return w  # Non-synonymous substitution


class EliminationScorerConfig:
    def __init__(self):
        """
        Initializes a DNASequenceAnalyzer object.
        Sets up the DNA alphabet containing the characters 'A', 'G', 'T', and 'C'.
        """
        self.alphabet = {'A', 'G', 'T', 'C'}

    @staticmethod
    def cost_function(target_sequence, coding_positions, codon_usage, alpha, beta, w):
        """
        Creates a dynamic cost function based on the given sequence properties and scoring parameters.

        Args:
            target_sequence (str): The DNA sequence being analyzed.
            coding_positions (list): Array where each index indicates coding or non-coding regions.
            codon_usage (dict): Dictionary of codon frequencies for synonymous substitutions.
            alpha (float): Cost for transition substitution in non-coding regions.
            beta (float): Cost for transversion substitution in non-coding regions.
            w (float): Cost for non-synonymous substitution in coding regions.

        Returns:
            function: A cost function that takes index i, current state v, and proposed symbol σ
                      as arguments, and returns the dynamic cost.
        """
        def cost(i, v, sigma):
            return calculate_cost(target_sequence, coding_positions, codon_usage, i, v, sigma, alpha, beta, w)

        return cost
