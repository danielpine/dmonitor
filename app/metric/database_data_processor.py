from app.data import (select_from_record, select_from_record_filter,
                      select_process_from_record_by_key_words)
from app.metric.abstract_data_processor import AbstractDataProcessor
from app.util.logger import log


class DataBaseDataProcessor(AbstractDataProcessor):
    @staticmethod
    def query(start, end, wildcard):
        if wildcard and len(wildcard.strip()) > 0:
            return select_from_record_filter(start, end, wildcard)
        else:
            return select_from_record(start, end)

    @staticmethod
    def query_process_by_key_words(parm):
        key_words = parm.get('key_words')
        log.warn(key_words)
        data = select_process_from_record_by_key_words('%'+key_words+'%')
        data.insert(0, 'pname')
        return '\n'.join(data)
