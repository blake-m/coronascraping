import logging

import requests


def run(file_path: str):
    url = "http://corona_db_manager:5000"
    fin = open(file_path, 'rb')
    files = {'file': fin}
    status_code = 500
    try:
        r = requests.post(url, files=files)
        logging.info("RESPONSE TEXT")
        logging.info(r.text)
        status_code = r.status_code
    finally:
        fin.close()
    return status_code


if __name__ == "__main__":
    local_file_path = "/CoronaScraping/worldmeter.json"
    run(local_file_path)
