from typing import Callable, Generic, Set, Tuple, Union, FrozenSet
from settings.shared_settings import StateType
from utils.table_cost_utils import DNASequenceAnalyzer

state = str
linear_reduced_state = Tuple[Union[str, None], str]
reduced_state = Tuple[FrozenSet[str], str]

class DNAMitigator(Generic[StateType]):

    def __init__(self, unwanted_patterns: Set[str]):
        self.unwanted_patterns = unwanted_patterns
        self.initial_state, self.states, self.transition_function = self.calculate_states_and_transition()

    def calculate_states_and_transition(self) -> Tuple[StateType, Set[StateType], Callable[[StateType, str], StateType | None]]:
        pass

    @property
    def state_type(self):
        return StateType


class SimpleCleaner(DNAMitigator[state]):
    def __init__(self, unwanted_patterns: set[str]):
        super(SimpleCleaner, self).__init__(unwanted_patterns)

    def calculate_states_and_transition(self) -> Tuple[state, Set[state], Callable[[state, str], state | None]]:
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        valid_states = set(w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns))
        initial_state = ''

        def transition_function(current_state: state, sigma: str) -> state | None:
            new_state = f"{current_state}{sigma}"
            if dna_analyzer.has_suffix(new_state, self.unwanted_patterns):
                return None
            return dna_analyzer.longest_suffix_in_set(new_state, prefix_patterns)

        return initial_state, valid_states, transition_function


class OneOccurrenceReducer(DNAMitigator[linear_reduced_state]):
    def __init__(self, unwanted_patterns: set[str]):
        super(OneOccurrenceReducer, self).__init__(unwanted_patterns)

    def calculate_states_and_transition(self) -> Tuple[linear_reduced_state, Set[linear_reduced_state], Callable[[linear_reduced_state, str], linear_reduced_state | None]]:
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        valid_prefixes = set(w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns))
        valid_states = dna_analyzer.cartesian_product([None] + list(self.unwanted_patterns), valid_prefixes)
        initial_state = (None, '')

        def transition_function(current_state: linear_reduced_state, sigma: str) -> linear_reduced_state | None:
            occurred_pattern, current_sequence = current_state
            new_sequence = f"{current_sequence}{sigma}"

            dna_analyzer = DNASequenceAnalyzer()
            suffix = dna_analyzer.longest_suffix_in_set(new_sequence, self.unwanted_patterns)

            if suffix is not None:  # has_suffix(new_sequence, unwanted_patterns)
                if occurred_pattern is not None:
                    return None

                occurred_pattern = suffix

            u = dna_analyzer.longest_suffix_in_set(new_sequence, prefix_patterns)

            return occurred_pattern, u

        return initial_state, valid_states, transition_function


class MultipleOccurrencesReducer(DNAMitigator[reduced_state]):
    def calculate_states_and_transition(self) -> Tuple[reduced_state, Set[reduced_state], Callable[[reduced_state, str], reduced_state | None]]:
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        occurred_pattern = prefix_patterns.powerset(self.unwanted_patterns)
        valid_prefixes = set(w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns))
        valid_occurrences = dna_analyzer.cartesian_product(occurred_pattern, valid_prefixes)
        initial_state = (frozenset(), '')

        def transition_function(current_state: reduced_state, sigma: str) -> reduced_state | None:
            occurred_patterns, current_sequence = current_state
            new_sequence = f"{current_sequence}{sigma}"
            suffix = dna_analyzer.longest_suffix_in_set(new_sequence, self.unwanted_patterns)

            if suffix is not None:  # has_suffix(w_sigma, P)
                if suffix in occurred_patterns:    # we allow only one occurence
                    return None

                # this is the first occurence
                tmp = set(occurred_patterns)
                tmp.add(suffix)
                occurred_patterns = frozenset(tmp)

                u = dna_analyzer.longest_suffix_in_set(new_sequence, prefix_patterns)

            return occurred_patterns, u

        return initial_state, valid_occurrences, transition_function
