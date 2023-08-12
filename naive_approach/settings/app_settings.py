# for development testing

# Unwanted Patterns set
P = {
    "TACA",        # BlaI
    "TATC",        #
    "ATTC",        #
}

# DNA sequence
S = "ATGTACATACAGTAA"     # Y, I, Q

# Cost
inf = float('inf')
o = 0.              # origin
s = inf             # for stop codon: {TAA, TAG, TGA}
w = inf             # changes codons
x = 1.              # does not change codons

C = [
    # start codon ATG
    dict(A=o,   T=w,    C=w,    G=w),
    dict(A=w,   T=o,    C=w,    G=w),
    dict(A=w,   T=x,    C=w,    G=o),

    # TAC
    dict(A=w,   T=o,    C=w,    G=w),
    dict(A=o,   T=w,    C=w,    G=w),
    dict(A=s,   T=x,    C=o,    G=s),

    # ATA
    dict(A=o,   T=w,    C=w,    G=w),
    dict(A=w,   T=o,    C=w,    G=w),
    dict(A=o,   T=x,    C=x,    G=w),

    # CAG
    dict(A=s,   T=s,    C=o,    G=s),
    dict(A=o,   T=w,    C=w,    G=w),
    dict(A=x,   T=w,    C=w,    G=o),

    # stop codon TAA
    dict(A=s,   T=o,    C=s,    G=s),
    dict(A=o,   T=s,    C=s,    G=x),
    dict(A=o,   T=s,    C=s,    G=x),
]