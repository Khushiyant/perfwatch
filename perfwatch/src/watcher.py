import io
import time
from contextlib import redirect_stdout

import line_profiler
import memory_profiler

from ..utils import logger

from .gpu import GPUProfiler
from .network import NetworkProfiler
from .cache import CacheProfiler
from .cpu import CPUProfiler
from .thread import ThreadProfiler
from .io import IOProfiler
from .system import SystemProfiler


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

        self.logger = logger

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
                self.logger.error(f"Error profiling {profiler_type}: {e}")
                results.append((profiler_type, None))
        return results

    def cpu_profile(self, func, *args, **kwargs):
        profiler = CPUProfiler()
        result = profiler.profile(func, *args, **kwargs)
        return result

    def time_profile(self, func, *args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        self.logger.info(f"Time execution: {execution_time:.6f} seconds")
        return result

    def memory_profile(self, func, *args, **kwargs):
        profiler = memory_profiler.profile
        result = profiler(func)(*args, **kwargs)
        return result

    def thread_profile(self, func, *args, **kwargs):
        profiler = ThreadProfiler()
        result = profiler.profile(func, *args, **kwargs)
        return result

    def line_profile(self, func, *args, **kwargs):
        profiler = line_profiler.LineProfiler()
        profiler.add_function(func)
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        f = io.StringIO()
        with redirect_stdout(f):
            profiler.print_stats(stream=None)
        self.logger.info(f.getvalue())
        return result

    def io_profile(self, func, *args, **kwargs):
        io_profiler = IOProfiler()
        return io_profiler.profile(func, *args, **kwargs)

    def database_profile(self, func, *args, **kwargs):
        # Will have to implment profile using django-debug-toolbar or pg_stat_statements to profile database
        raise NotImplementedError

    def network_profile(self, func, packet_src, *args, **kwargs):
        network_profiler = NetworkProfiler(packet_src=packet_src)
        return network_profiler.profile(func, *args, **kwargs)

    def gpu_profile(self, func, *args, **kwargs):
        gpu_profiler = GPUProfiler()
        return gpu_profiler.profile(func, *args, **kwargs)

    def cache_profile(self, func, *args, **kwargs):
        cache_profiler = CacheProfiler()
        return cache_profiler.profile(func, *args, **kwargs)

    def exception_profile(self, func, *args, **kwargs):
        # Will have to implment profile using sentry or rollbar to profile exceptions
        raise NotImplementedError

    def system_profile(self, func, *args, **kwargs):
        profiler = SystemProfiler()
        return profiler.profile(func, *args, **kwargs)

    def distributed_profile(self, func, *args, **kwargs):
        # Will have to implment profile using zipkin or opentracing to profile distributed system
        raise NotImplementedError


profiler_service = ProfilerService()


def watch(profiler_type, **kwargs):
    def decorator(func):
        def wrapper(*args, **wrapper_kwargs):
            merged_kwargs: dict = {**kwargs, **wrapper_kwargs}
            return profiler_service.profile(func, profiler_type, *args, **merged_kwargs)

        return wrapper

    return decorator
