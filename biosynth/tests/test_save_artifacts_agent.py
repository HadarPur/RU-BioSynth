"""Tests for biosynth.agents.save_artifacts_agent."""

import tempfile
import unittest
from pathlib import Path

from biosynth.agents.messages import SaveArtifactsRequest
from biosynth.agents.save_artifacts_agent import SaveArtifactsAgent


class TestSaveArtifactsAgent(unittest.TestCase):
    def setUp(self):
        self.agent = SaveArtifactsAgent()

    def test_name(self):
        self.assertEqual(self.agent.name, "save-artifacts")

    def test_writes_each_artifact_under_outputs_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            req = SaveArtifactsRequest(
                output_path=Path(tmp),
                artifacts={
                    "Optimized-Sequence_01-Jan.txt": "ATGCATGC",
                    "Cost-Contribution_01-Jan.txt": "table contents",
                },
            )
            result = self.agent.handle(req)

            outputs_dir = Path(tmp) / "BioSynth-Outputs"
            self.assertTrue(outputs_dir.is_dir())

            for filename in req.artifacts:
                full_path = outputs_dir / filename
                self.assertTrue(full_path.exists(), f"{filename} not saved")
                self.assertEqual(full_path.read_text(), req.artifacts[filename])

            # ``saved_paths`` keeps the same key set as the input.
            self.assertEqual(set(result.saved_paths.keys()), set(req.artifacts.keys()))

    def test_empty_artifacts_map_is_a_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            req = SaveArtifactsRequest(output_path=Path(tmp), artifacts={})
            result = self.agent.handle(req)
            self.assertEqual(result.saved_paths, {})