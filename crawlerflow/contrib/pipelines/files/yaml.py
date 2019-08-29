import json
from ..base import CrawlerFlowPipelineBase


class YamlWriterPipeline(CrawlerFlowPipelineBase):

    def open_spider(self, spider):
        self.file = open('items.csv', 'w')

    def close_spider(self, spider):
        self.file.close()

