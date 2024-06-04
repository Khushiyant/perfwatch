import scapy.all as scapy
import time
from ...utils import logger


class NetworkProfiler:
    def __init__(self, packet_src="192.168.1.100"):
        self.bytes_sent = 0
        self.bytes_received = 0
        self.packet_count = 0
        self.latency_sum = 0
        self.start_time = 0
        self.end_time = 0
        self.packet_src = packet_src

    def network_profile(self, func, *args, **kwargs):
        # Start sniffing network traffic
        self.start_time = time.time()
        scapy.sniff(prn=self.packet_handler, timeout=10)

        # Call the function being profiled
        func(*args, **kwargs)

        # Stop sniffing network traffic
        self.end_time = time.time()

        # Calculate and log network metrics
        self.calculate_metrics()
        self.log_metrics()

    def packet_handler(self, packet):
        # Handle incoming packets
        if packet.haslayer(scapy.IP):
            self.packet_count += 1
            self.bytes_received += len(packet)
            if packet.haslayer(scapy.TCP):
                self.latency_sum += packet.time - packet.sent_time
            elif packet.haslayer(scapy.UDP):
                self.latency_sum += packet.time - packet.sent_time

        # Handle outgoing packets
        if (
            packet.haslayer(scapy.IP) and packet.src == self.packet_src
        ):  # Replace with your IP address
            self.bytes_sent += len(packet)

    def calculate_metrics(self):
        self.latency_avg = self.latency_sum / self.packet_count
        self.throughput = (self.bytes_sent + self.bytes_received) / (
            self.end_time - self.start_time
        )

    def log_metrics(self):
        logger.info(f"Network Bytes Sent: {self.bytes_sent} bytes")
        logger.info(f"Network Bytes Received: {self.bytes_received} bytes")
        logger.info(f"Packet Count: {self.packet_count}")
        logger.info(f"Average Latency: {self.latency_avg:.2f} seconds")
        logger.info(f"Throughput: {self.throughput:.2f} bytes/second")
