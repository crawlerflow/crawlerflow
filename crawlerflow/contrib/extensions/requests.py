from scrapy.extensions.logstats import LogStats
import os
import yaml
from scrapy import signals
from scrapy.exceptions import NotConfigured


class CrawlerFlowRequestsStats(object):
    """
    This will write


    """

    def __init__(self, stats, interval=60.0):
        self.stats = stats
        self.interval = interval

        # crawler.signals.connect(self.request_received, signal=signals.request_received)

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')
        if not interval:
            raise NotConfigured
        o = cls(crawler.stats, interval)
        crawler.signals.connect(o.response_received, signal=signals.response_received)

        return o

    def response_received(self, response, request, spider):
        path = os.getcwd()
        log_director = '{}/.logs'.format(path)
        if not os.path.exists(log_director):
            os.makedirs(log_director)
        print ("response.headers", response.headers)
        response_stats = {
            "url": response.url,
            "status": response.status,
            "user-agent": response.headers.get("user-agent"),
            "referer-url": response.headers.get("Referer"),
            "elapsed_time": request.meta['request_end_time'] - request.meta['request_start_time']
        }

        with open('{}/all-requests.txt'.format(log_director), 'a') as yml:
            line = ",".join([str(v) for k, v in response_stats.items()])
            yml.write("{}\n".format(line))
