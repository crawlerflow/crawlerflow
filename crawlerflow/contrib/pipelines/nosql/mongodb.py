import pymongo
from ..base import CrawlerFlowPipelineBase
from datetime import datetime


class MongoDBPipeline(CrawlerFlowPipelineBase):
    """
    Pipeline to save the data to MongoDB

    """

    def create_connection(self, data_storage=None):
        data_storage_settings = data_storage['settings']
        return pymongo.MongoClient(data_storage_settings['connection_uri'])

    def create_or_update_item(self, item=None, spider=None, data_storage_connection=None):
        conn = data_storage_connection['connection']
        # data_storage = data_storage_connection['data_storage']
        data_storage_settings = data_storage_connection['data_storage']['settings']
        collection = conn[data_storage_settings['database_name']][data_storage_settings['collection_name']]
        actual_data = item['_data']
        data = dict(actual_data)
        data['_entry_updated_at'] = datetime.now()
        collection.insert(data)
