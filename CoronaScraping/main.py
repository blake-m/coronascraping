import logging
import os
import sys
from time import sleep

import twisted
from scrapy.utils.log import configure_logging

from CoronaScraping import executor
from file_sender import sender

configure_logging(install_root_handler=True)
# logging.disable(50)  # CRITICAL = 50


def main():
    while True:
        config_path = "./CoronaScraping/config.json"
        runner = executor.WorldMeterSpidersExecutor(config_path)
        spider_name = "country_graphs_data_extracting_spider"
        # if not runner.check_if_run_today(spider_name) and runner.time_is_right():
        not_run_today = not runner.check_if_run_today(spider_name)
        time_is_right = runner.time_is_right()
        logging.info(f"The scraper hasn't been run today yet: {not_run_today}")
        logging.info(f"Time is right: {time_is_right}")
        if not_run_today and time_is_right:
            logging.info("Running CoronaScraper.")
            output_data_file_paths = runner.run_all()
            for spider_name, file_path in output_data_file_paths.items():
                status_code = sender.run(file_path)
                if str(status_code).startswith("2"):
                    logging.info(f"Status Code: {status_code}")
                    runner.update_config_file_last_successful_run_date(spider_name)
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            logging.info("Conditions to run scraper not met. Checking again in 1 hour.")
            seconds_in_minute = 60
            minutes_in_hour = 60
            sleep(seconds_in_minute * minutes_in_hour * 1)  # check every hour


if __name__ == "__main__":
    main()
