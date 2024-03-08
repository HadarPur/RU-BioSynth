from utils.elimination_utils import EliminationUtils
from collections import defaultdict, deque


class FSM:
    def __init__(self, unwanted_patterns, alphabet):
        # Initialize FSM with unwanted patterns and alphabet
        self.alphabet = alphabet
        self.unwanted_patterns = unwanted_patterns

        # Get prefixes from unwanted patterns using EliminationUtils
        self.pref_P = EliminationUtils().get_prefixes(unwanted_patterns)
        self.v_init = ''  # Initialize the initial state as an empty string

        # Initializing tables for f and g
        self.table_f = {}  # Table for function f
        self.table_g = {}  # Table for function g

    def f(self, current_state, sigma):
        # Function f: computes transition for given state and symbol
        v_sigma = f"{current_state}{sigma}"

        # Check if transition for current state and symbol exists in table_f
        if v_sigma in self.table_f:
            return self.table_f[v_sigma]

        # Check if the combined state has a suffix in unwanted patterns
        if EliminationUtils().has_suffix(v_sigma, self.unwanted_patterns):
            self.table_f[v_sigma] = None  # Mark as None if it has an unwanted suffix
        else:
            # Find the longest suffix of v_sigma in the prefix set P
            self.table_f[v_sigma] = EliminationUtils().longest_suffix_in_set(v_sigma, self.pref_P)

        return self.table_f[v_sigma]

    def g(self, state):
        # Function g: computes transition for given state using the prefix set P
        if state in self.table_g:
            return self.table_g[state]

        # Find the longest suffix of the state in the prefix set P
        self.table_g[state] = EliminationUtils().longest_suffix_in_set(state, self.pref_P)
        return self.table_g[state]

    def generate(self):
        transition_back_tracker = defaultdict(set)
        state_queue = deque([(self.v_init, '')])
        V = set()  # Track visited states

        while state_queue:
            current_state, sequence = state_queue.popleft()

            # Check if the current state has been visited before
            if current_state in V:
                continue

            V.add(current_state)

            for symbol in self.alphabet:
                g_current_state = self.g(current_state)
                new_state = self.f(g_current_state, symbol)

                if new_state is not None:
                    new_sequence = sequence + symbol
                    transition_back_tracker[new_state].add((g_current_state, symbol))
                    state_queue.append((new_state, new_sequence))

        return transition_back_tracker  # Return transitions

