import psutil
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

class MemoryMetrics:
    @staticmethod
    def get_virtual_memory_percent():
        return psutil.virtual_memory().percent

    @staticmethod
    def plot_memory_usage(start_time, end_time, interval):
        timestamps = []
        memory_data = []

        current_time = start_time
        while current_time <= end_time:
            timestamps.append(current_time)
            memory_percent = MemoryMetrics.get_virtual_memory_percent()
            memory_data.append(memory_percent)

            time.sleep(interval)
            current_time = datetime.now()

        plt.plot(timestamps, memory_data, label='Memory Usage')
        plt.title('Memory Usage Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Percentage')
        plt.legend()
        plt.show()