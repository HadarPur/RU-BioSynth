from Bio.Seq import Seq
import random


def highlight_coding_regions(dna_seq, coding_regions):
    # List of available color codes
    available_color_codes = [code for code in range(91, 98) if code not in [93, 97]]

    # Create a dictionary to map each coding region sequence to a unique color
    region_color_mapping = {}

    # Generate colors for each coding region sequence
    for region_seq in coding_regions:
        if not available_color_codes:
            break  # No more available colors
        color_code = random.choice(available_color_codes)
        available_color_codes.remove(color_code)
        region_color_mapping[str(region_seq)] = f'\033[{color_code}m'

    # Create a copy of the DNA sequence to modify for highlighting
    highlighted_seq = str(dna_seq)

    # Iterate through the coding regions and highlight them in the sequence
    for region_seq in coding_regions:
        region_str = str(region_seq)
        region_start = highlighted_seq.find(region_str)

        while region_start >= 0:
            region_end = region_start + len(region_str)
            color_code = region_color_mapping[region_str]

            # Modify the highlighted_seq to include color codes
            highlighted_seq = (
                    highlighted_seq[:region_start] +
                    color_code + highlighted_seq[region_start:region_end] + '\033[0m' +  # Reset color after region
                    highlighted_seq[region_end:]
            )

            region_start = highlighted_seq.find(region_str, region_end)

    return highlighted_seq


def get_coding_region(dna_seq):
    # Define the DNA sequence
    dna_seq = Seq(dna_seq)

    # Define the start and stop codons
    start_codon = Seq("ATG")
    stop_codons = [Seq("TAA"), Seq("TAG"), Seq("TGA")]

    # Find the primary coding regions
    coding_regions = []
    i = 0

    while i < len(dna_seq):
        if dna_seq[i:i + 3] == start_codon:
            start_idx = i
            in_coding_region = True
            for j in range(i + 3, len(dna_seq), 3):
                if dna_seq[j:j + 3] in stop_codons:
                    coding_regions.append(dna_seq[start_idx:j + 3])
                    i = j + 3
                    in_coding_region = False
                    break
            if in_coding_region:
                i += 3
        else:
            i += 1

    return coding_regions
