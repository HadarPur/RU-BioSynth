from pipeline import run_dnachisel

run_dnachisel(
    gene_dir="maize_yeast_example",
    gene_name="SAUR40",
    pattern_file_name="ACE2_binding_patterns",
    codon_usage_file_name="codon_usage_s_cerevisiae",
    species="s_cerevisiae"
)