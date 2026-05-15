"""Background workers for long-running operations.

Each worker is a ``QObject`` that exposes ``finished`` / ``failed`` signals
and a ``run()`` slot. Use the standard Qt pattern::

    thread = QThread(parent)
    worker = EliminationWorker(...)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.finished.connect(on_finished)
    worker.failed.connect(on_failed)
    worker.finished.connect(thread.quit)
    worker.failed.connect(thread.quit)
    thread.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    thread.start()
"""

from PyQt5.QtCore import QObject, pyqtSignal

from biosynth.executions.execution_utils import eliminate_unwanted_patterns


class EliminationWorker(QObject):
    """Runs ``eliminate_unwanted_patterns`` off the UI thread."""

    finished = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, sequence, patterns, coding_positions):
        super().__init__()
        self._sequence = sequence
        self._patterns = patterns
        self._coding_positions = coding_positions

    def run(self):
        """Execute the elimination on the worker thread.

        Emits ``finished`` on success or ``failed`` with the error message
        if the underlying computation raises.
        """
        try:
            eliminate_unwanted_patterns(
                self._sequence, self._patterns, self._coding_positions
            )
            self.finished.emit()
        except Exception as e:  # pragma: no cover - surfaced to the UI
            self.failed.emit(str(e))
