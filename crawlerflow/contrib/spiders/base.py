from scrapy.spiders import CrawlSpider
from crawlerflow.utils.spiders import get_spider_from_list
from crawlerflow.core.traversals.generic import GenericLinkExtractor
import scrapy
from scrapy.http import Request, FormRequest


class LoginParser(object):
    pass


class CrawlerFlowSpiderBase(CrawlSpider):
    """

    TODO - document why we need this as base method.

    """

    # spider_id = None  # id of the current spider
    spider_config = None  # json config of the current crawler
    spider_data_storage = None  # TODO - we might not be using this anymore, remove with caution.
    manifest = {}
    current_request_traversal_id = None  # this will contain the config of traversal that led to this spider.

    def post_parse(self, response=None):
        pass

    def parse_error(self, failure):
        print("failure", failure)
        pass

    def get_spider_meta(self):
        return {
            "current_request_traversal_count": 0,
            "spider_config": self.spider_config,
            "manifest": self.manifest,
            "current_request_traversal_id": "init",
            "current_traversal_max_count": 1
        }

    def get_spider_request_kwargs(self):

        return {
            "errback": self.parse_error,
            "dont_filter": True,
            "meta": self.get_spider_meta()
        }

    def _prepare_start_requests(self, urls=None):
        print("Preparing start requests for urls: ", urls)
        start_requests = []
        for url in urls:
            init_request_kwargs = self.get_spider_request_kwargs()
            start_requests.append(scrapy.Request(
                url,
                callback=self.parse,
                **init_request_kwargs
            ))
        return start_requests

    def _prepare_login_request(self):
        """
        Generate a login parser request.
        """
        login_settings = self.spider_config.get("login_settings", None)
        if login_settings:
            login_request_kwargs = {}
            form_identifiers = login_settings.get("form_identifiers", {})
            auth_type = login_settings.get("auth_type")
            if auth_type == "cookies":
                form_kwargs = {
                    "formdata": {
                        form_identifiers['username_field']: login_settings['username'],
                        form_identifiers['password_field']: login_settings['password']
                    },
                    "formcss": form_identifiers['form_selector'],
                }
                login_request_kwargs.update(form_kwargs)
            else:
                raise NotImplementedError("only auth_type=cookies is supported currently.")
            return login_request_kwargs
        else:
            return None

    def login_request(self):
        """This function is called before crawling starts."""
        login_settings = self.spider_config.get("login_settings", {})
        login_url = login_settings.get("url")
        init_request_kwargs = self.get_spider_request_kwargs()
        return Request(url=login_url, **init_request_kwargs, callback=self.login_parser, )

    def login_parser(self, response):
        login_request_kwargs = self._prepare_login_request()
        request_kwargs = self.get_spider_request_kwargs()
        return FormRequest.from_response(
            response,
            **login_request_kwargs,
            **request_kwargs,
            callback=self.post_login_init_parser
        )

    def post_login_init_parser(self, response):
        start_requests = self._prepare_start_requests(self.start_urls)
        for request in start_requests:
            yield request

    def start_requests(self):
        login_settings = self.spider_config.get("login_settings", {})
        login_url = login_settings.get("url")
        if login_url:
            yield self.login_request()
        else:
            start_requests = self._prepare_start_requests(self.start_urls)
            for request in start_requests:
                yield request

    def get_spider_config(self, response=None):
        if response.meta.get("spider_config"):
            return response.meta.get("spider_config")
        else:
            return self.spider_config

    @staticmethod
    def get_default_storage(settings=None, spider_config=None):
        data_storages = settings.get("DATA_STORAGES", [])
        default_storage = None
        spider_storage_id = "default"
        for data_storage in data_storages:
            __storage_id = data_storage.get("storage_id") or data_storage.get("STORAGE_ID")
            if __storage_id == spider_storage_id:
                return data_storage
        return default_storage

    @staticmethod
    def prepare_data_for_yield(data=None, collection_name=None, storage_id="default"):
        return {
            "_data_storage_id": storage_id,
            "_data_storage_collection_name": collection_name,
            "_data": data
        }

    @staticmethod
    def is_this_request_from_same_traversal(response, traversal):
        """
        This mean the current request came from this  traversal,
        so we can put max pages condition on this, otherwise for different
        traversals of different spiders, adding max_page doest make sense.
        """
        traversal_id = traversal['traversal_id']
        current_request_traversal_id = response.meta.get('current_request_traversal_id', None)
        return current_request_traversal_id == traversal_id

    def make_traversal_requests(self, to_traverse_links_list=None, response=None):
        traversal_requests = []
        for to_traverse_link in to_traverse_links_list:
            traversal_requests.append(response.follow(
                to_traverse_link.get("link"),
                callback=self.parse,
                errback=self.parse_error,
                meta=to_traverse_link.get("meta", {})
            ))
        return traversal_requests

    @staticmethod
    def run_traversal(response=None, traversal=None, **kwargs):

        selector_type = traversal.get("selector_type", "css")
        kwargs = {}
        if selector_type == "css":
            kwargs['restrict_css'] = (traversal.get("selector_value"),)
        elif selector_type == "xpath":
            kwargs['restrict_xpaths'] = (traversal.get("selector_value"),)

        kwargs['allow_domains'] = traversal.get("allow_domains", [])
        return GenericLinkExtractor(**kwargs).extract_links(response=response)

    @staticmethod
    def get_traversal_max_pages(traversal=None):
        return traversal.get('max_pages', 1)

    def get_current_traversal_requests_count(self, traversal_id=None):
        return self.crawler.stats.get_value(
            'crawlerflow-stats/traversals/{}/requests_count'.format(traversal_id)) or 0

    def run_traversals(self, spider_config=None, response=None):
        """
        if spider_traversal_id is None, it means this response originated from the
        request raised by the start urls.

        If it is Not None, the request/response is raised some traversal strategy.
        """
        current_request_traversal_id = response.meta.get('current_request_traversal_id', None)

        """
        Note on current_request_spider_id:
        This can never be none, including the ones that are started by start_urls .
        """
        traversal_data = {}
        to_traverse_links_list = []
        spider_traversals = spider_config.get('traversals', [])
        spiders = response.meta.get("manifest", {}).get("spiders")

        for traversal in spider_traversals:
            next_spider_id = traversal['next_spider_id']
            next_spider = get_spider_from_list(spider_id=next_spider_id, spiders=spiders)

            traversal['allow_domains'] = next_spider.get("spider_settings", {}).get("allowed_domains", [])
            traversal_id = traversal['traversal_id']
            current_request_traversal_count = self.get_current_traversal_requests_count(traversal_id)
            traversal_max_pages = self.get_traversal_max_pages(traversal=traversal)
            traversal_links = []
            is_this_request_from_same_traversal = self.is_this_request_from_same_traversal(response, traversal)
            shall_traverse = False

            if current_request_traversal_id is None:
                """
                start urls will not have this traversal_id set, so we should allow then to traverse
                """
                shall_traverse = True

            elif is_this_request_from_same_traversal and current_request_traversal_count < traversal_max_pages:
                """
                This block will be valid for the traversals from same spider_id, ie., pagination of a spider 
                """

                shall_traverse = True

            elif is_this_request_from_same_traversal:
                """
                """
                shall_traverse = True

            elif is_this_request_from_same_traversal is False and current_request_traversal_count < traversal_max_pages:
                """
                This for the spider_a traversing to spider_b, this is not pagination, but trsversing between 
                spiders.
                """
                shall_traverse = True

            if shall_traverse:
                traversal_links = self.run_traversal(response=response, traversal=traversal)
                traversal_data[traversal_id] = {"traversal_urls": traversal_links}
                """
                Then validate for max_pages logic if traversal_id's traversal has any!.
                This is where the further traversal for this traversal_id  is decided 
                """
                max_pages = self.get_traversal_max_pages(traversal=traversal)

                for link in traversal_links:

                    """
                    we are already incrementing, the last number, so using <= might make it 6 pages when 
                    max_pages is 5 
                    """
                    # print ("=============traversal_id", traversal_id)
                    if current_request_traversal_count < max_pages:
                        to_traverse_links_list.append(
                            {
                                "link": link,
                                "meta": {
                                    "spider_config": next_spider,
                                    "manifest": response.meta.get("manifest"),
                                    "current_request_traversal_id": traversal_id,
                                    "current_request_traversal_count": current_request_traversal_count,
                                    "current_traversal_max_count": max_pages,

                                }}
                        )

                    current_request_traversal_count += 1

            print("Extracted {} traversal_links for traversal_id:'{}' in url:{}".format(len(traversal_links),
                                                                                        traversal_id, response.url))
        return traversal_data, to_traverse_links_list

    # def login_request(self):
