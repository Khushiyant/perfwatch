import sys
import io
from ...utils import logger


class IOProfiler:
    def __init__(self):
        pass

    def profile(self, func, *args, **kwargs):
        f = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = f

        input_bytes = 0
        original_stdin = sys.stdin
        input_buffer = io.StringIO()
        sys.stdin = input_buffer

        result = func(*args, **kwargs)

        sys.stdout = original_stdout
        captured_output = f.getvalue()
        write_bytes = len(captured_output.encode("utf-8"))

        sys.stdin = original_stdin
        input_bytes = len(input_buffer.getvalue().encode("utf-8"))

        logger.info(f"IO Write Bytes: {write_bytes} bytes")
        logger.info(f"IO Read Bytes: {input_bytes} bytes")

        return result
