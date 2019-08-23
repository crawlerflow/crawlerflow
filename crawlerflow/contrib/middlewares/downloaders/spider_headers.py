class CrawlerFlowSpiderHeaders(object):
    """
    This will set the spider headers from spider_settings of single spider config
    """

    def process_request(self, request, spider):
        headers = spider.spider_config.get("spider_settings", {}).get("headers", {})
        if headers:
            for k, v in headers.items():
                request.headers('{}'.format(k), v)
