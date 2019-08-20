# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import os
from crawlerflow.strategies.cti import CrawlerFlowJobRunner
from crawlerflow.core.jobs.default import JobGenerator
from crawlerflow.contrib.settings import DEFAULT_SETTINGS_FOR_SCRAPY


def run():
    spider_choices = (
        "web",
        "xml",
        "api"
    )
    parser = argparse.ArgumentParser(
        description='CrawlerFlow - Highly scalable Crawler Orchestration Products and Services for Humans with'
                    'High-Velocity data needs.')

    parser.add_argument('--path', type=str, default=os.getcwd(), help='The path of the manifest.yml')
    parser.add_argument('--type', type=str,
                        default='web',
                        help='options are : {}'.format(",".join(spider_choices)),
                        choices=spider_choices)

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    cf_type = args.type
    print("path", path)

    job_generator = JobGenerator(path=path,
                                 type=cf_type,
                                 settings=DEFAULT_SETTINGS_FOR_SCRAPY)
    job = job_generator.create_spider_job()

    runner = CrawlerFlowJobRunner()
    runner.start_job(job=job)
