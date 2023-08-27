from collections import deque, defaultdict
from typing import Callable, Generic, Set
from typing import TypeVar
from tqdm import tqdm

StateType = TypeVar('S')


class FSM(Generic[StateType]):
    """A Finite State Machine implementation.
    """

    def __init__(self, alphabet: Set[str], initial_state: StateType, states: Set[StateType],
                 transition_function: Callable[[StateType, str], StateType]):
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.states = states
        self.transition_function = transition_function

    def generate_valid_sequences(self, sequence_length: int) -> tuple[
        Set[str], defaultdict[int, Set[str]], defaultdict[StateType, Set[tuple[StateType, str]]]]:
        """Generate valid sequences of a given length using the deterministic transition function.

        Args:
            sequence_length (int): Length of the sequences to generate.

        Returns:
            tuple[set[str], defaultdict[int, set[str]], defaultdict[StateType, set[tuple[StateType, str]]]]:
                - valid_sequences
                - states_by_sequence_length - states that can generate sequences of a given length.
                - transition_back_tracker - mapping of {(new_state, symbol) | such that transition_function(current_state, symbol) = new_state} for each current_state.
        """
        valid_sequences = set()
        queue = deque([('', self.initial_state)])
        states_by_sequence_length = defaultdict(set)
        transition_back_tracker = defaultdict(set)

        total_states = len(self.alphabet) ** sequence_length  # Total states to process
        processed_states = 0

        with tqdm(total=total_states, desc="Generating Sequences", unit=" state") as pbar:
            while queue:
                sequence, current_state = queue.popleft()  # Use popleft() to pop from the left of deque
                states_by_sequence_length[len(sequence)].add(current_state)

                if len(sequence) == sequence_length:
                    valid_sequences.add(sequence)
                else:
                    for symbol in self.alphabet:
                        new_sequence = ''.join([sequence, symbol])
                        new_state = self.transition_function(current_state, symbol)
                        if new_state is not None:
                            queue.append((new_sequence, new_state))
                            transition_back_tracker[new_state].add((current_state, symbol))

                        processed_states += 1
                        pbar.update(1)

        print('Generation completed.')
        return valid_sequences, states_by_sequence_length, transition_back_tracker




