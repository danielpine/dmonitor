import time

from app.data import create_tables, insert_many_to_record
from app.util.logger import log
from app.util.metric_helper import list_realtime_metrics
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', second='*/5', max_instances=5)
def request_update_status():
    log.info('Starting job %s', int(time.time()))
    data = list_realtime_metrics()
    log.info('inserting')
    insert_many_to_record(data)
    log.info('inserted')


def start():
    create_tables()
    scheduler.start()


def shutdown():
    scheduler.shutdown()
