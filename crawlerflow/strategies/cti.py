from twisted.internet import reactor
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.settings import Settings
from crawlerflow.contrib.spiders.web import InvanaBotSingleWebCrawler
from crawlerflow.contrib.spiders.xml import GenericXMLFeedSpider
from crawlerflow.contrib.spiders.api import GenericAPISpider
from scrapy import signals
import yaml
import os
from datetime import datetime


class CrawlerFlowJobRunner(object):
    """


    """
    runner = CrawlerRunner()

    def start_job(self, job=None, path=None, callback_fn=None):
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

        spider = Crawler(spider_cls, Settings(spider_settings))

        def engine_stopped_callback():
            print("Alright! I'm done with job.")
            reactor.stop()

            log_director = '{}/.logs'.format(path)
            if not os.path.exists(log_director):
                os.makedirs(log_director)
            with open('{}/log.txt'.format(log_director), 'w') as yml:
                yaml.dump(spider.stats.get_stats(), yml, allow_unicode=True)

        def engine_started_callback():
            log_director = '{}/.logs'.format(path)

            if not os.path.exists(log_director):
                os.makedirs(log_director)

            # remove any log files
            for file in sorted(os.listdir(log_director)):
                os.remove("{}/{}".format(log_director, file))
            f = open('{}/timeseries-log.txt'.format(log_director), 'w')
            datum = {
                "item_scraped_count": 0,
                "response_received_count": 0,
                "requests_count": 0,
                "time": str(datetime.now())
            }
            line = ",".join([str(v) for k, v in datum.items()])
            f.write("{}\n".format(line))
            f.close()

        spider.signals.connect(engine_started_callback, signals.engine_started)
        spider.signals.connect(engine_stopped_callback, signals.engine_stopped)

        self.runner.crawl(spider, **spider_kwargs)
        reactor.run()
