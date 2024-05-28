from collections import defaultdict

from algorithm.fsm import FSM
from settings.costs_settings import elimination_process_description, coding_region_cost_description, \
    non_coding_region_cost_description
from utils.date_utils import format_current_date
from utils.elimination_utils import EliminationUtils
from utils.text_utils import format_text_bold_for_output


class EliminateSequence:
    @staticmethod
    def eliminate(seq, unwanted_patterns, cost_table):
        info = f"{format_text_bold_for_output('Starting Elimination Process...')}\n"
        info += f"\n{format_text_bold_for_output('Original Sequence:')}\n{seq}\n"
        info += f"\n{format_text_bold_for_output('Unwanted Patterns:')}\n{', '.join(sorted(unwanted_patterns))}\n"
        info += f"\n{format_text_bold_for_output('Elimination Process:')}\n{elimination_process_description}\n"
        info += f"\n{format_text_bold_for_output('Coding regions:')}\n{coding_region_cost_description}\n"
        info += f"\n{format_text_bold_for_output('Non-Coding regions:')}\n{non_coding_region_cost_description}\n"
        sequence_length = len(seq)
        backtrack = {}

        elimination_utils = EliminationUtils()
        cost_function = elimination_utils.cost_function(cost_table)
        fsm = FSM(unwanted_patterns, elimination_utils.alphabet)

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

        info += f"\n{format_text_bold_for_output('_' * 50)}\n"
        info += f"\n🎉 {format_text_bold_for_output('Congrats!')}\n\n"
        info += "🚀 Elimination Process Completed!\n"
        info += f"📆 {format_current_date()}\n"
        info += f"\n{format_text_bold_for_output('Modified Sequence:')}\n\t{''.join(sequence)}\n"
        info += f"\n{format_text_bold_for_output('Total Cost:')}\n{min_cost:.10g}\n"
        info += f"\n{format_text_bold_for_output('_' * 50)}\n"

        return info, ''.join(sequence), min_cost
