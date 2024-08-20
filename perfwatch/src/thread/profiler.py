import threading
from ...utils import logger


class ThreadProfiler:
    def __init__(self):
        pass

    def profile(self, func, *args, **kwargs):
        threads_before = set(threading.enumerate())
        result = func(*args, **kwargs)
        threads_after = set(threading.enumerate())
        new_threads = threads_after - threads_before
        logger.info(f"New threads created: {new_threads}")
        return result
