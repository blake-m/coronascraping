rm -f worldmeter.json
scrapy crawl worldmeter \
  -a path_selector_config="CoronaScraping/selector_config.json" \
  -o worldmeter.json
