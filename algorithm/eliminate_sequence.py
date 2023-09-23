from algorithm.fsm import FSM
from utils.elimination_utils import DNASequenceAnalyzer
from typing import Set
from collections import defaultdict


class EliminateSequence:
    # Define a static method 'eliminate' with parameters S, P, and C
    @staticmethod
    def eliminate(S: str, P: Set[str], C: list[dict[str, float]]) -> str:
        # Print a header for the elimination process
        print('\n' + 100 * '*')
        print(f"Eliminating {P} from the sequence...")

        # Calculate the length of sequence 'S'
        n = len(S)

        # Create an instance of 'DNASequenceAnalyzer' to compute sequence costs
        dna_analyzer = DNASequenceAnalyzer()
        cost = dna_analyzer.cost_function(C)

        # Create a finite state machine (FSM) instance ('fsm') to generate P-clean sequences
        fsm = FSM(unwanted_patterns=P, alphabet=dna_analyzer.alphabet)
        transition_back_tracker = fsm.generate()

        # Initialize a list 'A' to hold cost information for each state
        inf = float('inf')
        A_0 = defaultdict(lambda: inf)
        A_0[fsm.initial_state] = 0
        A = [A_0]

        # Create a list 'A_star' for tracking
        A_star = []

        # Loop over sequence lengths from 1 to 'n' and states in 'V_i'
        for i in range(1, n + 1):
            A_i = defaultdict(lambda: inf)
            A_star_i = dict()
            V_i = transition_back_tracker.keys()
            for v in V_i:
                u_star = ''
                sigma_star = ''
                cost_star = inf

                # Iterate over transitions from 'v' to find the minimum cost
                for u, sigma in transition_back_tracker[v]:
                    current_cost = A[i - 1][u] + cost(i, sigma)
                    if current_cost < cost_star:
                        cost_star = current_cost
                        u_star, sigma_star = u, sigma

                A_star_i[v] = (u_star, sigma_star)
                A_i[v] = cost_star

            A_star.append(A_star_i)
            A.append(A_i)

        # Find the state 'v_curr' with the minimum cost at length 'n'
        min_cost = inf
        v_curr = ''
        for v, c in A[n].items():
            if c < min_cost:
                min_cost = c
                v_curr = v

        # Check if there is a valid solution or not
        if min_cost == inf:
            print("No solution!")
            print(100 * '*' + '\n')
            print("No valid sequence matches the unwanted pattern list.")

        # Print the minimum cost
        print("min_cost = {}".format('{:.10g}'.format(min_cost)))

        # Construct the target sequence using A* algorithm
        print(f"Constructing target sequence using A*...")
        target_seq = []

        # Final update to build the target sequence
        for i in reversed(range(n)):
            v_curr, s_i = A_star[i][v_curr]
            target_seq.insert(0, s_i)

        # Print the constructed target sequence
        print(100 * '*' + '\n')
        return ''.join(target_seq)
