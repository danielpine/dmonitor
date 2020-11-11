import time

import psutil
from app.util.logger import log


def get_mem_size(process):
    mem_info = process.memory_info()
    return mem_info.rss / 1024


def list_realtime_metrics():
    data = []
    tms = int(time.time())
    log.info(tms)
    for p in psutil.process_iter():
        data.append((tms, p.pid, p.name(), get_mem_size(p), p.cpu_percent()))
    return data


def list_realtime_metrics_format_json():
    data_list = list_realtime_metrics()
    keys = ["timestamp", "pid", "pname", "mem", "cpu"]
    return data
