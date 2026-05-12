"""Stage that resolves the start codon and computes coding-region positions."""

from biosynth.agents.base import Agent, AgentError
from biosynth.agents.messages import CodingRegionRequest, CodingRegionResult
from biosynth.utils.dna_utils import DNAUtils


class CodingRegionAgent(Agent[CodingRegionRequest, CodingRegionResult]):
    """Wraps ``DNAUtils.find_start_codon`` + ``get_coding_and_non_coding_regions_positions``.

    A ``ValueError`` from ``find_start_codon`` (malformed ``*ATG`` marker
    or missing in-frame stop) is translated into an :class:`AgentError`
    with exit code 3 — same behaviour the legacy ``CommandController``
    exposed to the shell.
    """

    name = "coding-region"

    def handle(self, request: CodingRegionRequest) -> CodingRegionResult:
        try:
            start_codon_index, cleaned = DNAUtils.find_start_codon(request.dna_sequence)
        except ValueError as e:
            raise AgentError(
                code=3,
                message=f"Start codon validation failed: {e}",
            ) from e

        coding_positions, coding_indexes = (
            DNAUtils.get_coding_and_non_coding_regions_positions(cleaned, start_codon_index)
        )

        return CodingRegionResult(
            cleaned_sequence=cleaned,
            start_codon_index=start_codon_index,
            coding_positions=coding_positions,
            coding_indexes=coding_indexes,
        )
