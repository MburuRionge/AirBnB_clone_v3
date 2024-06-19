#!/usr/bin/python3
""" Database engine """

from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """handles storage for database"""
    __engine = None
    __session = None

    """ handles longterm storage of all class indtances"""
    CNC = {
        'BaseModel': BaseModel,
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }

    def __init__(self):
        """ creates the engine self.__engine """
        self.__engine = create_engine(getenv('HBNB_MYSQL_USER'),
                                        pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns a dictionary of all objects """
        all_dict = {}
        if cls:
            if cls in self.CNC:
                objs = self.__session.query(self.CNC[cls]).all()
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    all_dict[key] = obj
        else:
            for c in self.CNC.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    all_dict[key] = obj
        return all_dict

    def new(self, obj):
        """ adds objects to current database session """
        self.__session.add(obj)

    def get(self, cls, id):
        """
        fetches specific object
        :param cls: class of object as string
        :param id: id of object as string
        :return: found object or None
        """
        if cls and id:
            if cls in classes.values() and isinstance(id, str):
                all_objects = self.all(cls)
                for key, value in all_objects.items():
                    if key.split('.')[1] == id:
                        return value
            else:
                return


        return

    def count(self, cls=None):
        """
        count of instancesparam cls: class return: number of instancce
        """
        if not cls:
            inst_of_all_cls = self.all()
            return len(inst_of_all_cls)
        for cls, value in classes.items():
            if cls == clas or cls == value:
                all_inst_of_prov_cls = self.all(cls)
                return len(all_inst_of_prov_cls)
        if cls not in classes.values():
            return
    def save(self):
        """ commits all changes of current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes obj from current database session if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ creates all tables in database & session from engine """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                        expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
            calls remove() on private session attribute (self.session)
        """
        self.__session.remove()
