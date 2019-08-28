from scrapy.extensions.logstats import LogStats
import os
import yaml


class CrawlerFlowLogStats(LogStats):

    def log(self, spider):
        path = os.getcwd()
        log_director = '{}/.logs'.format(path)
        if not os.path.exists(log_director):
            os.makedirs(log_director)

        with open('{}/stats.txt'.format(log_director), 'w') as yml:
            yaml.dump(self.stats.get_stats(), yml, allow_unicode=True)
