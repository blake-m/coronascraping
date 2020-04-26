from scrapy import crawler
import json
import os
from scrapy.utils.project import get_project_settings


class WorldMeterSpidersExecutor:
    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as file:
                self.configuration = json.load(file)
        except FileNotFoundError as error:
            self.configuration = {}

        self.spiders = self.configuration.keys()
        print(self.spiders)

    def run_process(self, spider, output_file, spider_config):
        process = crawler.CrawlerProcess(settings={
            "FEEDS": output_file,
        })
        print(type(spider_config))
        print(spider_config)
        process.crawl(spider, spider_config)
        process.start()

    def run_all(self):
        from CoronaScraping.CoronaScraping.spiders.worldmeter import CountryGraphsDataExtractingSpider
        REAL_SPIDER = CountryGraphsDataExtractingSpider
        for spider_name in self.spiders:
            output_file = self.configuration[spider_name]["output_file"]
            spider_config = self.configuration[spider_name]["configuration"]
            self.run_process(REAL_SPIDER, output_file, spider_config)
