"""First-stage sanity check before any heavy work runs."""

from biosynth.agents.base import Agent, AgentError
from biosynth.agents.messages import PreflightRequest, PreflightResult


class PreflightAgent(Agent[PreflightRequest, PreflightResult]):
    """Rejects empty / missing input sequences with the same exit code
    the legacy ``CommandController`` always used (``sys.exit(3)``).
    """

    name = "preflight"

    def handle(self, request: PreflightRequest) -> PreflightResult:
        if not request.dna_sequence:
            raise AgentError(
                code=3,
                message="The input sequence is empty, please try again",
            )
        return PreflightResult(dna_sequence=request.dna_sequence)
