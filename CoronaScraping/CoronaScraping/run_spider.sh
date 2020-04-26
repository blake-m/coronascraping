rm -f worldmeter.json
scrapy crawl country_graphs_data_extracting_spider \
  -a selector_config= \
  -o worldmeter.json
