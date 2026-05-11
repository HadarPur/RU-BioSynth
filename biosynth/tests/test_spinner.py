"""Tests for biosynth.utils.spinner."""

import io
import unittest

from biosynth.utils.spinner import run_with_spinner


class _TtyStream(io.StringIO):
    """StringIO that reports itself as a TTY so the spinner animates."""

    def isatty(self):
        return True


class TestRunWithSpinner(unittest.TestCase):
    def test_returns_function_value(self):
        sink = io.StringIO()  # non-TTY → static line, no animation
        result = run_with_spinner("working", lambda: 42, stream=sink)
        self.assertEqual(result, 42)

    def test_forwards_args_and_kwargs(self):
        sink = io.StringIO()
        result = run_with_spinner(
            "summing",
            lambda a, b, *, c: a + b + c,
            1, 2, c=10,
            stream=sink,
        )
        self.assertEqual(result, 13)

    def test_propagates_exceptions(self):
        sink = io.StringIO()
        with self.assertRaises(RuntimeError) as cm:
            run_with_spinner(
                "boom",
                lambda: (_ for _ in ()).throw(RuntimeError("nope")),
                stream=sink,
            )
        self.assertIn("nope", str(cm.exception))

    def test_non_tty_writes_static_message(self):
        sink = io.StringIO()  # isatty() == False
        run_with_spinner("working", lambda: None, stream=sink)
        self.assertIn("working", sink.getvalue())
        # No carriage-return escape sequences in the non-TTY path.
        self.assertNotIn("\r", sink.getvalue())

    def test_tty_uses_carriage_returns_and_clears_line(self):
        sink = _TtyStream()
        run_with_spinner("working", lambda: None, stream=sink)
        out = sink.getvalue()
        # The TTY path uses '\r' to overwrite a single line.
        self.assertIn("\r", out)
        self.assertIn("working", out)
        # The final emit clears the line, so the last line written is blank.
        self.assertTrue(out.rstrip("\r").endswith("\r") or out.endswith("\r"))

    def test_tty_animates_when_worker_is_slow(self):
        """Exercise the loop branch that fires when the worker hasn't
        finished by the first frame check — the spinner waits for the next
        frame interval and increments its frame counter.
        """
        import biosynth.utils.spinner as spinner_mod
        import time as time_mod

        sink = _TtyStream()
        # Shorten the frame interval so the test is quick.
        old_interval = spinner_mod._FRAME_INTERVAL_SEC
        spinner_mod._FRAME_INTERVAL_SEC = 0.01
        try:
            run_with_spinner(
                "working",
                lambda: time_mod.sleep(0.05),
                stream=sink,
            )
        finally:
            spinner_mod._FRAME_INTERVAL_SEC = old_interval

        out = sink.getvalue()
        # The slow worker should have caused multiple '\r' rewrites.
        self.assertGreater(out.count("\r"), 1)
        self.assertIn("working", out)


if __name__ == "__main__":
    unittest.main()
