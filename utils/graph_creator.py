import graphviz


class FSMUtils:
    @staticmethod
    def generate_graph(states, output_format='png', output_filename='state_machine'):
        # Create a new graph
        graph = graphviz.Digraph(format=output_format)

        # Add nodes for each state
        for state, transition in states.items():
            graph.node(state)

        # Add edges based on transitions
        for current_state, transitions in states.items():
            for transition in transitions:
                input_symbol, next_state = transition
                graph.edge(current_state, next_state, label=input_symbol)

        # Render and save the FSM diagram to a file
        output_file = f'{output_filename}'
        graph.render(output_file, view=False)

        print(f"FSM diagram saved as '{output_file}'")



