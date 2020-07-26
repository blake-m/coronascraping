from db import db
from data_source.inserter import Inserter
from data_source.transformers import JSONDataSource


def run(path):
    database = db.DataBase(db_name="postgres")
    database.create_db("coronavirus")
    database.connect("coronavirus")
    data_source = JSONDataSource(path)
    db_inserter = Inserter(data_source=data_source, db=database)
    db_inserter.insert(clean_start=False)
