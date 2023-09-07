from Bio.Seq import Seq
import random


class DNAHighlighter:
    def __init__(self, seq):
        """
        Initializes a DNAHighlighter object with a DNA sequence.

        Parameters:
            seq (str): DNA sequence as a string.
        """
        self.seq = seq

    def highlight_coding_regions(self, coding_regions):
        """
        Highlights coding regions within the DNA sequence using colored escape codes.

        Parameters:
            coding_regions (list of Seq): List of coding regions (Seq objects) to be highlighted.

        Returns:
            str: DNA sequence with highlighted coding regions using escape codes.
        """
        available_color_codes = [code for code in range(91, 98) if code not in [93, 97]]
        region_color_mapping = {}

        for region_seq in coding_regions:
            if not available_color_codes:
                break
            color_code = random.choice(available_color_codes)
            available_color_codes.remove(color_code)
            region_color_mapping[str(region_seq)] = f'\033[{color_code}m'

        highlighted_seq = str(self.seq)

        for region_seq in coding_regions:
            region_str = str(region_seq)
            region_start = highlighted_seq.find(region_str)

            while region_start >= 0:
                region_end = region_start + len(region_str)
                color_code = region_color_mapping[region_str]

                highlighted_seq = (
                    highlighted_seq[:region_start] +
                    color_code + highlighted_seq[region_start:region_end] + '\033[0m' +
                    highlighted_seq[region_end:]
                )

                region_start = highlighted_seq.find(region_str, region_end)

        return highlighted_seq

    def get_coding_and_non_coding_regions(self):
        """
        Identifies and returns coding regions within the DNA sequence.

        Returns:
            list of dict: List of dictionaries containing "seq" (Seq object) and "is_coding_region" (bool) keys.
        """
        start_codon = Seq("ATG")
        stop_codons = [Seq("TAA"), Seq("TAG"), Seq("TGA")]
        coding_regions = []

        i = 0
        non_coding_region = ""
        in_coding_region = True

        while i < len(self.seq):
            if self.seq[i:i + 3] == start_codon:
                if in_coding_region is False:
                    coding_regions.append({
                        "seq": non_coding_region,
                        "is_coding_region": False
                    })
                    non_coding_region = ""

                start_idx = i
                in_coding_region = True
                for j in range(i + 3, len(self.seq), 3):
                    if self.seq[j:j + 3] in stop_codons:
                        coding_regions.append({
                            "seq": self.seq[start_idx:j + 3],
                            "is_coding_region": True
                        })
                        i = j + 3
                        in_coding_region = False
                        break
                if in_coding_region:
                    i += 3
            else:
                in_coding_region = False
                non_coding_region += self.seq[i:i + 3]
                i += 3

        return coding_regions

    def extract_coding_regions_with_indexes(self, region_list):
        """
        Extracts coding regions and their indexes from a list of dictionaries.

        Args:
            region_list (list of dict): List of dictionaries containing "seq" (Seq object) and "is_coding_region" (bool) keys.

        Returns:
            tuple: A tuple containing two lists:
                - List of Seq objects representing coding regions.
                - List of indexes (int) corresponding to the coding regions.
        """

        coding_regions = []
        coding_indexes = []

        for index, region in enumerate(region_list):
            if region["is_coding_region"]:
                coding_regions.append(region["seq"])
                coding_indexes.append(index)

        return coding_regions, coding_indexes

    def update_coding_regions(self, region_list, coding_indexes, coding_regions_to_exclude):
        """
        Update the 'is_coding_region' values in a list of dictionaries at specified indices.

        Args:
            region_list (list of dict): List of dictionaries containing "seq" (Seq object) and "is_coding_region" (bool) keys.
            coding_regions_to_exclude (dict of str): Dictionary of sequences to exclude.

        Returns:
            region_list
        """

        for key, value in coding_regions_to_exclude.items():
            coding_region_index = coding_indexes[key]
            region = region_list[coding_region_index]
            if region['seq'] == value:
                region['is_coding_region'] = False
                region_list[coding_region_index] = region

        return region_list

