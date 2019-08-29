DEFAULT_SETTINGS_FOR_SCRAPY = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': False,
    'TELNETCONSOLE_PORT': [6023, 6073],
    'ITEM_PIPELINES': {
        'crawlerflow.contrib.pipelines.files.json.JsonFileWriterPipeline': 1,
        'crawlerflow.contrib.pipelines.files.csv.CsvFileWriterPipeline': 2,

        'crawlerflow.contrib.pipelines.nosql.mongodb.MongoDBPipeline': 3,
        'crawlerflow.contrib.pipelines.nosql.elasticsearch.ElasticSearchPipeline': 4,
    },
    'LOGSTATS_INTERVAL': 5,
    'DOWNLOADER_MIDDLEWARES': {
        "crawlerflow.contrib.middlewares.downloaders.browser_engine_retry.BrowserEngineRetryMiddleware": 101,
        "crawlerflow.contrib.middlewares.downloaders.download_time.CrawlerFlowDownloadTime": 110,
        "crawlerflow.contrib.middlewares.downloaders.controllers.IgnoreTraversalMaxSuccessPagesController": 111,
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
    # 'ROBOTSTXT_OBEY': True,
    # 'ROBOTSTXT_ENABLED': True,
    'CONCURRENT_REQUESTS': 1,
    # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    # 'FEED_FORMAT': 'json',
    # 'FEED_URI': "data.json",
    'LOG_ENABLED': True,
    'LOG_LEVEL': "INFO",
    # 'LOG_STDOUT': False,
    'LOG_FILE': 'log.txt',
    'RETRY_ENABLED': True,
    'RETRY_TIMES': 10,
    # 'LOG_ENCODING': 'utf-8',
    # 'SCHEDULER_DEBUG': True,
    'USER_AGENT': "CrawlerFlow/beta (+http://crawlerflow.com/bot.html)"

}
