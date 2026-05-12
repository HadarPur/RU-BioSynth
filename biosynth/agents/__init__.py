"""Internal multi-agent decomposition of the BioSynth pipeline.

Each pipeline stage (preflight, coding-region discovery, elimination,
report rendering, artifact saving) is encapsulated as an
:class:`Agent` with a typed message contract. A linear
:class:`Pipeline` chains them together. The deterministic algorithmic
core (FSM + DP) is untouched — the agents just wrap existing
functions so each step has a self-describing input/output type and
can be tested, swapped, or instrumented in isolation.

The agents are *not* autonomous; they're deterministic stages that
together produce the same output the CLI always has.
"""

from biosynth.agents.base import Agent, AgentError
from biosynth.agents.coding_region_agent import CodingRegionAgent
from biosynth.agents.elimination_agent import EliminationAgent
from biosynth.agents.messages import (
    CodingRegionRequest,
    CodingRegionResult,
    EliminationRequest,
    EliminationResult,
    PipelineRequest,
    PipelineResult,
    PreflightRequest,
    PreflightResult,
    ReportRequest,
    ReportResult,
    SaveArtifactsRequest,
    SaveArtifactsResult,
)
from biosynth.agents.pipeline import Pipeline
from biosynth.agents.preflight_agent import PreflightAgent
from biosynth.agents.report_agent import ReportAgent
from biosynth.agents.save_artifacts_agent import SaveArtifactsAgent

__all__ = [
    "Agent",
    "AgentError",
    "CodingRegionAgent",
    "CodingRegionRequest",
    "CodingRegionResult",
    "EliminationAgent",
    "EliminationRequest",
    "EliminationResult",
    "Pipeline",
    "PipelineRequest",
    "PipelineResult",
    "PreflightAgent",
    "PreflightRequest",
    "PreflightResult",
    "ReportAgent",
    "ReportRequest",
    "ReportResult",
    "SaveArtifactsAgent",
    "SaveArtifactsRequest",
    "SaveArtifactsResult",
]
