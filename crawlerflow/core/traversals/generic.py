from scrapy.linkextractors import LinkExtractor
import re


class GenericLinkExtractor(object):
    """


    """

    def __init__(self,
                 restrict_xpaths=(),
                 restrict_css=(),
                 restrict_regex=(),
                 allow_domains=(),
                 link_extractor_cls=LinkExtractor, **kwargs):
        """

        :param restrict_xpaths: list of xpaths for links Extraction.
        :param restrict_css: list of xpath for links extraction
        :param restrict_regex: list of regex patterns
        :param link_extractor_cls: defaults to scrapy link extractor
        :param allow_domains: defaults to the allowed domains of spider
        """
        self.restrict_xpaths = restrict_xpaths
        self.restrict_css = restrict_css
        self.restrict_regex = restrict_regex
        self.allow_domains = allow_domains
        self.link_extractor_cls = link_extractor_cls

    def extract_links(self, response=None):
        all_links = self.link_extractor_cls(allow=self.restrict_xpaths,
                                            restrict_xpaths=self.restrict_xpaths,
                                            restrict_css=self.restrict_css,
                                            allow_domains=self.allow_domains
                                            ).extract_links(response=response)
        all_links_strings = [link.url for link in all_links]

        filtered_links = []
        if "*" in self.allow_domains:
            return all_links_strings
        for domain in self.allow_domains:
            regex_domain = r"/{}".format(domain).replace(".", "\.")
            pattern = re.compile(regex_domain)
            for link in all_links_strings:
                if pattern.search(link):
                    filtered_links.append(link)
        return filtered_links
