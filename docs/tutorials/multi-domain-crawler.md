# Multi Domain Crawler



## Crawl, Traverse and Index

```yaml
# spider_manifest.yml
spider_id: blog_list
whitelisted_domains:
- blog.scrapinghub.com
start_urls:
- https://blog.scrapinghub.com
extractors:
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
- extractor_type: ParagraphsExtractor
  extractor_id: paragraphs
- extractor_type: CustomContentExtractor
  extractor_id: blog_list_parser
  data_selectors:
  - selector_id: blogs
    selector: ".post-listing .post-item"
    selector_attribute: element
    multiple: true
    child_selectors:
    - selector_id: url
      selector: ".post-header h2 a"
      selector_type: css
      selector_attribute: href
      multiple: false
    - selector_id: title
      selector: ".post-header h2 a"
      selector_type: css
      selector_attribute: text
      multiple: false
    - selector_id: content
      selector: ".post-content"
      selector_type: css
      selector_attribute: html
      multiple: false
traversals:
- traversal_type: pagination
  pagination:
    selector: ".next-posts-link"
    selector_type: css
    max_pages: 2
  next_spider_id: blog_list
transformations:
- transformation_id: default
  transformation_fn: transformation_fn
callbacks:
- callback_id: default
  data_storage_id: default
  url: http://localhost/api/callback
  request_type: POST
  payload: {}
  headers:
    X-TOKEN: abc123456789
data_storages:
- data_storage_id: default
  transformation_id: default
  connection_uri: mongodb://127.0.0.1/spiders_data_index
  collection_name: blog_list
  unique_key: url
settings:
  allowed_domains:
  - blog.scrapinghub.com
  download_delay: 5
context:
  author: https://github.com/rrmerugu
  description: Crawler that scrapes scrapinghub blogs

```