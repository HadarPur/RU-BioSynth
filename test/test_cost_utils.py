import unittest
from utils.cost_utils import CodonScorer, get_codon_scores


class TestCodonScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = CodonScorer()

    def test_get_codon_scores(self):
        # Define a sample codon scoring scheme
        codon_scores = [
            {"ATG": [1, 2, 3]},
            {"TAA": [4, 5, 6]}
        ]
        self.assertEqual(get_codon_scores("ATG", codon_scores), [1, 2, 3])
        self.assertEqual(get_codon_scores("TAA", codon_scores), [4, 5, 6])
        self.assertIsNone(get_codon_scores("AAA", codon_scores))  # Codon not found

    def test_calculate_scores(self):
        # Define a sample list of sequences with is_coding_region information
        sequences = [
            {'seq': "ATG", 'is_coding_region': True},
            {'seq': "TAA", 'is_coding_region': True},
            {'seq': "AAA", 'is_coding_region': False},
            {'seq': "GGG", 'is_coding_region': False}
        ]
        expected_scores = [{'A': 0.0, 'T': 100.0, 'C': 100.0, 'G': 100.0},
                           {'A': 100.0, 'T': 0.0, 'C': 100.0, 'G': 100.0},
                           {'A': 100.0, 'T': 100.0, 'C': 100.0, 'G': 0.0},
                           {'A': float('inf'), 'T': 0.0, 'C': float('inf'), 'G': float('inf')},
                           {'A': 0.0, 'T': float('inf'), 'C': float('inf'), 'G': 1.0},
                           {'A': 0.0, 'T': float('inf'), 'C': float('inf'), 'G': 1.0},
                           {'A': 0.0, 'T': 1.0, 'C': 2.0, 'G': 2.0},
                           {'A': 0.0, 'T': 1.0, 'C': 2.0, 'G': 2.0},
                           {'A': 0.0, 'T': 1.0, 'C': 2.0, 'G': 2.0},
                           {'A': 2.0, 'T': 2.0, 'C': 1.0, 'G': 0.0},
                           {'A': 2.0, 'T': 2.0, 'C': 1.0, 'G': 0.0},
                           {'A': 2.0, 'T': 2.0, 'C': 1.0, 'G': 0.0}]

        self.assertEqual(self.scorer.calculate_scores(sequences), expected_scores)
