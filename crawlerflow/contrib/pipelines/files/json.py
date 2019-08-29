import json
from .base import FileWriterPipelineBase
from datetime import datetime


class JsonFileWriterPipeline(FileWriterPipelineBase):
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
        return open('{}.json'.format(data_storage['storage_id']), 'w')

    def create_or_update_item(self, item=None, spider=None, data_storage_connection=None):
        conn = data_storage_connection['connection']
        actual_data = item['_data']
        data = dict(actual_data)
        data['_entry_updated_at'] = datetime.now()
        line = json.dumps(data, default=str) + "\n"
        conn.write(line)
