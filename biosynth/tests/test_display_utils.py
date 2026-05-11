"""Tests for biosynth.utils.display_utils."""

import unittest

from biosynth.utils.display_utils import SequenceUtils, get_color_for_coding_region


class TestGetColorForCodingRegion(unittest.TestCase):
    def test_cycles_through_palette(self):
        colors = ["red", "blue", "green", "orange", "purple"]
        counter = 0
        for expected in colors:
            counter, color = get_color_for_coding_region(counter)
            self.assertEqual(color, expected)
        # Wraps back to the first colour.
        counter, color = get_color_for_coding_region(counter)
        self.assertEqual(color, "red")


class TestFindColorBoundaries(unittest.TestCase):
    def test_no_color_codes(self):
        starts, ends = SequenceUtils._find_color_boundaries("ATCG")
        self.assertEqual(starts, [])
        self.assertEqual(ends, [])

    def test_single_color_pair(self):
        s = "\033[36mATG\033[0m"
        starts, ends = SequenceUtils._find_color_boundaries(s)
        self.assertEqual(len(starts), 2)
        self.assertEqual(len(ends), 2)
        self.assertLess(starts[0], starts[1])


class TestGetSequence(unittest.TestCase):
    def test_formats_title_and_sequence(self):
        out = SequenceUtils.get_sequence("Target", "ATG")
        self.assertIn("Target", out)
        self.assertIn("ATG", out)
        self.assertTrue(out.startswith("\n"))


class TestGetPatterns(unittest.TestCase):
    def test_sorted_join(self):
        self.assertEqual(
            SequenceUtils.get_patterns({"CCC", "AAA", "BBB"}),
            "AAA, BBB, CCC",
        )

    def test_empty_returns_none_marker(self):
        self.assertEqual(SequenceUtils.get_patterns(set()), "None")


class TestSplitStringEveryNChars(unittest.TestCase):
    def test_exact_multiple(self):
        self.assertEqual(
            SequenceUtils.split_string_every_n_chars("ABCDEF", 3),
            ["ABC", "DEF"],
        )

    def test_remainder_kept_in_last_chunk(self):
        self.assertEqual(
            SequenceUtils.split_string_every_n_chars("ABCDE", 2),
            ["AB", "CD", "E"],
        )

    def test_empty(self):
        self.assertEqual(SequenceUtils.split_string_every_n_chars("", 3), [])


class TestMarkNonEqualCharacters(unittest.TestCase):
    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            SequenceUtils.mark_non_equal_characters("AAA", "AA", [0, 0, 0])

    def test_non_coding_diff_brackets_each_char(self):
        idx, m1, m2 = SequenceUtils.mark_non_equal_characters(
            "AAA", "ATA", [0, 0, 0]
        )
        self.assertIn("[A]", m1)
        self.assertIn("[T]", m2)
        self.assertIn("1", idx)
        self.assertIn("2", idx)
        self.assertIn("3", idx)

    def test_coding_diff_brackets_full_codon(self):
        idx, m1, m2 = SequenceUtils.mark_non_equal_characters(
            "ATGAAA", "ATGAAC", [1, 2, 3, 1, 2, 3]
        )
        # Only the second codon differs.
        self.assertIn("[AAA]", m1)
        self.assertIn("[AAC]", m2)
        # Index strings include the codon range.
        self.assertIn("4-6", idx)

    def test_identical_sequences_no_brackets(self):
        idx, m1, m2 = SequenceUtils.mark_non_equal_characters(
            "ATG", "ATG", [1, 2, 3]
        )
        self.assertNotIn("[", m1)
        self.assertNotIn("[", m2)

    def test_mixed_coding_and_non_coding(self):
        # 3 non-coding + 3 coding + 3 non-coding
        idx, m1, m2 = SequenceUtils.mark_non_equal_characters(
            "AAAATGCCC", "AATATGCCC",
            [0, 0, 0, 1, 2, 3, 0, 0, 0],
        )
        # Diff in non-coding (positions 3)
        self.assertIn("[A]", m1)
        self.assertIn("[T]", m2)


class TestHighlightSequencesToHtml(unittest.TestCase):
    def test_no_coding_region(self):
        out = SequenceUtils.highlight_sequences_to_html("ATGC", None, line_length=2)
        # No <span> wrappers expected when no coding region.
        self.assertNotIn("<span", out)
        # Lines are joined (no <br> by default).
        self.assertNotIn("<br>", out)

    def test_coding_region_wrapped_in_span(self):
        out = SequenceUtils.highlight_sequences_to_html(
            "ATGCAT", coding_index=(0, 3), line_length=10
        )
        self.assertIn('<span style="color:', out)

    def test_returnBr_inserts_breaks(self):
        out = SequenceUtils.highlight_sequences_to_html(
            "ATGCAT", coding_index=None, line_length=3, returnBr=True
        )
        self.assertIn("<br>", out)


class TestHighlightDifferencesWithCodingHtml(unittest.TestCase):
    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            SequenceUtils.highlight_differences_with_coding_html(
                "AAA", "AA", [0, 0, 0]
            )

    def test_non_coding_difference_bracketed(self):
        out = SequenceUtils.highlight_differences_with_coding_html(
            "AAA", "ATA", [0, 0, 0]
        )
        # The middle char differs and should appear bracketed.
        self.assertIn("[T]", out)

    def test_coding_difference_codon_bracketed(self):
        out = SequenceUtils.highlight_differences_with_coding_html(
            "ATGAAA", "ATGAAC", [1, 2, 3, 1, 2, 3]
        )
        # The diverging codon is bracketed in the marked string, but each
        # character is then wrapped in a <span> for HTML colouring — so we
        # check for the bracket markers and the changed base.
        self.assertIn("[", out)
        self.assertIn("]", out)
        self.assertIn(">C<", out)

    def test_partial_trailing_codon(self):
        # Coding region ends before a full codon is available — exercises the
        # partial-codon safety branch.
        out = SequenceUtils.highlight_differences_with_coding_html(
            "ATGAA", "ATGAC", [1, 2, 3, 1, 2]
        )
        self.assertIn("[", out)
        self.assertIn(">C<", out)

    def test_identical_sequences_yields_no_brackets(self):
        out = SequenceUtils.highlight_differences_with_coding_html(
            "ATGAAA", "ATGAAA", [1, 2, 3, 1, 2, 3]
        )
        self.assertNotIn("[", out)


class TestHighlightSequenceToTerminal(unittest.TestCase):
    def test_wraps_coding_region_in_ansi(self):
        out = SequenceUtils.highlight_sequence_to_terminal(
            "AAAATGAAA", coding_range=(3, 6)
        )
        self.assertEqual(out.index("\033["), 3)
        self.assertIn("ATG", out)
        self.assertIn("\033[0m", out)

    def test_empty_coding_range(self):
        out = SequenceUtils.highlight_sequence_to_terminal(
            "AAAA", coding_range=(0, 0)
        )
        # Reset code present even if no bases were highlighted.
        self.assertIn("\033[0m", out)


if __name__ == "__main__":
    unittest.main()
