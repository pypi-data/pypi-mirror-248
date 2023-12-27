import psutil
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

class NetworkMetrics:
    @staticmethod
    def get_network_io_counters():
        network_stats = psutil.net_io_counters()
        return network_stats.bytes_sent, network_stats.bytes_recv

    @staticmethod
    def plot_network_activity(start_time, end_time, interval):
        timestamps = []
        network_sent_data = []
        network_recv_data = []

        current_time = start_time
        while current_time <= end_time:
            timestamps.append(current_time)
            bytes_sent, bytes_recv = NetworkMetrics.get_network_io_counters()
            network_sent_data.append(bytes_sent)
            network_recv_data.append(bytes_recv)

            time.sleep(interval)
            current_time = datetime.now()

        plt.plot(timestamps, network_sent_data, label='Network Sent')
        plt.plot(timestamps, network_recv_data, label='Network Received')
        plt.title('Network Activity Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Bytes')
        plt.legend()
        plt.show()