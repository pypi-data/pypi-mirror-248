from device_analysis.cpu_metrics import CPUMetrics
from device_analysis.memory_metrics import MemoryMetrics
from device_analysis.network_metrics import NetworkMetrics

class  MacOSMetrics(CPUMetrics, MemoryMetrics, NetworkMetrics):
    print('UnderConstruction, Meanwhile you can just call generic methods from cpu_metrics, memory_metrics, network_metrics')
    pass