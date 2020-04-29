import time

import psycopg2


class DataBaseConstructor(object):
    def run(self):
        conn = psycopg2.connect(
            "dbname='postgres' user='postgres' host='coronavirus_db_1' password='postgres' port='5432'")
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS test;")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
        for i in range(10000):
            cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
                        (112521500, "abc'def"))
        cur.execute("SELECT * FROM test;")
        fetched = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        while True:
            # time.sleep(1)
            print(fetched)


def main():
    db = DataBaseConstructor()
    db.run()


if __name__ == "__main__":
    time.sleep(2)
    for i in range(100):
        print(i,
              "HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEee")

    main()
