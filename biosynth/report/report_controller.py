import os

import jinja2

# Application-specific data and utilities
from biosynth.data.app_data import InputData, EliminationData, OutputData
from biosynth.utils.sequence_display import SequenceUtils
from biosynth.utils.dna_utils import DNAUtils
from biosynth.utils.file_utils import create_dir, resource_path, save_file
from biosynth.utils.info_utils import (
    get_elimination_process_description,
    get_coding_region_cost_description,
    get_non_coding_region_cost_description,
)
from biosynth.utils.text_utils import handle_critical_error, get_execution_mode


# Convert plain text with dash-prefixed lines into HTML <ul>/<ol> + paragraphs
def convert_to_html_list(text: str, ordered=False) -> str:
    lines = text.strip().split("\n")
    list_items = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("-"):
            content = stripped[1:].strip()
            list_items.append(f"<li>{content}</li>")
        else:
            list_items.append(f"<p>{stripped}</p>")  # treat non-list lines as paragraphs

    tag = "ol" if ordered else "ul"
    html = f"<{tag}>\n" + "\n".join(li for li in list_items if li.startswith("<li>")) + f"\n</{tag}>"
    preamble = "\n".join(li for li in list_items if li.startswith("<p>"))
    return preamble + "\n" + html


class ReportController:
    """Controller responsible for constructing and saving the final HTML report.

    Inputs may be supplied as explicit keyword arguments (used by the
    agent pipeline) or left ``None`` to fall back to the module-level
    ``InputData`` / ``OutputData`` / ``EliminationData`` globals — that
    fallback preserves backward compatibility for the legacy CLI and GUI
    code paths that haven't been migrated to the typed-message API.
    """

    def __init__(
        self,
        *,
        cleaned_dna_sequence=None,
        coding_indexes=None,
        coding_positions=None,
        optimized_sequence=None,
        unwanted_patterns=None,
        cost_contribution=None,
        cost_substitution=None,
        min_cost=None,
    ):
        # Resolve each input: explicit kwarg wins, otherwise read globals.
        cleaned_dna_sequence = (
            cleaned_dna_sequence
            if cleaned_dna_sequence is not None
            else InputData.cleaned_dna_sequence
        )
        coding_indexes = (
            coding_indexes if coding_indexes is not None else InputData.coding_indexes
        )
        coding_positions = (
            coding_positions
            if coding_positions is not None
            else InputData.coding_positions
        )
        optimized_sequence = (
            optimized_sequence
            if optimized_sequence is not None
            else OutputData.optimized_sequence
        )
        unwanted_patterns = (
            unwanted_patterns
            if unwanted_patterns is not None
            else InputData.unwanted_patterns
        )
        cost_contribution = (
            cost_contribution
            if cost_contribution is not None
            else EliminationData.cost_contribution
        )
        cost_substitution = (
            cost_substitution
            if cost_substitution is not None
            else EliminationData.cost_substitution
        )
        min_cost = min_cost if min_cost is not None else EliminationData.min_cost

        self.input_seq = cleaned_dna_sequence

        # Save input DNA sequence and visually highlight coding regions
        self.highlight_input = SequenceUtils.highlight_sequences_to_html(
            cleaned_dna_sequence,
            coding_indexes,
            line_length=85
        )

        # Store optimized DNA sequence from backend
        self.optimized_seq = optimized_sequence

        # Mark character-level differences between input and optimized sequences
        self.index_seq_str, self.marked_input_seq, self.marked_optimized_seq = \
            SequenceUtils.mark_non_equal_characters(
                cleaned_dna_sequence,
                optimized_sequence,
                coding_positions
            )

        # Format other user input and results
        self.unwanted_patterns = ', '.join(unwanted_patterns)
        self.coding_idx = "" if coding_indexes is None else f"{coding_indexes[0] + 1} - {coding_indexes[1]}"
        self.cost_contribution = cost_contribution
        self.cost_substitution = cost_substitution

        # These are generated during report creation
        self.output_text = None
        self.report_filename = None

        self.highlight_optimized_selected = SequenceUtils.highlight_differences_with_coding_html(
            cleaned_dna_sequence,
            optimized_sequence,
            coding_positions,
            line_length=85
        )

        # Format cost with good numerical precision
        self.min_cost = f"{min_cost:.10g}"

    def create_report(self, file_date):
        # Build the context dictionary to render the Jinja2 HTML template
        context = {
            'today_date': file_date,
            'input': self.input_seq,
            'patterns': self.unwanted_patterns,
            'highlight_input': self.highlight_input,
            'coding_idx': self.coding_idx,
            'elimination_process_description': convert_to_html_list(get_elimination_process_description()),
            'coding_region_cost_description': convert_to_html_list(get_coding_region_cost_description()),
            'non_coding_region_cost_description': convert_to_html_list(get_non_coding_region_cost_description()),
            'cost': self.min_cost,
            'index_seq_str': self.index_seq_str,
            'marked_input_seq': self.marked_input_seq,
            'marked_optimized_seq': self.marked_optimized_seq,
            'optimized_seq': self.optimized_seq,
            'cost_contribution': self.cost_contribution,
            'cost_substitution': self.cost_substitution,
            'execution_mode' : get_execution_mode(),
            'highlight_optimized_selected': self.highlight_optimized_selected
        }

        try:
            # Load the HTML template using absolute path
            template_path = resource_path('report/report.html')
            template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template(os.path.basename(template_path))

            # Render the HTML using the context dictionary
            self.output_text = template.render(context)

            # Save report to 'output' folder
            create_dir('output')
            self.report_filename = f"BioSynth-Report_{file_date}.html"
            report_local_path = f'output/{self.report_filename}'

            with open(report_local_path, 'w', encoding="utf-8") as file:
                file.write(self.output_text)

            return report_local_path

        except jinja2.exceptions.TemplateNotFound as e:
            handle_critical_error(f"Template not found:\n{e}")
        except Exception as e:
            handle_critical_error(f"Exception has occurred:\n{e}")

        return None

    def download_report(self, path=None):
        # Allow external module (e.g., UI) to download/export the report
        return save_file(self.output_text, self.report_filename, path)
