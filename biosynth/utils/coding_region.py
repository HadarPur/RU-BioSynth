min_coding_region_length = 7 * 3  # start_codon_length + stop_codon_length + 5 codons length in the coding area


class CodingRegionLocator:
    """Static helpers for locating coding regions within DNA sequences."""

    @staticmethod
    def find_start_codon(seq):
        """Locate the ``*ATG`` marker in ``seq`` and return its index and cleaned sequence.

        Returns:
            tuple ``(index, cleaned_seq)`` where ``index`` is the position of the
            start codon in the cleaned sequence, or ``(None, seq)`` if no marker
            is present.

        Raises:
            ValueError: If ``*`` is not followed by ``ATG`` or no in-frame stop
                codon follows the start codon.
        """
        stop_codons = {"TAA", "TAG", "TGA"}

        idx = seq.find("*ATG")

        if idx == -1:
            if "*" in seq:
                raise ValueError("'*' present but not followed by ATG")
            return None, seq  # no marker at all

        cleaned_seq = seq[:idx] + seq[idx + 1:]

        # scan in-frame
        for i in range(idx + 3, len(cleaned_seq), 3):
            if cleaned_seq[i:i + 3] in stop_codons:
                return idx, cleaned_seq

        raise ValueError("No in-frame stop codon found after *ATG")

    @staticmethod
    def get_coding_sequence(coding_index, seq):
        """
        Extracts the coding region sequence from the DNA sequence.

        Parameters:
            coding_index (tuple[int, int] | None): (start, end) of the coding region (end exclusive)
            seq (str): DNA sequence (clean, without '*')

        Returns:
            str | None: coding region sequence, or None if no coding region exists
        """
        if coding_index is None:
            return None

        start, end = coding_index
        return seq[start:end]

    @staticmethod
    def get_coding_and_non_coding_regions_positions(clean_seq, atg_index):
        """
        Computes codon positions and a single coding region defined by a given start codon,
        subject to a minimum coding region length.

        Args:
            clean_seq (str): DNA sequence without '*'
            atg_index (int): index of 'A' in the start codon (ATG)

        Returns:
            tuple:
                - codon_positions (list[int])
                - coding_index (tuple[int, int] | None)
                  (start_index, end_index) where end_index is exclusive
        """
        stop_codons = {"TAA", "TAG", "TGA"}
        N = len(clean_seq)

        codon_positions = [0] * N
        start_idx = atg_index

        # Validate start codon
        if start_idx is None or clean_seq[start_idx:start_idx + 3] != "ATG":
            return codon_positions, None

        stop_idx = None

        # Search for first in-frame stop codon
        for j in range(start_idx + 3, N - 2, 3):
            if clean_seq[j:j + 3] in stop_codons:
                candidate_end = j + 3  # exclusive
                stop_idx = candidate_end

        # No valid coding region satisfying length constraint
        if stop_idx is None:
            return codon_positions, None

        # Assign codon positions
        for k in range(start_idx, stop_idx):
            codon_phase = ((k - start_idx) % 3) + 1

            # Special marking: third base of start codon
            if (k - start_idx) < 3 and codon_phase == 3:
                codon_positions[k] = -3
            else:
                codon_positions[k] = codon_phase

        coding_index = (start_idx, stop_idx)
        return codon_positions, coding_index
