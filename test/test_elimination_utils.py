import unittest

from utils.cost_utils import EliminationScorer


class TestEliminationUtils(unittest.TestCase):
    def setUp(self):
        self.elimination_utils = EliminationScorer()

    def test_cost_function(self):
        C = [{'A': 1, 'G': 2, 'T': 3, 'C': 4},
             {'A': 5, 'G': 6, 'T': 7, 'C': 8},
             {'A': 9, 'G': 10, 'T': 11, 'C': 12}]
        cost_func = self.elimination_utils.cost_function(C)
        self.assertEqual(cost_func(1, 'A'), 1)
        self.assertEqual(cost_func(2, 'G'), 6)
        self.assertEqual(cost_func(3, 'T'), 11)
