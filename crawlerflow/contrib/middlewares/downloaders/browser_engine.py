from scrapy.http import HtmlResponse
import urllib.parse
import requests


class BrowsersEngineBrowserMiddleware(object):
    """
    Scrapy middleware handling the requests using browser engine



    Example usage:
      browser_engine_settings:
        host: http://0.0.0.0:5000
        browser_type: selenium
        token: iamlazydeveloper
        take_screenshot: false
      login_settings:
        url: "https://www.xyzabc.co/users/sign_in"
        username: "*******"
        password: "******"
        form_identifiers:
          form_selector: ".sign__form form"
          username_field: "user[email]"
          password_field: "user[password]"
          formnumber: 0
        validation_string: "UserName"
        use_browser: false

    """
    timeout = 180

    def process_request(self, request, spider):
        spider_id = spider.spider_config.get("spider_id")
        browser_engine_settings = spider.spider_config.get("browser_engine_settings")
        use_browser = spider.spider_config.get("login_settings", {}) \
            .get("use_browser", True if browser_engine_settings else False)
        """
        
        This will ignore browser engine request if use_browser=False
        """

        if browser_engine_settings and use_browser is True:

            token = browser_engine_settings.get("token")
            browser_type = browser_engine_settings.get("browser_type", "default")
            browser_url = browser_engine_settings.get("browser_engine_host", "http://0.0.0.0:5000")
            take_screenshot = browser_engine_settings.get("take_screenshot", False)
            if browser_type != "default":
                url = urllib.parse.quote(request.url)
                request_response = requests.get("{}/render?url={}&browser_type={}&enable_screenshot={}&token={}".format(
                    browser_url,
                    url,
                    browser_type, 1 if take_screenshot is True else 0, token),
                    verify=False,
                    # timeout=self.timeout
                )
                # TODO - remove verify=False with caution
                if request_response.status_code == 200:
                    request_response_json = request_response.json()
                    html = request_response_json['response']['html']
                    screenshot = request_response_json['response']['screenshot']
                    request.meta['screenshot'] = screenshot
                    body = str.encode(html)
                    request.cookies = request_response_json['response']['cookies']
                    print("request.cookies", request.cookies)
                    return HtmlResponse(
                        request.url,
                        body=body,
                        encoding='utf-8',
                        request=request,
                    )

                else:
                    raise Exception("Browser Engine failed to get the data for spider: {}".format(spider_id))
