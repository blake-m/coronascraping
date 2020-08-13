import logging

import requests

def run(file_path: str):
    url = "http://corona_db_manager:5000"
    fin = open(file_path, 'rb')
    files = {'file': fin}
    try:
        r = requests.post(url, files=files)
        logging.info(r.text)
    finally:
        fin.close()


if __name__ == "__main__":
    local_file_path = "/CoronaScraping/worldmeter.json"
    run(local_file_path)
