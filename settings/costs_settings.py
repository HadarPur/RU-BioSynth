from data.app_data import CostData

elimination_process_description = 'When considering the costs associated with changing target sequences in both coding and non-coding regions, different expense structures come into play.'

coding_region_cost_description = (
    f'In coding regions, if the codon remains unchanged, no cost is incurred: cost(i,v,σ) = 0.'
    f'\nIf the codon is altered but still encodes the same amino acid, a small substitution-specific cost of -log(codon_usage[proposed_codon]) is assigned, reflecting the synonymous substitution.'
    f'\nIf the codon is altered to encode a different amino acid, a high uniform cost {CostData.w} is assigned.'
    f'\nIf the codon is altered to a stop codon, an infinite cost is assigned, reflecting that these substitutions are not allowed.'
)

non_coding_region_cost_description = (
    f'Within non-coding sections, altering bases within complementary pairs (A to G, G to A, C to T, T to C) incurs a cost of {CostData.alpha}.'
    f'\nSubstituting one base for another (e.g., A to T or G to C) raises the expense to {CostData.beta}.\n'
)