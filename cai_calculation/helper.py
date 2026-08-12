def find_coding_location(sequence):
    """
    Find coding region starting with *ATG and ending at the first stop codon.

    Args:
        sequence (str): DNA sequence containing * before the start codon.

    Returns:
        tuple: (start_position, end_position) or None if not found.
    """

    # Find start codon marker
    start_marker = sequence.find("*")

    if start_marker == -1:
        return None

    # ATG starts after the *
    start = start_marker + 1

    # Search for stop codon in the same reading frame
    for i in range(start + 3, len(sequence), 3):
        codon = sequence[i:i+3]

        if codon in ["TAA", "TAG", "TGA"]:
            end = i + 3
            return start-1, end-1

    return None
