import time

from app.data import create_tables, insert_many_to_record
from app.es.client import init, write
from app.metric.helper import list_realtime_metrics
from app.util.logger import log
from apscheduler.schedulers.blocking import BlockingScheduler
from config import APP_SETTINGS, ParameterIllegalException

scheduler = BlockingScheduler()

store = APP_SETTINGS.prop('dmonitor.store')


@scheduler.scheduled_job('cron', second='*/5', max_instances=5)
def request_update_status():
    log.info('Starting job %s', int(time.time()))
    do_write_metrics()
    log.info('Finish job %s', int(time.time()))


def do_write_metrics():
    if store == 'ES':
        write()
    elif store == 'DB':
        data = list_realtime_metrics()
        log.info('inserting')
        insert_many_to_record(data)
        log.info('inserted')


def start():
    if store == 'ES':
        init()
    elif store == 'DB':
        create_tables()
    else:
        raise ParameterIllegalException('Not support store type %s' % store)
    scheduler.start()


def shutdown():
    scheduler.shutdown()
