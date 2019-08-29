import json
from .base import FileWriterPipelineBase


class JsonFileWriterPipeline(FileWriterPipelineBase):
    """
    data_storages:
    - storage_id: dataset4
      storage_type: json_file
    """
    storage_type = "json_file"

    def before_closing_spider(self):
        for k, connection in self.data_storage_connections.items():
            conn = connection['connection']
            conn.close()
            data_storage = connection['data_storage']
            file_path = '{}.json'.format(data_storage['storage_id'])
            self.delete_file_if_exist(file_path)
            read_fh = open('{}_temp.txt'.format(data_storage['storage_id']), 'r')

            with open(file_path, "w") as fh:
                rows = tuple(json.loads(line.strip("\n")) for line in read_fh.readlines())
                json.dump(rows, fh)
            fh.close()
