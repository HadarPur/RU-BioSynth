from collections import defaultdict, deque
from typing import Callable, Set, Tuple, Union
from utils.elimination_utils import EliminationUtils


class FSM:
    """
    A class for performing state reduction operations and implementing a Finite State Machine (FSM).
    """

    def __init__(self, unwanted_patterns, alphabet):
        """
        Initializes an FSM object with a set of unwanted patterns and an alphabet.

        Parameters:
            unwanted_patterns (set of str): Set of unwanted patterns.
            alphabet (set of str): Alphabet of symbols for the FSM.
        """
        self.alphabet = alphabet
        self.unwanted_patterns = unwanted_patterns
        self.elimination_utils = EliminationUtils()
        self.pref_P = self.elimination_utils.get_prefixes(self.unwanted_patterns)
        self.v_init = ''

    def f(self, current_state, sigma):
        """
        Transition function to determine the next state given the current state and symbol.

        Parameters:
            current_state (str): Current state in the FSM.
            sigma (str): Input symbol.

        Returns:
            str or None: The next state if valid, or None if it leads to an unwanted pattern.
        """
        v_sigma = f"{current_state}{sigma}"

        # Check if the new state has an unwanted suffix
        if self.elimination_utils.has_suffix(v_sigma, self.unwanted_patterns):
            return None

        # Find the longest valid suffix in the prefix patterns g
        return self.elimination_utils.longest_suffix_in_set(v_sigma, self.pref_P)

    def generate(self):
        """
        Breadth-first search to generate valid sequences using a queue.

        Returns:
            - transition_back_tracker - mapping of {(new_state, symbol) | such that transition_function(current_state, symbol) = new_state} for each current_state.
        """

        state_queue = deque([(self.v_init, '')])  # Initialize the queue with (current_state, sequence)
        visited_states = set()  # Keep track of visited states

        transition_back_tracker = defaultdict(set)

        while state_queue:
            current_state, sequence = state_queue.popleft()

            # Check if the current state has been visited before
            if current_state in visited_states:
                continue

            visited_states.add(current_state)

            for symbol in self.alphabet:
                new_state = self.f(current_state, symbol)
                if new_state is not None:
                    new_sequence = sequence + symbol
                    transition_back_tracker[new_state].add((current_state, symbol))
                    state_queue.append((new_state, new_sequence))

        return transition_back_tracker
