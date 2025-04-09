from data.app_data import CostData

elimination_process_description = 'When considering the costs associated with changing target sequences in both coding and non-coding regions, different expense structures come into play.'

coding_region_cost_description = (
    "In coding regions:\n"
    "- If the codon remains unchanged, no cost is applied.\n"
    "- If the codon is modified but still encodes the same amino acid (a synonymous substitution), a small substitution-specific cost is applied: "
    "the negative logarithm of the proposed codon's frequency from the codon usage table.\n"
    "- If the codon is changed to encode a different amino acid (a non-synonymous substitution), a high uniform cost of "
    f"{CostData.w} is applied.\n"
    "- If the codon is altered to a stop codon, an infinite cost is applied, reflecting that such substitutions are prohibited."
)

non_coding_region_cost_description = (
    f'Within non-coding sections, altering bases within complementary pairs (A/G ↔ C/T) incurs a cost of {CostData.alpha}.'
    f'\nSubstituting one base for another (e.g., A ↔ G or T ↔ C) raises the expense to {CostData.beta}.\n'
)