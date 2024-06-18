# models/amenity.py

from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

# Use getenv directly to check storage type
if getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    Base = object

class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
