from collections import defaultdict

from algorithm.fsm import FSM
from settings.costs_settings import elimination_process_description, coding_region_cost_description, \
    non_coding_region_cost_description
from utils.cost_utils import EliminationScorerConfig
from utils.date_utils import format_current_date
from utils.text_utils import format_text_bold_for_output
from utils.fsm_utils import visualize_fsm, fsm_to_table
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

        n = len(target_sequence)

        # Initialize utility and FSM classes
        elimination_utils = EliminationScorerConfig()
        cost_function = elimination_utils.cost_function(target_sequence, coding_positions, CostData.codon_usage, CostData.alpha, CostData.beta, CostData.w)
        fsm = FSM(unwanted_patterns, elimination_utils.alphabet)

        visualize_fsm(fsm.V, fsm.f, fsm.initial_state)

        # print("States:", fsm.V)
        # print("\nTransition Function (f):")
        # for key, value in fsm.f.items():
        #     print(f"f{key} -> {value}")
        #
        # print("\nFailure Function (g):")
        # for key, value in fsm.g.items():
        #     print(f"g({key}) -> {value}")

        # Dynamic programming table A, initialized with infinity
        A = defaultdict(lambda: float('inf'))
        A[(0, fsm.initial_state)] = 0

        # A* table for backtracking (stores the previous state and transition symbol)
        A_star = {}

        # Fill the dynamic programming table
        for i in range(1, n + 1):
            for v in fsm.V:
                for sigma in fsm.sigma:
                    u = fsm.f.get((v, sigma))  # Transition to the next state
                    if u is not None:
                        changes, cost_f = cost_function(i - 1, u, sigma)
                        cost = A[(i - 1, v)] + cost_f
                        if cost < A[(i, u)]:
                            A[(i, u)] = cost
                            A_star[(i, u)] = (u, sigma, changes, cost_f)  # Store the best previous state and symbol

        # Find the minimum cost and final state
        min_cost = float('inf')
        final_state = None
        for v in fsm.V:
            if A[(n, v)] < min_cost:
                min_cost = A[(n, v)]
                final_state = v

        if min_cost == float('inf'):
            info += "\nNo valid sequence found that matches the unwanted pattern list."
            return info, None, None, min_cost

        # Reconstruct the sequence with the minimum cost
        sequence = []
        changes_info = []
        current_state = final_state

        # Backtrack to reconstruct the sequence
        for i in range(n, 0, -1):
            if (i, current_state) not in A_star:
                raise ValueError(f"No transition found for position {i} and state {current_state}")

            prev_state, char, changes, cost_f = A_star[(i, current_state)]  # Get the previous state and symbol

            if cost_f > 0:
                print(changes)
                log_change = f"Position {f'{i}:':<10}" \
                        f"\t{f'{changes[0]}':<8}->{f'{changes[1]}':>8}" \
                        f"\t\tCost: {f'{cost_f:.2f}':<7}"
                changes_info.append(log_change)

            sequence.append(char)
            current_state = prev_state

        # Reverse the sequence and changes info
        sequence.reverse()
        changes_info.reverse()

        # Append final information to the info string
        info += f"{format_text_bold_for_output('_' * 50)}\n"
        info += f"\n🎉 {format_text_bold_for_output('Congrats!')}\n\n"
        info += "🚀 Elimination Process Completed!\n"
        info += f"📆 {format_current_date()}\n"
        info += f"\n{format_text_bold_for_output('Optimized Sequence:')}\n{''.join(sequence)}\n"
        info += f"\n{format_text_bold_for_output('Total Cost:')}\n{min_cost}"

        return info, changes_info, ''.join(sequence), min_cost
