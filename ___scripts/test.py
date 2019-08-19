from invana_bot2.strategies.cti import JobRunner
from invana_bot2.core.jobs.default import JobGenerator
from invana_bot2.contrib.settings import DEFAULT_SETTINGS_FOR_SCRAPY

job_generator = JobGenerator(path="/Users/rrmerugu/Projects/invanalabs/invana-bot/___scripts/", settings=DEFAULT_SETTINGS_FOR_SCRAPY)
job = job_generator.create_spider_job()

runner = JobRunner()
runner.start_job(job=job)
