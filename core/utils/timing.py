from time import perf_counter


class Timer:
    """Simple context-free timer utility."""

    def __init__(self) -> None:
        self._start = perf_counter()

    def elapsed(self) -> float:
        """Return elapsed seconds."""
        return perf_counter() - self._start
