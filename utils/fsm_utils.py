from graphviz import Digraph
import pandas as pd
import matplotlib.pyplot as plt


def visualize_fsm_graph(states, transitions, output_file='fsm_diagram', size="20,20", nodesep=0.2, ranksep=1.0):
    """
    Visualizes the FSM using Graphviz.

    Args:
        states (list): List of states in the FSM.
        transitions (dict): Transition function {(state, character) -> new state}.
        initial_states (list): List of initial states of the FSM.
        output_file (str): The name of the output file for the diagram (without extension).
        size (str): Size of the diagram (width, height) in inches.
        nodesep (float): Spacing between adjacent nodes.
        ranksep (float): Spacing between ranks of nodes.
    """
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
