class AminoAcidConfigScheme:
    def __init__(self, w, o, x, s=None):
        self.w = w
        self.o = o
        self.x = x
        self.s = s

    def get_cost_table_non_coding_region(self):
        return [{
            "A": [dict(A=self.o, T=self.w, C=self.w, G=self.x)],
            "T": [dict(A=self.w, T=self.o, C=self.x, G=self.w)],
            "C": [dict(A=self.w, T=self.x, C=self.o, G=self.w)],
            "G": [dict(A=self.x, T=self.w, C=self.w, G=self.o)]
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
                dict(A=self.x, T=self.o, C=self.x, G=self.w)],
            "ATC": [
                dict(A=self.o, T=self.w, C=self.w, G=self.w),
                dict(A=self.w, T=self.o, C=self.w, G=self.w),
                dict(A=self.x, T=self.x, C=self.o, G=self.w)],
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

codon_to_amino_acid = {
    'TTT': 'F',
    'TTC': 'F',  # Phenylalanine (F)
    'TTA': 'L',
    'TTG': 'L',  # Leucine (L)
    'CTT': 'L',
    'CTC': 'L',
    'CTA': 'L',
    'CTG': 'L',  # Leucine (L)
    'ATT': 'I',
    'ATC': 'I',
    'ATA': 'I',  # Isoleucine (I)
    'ATG': 'M',  # Methionine (M) (Start codon)
    'GTT': 'V',
    'GTC': 'V',
    'GTA': 'V',
    'GTG': 'V',  # Valine (V)
    'TCT': 'S',
    'TCC': 'S',
    'TCA': 'S',
    'TCG': 'S',  # Serine (S)
    'CCT': 'P',
    'CCC': 'P',
    'CCA': 'P',
    'CCG': 'P',  # Proline (P)
    'ACT': 'T',
    'ACC': 'T',
    'ACA': 'T',
    'ACG': 'T',  # Threonine (T)
    'GCT': 'A',
    'GCC': 'A',
    'GCA': 'A',
    'GCG': 'A',  # Alanine (A)
    'TAT': 'Y',
    'TAC': 'Y',  # Tyrosine (Y)
    'CAT': 'H',
    'CAC': 'H',  # Histidine (H)
    'CAA': 'Q',
    'CAG': 'Q',  # Glutamine (Q)
    'AAT': 'N',
    'AAC': 'N',  # Asparagine (N)
    'AAA': 'K',
    'AAG': 'K',  # Lysine (K)
    'GAT': 'D',
    'GAC': 'D',  # Aspartic acid (D)
    'GAA': 'E',
    'GAG': 'E',  # Glutamic acid (E)
    'TGT': 'C',
    'TGC': 'C',  # Cysteine (C)
    'TGG': 'W',  # Tryptophan (W)
    'CGT': 'R',
    'CGC': 'R',
    'CGA': 'R',
    'CGG': 'R',  # Arginine (R)
    'AGT': 'S',
    'AGC': 'S',  # Serine (S)
    'AGA': 'R',
    'AGG': 'R',  # Arginine (R)
    'GGT': 'G',
    'GGC': 'G',
    'GGA': 'G',
    'GGG': 'G',  # Glycine (G)
    'TGA': '*',
    'TAA': '*',
    'TAG': '*'  # Stop codon (*)
}


class AminoAcidConfig:

    @staticmethod
    def get_last2(v):
        """
        Extracts the last two bases associated with the FSM state v.

        Parameters:
            v (str): FSM state representation as a string.

        Returns:
            str: Last two bases of the state v.
        """
        # Assuming v contains a string representation of the bases (e.g., "ACGT")
        if len(v) < 2:
            return f'NN{v}'[-2:]  # Default fallback
        return v[-2:]

    @staticmethod
    def get_last3(target_sequence, i):
        """
        Extracts the last three bases in the target sequence ending at position i.

        Parameters:
            target_sequence (str): The full target sequence as a string.
            i (int): Position in the target sequence (0-based index).

        Returns:
            str: Last three bases ending at position i.
        """
        if i < 2:
            raise ValueError("Position i must be at least 2 to extract the last three bases.")
        return target_sequence[i - 2:i + 1]

    @staticmethod
    def encodes_same_amino_acid(proposed_codon, current_codon):
        """
        Checks if two codons encode the same amino acid.

        Args:
            proposed_codon (str): The codon to be tested.
            current_codon (str): The current codon.

        Returns:
            bool: True if both codons encode the same amino acid, False otherwise.
        """
        return codon_to_amino_acid.get(proposed_codon) == codon_to_amino_acid.get(current_codon)

    @staticmethod
    def is_stop_codon(proposed_codon):
        """
        Checks if a given codon is a stop codon.

        Args:
            proposed_codon (str): The codon to be tested.

        Returns:
            bool: True if the codon is a stop codon, False otherwise.
        """
        return codon_to_amino_acid.get(proposed_codon) == '*'

    @staticmethod
    def is_transition(nucleotide1, nucleotide2):
        """
        Checks if the substitution between two nucleotides is a transition mutation.

        Args:
            nucleotide1 (str): The original nucleotide (A, C, G, or T).
            nucleotide2 (str): The proposed nucleotide (A, C, G, or T).

        Returns:
            bool: True if the substitution is a transition mutation, False otherwise.
        """
        purines = {'A', 'G'}
        pyrimidines = {'C', 'T'}

        if nucleotide1 == nucleotide2:
            return False  # No substitution

        return (nucleotide1 in purines and nucleotide2 in purines) or \
            (nucleotide1 in pyrimidines and nucleotide2 in pyrimidines)
