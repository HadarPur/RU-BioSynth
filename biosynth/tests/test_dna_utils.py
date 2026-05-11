import unittest

from Bio.Seq import Seq

from biosynth.utils.dna_utils import DNAUtils


class TestDNAHighlighter(unittest.TestCase):
    def test_get_coding_and_non_coding_regions(self):
        seq = Seq(
            "CGCGGTTTTGTAGAAGGTTAGGGGAATAGGTTAGATTGAGTGGCTTAAGAATGTAA*ATGCTTCTTGTGGAACTCGACAACGCAACAACGCGACGGATCTA"
            "CGTCACAGCGTGCATAGTGAAAACGGAGTTGCTGACGACGAAAGCGACATTGGGATCTGTCAGTTGTCATTCGCGAAAAACATCCGTCCCCGAGGCGGAC"
            "ACTGATTGAGCGTACAATGGTTTAGATGCCCTGA"
        )
        seq_str = str(seq)

        start_codon_identified, cleaned_seq = DNAUtils.find_start_codon(seq_str)

        coding_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(
            cleaned_seq, start_codon_identified)


        expected_coding_indexes = (56, 209)

        expected_coding_positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     1, 2, -3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2,
                                     3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2,
                                     3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.assertEqual(coding_indexes, expected_coding_indexes)
        self.assertEqual(coding_positions, expected_coding_positions)

    def test_get_coding_and_non_coding_regions_no_coding_region(self):
        seq = "AAACCCGGGTTT"  # No ATG or stop codons
        start_codon_identified, cleaned_seq = DNAUtils.find_start_codon(seq)

        coding_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(
            cleaned_seq, start_codon_identified)

        self.assertTrue(all(pos == 0 for pos in coding_positions))
        self.assertEqual(coding_indexes, None)

    def test_get_coding_and_non_coding_regions_start_no_stop(self):
        seq = "AA*ATGCCCCCCCC"  # ATG but no stop codon

        with self.assertRaises(ValueError) as cm:
            DNAUtils.find_start_codon(seq)

        self.assertEqual(
            str(cm.exception),
            "No in-frame stop codon found after *ATG"
        )

    def test_star_present_but_no_atg_after(self):
        seq = "AA*CCCCCC"  # '*' present, no ATG after

        with self.assertRaises(ValueError) as cm:
            DNAUtils.find_start_codon(seq)

        self.assertEqual(
            str(cm.exception),
            "'*' present but not followed by ATG"
        )

    def test_get_coding_sequence_returns_substring(self):
        seq = "AAAATGCCCAAA"
        # (3, 9) → "ATGCCC"
        self.assertEqual(DNAUtils.get_coding_sequence((3, 9), seq), "ATGCCC")

    def test_get_coding_sequence_returns_none_when_index_is_none(self):
        self.assertIsNone(DNAUtils.get_coding_sequence(None, "ATG"))

    def test_get_coding_regions_returns_none_when_atg_missing(self):
        # When the start_codon index is None, the method short-circuits and
        # returns (all-zero positions, None).
        positions, idx = DNAUtils.get_coding_and_non_coding_regions_positions(
            "ATGCCC", None
        )
        self.assertEqual(positions, [0] * 6)
        self.assertIsNone(idx)

    def test_get_coding_regions_no_in_frame_stop_returns_none(self):
        # Called directly (bypassing find_start_codon) with an ATG index but
        # a sequence that has no in-frame stop codon — exercises the
        # 'stop_idx is None' early return.
        seq = "ATGCCCAAA"  # ATG at 0, no in-frame stop
        positions, idx = DNAUtils.get_coding_and_non_coding_regions_positions(seq, 0)
        self.assertEqual(positions, [0] * 9)
        self.assertIsNone(idx)
