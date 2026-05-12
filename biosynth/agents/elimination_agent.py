"""Stage that runs the FSM + DP elimination algorithm."""

from biosynth.agents.base import Agent
from biosynth.agents.messages import EliminationRequest, EliminationResult
from biosynth.algorithm.elimination_controller import EliminationController


class EliminationAgent(Agent[EliminationRequest, EliminationResult]):
    """Wraps :meth:`EliminationController.eliminate` with explicit params.

    Thanks to the widened ``eliminate`` signature, this agent threads the
    cost parameters through the request message rather than reading them
    from the module-level ``CostData`` globals — so the agent is truly
    pure with respect to its declared inputs.
    """

    name = "elimination"

    def handle(self, request: EliminationRequest) -> EliminationResult:
        outcome = EliminationController.eliminate(
            request.cleaned_sequence,
            request.unwanted_patterns,
            request.coding_positions,
            codon_usage=request.codon_usage,
            alpha=request.alpha,
            beta=request.beta,
            w=request.w,
            optimized_codon=request.optimized_codon,
        )

        # ``eliminate`` returns a 5-tuple on the normal path and a
        # 4-tuple on the early-return paths (no-unwanted-patterns or
        # no-valid-sequence). Normalise both shapes into the result
        # dataclass so downstream stages don't have to special-case.
        if len(outcome) == 5:
            info, cost_contribution, cost_substitution, sequence, min_cost = outcome
        else:
            info, cost_contribution, sequence, min_cost = outcome
            cost_substitution = None

        return EliminationResult(
            info=info,
            optimized_sequence=sequence,
            cost_contribution=cost_contribution,
            cost_substitution=cost_substitution,
            min_cost=min_cost,
        )
