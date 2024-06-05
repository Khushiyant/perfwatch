import time
import threading
import memory_profiler
import line_profiler
import cProfile
import pstats
import io
import sys
from .network import NetworkProfiler
from .gpu import GPUProfiler
from ..utils import logger


class ProfilerService:
    def __init__(self):
        self.profiler_types = {
            "cpu": self.cpu_profile,
            "memory": self.memory_profile,
            "thread": self.thread_profile,
            "io": self.io_profile,
            "database": self.database_profile,
            "network": self.network_profile,
            "gpu": self.gpu_profile,
            "cache": self.cache_profile,
            "exception": self.exception_profile,
            "system": self.system_profile,
            "distributed": self.distributed_profile,
            "line": self.line_profile,
            "time": self.time_profile,
        }

    def profile(self, func, profiler_types, *args, **kwargs):
        if not isinstance(profiler_types, list):
            raise ValueError("Profiler types must be a list")
        for profiler_type in profiler_types:
            if profiler_type not in self.profiler_types:
                raise ValueError(f"Invalid profiler type: {profiler_type}")
        results = []
        for profiler_type in profiler_types:
            try:
                if profiler_type == "network":
                    packet_src = kwargs.pop("packet_src", None)
                    if packet_src is None:
                        raise ValueError(
                            "Packet source must be specified for network profiling"
                        )
                    result = self.profiler_types[profiler_type](
                        func, packet_src, *args, **kwargs
                    )
                else:
                    result = self.profiler_types[profiler_type](func, *args, **kwargs)
                results.append((profiler_type, result))
            except Exception as e:
                logger.error(f"Error profiling {profiler_type}: {e}")
                results.append((profiler_type, None))
        return results

    def cpu_profile(self, func, *args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
        ps.print_stats()
        logger.info(s.getvalue())
        return result

    def time_profile(self, func, *args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Time execution: {execution_time:.6f} seconds")
        return result

    def memory_profile(self, func, *args, **kwargs):
        profiler = memory_profiler.profile
        result = profiler(func)(*args, **kwargs)
        return result

    def thread_profile(self, func, *args, **kwargs):
        threads_before = threading.enumerate()
        result = func(*args, **kwargs)
        threads_after = threading.enumerate()
        new_threads = [t for t in threads_after if t not in threads_before]
        logger.info(f"New threads created: {new_threads}")
        return result

    def line_profile(self, func, *args, **kwargs):
        profiler = line_profiler.LineProfiler()
        profiler.add_function(func)
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        profiler.print_stats()
        return result

    def io_profile(self, func, *args, **kwargs):
        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output

        input_bytes = 0
        original_stdin = sys.stdin
        input_buffer = io.StringIO()
        sys.stdin = input_buffer

        func(*args, **kwargs)

        sys.stdout = original_stdout
        captured_output = output.getvalue()
        write_bytes = len(captured_output.encode("utf-8"))

        sys.stdin = original_stdin
        input_bytes = len(input_buffer.getvalue().encode("utf-8"))

        logger.info(f"IO Write Bytes: {write_bytes} bytes")
        logger.info(f"IO Read Bytes: {input_bytes} bytes")

    def database_profile(self, func, *args, **kwargs):
        # Will have to implment profile using django-debug-toolbar or pg_stat_statements to profile database
        raise NotImplementedError

    def network_profile(self, func, packet_src, *args, **kwargs):
        network_profiler = NetworkProfiler(packet_src=packet_src)
        return network_profiler.network_profile(func, *args, **kwargs)

    def gpu_profile(self, func, *args, **kwargs):
        gpu_profiler = GPUProfiler()
        return gpu_profiler.gpu_profile(func, *args, **kwargs)

    def cache_profile(self, func, *args, **kwargs):
        # Will have to implment profile using cachegrind or valgrind to profile cache
        raise NotImplementedError

    def exception_profile(self, func, *args, **kwargs):
        # Will have to implment profile using sentry or rollbar to profile exceptions
        raise NotImplementedError

    def system_profile(self, func, *args, **kwargs):
        # Will have to implment profile using top or htop to profile system
        raise NotImplementedError

    def distributed_profile(self, func, *args, **kwargs):
        # Will have to implment profile using zipkin or opentracing to profile distributed system
        raise NotImplementedError


profiler_service = ProfilerService()


def watch(profiler_type, **kwargs):
    def decorator(func):
        def wrapper(*args, **wrapper_kwargs):
            merged_kwargs = {**kwargs, **wrapper_kwargs}
            return profiler_service.profile(func, profiler_type, *args, **merged_kwargs)

        return wrapper

    return decorator
