# import unittest
# from unittest.mock import patch
# from algorithm.eliminate_sequence import EliminationController
# import numpy as np
#
#
# class TestEliminationCostCalculation(unittest.TestCase):
#     def setUp(self):
#         # Sample target sequence and coding positions
#         self.target_sequence = "ATGCTTACGTAG"
#         self.coding_positions = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
#
#         # Sample Codon Usage
#         self.codon_usage = {
#             "TAC": 0.2,
#             "GTA": 0.5,
#             "CGT": 0.1,
#             "TTA": 0.1,
#             "CTT": 0.1,
#             "TAG": 0.01,
#         }
#
#         # Cost function parameters
#         self.alpha = 1.0
#         self.beta = 2.0
#         self.w = 5.0
#
#     @patch("utils.cost_utils.EliminationScorerConfig")
#     def test_non_coding_transition_cost(self, MockEliminationScorerConfig):
#         # Mock the cost function to simulate transition mutation costs
#         MockEliminationScorerConfig.return_value.cost_function = lambda i, v, sigma: self.alpha if sigma == "T" else self.beta
#         MockEliminationScorerConfig.return_value.codon_usage = self.codon_usage  # Ensure codon_usage is set
#
#         # Test transition mutation (assuming a "T" substitution is a transition)
#         cost = EliminationController.eliminate(self.target_sequence, ["TAC"], self.coding_positions)[0]
#         self.assertEqual(self.alpha, cost)  # The cost should be equal to alpha for transitions
#
#     @patch("utils.cost_utils.EliminationScorerConfig")
#     def test_non_coding_transversion_cost(self, MockEliminationScorerConfig):
#         # Mock the cost function to simulate transversion mutation costs
#         MockEliminationScorerConfig.return_value.cost_function = lambda i, v, sigma: self.beta if sigma == "C" else self.alpha
#         MockEliminationScorerConfig.return_value.codon_usage = self.codon_usage  # Ensure codon_usage is set
#
#         # Test transversion mutation (assuming a "C" substitution is a transversion)
#         cost = EliminationController.eliminate(self.target_sequence, ["TAC"], self.coding_positions)[0]
#         self.assertEqual(self.beta, cost)  # The cost should be equal to beta for transversions
#
#     @patch("utils.cost_utils.EliminationScorerConfig")
#     def test_synonymous_substitution_cost(self, MockEliminationScorerConfig):
#         MockEliminationScorerConfig.return_value.cost_function = lambda i, v, sigma: -np.log(self.codon_usage["TTA"])
#         MockEliminationScorerConfig.return_value.codon_usage = self.codon_usage  # Ensure codon_usage is set
#
#         # Test synonymous substitution for codon "CTT" -> "TTA"
#         cost = EliminationController.eliminate(self.target_sequence, ["TAC"], self.coding_positions)[0]
#         self.assertEqual(-np.log(self.codon_usage['TTA']), cost)  # The cost should be based on codon usage
#
#     @patch("utils.cost_utils.EliminationScorerConfig")
#     def test_stop_codon_formation_cost(self, MockEliminationScorerConfig):
#         # Mock the cost function to simulate stop codon formation, which should return infinity
#         MockEliminationScorerConfig.return_value.cost_function = lambda i, v, sigma: float("inf")
#         MockEliminationScorerConfig.return_value.codon_usage = self.codon_usage  # Ensure codon_usage is set
#
#         # Test for stop codon formation (e.g., "TAA" or similar stop codon)
#         cost = EliminationController.eliminate(self.target_sequence, ["TAC"], self.coding_positions)[0]
#         self.assertEqual(float('inf'), cost)  # The cost should be infinity for stop codons
#
#     def test_invalid_codon_usage(self):
#         # Test invalid codon usage (negative value in codon usage)
#         invalid_codon_usage = {"TAC": -0.1}  # Invalid probability
#         with self.assertRaises(ValueError):
#             EliminationController.eliminate(self.target_sequence, ["TAC"], self.coding_positions)