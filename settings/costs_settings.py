from data.app_data import CostData


def format_cost(value):
    return f"{value:.3f}".rstrip('0').rstrip('.') if isinstance(value, float) else str(value)


def get_elimination_process_description():
    return (
        "When considering the costs associated with changing target sequences in both coding and non-coding regions, "
        "different expense structures come into play."
    )


def get_coding_region_cost_description():
    return (
        "In coding regions:\n"
        " • If the codon remains unchanged, no cost is applied.\n"
        " • If the codon is modified but still encodes the same amino acid (a synonymous substitution), "
        "a small substitution-specific cost is applied: the negative logarithm of the proposed codon's frequency "
        "from the codon usage table.\n"
        f" • If the codon is changed to encode a different amino acid (a non-synonymous substitution), "
        f"a high uniform cost of 𝑤 = {format_cost(CostData.w)} is applied.\n"
        " • If the codon is altered to a stop codon, an infinite cost is applied, reflecting that such substitutions are prohibited."
    )


def get_non_coding_region_cost_description():
    return (
        f"In non-coding regions:\n"
        f" • If the nucleotide remains unchanged, the cost is 0.\n"
        f" • If the substitution is a transition (A ↔ G or C ↔ T), a lower cost of ⍺ = {format_cost(CostData.alpha)} is applied.\n"
        f" • If the substitution is a transversion (A,G ↔ C,T), a higher cost of β = {format_cost(CostData.beta)} is applied.\n"
    )
