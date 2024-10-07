# Cost
s_coding_region = float('inf')  # stop codon
o_coding_region = 0.  # origin
w_coding_region = 100.  # changes codons
x_coding_region = 1.  # does not change codons

o_non_coding_region = 0.  # origin
w_non_coding_region = 2.  # changes codons
x_non_coding_region = 1.  # does not change codons

elimination_process_description = 'When considering the costs associated with changing target sequences in both coding and non-coding regions, different expense structures come into play.'

coding_region_cost_description = f'In coding regions, a substitution that does not change the amino acid incurs an expense of {x_coding_region}. ' \
                                 f'\nA higher cost of {w_coding_region} is associated with substitutions that change the amino acid.' \
                                 f'\nA substitution that converts an amino acid to a (premature) stop codon incurs a very high cost of {s_coding_region}'

non_coding_region_cost_description = f'Within non-coding sections, altering bases within complementary pairs (A to T, T to A, C to G, G to C) incurs a cost of {x_non_coding_region}.' \
                                     f'\nSubstituting one base for another (e.g., A to G or T to C) raises the expense to {w_non_coding_region}.\n'
