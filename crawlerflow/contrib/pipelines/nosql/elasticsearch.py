from ..base import CrawlerFlowPipelineBase
from elasticsearch import Elasticsearch
from datetime import datetime
import uuid


class ElasticSearchPipeline(CrawlerFlowPipelineBase):
    """
    Pipeline to save the data to ElasticSearch

    data_storages:
    - storage_id: default2
      storage_type: elasticsearch
      settings:
        connection_uri: localhost
        index_name: database33
        doc_type: pages_66

    """
    storage_type = "elasticsearch"

    def create_connection(self, data_storage=None):
        data_storage_settings = data_storage['settings']
        return Elasticsearch([{'host': data_storage_settings.get("connection_uri"), 'port': 9200}])

    def create_or_update_item(self, item=None, spider=None, data_storage_connection=None):
        conn = data_storage_connection['connection']
        data_storage_settings = data_storage_connection['data_storage']['settings']
        actual_data = item['_data']
        data = dict(actual_data)
        data['_entry_updated_at'] = datetime.now()
        conn.index(
            index=data_storage_settings['index_name'],
            doc_type=data_storage_settings['doc_type'],
            id=str(uuid.uuid4()),
            body=data)
