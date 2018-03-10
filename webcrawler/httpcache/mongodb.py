from __future__ import print_function
import os
import gzip
import logging
from six.moves import cPickle as pickle
from time import time
from w3lib.http import headers_raw_to_dict, headers_dict_to_raw
from scrapy.http import Headers, Response
from scrapy.responsetypes import responsetypes
from scrapy.utils.request import request_fingerprint
from scrapy.utils.project import data_path
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_bytes, to_unicode, garbage_collect
import pymongo
import urllib.parse
import json
from scrapy.http.headers import Headers

logger = logging.getLogger(__name__)


class MongoDBCacheStorage(object):
    """
    should set HTTPCACHE_MONGODB_DATABASE in the settings.py


    """
    COLLECTION_NAME = "weblinks"

    def __init__(self, settings):
        self.database = settings['HTTPCACHE_MONGODB_DATABASE']
        self.database_host = settings.get('HTTPCACHE_MONGODB_HOST', '127.0.0.1')

        self.database_port = settings.get('HTTPCACHE_MONGODB_PORT', 27017)

        auth = {
            "username": settings.get('HTTPCACHE_MONGODB_USERNAME', ''),
            "password": settings.get('HTTPCACHE_MONGODB_PASSWORD', '')
        }
        if auth.get('username'):
            self.db_client = pymongo.MongoClient(self.database_host, **auth)
        else:
            self.db_client = pymongo.MongoClient(self.database_host, )
        self.db = self.db_client[self.database]

        self.expiration_secs = settings.getint('HTTPCACHE_EXPIRATION_SECS')

    def open_spider(self, spider):
        logger.debug("Using mongodb cache storage with database name %(database)s" % {'database': self.database},
                     extra={'spider': spider})

    def close_spider(self, spider):
        pass

    def retrieve_response(self, spider, request):
        data = self._read_data(spider, request)
        if data is None:
            return  # not cached
        url = data['url']
        status = data['status']
        headers = Headers(data['headers'])
        body = data['body']
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)
        return response

    def _clean_headers(self, obj):
        cleaned_object = {}
        for k, v in obj.items():
            cleaned_object[k.decode('utf-8')] = v[0].decode('utf-8')
        return cleaned_object

    def store_response(self, spider, request, response):
        data = {
            'status': response.status,
            'url': response.url,
            'headers': self._clean_headers(response.headers),
            'body': response.body,
        }

        print(data)

        self.db[self.COLLECTION_NAME].insert_one(data)

    def _read_data(self, spider, request):
        return self.db[self.COLLECTION_NAME].find_one({'url': request.url})

    def _request_key(self, request):
        return to_bytes(request_fingerprint(request))