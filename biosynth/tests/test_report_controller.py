"""Tests for biosynth.report.report_controller."""

import os
import io
import tempfile
import unittest
import unittest.mock
from unittest.mock import patch
from jinja2 import Template

from biosynth.data import app_data
from biosynth.report.report_controller import (
    ReportController,
    convert_to_html_list,
)
from biosynth.utils.text_utils import OutputFormat, set_output_format
import biosynth.report.report_controller as mod

class TestConvertToHtmlList(unittest.TestCase):
    def test_dash_items_become_ul(self):
        out = convert_to_html_list("- one\n- two")
        self.assertIn("<ul>", out)
        self.assertIn("<li>one</li>", out)
        self.assertIn("<li>two</li>", out)

    def test_ordered_flag_uses_ol(self):
        out = convert_to_html_list("- one\n- two", ordered=True)
        self.assertIn("<ol>", out)

    def test_non_dash_lines_become_paragraphs(self):
        out = convert_to_html_list("intro\n- bullet")
        self.assertIn("<p>intro</p>", out)
        self.assertIn("<li>bullet</li>", out)


def _seed_app_data():
    """Populate enough InputData / OutputData / EliminationData for
    ReportController to build successfully.
    """
    app_data.InputData.cleaned_dna_sequence = "ATGAAATAA"
    app_data.InputData.coding_indexes = (0, 9)
    app_data.InputData.coding_positions = [1, 2, -3, 1, 2, 3, 1, 2, 3]
    app_data.InputData.unwanted_patterns = {"GGGG"}
    app_data.OutputData.optimized_sequence = "ATGAAATAA"
    app_data.EliminationData.cost_contribution = []
    app_data.EliminationData.cost_substitution = []
    app_data.EliminationData.min_cost = 0.0


class TestReportController(unittest.TestCase):
    def setUp(self):
        _seed_app_data()
        set_output_format(OutputFormat.TERMINAL)

    def test_construction_populates_fields(self):
        ctrl = ReportController()
        self.assertEqual(ctrl.input_seq, "ATGAAATAA")
        self.assertEqual(ctrl.optimized_seq, "ATGAAATAA")
        # Coding range is rendered as "1 - 9".
        self.assertIn("1", ctrl.coding_idx)
        # The unwanted patterns are joined for display.
        self.assertIn("GGGG", ctrl.unwanted_patterns)
        # Highlighted HTML body should contain at least one <span>.
        self.assertIn("<span", ctrl.highlight_input)

    def test_no_coding_region_gives_empty_coding_idx(self):
        app_data.InputData.coding_indexes = None
        app_data.InputData.coding_positions = [0] * 9
        ctrl = ReportController()
        self.assertEqual(ctrl.coding_idx, "")

    def test_create_report_writes_html_and_returns_path(self):
        ctrl = ReportController()
        path = ctrl.create_report(file_date="01-Jan-1970_00-00-00")
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        # The full coding region is rendered as per-character <span>s, so the
        # contiguous sequence string won't appear, but the rendered codons do.
        self.assertIn("ATG", html)  # printed in the diff <pre>
        self.assertIn("AAA", html)
        self.assertIn("TAA", html)
        self.assertIn("GGGG", html)  # unwanted patterns block
        self.assertIn("BioSynth Report", html)  # title rendered
        self.assertIn("01-Jan-1970", html)  # date rendered
        # Cleanup the file we wrote.
        os.remove(path)

    def test_download_report_to_custom_dir(self):
        ctrl = ReportController()
        ctrl.create_report(file_date="01-Jan-1970_00-00-00")
        with tempfile.TemporaryDirectory() as tmp:
            result = ctrl.download_report(path=tmp)
            self.assertIn("BioSynth-Outputs", result)
            # File should exist under the chosen output directory.
            outputs_dir = os.path.join(tmp, "BioSynth-Outputs")
            self.assertTrue(os.path.isdir(outputs_dir))
            files = os.listdir(outputs_dir)
            self.assertTrue(any(f.endswith(".html") for f in files))

        # Cleanup local report file too.
        if os.path.exists(f"output/{ctrl.report_filename}"):
            os.remove(f"output/{ctrl.report_filename}")

    def test_create_report_template_not_found_exits(self):
        # Patch resource_path so jinja2 cannot find the template — the
        # except branch calls handle_critical_error which raises SystemExit
        # under TERMINAL output.

        ctrl = ReportController()

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch.object(
                    mod, "resource_path", return_value="/no/such/dir/missing.html"
            ):
                with self.assertRaises(SystemExit):
                    ctrl.create_report(file_date="01-Jan-1970_00-00-00")

            output = fake_out.getvalue()

        self.assertIn("Template not found", output)

    def test_create_report_generic_exception_returns_none(self):
        # If render raises a non-TemplateNotFound exception and the critical
        # handler is stubbed out (i.e. doesn't exit), create_report falls
        # through and returns None.

        ctrl = ReportController()
        boom = unittest.mock.patch.object(
            Template, "render", side_effect=RuntimeError("render boom")
        )
        no_exit = unittest.mock.patch.object(mod, "handle_critical_error")
        with boom, no_exit:
            self.assertIsNone(
                ctrl.create_report(file_date="01-Jan-1970_00-00-00")
            )

