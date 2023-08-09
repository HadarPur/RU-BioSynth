from itertools import chain, combinations, product

class DNASequenceAnalyzer:
    def __init__(self):
        self.alphabet = {'A', 'G', 'T', 'C'}

    def cost_function(self, C):

        def cost(i, alphabet):
            return C[i - 1][alphabet]

        return cost

    def get_prefixes(self, s):
        return [s[:i] for i in range(len(s) + 1)]

    def get_suffixes(self, s):
        return [s[i:] for i in range(len(s) + 1)]

    def get_pref(self, P):
        pref_P = set()
        for p in P:
            pref_P.update(self.get_prefixes(p))
        return pref_P

    def has_suffix(self, w, P):
        for suf in self.get_suffixes(w):
            if suf in P:
                return True
        return False

    def longest_suffix_in_set(self, w, arr):
        for suf in self.get_suffixes(w):
            if suf in arr:
                return suf
        return None

    def powerset(self, iterable):
        s = list(iterable)
        return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

    def cartesian_product(self, l1, l2):
        return set(product(l1, l2))

    def get_alphabet(self):
        return self.alphabet
