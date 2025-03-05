from collections import defaultdict

from algorithm.fsm import FSM
from settings.costs_settings import elimination_process_description, coding_region_cost_description, \
    non_coding_region_cost_description
from utils.cost_utils import EliminationScorerConfig
from utils.date_utils import format_current_date
from utils.text_utils import format_text_bold_for_output
from utils.graphic_utils import visualize_fsm_graph, visualize_fsm_table, visualize_dp_table
from data.app_data import CostData


class EliminationController:
    @staticmethod
    def eliminate(target_sequence, unwanted_patterns, coding_positions):
        # Initialize information string for the elimination process
        info = f"{format_text_bold_for_output('Starting Elimination Process...')}\n"
        info += f"\n{format_text_bold_for_output('Target Sequence:')}\n{target_sequence}\n"
        info += f"\n{format_text_bold_for_output('Unwanted Patterns:')}\n{', '.join(sorted(unwanted_patterns))}\n"

        # Check if unwanted patterns exist
        if not any(x in target_sequence for x in unwanted_patterns):
            info += "\nNo unwanted patterns found. Returning the original sequence."
            return info, None, target_sequence, 0.0  # Return unchanged sequence

        # Additional descriptions (placeholders for actual descriptions)
        info += f"\n{format_text_bold_for_output('Elimination Process:')}\n{elimination_process_description}\n"
        info += f"\n{format_text_bold_for_output('Coding regions:')}\n{coding_region_cost_description}\n"
        info += f"\n{format_text_bold_for_output('Non-Coding regions:')}\n{non_coding_region_cost_description}\n"

        n = len(target_sequence)

        # Initialize utility and FSM classes
        elimination_scorer = EliminationScorerConfig()
        initial_cost_function, cost_function = elimination_scorer.cost_function(target_sequence,
                                                                                coding_positions,
                                                                                CostData.codon_usage,
                                                                                CostData.alpha,
                                                                                CostData.beta, CostData.w)
        fsm = FSM(unwanted_patterns, elimination_scorer.alphabet)

        # Dynamic programming table A, initialized with infinity
        A = defaultdict(lambda: float('inf'))
        # A* table for backtracking (stores the previous state and transition symbol)
        A_star = {}

        # Initialize all bigram states in column 2
        for v in fsm.bigram_states:
            A[(2, v)] = 0  # Initialize as zero cost
            A_star[(2, v)] = (None, None, None, 0.0)  # Initialize A_star with placeholders

        # Fill the initial dynamic programming table (columns 0 and 1 are skipped)
        for i in range(0, 2):
            for v in fsm.bigram_states:
                changes, cost_f = initial_cost_function(i, v)  # Compute cost
                A[(2, v)] += cost_f  # Update cost
                A_star[(2, v)] = (v, v, changes, cost_f)  # Store initial state information

        # Fill the dynamic programming table
        for i in range(3, n + 1):
            for v in fsm.V:
                for sigma in fsm.sigma:
                    u = fsm.f.get((v, sigma))  # Transition to the next state
                    if u is not None:
                        changes, cost_f = cost_function(i - 1, u, sigma)  # Compute cost

                        # Compute cost and update DP table if it's a better path
                        cost = A[(i - 1, v)] + cost_f
                        if cost < A[(i, u)]:
                            A[(i, u)] = cost
                            A_star[(i, u)] = (v, sigma, changes, cost_f)  # Store the best previous state

        # Find the minimum cost and final state
        min_cost = float('inf')
        final_state = None
        for v in fsm.V:
            if A[(n, v)] < min_cost:
                min_cost = A[(n, v)]
                final_state = v

        # If no valid sequence was found
        if min_cost == float('inf'):
            info += "\nNo valid sequence found that avoids the unwanted patterns."
            return info, None, None, min_cost

        # Reconstruct the sequence with the minimum cost
        sequence = []
        changes_info = []
        path = []
        current_state = final_state

        # Backtrack to reconstruct the sequence
        for i in range(n, 1, -1):
            if (i, current_state) not in A_star:
                raise ValueError(f"No transition found for position {i} and state {current_state}")

            prev_state, char, changes, cost_f = A_star[(i, current_state)]  # Get the previous state and symbol

            # Log changes if cost is incurred
            if cost_f > 0:
                log_change = f"Position {i:<10}\t{changes[0]:<8}->{changes[1]:>8}\t\tCost: {cost_f:.2f}"
                changes_info.append(log_change)

            path.append((i, current_state))
            sequence.append(char)
            current_state = prev_state

        # Reverse the sequence and changes info for correct order
        path.reverse()
        sequence.reverse()
        changes_info.reverse()

        visualize_fsm_graph(fsm.V, fsm.f)
        visualize_fsm_table(fsm.V, fsm.f)
        visualize_dp_table(A, n, fsm, path)

        # Append final information to the info string
        info += f"{format_text_bold_for_output('_' * 50)}\n"
        info += f"\n🎉 {format_text_bold_for_output('Congrats!')}\n\n"
        info += "🚀 Elimination Process Completed!\n"
        info += f"📆 {format_current_date()}\n"
        info += f"\n{format_text_bold_for_output('Optimized Sequence:')}\n{''.join(sequence)}\n"
        info += f"\n{format_text_bold_for_output('Total Cost:')}\n{min_cost}"

        return info, changes_info, ''.join(sequence), min_cost
