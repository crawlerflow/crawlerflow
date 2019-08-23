class CrawlerFlowSpiderCookies(object):
    """
    This will set the spider cookies from spider_settings of single spider config
    """

    def process_request(self, request, spider):
        cookies = spider.spider_config.get("spider_settings", {}).get("cookies", {})
        if cookies:
            for k, v in cookies.items():
                request.headers('{}'.format(k), v)
