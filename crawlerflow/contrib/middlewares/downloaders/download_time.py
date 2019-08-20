from time import time
from scrapy.http import Response


class CrawlerFlowDownloadTime(object):
    """
    This will let us determine the time took for a request to be finished.
    """

    def process_request(self, request, spider):
        request.meta['request_start_time'] = time()
        # # this not block middlewares which are has greater number then this
        # return None

    def process_response(self, request, response, spider):
        request.meta['request_end_time'] = time()
        return response  # return response coz we should

    def process_exception(self, request, exception, spider):
        request.meta['request_end_time'] = time()
        return Response(
            url=request.url,
            status=110,
            request=request)
