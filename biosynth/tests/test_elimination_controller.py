import unittest
from unittest.mock import patch

from biosynth.algorithm.elimination_controller import EliminationController
from biosynth.utils.text_utils import OutputFormat, set_output_format

class TestEliminationController(unittest.TestCase):
    def setUp(self):
        set_output_format(OutputFormat.TEST)

        # Setup input data
        self.target_sequence = "ATGCTTACGTAG"
        self.unwanted_patterns = {"CGT", "TAG"}
        self.coding_positions = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]

        # Patch CostData constants
        self.patcher_usage = patch("biosynth.data.app_data.CostData.codon_usage",
                                   new=dict(TTT=0.94, TCT=0.4, TAT=0.89, TGT=0.85, TTC=0.06, TCC=0.05, TAC=0.11,
                                            TGC=0.15, TTA=0.67, TCA=0.23, TAA=0.91, TGA=0.02, TTG=0.07, TCG=0.03,
                                            TAG=0.06, TGG=1.0, CTT=0.19, CCT=0.51, CAT=0.86, CGT=0.34, CTC=0.01,
                                            CCC=0.04, CAC=0.14, CGC=0.05, CTA=0.05, CCA=0.4, CAA=0.94, CGA=0.23,
                                            CTG=0.01, CCG=0.05, CAG=0.06, CGG=0.02, ATT=0.65, ACT=0.51, AAT=0.88,
                                            AGT=0.26, ATC=0.04, ACC=0.05, AAC=0.12, AGC=0.03, ATA=0.3, ACA=0.4,
                                            AAA=0.95, AGA=0.34, ATG=1.0, ACG=0.04, AAG=0.05, AGG=0.02, GTT=0.54,
                                            GCT=0.58, GAT=0.91, GGT=0.43, GTC=0.04, GCC=0.05, GAC=0.09, GGC=0.05,
                                            GTA=0.38, GCA=0.34, GAA=0.93, GGA=0.45, GTG=0.04, GCG=0.03, GAG=0.07,
                                            GGG=0.06)
                                   )
        self.patcher_alpha = patch("biosynth.data.app_data.CostData.alpha", new=1.0)
        self.patcher_beta = patch("biosynth.data.app_data.CostData.beta", new=2.0)
        self.patcher_w = patch("biosynth.data.app_data.CostData.w", new=5.0)
        self.patcher_oc = patch("biosynth.data.app_data.CostData.optimized_codon", new=False)

        self.patcher_usage.start()
        self.patcher_alpha.start()
        self.patcher_beta.start()
        self.patcher_w.start()
        self.patcher_oc.start()

    def tearDown(self):
        self.patcher_usage.stop()
        self.patcher_alpha.stop()
        self.patcher_beta.stop()
        self.patcher_w.stop()
        self.patcher_oc.stop()

    def test_no_unwanted_patterns(self):
        result_info, changes, new_seq, cost = EliminationController.eliminate(
            "AAAAAA", {"TTT"}, [1] * 6
        )
        self.assertEqual(new_seq, "AAAAAA")
        self.assertEqual(cost, 0.0)
        self.assertIsNone(changes)
        self.assertIn("No invalid patterns identified", result_info)

    def test_patterns_eliminated(self):
        info, cost_contribution, cost_substitution, new_seq, cost = EliminationController.eliminate(
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
        _, _, _, _, cost = EliminationController.eliminate(
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
        self.assertIn("No invalid patterns identified", info)

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

    def test_substitution_forced_at_initial_bigram(self):
        """If every continuation from the input's initial bigram is blocked
        by patterns, the DP must alter one of the first two bases.

        This particular pattern set ties at the very first position of the
        bigram, exercising the position-1 substitution-recording branches.
        """
        target_sequence = "TTA"
        # Block every transition out of state 'TT' (sigma A/T/G/C).
        unwanted_patterns = {"TTA", "TTT", "TTG", "TTC"}
        coding_positions = [0, 0, 0]
        info, cost_contribution, cost_substitution, new_seq, cost = (
            EliminationController.eliminate(
                target_sequence, unwanted_patterns, coding_positions
            )
        )
        for p in unwanted_patterns:
            self.assertNotIn(p, new_seq)
        # At least one substitution must land at the very start
        # (position 1 or 2 in 1-indexed terms used by the recorder).
        starting_positions = {
            entry["Position"] for entry in (cost_substitution or [])
            if entry.get("Position") in (1, 2)
        }
        self.assertTrue(
            starting_positions,
            f"Expected a substitution at position 1 or 2; got {cost_substitution}",
        )

    def test_substitution_forced_at_first_position_only(self):
        """A configuration where the cheapest escape route requires
        substituting the FIRST base of the initial bigram, exercising the
        position-1 (current_state[0] != original_0) recording branches.

        Patterns:
          - 'AG?' (×4) blocks every transition out of state 'AG'.
          - 'AAT' additionally blocks the alternative of substituting only
            position 2 via the 'A' → 'A' / 'G' → 'A' route through state
            'AA' followed by the original T.
        Together these make an A → G transition at position 1 (cost α) the
        unique cheapest path.
        """
        target_sequence = "AGT"
        unwanted_patterns = {"AGT", "AGA", "AGC", "AGG", "AAT"}
        coding_positions = [0, 0, 0]
        info, cost_contribution, cost_substitution, new_seq, cost = (
            EliminationController.eliminate(
                target_sequence, unwanted_patterns, coding_positions
            )
        )
        for p in unwanted_patterns:
            self.assertNotIn(p, new_seq)
        positions = {
            entry["Position"] for entry in (cost_substitution or [])
            if entry.get("Position") in (1, 2)
        }
        # Position 1 should appear among the recorded substitutions.
        self.assertIn(
            1, positions,
            f"Expected a substitution at position 1; got {cost_substitution}",
        )

    def test_substitution_forced_at_second_position_only(self):
        """A configuration where the cheapest escape route requires
        substituting the SECOND base of the initial bigram, exercising the
        position-2 (current_state[1] != original_1) recording branch.

        Patterns:
          - '?TT' (×4) forbids every transition into '?T' followed by 'T'.
          - 'TTC' additionally forbids the alternative of substituting only
            the final base (T → C at position 3 via u='TT').
        These together make the uniquely cheapest path a T → C transition
        at position 2, so the optimized sequence at column 2 is 'TC'.
        """
        target_sequence = "TTT"
        unwanted_patterns = {"TTT", "ATT", "CTT", "GTT", "TTC"}
        coding_positions = [0, 0, 0]
        info, cost_contribution, cost_substitution, new_seq, cost = (
            EliminationController.eliminate(
                target_sequence, unwanted_patterns, coding_positions
            )
        )
        for p in unwanted_patterns:
            self.assertNotIn(p, new_seq)
        positions = {
            entry["Position"] for entry in (cost_substitution or [])
            if entry.get("Position") in (1, 2)
        }
        # Position 2 should appear among the recorded substitutions.
        self.assertIn(
            2, positions,
            f"Expected a substitution at position 2; got {cost_substitution}",
        )

    def test_substitution_at_first_positions_non_coding(self):
        """A non-coding sequence where the unwanted pattern straddles
        positions 0/1/2 forces edits at the start.

        Exercises the backtrack-reconstruction branches that fire only when
        ``coding_positions[0] == 0`` or ``coding_positions[1] == 0``.
        """
        target_sequence = "TAGTAC"
        unwanted_patterns = {"TAGTAC"}
        coding_positions = [0] * 6
        info, cost_contribution, cost_substitution, new_seq, cost = (
            EliminationController.eliminate(
                target_sequence, unwanted_patterns, coding_positions
            )
        )
        self.assertNotIn("TAGTAC", new_seq)
        # At least one substitution should be recorded somewhere.
        self.assertTrue(cost_substitution or cost_contribution)
        # The substitution cost should be finite and >= 0.
        self.assertGreaterEqual(cost, 0.0)
        self.assertLess(cost, float("inf"))
