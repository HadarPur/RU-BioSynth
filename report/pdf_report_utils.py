import jinja2
from datetime import datetime
import os
from pathlib import Path
import re


class Report:
    def __init__(self, input_seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns, regions, chosen_regions, region_list, selected_region_list, min_cost):
        self.input_seq = input_seq
        self.highlight_input = self.highlight_sequences_to_html(region_list)
        self.target_seq = target_seq
        self.marked_input_seq = marked_input_seq
        self.marked_target_seq = marked_target_seq
        self.unwanted_patterns = ', '.join(unwanted_patterns)
        self.num_of_coding_regions = len(regions)
        self.regions = '<br>'.join(f"[{key}] {value}" for key, value in regions.items())

        if chosen_regions is not None and len(chosen_regions) > 0:
            self.chosen_regions = '''The specific coding regions you wish to exclude from the elimination process are as follows:<br>
                                  ''' + '<br>'.join(f"[{key}] {value}" for key, value in chosen_regions.items()) + '''
                                  <br><br>These coding regions will be classified as non-coding areas within the scoring schemes.'''

            self.highlight_selected = '''<br>The full sequence after selection is:<br>
                                  ''' + ''.join(self.highlight_sequences_to_html(selected_region_list))
        else:
            self.chosen_regions = "No coding regions were selected for exclusion. Continuing with the current settings."
            self.highlight_selected = ""

        self.min_cost = "{}".format('{:.10g}'.format(min_cost))

    def create_report(self):
        today_date = datetime.today().strftime("%d %b %Y, %H:%M:%S")

        context = {'today_date': today_date,
                   'input': self.input_seq,
                   'highlight_input': self.highlight_input,
                   'highlight_selected': self.highlight_selected,
                   'target': self.target_seq,
                   'marked_input_seq': self.marked_input_seq,
                   'marked_target_seq': self.marked_target_seq,
                   'patterns': self.unwanted_patterns,
                   'num_of_coding_regions': self.num_of_coding_regions,
                   'chosen_regions': self.chosen_regions,
                   'regions': self.regions,
                   'cost': self.min_cost
                   }

        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)

        html_template = 'report/report.html'
        template = template_env.get_template(html_template)
        output_text = template.render(context)

        # Save the HTML content to a file
        downloads_path = Path.home() / 'Downloads'
        html_output_file = 'elimination_output.html'
        html_output_path = downloads_path / html_output_file
        with open(html_output_path, 'w', encoding='utf-8') as file:
            file.write(output_text)

        # Get the absolute path of the output PDF/HTML file
        output_html_path = os.path.abspath(html_output_path)

        print(f"\nOutput HTML file report save in: {output_html_path}")

    def highlight_sequences_to_html(self, sequences):
        """
        Converts DNA sequences to HTML markup with highlighted coding regions.

        Parameters:
            sequences (list of dict): List of dictionaries containing sequences and flags for coding regions.

        Returns:
            str: HTML markup with highlighted coding regions.
        """
        html_output = ""

        for seq_info in sequences:
            if seq_info['is_coding_region']:
                coding_sequence = seq_info["seq"]
                coding_sequence_with_spaces = ' '.join(coding_sequence[i:i + 3] for i in range(0, len(coding_sequence), 3))
                html_output += f' <span style="color: {self.get_color_for_coding_region()};">{coding_sequence_with_spaces} </span>'
            else:
                html_output += seq_info['seq']

        return html_output

    def get_color_for_coding_region(self):
        # Define a list of colors or a logic to select colors
        colors = ["red", "blue", "green", "orange", "purple"]  # Example list of colors

        # Implement logic to cycle through colors or choose based on some criteria
        # For example, cycling through a list of colors
        # You can maintain a counter to cycle through the colors
        if not hasattr(self, 'color_counter'):
            self.color_counter = 0

        color = colors[self.color_counter % len(colors)]
        self.color_counter += 1

        return color

