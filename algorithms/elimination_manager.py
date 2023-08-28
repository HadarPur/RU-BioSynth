from typing import Callable, Generic, Set, Tuple, Union, FrozenSet
from utils.table_cost_utils import DNASequenceAnalyzer
from typing import TypeVar

StateType = TypeVar('S')  # Type variable representing a state
state = str  # Alias for state, representing a string
linear_reduced_state = Tuple[Union[str, None], str]  # Tuple representing a linear reduced state
reduced_state = Tuple[FrozenSet[str], str]  # Tuple representing a reduced state

class Reducer(Generic[StateType]):
    """
    A generic Reducer class that performs state reduction operations.

    Parameters:
        unwanted_patterns (set of str): Set of unwanted patterns.

    Attributes:
        unwanted_patterns (set of str): Set of unwanted patterns.
        initial_state (StateType): The initial state of the reducer.
        states (set of StateType): Set of valid states.
        transition_function (Callable[[StateType, str], StateType]): Transition function for state transitions.
    """

    def __init__(self, unwanted_patterns: Set[str]):
        """
        Initializes a Reducer object with a set of unwanted patterns.

        Parameters:
            unwanted_patterns (set of str): Set of unwanted patterns.
        """
        self.unwanted_patterns = unwanted_patterns
        self.initial_state, self.states, self.transition_function = self.calculate_states_and_transition()

    def calculate_states_and_transition(self) -> Tuple[StateType, Set[StateType], Callable[[StateType, str], StateType]]:
        """
        Calculates the initial state, valid states, and transition function for the reducer.

        Returns:
            tuple: A tuple containing the initial state, set of valid states, and transition function.
        """
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        valid_prefixes = set(w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns))
        initial_state = ''

        def transition_function(current_state: state, sigma: str) -> state:
            """
            Computes the transition to a new state based on the current state and an input symbol.

            Parameters:
                current_state (state): Current state.
                sigma (str): Input symbol.

            Returns:
                state: The new state after transition, or None if transition is not allowed.
            """
            new_state = f"{current_state}{sigma}"
            if dna_analyzer.has_suffix(new_state, self.unwanted_patterns):
                return None
            return dna_analyzer.longest_suffix_in_set(new_state, prefix_patterns)

        return initial_state, valid_prefixes, transition_function

    @property
    def state_type(self) -> TypeVar:
        """
        Returns the type of states used in the reducer.

        Returns:
            TypeVar: Type representing the state.
        """
        return StateType
