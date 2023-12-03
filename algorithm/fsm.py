from collections import defaultdict, deque
from typing import Callable, Set, Tuple, Union
from utils.elimination_utils import EliminationUtils


class FSM:
    """
    A class for performing state reduction operations and implementing a Finite State Machine (FSM).
    """

    def __init__(self, unwanted_patterns: Set[str], alphabet: Set[str]):
        """
        Initializes an FSM object with a set of unwanted patterns and an alphabet.

        Parameters:
            unwanted_patterns (set of str): Set of unwanted patterns.
            alphabet (set of str): Alphabet of symbols for the FSM.
        """
        self.alphabet = alphabet
        self.initial_state, self.states, self.transition_function = self.calculate_states_and_transition(unwanted_patterns)

    def calculate_states_and_transition(self, unwanted_patterns: Set[str]) -> Tuple[str, Set[str], Callable[[str, str], Union[None, str]]]:
        """
        Calculates the initial state, valid states, and transition function for the FSM.

        Returns:
            tuple: A tuple containing the initial state, set of valid states, and transition function.
        """
        # Create a DNASequenceAnalyzer object to work with DNA sequences
        elimination_utils = EliminationUtils()

        # Calculate prefix patterns of unwanted patterns
        prefix_patterns = elimination_utils.get_pref(unwanted_patterns)

        # Filter valid prefix patterns that do not have unwanted suffixes
        valid_prefixes = {w for w in prefix_patterns if not elimination_utils.has_suffix(w, unwanted_patterns)}

        # Initialize the initial state to an empty string
        initial_state = ''

        def transition_function(current_state, sigma):
            """
            Transition function to determine the next state given the current state and symbol.

            Parameters:
                current_state (str): Current state in the FSM.
                sigma (str): Input symbol.

            Returns:
                str or None: The next state if valid, or None if it leads to an unwanted pattern.
            """
            new_state = f"{current_state}{sigma}"

            # Check if the new state has an unwanted suffix
            if elimination_utils.has_suffix(new_state, unwanted_patterns):
                return None

            # Find the longest valid suffix in the prefix patterns
            return elimination_utils.longest_suffix_in_set(new_state, prefix_patterns)

        return initial_state, valid_prefixes, transition_function

    def generate(self):
        """
        Breadth-first search to generate valid sequences using a queue.

        Returns:
            - transition_back_tracker - mapping of {(new_state, symbol) | such that transition_function(current_state, symbol) = new_state} for each current_state.
        """

        state_queue = deque([(self.initial_state, '')])  # Initialize the queue with (current_state, sequence)
        visited_states = set()  # Keep track of visited states

        transition_back_tracker = defaultdict(set)

        while state_queue:
            current_state, sequence = state_queue.popleft()

            # Check if the current state has been visited before
            if current_state in visited_states:
                continue

            visited_states.add(current_state)

            for symbol in self.alphabet:
                new_state = self.transition_function(current_state, symbol)
                if new_state is not None:
                    new_sequence = sequence + symbol
                    transition_back_tracker[new_state].add((current_state, symbol))
                    state_queue.append((new_state, new_sequence))

        return transition_back_tracker
