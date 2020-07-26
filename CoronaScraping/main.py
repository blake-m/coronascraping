import logging
from scrapy.utils.log import configure_logging


from CoronaScraping import executor
from file_sender import sender

configure_logging(install_root_handler=True)
logging.disable(50)  # CRITICAL = 50


def main():
    config_path = "./CoronaScraping/config.json"
    runner = executor.WorldMeterSpidersExecutor(config_path)
    spider_name = "country_graphs_data_extracting_spider"
    if not runner.check_if_run_successfully_in_last_24_hours(spider_name):
        output_data_file_paths = runner.run_all()
        for file_path in output_data_file_paths:
            sender.run(file_path)


if __name__ == "__main__":
    main()
