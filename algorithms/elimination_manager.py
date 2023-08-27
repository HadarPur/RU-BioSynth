from typing import Callable, Generic, Set, Tuple, Union, FrozenSet
from utils.table_cost_utils import DNASequenceAnalyzer
from typing import TypeVar

StateType = TypeVar('S')
state = str
linear_reduced_state = Tuple[Union[str, None], str]
reduced_state = Tuple[FrozenSet[str], str]


class Reducer(Generic[StateType]):

    def __init__(self, unwanted_patterns: Set[str]):
        self.unwanted_patterns = unwanted_patterns
        self.initial_state, self.states, self.transition_function = self.calculate_states_and_transition()

    def calculate_states_and_transition(self) -> Tuple[StateType, Set[StateType], Callable[[StateType, str], StateType]]:
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        valid_prefixes = set(w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns))
        initial_state = ''

        def transition_function(current_state: state, sigma: str) -> state:
            new_state = f"{current_state}{sigma}"
            if dna_analyzer.has_suffix(new_state, self.unwanted_patterns):
                return None
            return dna_analyzer.longest_suffix_in_set(new_state, prefix_patterns)

        return initial_state, valid_prefixes, transition_function

    @property
    def state_type(self):
        return StateType

