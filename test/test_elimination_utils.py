import unittest
from algorithm.eliminate_sequence import EliminationController
from utils.text_utils import set_output_format, OutputFormat
from unittest.mock import MagicMock, patch

class TestEliminationController(unittest.TestCase):
    def setUp(self):
        # Set output format
        set_output_format(OutputFormat.TERMINAL)

        # Setup input data
        self.target_sequence = "ATGCTTACGTAG"
        self.unwanted_patterns = {"CGT", "TAG"}
        self.coding_positions = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]

        # Patch CostData constants
        self.patcher_usage = patch("data.app_data.CostData.codon_usage", new={
             'TTT': 0.46, 'TTC': 0.54, 'TTA': 0.08, 'TTG': 0.13, 'CTT': 0.13, 'CTC': 0.2, 'CTA': 0.07, 'CTG': 0.4,
             'ATT': 0.36, 'ATC': 0.47, 'ATA': 0.17, 'ATG': 1.0, 'GTT': 0.18, 'GTC': 0.24, 'GTA': 0.12, 'GTG': 0.46,
             'TCT': 0.19, 'TCC': 0.22, 'TCA': 0.15, 'TCG': 0.05, 'CCT': 0.29, 'CCC': 0.32, 'CCA': 0.28, 'CCG': 0.11,
             'ACT': 0.25, 'ACC': 0.36, 'ACA': 0.28, 'ACG': 0.11, 'GCT': 0.27, 'GCC': 0.4, 'GCA': 0.23, 'GCG': 0.11,
             'TAT': 0.44, 'TAC': 0.56, 'TAA': 0.3, 'TAG': 0.24, 'CAT': 0.42, 'CAC': 0.58, 'CAA': 0.27, 'CAG': 0.73,
             'AAT': 0.47, 'AAC': 0.53, 'AAA': 0.43, 'AAG': 0.57, 'GAT': 0.46, 'GAC': 0.54, 'GAA': 0.42, 'GAG': 0.58,
             'TGT': 0.46, 'TGC': 0.54, 'TGA': 0.47, 'TGG': 1.0, 'CGT': 0.08, 'CGC': 0.18, 'CGA': 0.11, 'CGG': 0.2,
             'AGT': 0.15, 'AGC': 0.24, 'AGA': 0.21, 'AGG': 0.21, 'GGT': 0.16, 'GGC': 0.34, 'GGA': 0.25, 'GGG': 0.25
        })
        self.patcher_alpha = patch("data.app_data.CostData.alpha", new=1.0)
        self.patcher_beta = patch("data.app_data.CostData.beta", new=2.0)
        self.patcher_w = patch("data.app_data.CostData.w", new=5.0)

        self.patcher_usage.start()
        self.patcher_alpha.start()
        self.patcher_beta.start()
        self.patcher_w.start()

    def tearDown(self):
        self.patcher_usage.stop()
        self.patcher_alpha.stop()
        self.patcher_beta.stop()
        self.patcher_w.stop()

    def test_no_unwanted_patterns(self):
        result_info, changes, new_seq, cost = EliminationController.eliminate(
            "AAAAAA", {"TTT"}, [1] * 6
        )
        self.assertEqual(new_seq, "AAAAAA")
        self.assertEqual(cost, 0.0)
        self.assertIsNone(changes)
        self.assertIn("No unwanted patterns", result_info)

    def test_patterns_eliminated(self):
        info, changes, new_seq, cost = EliminationController.eliminate(
            self.target_sequence,
            self.unwanted_patterns,
            self.coding_positions
        )
        for pattern in self.unwanted_patterns:
            self.assertNotIn(pattern, new_seq)
        self.assertIsInstance(new_seq, str)
        self.assertGreater(len(new_seq), 0)
        self.assertIsInstance(cost, float)

    def test_cost_non_negative(self):
        _, _, _, cost = EliminationController.eliminate(
            self.target_sequence,
            self.unwanted_patterns,
            self.coding_positions
        )
        self.assertGreaterEqual(cost, 0.0)

    def test_empty_sequence(self):
        info, changes, new_seq, cost = EliminationController.eliminate(
            "", {"TAG"}, []
        )
        self.assertEqual(new_seq, "")
        self.assertEqual(cost, 0.0)
        self.assertIsNone(changes)
        self.assertIn("No unwanted patterns", info)

    def test_empty_patterns(self):
        info, changes, new_seq, cost = EliminationController.eliminate(
            self.target_sequence,
            set(),
            self.coding_positions
        )
        self.assertEqual(new_seq, self.target_sequence)
        self.assertEqual(cost, 0.0)
        self.assertIsNone(changes)


    def test_invalid_transition_handling(self):
        target_sequence = "ATG"
        unwanted_patterns = {'AAA', 'AAT', 'AAG', 'AAC',
                             'ATA', 'ATT', 'ATG', 'ATC',
                             'AGA', 'AGT', 'AGG', 'AGC',
                             'ACA', 'ACT', 'ACG', 'ACC',
                             'TAA', 'TAT', 'TAG', 'TAC',
                             'TTA', 'TTT', 'TTG', 'TTC',
                             'TGA', 'TGT', 'TGG', 'TGC',
                             'TCA', 'TCT', 'TCG', 'TCC',
                             'GAA', 'GAT', 'GAG', 'GAC',
                             'GTA', 'GTT', 'GTG', 'GTC',
                             'GGA', 'GGT', 'GGG', 'GGC',
                             'GCA', 'GCT', 'GCG', 'GCC',
                             'CAA', 'CAT', 'CAG', 'CAC',
                             'CTA', 'CTT', 'CTG', 'CTC',
                             'CGA', 'CGT', 'CGG', 'CGC',
                             'CCA', 'CCT', 'CCG', 'CCC'}

        coding_positions = [0, 0, 0]
        info, changes, new_seq, cost = EliminationController.eliminate(
            target_sequence,
            unwanted_patterns,
            coding_positions
        )
        self.assertIsNone(new_seq)
        self.assertEqual(cost, float("inf"))
        self.assertIn("No valid sequence", info)
