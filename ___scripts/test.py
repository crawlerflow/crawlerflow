from crawlerflow.strategies.cti import JobRunner
from crawlerflow.core.jobs.default import JobGenerator
from crawlerflow.contrib.settings import DEFAULT_SETTINGS_FOR_SCRAPY

job_generator = JobGenerator(path="/Users/rrmerugu/Projects/invanalabs/invana-bot/___scripts/", settings=DEFAULT_SETTINGS_FOR_SCRAPY)
job = job_generator.create_spider_job()

runner = JobRunner()
runner.start_job(job=job)
