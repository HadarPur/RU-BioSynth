"""GUI-side validation adapter.

Wraps the CLI validation functions in `biosynth.executions.execution_utils`
so the GUI and CLI share a single source of truth for input rules. On
failure a `QMessageBox.critical` is shown instead of logging to stderr.
"""

from PyQt5.QtWidgets import QMessageBox

from biosynth.executions.execution_utils import (
    is_valid_codon_usage,
    is_valid_dna,
    is_valid_patterns,
)
from biosynth.utils.coding_region import CodingRegionLocator


class GuiValidator:
    """Run input validation and pop QMessageBox dialogs on failure."""

    MUCH_LESS_FACTOR = 10

    def __init__(self, parent):
        self.parent = parent

    def _error(self, message: str):
        QMessageBox.critical(self.parent, "Error", message)

    def validate_target_sequence(self, dna_sequence):
        """Returns (ok, start_codon_index, cleaned_sequence)."""
        if dna_sequence is None:
            self._error("Target sequence file is missing")
            return False, None, None
        if len(dna_sequence) == 0:
            self._error("Target sequence file is empty")
            return False, None, None
        if not is_valid_dna(dna_sequence):
            self._error("Invalid target sequence format in file")
            return False, None, None
        try:
            start_codon_identified, cleaned = CodingRegionLocator.find_start_codon(dna_sequence)
        except ValueError as e:
            self._error(f"Start codon validation failed:\n{e}")
            return False, None, None
        return True, start_codon_identified, cleaned

    def validate_unwanted_patterns(self, unwanted_patterns) -> bool:
        """Return True if the patterns list is present, non-empty, and well-formed."""
        if unwanted_patterns is None:
            self._error("Unwanted patterns file is missing")
            return False
        if len(unwanted_patterns) == 0:
            self._error("Unwanted patterns file is empty")
            return False
        if not is_valid_patterns(unwanted_patterns):
            self._error("Invalid unwanted patterns format in file")
            return False
        return True

    def validate_codon_usage(self, codon_usage) -> bool:
        """Return True if the codon-usage table is present, non-empty, and valid."""
        if codon_usage is None:
            self._error("Codon usage file is missing")
            return False
        if len(codon_usage) == 0:
            self._error("Codon usage file is empty")
            return False
        if not is_valid_codon_usage(codon_usage):
            self._error("Invalid codon usage table format in file")
            return False
        return True

    def validate_cost(self, alpha, beta, w) -> bool:
        """Return True iff α, β, w are positive numbers with α < β and β ≪ w."""
        if not (isinstance(alpha, (int, float)) and alpha > 0):
            self._error(f"Invalid alpha value: α = {alpha}. Must be a positive number.")
            return False
        if not (isinstance(beta, (int, float)) and beta > 0):
            self._error(f"Invalid beta value: β = {beta}. Must be a positive number.")
            return False
        if not (isinstance(w, (int, float)) and w > 0):
            self._error(f"Invalid w value: w = {w}. Must be a positive number.")
            return False
        if not (alpha < beta):
            self._error(
                f"Biological Constraint violated: α < β required "
                f"(α={alpha}, β={beta})."
            )
            return False
        if not (beta * self.MUCH_LESS_FACTOR < w):
            self._error(
                f"Constraint violated: β ≪ w required "
                f"(β={beta}, w={w}, factor={self.MUCH_LESS_FACTOR})."
            )
            return False
        return True
