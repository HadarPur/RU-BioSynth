from graphviz import Digraph
import pandas as pd


def visualize_fsm(states, transitions, initial_state, output_file='fsm_diagram', size="20,20", nodesep=0.3, ranksep=2.0):
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


def fsm_to_table(states, transitions, initial_state):
    """
    Converts an FSM representation into a table format.

    Args:
        states (list): List of states in the FSM.
        transitions (dict): Transition function (state, character) -> new state.
        initial_state (str): The initial state of the FSM.

    Returns:
        pd.DataFrame: FSM transition table.
    """
    table_data = []

    for (state, char), next_state in transitions.items():
        if next_state is not None:
            table_data.append([state, char, next_state])

    # Create DataFrame
    df = pd.DataFrame(table_data, columns=["Current State", "Input Symbol", "Next State"])

    # Ensure all states are included in the table, even if they have no transitions
    for state in states:
        if state not in df["Current State"].values:
            df = pd.concat([df, pd.DataFrame([[state, "-", "-"]], columns=df.columns)], ignore_index=True)

    # Mark the initial state
    df["Current State"] = df["Current State"].apply(lambda x: f"-> {x}" if x == initial_state else x)

    return df
