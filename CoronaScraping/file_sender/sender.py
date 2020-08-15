import logging

import requests


def run(file_path: str) -> int:
    url = "http://corona_db_manager:5000"
    fin = open(file_path, 'rb')
    files = {'file': fin}
    r = requests.post(url, files=files)
    logging.info(r.text)
    fin.close()
    return r.status_code


if __name__ == "__main__":
    local_file_path = "/CoronaScraping/worldmeter.json"
    run(local_file_path)
