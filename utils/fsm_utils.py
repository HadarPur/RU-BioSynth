from graphviz import Digraph
import pandas as pd
import matplotlib.pyplot as plt


def visualize_fsm(states, transitions, initial_state, output_file='fsm_diagram', size="25,20", nodesep=0.3, ranksep=2.0):
    """
    Visualizes the FSM using Graphviz.

    Args:
        states (list): List of states in the FSM.
        transitions (dict): Transition function (state, character) -> new state.
        initial_state (str): The initial state of the FSM.
        output_file (str): The name of the output file for the diagram (without extension).
        size (str): Size of the diagram (width,height) in inches.
        nodesep (float): Spacing between adjacent nodes.
        ranksep (float): Spacing between ranks of nodes.
    """
    fsm_graph = Digraph(format='png')
    fsm_graph.attr(rankdir='LR', size=size, nodesep=str(nodesep), ranksep=str(ranksep))  # Adjust size and spacing

    # Add nodes (states)
    for state in states:
        shape = 'doublecircle' if state is None else 'circle'  # Highlight final states
        fsm_graph.node(str(state), shape=shape)

    # Add initial state marker
    fsm_graph.node("start", shape="point")  # Invisible starting point
    fsm_graph.edge("start", initial_state)

    # Add transitions
    for (state, char), next_state in transitions.items():
        if next_state is not None:  # Exclude transitions leading to invalid states
            fsm_graph.edge(str(state), str(next_state), label=char)

    # Render the FSM diagram
    fsm_graph.render(output_file, cleanup=True)
    print(f"FSM diagram saved as {output_file}.png")



def save_fsm_table_as_image(states, transitions, initial_state, output_file="fsm_table_v1.png"):
    headers = ["State", "Initial"] + sorted(set(char for (_, char) in transitions.keys()))
    table = []

    for state in states:
        row = [state, "Yes" if state == initial_state else "No"]
        for char in headers[2:]:
            next_state = transitions.get((state, char), "-")
            row.append(next_state if next_state is not None else "-")
        table.append(row)

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