class DNASequenceAnalyzer:
    def __init__(self):
        """
        Initializes a DNASequenceAnalyzer object.
        Sets up the DNA alphabet containing the characters 'A', 'G', 'T', and 'C'.
        """
        self.alphabet = {'A', 'G', 'T', 'C'}

    @staticmethod
    def cost_function(C):
        """
        Creates a cost function based on the given cost matrix C.

        Args:
            C (list of dict): Cost matrix where each entry corresponds to costs for specific characters.

        Returns:
            function: A cost function that takes an index i and a character from the alphabet as arguments,
                      and returns the cost associated with that character at position i in the cost matrix.
        """
        def cost(i, alphabet):
            return C[i - 1][alphabet]

        return cost

    @staticmethod
    def get_prefixes(input_str):
        """
        Computes the set of all prefixes of the given input string.

        Args:
            input_str (str): The input string for which prefixes need to be computed.

        Returns:
            set of str: Set containing all prefixes of the input string.
        """
        prefixes = set()
        for i in range(len(input_str) + 1):
            prefixes.add(input_str[:i])
        return prefixes

    @staticmethod
    def get_suffixes(s):
        """
        Generates a list of all suffixes of the input string s.

        Args:
            s (str): Input string.

        Returns:
            list of str: List of all suffixes of the input string.
        """
        return [s[i:] for i in range(len(s) + 1)]

    def get_pref(self, P):
        """
        Computes the set of all prefixes of strings in the given set P.

        Args:
            P (set of str): Set of input strings.

        Returns:
            set of str: Set containing all prefixes of strings in the input set.
        """
        pref_P = set()
        for p in P:
            pref_P.update(self.get_prefixes(p))

        return pref_P

    def has_suffix(self, w, P):
        """
        Checks if the string w has any suffix that is present in the given set P.

        Args:
            w (str): Input string.
            P (set of str): Set of strings to compare suffixes with.

        Returns:
            bool: True if any suffix of w is present in set P, False otherwise.
        """
        for suf in self.get_suffixes(w):
            if suf in P:
                return True
        return False

    def longest_suffix_in_set(self, w, arr):
        """
        Finds the longest suffix of string w that is present in the given set arr.

        Args:
            w (str): Input string.
            arr (set of str): Set of strings to compare suffixes with.

        Returns:
            str or None: The longest suffix of w that is present in set arr, or None if not found.
        """
        for suf in self.get_suffixes(w):
            if suf in arr:
                return suf
        return None
