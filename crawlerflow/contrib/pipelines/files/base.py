import json
from ..base import CrawlerFlowPipelineBase
from datetime import datetime
import os


class FileWriterPipelineBase(CrawlerFlowPipelineBase):
    """
    data_storages:
    - storage_id: dataset4
      storage_type: json_file/csv_file
    """
    storage_type = None

    def close_file_connection(self):
        for k, connection in self.data_storage_connections.items():
            try:
                connection["connection"].close()
            except Exception as e:
                pass

    def before_closing_spider(self):
        raise NotImplementedError()

    def close_spider(self, spider):
        self.before_closing_spider()
        # self.close_file_connection()

    @staticmethod
    def delete_file_if_exist(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def create_connection(self, data_storage=None):
        """
        This will be
        """
        ## delete if file exist
        file_path = '{}_temp.txt'.format(data_storage['storage_id'])
        self.delete_file_if_exist(file_path)
        return open(file_path, 'w+')

    def create_or_update_item(self, item=None, spider=None, data_storage_connection=None):
        conn = data_storage_connection['connection']
        actual_data = item['_data']
        data = dict(actual_data)
        data['_entry_updated_at'] = datetime.now()

        line = json.dumps(data, default=str) + "\n"
        conn.write(line)
