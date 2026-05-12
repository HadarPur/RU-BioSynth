"""Base abstractions for the BioSynth agent pipeline.

Every pipeline stage implements :class:`Agent[InputT, OutputT]`. Errors
inside an agent are surfaced via :class:`AgentError`, which carries the
process exit code the CLI should propagate so the existing semantics
(``sys.exit(2)`` for validation failures, ``sys.exit(3)`` for empty /
malformed sequences) are preserved by the orchestrator.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class AgentError(Exception):
    """Raised by an agent to signal a recoverable / user-visible failure.

    ``code`` is the process exit code the orchestrator should pass to
    ``sys.exit`` so the CLI keeps its current contract with shells and
    CI pipelines.
    """

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class Agent(ABC, Generic[InputT, OutputT]):
    """Typed pipeline stage.

    Subclasses set :attr:`name` and implement :meth:`handle`. Agents are
    expected to be stateless (or read-only with respect to module
    globals) so they can be reused across runs without coupling.
    """

    name: str = "agent"

    @abstractmethod
    def handle(self, request: InputT) -> OutputT:  # pragma: no cover - ABC
        """Run this stage. May raise :class:`AgentError` on failure."""
        raise NotImplementedError
