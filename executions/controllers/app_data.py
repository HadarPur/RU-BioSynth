class AppData:
    # Input Data
    dna_sequence = ""
    patterns = ""
    codon_usage = ""
    download_location = ""
    optimized_sequence = ""

    # Intermediate Data
    original_region_list = []
    original_coding_regions = {}
    selected_regions_to_exclude = {}
    selected_region_list = []

    # Output Data
    optimized_seq = ""
    index_seq_str = ""
    marked_input_seq = ""
    marked_optimized_seq = ""
    detailed_changes = []
    highlighted_sequence = ""

    # Metadata
    num_of_coding_regions = 0
    min_cost = 0.0