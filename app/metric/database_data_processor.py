from app.metric.abstract_data_processor import AbstractDataProcessor


class DataBaseDataProcessor(AbstractDataProcessor):
    @staticmethod
    def query():
        """query metric data set"""
        print('hello db')
        pass
