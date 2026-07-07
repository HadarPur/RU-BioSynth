import unittest
from biosynth.data import app_data
from biosynth.utils import descriptions

class TestInfoUtils(unittest.TestCase):

    def test_format_cost_float(self):
        self.assertEqual(descriptions.format_cost(2.0), "2")
        self.assertEqual(descriptions.format_cost(2.3456), "2.346")
        self.assertEqual(descriptions.format_cost(2.300), "2.3")

    def test_format_cost_non_float(self):
        self.assertEqual(descriptions.format_cost("text"), "text")
        self.assertEqual(descriptions.format_cost(123), "123")

    def test_coding_region_description_contains_cost(self):
        app_data.CostData.w = 50.0
        app_data.CostData.codon_usage_filename = "codon.txt"
        desc = descriptions.get_coding_region_cost_description()
        self.assertIn("w = 50", desc)
        self.assertIn("codon.txt", desc)

    def test_non_coding_region_description_contains_alpha_beta(self):
        app_data.CostData.alpha = 1.5
        app_data.CostData.beta = 2.5
        desc = descriptions.get_non_coding_region_cost_description()
        self.assertIn("α = 1.5", desc)
        self.assertIn("β = 2.5", desc)

    def test_info_usage_boxed_format(self):
        result = descriptions.get_info_usage()
        lines = result.splitlines()
        self.assertTrue(all(line.startswith("\t") for line in lines))
        self.assertIn("Your sequence should satisfy the following properties", result)

    def test_elimination_info_boxed_format(self):
        result = descriptions.get_elimination_info()
        lines = [line for line in result.splitlines() if line.strip()]  # ignore empty lines
        self.assertTrue(all(line.startswith("\t") for line in lines))
        self.assertIn("Non-Coding regions:", result)
        self.assertIn("Coding regions:", result)