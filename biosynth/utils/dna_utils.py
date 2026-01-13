min_coding_region_length = 7 * 3  # start_codon_length + stop_codon_length + 5 codons length in the coding area


class DNAUtils:

    @staticmethod
    def find_start_codon(seq):
        """
        Finds a marked start codon (*ATG), returns its position in the
        cleaned sequence and the cleaned sequence itself.

        Parameters:
            seq (str): DNA sequence containing a marked start codon.

        Returns:
            tuple:
                - int: 0-based index of 'A' in ATG in the cleaned sequence,
                       or -1 if not found
                - str: sequence with '*' removed
        """
        idx = seq.find("*ATG")
        cleaned_seq = seq[:idx] + seq[idx + 1:]

        return idx, cleaned_seq

    @staticmethod
    def get_orf_sequence(orf_index, seq):
        """
        Extracts the ORF sequence from the DNA sequence.

        Parameters:
            orf_index (tuple[int, int] | None): (start, end) of the ORF (end exclusive)
            seq (str): DNA sequence (clean, without '*')

        Returns:
            str | None: ORF sequence, or None if no ORF exists
        """
        if orf_index is None:
            return None

        start, end = orf_index
        return seq[start:end]

    @staticmethod
    def get_coding_and_non_coding_regions_positions(clean_seq, atg_index):
        """
        Computes codon positions and a single ORF defined by a given start codon,
        subject to a minimum coding region length.

        Args:
            clean_seq (str): DNA sequence without '*'
            atg_index (int): index of 'A' in the start codon (ATG)

        Returns:
            tuple:
                - codon_positions (list[int])
                - orf_index (tuple[int, int] | None)
                  (start_index, end_index) where end_index is exclusive
        """
        stop_codons = {"TAA", "TAG", "TGA"}
        N = len(clean_seq)

        codon_positions = [0] * N
        start_idx = atg_index

        # Validate start codon
        if start_idx < 0 or clean_seq[start_idx:start_idx + 3] != "ATG":
            return codon_positions, None

        stop_idx = None

        # Search for first in-frame stop codon
        for j in range(start_idx + 3, N - 2, 3):
            if clean_seq[j:j + 3] in stop_codons:
                candidate_end = j + 3  # exclusive
                if candidate_end - start_idx >= min_coding_region_length:
                    stop_idx = candidate_end
                    break

        # No valid ORF satisfying length constraint
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

        orf_index = (start_idx, stop_idx)
        return codon_positions, orf_index
