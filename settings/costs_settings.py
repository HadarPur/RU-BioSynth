# Cost
s_coding_region = float('inf')      # stop codon
o_coding_region = 0.                # origin
w_coding_region = 1e+15             # changes codons
x_coding_region = 1.                # does not change codons

s_non_coding_region = 500.         # stop codon
o_non_coding_region = 0.           # origin
w_non_coding_region = 100.         # changes codons
x_non_coding_region = 1.           # does not change codons

# # Symmetric amino acids scoring scheme - 1 aa
# Tryptophan = {"TGG":  [
#     dict(A=w,   T=o,    C=w,    G=w),
#     dict(A=s,   T=w,    C=w,    G=o),
#     dict(A=s,   T=w,    C=w,    G=o)]
#     }
#
# # start codon
# Methionine = {"ATG" : [
#     dict(A=o,   T=w,    C=w,    G=w),
#     dict(A=w,   T=o,    C=w,    G=w),
#     dict(A=w,   T=w,    C=w,    G=o)]
#     }
#
# # Symmetric amino acids scoring scheme - 2 aa
# Phenylalanine = {
#     "TTT": [
#         dict(A=w,   T=o,    C=w,    G=w),
#         dict(A=w,   T=o,    C=w,    G=w),
#         dict(A=w,   T=o,    C=x,    G=w)],
#     "TTC": [
#         dict(A=w,   T=o,    C=w,    G=w),
#         dict(A=w,   T=o,    C=w,    G=w),
#         dict(A=w,   T=x,    C=o,    G=w)]
#     }
#
# Histidine = {
#     "CAT": [
#         dict(A=w,   T=w,    C=o,    G=w),
#         dict(A=o,   T=w,    C=w,    G=w),
#         dict(A=w,   T=o,    C=x,    G=w)],
#     "CAC": [
#         dict(A=w,   T=w,    C=o,    G=w),
#         dict(A=o,   T=w,    C=w,    G=w),
#         dict(A=w,   T=x,    C=o,    G=w)]
#     }
#
# Asparagine = {
#     "AAT": [
#         dict(A=o,   T=w,    C=w,    G=w),
#         dict(A=o,   T=w,    C=w,    G=w),
#         dict(A=w,   T=o,    C=x,    G=w)],
#     "AAC": [
#         dict(A=o,   T=w,    C=w,    G=w),
#         dict(A=o,   T=w,    C=w,    G=w),
#         dict(A=w,   T=x,    C=o,    G=w)]
#     }
#
# Aspartic_acid = {
#     "GAT": [
#         dict(A=w,   T=w,    C=w,    G=o),
#         dict(A=o,   T=w,    C=w,    G=w),
#         dict(A=w,   T=o,    C=x,    G=w)],
#     "GAC": [
#         dict(A=w,   T=w,    C=w,    G=o),
#         dict(A=o,   T=w,    C=w,    G=w),
#         dict(A=w,   T=x,    C=o,    G=w)]
#     }
#
# Tyrosine = {
#     "TAT": [
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=s,     T=o,    C=x,    G=s)],
#     "TAC": [
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=s,     T=x,    C=o,    G=s)]
#     }
#
# Glutamine = {
#     "CAA": [
#         dict(A=w,     T=s,    C=o,    G=w),
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=o,     T=w,    C=w,    G=x)],
#     "CAG": [
#         dict(A=w,     T=s,    C=o,    G=w),
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=x,     T=w,    C=w,    G=o)]
#     }
#
# Lysine = {
#     "AAA": [
#         dict(A=o,     T=s,    C=w,    G=w),
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=o,     T=w,    C=w,    G=x)],
#     "AAG": [
#         dict(A=o,     T=s,    C=w,    G=w),
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=x,     T=w,    C=w,    G=o)]
#     }
#
# Glutamic_acid = {
#     "GAA": [
#         dict(A=w,     T=s,    C=w,    G=o),
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=o,     T=w,    C=w,    G=x)],
#     "GAG": [
#         dict(A=w,     T=s,    C=w,    G=o),
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=x,     T=w,    C=w,    G=o)]
#     }
#
# Cysteine = {
#     "TGT": [
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=o,    C=x,    G=w)],
#     "TGC": [
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=x,    C=o,    G=w)]
#     }
#
# # Symmetric amino acids scoring scheme - 3 aa
# Isoleucine = {
#     "ATT": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=o,     T=x,    C=x,    G=w)],
#     "ATC": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=o,     T=x,    C=x,    G=w)],
#     "ATA": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=o,     T=x,    C=x,    G=w)]
#     }
#
# # Symmetric amino acids scoring scheme - 4 aa
# Alanine = {
#     "GCT": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=o,    C=x,    G=x)],
#     "GCC": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "GCA": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=o,     T=x,    C=x,    G=x)],
#     "GCG": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=x,    C=x,    G=o)]
#     }
#
# Proline = {
#     "CCT": [
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=o,    C=x,    G=x)],
#     "CCC": [
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "CCA": [
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=o,     T=x,    C=x,    G=x)],
#     "CCG": [
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=x,    C=x,    G=o)]
#     }
#
# Threonine = {
#     "ACT": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=o,    C=x,    G=x)],
#     "ACC": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "ACA": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=o,     T=x,    C=x,    G=x)],
#     "ACG": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=x,    C=x,    G=o)]
#     }
#
# Valine = {
#     "GTT": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=x,     T=o,    C=x,    G=x)],
#     "GTC": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "GTA": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=o,     T=x,    C=x,    G=x)],
#     "GTG": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=x,     T=x,    C=x,    G=o)]
#     }
#
# # Non-Symmetric amino acids scoring scheme with 4 codons
# Glycine = {
#     "GGT": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=x,     T=o,    C=x,    G=x)],
#     "GGC": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "GGA": [
#         dict(A=w,     T=s,    C=w,    G=o),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=o,     T=x,    C=x,    G=x)],
#     "GGG": [
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=x,     T=x,    C=x,    G=o)]
#     }
#
# # Non-Symmetric amino acids scoring scheme with 6 codons
# Arginine = {
#     "CGT": [
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=x,     T=o,    C=x,    G=x)],
#     "CGC": [
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "CGA": [
#         dict(A=x,     T=s,    C=o,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "CGG": [
#         dict(A=x,     T=w,    C=o,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=x,     T=x,    C=x,    G=o)],
#     "AGA": [
#         dict(A=o,     T=s,    C=x,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=o,     T=w,    C=w,    G=x)],
#     "AGG": [
#         dict(A=o,     T=w,    C=x,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=x,     T=w,    C=w,    G=o)]
#     }
#
# Serine = {
#     "TCT": [
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=o,    C=x,    G=x)],
#     "TCC": [
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "TCA": [
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=w,     T=w,    C=o,    G=s),
#         dict(A=o,     T=x,    C=x,    G=x)],
#     "TCG": [
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=x,     T=x,    C=x,    G=o)],
#     "AGT": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=o,    C=x,    G=w)],
#     "AGC": [
#         dict(A=o,     T=w,    C=w,    G=w),
#         dict(A=w,     T=w,    C=w,    G=o),
#         dict(A=w,     T=x,    C=o,    G=w)]
#     }
#
# Leucine = {
#     "CTT": [
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=x,     T=o,    C=x,    G=x)],
#     "CTC": [
#         dict(A=w,     T=w,    C=o,    G=w),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=x,     T=x,    C=o,    G=x)],
#     "CTA": [
#         dict(A=w,     T=x,    C=o,    G=w),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=o,     T=x,    C=x,    G=x)],
#     "CTG": [
#         dict(A=w,     T=x,    C=o,    G=w),
#         dict(A=w,     T=o,    C=w,    G=w),
#         dict(A=x,     T=x,    C=x,    G=o)],
#     "TTA": [
#         dict(A=w,     T=o,    C=x,    G=w),
#         dict(A=s,     T=o,    C=w,    G=s),
#         dict(A=w,     T=o,    C=x,    G=w)],
#     "TTG": [
#         dict(A=w,     T=o,    C=x,    G=w),
#         dict(A=s,     T=o,    C=w,    G=w),
#         dict(A=w,     T=x,    C=o,    G=w)]
#     }
#
# # stop codons
# Stop = {
#     "TAA": [
#         dict(A=s, T=o, C=s, G=s),
#         dict(A=o, T=s, C=s, G=x),
#         dict(A=o, T=s, C=s, G=x)],
#     "TAG": [
#         dict(A=s, T=o, C=s, G=s),
#         dict(A=o, T=s, C=s, G=s),
#         dict(A=x, T=s, C=s, G=o)],
#     "TGA": [
#         dict(A=s, T=o, C=s, G=s),
#         dict(A=x, T=s, C=s, G=o),
#         dict(A=o, T=s, C=s, G=s)]
#     }
#
# C = [
#     Tryptophan,
#     Methionine,
#     Phenylalanine,
#     Histidine,
#     Asparagine,
#     Aspartic_acid,
#     Tyrosine,
#     Glutamine,
#     Lysine,
#     Glutamic_acid,
#     Cysteine,
#     Isoleucine,
#     Alanine,
#     Proline,
#     Threonine,
#     Valine,
#     Glycine,
#     Arginine,
#     Serine,
#     Leucine,
#     Stop
# ]
