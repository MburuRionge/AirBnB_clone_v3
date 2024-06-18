# models/city.py

from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

# Use getenv directly to check storage type
if getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    Base = object

class City(BaseModel, Base):
    __tablename__ = 'cities'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
    else:
        state_id = ""
        name = ""
