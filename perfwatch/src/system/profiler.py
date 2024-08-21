import platform
import subprocess
from .parser import Parser
from tabulate import tabulate

from ...utils import logger


class SystemProfiler:
    def __init__(self):
        # Ensure the system is Unix-based
        if not self.is_unix():
            raise EnvironmentError(
                "SystemProfiler can only be run on Unix-based systems."
            )

        self.headers = ["Metric", "Before", "After"]
        self.parser = Parser()

    def is_unix(self):
        # Check if the system is Unix-based
        return platform.system() in ["Linux", "Darwin", "Unix"]

    def run_top_command(self):
        # Run the top command and return the output
        return subprocess.check_output(["top", "-l", "1"]).decode("utf-8")

    def profile(self, func, *args, **kwargs):
        # Capture system metrics before function execution
        top_output_before = self.run_top_command()
        cpu_before, mem_before = self.parser.parse_top(top_output_before)

        # Execute the function
        result = func(*args, **kwargs)

        # Capture system metrics after function execution
        top_output_after = self.run_top_command()
        cpu_after, mem_after = self.parser.parse_top(top_output_after)

        # Prepare table data
        cpu_data = [
            ["CPU Usage (user)", f"{cpu_before['user']}%", f"{cpu_after['user']}%"],
            [
                "CPU Usage (system)",
                f"{cpu_before['system']}%",
                f"{cpu_after['system']}%",
            ],
        ]
        mem_data = [
            ["Memory Usage (used)", f"{mem_before['used']}M", f"{mem_after['used']}M"],
            [
                "Memory Usage (wired)",
                f"{mem_before['wired']}M",
                f"{mem_after['wired']}M",
            ],
            [
                "Memory Usage (compressor)",
                f"{mem_before['compressor']}M",
                f"{mem_after['compressor']}M",
            ],
            [
                "Memory Usage (unused)",
                f"{mem_before['unused']}M",
                f"{mem_after['unused']}M",
            ],
        ]

        logger.info("System metrics:")
        logger.info(
            tabulate(
                cpu_data + mem_data,
                headers=self.headers,
                tablefmt="grid",
            )
        )

        return result
