"""Terminal busy indicator for long-running operations.

The CLI counterpart of the GUI's :class:`BusyDialog`. Runs a callable on a
background thread while a small Braille spinner with an elapsed-time
counter animates on ``stdout`` and returns whatever the callable returns.

stdout is the default because :mod:`biosynth.executions.controllers.gui_controller`
redirects ``sys.stderr`` to ``/dev/null`` at import time, so a stderr-based
spinner would be invisible during CLI runs.

If the target stream is not attached to a TTY (e.g. piped to a file or
captured by pytest), the spinner falls back to a single static status line
so logs stay readable.

Usage::

    from biosynth.utils.spinner import run_with_spinner
    result = run_with_spinner("Running elimination algorithm", do_work, arg1, kw=2)
"""

import os
import sys
import threading
import time

_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
_FRAME_INTERVAL_SEC = 0.1
_CLEAR_LINE = "\r\033[K"  # carriage return + ANSI "erase to end of line"


def _is_animation_capable(stream):
    """Return True if ``stream`` can render a single-line spinner.

    Real terminals report ``isatty()==True``. Some IDE run consoles
    (PyCharm in particular) handle carriage returns just fine but report
    ``isatty()==False`` — we treat them as TTYs explicitly so users see
    the spinner there too.
    """
    if bool(getattr(stream, "isatty", lambda: False)()):
        return True
    # PyCharm's run window: processes '\r' but isatty() is False.
    if os.environ.get("PYCHARM_HOSTED"):
        return True
    return False


def run_with_spinner(message, fn, *args, stream=None, **kwargs):
    """Run ``fn(*args, **kwargs)`` on a worker thread while animating a
    spinner on the given stream.

    :param message: Status text shown next to the spinner.
    :param fn: Callable to run on the background thread.
    :param stream: Optional output stream (defaults to ``sys.stdout``).
    :param args, kwargs: Forwarded to ``fn``.
    :returns: The value returned by ``fn``.
    :raises: Any exception raised by ``fn`` is re-raised on the main thread.
    """
    out = stream if stream is not None else sys.stdout
    done = threading.Event()
    box = {}

    def worker():
        try:
            box["value"] = fn(*args, **kwargs)
        except BaseException as exc:  # noqa: BLE001 - re-raised below
            box["error"] = exc
        finally:
            done.set()

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    _animate(out, message, done)
    thread.join()

    if "error" in box:
        raise box["error"]
    return box.get("value")


def _animate(stream, message, done):
    """Drive the spinner until ``done`` is set.

    On a TTY this rewrites a single line each frame and shows an elapsed-
    time counter. On a non-TTY (pipe, log file, captured stream) it prints
    a single static line instead of control characters that would look
    like garbage in a log.
    """
    if not _is_animation_capable(stream):
        stream.write(f"{message}...\n")
        stream.flush()
        done.wait()
        return

    start = time.monotonic()
    i = 0
    try:
        # Always paint at least one frame so brief operations still show
        # an indicator (and the worker has time to record completion).
        while True:
            frame = _FRAMES[i % len(_FRAMES)]
            elapsed = time.monotonic() - start
            stream.write(f"{_CLEAR_LINE}{frame} {message}... ({elapsed:.1f}s)")
            stream.flush()
            if done.is_set():
                break
            done.wait(timeout=_FRAME_INTERVAL_SEC)
            i += 1
    finally:
        # Erase the spinner line so subsequent output starts cleanly.
        stream.write(_CLEAR_LINE)
        stream.flush()
