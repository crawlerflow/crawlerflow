from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from crawlerflow.contrib.spiders.web import CrawlerFlowWebSpider
from crawlerflow.contrib.spiders.xml import GenericXMLFeedSpider
from crawlerflow.contrib.spiders.api import GenericAPISpider
from scrapy import signals
from crawlerflow.core.storage.default import item_scraped_callback
import yaml
import os
from datetime import datetime
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.exceptions import DontCloseSpider


def spider_idle_callback(spider):
    print("============ SPIDER IDLE", spider)
    raise DontCloseSpider


def spider_closed_callback(spider, reason):
    print("============= SPIDER CLOSED", reason)


class CrawlerFlowJobRunner(object):
    """


    """

    @staticmethod
    def clean_directory(path=None):
        log_director = '{}/.logs'.format(path)

        if not os.path.exists(log_director):
            os.makedirs(log_director)
        # remove data.json
        data_path = os.path.join(path, "data.json")
        if os.path.exists(data_path):
            os.remove(data_path)

        # remove any log files
        for file in sorted(os.listdir(log_director)):
            os.remove("{}/{}".format(log_director, file))

    def validate_storages(self, data_storages=None):
        pass
        # for data_storage in data_storages:
        #     # validate
        #     print(data_storage)

    def start_job(self, job=None, path=None, callback_fn=None):
        spider_type = job['spider_type']

        if spider_type == "web":
            spider_cls = CrawlerFlowWebSpider
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
            with open('{}/stats.txt'.format(log_director), 'w') as yml:
                yaml.dump(spider.stats.get_stats(), yml, allow_unicode=True)

        def engine_started_callback():
            log_director = '{}/.logs'.format(path)

            f = open('{}/timeseries-stats.txt'.format(log_director), 'w')
            datum = {
                "item_scraped_count": 0,
                "response_received_count": 0,
                "requests_count": 0,
                "time": str(datetime.now())
            }
            line = ",".join([str(v) for k, v in datum.items()])
            f.write("{}\n".format(line))
            f.close()
            open('{}/all-requests.txt'.format(log_director), 'w').close()

        self.clean_directory(path=path)
        self.validate_storages(data_storages=job['spider_kwargs'].get("manifest", {}).get("data_storages", []))

        # process_settings = {
        #     "LOG_LEVEL": spider_settings.get("LOG_LEVEL", ),
        #     "CONCURRENT_REQUESTS": spider_settings.get("CONCURRENT_REQUESTS", 1)
        # }
        process = CrawlerProcess()  # TODO - send only log for debug mode
        spider.signals.connect(engine_started_callback, signals.engine_started)
        spider.signals.connect(engine_stopped_callback, signals.engine_stopped)
        # spider.signals.connect(spider_idle_callback, signals.spider_idle)
        spider.signals.connect(spider_closed_callback, signals.spider_closed)
        # spider.signals.connect(item_scraped_callback, signals.item_scraped)

        process.crawl(spider, **spider_kwargs)
        reactor.run()
