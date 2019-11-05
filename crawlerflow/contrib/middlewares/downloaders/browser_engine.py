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

    @staticmethod
    def get_headers_from_response(response):
        cookies = response['cookies']
        cookies_dict = {}
        headers = {}
        if cookies is not None:
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie['value']
        headers['Cookies'] = cookies_dict
        return headers

    @staticmethod
    def get_headers_from_post_data(request):
        all_headers = {}
        headers = request.headers
        cookies_temp = [cookie.decode().split(";")[0] for cookie in headers.getlist("Set-Cookie")]
        cookies = []
        for cookie in cookies_temp:
            _ = cookie.split("=")
            cookies.append({
                "name": _[0],
                "value": _[1]
            })

        all_headers['Cookies'] = cookies
        # init_request_kwargs['cookies'] = cookies
        return all_headers

    def process_request(self, request, spider):
        spider_id = spider.spider_config.get("spider_id")
        browser_engine_settings = spider.spider_config.get("browser_engine_settings")
        form_settings = spider.spider_config.get("login_settings", {}).get("form_settings")
        use_browser = spider.spider_config.get("login_settings", {}) \
            .get("use_browser", True if browser_engine_settings else False)
        """
        
        This will ignore browser engine request if use_browser=False
        """
        is_login_request = request.meta.get("is_login_request", False)
        shall_use_browser = False
        if browser_engine_settings:
            shall_use_browser = True

        if shall_use_browser and is_login_request and use_browser is False:
            shall_use_browser = False

        if shall_use_browser is True:

            token = browser_engine_settings.get("token")
            browser_type = browser_engine_settings.get("browser_type", "default")
            browser_url = browser_engine_settings.get("browser_engine_host", "http://0.0.0.0:5000")
            take_screenshot = browser_engine_settings.get("take_screenshot", False)
            all_headers = self.get_headers_from_post_data(request)

            print("request_headers", all_headers)
            # print ("======", request.headers)
            if browser_type != "default":
                url = urllib.parse.quote(request.url)

                payload = {"headers": all_headers}

                if is_login_request:
                    payload['form_data'] = form_settings
                try:
                    request_response = requests.post(
                        "{}/execute?url={}&enable_screenshot={}&token={}".format(
                            browser_url,
                            url,
                            1 if take_screenshot is True else 0,
                            token
                        ),
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        verify=False,
                        timeout=self.timeout
                    )
                    # TODO - remove verify=False with caution
                    if request_response.status_code == 200:
                        request_response_json = request_response.json()
                        html = request_response_json['response']['html']
                        screenshot = request_response_json['response']['screenshot']
                        request.meta['screenshot'] = screenshot
                        body = str.encode(html)
                        headers = self.get_headers_from_response(request_response_json['response'])
                        request.cookies = request_response_json['response']['cookies']
                        print("post response headers", headers)
                        print("request.cookies", request.cookies)
                        return HtmlResponse(
                            request.url,
                            body=body,
                            encoding='utf-8',
                            request=request,
                            headers=headers,
                            # headers=headers
                            # headers={
                            # "Cookies": request_response_json['response']['cookies'],
                            # }
                        )
                except Exception as e:
                    raise Exception("Browser Engine failed to get the data for spider: {}".format(spider_id))
