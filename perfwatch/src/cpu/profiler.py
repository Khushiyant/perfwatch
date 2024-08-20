import cProfile
import pstats
import io
from ...utils import logger


class CPUProfiler:
    def __init__(self):
        pass

    def profile(self, func, *args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        f = io.StringIO()
        ps = pstats.Stats(profiler, stream=f).sort_stats("cumulative")
        ps.print_stats()
        logger.info(f.getvalue())
        return result
