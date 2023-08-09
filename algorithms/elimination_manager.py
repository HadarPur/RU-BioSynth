from typing import Callable, Generic, Set, Tuple, Union, FrozenSet
from settings.shared_settings import StateType

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
    def calculate_states_and_transition(self) -> Tuple[state, Set[state], Callable[[state, str], state | None]]:
        prefix_patterns = {w for w in self.unwanted_patterns if not w in self.unwanted_patterns}
        valid_states = {w for w in prefix_patterns if not any(w.endswith(p) for p in self.unwanted_patterns)}
        initial_state = ''

        def transition_function(current_state: state, sigma: str) -> state | None:
            new_state = f"{current_state}{sigma}"
            if any(new_state.endswith(p) for p in self.unwanted_patterns):
                return None
            return max((p for p in prefix_patterns if new_state.endswith(p)), key=len, default=new_state)

        return initial_state, valid_states, transition_function


class OneOccurrenceReducer(DNAMitigator[linear_reduced_state]):
    def calculate_states_and_transition(self) -> Tuple[linear_reduced_state, Set[linear_reduced_state], Callable[[linear_reduced_state, str], linear_reduced_state | None]]:
        prefix_patterns = {w for w in self.unwanted_patterns if not w in self.unwanted_patterns}
        valid_prefixes = {w for w in prefix_patterns if not any(w.endswith(p) for p in self.unwanted_patterns)}
        valid_states = {(None, w) for w in valid_prefixes}
        initial_state = (None, '')

        def transition_function(current_state: linear_reduced_state, sigma: str) -> linear_reduced_state | None:
            occurred_pattern, current_sequence = current_state
            new_sequence = f"{current_sequence}{sigma}"

            for p in prefix_patterns:
                if new_sequence.endswith(p):
                    if occurred_pattern is not None:
                        return None
                    occurred_pattern = p

            return occurred_pattern, max((p for p in prefix_patterns if new_sequence.endswith(p)), key=len,
                                         default=new_sequence)

        return initial_state, valid_states, transition_function


class MultipleOccurrencesReducer(DNAMitigator[reduced_state]):
    def calculate_states_and_transition(self) -> Tuple[reduced_state, Set[reduced_state], Callable[[reduced_state, str], reduced_state | None]]:
        prefix_patterns = {w for w in self.unwanted_patterns if not w in self.unwanted_patterns}
        valid_prefixes = {w for w in prefix_patterns if not any(w.endswith(p) for p in self.unwanted_patterns)}
        valid_occurrences = frozenset()
        valid_states = {(valid_occurrences, w) for w in valid_prefixes}
        initial_state = (valid_occurrences, '')

        def transition_function(current_state: reduced_state, sigma: str) -> reduced_state | None:
            occurred_patterns, current_sequence = current_state
            new_sequence = f"{current_sequence}{sigma}"

            for p in prefix_patterns:
                if new_sequence.endswith(p):
                    if p in occurred_patterns:
                        return None
                    occurred_patterns = occurred_patterns | {p}

            return occurred_patterns, max((p for p in prefix_patterns if new_sequence.endswith(p)), key=len,
                                          default=new_sequence)

        return initial_state, valid_states, transition_function

