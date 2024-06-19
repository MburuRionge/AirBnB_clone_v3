from os import getenv

# Initialize storage_t first
storage_t = getenv('HBNB_TYPE_STORAGE')

# Import storage classes based on storage_t
if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
elif storage_t == "file":
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
else:
    raise ValueError("HBNB_TYPE_STORAGE environment variable is not set correctly. Expected 'db' or 'file'.")

# Reload the storage to deserialize the JSON file to objects
storage.reload()
