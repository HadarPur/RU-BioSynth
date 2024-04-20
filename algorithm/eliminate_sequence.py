from utils.elimination_utils import EliminationUtils
from algorithm.fsm import FSM
from typing import Set
from collections import defaultdict
from settings.costs_settings import elimination_process_description, coding_region_cost_description, non_coding_region_cost_description


class EliminateSequence:
    @staticmethod
    def eliminate(S: str, P: Set[str], C: list[dict[str, float]]):
        info = f"Starting Elimination Process..."
        info += f"\nUnwanted Patterns: {P}"
        info += f"\nOriginal Sequence: {S}"
        info += f"\n\nElimination Process: \n{elimination_process_description}"
        info += f"\n\nCoding regions: \n{coding_region_cost_description}"
        info += f"\n\nNon-Coding regions: \n{non_coding_region_cost_description}"
        sequence_length = len(S)
        backtrack = {}

        elimination_utils = EliminationUtils()
        cost_function = elimination_utils.cost_function(C)
        fsm = FSM(P, elimination_utils.alphabet)

        A = defaultdict(lambda: float('inf'))
        A[(0, '')] = 0

        for i in range(1, sequence_length + 1):
            for v in fsm.V:
                for s in fsm.sigma:
                    u = fsm.f.get((v, s))
                    if u is not None:
                        cost = A[(i - 1, v)] + cost_function(i, s)
                        if cost < A[(i, u)]:
                            A[(i, u)] = cost
                            backtrack[(i, u)] = (v, s)

        min_cost = float('inf')
        final_state = None
        for v in fsm.V:
            if A[(sequence_length, v)] < min_cost:
                min_cost = A[(sequence_length, v)]
                final_state = v

        if min_cost == float('inf'):
            info += "\nNo valid sequence found that matches the unwanted pattern list."
            return info, None, min_cost

        sequence = []
        current_state = final_state
        for i in range(sequence_length, 0, -1):
            prev_state, char = backtrack[(i, current_state)]
            sequence.append(char)
            current_state = prev_state
        sequence.reverse()

        info += "\nElimination Process Completed!"
        info += f"\nModified Sequence: {''.join(sequence)}"
        info += f"\nTotal Cost: {min_cost:.10g}\n"

        return info, ''.join(sequence), min_cost
