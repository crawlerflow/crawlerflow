from .base import FileWriterPipelineBase
import csv, json


class CsvFileWriterPipeline(FileWriterPipelineBase):
    """
    data_storages:
    - storage_id: dataset3
      storage_type: csv_file

    """
    storage_type = "csv_file"

    def before_closing_spider(self):
        for k, connection in self.data_storage_connections.items():
            conn = connection['connection']
            conn.close()
            data_storage = connection['data_storage']
            file_path = '{}.csv'.format(data_storage['storage_id'])
            read_fh = open('{}_temp.txt'.format(data_storage['storage_id']), 'r')
            self.delete_file_if_exist(file_path)
            with open(file_path, 'w') as fh:
                writer = csv.writer(fh)
                rows = tuple(json.loads(line.strip("\n")) for line in read_fh.readlines())
                if rows.__len__() > 0:
                    writer.writerow(rows[0].keys())
                for row in rows:
                    writer.writerow(row.values())
