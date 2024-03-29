from utils.elimination_utils import EliminationUtils
from algorithm.fsm import FSM
from typing import Set
from collections import defaultdict


class EliminateSequence:
    @staticmethod
    def eliminate(S: str, P: Set[str], C: list[dict[str, float]]) -> str:
        print('\n' + '=' * 50)
        print(f"Starting Elimination Process")
        print(f"Unwanted Patterns: {P}")
        print(f"Original Sequence: {S}")
        print('=' * 50 + '\n')

        sequence_length = len(S)
        backtrack = {}

        elimination_utils = EliminationUtils()
        cost_function = elimination_utils.cost_function(C)
        fsm = FSM(P, elimination_utils.alphabet)

        A = defaultdict(lambda: float('inf'))
        A[(0, '')] = 0

        for i in range(1, sequence_length + 1):
            for v in fsm.V:
                for σ in fsm.Σ:
                    u = fsm.f.get((v, σ))
                    if u is not None:
                        cost = A[(i - 1, v)] + cost_function(i, σ)
                        if cost < A[(i, u)]:
                            A[(i, u)] = cost
                            backtrack[(i, u)] = (v, σ)

        min_cost = float('inf')
        final_state = None
        for v in fsm.V:
            if A[(sequence_length, v)] < min_cost:
                min_cost = A[(sequence_length, v)]
                final_state = v

        if min_cost == float('inf'):
            print("No valid sequence found that matches the unwanted pattern list.")
            print('=' * 50 + '\n')
            return None, min_cost

        sequence = []
        current_state = final_state
        for i in range(sequence_length, 0, -1):
            prev_state, char = backtrack[(i, current_state)]
            sequence.append(char)
            current_state = prev_state
        sequence.reverse()

        print("Elimination Process Completed")
        print(f"Modified Sequence: {''.join(sequence)}")
        print(f"Total Cost: {min_cost:.10g}")
        print('=' * 50 + '\n')

        return ''.join(sequence), min_cost
