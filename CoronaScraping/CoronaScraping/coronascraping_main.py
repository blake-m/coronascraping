from CoronaScraping.CoronaScraping import executor


def main():
    config_path = "/home/blake/PycharmProjects/Coronavirus/CoronaScraping/CoronaScraping/config.json"
    runner = executor.WorldMeterSpidersExecutor(config_path)
    runner.run_all()


if __name__ == "__main__":
    main()
