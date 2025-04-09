import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from graphviz import Digraph


def visualize_dp_table(A, sequence_length, fsm, path=None, output_file='dp_heatmap'):
    states = sorted(fsm.V)
    state_to_idx = {state: idx for idx, state in enumerate(states)}

    dp_matrix = np.full((len(states), sequence_length + 1), np.inf)

    for (i, state), cost in A.items():
        if state in state_to_idx:
            dp_matrix[state_to_idx[state], i] = cost

    plt.figure(figsize=(12, 7))
    plt.imshow(dp_matrix, aspect='auto', cmap='coolwarm', origin='lower')

    for i in range(sequence_length + 1):
        for j in range(len(states)):
            cost_value = dp_matrix[j, i]
            if cost_value != np.inf:
                plt.text(i, j, f"{cost_value:.2f}", ha='center', va='center', color='black')

    if path:
        path_x = [i for i, _ in path]
        path_y = [state_to_idx[state] for _, state in path]
        plt.plot(path_x, path_y, marker='o', color='black', markersize=8, linestyle='-', linewidth=2, label="Optimal Path")

    plt.colorbar(label='Cost')
    plt.xticks(ticks=range(sequence_length + 1), labels=range(sequence_length + 1))
    plt.yticks(ticks=range(len(states)), labels=states)

    plt.xlabel("Sequence Position")
    plt.ylabel("FSM State")
    plt.title("Dynamic Programming Table with Optimal Path")
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1))

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"DP table saved as {output_file}")


def visualize_fsm_graph(states, transitions, output_file='fsm_diagram', size="20,20", nodesep=0.2, ranksep=1.0):
    fsm_graph = Digraph(format='png')
    fsm_graph.attr(rankdir='LR', size=size, nodesep=str(nodesep), ranksep=str(ranksep))  # Adjust size and spacing

    # Add nodes (states)
    for state in states:
        shape = 'doublecircle'  # Highlight final states
        fsm_graph.node(str(state), shape=shape)

    # Add transitions
    for (state, char), next_state in transitions.items():
        if next_state is not None:  # Exclude transitions leading to invalid states
            fsm_graph.edge(str(state), str(next_state), label=char)

    # Render the FSM diagram
    fsm_graph.render(output_file, cleanup=True)
    print(f"FSM diagram saved as {output_file}.png")


def visualize_fsm_table(states, transitions, output_file="fsm_table.png"):
    if not states or not transitions:  # Check if states/transitions are empty
        print("Warning: FSM states or transitions are empty. No table will be generated.")
        return

    # Sort states first by length, then alphabetically
    states = sorted(states, key=lambda x: (len(x), x))

    # Get the unique characters from transitions for table headers
    headers = ["State"] + sorted(set(char for (_, char) in transitions.keys()))
    table = []

    # Build the table rows
    for state in states:
        row = [state]
        for char in headers[1:]:
            next_state = transitions.get((state, char), None)
            row.append(next_state if next_state is not None else "Invalid")
        table.append(row)

    if not table:  # Extra safeguard
        print("Warning: No valid FSM transitions to display.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(table, columns=headers)

    # Plot table using Matplotlib
    fig, ax = plt.subplots(figsize=(10, len(states) * 0.5))
    ax.axis("tight")
    ax.axis("off")
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

    # Save image
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"FSM table saved as {output_file}")
