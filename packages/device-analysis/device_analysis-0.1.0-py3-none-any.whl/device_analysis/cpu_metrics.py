import psutil
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

class CPUMetrics:
    @staticmethod
    def get_cpu_percent():
        return psutil.cpu_percent()

    @staticmethod
    def plot_cpu_usage(start_time, end_time, interval):
        timestamps = []
        cpu_data = []

        current_time = start_time
        while current_time <= end_time:
            timestamps.append(current_time)
            cpu_percent = CPUMetrics.get_cpu_percent()
            cpu_data.append(cpu_percent)

            time.sleep(interval)
            current_time = datetime.now()

        plt.plot(timestamps, cpu_data, label='CPU Usage')
        plt.title('CPU Usage Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Percentage')
        plt.legend()
        plt.show()
