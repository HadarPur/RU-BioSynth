from collections import deque
from itertools import product


def kmp_based_fsm(unwanted_patterns, sigma):
    """
    Constructs the FSM by calculating the states and transition function.

    Args:
        unwanted_patterns (set): The set of unwanted patterns.
        sigma (set): The alphabet of allowed characters.

    Returns:
        V (set): The set of states in the FSM.
        f (dict): The transition function of the FSM, mapping (state, character) pairs to new states.
        g (dict): A helper function used to compute the transition function.
    """

    f = {}
    g = {}
    states = list()
    epsilon = ''

    # Prefix elongation and invalid transitions
    for p in unwanted_patterns:
        for j in range(1, len(p) + 1):
            f[(p[:j - 1], p[j - 1])] = p[:j]
        f[(p[:- 1], p[- 1])] = None  # Invalid transition into complete pattern

    # Computing state space V and the functions f and g
    state_queue = deque()
    states.append(epsilon)
    for s in sigma:
        if (epsilon, s) not in f:
            f[(epsilon, s)] = epsilon
        if f[(epsilon, s)] == s:
            g[s] = epsilon
            state_queue.append(s)

    # Efficient BFS State Processing in FSM Pattern Matching
    while state_queue:
        v = state_queue.popleft()
        states.append(v)

        for s in sigma:
            if f[g[v], s] is None:
                f[(v, s)] = None
            if (v, s) not in f:
                f[(v, s)] = f[(g[v], s)]
            if f[(v, s)] == v + s:
                g[v + s] = f[(g[v], s)]
                state_queue.append(v + s)

    return epsilon, states, f, g


def pairwise_kmp_fsm(unwanted_patterns, sigma):
    """
    Constructs the FSM by calculating the states and transition function.

    Args:
        unwanted_patterns (set): The set of unwanted patterns.
        sigma (list): The alphabet of allowed characters.

    Returns:
        pair_states (set): The set of pairwise bases in the FSM.
        states (set): The full state space of the FSM.
        f (dict): The transition function of the FSM.
    """

    # Initialize dictionaries for the transition (f) and failure (g) functions
    f = {}
    states = set()

    # Generate all bigrams from the alphabet
    pair_states = [x + y for x in sigma for y in sigma]

    # Initialize states based on bigrams instead of '' (empty string), A, T
    for v in pair_states:
        for s in sigma:
            if (v, s) not in f:
                f[(v, s)] = v[-1] + s
                states.add(v)

    # Prefix elongation and invalid transitions
    for p in unwanted_patterns:
        for j in range(3, len(p) + 1):
            f[(p[:j - 1], p[j - 1])] = p[:j]
            states.add(p[:j - 1])
        f[(p[:- 1], p[- 1])] = None  # Invalid transition into complete pattern

    for v in states:
        for s in sigma:
            if (v, s) not in f:
                f[(v, s)] = v[-1:] + s
            if v[-2:] + s in states:
                f[(v, s)] = v[-2:] + s

    return pair_states, states, f


class FSM:
    """
    A class representing a finite state machine (FSM) for eliminating unwanted patterns from a sequence.

    Attributes:
        sigma (set): The alphabet of allowed characters in the sequence.
        unwanted_patterns (set): The set of unwanted patterns to be eliminated.
        V (set): The set of states in the FSM.
        f (dict): The transition function of the FSM, mapping (state, character) pairs to new states.
        g (dict): A helper function used to compute the transition function.

    Methods:
        __init__(self, unwanted_patterns, alphabet): Initializes the FSM with the given unwanted patterns and alphabet.
        calculate_fsm(self, P, Σ): Constructs the FSM by calculating the states and transition function.
    """

    def __init__(self, unwanted_patterns, alphabet):
        """
        Initializes the FSM with the given unwanted patterns and alphabet.

        Args:
            unwanted_patterns (set): The set of unwanted patterns to be eliminated.
            alphabet (set): The alphabet of allowed characters in the sequence.
        """
        self.sigma = alphabet
        self.unwanted_patterns = unwanted_patterns

        # self.initial_states, self.V, self.f, self.g = kmp_based_fsm(self.unwanted_patterns, self.sigma)
        self.pair_states, self.V, self.f = pairwise_kmp_fsm(self.unwanted_patterns, self.sigma)


