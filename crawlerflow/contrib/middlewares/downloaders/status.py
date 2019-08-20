class CrawlerFlowStatusStats(object):
    """
    This will let us determine the statuses of the responses
    """

    def process_response(self, request, response, spider):
        status = response.status
        spider.crawler.stats.inc_value('crawlerflow-stats/response-status/{}'.format(status), spider=spider)
        return response  # return response coz we should
