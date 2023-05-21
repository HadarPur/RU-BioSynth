from Bio.Seq import Seq


def get_coding_region(dna_seq):
    # Define the DNA sequence
    dna_seq = Seq(dna_seq)

    # Define the start and stop codons
    start_codon = Seq("ATG")
    stop_codons = [Seq("TAA"), Seq("TAG"), Seq("TGA")]

    # Find the coding regions
    coding_regions = []
    for i in range(len(dna_seq)):
        if dna_seq[i:i + 3] == start_codon:
            for j in range(i + 3, len(dna_seq), 3):
                if dna_seq[j:j + 3] in stop_codons:
                    coding_regions.append(dna_seq[i:j + 3])
                    break

    # # Save the extracted coding regions to a file or use them for further analysis
    # with open("coding_regions.txt", "w") as f:
    #     for region in coding_regions:
    #         f.write(region + "\n")

    return coding_regions
