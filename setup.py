#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='crawlerflow',
    version='0.1.36',
    description='Web Crawlers orchestration Framework that lets you create datasets from multiple web sources.',
    author='Ravi Raja Merugu',
    author_email='ravi@invanalabs.ai',
    url='https://github.com/crawlerflow/crawlerflow',
    packages=find_packages(
        exclude=("dist", "docs", "examples", "tests",)
    ),
    install_requires=[
        'lxml==4.1.1',
        'pymongo',
        'requests',
        'Scrapy==1.6.0',
        'pyyaml',
        'python-slugify',
        'elasticsearch'
    ],
    entry_points={
        'console_scripts': ['crawlerflow = crawlerflow.core.cmd.run:run']
    },
)
