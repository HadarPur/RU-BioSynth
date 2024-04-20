class EliminationUtils:
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
