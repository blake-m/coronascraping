import logging
import multiprocessing
import os
import time

from receiver import file_receiver
from db import db
from data_source.inserter import Inserter
from data_source.transformers import JSONDataSource


def db_process():
    time.sleep(5)
    database = db.DataBase(db_name="postgres")
    database.create_db("coronavirus")
    database.connect("coronavirus")
    # database.run_query("""DROP TABLE test;""", commit=True)
    # database.run_query("""CREATE TABLE test (
    #     id SERIAL,
    #     num INTEGER,
    #     DATA VARCHAR
    # );""", commit=True)
    # database.read_table()
    # database.add_n_to_table()
    # database.read_table()
    #
    # database.connect("coronavirus_local")
    # database.run_query("""DROP TABLE test;""", commit=True)
    # database.run_query("""CREATE TABLE test (
    #     id SERIAL,
    #     num INTEGER,
    #     DATA VARCHAR
    # );""", commit=True)
    # database.read_table()
    # database.add_n_to_table()
    # database.read_table()
    # database.reset_db("postgres")

    while True:
        time.sleep(5)
        time_now = time.time()
        logging.info(f"{time_now}: JSON data still not here.")
        if os.path.exists("receiver/received/worldmeter.json"):
            logging.info("JSON INFO ARRIVED. STARTING INSERTION.")
            break
    # TODO(blake): change to more elegant version ;)
    data_source = JSONDataSource(config_path="data_source/config.ini")
    db_inserter = Inserter(data_source=data_source, db=database)
    db_inserter.insert(clean_start=True)


def file_receiver_process():
    file_receiver.app.run(host='0.0.0.0', port=5000, debug=True)


def main():
    p1 = multiprocessing.Process(target=db_process)
    p2 = multiprocessing.Process(target=file_receiver_process)

    p1.start()
    p2.start()

    p1.join()
    p2.join()


if __name__ == "__main__":
    main()
