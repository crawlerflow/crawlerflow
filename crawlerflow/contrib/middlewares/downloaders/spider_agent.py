class CrawlerFlowSpiderAgent(object):
    """
    This will set the spider user agent from spider_settings of single spider config
    """

    def process_request(self, request, spider):
        spider_user_agent = spider.spider_config.get("spider_settings", {}).get("user_agent")
        if spider_user_agent:
            request.headers.setdefault(b'User-Agent', spider_user_agent)
