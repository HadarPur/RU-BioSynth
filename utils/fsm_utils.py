from graphviz import Digraph
import graphviz


# def visualize_fsm(states, transitions, initial_state, output_file='fsm_diagram', size="10,10", nodesep=1.0, ranksep=1.0):
#     """
#     Visualizes the FSM using Graphviz.
#
#     Args:
#         states (list): List of states in the FSM.
#         transitions (dict): Transition function (state, character) -> new state.
#         initial_state (str): The initial state of the FSM.
#         output_file (str): The name of the output file for the diagram (without extension).
#         size (str): Size of the diagram (width,height) in inches.
#         nodesep (float): Spacing between adjacent nodes.
#         ranksep (float): Spacing between ranks of nodes.
#     """
#     fsm_graph = Digraph(format='png')
#     fsm_graph.attr(rankdir='LR', size=size, nodesep=str(nodesep), ranksep=str(ranksep))  # Adjust size and spacing
#
#     # Add nodes (states)
#     for state in states:
#         shape = 'doublecircle' if state is None else 'circle'  # Highlight final states
#         fsm_graph.node(str(state), shape=shape)
#
#     # Add initial state marker
#     fsm_graph.node("start", shape="point")  # Invisible starting point
#     fsm_graph.edge("start", initial_state)
#
#     # Add transitions
#     for (state, char), next_state in transitions.items():
#         if next_state is not None:  # Exclude transitions leading to invalid states
#             fsm_graph.edge(str(state), str(next_state), label=char)
#
#     # Render the FSM diagram
#     fsm_graph.render(output_file, cleanup=True)
#     print(f"FSM diagram saved as {output_file}.png")
#

def visualize_fsm(states, transitions, initial_state, failure_transitions=None):
    output_file = "fsm_diagram"
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir="LR", splines="polyline")  # Top to Bottom layout

    # Add nodes (highlight initial state)
    for state in states:
        if state == initial_state:
            dot.node(state, label=state, shape="doublecircle", style="filled",
                     fillcolor="lightgreen")  # Initial state
        else:
            dot.node(state, label=state, shape="circle", style="filled", fillcolor="lightblue")

    # Add transitions (solid edges for f)
    for (state, symbol), next_state in transitions.items():
        if next_state:  # Ensure there is a valid transition
            dot.edge(state, next_state, label=symbol, color="black")

    # Add failure transitions (dashed red edges)
    if failure_transitions:
        for state, fallback in failure_transitions.items():
            if state != fallback:
                dot.edge(state, fallback, style="dashed", color="red", constraint="false")

    # Render and open the FSM
    dot.render(output_file, view=True)
    print(f"FSM diagram saved as {output_file}.png")

