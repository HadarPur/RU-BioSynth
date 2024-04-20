import jinja2
from datetime import datetime
import os
from pathlib import Path
from settings.costs_settings import elimination_process_description, coding_region_cost_description, non_coding_region_cost_description
from utils.display_utils import SequenceUtils


class Report:
    def __init__(self, input_seq, target_seq, marked_input_seq, marked_target_seq, unwanted_patterns, regions, chosen_regions, region_list, selected_region_list, min_cost):
        self.input_seq = input_seq
        self.highlight_input = SequenceUtils.highlight_sequences_to_html(region_list)
        self.target_seq = target_seq
        self.marked_input_seq = marked_input_seq
        self.marked_target_seq = marked_target_seq
        self.unwanted_patterns = ', '.join(unwanted_patterns)
        self.num_of_coding_regions = len(regions)

        if self.num_of_coding_regions > 0:
            self.regions = '''<p>The total number of coding regions - ''' + ''.join(f'{self.num_of_coding_regions}') + ''', identifies as follows:<br>
                                  ''' + '<br>'.join(f"[{key}] {value}" for key, value in regions.items()) + '''</p>'''

            if chosen_regions is not None and len(chosen_regions) > 0:
                self.chosen_regions = '''<p>The specific coding regions that the user wish to exclude from the elimination process are as follows:<br>
                                      ''' + '<br>'.join(f"[{key}] {value}" for key, value in chosen_regions.items()) + '''
                                      <br><br>These coding regions will be classified as non-coding areas.</p>'''

                self.highlight_selected = '''<p>The full sequence after selection is:<br>
                                      ''' + ''.join(SequenceUtils.highlight_sequences_to_html(selected_region_list)) + '''</p>'''

            else:
                self.chosen_regions = '''<p>No coding regions were selected for exclusion. Continuing with the current settings.</p>'''
                self.highlight_selected = ""
        else:
            self.regions = '''<p>No coding region was identified in the provided DNA sequence</p>'''
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

        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)

        html_template = 'report/report.html'
        template = template_env.get_template(html_template)
        output_text = template.render(context)

        # Save the HTML content to a file
        downloads_path = Path.home() / 'Downloads'
        file_name = "Elimination output report"
        today_date = datetime.today().strftime("%d %b %y, %H_%M_%S")
        html_output_file = f'{file_name} {today_date}.html'
        html_output_path = downloads_path / html_output_file
        with open(html_output_path, 'w', encoding='utf-8') as file:
            file.write(output_text)

        # Get the absolute path of the output PDF/HTML file
        output_html_path = os.path.abspath(html_output_path)

        print(f"\nOutput HTML file report save in: {output_html_path}")
