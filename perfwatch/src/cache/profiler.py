import subprocess
from cachetools import LFUCache, TTLCache
import shutil
from ...utils import logger


class CacheProfiler:
    def __init__(self, cache_type="ttl", maxsize=100, ttl=10):
        if cache_type == "ttl":
            self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        elif cache_type == "lfu":
            self.cache = LFUCache(maxsize=maxsize)
        else:
            raise ValueError(f"Invalid cache type: {cache_type}")
        self.hits = 0
        self.misses = 0
        self.cache_type = cache_type

    def run_valgrind(self, func, *args, **kwargs):
        try:
            # Check if Valgrind is installed
            if not shutil.which("valgrind"):
                logger.error(
                    "Valgrind is not installed. Please install it before running this command."
                )
                return None

            # Run Valgrind on the function
            valgrind_cmd = f"valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all {func.__module__} {func.__name__}"
            process = subprocess.Popen(
                valgrind_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output, error = process.communicate()

            # Check for memory leaks
            if "definitely lost" in error.decode("utf-8"):
                logger.error("Memory leak detected! Restarting process...")
                # Restart the process or take other action to handle the memory leak
            elif "possibly lost" in error.decode("utf-8"):
                logger.warning("Possible memory leak detected!")
            else:
                logger.info("No memory leaks detected.")

            # Run the function with caching
            result = self.cache_profile(func, *args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error running Valgrind: {e}")
            return None

    def cache_profile(self, func, *args, **kwargs):
        # Run the function with caching
        result = func(*args, **kwargs)
        self.hits += 1
        return result
