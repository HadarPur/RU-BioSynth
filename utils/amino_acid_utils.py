class AminoAcidScheme:
    def __init__(self, w, o, x, s=None):
        self.w = w
        self.o = o
        self.x = x
        self.s = s

    def get_cost_table_none_coding_region(self):
        return [{
            "A": [dict(A=self.o, T=self.x, C=self.w, G=self.w)],
            "T": [dict(A=self.x, T=self.o, C=self.w, G=self.w)],
            "C": [dict(A=self.w, T=self.w, C=self.o, G=self.x)],
            "G": [dict(A=self.w, T=self.w, C=self.x, G=self.o)]
        }]

    def get_cost_table_coding_region(self):
        # Symmetric amino acids scoring scheme - 1 aa
        Tryptophan = {"TGG": [
            dict(A=self.w, T=self.o, C=self.w, G=self.w),
            dict(A=self.s, T=self.w, C=self.w, G=self.o),
            dict(A=self.s, T=self.w, C=self.w, G=self.o)]
        }

        # start codon
        Methionine = {"ATG": [
            dict(A=self.o, T=self.w, C=self.w, G=self.w),
            dict(A=self.w, T=self.o, C=self.w, G=self.w),
            dict(A=self.w, T=self.w, C=self.w, G=self.o)]
        }

        # Symmetric amino acids scoring scheme - 2 aa
        Phenylalanine = {
            "TTT": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.x, G=self.w)],
            "TTC": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.x, C=self.o, G=self.w)]
        }

        Histidine = {
            "CAT": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.x, G=self.w)],
            "CAC": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.x, C=self.o, G=self.w)]
        }

        Asparagine = {
            "AAT": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.x, G=self.w)],
            "AAC": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.x, C=self.o, G=self.w)]
        }

        Aspartic_acid = {
            "GAT": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.x, G=self.w)],
            "GAC": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.x, C=self.o, G=self.w)]
        }

        Tyrosine = {
            "TAT": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.s, T=self.o, C=self.x, G=self.s)],
            "TAC": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.s, T=self.x, C=self.o, G=self.s)]
        }

        Glutamine = {
            "CAA": [
                dict(A=self.w, T=self.s, C=self.o, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.x)],
            "CAG": [
                dict(A=self.w, T=self.s, C=self.o, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.x, T=self.w, C=self.w, G=self.o)]
        }

        Lysine = {
            "AAA": [
                dict(A=self.o, T=self.s, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.x)],
            "AAG": [
                dict(A=self.o, T=self.s, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.x, T=self.w, C=self.w, G=self.o)]
        }

        Glutamic_acid = {
            "GAA": [
                dict(A=self.w, T=self.s, C=self.w, G=self.o),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.o, T=self.w, C=self.w, G=self.x)],
            "GAG": [
                dict(A=self.w, T=self.s, C=self.w, G=self.o),
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.x, T=self.w, C=self.w, G=self.o)]
        }

        Cysteine = {
            "TGT": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.o, C=self.x, G=self.w)],
            "TGC": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.x, C=self.o, G=self.w)]
        }

        # Symmetric amino acids scoring scheme - 3 aa
        Isoleucine = {
            "ATT": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.o, T=self.x, C=self.x, G=self.w)],
            "ATC": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.o, T=self.x, C=self.x, G=self.w)],
            "ATA": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.o, T=self.x, C=self.x, G=self.w)]
        }

        # Symmetric amino acids scoring scheme - 4 aa
        Alanine = {
            "GCT": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.o, C=self.x, G=self.x)],
            "GCC": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "GCA": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.o, T=self.x, C=self.x, G=self.x)],
            "GCG": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.x, C=self.x, G=self.o)]
        }

        Proline = {
            "CCT": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.o, C=self.x, G=self.x)],
            "CCC": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "CCA": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.o, T=self.x, C=self.x, G=self.x)],
            "CCG": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.x, C=self.x, G=self.o)]
        }

        Threonine = {
            "ACT": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.o, C=self.x, G=self.x)],
            "ACC": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "ACA": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.o, T=self.x, C=self.x, G=self.x)],
            "ACG": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.x, C=self.x, G=self.o)]
        }

        Valine = {
            "GTT": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.x, T=self.o, C=self.x, G=self.x)],
            "GTC": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "GTA": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.o, T=self.x, C=self.x, G=self.x)],
            "GTG": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.x, T=self.x, C=self.x, G=self.o)]
        }

        # Non-Symmetric amino acids scoring scheme with 4 codons
        Glycine = {
            "GGT": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.x, T=self.o, C=self.x, G=self.x)],
            "GGC": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "GGA": [
                dict(A=self.w, T=self.s, C=self.w, G=self.o),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.o, T=self.x, C=self.x, G=self.x)],
            "GGG": [
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.x, T=self.x, C=self.x, G=self.o)]
        }

        # Non-Symmetric amino acids scoring scheme with 6 codons
        Arginine = {
            "CGT": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.x, T=self.o, C=self.x, G=self.x)],
            "CGC": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "CGA": [
                dict(A=self.x, T=self.s, C=self.o, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "CGG": [
                dict(A=self.x, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.x, T=self.x, C=self.x, G=self.o)],
            "AGA": [
                dict(A=self.o, T=self.s, C=self.x, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.o, T=self.w, C=self.w, G=self.x)],
            "AGG": [
                dict(A=self.o, T=self.w, C=self.x, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.x, T=self.w, C=self.w, G=self.o)]
        }

        Serine = {
            "TCT": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.o, C=self.x, G=self.x)],
            "TCC": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "TCA": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.s),
                dict(A=self.o, T=self.x, C=self.x, G=self.x)],
            "TCG": [
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.x, T=self.x, C=self.x, G=self.o)],
            "AGT": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.o, C=self.x, G=self.w)],
            "AGC": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.w, C=self.w, G=self.o),
                dict(A=self.w, T=self.x, C=self.o, G=self.w)]
        }

        Leucine = {
            "CTT": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.x, T=self.o, C=self.x, G=self.x)],
            "CTC": [
                dict(A=self.w, T=self.w, C=self.o, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.x, T=self.x, C=self.o, G=self.x)],
            "CTA": [
                dict(A=self.w, T=self.x, C=self.o, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.o, T=self.x, C=self.x, G=self.x)],
            "CTG": [
                dict(A=self.w, T=self.x, C=self.o, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.x, T=self.x, C=self.x, G=self.o)],
            "TTA": [
                dict(A=self.w, T=self.o, C=self.x, G=self.w),
                dict(A=self.s, T=self.o, C=self.w, G=self.s),
                dict(A=self.w, T=self.o, C=self.x, G=self.w)],
            "TTG": [
                dict(A=self.w, T=self.o, C=self.x, G=self.w),
                dict(A=self.s, T=self.o, C=self.w, G=self.w),
                dict(A=self.w, T=self.x, C=self.o, G=self.w)]
        }

        # stop codons
        Stop = {
            "TAA": [
                dict(A=self.s, T=self.o, C=self.s, G=self.s),
                dict(A=self.o, T=self.s, C=self.s, G=self.x),
                dict(A=self.o, T=self.s, C=self.s, G=self.x)],
            "TAG": [
                dict(A=self.s, T=self.o, C=self.s, G=self.s),
                dict(A=self.o, T=self.s, C=self.s, G=self.s),
                dict(A=self.x, T=self.s, C=self.s, G=self.o)],
            "TGA": [
                dict(A=self.s, T=self.o, C=self.s, G=self.s),
                dict(A=self.x, T=self.s, C=self.s, G=self.o),
                dict(A=self.o, T=self.s, C=self.s, G=self.s)]
        }

        return [
            Tryptophan,
            Methionine,
            Phenylalanine,
            Histidine,
            Asparagine,
            Aspartic_acid,
            Tyrosine,
            Glutamine,
            Lysine,
            Glutamic_acid,
            Cysteine,
            Isoleucine,
            Alanine,
            Proline,
            Threonine,
            Valine,
            Glycine,
            Arginine,
            Serine,
            Leucine,
            Stop
        ]