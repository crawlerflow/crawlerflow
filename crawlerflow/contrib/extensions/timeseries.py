from scrapy.extensions.logstats import LogStats
from datetime import datetime
import os
import yaml


class CrawlerFlowTimeSeriesStats(LogStats):

    def log(self, spider):
        item_scraped_count = self.stats.get_value('item_scraped_count', 0)
        requests_count = self.stats.get_value('downloader/request_count', 0)
        response_received_count = self.stats.get_value('response_received_count', 0)
        datum = {
            "item_scraped_count": item_scraped_count,
            "response_received_count": response_received_count,
            "requests_count": requests_count,
            "time": str(datetime.now())
        }
        path = os.getcwd()
        log_director = '{}/.logs'.format(path)
        if not os.path.exists(log_director):
            os.makedirs(log_director)

        timeseries_log_file = '{}/timeseries-stats.txt'.format(log_director)
        with open(timeseries_log_file, 'a') as fh:
            line = ",".join([str(v) for k, v in datum.items()])
            fh.write("{}\n".format(line))
