import jinja2
import pdfkit
from datetime import datetime
import re
import os
from pathlib import Path


class Report:
    def __init__(self, input_seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns, regions, min_cost):
        self.input_seq = input_seq
        self.target_seq = target_seq
        self.marked_input_seq = marked_input_seq
        self.marked_target_seq = marked_target_seq
        self.unwanted_patterns = ', '.join(unwanted_patterns)
        self.regions = self.ansi_escape_to_html(regions)
        self.min_cost = "{}".format('{:.10g}'.format(min_cost))

    def create_report(self):
        today_date = datetime.today().strftime("%d %b %Y, %H:%M:%S")

        context = {'today_date': today_date,
                   'input': self.input_seq,
                   'target': self.target_seq,
                   'item1': self.marked_input_seq,
                   'item2': self.marked_target_seq,
                   'patterns': self.unwanted_patterns,
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

    def ansi_escape_to_html(self, text):
        # Define a mapping of ANSI color codes to HTML styles
        color_mapping = {
            '30': 'color: black;',  # Black
            '31': 'color: red;',  # Red
            '32': 'color: green;',  # Green
            '33': 'color: yellow;',  # Yellow
            '34': 'color: blue;',  # Blue
            '35': 'color: magenta;',  # Magenta
            '36': 'color: cyan;',  # Cyan
            '37': 'color: white;',  # White
        }

        # Replace ANSI color codes with HTML span tags for colors
        for code, style in color_mapping.items():
            text = re.sub(fr'\x1B\[{code}m(.*?)(?=\x1B\[0m|\Z)', f'<span style="{style}">\\1</span>', text, flags=re.DOTALL)

        # Remove ANSI escape codes
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        text = ansi_escape.sub('', text)

        # Replace newline characters with HTML line breaks
        text = text.replace('\n', '<br>')

        # Wrap the text in a span with inline styles for font
        html = f'<span style="color: inherit;">{text}</span>'
        return html
