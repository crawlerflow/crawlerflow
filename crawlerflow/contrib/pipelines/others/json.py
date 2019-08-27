import json
from ..base import CrawlerFlowPipelineBase
from datetime import datetime


class JsonFileWriterPipeline(CrawlerFlowPipelineBase):
    """
    data_storages:
    - storage_id: dataset4
      storage_type: json_file
    """
    storage_type = "json_file"

    def create_connection(self, data_storage=None):
        """
        This will be
        """
        self.file = open('{}.json'.format(data_storage['storage_id']), 'w')
        return None

    def close_spider(self, spider):
        try:
            self.file.close()
        except Exception as e:
            pass

    def create_or_update_item(self, item=None, spider=None, data_storage_connection=None):
        actual_data = item['_data']
        data = dict(actual_data)
        data['_entry_updated_at'] = datetime.now()
        line = json.dumps(data, default=str) + "\n"
        self.file.write(line)
