from ..manifests.cti import CTIManifestManager
from datetime import datetime
from crawlerflow.utils.other import generate_random_id
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class JobGenerator(object):
    """
        job_generator = JobGenerator(path="./", settings=<scrapy settings>)
        job = job_generator.create_spider_job()

    """

    def __init__(self, path="./", job_id=None, type=None, settings=None, **kwargs):
        """


        :param path:
        :param job_id:
        :param settings:
        :param extra_context:
        :param kwargs:
        """
        self.path = path
        self.type = type
        self.job_id = generate_random_id() if job_id is None else job_id
        self.settings = settings or {}
        self.context = None

    def get_spider_type(self, spider_data):
        """

        :param spider_data:
        :return:
        """
        return spider_data.get("spider_type", "web")

    def import_files(self):
        """

        :return:
        """
        manifest_manager = CTIManifestManager(
            cf_path=self.path
        )
        manifest, start_urls, errors = manifest_manager.get_manifest()
        return manifest, start_urls, errors

    def generate_spider_kwargs(self, spider_config=None, start_urls=None, manifest=None):
        """

        :param spider_config:
        :param manifest:
        :return:
        """
        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)  # TODO - add regex types of needed.
        ]
        context = manifest.get("context")
        if context is None:
            context = {}
        if 'job_id' not in context.keys():
            context['job_id'] = self.job_id
            context['job_started'] = datetime.now()
        spider_kwargs = {
            "start_urls": start_urls,
            "allowed_domains": [],
            "rules": rules,
            "spider_config": spider_config,
            "manifest": manifest,
            "context": context,
        }
        return spider_kwargs

    def create_spider_job(self):
        """

        :return:
        """
        manifest, start_urls, errors = self.import_files()
        spider_config = manifest.get("spiders", [])[0]
        spider_type = self.get_spider_type(spider_data=spider_config)
        settings_from_manifest = manifest.get("settings", {})
        for k, v in settings_from_manifest.items():
            self.settings[k.upper()] = v
        spider_kwargs = self.generate_spider_kwargs(spider_config=spider_config, start_urls=start_urls,
                                                    manifest=manifest)
        return {
            "spider_type": spider_type,
            "spider_kwargs": spider_kwargs,
            "spider_settings": self.settings
        }
