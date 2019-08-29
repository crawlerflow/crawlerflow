from crawlerflow.contrib.spiders.base import CrawlerFlowSpiderBase
from importlib import import_module
from crawlerflow.utils.url import get_domain
import logging
import copy

logger = logging.getLogger(__name__)


class CrawlerFlowWebSpider(CrawlerFlowSpiderBase):
    """
    This is generic spider
    """
    name = "CrawlerFlowWebSpider"

    def closed(self, reason):
        logger.info("spider closed with reason {}".format(reason))

    @staticmethod
    def run_extractor(response=None, extractor=None):
        extractor_type = extractor.get("extractor_type")
        extractor_id = extractor.get("extractor_id")
        logger.info("Running extractor:'{}' on url:{}".format(extractor_id, response.url))
        driver_klass_module = import_module(f'crawlerflow.extractors')
        driver_klass = getattr(driver_klass_module, extractor_type)
        if extractor_type is None:
            return {extractor_id: None}
        else:
            try:
                extractor_object = driver_klass(response=response,
                                                extractor=extractor,
                                                extractor_id=extractor_id)
                data = extractor_object.run()
                return data
            except Exception as e:
                logger.error("Failed to run the extractor_id {} on url {} with error:".format(extractor_id,
                                                                                              response.url,
                                                                                              e))
        return {extractor_id: None}

    def get_data_storages(self):
        return self.manifest.get("data_storages")

    def get_bank_storages_dict(self):
        """
        this is used to fill the data from the extractors and then move to respective
        datastorage pipelines.

        :return:
        """
        return {data_storage['storage_id']: None for data_storage in self.get_data_storages()}

    def parse(self, response=None):
        spider_config = self.get_spider_config(response=response)
        """
        Use this when multiple databases concept is implemented

        default_storage = self.get_default_storage(
            settings=self.settings,
            spider_config=spider_config
        )
        """
        data = {}

        # TODO -  May be add validation to talk about the login status for login + crawler
        # Anyways, login status is already conveyed in post login parser

        all_extracted_data = {}

        datasets_dict = self.get_bank_storages_dict()
        for extractor in spider_config.get('extractors', []):
            extracted_data = self.run_extractor(response=response, extractor=extractor)
            extractor_storage_id = extractor.get("storage_id")
            if extractor_storage_id:
                datasets_dict[extractor_storage_id] = copy.deepcopy(extracted_data[extractor.get("extractor_id")])
            all_extracted_data.update(extracted_data)

        ## save datasets
        for storage_id, dataset_data in datasets_dict.items():
            if dataset_data:
                yield self.prepare_data_for_yield(
                    data=dataset_data,
                    storage_id=storage_id,
                )

        context = self.manifest.get("context")
        if context is not None:
            data.update({"context": context})
        data['url'] = response.url
        data['screenshot'] = response.meta.get("screenshot")
        data['domain'] = get_domain(response.url)
        data['context']['spider_id'] = spider_config['spider_id']
        traversal_data, to_traverse_links_list = self.run_traversals(spider_config=spider_config, response=response)
        # This will save the data
        data['extracted_data'] = all_extracted_data
        data['traversal_data'] = traversal_data
        yield self.prepare_data_for_yield(
            data=data,
            storage_id=spider_config.get("storage_id"),
            # collection_name=default_storage.get("collection_name")
        )

        # This will initiate new traversals
        traversal_requests = self.make_traversal_requests(to_traverse_links_list=to_traverse_links_list,
                                                          response=response)
        for traversal_request in traversal_requests:
            yield traversal_request
        self.post_parse(response=response)
