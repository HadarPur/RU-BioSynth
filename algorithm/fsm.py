from collections import defaultdict
from typing import Callable, Set, Tuple, Union
from utils.table_cost_utils import DNASequenceAnalyzer


class FSM:
    """
    A combined class that performs state reduction operations and implements a Finite State Machine (FSM).
    """

    def __init__(self, unwanted_patterns: Set[str], alphabet: Set[str]):
        """
        Initializes an FSM object with a set of unwanted patterns and an alphabet.

        Parameters:
            unwanted_patterns (set of str): Set of unwanted patterns.
            alphabet (set of str): Alphabet of symbols for the FSM.
        """
        self.unwanted_patterns = unwanted_patterns
        self.alphabet = alphabet
        self.initial_state, self.states, self.transition_function = self.calculate_states_and_transition()
        self.valid_sequences = set()
        self.states_by_sequence_length = defaultdict(set)
        self.transition_back_tracker = defaultdict(set)
        self.memoization = {}  # Memoization dictionary to store computed transitions

    def calculate_states_and_transition(self) -> Tuple[str, Set[str], Callable[[str, str], Union[None, str]]]:
        """
        Calculates the initial state, valid states, and transition function for the FSM.

        Returns:
            tuple: A tuple containing the initial state, set of valid states, and transition function.
        """
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        valid_prefixes = {w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns)}
        initial_state = ''

        print(f"|V| = {len(valid_prefixes)}")
        print(f"V = {valid_prefixes}")

        def transition_function(current_state, sigma):
            new_state = f"{current_state}{sigma}"
            if dna_analyzer.has_suffix(new_state, self.unwanted_patterns):
                return None
            return dna_analyzer.longest_suffix_in_set(new_state, prefix_patterns)

        return initial_state, valid_prefixes, transition_function

    def dfs(self, sequence, current_state, sequence_length):
        """
        Depth-first search to generate valid sequences.

        Parameters:
            sequence (str): Current sequence being generated.
            current_state (str): Current state in the FSM.
            sequence_length (int): Length of sequences to generate.
        """
        self.states_by_sequence_length[len(sequence)].add(current_state)

        if len(sequence) == sequence_length:
            self.valid_sequences.add(sequence)
        else:
            for symbol in self.alphabet:
                new_state = self.transition_function(current_state, symbol)
                if new_state is not None:
                    new_sequence = sequence + symbol
                    self.transition_back_tracker[new_state].add((current_state, symbol))
                    if (new_state, sequence_length - len(new_sequence)) not in self.memoization:
                        self.dfs(new_sequence, new_state, sequence_length)
                        self.memoization[(new_state, sequence_length - len(new_sequence))] = True

    def generate_valid_sequences(self, sequence_length: int) -> Tuple[set[str], defaultdict[int, set[str]], defaultdict[str, set[Tuple[str, str]]]]:
        """
        Generate valid sequences of a given length using the deterministic transition function.

        Args:
            sequence_length (int): Length of the sequences to generate.

        Returns:
            tuple[set[str], defaultdict[int, set[str]], defaultdict[str, set[Tuple[str, str]]]]:
                - valid_sequences
                - states_by_sequence_length - states that can generate sequences of a given length.
                - transition_back_tracker - mapping of {(new_state, symbol) | such that transition_function(current_state, symbol) = new_state} for each current_state.
        """
        self.dfs('', self.initial_state, sequence_length)
        print('Generation completed.')
        return self.valid_sequences, self.states_by_sequence_length, self.transition_back_tracker
