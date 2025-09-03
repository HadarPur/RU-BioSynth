import unittest

from Bio.Seq import Seq

from biosynth.utils.dna_utils import DNAUtils


class TestDNAHighlighter(unittest.TestCase):
    def test_get_coding_and_non_coding_regions(self):
        seq = Seq(
            "CGCGGTTTTGTAGAAGGTTAGGGGAATAGGTTAGATTGAGTGGCTTAAGAATGTAAATGCTTCTTGTGGAACTCGACAACGCAACAACGCGACGGATCTA"
            "CGTCACAGCGTGCATAGTGAAAACGGAGTTGCTGACGACGAAAGCGACATTGGGATCTGTCAGTTGTCATTCGCGAAAAACATCCGTCCCCGAGGCGGAC"
            "ACTGATTGAGCGTACAATGGTTTAGATGCCCTGA"
        )
        seq_str = str(seq)

        coding_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(seq_str)

        expected_coding_indexes = [(56, 209)]

        expected_coding_positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     1, 2, -3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2,
                                     3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.assertEqual(coding_indexes, expected_coding_indexes)
        self.assertEqual(coding_positions, expected_coding_positions)

    def test_get_coding_and_non_coding_regions_contained(self):
        seq = Seq("TATAATGTACATACAGTAAATGATGTACATACAGATGATGTACATACAGATGTAATACATACAGATGATGTACATACAGATGTAATAA")
        seq_str = str(seq)

        coding_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(seq_str)
        expected_coding_indexes = [(19, 55), (64, 85)]

        expected_coding_positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, -3, 1, 2, 3, 1, 2,
                                     3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, -3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 0, 0, 0]

        self.assertEqual(coding_indexes, expected_coding_indexes)
        self.assertEqual(coding_positions, expected_coding_positions)

    def test_find_overlapping_regions_with_overlap(self):
        seq = "ATGGCTAACGTTGACCTAAATGCGTACCGGATGATGTAGATGCCCGCTTCAAGGGTGA"  # Two overlapping ORFs
        has_overlap, overlaps = DNAUtils.find_overlapping_regions(seq)
        self.assertTrue(has_overlap)
        self.assertGreater(len(overlaps), 0)
        # Ensure overlaps are correctly reported as tuples
        for (start1, end1), (start2, end2) in overlaps:
            self.assertTrue(start1 < end1 and start2 < end2)

    def test_find_overlapping_regions_without_overlap(self):
        seq = "AAATGAAAATAA"  # Single valid ORF
        has_overlap, overlaps = DNAUtils.find_overlapping_regions(seq)
        self.assertFalse(has_overlap)
        self.assertEqual(overlaps, []) # pointer line should be present

    def test_get_coding_regions_list(self):
        seq = "AAATGAAATAAATGCCCCTAGGG"
        coding_indexes = [(3, 12), (12, 21)]
        coding_regions = DNAUtils.get_coding_regions_list(coding_indexes, seq)
        self.assertEqual(len(coding_regions), 2)
        self.assertEqual(coding_regions["1"], seq[3:12])
        self.assertEqual(coding_regions["2"], seq[12:21])
