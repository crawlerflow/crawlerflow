import logging
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)


class BrowserEngineRetryMiddleware(object):
    """

    This middleware would be usefull when browser engines are busy
    processing other requests.

    No extra settings needed other than browser_settings
    """
    priority_adjust = 1
    browser_engine_retry_http_codes = [110]
    max_retry_times = 100

    def _retry(self, request, reason, spider):
        retries = request.meta.get('browser_engine_retry_times', 0) + 1
        retry_times = self.max_retry_times
        if 'browser_engine_max_retry_times' in request.meta:
            retry_times = request.meta['browser_engine_max_retry_times']

        stats = spider.crawler.stats
        if retries <= retry_times:
            # Log entry here
            logger.debug("BrowserEngine Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['browser_engine_retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('browser-engine/retry/count')
            stats.inc_value('browser-engine/retry/reason_count/%s' % reason)
            return retryreq
        else:
            stats.inc_value('browser-engine/retry/max_reached')
            logger.debug("BrowserEngine Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            # Log Entry here.

    def process_exception(self, request, exception, spider):
        retry_disabled = spider.spider_config.get("browser_engine_settings", {}).get("retry_disabled", False)
        if not retry_disabled:
            return self._retry(request, exception, spider)

    def process_response(self, request, response, spider):
        browser_engine_settings = spider.spider_config.get("browser_engine_settings")
        if browser_engine_settings:
            if browser_engine_settings.get('retry_disabled', False):
                return response
            if response.status in self.browser_engine_retry_http_codes:
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response
        return response
