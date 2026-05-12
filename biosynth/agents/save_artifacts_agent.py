"""Stage that persists optimized sequence + cost tables to the output dir."""

from biosynth.agents.base import Agent
from biosynth.agents.messages import SaveArtifactsRequest, SaveArtifactsResult
from biosynth.utils.file_utils import save_file


class SaveArtifactsAgent(Agent[SaveArtifactsRequest, SaveArtifactsResult]):
    """Wraps :func:`save_file` for a batch of filename → content artifacts.

    Each save returns a status string (the absolute path or an error
    message); the agent collects them into a mapping so callers can
    display the locations without re-deriving them.
    """

    name = "save-artifacts"

    def handle(self, request: SaveArtifactsRequest) -> SaveArtifactsResult:
        saved = {
            filename: save_file(content, filename, request.output_path)
            for filename, content in request.artifacts.items()
        }
        return SaveArtifactsResult(saved_paths=saved)
