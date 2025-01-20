from collections import defaultdict

from algorithm.fsm import FSM
from settings.costs_settings import elimination_process_description, coding_region_cost_description, \
    non_coding_region_cost_description
from utils.cost_utils import EliminationScorerConfig
from utils.date_utils import format_current_date
from utils.text_utils import format_text_bold_for_output
from data.app_data import CostData


class EliminationController:
    @staticmethod
    def eliminate(target_sequence, unwanted_patterns, coding_positions):
        # Initialize information string for the elimination process
        info = f"{format_text_bold_for_output('Starting Elimination Process...')}\n"
        info += f"\n{format_text_bold_for_output('Target Sequence:')}\n{target_sequence}\n"
        info += f"\n{format_text_bold_for_output('Unwanted Patterns:')}\n{', '.join(sorted(unwanted_patterns))}\n"

        # Additional descriptions (placeholders for actual descriptions)
        info += f"\n{format_text_bold_for_output('Elimination Process:')}\n{elimination_process_description}\n"
        info += f"\n{format_text_bold_for_output('Coding regions:')}\n{coding_region_cost_description}\n"
        info += f"\n{format_text_bold_for_output('Non-Coding regions:')}\n{non_coding_region_cost_description}\n"

        sequence_length = len(target_sequence)
        backtrack = {}

        # Initialize utility and FSM classes
        elimination_utils = EliminationScorerConfig()
        cost_function = elimination_utils.cost_function(target_sequence, coding_positions, CostData.codon_usage, CostData.alpha, CostData.beta, CostData.w)
        fsm = FSM(unwanted_patterns, elimination_utils.alphabet)

        # Dynamic programming table A, initialized with infinity
        A = defaultdict(lambda: float('inf'))
        A[(0, fsm.initial_state)] = 0

        changes_backtrack = {}
        # Fill the dynamic programming table
        for i in range(1, sequence_length + 1):
            for v in fsm.V:
                for sigma in fsm.sigma:
                    u = fsm.f.get((v, sigma))
                    if u is not None:
                        cost = A[(i - 1, v)] + cost_function(i-1, v, sigma)
                        if cost < A[(i, u)]:
                            A[(i, u)] = cost
                            backtrack[(i, u)] = (v, sigma)
                            changes_backtrack[(i, u)] = cost_function(i, v, sigma)

        # Find the minimum cost and final state
        min_cost = float('inf')
        final_state = None
        for v in fsm.V:
            if A[(sequence_length, v)] < min_cost:
                min_cost = A[(sequence_length, v)]
                final_state = v

        if min_cost == float('inf'):
            info += "\nNo valid sequence found that matches the unwanted pattern list."
            return info, None, None, min_cost

        # Reconstruct the sequence with the minimum cost
        sequence = []
        changes_info = []
        current_state = final_state
        for i in range(sequence_length, 0, -1):
            prev_state, char = backtrack[(i, current_state)]
            cost = changes_backtrack[(i, current_state)]

            if target_sequence[i - 1] != char:
                change = f"Position {f'{i}:':<10}" \
                         f"\t{f'{target_sequence[i - 1]}':<5}->{f'{char}':>5}" \
                         f"\t\tCost: {f'{cost:.2f}':<7}"
                changes_info.append(change)

            sequence.append(char)
            current_state = prev_state

        sequence.reverse()
        changes_info.reverse()

        # Append final information to the info string
        info += f"{format_text_bold_for_output('_' * 50)}\n"
        info += f"\n🎉 {format_text_bold_for_output('Congrats!')}\n\n"
        info += "🚀 Elimination Process Completed!\n"
        info += f"📆 {format_current_date()}\n"
        info += f"\n{format_text_bold_for_output('Optimized Sequence:')}\n{''.join(sequence)}\n"
        info += f"\n{format_text_bold_for_output('Total Cost:')}\n{min_cost:.10g}"

        return info, changes_info, ''.join(sequence), min_cost
