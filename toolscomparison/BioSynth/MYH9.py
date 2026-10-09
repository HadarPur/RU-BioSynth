from pipeline import run_biosynth

run_biosynth(
    gene_dir="cloning_example",
    gene_name="OQ689691.1",
    pattern_file_name="mcs_unwanted_patterns",
    codon_usage_file_name="codon_usage_ecoli",
)