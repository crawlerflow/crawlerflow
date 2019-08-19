class SpiderController(object):
    """
    This middleware will stop the requests when the scraper reaches the maximum traversal
    requests.

    TODO - currently max pages is considered as maximum requests, without considering
    retry requests.

    """

    def process_request(self, request, spider):
        spider_id = spider.spider_config.get("spider_id")
        spider_requests_count = spider.crawler.stats.inc_value('invana-stats/spiders/{}/requests_count'.format(spider_id),
                                                               spider=spider)

