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

    def run_process(self, spider, output_file_config, spider_config):
        process = crawler.CrawlerProcess(settings={
            "FEEDS": output_file_config,
        })
        # TODO(blake): change this to a more elegant solution
        # you need to remove the previous file cause scrappy be default appends
        # to the file, not overwrites it
        output_file = list(output_file_config)[0]
        os.unlink(output_file)
        process.crawl(spider, spider_config)
        process.start()
        return output_file

    def run_all(self):
        from CoronaScraping.spiders.worldmeter import \
            CountryGraphsDataExtractingSpider
        REAL_SPIDER = CountryGraphsDataExtractingSpider
        print(self.spiders)
        print(self.configuration)
        output_files = []
        for spider_name in self.spiders:
            output_file_config = self.configuration[spider_name]["output_file"]
            spider_config = self.configuration[spider_name]["configuration"]
            output_file = self.run_process(REAL_SPIDER, output_file_config,
                                           spider_config)
            output_files.append(output_file)

        return output_files
