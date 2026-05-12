"""Typed messages exchanged between agents in the BioSynth pipeline.

All messages are frozen dataclasses so they can be safely passed
between stages without aliasing concerns. Each ``*Request`` is the
input a single agent expects; each ``*Result`` is its output.
``PipelineRequest`` and ``PipelineResult`` are the orchestrator's
top-level envelope — they collect everything the CLI/GUI need from a
single end-to-end run.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# PreflightAgent
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PreflightRequest:
    """Bare-minimum sanity check before the pipeline does any real work."""

    dna_sequence: Optional[str]


@dataclass(frozen=True)
class PreflightResult:
    dna_sequence: str  # guaranteed non-empty


# ---------------------------------------------------------------------------
# CodingRegionAgent
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CodingRegionRequest:
    dna_sequence: str


@dataclass(frozen=True)
class CodingRegionResult:
    cleaned_sequence: str
    start_codon_index: Optional[int]
    coding_positions: list
    coding_indexes: Optional[tuple]


# ---------------------------------------------------------------------------
# EliminationAgent
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EliminationRequest:
    cleaned_sequence: str
    unwanted_patterns: set
    coding_positions: list
    codon_usage: dict
    alpha: float
    beta: float
    w: float
    optimized_codon: bool


@dataclass(frozen=True)
class EliminationResult:
    info: str
    optimized_sequence: Optional[str]
    cost_contribution: Optional[list]
    cost_substitution: Optional[list]
    min_cost: float


# ---------------------------------------------------------------------------
# ReportAgent
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ReportRequest:
    file_date: str
    cleaned_sequence: str
    coding_indexes: Optional[tuple]
    coding_positions: list
    optimized_sequence: Optional[str]
    unwanted_patterns: set
    cost_contribution: Optional[list]
    cost_substitution: Optional[list]
    min_cost: float
    output_path: Optional[Path] = None  # forwarded to download_report


@dataclass(frozen=True)
class ReportResult:
    report_filename: str
    local_report_path: str
    downloaded_path: str  # rendered status message including final saved path


# ---------------------------------------------------------------------------
# SaveArtifactsAgent
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SaveArtifactsRequest:
    """Save a batch of text artifacts under ``output_path / BioSynth-Outputs/``.

    ``artifacts`` maps filename → file content.
    """

    output_path: Path
    artifacts: dict


@dataclass(frozen=True)
class SaveArtifactsResult:
    saved_paths: dict  # filename → status string from save_file


# ---------------------------------------------------------------------------
# Pipeline envelope
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PipelineRequest:
    """End-to-end input for a single BioSynth run."""

    dna_sequence: Optional[str]
    unwanted_patterns: set
    codon_usage: dict
    alpha: float
    beta: float
    w: float
    optimized_codon: bool
    output_path: Path
    file_date: str
    # Pre-formatted, table-rendered text for the cost-contribution and
    # cost-substitution save files. CommandController already does the
    # tabulate rendering for terminal display, so it passes the same
    # strings here to avoid re-rendering. The keys are the basename
    # prefixes ("Cost-Contribution", "Cost-Substitution").
    extra_artifacts: dict = field(default_factory=dict)


@dataclass(frozen=True)
class PipelineResult:
    cleaned_sequence: str
    start_codon_index: Optional[int]
    coding_positions: list
    coding_indexes: Optional[tuple]

    elimination_info: str
    optimized_sequence: Optional[str]
    cost_contribution: Optional[list]
    cost_substitution: Optional[list]
    min_cost: float

    report_filename: str
    local_report_path: str
    downloaded_report_path: str
    saved_artifact_paths: dict
