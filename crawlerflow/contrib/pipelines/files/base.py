import json
from ..base import CrawlerFlowPipelineBase
from datetime import datetime


class FileWriterPipelineBase(CrawlerFlowPipelineBase):
    """
    data_storages:
    - storage_id: dataset4
      storage_type: json_file/csv_file
    """
    storage_type = None

    def close_spider(self, spider):
        for file in self.data_storage_connections:
            try:
                file.close()
            except Exception as e:
                pass

    def create_connection(self, data_storage=None):
        """
        This will be
        """
        return open('{}.json'.format(data_storage['storage_id']), 'w')

    def create_or_update_item(self, item=None, spider=None, data_storage_connection=None):
        actual_data = item['_data']
        data = dict(actual_data)
        data['_entry_updated_at'] = datetime.now()
        line = json.dumps(data, default=str) + "\n"
        self.file.write(line)
