import datetime
import logging

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
            "FEEDS": {
                output_file_config["name"]: {"format": output_file_config["format"]},
            },
        })
        # TODO(blake): change this to a more elegant solution
        # you need to remove the previous file cause scrappy by default appends
        # to the file, not overwrites it
        output_file = output_file_config["name"]
        try:
            os.unlink(output_file)
        except FileNotFoundError:
            pass
        process.crawl(spider, spider_config)
        process.start()
        return output_file

    def run_all(self):
        from CoronaScraping.spiders.worldmeter import \
            CountryGraphsDataExtractingSpider
        REAL_SPIDER = CountryGraphsDataExtractingSpider
        output_files = {}
        for spider_name in self.spiders:
            output_file_config = self.configuration[spider_name]["output_file"]
            spider_config = self.configuration[spider_name]["configuration"]
            output_file = self.run_process(REAL_SPIDER, output_file_config,
                                           spider_config)
            output_files[spider_name] = output_file

        return output_files

    def check_if_run_today(self, spider_name) -> bool:
        spider_last_run_config = self.configuration[spider_name]["last_run"]
        last_run_date_str = spider_last_run_config["date"]
        last_run_date = datetime.datetime.strptime(last_run_date_str, "%Y-%m-%d %H:%M:%S.%f")
        last_run_date = last_run_date.date()
        todays_date = datetime.datetime.now().date()
        logging.info(f"LAST RUN: {last_run_date}\nTODAY'S DATE: {todays_date}")
        if last_run_date >= todays_date:
            logging.info(f"last_run_date >= todays_date - result: {last_run_date >= todays_date}")
            return True
        logging.info(
            f"last_run_date >= todays_date - result: {last_run_date >= todays_date}")

        return False

    def time_is_right(self):
        hour_now = datetime.datetime.now().hour
        logging.info("HOUR NOW IS ", hour_now)
        if hour_now >= 1 & hour_now <= 15:
            return True
        return False

    def update_config_file_last_successful_run_date(self, spider_name):
        spider_last_run_config = self.configuration[spider_name]["last_run"]
        spider_last_run_config["date"] = str(datetime.datetime.now())
        try:
            with open(self.config_path, 'w') as file:
                file.write(json.dumps(self.configuration, indent=4))
        except FileNotFoundError as error:
            print(error)
