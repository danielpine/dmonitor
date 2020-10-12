import time
import psutil
import logging
from data import insert_many_to_record
from data import create_table_record
from apscheduler.schedulers.blocking import BlockingScheduler
from logger import log

scheduler = BlockingScheduler()


def get_mem_size(process):
    mem_info = process.memory_info()
    return mem_info.rss / 1024


@scheduler.scheduled_job('cron', second='*/5', max_instances=5)
def request_update_status():
    print(int(time.time()), 'Doing job')
    data = []
    log.info('start')
    tms = int(time.time())
    log.info(tms)
    for p in psutil.process_iter():
        data.append((tms, p.pid, p.name(), get_mem_size(p), p.cpu_percent()))
    log.info('inserting')
    insert_many_to_record(data)
    log.info('inserted')


def start():
    create_table_record()
    scheduler.start()


def shutdown():
    scheduler.shutdown()
