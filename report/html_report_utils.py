import os

import jinja2

from data.app_data import InputData, EliminationData, OutputData
from settings.costs_settings import elimination_process_description, coding_region_cost_description, \
    non_coding_region_cost_description
from utils.display_utils import SequenceUtils
from utils.file_utils import create_dir, resource_path, save_file
from utils.output_utils import Logger


class ReportController:
    def __init__(self, updated_coding_positions):

        self.input_seq = InputData.dna_sequence
        self.highlight_input = SequenceUtils.highlight_sequences_to_html(InputData.dna_sequence, InputData.coding_indexes)
        self.optimized_seq = OutputData.optimized_sequence

        # Mark non-equal codons
        self.index_seq_str, self.marked_input_seq, self.marked_optimized_seq = SequenceUtils.mark_non_equal_characters(
            InputData.dna_sequence, OutputData.optimized_sequence, updated_coding_positions
        )

        self.unwanted_patterns = ', '.join(InputData.unwanted_patterns)
        self.num_of_coding_regions = len(InputData.coding_indexes)
        self.detailed_changes = '<br>'.join(EliminationData.detailed_changes) if EliminationData.detailed_changes else None
        self.output_text = None
        self.report_filename = None

        if self.num_of_coding_regions > 0:
            self.regions = '''<p><br>The total number of coding regions is ''' + ''.join(
                f'{self.num_of_coding_regions}') + ''', identifies as follows:</p>
                                  <p class="scrollable-paragraph horizontal-scroll">''' + '<br>'.join(
                f"[{key}] {value}" for key, value in InputData.coding_regions_list.items()) + '''</p>'''

            if InputData.excluded_regions_list is not None and len(InputData.excluded_regions_list) > 0:
                self.chosen_regions = '''<p><br>The specific coding regions that the user wish to exclude from the elimination process are as follows:</p>
                                            <p class="scrollable-paragraph horizontal-scroll">''' + '<br>'.join(
                    f"[{key}] {value}" for key, value in InputData.excluded_regions_list.items()) + '''</p>
                                      <p>These coding regions will be classified as non-coding areas.</p>'''

                self.highlight_selected = '''<p><br>The full sequence after selection is:</p>
                                      <p class="scrollable-paragraph">''' + ''.join(
                    SequenceUtils.highlight_sequences_to_html(InputData.dna_sequence, InputData.excluded_coding_indexes)) + '''</p>'''

            else:
                self.chosen_regions = '''<p><br>No coding regions were selected for exclusion. Continuing with the current settings.</p>'''
                self.highlight_selected = ""
        else:
            self.regions = '''<p><br>No coding region was identified in the provided target sequence</p>'''
            self.chosen_regions = ""
            self.highlight_selected = ""

        self.min_cost = "{}".format('{:.10g}'.format(EliminationData.min_cost))

    def create_report(self, file_date):
        context = {'today_date': file_date,
                   'input': self.input_seq,
                   'highlight_input': self.highlight_input,
                   'highlight_selected': self.highlight_selected,
                   'optimized_seq': self.optimized_seq,
                   'index_seq_str': self.index_seq_str,
                   'marked_input_seq': self.marked_input_seq,
                   'marked_optimized_seq': self.marked_optimized_seq,
                   'patterns': self.unwanted_patterns,
                   'num_of_coding_regions': self.num_of_coding_regions,
                   'chosen_regions': self.chosen_regions,
                   'regions': self.regions,
                   'cost': self.min_cost,
                   'elimination_process_description': elimination_process_description.replace("\n", "<br>"),
                   'coding_region_cost_description': coding_region_cost_description.replace("\n", "<br>"),
                   'non_coding_region_cost_description': non_coding_region_cost_description.replace("\n", "<br>"),
                   'detailed_changes': self.detailed_changes
                   }

        try:
            # Get the absolute path to the report.html file
            template_path = resource_path('report/report.html')

            # Create a Jinja2 environment
            template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
            template_env = jinja2.Environment(loader=template_loader)

            # Load the template using the absolute path
            template = template_env.get_template(os.path.basename(template_path))

            self.output_text = template.render(context)

            # Save to a file
            create_dir('output')
            file_name = "BioSynth Report"
            self.report_filename = f'{file_name} - {file_date}.html'

            # for ui usage
            report_local_path = f'output/{self.report_filename}'
            with open(report_local_path, 'w') as file:
                file.write(self.output_text)

            return report_local_path
        except jinja2.exceptions.TemplateNotFound as e:
            Logger.error(f"Template not found: {e}")
            return None
        except Exception as e:
            Logger.error(f"An error occurred: {e}")
            return None

    def download_report(self, path=None):
        path = save_file(self.output_text, self.report_filename, path)
        return path
