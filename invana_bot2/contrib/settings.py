DEFAULT_SETTINGS_FOR_SCRAPY = {
    'COMPRESSION_ENABLED': True,
    'HTTPCACHE_ENABLED': True,
    'TELNETCONSOLE_PORT': [6023, 6073],
    'ITEM_PIPELINES': {
        'invana_bot2.contrib.pipelines.default.InvanaDataPipeline': 1,
    },
    'DOWNLOADER_MIDDLEWARES': {
        "invana_bot2.contrib.middlewares.downloaders.spider_analytics.IndividualSpiderRequestStats": 121,
        "invana_bot2.contrib.middlewares.downloaders.spider_analytics.IndividualSpiderResponseStats": 800,
    }
}
