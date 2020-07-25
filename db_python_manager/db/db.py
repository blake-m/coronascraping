try:
    from db_python_manager.db.constructor import DataBaseConstructor
    from db_python_manager.db.methods import CRUDMethods
except ModuleNotFoundError:
    from db.constructor import DataBaseConstructor
    from db.methods import CRUDMethods


class DataBase(DataBaseConstructor, CRUDMethods):
    pass
