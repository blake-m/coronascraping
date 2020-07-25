import requests


def run(file_path: str):
    # url = "http://localhost:5000/"
    url = "http://coronavirus_db_python_manager_1:5000"
    fin = open(file_path, 'rb')
    files = {'file': fin}
    try:
        r = requests.post(url, files=files)
        print(r.text)
    finally:
        fin.close()


if __name__ == "__main__":
    local_file_path = "/CoronaScraping/worldmeter.json"
    run(local_file_path)
