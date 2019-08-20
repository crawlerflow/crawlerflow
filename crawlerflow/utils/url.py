from urllib.parse import urlparse


def get_urn(url):
    """
    convert https://blog.scrapinghub.com/page/6/ into blog.scrapinghub.com/page/6/
    :param url:
    :return:
    """
    if "://" in url:
        return url.split("://")[1]
    return url


def get_domain(url):
    url_parsed = urlparse(url)
    return url_parsed.netloc


def get_absolute_url(url=None, origin_url=None):
    url = url.lstrip("/")

    url_parsed = urlparse(origin_url)
    scheme = url_parsed.scheme
    host = url_parsed.netloc
    if "://" in url:
        return url
    else:
        url = "{}://{}/{}".format(scheme, host, url)
        return url
