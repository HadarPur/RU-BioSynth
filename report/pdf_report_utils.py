import os
from datetime import datetime
from pathlib import Path

import jinja2

from settings.costs_settings import elimination_process_description, coding_region_cost_description, \
    non_coding_region_cost_description
from utils.display_utils import SequenceUtils
from utils.file_utils import create_dir, resource_path


class Report:
    def __init__(self, input_seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns,
                 original_coding_regions, original_region_list, selected_regions_to_exclude, selected_region_list,
                 min_cost):
        self.input_seq = input_seq
        self.highlight_input = SequenceUtils.highlight_sequences_to_html(original_region_list)
        self.target_seq = target_seq
        self.marked_input_seq = marked_input_seq
        self.marked_target_seq = marked_target_seq
        self.unwanted_patterns = ', '.join(unwanted_patterns)
        self.num_of_coding_regions = len(original_coding_regions)
        self.output_text = None
        self.report_filename = None

        if self.num_of_coding_regions > 0:
            self.regions = '''<p><br>The total number of coding regions is ''' + ''.join(f'{self.num_of_coding_regions}') + ''', identifies as follows:</p>
                                  <p class="scrollable-paragraph horizontal-scroll">''' + '<br>'.join(
                f"[{key}] {value}" for key, value in original_coding_regions.items()) + '''</p>'''

            if selected_regions_to_exclude is not None and len(selected_regions_to_exclude) > 0:
                self.chosen_regions = '''<p><br>The specific coding regions that the user wish to exclude from the elimination process are as follows:</p>
                                            <p class="scrollable-paragraph horizontal-scroll">''' + '<br>'.join(
                    f"[{key}] {value}" for key, value in selected_regions_to_exclude.items()) + '''</p>
                                      <p>These coding regions will be classified as non-coding areas.</p>'''

                self.highlight_selected = '''<p><br>The full sequence after selection is:</p>
                                      <p class="scrollable-paragraph">''' + ''.join(
                    SequenceUtils.highlight_sequences_to_html(selected_region_list)) + '''</p>'''

            else:
                self.chosen_regions = '''<p><br>No coding regions were selected for exclusion. Continuing with the current settings.</p>'''
                self.highlight_selected = ""
        else:
            self.regions = '''<p><br>No coding region was identified in the provided DNA sequence</p>'''
            self.chosen_regions = ""
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
                   'cost': self.min_cost,
                   'elimination_process_description': elimination_process_description,
                   'coding_region_cost_description': coding_region_cost_description,
                   'non_coding_region_cost_description': non_coding_region_cost_description,

                   }

        try:
            # Get the absolute path to the report.html file
            template_path = resource_path('report_template/report.html')

            # Create a Jinja2 environment
            template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
            template_env = jinja2.Environment(loader=template_loader)

            # Load the template using the absolute path
            template = template_env.get_template(os.path.basename(template_path))

            self.output_text = template.render(context)

            # Save to a file
            create_dir('report_output')
            file_name = "Elimination Output Report - "
            today_date = datetime.today().strftime("%d %b %y, %H_%M_%S")
            self.report_filename = f'{file_name} {today_date}.html'

            report_local_path = f'report_output/{self.report_filename}'
            with open(report_local_path, 'w') as file:
                file.write(self.output_text)

            return report_local_path
        except jinja2.exceptions.TemplateNotFound as e:
            print(f"Template not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

            return None

    def download_report(self):
        # Save the HTML content to a file
        downloads_path = Path.home() / 'Downloads'
        html_output_path = downloads_path / self.report_filename
        with open(html_output_path, 'w', encoding='utf-8') as file:
            file.write(self.output_text)

        # Get the absolute path of the output PDF/HTML file
        output_html_path = os.path.abspath(html_output_path)

        return f"\nReport saved to: {output_html_path}"

