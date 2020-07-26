import datetime

from scrapy import crawler
import json
import os


class WorldMeterSpidersExecutor:
    def __init__(self, config_path):
        self.config_path = config_path
        try:
            with open(self.config_path, 'r') as file:
                self.configuration = json.load(file)
        except FileNotFoundError as error:
            self.configuration = {}

        self.spiders = self.configuration.keys()

    def run_process(self, spider, output_file_config, spider_config):
        process = crawler.CrawlerProcess(settings={
            "FEEDS": output_file_config,
        })
        # TODO(blake): change this to a more elegant solution
        # you need to remove the previous file cause scrappy by default appends
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
        output_files = []
        for spider_name in self.spiders:
            output_file_config = self.configuration[spider_name]["output_file"]
            spider_config = self.configuration[spider_name]["configuration"]
            output_file = self.run_process(REAL_SPIDER, output_file_config,
                                           spider_config)
            self.update_config_file_last_successful_run_date(spider_name)

            output_files.append(output_file)

        return output_files

    def check_if_run_successfully_in_last_24_hours(self, spider_name) -> bool:
        print(datetime.datetime.now())
        spider_last_run_config = self.configuration[spider_name]["last_run"]
        last_run_date_str = spider_last_run_config["date"]
        last_run_date = datetime.datetime.strptime(last_run_date_str, "%Y-%m-%d %H:%M:%S.%f")
        last_run_plus_one_day = last_run_date + datetime.timedelta(days=1)

        time_now = datetime.datetime.now()
        if last_run_plus_one_day > time_now:
            return True
        return False

    def run_all_if_not_run_today(self):
        spider_name = "country_graphs_data_extracting_spider"
        if not self.check_if_run_successfully_in_last_24_hours(spider_name):
            return self.run_all()
        return [self.configuration[spider_name]["output_file"]["name"]]

    def update_config_file_last_successful_run_date(self, spider_name):
        spider_last_run_config = self.configuration[spider_name]["last_run"]
        spider_last_run_config["date"] = str(datetime.datetime.now())
        try:
            with open(self.config_path, 'w') as file:
                file.write(json.dumps(self.configuration, indent=4))
        except FileNotFoundError as error:
            print(error)
