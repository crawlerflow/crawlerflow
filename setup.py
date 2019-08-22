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
        'feedparser==5.2.1',
        'lxml==4.1.1',
        'pymongo==3.7.2',
        'requests==2.21.0',
        'Scrapy==1.6.0',
        'pyyaml==5.1',
        'python-slugify'
    ],
    entry_points={
        'console_scripts': ['crawlerflow = crawlerflow.core.cmd.run:run']
    },
)
