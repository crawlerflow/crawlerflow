DEFAULT_SETTINGS_FOR_SCRAPY = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': False,
    'TELNETCONSOLE_PORT': [6023, 6073],
    'ITEM_PIPELINES': {
        'crawlerflow.contrib.pipelines.others.json.JsonFileWriterPipeline': 1,
        'crawlerflow.contrib.pipelines.others.csv.CsvFileWriterPipeline': 2,

        'crawlerflow.contrib.pipelines.nosql.mongodb.MongoDBPipeline': 3,
        'crawlerflow.contrib.pipelines.nosql.elasticsearch.ElasticSearchPipeline': 4,
    },
    'LOGSTATS_INTERVAL': 1,
    'DOWNLOADER_MIDDLEWARES': {
        "crawlerflow.contrib.middlewares.downloaders.download_time.CrawlerFlowDownloadTime": 110,
        "crawlerflow.contrib.middlewares.downloaders.controllers.IgnoreTraversalRequestsController": 111,
        "crawlerflow.contrib.middlewares.downloaders.controllers.SpiderRequestsBasedStopController": 112,
        "crawlerflow.contrib.middlewares.downloaders.controllers.SpiderResponsesBasedStopController": 113,
        "crawlerflow.contrib.middlewares.downloaders.spider_delay.IndividualSpiderDownloadDelay": 114,
        "crawlerflow.contrib.middlewares.downloaders.spider_analytics.IndividualSpiderRequestStats": 121,
        "crawlerflow.contrib.middlewares.downloaders.status.CrawlerFlowStatusStats": 800,
        "crawlerflow.contrib.middlewares.downloaders.spider_analytics.IndividualSpiderResponseStats": 801,
        "crawlerflow.contrib.middlewares.downloaders.browser_engine.BrowsersEngineBrowserMiddleware": 802,
    },
    'EXTENSIONS': {
        'crawlerflow.contrib.extensions.timeseries.CrawlerFlowTimeSeriesStats': 10,
        'crawlerflow.contrib.extensions.logstats.CrawlerFlowLogStats': 11,
        'crawlerflow.contrib.extensions.requests.CrawlerFlowRequestsStats': 12
    },
    # 'FEED_FORMAT': 'json',
    # 'FEED_URI': "data.json",
    'LOG_ENABLED': False
}
