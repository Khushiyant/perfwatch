import re


class Parser:
    def __init__(self):
        pass

    def parse_top(self, output):
        cpu_usage, mem_usage = {}, {}
        for line in output.splitlines():
            if "CPU usage" in line:
                cpu_match = re.search(r"(\d+\.\d+)% user, (\d+\.\d+)% sys", line)
                if cpu_match:
                    cpu_usage = {
                        "user": float(cpu_match.group(1)),
                        "system": float(cpu_match.group(2)),
                    }
            elif "PhysMem" in line:
                mem_match = re.search(
                    r"(\d+)M used \((\d+)M wired, (\d+)M compressor\), (\d+)M unused",
                    line,
                )
                if mem_match:
                    mem_usage = {
                        "used": int(mem_match.group(1)),
                        "wired": int(mem_match.group(2)),
                        "compressor": int(mem_match.group(3)),
                        "unused": int(mem_match.group(4)),
                    }

        if not cpu_usage:
            cpu_usage = {"user": 0.0, "system": 0.0}
        if not mem_usage:
            mem_usage = {"used": 0, "wired": 0, "compressor": 0, "unused": 0}

        return cpu_usage, mem_usage
