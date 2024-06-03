import timeit
import cProfile
import memory_profiler

from ..utils import logger


class PerformanceProfiler:
    """
    A class that provides performance profiling capabilities for functions.
    """

    logging = True  # A flag to enable or disable logging.

    @staticmethod
    def _profile_cpu(func):
        """
        Profile the CPU usage of a function.

        Args:
            func: The function to be profiled.

        Returns:
            The wrapper function that profiles the CPU usage.
        """

        def wrapper(*args, **kwargs):
            if PerformanceProfiler.logging:
                pr = cProfile.Profile()
                pr.enable()
            func(*args, **kwargs)
            if PerformanceProfiler.logging:
                pr.disable()
                pr.print_stats(sort="cumulative")

        return wrapper

    @staticmethod
    def _profile_memory(func):
        """
        Profile the memory usage of a function.

        Args:
            func: The function to be profiled.

        Returns:
            The wrapper function that profiles the memory usage.
        """

        def wrapper(*args, **kwargs):
            if PerformanceProfiler.logging:
                mem_usage = memory_profiler.memory_usage(
                    proc=-1, interval=0.1, timeout=None, timestamps=False
                )
            func(*args, **kwargs)
            if PerformanceProfiler.logging:
                mem_usage = memory_profiler.memory_usage(
                    proc=-1, interval=0.1, timeout=None, timestamps=False
                )
                logger.info(f"Memory usage: {mem_usage}")

        return wrapper

    @staticmethod
    def _profile_time(func):
        """
        Profile the time taken by a function.

        Args:
            func: The function to be profiled.

        Returns:
            The wrapper function that profiles the time taken.
        """

        def wrapper(*args, **kwargs):
            if PerformanceProfiler.logging:
                start = timeit.default_timer()
            func(*args, **kwargs)
            if PerformanceProfiler.logging:
                end = timeit.default_timer()
                logger.info(f"Time taken: {end - start}")

        return wrapper

    @staticmethod
    def performance_profile(func):
        """
        Profile the CPU, memory, and time taken by a function.

        Args:
            func: The function to be profiled.

        Returns:
            The wrapper function that profiles the CPU, memory, and time taken.
        """

        @PerformanceProfiler._profile_cpu
        @PerformanceProfiler._profile_memory
        @PerformanceProfiler._profile_time
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper
