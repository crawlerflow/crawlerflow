from twisted.internet import reactor
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.settings import Settings
from invana_bot2.contrib.spiders.web import InvanaBotSingleWebCrawler
from invana_bot2.contrib.spiders.xml import GenericXMLFeedSpider
from invana_bot2.contrib.spiders.api import GenericAPISpider
from scrapy import signals


class JobRunner(object):
    """


    """
    runner = CrawlerRunner()

    def start_job(self, job=None, callback_fn=None):
        print(job)
        spider_type = job['spider_type']

        if spider_type == "web":
            spider_cls = InvanaBotSingleWebCrawler
        elif spider_type == "xml":
            spider_cls = GenericXMLFeedSpider
        elif spider_type == "api":
            spider_cls = GenericAPISpider
        else:
            spider_cls = None

        spider_settings = job['spider_settings']
        spider_kwargs = job['spider_kwargs']

        def engine_stopped_callback():
            print("Alright! I'm done with job.")
            reactor.stop()

        spider = Crawler(spider_cls, Settings(spider_settings))
        spider.signals.connect(engine_stopped_callback, signals.engine_stopped)

        self.runner.crawl(spider, **spider_kwargs)
        reactor.run()
