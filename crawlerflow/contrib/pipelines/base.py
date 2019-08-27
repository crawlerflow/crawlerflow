class CrawlerFlowPipelineBase(object):

    def __init__(self, data_storages=None):
        self.data_storage_connections = self.create_connections(data_storages=data_storages)

    def create_connection(self, data_storage=None):
        """


        :param data_storages:
        :return: dictionary of data_storage_connections
        """
        raise NotImplementedError()

    def create_connections(self, data_storages=None):
        data_storage_connections = {}
        for data_storage in data_storages:
            storage_type = data_storage['storage_type']
            storage_id = data_storage['storage_id']
            if storage_type == "mongodb":
                data_storage_connections[storage_id] = {
                    "connection": self.create_connection(data_storage=data_storage),
                    "data_storage": data_storage
                }
        return data_storage_connections

    @classmethod
    def from_crawler(cls, crawler):
        data_storages = crawler.spider.manifest.get("data_storages", [])
        return cls(
            data_storages=data_storages
        )

    def get_connection_from_item(self, item=None):
        return self.data_storage_connections[item['_data_storage_id']]

    def create_or_update_item(self, item=None, spider=None, data_storage_connection=None):
        """
        Code comes here with all validations that item is suppose to be saved
        to this Storage.


        item = {
            "_data_storage_id": storage_id,
            "_data_storage_collection_name": collection_name,
            "_data": data
        }

        spider = {
            spider_config: {},
            manifest: {}
        }

        data_storage_connection = {
            connection: <ConnectionClient>,
            data_storage: {

            }
        }

        :param item:
        :param spider:
        :param data_storage_connection:
        :return:
        """
        raise NotImplementedError()

    def process_item(self, item, spider):
        print("=======", self.data_storage_connections.keys(), item)
        if item.get("_data_storage_id") in self.data_storage_connections.keys():
            data_storage_connection = self.get_connection_from_item(item=item)
            self.create_or_update_item(item=item, spider=spider, data_storage_connection=data_storage_connection)
            return
        else:
            return item
