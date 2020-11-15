from app.es import client
from app.metric.abstract_data_processor import AbstractDataProcessor
from app.util.logger import log
import re


def fill_wildcard(keyword):
    return '%'+'%'.join(re.sub('[\s+]', '', keyword))+'%'


class ElasticSearchDataProcessor(AbstractDataProcessor):
    @staticmethod
    def query(start, end, wildcard):
        return client.excute_sql("SELECT * FROM record WHERE pname in (%s) AND timestamp BETWEEN '%s' AND '%s' ORDER BY timestamp" % (wildcard, start, end))

    @staticmethod
    def query_process_by_key_words(parm):
        wildcard = fill_wildcard(parm.get('key_words'))
        start = parm.get('start')
        end = parm.get('end')
        log.warn("%s %s %s", wildcard, start, end)
        return client.excute_sql("SELECT pname FROM record WHERE pname LIKE '%s' AND timestamp BETWEEN '%s' AND '%s' GROUP BY pname" % (wildcard, start, end))
