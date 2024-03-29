from collections import deque


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

        self.V, self.f, self.g = self.calculate_fsm(self.P, self.Σ)

    def calculate_fsm(self, P, Σ):
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

        # Phase 1: Prefix elongation and invalid transitions
        for p in P:
            for j in range(1, len(p) + 1):
                prefix = p[:j]
                if prefix in P:
                    f[(p[:j - 1], p[j - 1])] = None  # Invalid transition into complete pattern
                else:
                    f[(p[:j - 1], p[j - 1])] = prefix

        # Phase 2: Initial state processing
        state_queue = deque()
        V.add('')

        for σ in Σ:
            if ('', σ) not in f:
                f[('', σ)] = ''
            if f[('', σ)] == σ:
                g[σ] = ''
                state_queue.append(σ)

        # Phase 3: Processing the rest of the states
        while state_queue:
            v = state_queue.popleft()
            V.add(v)

            for σ in Σ:
                if f.get((g.get(v, ''), σ)) is None:
                    f[(v, σ)] = None
                else:
                    next_state = f.get((v, σ), f[(g.get(v, ''), σ)])
                    f[(v, σ)] = next_state
                    if next_state not in V and next_state is not None:
                        g[next_state] = f[(g.get(v, ''), σ)]
                        state_queue.append(next_state)

        return V, f, g
