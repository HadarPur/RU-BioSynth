from utils.elimination_utils import EliminationUtils
from algorithm.fsm import FSM
from typing import Set
from collections import defaultdict
from settings.costs_settings import s_coding_region, w_coding_region, x_coding_region
from settings.costs_settings import w_non_coding_region, x_non_coding_region


class EliminateSequence:
    @staticmethod
    def eliminate(S: str, P: Set[str], C: list[dict[str, float]]) -> str:
        print('\n' + '=' * 50 + '\n')
        print(f"Starting Elimination Process")
        print(f"Unwanted Patterns: {P}")
        print(f"Original Sequence: {S}")
        print('\nWhen considering the costs associated with changing DNA sequences in both coding and non-coding regions, different expense structures come into play.')
        print(f'\nCoding regions:'
              f'\nIn coding regions, a substitution that does not change the amino acid incurs an expense of {x_coding_region}.'
              f'\nA higher cost of {w_coding_region}is associated with substitutions that change the amino acid.'
              f'\nA substitution that converts an amino acid to a (premature) stop codon incurs a very high cost of {s_coding_region}')
        print(f'\nNon-Coding regions:'
              f'\nWithin non-coding sections, altering bases within complementary pairs (A to T, T to A, C to G, G to C) incurs a cost of {x_non_coding_region}.'
              f'\nSubstituting one base for another (e.g., A to G or T to C) raises the expense to {w_non_coding_region}.\n')

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
        print('\n' + '=' * 50 + '\n')

        return ''.join(sequence), min_cost
