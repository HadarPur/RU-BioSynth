import graphviz
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


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

    @staticmethod
    def generate_table(states, output_format='pdf', output_filename='fsm_table'):
        # Create a new graph
        graph = graphviz.Digraph(format=output_format)

        # Add nodes for each state
        for state, transition in states.items():
            graph.node(state)

        output_file = f'{output_filename}.{output_format}'
        doc = SimpleDocTemplate(output_file, pagesize=letter)

        # Add edges based on transitions
        data = [['Current State', 'Input Symbol', 'Next State']]
        for current_state, transitions in states.items():
            for transition in transitions:
                input_symbol, next_state = transition
                data.append([current_state, input_symbol, next_state])

        # Create the PDF table
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        # Build the PDF document with the table
        elements = [table]
        doc.build(elements)

        print(f"PDF file '{output_file}' generated successfully.")
