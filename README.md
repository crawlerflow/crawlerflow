# CrawlerFlow

Web Crawlers orchestration Framework that lets you create datasets from multiple web sources with yaml 
configurations.



**NOTE: This project is under active development**

[![Build Status](https://travis-ci.org/invanalabs/invana-bot.svg?branch=master)](https://travis-ci.org/invanalabs/invana-bot) 
[![codecov](https://codecov.io/gh/invanalabs/invana-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-bot) 


[**Features**](#features) | [**Install**](#install) | [**Usage**](#usage) | [**Documentation**](#documentation) | [**Support**](#support)


## Features

1. Write spiders in the YAML configuration.

2. Define multiple extractors per spider.
 
3. Traverse between multiple websites.

3. Use standard extractors to scrape data like Tables, Paragraphs, Meta data of the page.

4. Define custom extractors to scrapy the data in the format you want in yaml config.

5. Write Python Extractors for advanced extraction strategy


## Install

```bash
pip install git+https://github.com/crawlerflow/crawlerflow#egg=crawlerflow
# This project is under constant development and might brake any previous implementation.
```



## Usage

To run a single website spider, to extract information from one website only.

```bash
crawlerflow --path examples/ --type=web
```


## Documentation

Refer examples in the `examples/` folder or check [doc/index.md](docs/index.md) for more details.


## Support

Few features like IP rotation, headless browsing, data backups, scheduling and monitoring are 
available in our [InvanaBot Cloud](https://crawlerflow.com) version.

For any futher queries or dedicated support, please feel free to [contact us](http://crawlerflow.com)