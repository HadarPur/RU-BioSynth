import unittest
from unittest.mock import patch

from algorithm.eliminate_sequence import EliminationController
from utils.text_utils import set_output_format, OutputFormat


class TestEliminationController(unittest.TestCase):
    def setUp(self):
        # Set output format
        set_output_format(OutputFormat.TERMINAL)

        # Setup input data
        self.target_sequence = "ATGCTTACGTAG"
        self.unwanted_patterns = { "CGT", "TAG" }
        self.coding_positions = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]

        # Patch CostData constants
        self.patcher_usage = patch("data.app_data.CostData.codon_usage",
                                   new={ 'TTT': { 'aa': 'Phe', 'freq': 0.46 }, 'TTC': { 'aa': 'Phe', 'freq': 0.54 },
                                         'TTA': { 'aa': 'Leu', 'freq': 0.08 }, 'TTG': { 'aa': 'Leu', 'freq': 0.13 },
                                         'CTT': { 'aa': 'Leu', 'freq': 0.13 }, 'CTC': { 'aa': 'Leu', 'freq': 0.2 },
                                         'CTA': { 'aa': 'Leu', 'freq': 0.07 }, 'CTG': { 'aa': 'Leu', 'freq': 0.4 },
                                         'ATT': { 'aa': 'Ile', 'freq': 0.36 }, 'ATC': { 'aa': 'Ile', 'freq': 0.47 },
                                         'ATA': { 'aa': 'Ile', 'freq': 0.17 }, 'ATG': { 'aa': 'Met', 'freq': 1.0 },
                                         'GTT': { 'aa': 'Val', 'freq': 0.18 }, 'GTC': { 'aa': 'Val', 'freq': 0.24 },
                                         'GTA': { 'aa': 'Val', 'freq': 0.12 }, 'GTG': { 'aa': 'Val', 'freq': 0.46 },
                                         'TCT': { 'aa': 'Ser', 'freq': 0.19 }, 'TCC': { 'aa': 'Ser', 'freq': 0.22 },
                                         'TCA': { 'aa': 'Ser', 'freq': 0.15 }, 'TCG': { 'aa': 'Ser', 'freq': 0.05 },
                                         'CCT': { 'aa': 'Pro', 'freq': 0.29 }, 'CCC': { 'aa': 'Pro', 'freq': 0.32 },
                                         'CCA': { 'aa': 'Pro', 'freq': 0.28 }, 'CCG': { 'aa': 'Pro', 'freq': 0.11 },
                                         'ACT': { 'aa': 'Thr', 'freq': 0.25 }, 'ACC': { 'aa': 'Thr', 'freq': 0.36 },
                                         'ACA': { 'aa': 'Thr', 'freq': 0.28 }, 'ACG': { 'aa': 'Thr', 'freq': 0.11 },
                                         'GCT': { 'aa': 'Ala', 'freq': 0.27 }, 'GCC': { 'aa': 'Ala', 'freq': 0.4 },
                                         'GCA': { 'aa': 'Ala', 'freq': 0.23 }, 'GCG': { 'aa': 'Ala', 'freq': 0.11 },
                                         'TAT': { 'aa': 'Tyr', 'freq': 0.44 }, 'TAC': { 'aa': 'Tyr', 'freq': 0.56 },
                                         'TAA': { 'aa': 'Ter', 'freq': 0.3 }, 'TAG': { 'aa': 'Ter', 'freq': 0.24 },
                                         'CAT': { 'aa': 'His', 'freq': 0.42 }, 'CAC': { 'aa': 'His', 'freq': 0.58 },
                                         'CAA': { 'aa': 'Gln', 'freq': 0.27 }, 'CAG': { 'aa': 'Gln', 'freq': 0.73 },
                                         'AAT': { 'aa': 'Asn', 'freq': 0.47 }, 'AAC': { 'aa': 'Asn', 'freq': 0.53 },
                                         'AAA': { 'aa': 'Lys', 'freq': 0.43 }, 'AAG': { 'aa': 'Lys', 'freq': 0.57 },
                                         'GAT': { 'aa': 'Asp', 'freq': 0.46 }, 'GAC': { 'aa': 'Asp', 'freq': 0.54 },
                                         'GAA': { 'aa': 'Glu', 'freq': 0.42 }, 'GAG': { 'aa': 'Glu', 'freq': 0.58 },
                                         'TGT': { 'aa': 'Cys', 'freq': 0.46 }, 'TGC': { 'aa': 'Cys', 'freq': 0.54 },
                                         'TGA': { 'aa': 'Ter', 'freq': 0.47 }, 'TGG': { 'aa': 'Trp', 'freq': 1.0 },
                                         'CGT': { 'aa': 'Arg', 'freq': 0.08 }, 'CGC': { 'aa': 'Arg', 'freq': 0.18 },
                                         'CGA': { 'aa': 'Arg', 'freq': 0.11 }, 'CGG': { 'aa': 'Arg', 'freq': 0.2 },
                                         'AGT': { 'aa': 'Ser', 'freq': 0.15 }, 'AGC': { 'aa': 'Ser', 'freq': 0.24 },
                                         'AGA': { 'aa': 'Arg', 'freq': 0.21 }, 'AGG': { 'aa': 'Arg', 'freq': 0.21 },
                                         'GGT': { 'aa': 'Gly', 'freq': 0.16 }, 'GGC': { 'aa': 'Gly', 'freq': 0.34 },
                                         'GGA': { 'aa': 'Gly', 'freq': 0.25 }, 'GGG': { 'aa': 'Gly', 'freq': 0.25 } })
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
            "AAAAAA", { "TTT" }, [1] * 6
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
            "", { "TAG" }, []
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
        unwanted_patterns = { 'AAA', 'AAT', 'AAG', 'AAC',
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
                              'CCA', 'CCT', 'CCG', 'CCC' }

        coding_positions = [0, 0, 0]
        info, changes, new_seq, cost = EliminationController.eliminate(
            target_sequence,
            unwanted_patterns,
            coding_positions
        )
        self.assertIsNone(new_seq)
        self.assertEqual(cost, float("inf"))
        self.assertIn("No valid sequence", info)
