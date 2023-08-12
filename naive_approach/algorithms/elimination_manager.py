from typing import Callable, Generic, Set, Tuple, Union, FrozenSet
from naive_approach.utils.table_cost_utils import DNASequenceAnalyzer
from typing import TypeVar

StateType = TypeVar('S')
state = str
linear_reduced_state = Tuple[Union[str, None], str]
reduced_state = Tuple[FrozenSet[str], str]


class DNAMitigator(Generic[StateType]):

    def __init__(self, unwanted_patterns: Set[str]):
        self.unwanted_patterns = unwanted_patterns
        self.initial_state, self.states, self.transition_function = self.calculate_states_and_transition()

    def calculate_states_and_transition(self) -> Tuple[StateType, Set[StateType], Callable[[StateType, str], StateType]]:
        pass

    @property
    def state_type(self):
        return StateType


class NoneOccurrenceReducer(DNAMitigator[state]):
    def __init__(self, unwanted_patterns: Set[str]):
        super(NoneOccurrenceReducer, self).__init__(unwanted_patterns)

    def calculate_states_and_transition(self) -> Tuple[state, Set[state], Callable[[state, str], state]]:
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        valid_states = set(w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns))
        initial_state = ''

        print(f"|V| = {len(valid_states)}")
        print(f"V:\n\t{valid_states}")

        def transition_function(current_state: state, sigma: str) -> state:
            new_state = f"{current_state}{sigma}"
            if dna_analyzer.has_suffix(new_state, self.unwanted_patterns):
                return None
            return dna_analyzer.longest_suffix_in_set(new_state, prefix_patterns)

        return initial_state, valid_states, transition_function


class OneOccurrenceReducer(DNAMitigator[linear_reduced_state]):
    def __init__(self, unwanted_patterns: Set[str]):
        super(OneOccurrenceReducer, self).__init__(unwanted_patterns)

    def calculate_states_and_transition(self) -> Tuple[linear_reduced_state, Set[linear_reduced_state], Callable[[linear_reduced_state, str], linear_reduced_state]]:
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        valid_prefixes = set(w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns))
        valid_states = dna_analyzer.cartesian_product([None] + list(self.unwanted_patterns), valid_prefixes)
        initial_state = (None, '')

        print(f"|V| = {len(valid_states)}")

        def transition_function(current_state: linear_reduced_state, sigma: str) -> linear_reduced_state:
            occurred_pattern, current_sequence = current_state
            new_sequence = f"{current_sequence}{sigma}"

            suffix = dna_analyzer.longest_suffix_in_set(new_sequence, self.unwanted_patterns)

            if suffix is not None:  # has_suffix(new_sequence, unwanted_patterns)
                if occurred_pattern is not None:
                    return None

                occurred_pattern = suffix

            u = dna_analyzer.longest_suffix_in_set(new_sequence, prefix_patterns)

            return occurred_pattern, u

        return initial_state, valid_states, transition_function


class MultipleOccurrencesReducer(DNAMitigator[reduced_state]):
    def __init__(self, unwanted_patterns: Set[str]):
        super(MultipleOccurrencesReducer, self).__init__(unwanted_patterns)

    def calculate_states_and_transition(self) -> Tuple[reduced_state, Set[reduced_state], Callable[[reduced_state, str], reduced_state]]:
        dna_analyzer = DNASequenceAnalyzer()
        prefix_patterns = dna_analyzer.get_pref(self.unwanted_patterns)
        occurred_pattern = dna_analyzer.powerset(self.unwanted_patterns)
        valid_prefixes = set(w for w in prefix_patterns if not dna_analyzer.has_suffix(w, self.unwanted_patterns))
        valid_occurrences = dna_analyzer.cartesian_product(occurred_pattern, valid_prefixes)
        initial_state = (frozenset(), '')

        print(f"|V| = {len(valid_prefixes)}")

        def transition_function(current_state: reduced_state, sigma: str) -> reduced_state:
            occurred_patterns, current_sequence = current_state
            new_sequence = f"{current_sequence}{sigma}"
            suffix = dna_analyzer.longest_suffix_in_set(new_sequence, self.unwanted_patterns)

            if suffix is not None:
                if suffix in occurred_patterns:
                    return None

                # this is the first occurence
                tmp = set(occurred_patterns)
                tmp.add(suffix)
                occurred_patterns = frozenset(tmp)

            u = dna_analyzer.longest_suffix_in_set(new_sequence, prefix_patterns)

            return occurred_patterns, u

        return initial_state, valid_occurrences, transition_function
