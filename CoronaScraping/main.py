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
        # if not runner.check_if_run_today(spider_name) and runner.time_is_right():
        not_run_today = not runner.check_if_run_today(spider_name)
        time_is_right = runner.time_is_right()
        logging.info(f"The scraper hasn't been run today yet: {not_run_today}")
        logging.info(f"Time is right: {time_is_right}")
        if not_run_today and time_is_right:
            logging.info("Running CoronaScraper.")
            output_data_file_paths = runner.run_all()
            for spider_name, file_path in output_data_file_paths.items():
                response = sender.run(file_path)
                if str(response).startswith("2"):
                    runner.update_config_file_last_successful_run_date(spider_name)

        logging.info("Conditions to run scraper not met. Checking again in 1 hour.")
        seconds_in_minute = 60
        minutes_in_hour = 60
        sleep(seconds_in_minute * 1)  # check every hour


if __name__ == "__main__":
    main()
