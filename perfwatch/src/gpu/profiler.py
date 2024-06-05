import pynvml
import time
from ...utils import logger


class GPUProfiler:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.memory_usage_start = 0
        self.memory_usage_end = 0
        self.gpu_utilization_start = 0
        self.gpu_utilization_end = 0
        self.power_usage_start = 0
        self.power_usage_end = 0

    def gpu_profile(self, func, *args, **kwargs):
        # Initialize NVML
        pynvml.nvmlInit()

        # Get handle to the first GPU (you can modify this to profile a different GPU)
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        # Start profiling
        self.start_time = time.time()
        self.memory_usage_start = pynvml.nvmlDeviceGetMemoryInfo(handle).used
        self.gpu_utilization_start = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        self.power_usage_start = pynvml.nvmlDeviceGetPowerUsage(handle)

        # Call the function being profiled
        func(*args, **kwargs)

        # Stop profiling
        self.end_time = time.time()
        self.memory_usage_end = pynvml.nvmlDeviceGetMemoryInfo(handle).used
        self.gpu_utilization_end = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        self.power_usage_end = pynvml.nvmlDeviceGetPowerUsage(handle)

        # Calculate and log GPU metrics
        self.calculate_metrics()
        self.log_metrics()

        # Shutdown NVML
        pynvml.nvmlShutdown()

    def calculate_metrics(self):
        self.memory_usage_delta = self.memory_usage_end - self.memory_usage_start
        self.gpu_utilization_avg = (
            self.gpu_utilization_start + self.gpu_utilization_end
        ) / 2
        self.power_usage_avg = (self.power_usage_start + self.power_usage_end) / 2
        self.execution_time = self.end_time - self.start_time

    def log_metrics(self):
        logger.info(f"GPU Memory Usage Delta: {self.memory_usage_delta} bytes")
        logger.info(f"GPU Utilization Average: {self.gpu_utilization_avg}%")
        logger.info(f"GPU Power Usage Average: {self.power_usage_avg} watts")
        logger.info(f"Execution Time: {self.execution_time:.2f} seconds")
