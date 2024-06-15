#!/usr/bin/python3
"""
initialize the models package
"""
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    storage = DBStorage()
else:
    storage = FileStorage()
    storage.reload()
