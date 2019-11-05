#

class IndividualSpiderRequestStats(object):
    """
    To calculate the spider stats
    """

    def process_request(self, request, spider):
        current_request_traversal_id = request.meta.get("current_request_traversal_id")
        if current_request_traversal_id:
            spider.crawler.stats.inc_value(
                'crawlerflow-stats/traversals/{}/requests_count'.format(current_request_traversal_id), spider=spider)

        spider_id = spider.spider_config.get("spider_id")
        spider.crawler.stats.inc_value('crawlerflow-stats/spiders/{}/requests_count'.format(spider_id), spider=spider)
        spider.crawler.stats.inc_value('downloader/request_count', spider=spider)


class IndividualSpiderResponseStats(object):
    """
    This will calculate the individual spider stats
    """

    def process_response(self, request, response, spider):
        spider_id = spider.spider_config.get("spider_id")
        spider.crawler.stats.inc_value('crawlerflow-stats/{}/responses_count'.format(spider_id), spider=spider)

        current_request_traversal_id = request.meta.get("current_request_traversal_id")
        if current_request_traversal_id:
            spider.crawler.stats.inc_value(
                'crawlerflow-stats/traversals/{}/responses/all/count'.format(current_request_traversal_id), spider=spider)
            if response.status == 200:
                spider.crawler.stats.inc_value(
                    'crawlerflow-stats/traversals/{}/responses/200/count'.format(current_request_traversal_id), spider=spider)

        return response
