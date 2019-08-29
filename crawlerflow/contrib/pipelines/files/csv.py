import json
from .base import FileWriterPipelineBase
from datetime import datetime

import csv, json, sys


class CsvFileWriterPipeline(FileWriterPipelineBase):
    """
    data_storages:
    - storage_id: dataset3
      storage_type: csv_file

    """
    storage_type = "csv_file"

    def create_connection(self, data_storage=None):
        """
        This will be
        """
        return csv.writer(open('{}.csv'.format(data_storage['storage_id']), 'w'))

    def create_or_update_item(self, item=None, spider=None, data_storage_connection=None):
        conn = data_storage_connection['connection']

        actual_data = item['_data']
        data = dict(actual_data)
        data['_entry_updated_at'] = datetime.now()
        conn.writerow(data.values())
