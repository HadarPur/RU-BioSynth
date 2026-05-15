from biosynth.data.app_data import CostData
from biosynth.utils.text_utils import format_text_bold_for_output


def format_cost(value):
    """Return ``value`` rendered as a trimmed three-decimal float string, or its ``str()`` otherwise."""
    return f"{value:.3f}".rstrip('0').rstrip('.') if isinstance(value, float) else str(value)

def get_elimination_process_description():
    """Return the introductory description of the cost parameters used during elimination."""
    return (
        "Sequence optimization assumes the following cost parameters:"
    )


def get_coding_region_cost_description():
    """Return a bullet-list string describing the coding-region cost parameters."""
    return (
        f"• Non-synonymous substitution cost in coding region: w = {format_cost(CostData.w)}\n"
        f"• Synonymous substitution costs determined by codon usage frequencies from: {CostData.codon_usage_filename}"
    )


def get_non_coding_region_cost_description():
    """Return a bullet-list string describing the non-coding-region transition/transversion costs."""
    return (
        f"• Transition substitution in non-coding sites (A ↔ G, C ↔ T): α = {format_cost(CostData.alpha)}\n"
        f"• Transversion substitution in non-coding sites ({{A,G}} ↔ {{C,T}}): β = {format_cost(CostData.beta)}"
    )

def get_info_usage():
    """Return formatted help text describing the expected target-sequence properties."""
    lines = [
        "Your target sequence should satisfy the following properties:",
        "• The target sequence must contain at most one asterisk character (*) marking the coding region.",
        "• The asterisk character should be immediately followed by a start codon, and the coding region continues",
        "  until the first in-frame stop codon.",
        "• If the target sequence does not contain an asterisk, then the entire target sequence will be treated as non-coding."
    ]

    width = max(len(line.expandtabs(4)) for line in lines)
    boxed_text = []

    for line in lines:
        boxed_text.append("\t" + line.ljust(width))

    return "\n".join(boxed_text)

def get_elimination_info():
    """Return formatted help text explaining the elimination algorithm's cost scheme."""
    lines = [
        "The cost scheme assumed by the optimization algorithm utilizes the following parameters:",
        "",
        "Non-Coding regions:",
        "• If the nucleotide remains unchanged, the cost is 0.",
        "• If the substitution is a transition (A ↔ G or C ↔ T), a low cost of ⍺ is applied.",
        "• If the substitution is a transversion (A,G ↔ C,T), a higher cost of β is applied."
        "\n",
        "Coding regions:",
        "• If the codon remains unchanged, no cost is applied.",
        "• If the codon is modified but still encodes the same amino acid (a synonymous substitution),",
        "  a small substitution-specific cost is applied: the negative logarithm of the proposed codon's",
        "  frequency from the user-specified codon usage table.",
        "• If the codon is changed to encode a different amino acid (a non-synonymous substitution),",
        "  a high uniform cost of w is applied.",
        "",
        "Any substitutions that change the location of a coding region are associated with infinite cost and ",
        "are thus avoided. These include any substitution to the start codon, substitutions that change a non-stop codon",
        "to a stop-codon and substitutions that change the stop codon to a non-stop codon."
    ]

    width = max(len(line.expandtabs(4)) for line in lines)
    boxed_text = []

    for line in lines:
        boxed_text.append("\t" + line.ljust(width))

    return "\n".join(boxed_text)