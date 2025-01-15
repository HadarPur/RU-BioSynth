import unittest

from Bio.Seq import Seq
from utils.dna_utils import DNAUtils


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
                                     0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2,
                                     3, 1, 2, 3, 1, 2, 3, 1, 2,
                                     3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.assertEqual(coding_indexes, expected_coding_indexes)
        self.assertEqual(coding_positions, expected_coding_positions)

    def test_get_coding_and_non_coding_regions_contained(self):
        seq = Seq("TATAATGTACATACAGTAAATGATGTACATACAGATGATGTACATACAGATGTAATACATACAGATGATGTACATACAGATGTAATAA")
        seq_str = str(seq)

        coding_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(seq_str)
        expected_coding_indexes = [(19, 55), (64, 85)]

        expected_coding_positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 0, 0, 0]

        self.assertEqual(coding_indexes, expected_coding_indexes)
        self.assertEqual(coding_positions, expected_coding_positions)

    def test_extract_coding_regions_with_indexes(self):
        region_list = [
            {"seq": Seq("ATG"), "is_coding_region": True},
            {"seq": Seq("GGC"), "is_coding_region": True},
            {"seq": Seq("CTAG"), "is_coding_region": False}
        ]
        coding_regions, coding_indexes = DNAUtils.extract_coding_regions_with_indexes(region_list)
        expected_coding_regions = [Seq("ATG"), Seq("GGC")]
        expected_coding_indexes = [0, 1]
        self.assertEqual(coding_regions, expected_coding_regions)
        self.assertEqual(coding_indexes, expected_coding_indexes)

    def test_update_coding_regions(self):
        region_list = [
            {"seq": Seq("ATG"), "is_coding_region": True},
            {"seq": Seq("GGC"), "is_coding_region": True},
            {"seq": Seq("CTAG"), "is_coding_region": False}
        ]
        coding_indexes = [0, 1]
        coding_regions_to_exclude = {0: Seq("ATG")}
        updated_region_list = DNAUtils.update_coding_regions(region_list, coding_indexes,
                                                             coding_regions_to_exclude)
        expected_updated_region_list = [
            {"seq": Seq("ATG"), "is_coding_region": False},
            {"seq": Seq("GGC"), "is_coding_region": True},
            {"seq": Seq("CTAG"), "is_coding_region": False}
        ]
        self.assertEqual(updated_region_list, expected_updated_region_list)
