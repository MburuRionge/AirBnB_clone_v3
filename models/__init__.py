# models/__init__.py

from os import getenv

# Initialize storage_t first
storage_t = getenv('HBNB_TYPE_STORAGE')

# Import storage classes based on storage_t
if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Reload the storage to deserialize the JSON file to objects
storage.reload()
