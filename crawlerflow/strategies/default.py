from scrapy.crawler import CrawlerProcess
from crawlerflow.contrib.settings import DEFAULT_SETTINGS_FOR_SCRAPY
from crawlerflow.core.jobs.default import JobGenerator


class DefaultRunner(object):

    def run(self, spider_type=None, spider_kwargs=None, spider_settings=None):
        process = CrawlerProcess(settings=spider_settings or DEFAULT_SETTINGS_FOR_SCRAPY, **spider_kwargs)
        process.crawl(spider_type)
        process.start()  # the script will block here until the crawling is finished
