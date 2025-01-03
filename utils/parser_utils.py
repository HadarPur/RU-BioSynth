from Bio import SeqIO
from collections import Counter


def codon_usage_from_fasta(fasta_file):
    """
    Calculate codon usage frequencies from sequences in a FASTA file.
    :param fasta_file: Path to the FASTA file
    :return: Dictionary with codon frequencies
    """
    codon_counts = Counter()
    total_codons = 0

    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence = str(record.seq).upper()
        codons = [sequence[i:i + 3] for i in range(0, len(sequence) - 2, 3) if len(sequence[i:i + 3]) == 3]
        codon_counts.update(codons)
        total_codons += len(codons)

    codon_frequencies = {codon: count / total_codons for codon, count in codon_counts.items()}
    return codon_frequencies
