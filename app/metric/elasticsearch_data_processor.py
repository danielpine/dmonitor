from app.metric.abstract_data_processor import AbstractDataProcessor


class ElasticSearchDataProcessor(AbstractDataProcessor):
    @staticmethod
    def query():
        """query metric data set"""
        print('hello es')
        pass
