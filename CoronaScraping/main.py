import logging
from time import sleep

from scrapy.utils.log import configure_logging

from CoronaScraping import executor
from file_sender import sender

configure_logging(install_root_handler=True)
# logging.disable(50)  # CRITICAL = 50


def main():
    config_path = "./CoronaScraping/config.json"
    runner = executor.WorldMeterSpidersExecutor(config_path)
    spider_name = "country_graphs_data_extracting_spider"
    while True:
        if not runner.check_if_run_today(spider_name) and runner.time_is_right():
            logging.info("Time is right. Running CoronaScraper.")
            output_data_file_paths = runner.run_all()
            for file_path in output_data_file_paths:
                sender.run(file_path)
        logging.info("Time is not right. Gonna check in an hour.")
        seconds_in_minute = 60
        minutes_in_hour = 60
        sleep(seconds_in_minute * minutes_in_hour * 1)  # check every hour


if __name__ == "__main__":
    main()
