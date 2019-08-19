from scrapy.crawler import CrawlerProcess
from invana_bot2.contrib.settings import DEFAULT_SETTINGS_FOR_SCRAPY
from invana_bot2.core.jobs.default import JobGenerator


class DefaultRunner(object):

    def run(self, spider_type=None, spider_kwargs=None, spider_settings=None):
        print (spider_kwargs)
        process = CrawlerProcess(settings=spider_settings or DEFAULT_SETTINGS_FOR_SCRAPY, **spider_kwargs)

        process.crawl(spider_type)
        process.start()  # the script will block here until the crawling is finished


# job_generator = JobGenerator(path=".", settings=DEFAULT_SETTINGS_FOR_SCRAPY)
# job = job_generator.create_spider_job()
#
# DefaultRunner().run(**job)
