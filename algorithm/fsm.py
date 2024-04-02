from collections import deque


def calculate_fsm(P, Σ):
    """
    Constructs the FSM by calculating the states and transition function.

    Args:
        P (set): The set of unwanted patterns.
        Σ (set): The alphabet of allowed characters.

    Returns:
        tuple: A tuple containing the set of states (V), the transition function (f), and the helper function (g).
    """
    f = {}
    g = {}
    V = set()
    ε = ''

    # Prefix elongation and invalid transitions
    for p in P:
        for j in range(1, len(p)):
            f[(p[:j - 1], p[j - 1])] = p[:j]
        f[(p[:- 1], p[- 1])] = None  # Invalid transition into complete pattern

    # Computing state space V and the functions f and g
    state_queue = deque()
    V.add(ε)
    for σ in Σ:
        if (ε, σ) not in f:
            f[(ε, σ)] = ε
        if f[(ε, σ)] == σ:
            g[σ] = ε
            state_queue.append(σ)

    # Efficient BFS State Processing in FSM Pattern Matching
    while state_queue:
        v = state_queue.popleft()
        V.add(v)

        for σ in Σ:
            if f.get(g.get(v), σ) is None:
                f[(v, σ)] = None
            if (v, σ) not in f:
                f[(v, σ)] = f.get((g.get(v), σ))
            if f[(v, σ)] == v + σ:
                g[v + σ] = f.get((g.get(v), σ))
                state_queue.append(v + σ)

    return V, f, g


class FSM:
    """
    A class representing a finite state machine (FSM) for eliminating unwanted patterns from a sequence.

    Attributes:
        Σ (set): The alphabet of allowed characters in the sequence.
        P (set): The set of unwanted patterns to be eliminated.
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
        self.Σ = alphabet
        self.P = unwanted_patterns

        self.V, self.f, self.g = calculate_fsm(self.P, self.Σ)
