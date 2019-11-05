import uuid
from scrapy.http.headers import Headers


def generate_random_id():
    return str(uuid.uuid4().hex)


def convert_dict_to_scrapy_headers(headers_dict):
    return Headers(headers_dict)
