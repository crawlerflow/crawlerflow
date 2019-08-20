import time


class IndividualSpiderDownloadDelay(object):
    """
    Individual Spider Download delay.


    """

    def process_request(self, request, spider):
        download_delay = spider.spider_config.get("spider_settings", {}).get("download_delay")
        print ("==============download_delay,", download_delay)
        if download_delay:
            time.sleep(download_delay)
