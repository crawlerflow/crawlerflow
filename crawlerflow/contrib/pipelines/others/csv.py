import json
from ..base import CrawlerFlowPipelineBase
from datetime import datetime

import csv, json, sys


class CsvFileWriterPipeline(CrawlerFlowPipelineBase):
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
        self.file = csv.writer(open('{}.csv'.format(data_storage['storage_id']), 'w'))
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
        self.file.writerow(data.values())
