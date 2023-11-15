import jinja2
import pdfkit
from datetime import datetime
import re


class Report:
    def __init__(self, input_seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns, regions):
        self.input_seq = input_seq
        self.target_seq = target_seq
        self.marked_input_seq = marked_input_seq
        self.marked_target_seq = marked_target_seq
        self.unwanted_patterns = ', '.join(unwanted_patterns)
        self.regions = regions

    def create_report(self):
        client_name = "Hadar Pur"

        today_date = datetime.today().strftime("%d %b %Y, %H:%M:%S")

        context = {'client_name': client_name,
                   'today_date': today_date,
                   'input': self.input_seq,
                   'target': self.target_seq,
                   'item1': self.marked_input_seq,
                   'item2': self.marked_target_seq,
                   'patterns': self.unwanted_patterns,
                   'regions': self.ansi_escape_to_html(self.regions),
                   }

        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)

        html_template = 'report/report2.html'
        template = template_env.get_template(html_template)
        output_text = template.render(context)

        # Save the HTML content to a file
        html_output_file = 'report_output.html'
        with open(html_output_file, 'w', encoding='utf-8') as html_file:
            html_file.write(output_text)

        # If needed, you can still generate a PDF from the HTML file
        output_pdf = 'report_output.pdf'
        pdfkit.from_file(html_output_file, output_pdf, css='report/report2.css',
                         options={"enable-local-file-access": ""})

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

        # Remove ANSI escape codes
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        text = ansi_escape.sub('', text)

        # Replace newline characters with HTML line breaks
        text = text.replace('\n', '<br>')

        # Replace ANSI color codes with HTML styles
        for code, style in color_mapping.items():
            text = text.replace(f'\x1B[{code}m', f'<span style="{style}">')
            text = text.replace('\x1B[0m', '</span>')

        # Wrap the text in a <pre> tag to preserve whitespace
        html = f'<pre>{text}</pre>'
        return html
