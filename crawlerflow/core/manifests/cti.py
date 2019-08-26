import sys
import os
import yaml


class CTIManifestManager(object):
    """



    """
    ib_functions = None
    required_files = ["manifest.yml", "ib_functions.py", "start-urls.txt"]
    manifest = None

    def __init__(self, cf_path="."):
        print("===========================================================")
        print("===============     CrawlerFlow vBeta     =================")
        print("===============   http://crawlerfow.com   =================")
        print("===========================================================")
        print("Setting CrawlerFlow path as: {}".format(cf_path))
        self.cf_path = cf_path or "."
        self.ib_functions = None
        self.manifest = None
        self.start_urls = []

    def import_files(self):

        self.cf_path = self.cf_path.rstrip("/")
        self.manifest = yaml.load(open("{}/manifest.yml".format(self.cf_path)), Loader=yaml.FullLoader)
        self.start_urls = [line.strip() for line in open("{}/start-urls.txt".format(self.cf_path)).readlines()]

        try:
            import ib_functions
        except Exception as e:
            print(e)
            ib_functions = None
        self.ib_functions = ib_functions

    def validate_cti_path_and_files(self):
        errors = []

        try:
            files_in_path = os.listdir(self.cf_path)
        except Exception as e:
            errors.append("No such path exist {}".format(self.cf_path))
            files_in_path = []
        if errors == 0:
            for required_file in self.required_files:
                if required_file not in files_in_path:
                    errors.append("{} file not in the path {}".format(required_file, self.cf_path))
        return errors

    def import_cti_transformations(self):
        if self.ib_functions:
            for transformation in self.manifest.get("transformations", []):
                if transformation.get("transformation_fn"):
                    method_to_call = getattr(self.ib_functions, transformation.get("transformation_fn"))
                    transformation['transformation_fn'] = method_to_call

    def import_extractor_functions(self):
        if self.ib_functions:
            for spider in self.manifest.get("spiders", []):
                for extractor in spider.get("extractors", []):
                    if extractor.get("extractor_fn"):
                        method_to_call = getattr(self.ib_functions, extractor.get("extractor_fn"))
                        extractor['extractor_fn'] = method_to_call

    def get_manifest(self):
        errors = self.validate_cti_path_and_files()
        if len(errors) > 0:
            return None, errors
        self.import_files()
        self.import_cti_transformations()
        self.import_extractor_functions()
        return self.manifest, self.start_urls, errors
