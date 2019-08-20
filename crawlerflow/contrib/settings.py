DEFAULT_SETTINGS_FOR_SCRAPY = {
    'COMPRESSION_ENABLED': True,
    'HTTPCACHE_ENABLED': True,
    'TELNETCONSOLE_PORT': [6023, 6073],
    'ITEM_PIPELINES': {
        'crawlerflow.contrib.pipelines.default.InvanaDataPipeline': 1,
    },
    'LOGSTATS_INTERVAL': 1,
    'DOWNLOADER_MIDDLEWARES': {
        "crawlerflow.contrib.middlewares.downloaders.download_time.CrawlerFlowDownloadTime": 110,
        "crawlerflow.contrib.middlewares.downloaders.controllers.IgnoreTraversalRequestsController": 111,
        "crawlerflow.contrib.middlewares.downloaders.controllers.SpiderRequestsBasedStopController": 112,
        "crawlerflow.contrib.middlewares.downloaders.controllers.SpiderResponsesBasedStopController": 113,
        "crawlerflow.contrib.middlewares.downloaders.spider_analytics.IndividualSpiderRequestStats": 121,
        "crawlerflow.contrib.middlewares.downloaders.spider_analytics.IndividualSpiderResponseStats": 800,
    },
    'EXTENSIONS': {
        'crawlerflow.contrib.extensions.timeseries.CrawlerFlowTimeSeriesStats': 10,
        'crawlerflow.contrib.extensions.logstats.CrawlerFlowLogStats': 11,
        'crawlerflow.contrib.extensions.requests.CrawlerFlowRequestsStats': 12,
    }
}
