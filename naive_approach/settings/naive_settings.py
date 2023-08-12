# Unwanted Patterns set
P = {
    "TACA",        # BlaI
    "TATC",        #
    "ATTC",        #
}

# DNA sequence
S = "TACATACAG"     # Y, I, Q

# Cost
inf = float('inf')
o = 0.              # origin
s = inf             # for stop codon: {TAA, TAG, TGA}
w = inf             # changes codons
x = 1.              # does not change codons
C = [
    dict(A=w,   T=o,    C=w,    G=w),
    dict(A=o,   T=w,    C=w,    G=w),
    dict(A=s,   T=x,    C=o,    G=s),
    dict(A=o,   T=w,    C=w,    G=w),
    dict(A=w,   T=o,    C=w,    G=w),
    dict(A=o,   T=x,    C=x,    G=w),
    dict(A=s,   T=s,    C=o,    G=s),
    dict(A=o,   T=w,    C=w,    G=w),
    dict(A=x,   T=w,    C=w,    G=o),
]
