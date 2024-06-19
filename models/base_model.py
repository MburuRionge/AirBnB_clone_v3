#!/usr/bin/python3
"""
BaseModel Class of Models Module
"""

from os import getenv
import json
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


#Use getenv directly to check storage type
if getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initialization code """
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)
        if 'id' not in kwargs:
            self.id = str(uuid4())
        if 'created_at' not in kwargs:
            self.created_at = datetime.now()
        if 'updated-at' not in kwargs:
            self.updated_at = datetime.now()

    def __is_serializable(self, obj_v):
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except Exception:
            return False

    def bm_update(self, name, value):
        """
            updates the basemodel and sets the correct attributes
        """
        setattr(self, name, value)
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            self.save()

    def save(self):
        """updates attribute updated_at to current time"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns json representation of self"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def __str__(self):
        """returns string type representation of object instance"""
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
            deletes current instance from storage
        """
        models.storage.delete(self)
